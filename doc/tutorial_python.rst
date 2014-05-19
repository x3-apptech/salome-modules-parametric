..
   Copyright (C) 2012-2014 EDF

   This file is part of SALOME PARAMETRIC module.

   SALOME PARAMETRIC module is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   SALOME PARAMETRIC module is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with SALOME PARAMETRIC module.  If not, see <http://www.gnu.org/licenses/>.


###################################################################
Tutorial: Parametric study using a Python script as the solver code
###################################################################

This tutorial explains how to create and run a parametric study using a Python
script as the solver code. We will use an example script that implements a
classical example: the computation of the deviation of a cantilever beam.

This computation is done with the simple formula
*dev = (F * L * L * L) / (3. * E * I)*, where *dev* is the deviation, *F* is
the vertical force applied to the end of the beam, *L* is the length of the
beam, *E* is the Young's modulus and *I* is the section modulus.

.. toctree::
   :maxdepth: 2

   tut_variables_python.rst
   tut_values_python.rst
   tut_solver_python.rst
   tut_execution_python.rst
