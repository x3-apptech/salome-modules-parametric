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


=================================
Execution of the parametric study
=================================

The parametric study can be either executed directly on the local computer or
as a batch job on a remote cluster.

Local execution
===============

For a local execution, the number of parallel computations should in most
cases be set to the number of cores of the local computer. If the solver code
uses a lot of memory, it may be necessary to decrease this number.

Note that with a local execution, the Salome application will be freezed
during the whole computation. This mode should thus be reserved for relatively
small cases.

Batch execution
===============

To execute the parametric study in batch, it is first necessary to generate a
job. This can be done easily in the graphical interface of the PARAMETRIC
module (right-click on the parametric study and select "Generate batch job").
You can then select the resource to use to run this job. When the job is
generated, it will appear in the JOBMANAGER module and you can then manage it
as any other job, for instance to set a time limit for the job. You can then
launch and follow the job and get the results with the JOBMANAGER module. With
those results comes a new Salome study that contains the results of the
parametric computation. Open it and export the results in a CSV file to
analyze them.
