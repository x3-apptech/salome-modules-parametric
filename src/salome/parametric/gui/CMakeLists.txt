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

INCLUDE(UsePyQt4)

# --- Python files ---

SET(PYFILES
  __init__.py
  definevalues.py
  execparams.py
  genjob.py
  mainpanel.py
  selectvars.py
  wizard.py
)

# uic files / to be processed by pyuic
SET(UIFILES
  wizard.ui
  varrange.ui
  execparams.ui
  genjob.ui
  definevalues.ui
)

# --- rules ---

# scripts / pyuic wrappings
PYQT4_WRAP_UIC(PYUICFILES ${UIFILES})

SET(ALLPYFILES ${PYFILES} ${PYUICFILES})

INSTALL_AND_COMPILE_PYTHON_FILE("${ALLPYFILES}" ${SALOME_INSTALL_PYTHON}/salome/parametric/gui)
