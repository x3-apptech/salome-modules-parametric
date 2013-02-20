# Copyright (C) 2012 EDF
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

import h5py

from study import ParametricStudy

def save_param_study_dict(param_study_dict, filename):
  f = h5py.File(filename)
  f.attrs["filetype"] = "salome_parametric" # simple tag used to identify PARAMETRIC files
  f.attrs["version"] = "7.2" # version tag used to ensure backwards compatibility
  for entry, param_study in param_study_dict.iteritems():
    param_study_group = f.create_group(entry)
    if param_study.name is not None:
      param_study_group.attrs["name"] = param_study.name
    
    # Store input and output variables definitions
    ordered_vars = []
    input_vars_group = param_study_group.create_group("input_vars")
    for input_var in param_study.input_vars:
      ordered_vars.append(input_var.name)
      var_group = input_vars_group.create_group(input_var.name)
      var_group.attrs["min"] = input_var.min
      var_group.attrs["max"] = input_var.max
      var_group.attrs["step"] = input_var.step
    output_vars_group = param_study_group.create_group("output_vars")
    for output_varname in param_study.output_vars:
      ordered_vars.append(output_varname)
      var_group = output_vars_group.create_group(output_varname)
    
    # Store solver definition
    solver_group = param_study_group.create_group("solver")
    if param_study.solver_code_type == ParametricStudy.SALOME_COMPONENT:
      solver_group.attrs["solver_code_type"] = "salome_component"
      if param_study.salome_component_name is not None:
        solver_group.attrs["salome_component_name"] = param_study.salome_component_name
      if param_study.solver_case_entry is not None:
        solver_group.attrs["solver_case_entry"] = param_study.solver_case_entry
    else:
      solver_group.attrs["solver_code_type"] = "python_script"
      if param_study.python_script is not None:
        solver_group.attrs["python_script"] = param_study.python_script
 
    # Execution parameters
    execution_group = param_study_group.create_group("execution")
    execution_group.attrs["nb_parallel_computations"] = param_study.nb_parallel_computations
    
    # Data
    if param_study.data is not None:
      dset = param_study_group.create_dataset("data", (param_study.datasize, len(ordered_vars)))
      dset.attrs["ordered_vars"] = ordered_vars
      for idx_var, var in enumerate(ordered_vars):
        if var in param_study.data and len(param_study.data[var]) > 0:
          for idx_value, value in enumerate(param_study.data[var]):
            if value is not None:
              dset[idx_value, idx_var] = value
      
      # Error messages
      if "__ERROR_MESSAGE__" in param_study.data and len(param_study.data["__ERROR_MESSAGE__"]) > 0:
        dt = h5py.special_dtype(vlen=str)
        error_set = param_study_group.create_dataset("error_message", (param_study.datasize,), dt)
        for idx_value, value in enumerate(param_study.data["__ERROR_MESSAGE__"]):
          if value is not None:
            error_set[idx_value] = value

  f.close()

def load_param_study_dict(filename):
  pass
