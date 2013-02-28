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

import cPickle
import numpy

import salome
import SALOME
from salome.kernel.studyedit import getActiveStudyId
import PARAMETRIC

PARAM_STUDY_TYPE_ID = 1

class ParametricStudyEditor:
  """
  This class provides utility methods to edit the component "Parametric" in
  the study. The parameter `studyId` defines the ID of the study to edit. If
  it is :const:`None`, the edited study will be the current study.
  """
  def __init__(self, study_id = None):
    self.study_id = study_id
    if self.study_id is None:
      self.study_id = getActiveStudyId()
    self.engine = None

  def find_or_create_engine(self):
    """
    Find the engine "PARAMETRIC" or create it if none is found
    :return: the PARAMETRIC engine
    """
    if self.engine is None:
      self.engine = salome.lcc.FindOrLoadComponent("FactoryServer", "PARAMETRIC")
    return self.engine

  def add_parametric_study(self, parametric_study):
    engine = self.find_or_create_engine()
    pickled_param_study = cPickle.dumps(parametric_study)
    try:
      engine.AddParametricStudy(pickled_param_study, self.study_id)
    except SALOME.SALOME_Exception, exc:
      raise Exception(exc.details.text)

  def set_parametric_study_at_entry(self, parametric_study, entry):
    engine = self.find_or_create_engine()
    pickled_param_study = cPickle.dumps(parametric_study)
    try:
      engine.SetParametricStudy(pickled_param_study, self.study_id, entry)
    except SALOME.SALOME_Exception, exc:
      raise Exception(exc.details.text)

  def get_parametric_study(self, entry):
    engine = self.find_or_create_engine()
    try:
      pickled_param_study = engine.GetParametricStudy(self.study_id, entry)
    except SALOME.SALOME_Exception, exc:
      raise Exception(exc.details.text)
    param_study = cPickle.loads(pickled_param_study)
    return param_study


class VariableRange:

  def __init__(self, minval = None, maxval = None, step = None):
    self.min = minval
    self.max = maxval
    self.step = step


class ParametricStudy:
  
  SALOME_COMPONENT = 0
  PYTHON_SCRIPT = 1
  
  SAMPLE_VAR_RANGE = 0
  SAMPLE_PYTHON_SCRIPT = 1
  SAMPLE_CSV_FILE = 2

  def __init__(self):
    self.input_vars = []
    self.output_vars = []
    self.sample_definition_method = ParametricStudy.SAMPLE_VAR_RANGE
    self.sample_var_range = None
    self.sample_python_script = None
    self.sample_csv_file = None
    self.solver_code_type = ParametricStudy.SALOME_COMPONENT
    self.salome_component_name = None
    self.solver_case_entry = None
    self.python_script = None
    self.name = None
    self.nb_parallel_computations = 1
    self.data = None
    self.datasize = 0
    self._value_dict = None
    self.entry = None

  def set_variable_range(self, varname, varrange):
    if varname not in self.input_vars:
      raise Exception('Can\'t define range for variable "%s", which is not an input variable' % varname)
    if self.sample_var_range is None:
      self.sample_var_range = {}
    self.sample_var_range[varname] = varrange

  def generate_data(self):
    if self.sample_definition_method == ParametricStudy.SAMPLE_VAR_RANGE:
      self.generate_data_complete_sampling()
    else:
      raise Exception("This sample definition method is not implemented")

  def generate_data_complete_sampling(self):
    self.data = {}
    self.datasize = 0
    for varname in self.input_vars:
      self.data[varname] = []
    self._value_dict = {}
    self._fill_data_complete_sampling(self.input_vars)

  def _fill_data_complete_sampling(self, remaining_var_list):
    if len(remaining_var_list) == 0:
      for (name, value) in self._value_dict.iteritems():
        self.data[name].append(value)
      self.datasize += 1
    else:
      varname = remaining_var_list[0]
      next_var_list = remaining_var_list[1:]
      varrange = self.sample_var_range[varname]
      for value in numpy.arange(varrange.min, varrange.max, varrange.step):
        self._value_dict[varname] = value
        self._fill_data_complete_sampling(next_var_list)

  def export_data_to_csv_file(self, filepath, sep = ","):
    if self.data is None:
      raise Exception("Parametric study does not contain any data")
    f = open(filepath, "w")
    
    # Header
    for invarname in self.input_vars:
      f.write(invarname + sep)
    for outvarname in self.output_vars:
      f.write(outvarname + sep)
    f.write("Error message\n")
    
    # Data
    for i in range(self.datasize):
      for invarname in self.input_vars:
        f.write(self._format_value(self.data[invarname][i]) + sep)
      for outvarname in self.output_vars:
        f.write(self._format_value(self.data[outvarname][i]) + sep)
      f.write(self._format_value(self.data["__ERROR_MESSAGE__"][i]) + "\n")

    f.close()

  def _format_value(self, value):
    if value is None:
      val = ""
    else:
      val = unicode(value)
    return val.encode("utf-8")
