# -*- coding: utf-8 -*-
#
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

from salome.parametric.gui.eficas.appli import SalomeEntry
from Accas import *

JdC = JDC_CATA(regles = (UN_PARMI('EXECUTION_PARAMETERS',)),
                        )

EXECUTION_PARAMETERS = PROC(
    nom = "EXECUTION_PARAMETERS", op = None,
    fr = u"Paramètres d'exécution de l'étude paramétrique",
    PARAMETRIC_STUDY_NAME = SIMP(statut = "o", typ = 'TXM',
                                 defaut = "Parametric Study",
                                 fr = u"Nom de l'étude paramétrique qui sera créée dans l'arbre d'étude de Salome"),
    SOLVER_CODE = SIMP(statut = "o", typ = 'TXM',
                       defaut = "DEVIATION",
                       fr = u"Nom du composant de calcul"),
    DETERMINISTIC_CASE_ENTRY = SIMP(statut = "o", typ = SalomeEntry,
                                    fr = u"Cas déterministe dans l'arbre d'étude de Salome"),
    NUMBER_OF_PARALLEL_COMPUTATIONS = SIMP(statut = "o", typ = 'I', defaut = 1,
                                           fr = u"Nombre de branches de calcul parallèles"),
)
