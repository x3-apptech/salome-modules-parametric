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

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
PROJECT(PARAMETRIC)
SET(VERSION "7.2.0")
SET(SHORT_VERSION "7.2")

SET(KERNEL_ROOT_DIR $ENV{KERNEL_ROOT_DIR})
IF(NOT KERNEL_ROOT_DIR)
  MESSAGE(FATAL_ERROR "Environment variable KERNEL_ROOT_DIR not set")
ENDIF(NOT KERNEL_ROOT_DIR)

SET(GUI_ROOT_DIR $ENV{GUI_ROOT_DIR})
IF(NOT GUI_ROOT_DIR)
  MESSAGE(FATAL_ERROR "Environment variable GUI_ROOT_DIR not set")
ENDIF(NOT GUI_ROOT_DIR)

SET(CMAKE_MODULE_PATH ${KERNEL_ROOT_DIR}/salome_adm/cmake_files
                      ${GUI_ROOT_DIR}/adm_local/cmake_files)

INCLUDE(SalomeMacros)
FIND_PACKAGE(SalomeKERNEL REQUIRED)
FIND_PACKAGE(SalomePython)
FIND_PACKAGE(SalomeOmniORB)
FIND_PACKAGE(SalomeOmniORBPy)
FIND_PACKAGE(SalomeSIP)
FIND_PACKAGE(SalomePyQt4)
IF(SALOME_BUILD_DOC)
  FIND_PACKAGE(SalomeSphinx REQUIRED)
ENDIF()

SET(BINDIR bin/salome)
SET(RESDIR share/salome/resources/parametric)
SET(LIBDIR lib/salome)
SET(PYTHONDIR lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages/salome)
SET(DOCDIR share/doc/salome/gui/PARAMETRIC)

ADD_SUBDIRECTORY(idl)
ADD_SUBDIRECTORY(src)
IF(SALOME_BUILD_DOC)
  ADD_SUBDIRECTORY(doc)
ENDIF(SALOME_BUILD_DOC)
ADD_SUBDIRECTORY(resources)
