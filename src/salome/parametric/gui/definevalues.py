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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from varrange_ui import Ui_VariableRange
from definevalues_ui import Ui_SampleDefinition


class VariableRange(QtGui.QWidget, Ui_VariableRange):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setupUi(self)


class DefineValuesFrame(QtGui.QWidget, Ui_SampleDefinition):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)
    self.varwidgets = {}

  def set_variables(self, varlist):
    previous_set = set(self.varwidgets.keys())
    new_set = set([var.name for var in varlist])
    var_to_remove = previous_set - new_set
    var_to_add = new_set - previous_set
    for var in var_to_remove:
      self.variablesRangesWidget.layout().removeWidget(self.varwidgets[var])
      self.varwidgets[var].close()
      del self.varwidgets[var]
    for var in var_to_add:
      varrange = VariableRange(self)
      varrange.nameLabel.setText(var)
      self.varwidgets[var] = varrange
      self.variablesRangesWidget.layout().addWidget(varrange)

  def set_ranges_from_param_study(self, param_study):
    for var in param_study.input_vars:
      varrange = VariableRange(self)
      varrange.nameLabel.setText(var.name)
      varrange.fromSpinBox.setValue(var.min)
      varrange.toSpinBox.setValue(var.max)
      varrange.stepSpinBox.setValue(var.step)
      self.varwidgets[var.name] = varrange
      self.variablesRangesWidget.layout().addWidget(varrange)

  def check_values(self):
    return True
