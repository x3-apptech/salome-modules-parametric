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

from salome.kernel.parametric import study_exchange_vars
from salome.gui.selectvars import MySelectVarsDialog

class SelectVarsFrame(MySelectVarsDialog):

  def __init__(self, parent = None):
    MySelectVarsDialog.__init__(self, parent)
    self.OKButton.hide()
    self.cancelButton.hide()

  def set_vars_from_param_study(self, param_study):
    input_var_list = [study_exchange_vars.Variable(var.name) for var in param_study.input_vars]
    output_var_list = [study_exchange_vars.Variable(varname) for varname in param_study.output_vars]
    exchange_vars = study_exchange_vars.ExchangeVariables(input_var_list, output_var_list)
    self.setExchangeVariables(exchange_vars)
