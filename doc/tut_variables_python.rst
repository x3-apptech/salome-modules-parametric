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


=====================================================================
Step 1: Define the parametric variables and the variables of interest
=====================================================================

In this step we will define the variables that will be exchanged between
the PARAMETRIC module and the calculation script. The parametric variables are
the input variables of the calculation script that will vary in a given range.
Let's say that in our example, *F* and *L* are the two parametric variables and
*E* and *I* are fixed variables.

The variables of interest are the output variables of the calculation code
that we want to study. In our example, there is only one output variable and
thus only one variable of interest: the deviation *dev*. 

To define those variables, you first have to activate the PARAMETRIC module.

.. image:: /_static/activate_parametric.png
   :align: center

.. |button_new_study| image:: /_static/button_new_study.png
   :align: middle

Then click on the button |button_new_study| to create a new parametric study
and to open the variables definition window.

.. image:: /_static/select_variables_empty.png
   :align: center

Now click on the "New..." button in the upper part of the window. Double click
on the new item named "TO EDIT!" to set it to the value "F". Then do the same
for the variable "L". In the lower part of the window, create the output
variable "dev" with the same method. In the end, your variables definition
window should look like this:

.. image:: /_static/select_variables_python_full.png
   :align: center

Finally, when you have created all the desired variables, click button
"Next >>" to proceed to the next step.

:ref:`tut-values-python-label`
