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

from PyQt4 import QtCore, QtGui

import salome
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from wizard_ui import Ui_Wizard
from selectvars import SelectVarsFrame
from definevalues import DefineValuesFrame
from salome.parametric.gui.eficas.appli import EficasFrame
from salome.parametric.study import ParametricVariable, ParametricStudy, ParametricStudyEditor


class Wizard(QtGui.QWidget, Ui_Wizard):
  
  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)
    self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.next_step)
    self.connect(self.previousButton, QtCore.SIGNAL("clicked()"), self.previous_step)
    self.connect(self.OKButton, QtCore.SIGNAL("clicked()"), self.validate)
    self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.close)
    self.select_vars_frame = SelectVarsFrame(self)
    self.innerFrame.layout().addWidget(self.select_vars_frame)
    self.define_values_frame = DefineValuesFrame(self)
    self.innerFrame.layout().addWidget(self.define_values_frame)
    self.exec_params_frame = EficasFrame(self)
    self.innerFrame.layout().addWidget(self.exec_params_frame)
    self.reset_step()
    self.step = 1
    self.step_methods[self.step](self)
    self.entry = None
    self.view_id = None

  def next_step(self):
    self.reset_step()
    self.step += 1
    self.step_methods[self.step](self)

  def previous_step(self):
    self.reset_step()
    self.step -= 1
    self.step_methods[self.step](self)

  def reset_step(self):
    self.select_vars_frame.hide()
    self.define_values_frame.hide()
    self.exec_params_frame.hide()
    self.OKButton.hide()
    self.previousButton.show()
    self.nextButton.show()

  def define_variables(self):
    self.select_vars_frame.show()
    self.previousButton.hide()

  def define_values(self):
    exchange_vars = self.select_vars_frame.getSelectedExchangeVariables()
    self.define_values_frame.set_variables(exchange_vars.inputVarList)
    self.define_values_frame.show()

  def define_exec_params(self):
    self.exec_params_frame.show()
    self.nextButton.hide()
    self.OKButton.show()
  
  def validate(self):
    param_study = ParametricStudy()
    # Input variables
    for (name, range_widget) in self.define_values_frame.varwidgets.iteritems():
      min = range_widget.fromSpinBox.value()
      max = range_widget.toSpinBox.value()
      step = range_widget.stepSpinBox.value()
      var = ParametricVariable(name, min, max, step)
      param_study.add_input_variable(var)
    # Output variables
    exch_vars = self.select_vars_frame.getSelectedExchangeVariables()
    for outvar in exch_vars.outputVarList:
      param_study.add_output_variable(outvar.name)
    # Execution parameters
    exec_params_comm = self.exec_params_frame.get_text_jdc()
    param_study.set_exec_params(exec_params_comm)
    # Save to Salome study
    ed = ParametricStudyEditor()
    if self.entry is not None:
      ed.set_parametric_study_at_entry(param_study, self.entry)
    else:
      ed.add_parametric_study(param_study)
    salome.sg.updateObjBrowser(0)
    self.close()

  def set_study(self, param_study):
    self.entry = param_study.entry
    self.select_vars_frame.set_vars_from_param_study(param_study)
    self.define_values_frame.set_ranges_from_param_study(param_study)
    self.exec_params_frame.set_exec_params_from_param_study(param_study)

  def close(self):
    QtGui.QWidget.close(self)
    if self.view_id is not None:
      sgPyQt.closeView(self.view_id)

  step_methods = {1: define_variables,
                  2: define_values,
                  3: define_exec_params}
