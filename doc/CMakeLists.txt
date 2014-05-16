# Copyright (C) 2012-2014 EDF
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

SET(RSTFILES
  index.rst
  reference.rst
  ref_solver.rst
  tut_deterministic.rst
  tutorial.rst
  tut_values.rst
  ref_csv_export.rst
  ref_execution.rst
  ref_values.rst
  tut_execution.rst
  tut_solver.rst
  tut_variables.rst
)

SET(SPHINXOPTS )
SET(SOURCEDIR ${CMAKE_CURRENT_SOURCE_DIR})
SET(PAPEROPT_a4 -D latex_paper_size=a4)
SET(ALLSPHINXOPTS -d doctrees ${PAPEROPT_a4} ${SPHINXOPTS} ${SOURCEDIR})

# install user's documentation

SALOME_CONFIGURE_FILE(conf.py.in conf.py)

SET(HTML_ROOT_FILE html/index.html)

ADD_CUSTOM_COMMAND(OUTPUT ${HTML_ROOT_FILE} 
  COMMAND ${CMAKE_COMMAND} -E make_directory html 
  COMMAND ${CMAKE_COMMAND} -E make_directory doctrees
  COMMAND ${SPHINX_EXECUTABLE} -c ${CMAKE_BINARY_DIR}/doc -b html ${ALLSPHINXOPTS} html
  DEPENDS ${RSTFILES}
)

ADD_CUSTOM_TARGET(BUILD_HTML ALL DEPENDS ${HTML_ROOT_FILE})

INSTALL(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/html/ 
  DESTINATION ${SALOME_PARAMETRIC_INSTALL_DOC}
  PATTERN ".buildinfo" EXCLUDE
)
