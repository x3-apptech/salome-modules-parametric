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


=====================================
Step 1: Define the deterministic case
=====================================

The first step is to create a deterministic case, that is a description of the
calculation to be done. As our example uses the GENERICSOLVER module, first
you must activate this module:

.. image:: /_static/activate_gensolver.png
   :align: center

.. raw:: html

   <br/>

.. image:: /_static/new_gensolver.png
   :align: center

Then create a calculation case:

.. image:: /_static/new_detcase.png
   :align: center

You can modify the values of the different variables if you want, but note
that the values of the variables that you will define as parametric will be
overrided.

.. image:: /_static/setvalue_detcase.png
   :align: center

You can also run a deterministic calculation of the deviation of the beam with
the values set for the variables:

.. image:: /_static/runsolver_detcase.png
   :align: center

.. raw:: html

   <br/>

.. image:: /_static/result_detcase.png
   :align: center

Now we have defined the target of our parametric study. It's time to describe
what this study will look like.

:ref:`tut-variables-label`
