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

import os
import logging

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import salome
import SALOME

# Get SALOME PyQt interface
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from salome.kernel.studyedit import getStudyEditor, getActiveStudyId
from salome.kernel.logger import Logger
from salome.kernel import termcolor
logger = Logger("PARAMETRICGUI", color = termcolor.GREEN_FG)
#logger.setLevel(logging.ERROR)
from salome.kernel.parametric import study_exchange_vars

import PARAMETRIC
from salome.parametric.gui.mainpanel import MainPanel
from salome.parametric.study import ParametricStudyEditor

################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################

class GUIcontext:
  # menus/toolbars/actions IDs
  PARAMETRIC_MENU = 0
  CREATE_PARAMETRIC_STUDY = 1
  RUN_PARAMETRIC_STUDY = 2
  EXPORT_DATA_TO_CSV = 3
  EDIT_PARAMETRIC_STUDY = 4

  # constructor
  def __init__( self ):
    # create top-level menu
    mid = sgPyQt.createMenu("Parametric", -1, GUIcontext.PARAMETRIC_MENU, sgPyQt.defaultMenuGroup())
    # create toolbar
    tid = sgPyQt.createTool("Parametric")
    # create actions and fill menu and toolbar with actions
    a = sgPyQt.createAction(GUIcontext.CREATE_PARAMETRIC_STUDY,
                            "Create parametric study",
                            "Create parametric study",
                            "Create a new parametric study",
                            "new_param_study.png")
    sgPyQt.createMenu( a, mid )
    sgPyQt.createTool( a, tid )

    # Actions for popup menus
    sgPyQt.createAction(GUIcontext.RUN_PARAMETRIC_STUDY,
                        "Run parametric study",
                        "Run parametric study",
                        "Run the selected parametric study",
                        "run_param_study.png")

    sgPyQt.createAction(GUIcontext.EXPORT_DATA_TO_CSV,
                        "Export data to CSV file",
                        "Export data to CSV file",
                        "Export data to CSV file",
                        "export_to_csv_file.png")

    sgPyQt.createAction(GUIcontext.EDIT_PARAMETRIC_STUDY,
                        "Edit parametric study",
                        "Edit parametric study",
                        "Edit the selected parametric study",
                        "edit_param_study.png")

################################################
# Global variables
################################################

# study-to-context map
__study2context__   = {}
# current context
__current_context__ = None

################################################
# Internal methods
################################################

###
# get current GUI context
###
def _getContext():
  global __current_context__
  return __current_context__

###
# set and return current GUI context
# study ID is passed as parameter
###
def _setContext( studyID ):
  global __study2context__, __current_context__
  if not __study2context__.has_key(studyID):
    __study2context__[studyID] = GUIcontext()
  __current_context__ = __study2context__[studyID]
  return __current_context__

################################################
# Callback functions

# called when module is initialized
# return map of popup windows to be used by the module
def windows():
  wm = {}
  wm[SalomePyQt.WT_ObjectBrowser] = Qt.LeftDockWidgetArea
  return wm

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
  ctx = _setContext(getActiveStudyId())
  return True

# called when module is deactivated
def deactivate():
  pass

# called when active study is changed
# active study ID is passed as parameter
def activeStudyChanged(studyID):
  ctx = _setContext(studyID)

# called when popup menu is invoked
# popup menu and menu context are passed as parameters
def createPopupMenu(popup, context):
  logger.debug("createPopupMenu(): context = %s" % context)
  ed = getStudyEditor()
  _setContext(ed.studyId)
  if salome.sg.SelectedCount() == 1:
    # one object is selected
    sobj = ed.study.FindObjectID(salome.sg.getSelected(0))
    selectedType = ed.getTypeId(sobj)
    logger.debug("Selected type: %s" % selectedType)
    if selectedType == salome.parametric.study.PARAM_STUDY_TYPE_ID:
      popup.addAction(sgPyQt.action(GUIcontext.EDIT_PARAMETRIC_STUDY))
      popup.addAction(sgPyQt.action(GUIcontext.RUN_PARAMETRIC_STUDY))
      popup.addAction(sgPyQt.action(GUIcontext.EXPORT_DATA_TO_CSV))

# process GUI action
def OnGUIEvent( commandID ) :
  logger.debug("OnGUIEvent: commandID = %d" % commandID)
  if dict_command.has_key( commandID ):
    command = dict_command[commandID]
    try:
      command()
    except:
      logger.exception("Error while running command %s" % command)
  else:
    logger.error("The command %d is not implemented" % commandID)


################################################
# GUI actions implementation

def new_study():
  panel = MainPanel()
  panel.new_study()

def edit_study():
  study_id = sgPyQt.getStudyId()
  entry = salome.sg.getSelected(0)
  ed = ParametricStudyEditor(study_id)
  panel = MainPanel()
  panel.edit_study(ed.get_parametric_study(entry))

def run_study():
  qapp = QtGui.QApplication
  try:
    qapp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    study_id = sgPyQt.getStudyId()
    entry = salome.sg.getSelected(0)
    engine = salome.lcc.FindOrLoadComponent("ParametricContainer", "PARAMETRIC")
    engine.RunStudy(study_id, entry)
    qapp.restoreOverrideCursor()
  except SALOME.SALOME_Exception, exc:
    qapp.restoreOverrideCursor()
    logger.exception("An error happened while trying to run parametric study.")
    QtGui.QMessageBox.critical(sgPyQt.getDesktop(),
        qapp.translate("run_study", "Error"),
        qapp.translate("run_study", "An error happened while trying to run parametric study: %s" % exc.details.text))
  except Exception, exc:
    qapp.restoreOverrideCursor()
    logger.exception("An error happened while trying to run parametric study.")
    QtGui.QMessageBox.critical(sgPyQt.getDesktop(),
        qapp.translate("run_study", "Error"),
        qapp.translate("run_study", "An error happened while trying to run parametric study: %s" % exc))

def export_to_csv():
  qapp = QtGui.QApplication
  filename = QtGui.QFileDialog.getSaveFileName(sgPyQt.getDesktop(),
                                               qapp.translate("export_to_csv", "Export data to CSV file"),
                                               filter = qapp.translate("export_to_csv", "CSV files (*.csv)"))
  if filename is not None and len(filename) > 0:
    try:
        qapp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        study_id = sgPyQt.getStudyId()
        entry = salome.sg.getSelected(0)
        ed = ParametricStudyEditor(study_id)
        param_study = ed.get_parametric_study(entry)
        param_study.export_data_to_csv_file(filename)
        qapp.restoreOverrideCursor()
    except Exception, exc:
      qapp.restoreOverrideCursor()
      logger.exception("Export to CSV file failed")
      QtGui.QMessageBox.critical(sgPyQt.getDesktop(),
        qapp.translate("export_to_csv", "Error"),
        qapp.translate("export_to_csv", "Export to CSV file failed: %s" % exc))

# ----------------------- #
dict_command = {
  GUIcontext.CREATE_PARAMETRIC_STUDY: new_study,
  GUIcontext.RUN_PARAMETRIC_STUDY: run_study,
  GUIcontext.EXPORT_DATA_TO_CSV: export_to_csv,
  GUIcontext.EDIT_PARAMETRIC_STUDY: edit_study
}
