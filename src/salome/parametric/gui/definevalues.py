# Copyright (C) 2012-2014 EDF
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from varrange_ui import Ui_VariableRange
from definevalues_ui import Ui_SampleDefinition

from salome.parametric import ParametricStudy, VariableRange

class VariableRangeWidget(QtGui.QWidget, Ui_VariableRange):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setupUi(self)


class DefineValuesFrame(QtGui.QWidget, Ui_SampleDefinition):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)
    self.connect(self.chooseCsvFileButton, QtCore.SIGNAL("clicked()"), self.choose_csv_file)
    self.varwidgets = {}
  
  def choose_csv_file(self):
    filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Load data from CSV file"),
                                                 filter = self.tr("CSV files (*.csv)"))
    if filename is not None and len(filename) > 0:
      self.csvFileLE.setText(filename)

  def set_variables(self, varlist):
    previous_set = set(self.varwidgets.keys())
    new_list = [var.name for var in varlist]
    var_to_remove = previous_set - set(new_list)
    for var in var_to_remove:
      self.variablesRangesWidget.layout().removeWidget(self.varwidgets[var])
      self.varwidgets[var].close()
      del self.varwidgets[var]
    for idx_var, var in enumerate(new_list):
      if var not in self.varwidgets:
        range_widget = VariableRangeWidget(self)
        range_widget.nameLabel.setText(var)
        self.varwidgets[var] = range_widget
        self.variablesRangesWidget.layout().insertWidget(idx_var, range_widget)

  def set_pyscript_label_from_vars(self, exchange_vars):
    input_var_names = [var.name for var in exchange_vars.inputVarList]
    text  = "This script must create a NumPy array of dimension (n, %d)" % len(input_var_names)
    text += " named <b>sample</b> where n is the number of points in the sample."
    if len(input_var_names) > 1:
      text += "<br>The order of the input variables (columns of the sample) must be"
      for i, var in enumerate(input_var_names):
        if i != 0:
          text += ","
        text += " <b>" + var + "</b>"
      text += "."
    self.pyscriptLabel.setText(text)

  def study_to_gui(self, param_study):
    if param_study.sample_definition_method == ParametricStudy.SAMPLE_VAR_RANGE:
      self.variableRangeRB.setChecked(True)
      for varname in param_study.input_vars:
        varrange = param_study.sample_var_range[varname]
        range_widget = VariableRangeWidget(self)
        range_widget.nameLabel.setText(varname)
        range_widget.fromSpinBox.setValue(varrange.min)
        range_widget.toSpinBox.setValue(varrange.max)
        range_widget.stepSpinBox.setValue(varrange.step)
        self.varwidgets[varname] = range_widget
        self.variablesRangesWidget.layout().addWidget(range_widget)
    elif param_study.sample_definition_method == ParametricStudy.SAMPLE_PYTHON_SCRIPT:
      self.pythonScriptRB.setChecked(True)
      self.pythonScriptTE.setText(param_study.sample_python_script)
    else:
      self.loadSampleRB.setChecked(True)
      self.csvFileLE.setText(param_study.sample_csv_file)

  def gui_to_study(self, param_study):
    if self.variableRangeRB.isChecked():
      param_study.sample_definition_method = ParametricStudy.SAMPLE_VAR_RANGE
      for (name, range_widget) in self.varwidgets.iteritems():
        minval = range_widget.fromSpinBox.value()
        maxval = range_widget.toSpinBox.value()
        step = range_widget.stepSpinBox.value()
        param_study.set_variable_range(name, VariableRange(minval, maxval, step))
    elif self.pythonScriptRB.isChecked():
      param_study.sample_definition_method = ParametricStudy.SAMPLE_PYTHON_SCRIPT
      param_study.sample_python_script = str(self.pythonScriptTE.toPlainText())
    else:
      param_study.sample_definition_method = ParametricStudy.SAMPLE_CSV_FILE
      param_study.sample_csv_file = str(self.csvFileLE.text())

  def check_values(self):
    return True
