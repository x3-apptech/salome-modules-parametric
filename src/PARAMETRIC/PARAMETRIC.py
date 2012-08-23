# Copyright (C) 2012 EDF
#
# This file is part of SALOME PARAMETRIC module.
#
# SALOME PARAMETRIC module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SALOME PARAMETRIC module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SALOME PARAMETRIC module.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
import inspect
import traceback
import re
import copy

import salome
import SALOME
import SALOME_ModuleCatalog
import PARAMETRIC_ORB__POA
from SALOME_ComponentPy import SALOME_ComponentPy_i
from SALOME_DriverPy import SALOME_DriverPy_i
import SALOMERuntime
import loader
import pilot

from salome.kernel.logger import Logger
from salome.kernel import termcolor
logger = Logger("PARAMETRIC", color = termcolor.BLUE)
logger.setLevel(logging.DEBUG)

from salome.parametric.study import ParametricStudyEditor

class PARAMETRIC(PARAMETRIC_ORB__POA.PARAMETRIC_Gen, SALOME_ComponentPy_i, SALOME_DriverPy_i):

  lock = threading.Lock()

  def __init__(self, orb, poa, contID, containerName, instanceName, interfaceName):
    SALOME_ComponentPy_i.__init__(self, orb, poa, contID, containerName, instanceName, interfaceName, 0)
    SALOME_DriverPy_i.__init__(self, interfaceName)
    self.salome_runtime = None
    self.session_catalog = None

  def _raiseSalomeError(self):
    message = "Error in component %s running in container %s." % (self._instanceName, self._containerName)
    logger.exception(message)
    message += " " + traceback.format_exc()
    exc = SALOME.ExceptionStruct(SALOME.INTERNAL_ERROR, message,
                                 inspect.stack()[1][1], inspect.stack()[1][2])
    raise SALOME.SALOME_Exception(exc)

  def _get_salome_runtime(self):
    if self.salome_runtime is None:
      # Initialize runtime for YACS
      SALOMERuntime.RuntimeSALOME.setRuntime()
      self.salome_runtime = SALOMERuntime.getSALOMERuntime()
      mc = salome.naming_service.Resolve('/Kernel/ModulCatalog')
      if mc is None:
        raise Exception ("Internal error: Cannot find SALOME Module Catalog")
      ior = salome.orb.object_to_string(mc)
      self.session_catalog = self.salome_runtime.loadCatalog("session", ior)
      self.salome_runtime.addCatalog(self.session_catalog)
    return self.salome_runtime

  def _parse_entry(self, selected_value):
    """
    Find entry if selected_value is something like "name (entry)"
    """
    entry = selected_value
    match = re.search("\((.*)\)$", entry)
    if match is not None:
      entry = match.group(1)
    return entry

  def RunStudy(self, studyId, caseEntry):
    try:
      self.beginService("PARAMETRIC.RunStudy")

      PARAMETRIC.lock.acquire()
      salome.salome_init()
      PARAMETRIC.lock.release()
      
      # Get parametric study from the case in Salome study
      ed = ParametricStudyEditor(studyId)
      param_study = ed.get_parametric_study(caseEntry)

      # Generate YACS schema
      runtime = self._get_salome_runtime()
      proc = pilot.Proc("ParametricSchema")
      param_input_tc = runtime.getTypeCode("SALOME_TYPES/ParametricInput")
      if param_input_tc is None:
        raise Exception ("Internal error: No typecode found for type 'SALOME_TYPES/ParametricInput'")
      foreach = pilot.ForEachLoop("ForEach", param_input_tc)
      foreach.edGetNbOfBranchesPort().edInit(param_study.get_exec_param("NUMBER_OF_PARALLEL_COMPUTATIONS"))
      proc.edAddChild(foreach)

      solver_code = param_study.get_exec_param("SOLVER_CODE")
      solver_compo_inst = proc.createComponentInstance(solver_code)
      solver_compo_def = self.session_catalog._componentMap[solver_code]
      
      distrib_container = proc.createContainer("DistribContainer")
      distrib_container.setProperty("hostname", "localhost")
      solver_compo_inst.setContainer(distrib_container)

      init_solver = solver_compo_def._serviceMap["Init"].clone(None)
      init_solver.setComponent(solver_compo_inst)
      init_solver.getInputPort("studyID").edInit(studyId)
      entry = self._parse_entry(param_study.get_exec_param("DETERMINISTIC_CASE_ENTRY"))
      init_solver.getInputPort("detCaseEntry").edInit(entry)
      foreach.edSetInitNode(init_solver)

      exec_solver = solver_compo_def._serviceMap["Exec"].clone(None)
      exec_solver.setComponent(solver_compo_inst)
      foreach.edSetNode(exec_solver)

      finalize_solver = solver_compo_def._serviceMap["Finalize"].clone(None)
      finalize_solver.setComponent(solver_compo_inst)
      foreach.edSetFinalizeNode(finalize_solver)

      param_output_tc = runtime.getTypeCode("SALOME_TYPES/ParametricOutput")
      if param_output_tc is None:
        raise Exception ("Internal error: No typecode found for type 'SALOME_TYPES/ParametricOutput'")
      seq_param_output_tc = proc.createSequenceTc("", "seq_param_output", param_output_tc)
      aggregator = runtime.createScriptNode(SALOMERuntime.PythonNode.KIND, "Aggregator")
      aggregator_input_port = aggregator.edAddInputPort("results", seq_param_output_tc)
      proc.edAddChild(aggregator)

      #proc.edAddLink(init_data_output_port, foreach.edGetSeqOfSamplesPort())
      proc.edAddLink(foreach.edGetSamplePort(), exec_solver.getInputPort("paramInput"))
      proc.edAddCFLink(foreach, aggregator)
      proc.edAddLink(exec_solver.getOutputPort("paramOutput"), aggregator_input_port)

      # Set input data
      if param_study.data is None:
        param_study.generate_data()
      
      seqsamples = []
      refsample = {"inputVarList": [],
                   "outputVarList": [],
                   "inputValues": [[[]]],
                   "specificParameters": [],
                  }
      for varname in param_study.output_vars:
        refsample["outputVarList"].append(varname)

      for i in range(param_study.datasize):
        sample = copy.deepcopy(refsample)
        for var in param_study.input_vars:
          sample["inputVarList"].append(var.name)
          sample["inputValues"][0][0].append([param_study.data[var.name][i]])
        seqsamples.append(sample)
      foreach.edGetSeqOfSamplesPort().edInitPy(seqsamples)

      logger.debug("Checking validity...")
      if not proc.isValid():
        raise Exception("The schema is not valid and can not be executed.")
      
      logger.debug("Checking consistency...")
      info = pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
      proc.checkConsistency(info)
      if info.areWarningsOrErrors():
        logger.error(info.getGlobalRepr())
        raise Exception("The schema is not consistent and can not be executed.")
      logger.debug("Schema validated")
  
      # Launch computation
      executor = pilot.ExecutorSwig()
      executor.RunPy(proc)
      state = proc.getEffectiveState()
      if proc.getEffectiveState() != pilot.DONE:
        msg = proc.getErrorReport()
        if msg != "":
          raise Exception("YACS schema execution ended with errors:\n%s" % msg)
        else:
          raise Exception("YACS schema execution failed. No error report available.")

      # Get output values
      seqresults = aggregator.getInputPort("results").getPyObj()
      for varname in param_study.output_vars:
        param_study.data[varname] = []
      param_study.data["__ERROR_MESSAGE__"] = []

      for result in seqresults:
        if result["returnCode"] == 0:
          valuelist = result["outputValues"][0][0]
          if len(valuelist) != len(param_study.output_vars):
            raise Exception("Incoherent number of result variables")
          for i in range(len(valuelist)):
            param_study.data[param_study.output_vars[i]].append(valuelist[i][0])
          param_study.data["__ERROR_MESSAGE__"].append(None)
        else:
          for varname in param_study.output_vars:
            param_study.data[varname].append(None)
          param_study.data["__ERROR_MESSAGE__"].append(result["errorMessage"])

      # Save results in Salome study
      ed.set_parametric_study_at_entry(param_study, caseEntry)

      self.endService("PARAMETRIC.RunStudy")
    except:
      self._raiseSalomeError()
