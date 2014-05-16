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


========================
Definition of the solver
========================

The PARAMETRIC module offers two methods to define a solver code.

Salome component
================

The solver can be implemented as a Salome component that provides three
services: Init, Exec and Finalize. Those services must also be available as
YACS nodes. For the detailed description of those services, please see the
documentation of OpenTURNS module. Every component adapted for OpenTURNS in
Salome can be reused directly with the PARAMETRIC module.

If the solver code is implemented as a Salome component, the module providing
this component must also provide a way to describe a study case and store it
in Salome study so that it appears in the object browser. The user can then
select this case in the graphical interface of PARAMETRIC module to associate
the parametric study with a solver case.

Python script
=============

The solver can also be implemented as a Python script directly in the
graphical interface of PARAMETRIC module. This script must meet some
requirements:

* It can (and should) use the parametric variables that are directly defined
  in the environment of the script before its execution.
* It must create the variables of interest (if any).

For instance, a solver code that computes a variable of interest C that is the
product of the two parametric variables A and B can be written simply as::

    C = A * B
