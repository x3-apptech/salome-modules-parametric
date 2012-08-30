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

from PyQt4 import QtGui, QtCore

import salome
from salome.kernel.studyedit import getStudyEditor

from salome.parametric.study import ParametricStudy
from execparams_ui import Ui_ExecParams


class ExecParamsFrame(QtGui.QWidget, Ui_ExecParams):

  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)
    self.connect(self.selectFromSalomeButton, QtCore.SIGNAL("clicked()"), self.select_from_salome)
    self.case_entry = None
  
  def select_from_salome(self):
    nb_entries = salome.sg.SelectedCount()
    if nb_entries < 1:
      QtGui.QMessageBox.information(self, self.tr("Select from Salome"),
                                    self.tr("Please select an entry in Salome Object Browser"))
    elif nb_entries > 1:
      QtGui.QMessageBox.information(self, self.tr("Select from Salome"),
                                    self.tr("Only one entry must be selected in Salome Object Browser"))
    else:
      self.set_case_entry(salome.sg.getSelected(0))

  def set_case_entry(self, entry):
    self.case_entry = entry
    self.caseEntryLE.setText(getStudyEditor().study.FindObjectID(entry).GetName() + " (" + entry + ")")

  def gui_to_study(self, param_study):
    if self.salomeComponentRB.isChecked():
      param_study.solver_code_type = ParametricStudy.SALOME_COMPONENT
      param_study.salome_component_name = str(self.componentNameLE.text())
      param_study.solver_case_entry = self.case_entry
    else:
      param_study.solver_code_type = ParametricStudy.PYTHON_SCRIPT
      param_study.python_script = str(self.pythonScriptTE.text())
    param_study.name = str(self.studyNameLE.text())
    param_study.nb_parallel_computations = self.nbParallelSB.value()

  def study_to_gui(self, param_study):
    if param_study.solver_code_type == ParametricStudy.SALOME_COMPONENT:
      self.salomeComponentRB.setChecked(True)
      self.componentNameLE.setText(param_study.salome_component_name)
      self.set_case_entry(param_study.solver_case_entry)
    else:
      self.pythonScriptRB.setChecked(True)
      self.pythonScriptTE.setText(param_study.python_script)
    self.studyNameLE.setText(param_study.name)
    self.nbParallelSB.setValue(param_study.nb_parallel_computations)
