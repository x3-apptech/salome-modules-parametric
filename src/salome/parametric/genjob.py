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

import os
import re
import tempfile
from datetime import datetime

import salome
from salome.kernel.studyedit import getStudyEditor
from study import ParametricStudy

job_script_template = """
#!/usr/bin/env python

import salome
import PARAMETRIC

salome.salome_init()

# load study
study = salome.myStudyManager.Open("%(input_study)s")

# start container and load PARAMETRIC component
comp = salome.lcc.FindOrLoadComponent("ParametricContainer", "PARAMETRIC")

# run parametric study
comp.RunStudy(study._get_StudyId(), "%(param_entry)s")

# save study
salome.myStudyManager.SaveAs("%(output_study)s", study, False)
"""

def generate_job(param_study, result_study_file_name, result_dir, resource):
  """
  Create a Launcher job using the parameters specified by the user.
  """
  # Save Salome study
  ed = getStudyEditor()
  name_wo_space = param_study.name.replace(" ", "_")
  (fd, input_study) = tempfile.mkstemp(prefix = name_wo_space + "_Input_", suffix = ".hdf")
  os.close(fd)
  salome.myStudyManager.SaveAs(input_study, ed.study, False)

  # Generate job script
  job_script = job_script_template % {"input_study": os.path.basename(input_study),
                                      "param_entry": param_study.entry,
                                      "output_study": result_study_file_name}
  (fd, job_script_file) = tempfile.mkstemp(prefix = "job_" + name_wo_space + "_", suffix = ".py")
  os.close(fd)
  f = open(job_script_file, "w")
  f.write(job_script)
  f.close()
  
  # Define job parameters
  job_params = salome.JobParameters()
  job_params.job_name = name_wo_space
  job_params.job_type = "python_salome"
  job_params.job_file = job_script_file
  job_params.in_files = [input_study]
  job_params.out_files = [result_study_file_name]
  job_params.result_directory = result_dir

  # Add files to transfer from the computation code
  if param_study.solver_code_type == ParametricStudy.SALOME_COMPONENT:
    code = param_study.salome_component_name
    comp = salome.lcc.FindOrLoadComponent("FactoryServer", code)
    if comp is not None and hasattr(comp, "GetFilesToTransfer"):
        (code_in_files, code_out_files) = comp.GetFilesToTransfer(ed.studyId,
                parse_entry(param_study.solver_case_entry))
        job_params.in_files += code_in_files
        job_params.out_files += code_out_files        

  # Define resource parameters
  job_params.resource_required = salome.ResourceParameters()
  job_params.resource_required.name = resource
  job_params.resource_required.nb_proc = param_study.nb_parallel_computations + 1

  # Generate name for the working directory
  res_manager = salome.naming_service.Resolve("/ResourcesManager")
  res_definition = res_manager.GetResourceDefinition(resource)
  res_work_dir = res_definition.working_directory
  if res_work_dir != "":
      timestr = datetime.now().ctime()
      timestr = timestr.replace('/', '_')
      timestr = timestr.replace('-', '_')
      timestr = timestr.replace(':', '_')
      timestr = timestr.replace(' ', '_')
      work_dir = res_work_dir + "/" + job_params.job_name + "_" + timestr
      job_params.work_directory = work_dir
  
  # Create Launcher job
  launcher = salome.naming_service.Resolve('/SalomeLauncher')
  launcher.createJob(job_params)

def parse_entry(selected_value):
  """
  Find entry if selected_value is something like "name (entry)"
  """
  entry = selected_value
  match = re.search("\((.*)\)$", entry)
  if match is not None:
    entry = match.group(1)
  return entry
