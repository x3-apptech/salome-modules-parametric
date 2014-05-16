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

SET(PARAMETRIC_RESOURCES_FILES
  export_to_csv_file.png
  new_param_study.png
  PARAMETRIC.png
  param_study.png
  edit_param_study.png
  generate_job.png
  PARAMETRICCatalog.xml
  PARAMETRIC_small.png
  run_param_study.png
)

INSTALL(FILES ${PARAMETRIC_RESOURCES_FILES} DESTINATION ${SALOME_PARAMETRIC_INSTALL_RES_DATA})

MESSAGE(STATUS "Creation of ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml")
CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/SalomeApp.xml.in ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml @ONLY)
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml DESTINATION ${SALOME_PARAMETRIC_INSTALL_RES_DATA})
