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
import copy
import cPickle
import tempfile
import os

import salome
import SALOME
import SALOME_ModuleCatalog
import PARAMETRIC_ORB__POA
from SALOME_ComponentPy import SALOME_ComponentPy_i
from SALOME_DriverPy import SALOME_DriverPy_i
import SALOMERuntime
import pilot

from salome.kernel.studyedit import getStudyEditor
from salome.kernel.logger import Logger
from salome.kernel import termcolor
logger = Logger("PARAMETRIC", color = termcolor.BLUE)
logger.setLevel(logging.DEBUG)

from salome.parametric import PARAM_STUDY_TYPE_ID, ParametricStudy, parse_entry
from salome.parametric.persistence import load_param_study_dict, save_param_study_dict

# module constants
MODULE_NAME = "PARAMETRIC"

COMPONENT_NAME = "Parametric"
COMPONENT_ICON = "PARAMETRIC_small.png"

PARAM_STUDY_ICON = "param_study.png"

start_script = """
from salome.kernel.parametric.pyscript_utils import \
    create_input_dict, create_normal_parametric_output, create_error_parametric_output

try:
  globals().update(create_input_dict({}, paramInput))
  
  ### Start of user code
  
"""

end_script = """  
  ### End of user code

  output_dict = {}
  for output_var in paramInput["outputVarList"]:
    if globals().has_key(output_var):
      output_dict[output_var] = globals()[output_var]
    else:
      raise Exception("User Python script has not created variable %s" % output_var)

  paramOutput = create_normal_parametric_output(output_dict, paramInput)

except Exception, exc:
  paramOutput = create_error_parametric_output(str(exc))
"""

