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

from study import ParametricStudy, ParametricVariable

def save_param_study_dict(param_study_dict, filename):
  with h5py.File(filename, "w") as f:
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

def load_param_study_dict(filename):
  param_study_dict = {}
  with h5py.File(filename, 'r') as f:
    filetype = f.attrs.get("filetype")
    version = f.attrs.get("version")
    if filetype is None or filetype != "salome_parametric" or version is None:
      raise Exception("The file is not a valid parametric study file")
    if version == "7.2":
      param_study_dict = _load_param_study_dict_7_2(f)
    else:
      raise Exception('Invalid version "%s" for parametric study file' % version)
  return param_study_dict

def _load_param_study_dict_7_2(hdffile):
  param_study_dict = {}
  for entry, param_study_group in hdffile.iteritems():
    param_study = ParametricStudy()
    param_study.name = param_study_group.attrs.get("name")

    # Load input and output variables definitions
    input_vars_group = param_study_group["input_vars"]
    for varname, var_group in input_vars_group.iteritems():
      minval = var_group.attrs["min"]
      maxval = var_group.attrs["max"]
      step = var_group.attrs["step"]
      param_study.add_input_variable(ParametricVariable(str(varname), minval, maxval, step))
    output_vars_group = param_study_group["output_vars"]
    for output_varname in output_vars_group.iterkeys():
      param_study.add_output_variable(str(output_varname))

    # Load solver definition
    solver_group = param_study_group["solver"]
    if solver_group.attrs["solver_code_type"] == "salome_component":
      param_study.solver_code_type = ParametricStudy.SALOME_COMPONENT
      param_study.salome_component_name = solver_group.attrs.get("salome_component_name")
      param_study.solver_case_entry = solver_group.attrs.get("solver_case_entry")
    else:
      param_study.solver_code_type = ParametricStudy.PYTHON_SCRIPT
      param_study.python_script = solver_group.attrs.get("python_script")

    # Load execution parameters
    execution_group = param_study_group["execution"]
    param_study.nb_parallel_computations = execution_group.attrs["nb_parallel_computations"]

    # Load data
    if "data" in param_study_group:
      dset = param_study_group["data"]
      ordered_vars = dset.attrs["ordered_vars"]
      param_study.data = {}
      param_study.datasize = len(dset)
      for idx_var, var in enumerate(ordered_vars):
        param_study.data[var] = list(dset[:,idx_var])

      # Error messages
      if "error_message" in param_study_group:
        error_set = param_study_group["error_message"]
        param_study.data["__ERROR_MESSAGE__"] = list(error_set)

    param_study_dict[str(entry)] = param_study

  return param_study_dict
