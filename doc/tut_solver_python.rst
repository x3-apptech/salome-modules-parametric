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


.. _tut-solver-python-label:

======================================================
Step 3: Define the solver and the execution parameters
======================================================

In this step we will define the solver to use for our parametric study. Two
types of solvers can be used with the PARAMETRIC module:

* The solver can be a Salome component that must define a few methods with
  given signatures.
* The solver can be a Python script.

In this tutorial, we use a Python script. Select the second radio button
"Python script", and implement the script directly in this window (of course,
you can also copy-paste the script from an external editor if you prefer).
This script should directly use the input variables *F* and *L* that will be
set automatically in the context of the script before running it. It should
create the output variable *dev*, like in the example below.

We can also change the name of the parametric study (the name that the study
will have in the object browser) and the number of computations that will be
launched in parallel.

.. image:: /_static/define_solver_python.png
   :align: center

Finally, just click the "OK" button to validate the creation of the parametric
study. A new item representing the study appears in the object browser.

.. image:: /_static/ob_new_study_python.png
   :align: center

:ref:`tut-execution-python-label`
