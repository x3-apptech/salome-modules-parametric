..
   Copyright (C) 2012-2015 EDF

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


.. _tut-values-compo-label:

======================================================
Step 3: Define the values for the parametric variables
======================================================

In this step we will define the values that the parametric variables will take
in the parametric study. Three methods are proposed for that:

* Define ranges for each variable. The domain that is defined by those ranges
  will be completely sampled to build the experimental plane.
* Write a Python script that will create the sample.
* Import the sample from a CSV file.

In this tutorial, we will use the first method. To define the ranges for the
parametric variables, you just have to select the minimum and maximum value
for each variable along with the sampling step, as illustrated below.

.. image:: /_static/define_ranges.png
   :align: center

Then click button "Next >>" to proceed to the last step of the parametric
study creation.

:ref:`tut-solver-compo-label`
