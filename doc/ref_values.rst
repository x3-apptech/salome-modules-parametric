..
   Copyright (C) 2012-2013 EDF

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


====================================
Definition of the experimental plane
====================================

The PARAMETRIC module offers three methods to define the experimental plane
(i.e. the set of values that the parametric variables can take).

Complete sampling of a given domain
===================================

The user must define ranges for each parametric variable. A range is described
by:

* The minimum value (that will be included in the generated sample)
* The maximum value (that will **not** be included in the generated sample)
* The step between two consecutive values

The domain that is defined by those ranges is then sampled completely and
regularly to build the experimental plane.

Generation by a Python script
=============================

A Python script written by the user creates the whole sample. The script must
create a Numpy array that contains all the points of the experimental plane.
The dimension of this array must thus be (n, d) where n is the number of
points in the sample and d is the number of parametric variables. This Numpy
array must be stored in a variable named "sample".

Importation of a sample defined in a CSV file
=============================================

The sample is imported from a CSV file defined by the user. This file must
meet some requirements:

* The separator character must be "," (comma). Thus the decimal separator for
  numerical values must be "." (dot).
* The first line of the file must contain the name of the parametric variables
  separated by commas in order to identify the columns of the file.
* Each other line must contain a number of values equal to the number of
  parametric variables, separated by commas. Each line corresponds to a point
  in the sample.
