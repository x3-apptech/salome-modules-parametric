# Copyright (C) 2012-2013 EDF
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

import study
import genjob

PARAM_STUDY_TYPE_ID = study.PARAM_STUDY_TYPE_ID
PARAMETRIC_ENGINE_CONTAINER = study.PARAMETRIC_ENGINE_CONTAINER
ParametricStudy = study.ParametricStudy
VariableRange = study.VariableRange
ParametricStudyEditor = study.ParametricStudyEditor
generate_job = genjob.generate_job
parse_entry = genjob.parse_entry
