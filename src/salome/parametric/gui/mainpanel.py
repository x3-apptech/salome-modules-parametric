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

import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from wizard import Wizard

class MainPanel():

  def new_study(self):
    wizard = Wizard(sgPyQt.getDesktop())
    view_id = sgPyQt.createView("New Parametric Study", wizard)
    wizard.view_id = view_id

  def edit_study(self, param_study):
    wizard = Wizard(sgPyQt.getDesktop())
    wizard.set_study(param_study)
    view_id = sgPyQt.createView(param_study.name, wizard)
    wizard.view_id = view_id