class PARAMETRIC(PARAMETRIC_ORB__POA.PARAMETRIC_Gen, SALOME_ComponentPy_i, SALOME_DriverPy_i):

  lock = threading.Lock()

  def __init__(self, orb, poa, contID, containerName, instanceName, interfaceName):
    SALOME_ComponentPy_i.__init__(self, orb, poa, contID, containerName, instanceName, interfaceName, 0)
    SALOME_DriverPy_i.__init__(self, interfaceName)
    self.param_comp = {}
    self.param_study_dict = {}
    self.salome_runtime = None
    self.session_catalog = None

  def _raiseSalomeError(self):
    message = "Error in component %s running in container %s." % (self._instanceName, self._containerName)
    logger.exception(message)
    message += " " + traceback.format_exc()
    exc = SALOME.ExceptionStruct(SALOME.INTERNAL_ERROR, message,
                                 inspect.stack()[1][1], inspect.stack()[1][2])
    raise SALOME.SALOME_Exception(exc)

  def _find_or_create_param_component(self, salomeStudyID):
    """
    Find the component "Parametric" or create it if none is found
    :return: the SComponent found or created.
    """
    if salomeStudyID not in self.param_comp:
      ed = getStudyEditor(salomeStudyID)
      self.param_comp[salomeStudyID] = ed.findOrCreateComponent(MODULE_NAME, COMPONENT_NAME, COMPONENT_ICON)
    return self.param_comp[salomeStudyID]

  def _set_param_study_sobj(self, parametric_study, salomeStudyID, sobj):
    getStudyEditor(salomeStudyID).setItem(sobj,
                                          name = parametric_study.name,
                                          icon = PARAM_STUDY_ICON,
                                          typeId = PARAM_STUDY_TYPE_ID)
    if salomeStudyID not in self.param_study_dict:
      self.param_study_dict[salomeStudyID] = {}
    entry = sobj.GetID()
    self.param_study_dict[salomeStudyID][entry] = parametric_study

  def AddParametricStudy(self, parametricStudy, salomeStudyID):
    try:
      self.beginService("PARAMETRIC.AddParametricStudy")
      param_study = cPickle.loads(parametricStudy)
      param_comp = self._find_or_create_param_component(salomeStudyID)
      sobj = getStudyEditor(salomeStudyID).createItem(param_comp, "__NEW_STUDY__")
      self._set_param_study_sobj(param_study, salomeStudyID, sobj)
      self.endService("PARAMETRIC.AddParametricStudy")
    except:
      self._raiseSalomeError()

  def _set_parametric_study(self, param_study, salomeStudyID, entry):
    sobj = getStudyEditor(salomeStudyID).study.FindObjectID(entry)
    self._set_param_study_sobj(param_study, salomeStudyID, sobj)

  def SetParametricStudy(self, parametricStudy, salomeStudyID, entry):
    try:
      self.beginService("PARAMETRIC.SetParametricStudy")
      param_study = cPickle.loads(parametricStudy)
      self._set_parametric_study(param_study, salomeStudyID, entry)
      self.endService("PARAMETRIC.SetParametricStudy")
    except:
      self._raiseSalomeError()

  def _get_parametric_study(self, salomeStudyID, entry):
    if salomeStudyID not in self.param_study_dict or entry not in self.param_study_dict[salomeStudyID]:
      raise Exception("No valid parametric study at entry %s" % entry)
    param_study = self.param_study_dict[salomeStudyID][entry]
    param_study.entry = entry
    return param_study

  def GetParametricStudy(self, salomeStudyID, entry):
    try:
      self.beginService("PARAMETRIC.GetParametricStudy")
      param_study = self._get_parametric_study(salomeStudyID, entry)
      return cPickle.dumps(param_study)
      self.endService("PARAMETRIC.GetParametricStudy")
    except:
      self._raiseSalomeError()

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

  def RunStudy(self, salomeStudyID, entry):
    try:
      self.beginService("PARAMETRIC.RunStudy")

      PARAMETRIC.lock.acquire()
      salome.salome_init()
      PARAMETRIC.lock.release()
      
      # Get parametric study from the case in Salome study
      param_study = self._get_parametric_study(salomeStudyID, entry)

      # Generate YACS schema
      runtime = self._get_salome_runtime()
      proc = pilot.Proc("ParametricSchema")
      param_input_tc = runtime.getTypeCode("SALOME_TYPES/ParametricInput")
      if param_input_tc is None:
        raise Exception ("Internal error: No typecode found for type 'SALOME_TYPES/ParametricInput'")
      param_output_tc = runtime.getTypeCode("SALOME_TYPES/ParametricOutput")
      if param_output_tc is None:
        raise Exception ("Internal error: No typecode found for type 'SALOME_TYPES/ParametricOutput'")
      foreach = pilot.ForEachLoop("ForEach", param_input_tc)
      foreach.edGetNbOfBranchesPort().edInit(param_study.nb_parallel_computations)
      proc.edAddChild(foreach)
      
      distrib_container = proc.createContainer("DistribContainer")
      distrib_container.setProperty("hostname", "localhost")

      if param_study.solver_code_type == ParametricStudy.SALOME_COMPONENT:
        solver_code = param_study.salome_component_name
        solver_compo_inst = proc.createComponentInstance(solver_code)
        solver_compo_def = self.session_catalog._componentMap[solver_code]
        solver_compo_inst.setContainer(distrib_container)
  
        init_solver = solver_compo_def._serviceMap["Init"].clone(None)
        init_solver.setComponent(solver_compo_inst)
        init_solver.getInputPort("studyID").edInit(salomeStudyID)
        solver_case_entry = parse_entry(param_study.solver_case_entry)
        init_solver.getInputPort("detCaseEntry").edInit(solver_case_entry)
        foreach.edSetInitNode(init_solver)
  
        exec_solver = solver_compo_def._serviceMap["Exec"].clone(None)
        exec_solver.setComponent(solver_compo_inst)
        foreach.edSetNode(exec_solver)
  
        finalize_solver = solver_compo_def._serviceMap["Finalize"].clone(None)
        finalize_solver.setComponent(solver_compo_inst)
        foreach.edSetFinalizeNode(finalize_solver)
      else:
        exec_solver = runtime.createScriptNode(SALOMERuntime.PythonNode.KIND, "Exec")
        exec_solver.edAddInputPort("paramInput", param_input_tc)
        exec_solver.edAddOutputPort("paramOutput", param_output_tc)
        indented_user_script = ""
        for line in param_study.python_script.splitlines():
          indented_user_script += "  " + line + "\n"
        exec_script = start_script + indented_user_script + end_script
        exec_solver.setScript(exec_script)
        exec_solver.setExecutionMode("remote")
        exec_solver.setContainer(distrib_container)
        foreach.edSetNode(exec_solver)

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
      self._set_parametric_study(param_study, salomeStudyID, entry)

      self.endService("PARAMETRIC.RunStudy")
    except:
      self._raiseSalomeError()

  def Save(self, theComponent, theURL, isMultiFile):
    try:
      # Select parametric studies to save
      salomeStudyID = theComponent.GetStudy()._get_StudyId()
      componentEntry = theComponent.GetID()
      dict_to_save = {}
      if salomeStudyID in self.param_study_dict:
        for (entry, param_study) in self.param_study_dict[salomeStudyID].iteritems():
          if entry.startswith(componentEntry):
            dict_to_save[entry] = param_study
      
      if len(dict_to_save) > 0:
        # Save parametric studies in temporary file
        (fd, filename) = tempfile.mkstemp(prefix = "PARAMETRIC_", suffix = ".hdf")
        os.close(fd)
        save_param_study_dict(dict_to_save, filename)
        
        # Return the content of the temporary file as a byte sequence
        with open(filename) as f:
          buf = f.read()
        
        # Delete the temporary file
        #os.remove(filename)
        
        return buf
      else:
        return ""
    except:
      logger.exception("Error while trying to save study")
      return ""

  def Load(self, theComponent, theStream, theURL, isMultiFile):
    try:
      print "PARAMETRIC load"
      return 1
    except:
      logger.exception("Error while trying to load study")
      return 0
