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

INSTALL(DIRECTORY ./ DESTINATION ${RESDIR} FILES_MATCHING PATTERN "*.png")
INSTALL(FILES PARAMETRICCatalog.xml DESTINATION ${RESDIR})

MESSAGE(STATUS "Creation of ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml")
CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/SalomeApp.xml.in ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml @ONLY)
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml DESTINATION ${RESDIR})
