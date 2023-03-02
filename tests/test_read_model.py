###
# #%L
# PyomoForge
# 
# Module name: com.orange.common:pyomoforge
# Version:     1.0
# Created:     2022-08-24
# %%
# Copyright (C) 2022 Orange
# %%
# The license and distribution terms in 'LGPL-3.0+' for this file may be found 
# in the file 'gnu lesser general public license v3.0 or later - license.txt' in this distribution 
# or LICENSE.txt or at http://www.gnu.org/licenses/lgpl-3.0-standalone.html.
# #L%
###
from pyomoforge.parse import read_model


def test_belong():
    tex = "y_{p}^{t} \\in {0,1}"
    model = read_model(tex, lambda parser: parser.belong())
    assert model == [{'variables': [{
        'model_variable': 'y',
        'local_variables': [
            {'model_variable': 't', 'local_variables': []},
            {'model_variable': 'p', 'local_variables': []},
        ]
    }], 
    'domains': [],
    'ensemble': {'content': ['0', '1'], 'type': 'ensemble_definition'}}]


def test_ens_T():
    tex = "T"
    model = read_model(tex, lambda parser: parser.ens())
    assert model == [{
        'type': 'ensemble_name',
        'name': 'T',
    }]


def test_ens_T_minus_0_1():
    tex = "T  \\cup\\{0,1\\}"
    model = read_model(tex, lambda parser: parser.ens())
    assert model == [{
        'type': 'ensemble_name',
        'name': 'T_minus_0_1',
    }]


def test_ens_0_1():
    tex = "\\{0,1\\}"
    model = read_model(tex, lambda parser: parser.ens())
    assert model == [{
        'type': 'ensemble_definition',
        'content': ['0', '1'],
    }]


def test_var():
    tex = "y_{p}^{t}"
    model = read_model(tex, lambda parser: parser.var())
    assert model == [{
        'model_variable': 'y',
        'local_variables': [
            {'model_variable': 't', 'local_variables': []},
            {'model_variable': 'p', 'local_variables': []},
        ]}]


def test_command_substitution():
    tex = """
\\newcommand{\\TZ}{\\mathcal{T} \\cup \\{0\\}}
 \\min 0 & \\\\
 st. & \\\\
&  t \\leq 0,  \\forall t \\in \\TZ \\label{eqincr_4_32}\\\\
\\end{align} 
"""
    model = read_model(tex, lambda parser: parser.model())
    assert model == {
        'constraints': [{'condition': '\\leq',
                         'domains': [{'ensemble': {'name': 'T_minus_0',
                                                   'type': 'ensemble_name'},
                                      'variables': [{'local_variables': [],
                                                     'model_variable': 't'}]}],
                         'indice': 'eqincr_4_32',
                         'left_expr': [{'local_variables': [],
                                        'model_variable': 't'}],
                         'right_expr': [{'local_variables': [],
                                         'model_variable': '0'}]}],
        'objective': {'expr': {'local_variables': [],
                               'model_variable': '0'},
                      'sense': '\\min'},
        'variables': None,
    }
