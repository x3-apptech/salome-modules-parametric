# Copyright (C) 2012-2015 EDF
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

import os
from PyQt4 import QtGui, QtCore

import salome
from salome.parametric import generate_job
from genjob_ui import Ui_GenJobDialog


class GenJobDialog(QtGui.QDialog, Ui_GenJobDialog):

  def __init__(self, parent, param_study):
    QtGui.QDialog.__init__(self, parent)
    self.setupUi(self)
    self.connect(self.dialogButtonBox, QtCore.SIGNAL("accepted()"), self.validate)
    self.connect(self.dialogButtonBox, QtCore.SIGNAL("rejected()"), self.close)
    self.connect(self.chooseResultDirectoryButton, QtCore.SIGNAL("clicked()"), self.choose_result_dir)
    self.resultStudyLE.setText(param_study.name.replace(" ", "_") + "_Result.hdf")
    self.resultDirectoryLE.setText(os.getcwd())
    
    # Populate resource combo box
    res_manager = salome.naming_service.Resolve("/ResourcesManager")
    res_params = salome.ResourceParameters()
    res_list = res_manager.GetFittingResources(res_params)
    self.resourceCB.addItems(res_list)
    
    self.param_study = param_study

  def choose_result_dir(self):
    directory = QtGui.QFileDialog.getExistingDirectory(self,
            directory = self.resultDirectoryLE.text(),
            options = QtGui.QFileDialog.ShowDirsOnly)
    if not directory.isNull():
      self.resultDirectoryLE.setText(directory)

  def validate(self):
    generate_job(self.param_study, str(self.resultStudyLE.text()),
                 str(self.resultDirectoryLE.text()), str(self.resourceCB.currentText()))
    self.close()
