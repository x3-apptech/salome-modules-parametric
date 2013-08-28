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

INCLUDE(UseOmniORB)

INCLUDE_DIRECTORIES(
  ${OMNIORB_INCLUDE_DIR}
  ${KERNEL_ROOT_DIR}/include/salome
  ${CMAKE_CURRENT_BINARY_DIR}
)

SET(PARAMETRIC_IDL_FILES PARAMETRIC_Gen.idl)
SET(IDL_INCLUDE_DIRS ${KERNEL_ROOT_DIR}/idl/salome)

OMNIORB_ADD_MODULE(SalomeIDLPARAMETRIC "${PARAMETRIC_IDL_FILES}" "${IDL_INCLUDE_DIRS}"
                   ${KERNEL_SalomeIDLKernel})
INSTALL(TARGETS SalomeIDLPARAMETRIC DESTINATION ${SALOME_INSTALL_LIBS})
