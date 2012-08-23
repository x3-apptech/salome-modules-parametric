# -*- coding: utf-8 -*-
#
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
import sys
import re
import tempfile

from PyQt4.QtGui import QMessageBox

import salome
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from salome.kernel.logger import Logger
from salome.kernel import termcolor
logger = Logger("salome.openturns.eficas_yacs_schema.appli",
                color = termcolor.GREEN_FG)
from salome.kernel.studyedit import getStudyEditor

import eficasSalome


class SalomeEntry:
  
  enable_salome_selection = True
  help_message = u"Une entrée de l'arbre d'étude de Salome est attendue"
  
  def __init__(self, entryStr):
    self._entry = entryStr
  
  @staticmethod
  def __convert__(entryStr):
    return SalomeEntry(entryStr)
  
  @staticmethod
  def get_selected_value(selected_entry, study_editor):
    sobj = study_editor.study.FindObjectID(selected_entry)
    name = sobj.GetName()
    return "%s (%s)" % (name, selected_entry)

def parse_entry(selected_value):
  """
  Find entry if selected_value is something like "name (entry)"
  """
  entry = selected_value
  match = re.search("\((.*)\)$", entry)
  if match is not None:
    entry = match.group(1)
  return entry

class EficasFrame(eficasSalome.MyEficas):
  """
  This class launches Eficas for PARAMETRIC module. The messages in this class are in
  french because they are displayed in Eficas interface.

  """
  def __init__(self, parent = None):
    self.codedir = os.path.dirname(__file__)
    sys.path[:0] = [self.codedir]
    eficasSalome.MyEficas.__init__(self, parent, "parametric_exec_params")
    self.editor = getStudyEditor()

  def selectGroupFromSalome(self, kwType = None, editor = None):
    """
    Select an entry from Salome object browser
    """
    nbEntries = salome.sg.SelectedCount()
    if nbEntries < 1:
      msg = u"Veuillez sélectionner une entrée de l'arbre d'étude de Salome"
      QMessageBox.information(self, self.tr(u"Sélection depuis Salome"), self.tr(msg))
      return [], msg
    elif nbEntries > 1:
      msg = u"Une seule entrée doit être sélectionnée dans l'arbre d'étude de Salome"
      QMessageBox.information(self, self.tr(u"Sélection depuis Salome"), self.tr(msg))
      return [], msg
    else:
      try:
        value = kwType.get_selected_value(salome.sg.getSelected(0), self.editor)
        msg = u"L'entrée de l'arbre d'étude de Salome a été sélectionnée"
        return [value], msg
      except Exception, e:
        QMessageBox.information(self, self.tr(u"Sélection depuis Salome"), self.tr(unicode(e)))
        return [], unicode(e)

  def get_text_jdc(self):
    """
    Return the currently edited JDC as text
    """
    editor_index = self.viewmanager.myQtab.currentIndex()
    if editor_index < 0:
      return None
    eficas_editor = self.viewmanager.dict_editors[editor_index]
    return eficas_editor.get_text_JDC(eficas_editor.format)

  def closeEvent(self, event):
    while self.codedir in sys.path:
      sys.path.remove(self.codedir)
    eficasSalome.MyEficas.closeEvent(self, event)

  def set_exec_params_from_param_study(self, param_study):
    # No clean way to load JDC directly in Eficas, use a temp file instead
    (fd, filename) = tempfile.mkstemp()
    os.close(fd)
    f = open(filename, "w")
    f.write(param_study.exec_params)
    f.close()
    self.viewmanager.handleOpen(filename)
