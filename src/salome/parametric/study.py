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

from salome.kernel.studyedit import getStudyEditor

# module constants
MODULE_NAME = "PARAMETRIC"

COMPONENT_NAME = "Parametric"
COMPONENT_ICON = "PARAMETRIC_small.png"

PARAM_STUDY_ICON = "param_study.png"
PARAM_STUDY_TYPE_ID = 1

def jdc_to_dict(jdc, command_list):
    """
    This tricky function transforms a JdC with a single command into a
    dictionary that can be used more easily from a Python context (thanks to
    M. Courtois and G. Boulant).
    """
    context = {}
    for command in command_list:
        context[command] = _args_to_dict
    exec "parameters = " + jdc.strip() in context
    return context['parameters']

def _args_to_dict(**kwargs):
    return kwargs

class ParametricStudyEditor:
  """
  This class provides utility methods to edit the component "Parametric" in
  the study. The parameter `studyId` defines the ID of the study to edit. If
  it is :const:`None`, the edited study will be the current study.
  """
  def __init__(self, study_id = None):
    self.editor = getStudyEditor(study_id)
    self.param_comp = None

  def find_or_create_param_component(self):
    """
    Find the component "Parametric" or create it if none is found
    :return: the SComponent found or created.
    """
    if self.param_comp is None:
      self.param_comp = self.editor.findOrCreateComponent(MODULE_NAME, COMPONENT_NAME, COMPONENT_ICON)
    return self.param_comp

  def add_parametric_study(self, parametric_study):
    self.find_or_create_param_component()
    sobj = self.editor.createItem(self.param_comp, "__NEW_STUDY__")
    self._set_sobj(parametric_study, sobj)

  def set_parametric_study_at_entry(self, parametric_study, entry):
    sobj = self.editor.study.FindObjectID(entry)
    self._set_sobj(parametric_study, sobj)

  def _set_sobj(self, parametric_study, sobj):
    self.editor.setItem(sobj,
                        name = parametric_study.get_exec_param("PARAMETRIC_STUDY_NAME"),
                        comment = cPickle.dumps(parametric_study),
                        icon = PARAM_STUDY_ICON,
                        typeId = PARAM_STUDY_TYPE_ID)

  def get_parametric_study(self, entry):
    sobj = self.editor.study.FindObjectID(entry)
    if sobj is None or self.editor.getTypeId(sobj) != PARAM_STUDY_TYPE_ID:
      raise Exception("No valid parametric study at entry %s" % entry)
    param_study = cPickle.loads(sobj.GetComment())
    param_study.entry = entry
    return param_study


class ParametricVariable:

  def __init__(self, name, min = None, max = None, step = None):
    self.name = name
    self.min = min
    self.max = max
    self.step = step


class ParametricStudy:

  def __init__(self):
    self.input_vars = []
    self.output_vars = []
    self.exec_params = None
    self.data = None
    self.datasize = 0
    self._value_dict = None
    self.entry = None

  def add_input_variable(self, var):
    self.input_vars.append(var)

  def add_output_variable(self, varname):
    self.output_vars.append(varname)

  def set_exec_params(self, params):
    self.exec_params = params

  def get_exec_param(self, name):
    param_dict = jdc_to_dict(self.exec_params, ["EXECUTION_PARAMETERS"])
    return param_dict[name]
  
  def generate_data(self):
    self.data = {}
    self.datasize = 0
    for var in self.input_vars:
      self.data[var.name] = []
    self._value_dict = {}
    self._fill_data(self.input_vars)

  def _fill_data(self, remaining_var_list):
    if len(remaining_var_list) == 0:
      for (name, value) in self._value_dict.iteritems():
        self.data[name].append(value)
      self.datasize += 1
    else:
      var = remaining_var_list[0]
      next_var_list = remaining_var_list[1:]
      for value in numpy.arange(var.min, var.max, var.step):
        self._value_dict[var.name] = value
        self._fill_data(next_var_list)

  def export_data_to_csv_file(self, filepath, sep = ","):
    if self.data is None:
      raise Exception("Parametric study does not contain any data")
    f = open(filepath, "w")
    
    # Header
    for invar in self.input_vars:
      f.write(invar.name + sep)
    for outvarname in self.output_vars:
      f.write(outvarname + sep)
    f.write("Error message\n")
    
    # Data
    for i in range(self.datasize):
      for invar in self.input_vars:
        f.write(self._format_value(self.data[invar.name][i]) + sep)
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
