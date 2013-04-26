# Copyright (C) 2012-2013 EDF
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
from execparams import ExecParamsFrame
from salome.parametric import ParametricStudy, ParametricStudyEditor


class Wizard(QtGui.QWidget, Ui_Wizard):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)
    self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.next_step)
    self.connect(self.previousButton, QtCore.SIGNAL("clicked()"), self.previous_step)
    self.connect(self.OKButton, QtCore.SIGNAL("clicked()"), self.validate)
    self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.close)
    self.step_labels = []
    for i in range(len(self.step_texts)):
      self.step_labels.append(QtGui.QLabel(self))
      self.stepLayout.addWidget(self.step_labels[i])
    self.select_vars_frame = SelectVarsFrame(self)
    self.define_values_frame = DefineValuesFrame(self)
    self.exec_params_frame = ExecParamsFrame(self)
    self.step_frames = [self.select_vars_frame,
                        self.define_values_frame,
                        self.exec_params_frame]
    for frame in self.step_frames:
      self.innerFrame.layout().addWidget(frame)
    self.curstep = 0
    self.step()
    self.entry = None
    self.view_id = None

  def next_step(self):
    if self.step_frames[self.curstep].check_values():
      self.curstep += 1
      self.step()

  def previous_step(self):
    if self.step_frames[self.curstep].check_values():
      self.curstep -= 1
      self.step()

  def step(self):
    if self.step_methods[self.curstep] is not None:
      self.step_methods[self.curstep](self)
    for i in range(len(self.step_texts)):
      if i == self.curstep:
        self.step_labels[i].setText("<b>" + self.tr(self.step_texts[i]) + "</b>")
        self.step_frames[i].show()
      else:
        self.step_labels[i].setText(self.tr(self.step_texts[i]))
        self.step_frames[i].hide()
    if self.curstep == 0:
      self.previousButton.hide()
    else:
      self.previousButton.show()
    if self.curstep == len(self.step_texts)-1:
      self.nextButton.hide()
      self.OKButton.show()
    else:
      self.nextButton.show()
      self.OKButton.hide()

  def define_values(self):
    exchange_vars = self.select_vars_frame.getSelectedExchangeVariables()
    self.define_values_frame.set_variables(exchange_vars.inputVarList)
    self.define_values_frame.set_pyscript_label_from_vars(exchange_vars)

  def set_pyscript_label(self):
    exchange_vars = self.select_vars_frame.getSelectedExchangeVariables()
    self.exec_params_frame.set_pyscript_label_from_vars(exchange_vars)

  def validate(self):
    try:
      if not self.step_frames[self.curstep].check_values():
        return
      param_study = ParametricStudy()
      for frame in self.step_frames:
        frame.gui_to_study(param_study)
  
      # Save to Salome study
      ed = ParametricStudyEditor()
      if self.entry is not None:
        ed.set_parametric_study_at_entry(param_study, self.entry)
      else:
        ed.add_parametric_study(param_study)
      salome.sg.updateObjBrowser(0)
      self.close()
    except Exception, exc:
      QtGui.QMessageBox.critical(self, self.tr("Error"), str(exc))

  def set_study(self, param_study):
    self.entry = param_study.entry
    for frame in self.step_frames:
      frame.study_to_gui(param_study)

  def close(self):
    QtGui.QWidget.close(self)
    if self.view_id is not None:
      sgPyQt.closeView(self.view_id)

  step_texts = ["Step 1: Parametric Variables",
                "Step 2: Sample Definition",
                "Step 3: Execution Parameters"]

  step_methods = [None,
                  define_values,
                  set_pyscript_label]
