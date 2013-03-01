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

SET(PYTHON_FILES
  __init__.py
  definevalues.py
  execparams.py
  genjob.py
  mainpanel.py
  selectvars.py
  wizard.py
)
SET(PYUIC_FILES wizard_ui.py varrange_ui.py execparams_ui.py genjob_ui.py definevalues_ui.py)
SET(INSTALL_DIR ${PYTHONDIR}/salome/parametric/gui)

FOREACH(OUTPUT ${PYUIC_FILES})
  STRING(REPLACE "_ui.py" ".ui" INPUT ${OUTPUT})
  SET(INPUT ${CMAKE_CURRENT_SOURCE_DIR}/${INPUT})
  SET(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${OUTPUT})
  ADD_CUSTOM_COMMAND(OUTPUT ${OUTPUT}
                     COMMAND ${PYQT_PYUIC_EXECUTABLE} -o ${OUTPUT} ${INPUT}
                     MAIN_DEPENDENCY ${INPUT}
                    )
  SET(PYTHON_FILES ${PYTHON_FILES} ${OUTPUT})
ENDFOREACH(OUTPUT ${PYUIC_FILES})

ADD_CUSTOM_TARGET(BUILD_PY_UI_FILES ALL DEPENDS ${PYUIC_FILES})

INSTALL_AND_COMPILE_PYTHON_FILE("${PYTHON_FILES}" ${INSTALL_DIR})
