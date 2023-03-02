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
from pyomoforge.format import format_variable, format_variables, variables, format_model
from pyomoforge.parse import read_model

def test_variables():
  model = [{'ensemble': {'name': 'PositiveIntegers', 'type': 'ensemble_name'},
  'variables': [{'local_variables': [{'local_variables': [],
                                      'model_variable': 'j'}],
                 'model_variable': 'y'}]},
 {'ensemble': {'name': 'J', 'type': 'ensemble_name'},
  'variables': [{'local_variables': [], 'model_variable': 'j'}]}]
  vars = variables(model)
  assert vars == {
    "y": ["PositiveIntegers"],
    "j": ["J"],
  }

def test_format_real_variable():
  tex = """vars &\\nonumber \\\\
 &\\alpha^{t} \\geq 0 ,\\forall t \\in T  \\cup\\{0\\}\\\\"""
  pyomo_output = format_variable(read_model(tex, lambda parser: parser.vardefs())[0])
  assert pyomo_output == "model.α = Var(model.T_minus_0, domain=NonNegativeReals)"

# def test_format_boolean_variable():
#   tex = """vars &\\nonumber \\\\
#  & y_p^t \\in \\{0,1\\}, \\forall t \\in T  \cup\\{0\\}, \\forall p \\in \\mathcal{P}, \\\\"""
#   pyomo_output = format_variable(read_model(tex, lambda parser: parser.vardefs())[0])
#   assert pyomo_output == "model.y = Var(model.T_minus_0,model.P, domain=Boolean)"

def test_format_variables():
  tex = """vars &\\nonumber \\\\
       &  u^t_{a,o,s,g} \\geq 0 ,   \\forall  t\\in T,\\forall (a,o,s,g) \\in \\mathcal{AOSG},  \\label{def_u_filtered} \\\\
 &\\alpha^{t} \\geq 0 ,\\forall t \\in T  \\cup\\{0\\}\\\\"""
  pyomo_output = format_variables(read_model(tex, lambda parser: parser.vardefs()))
  assert pyomo_output == """model.u = Var(model.T,model.AOSG, domain=NonNegativeReals)
model.α = Var(model.T_minus_0, domain=NonNegativeReals)"""

def test_PositiveIntegers():
  tex = """vars &\\nonumber \\\\
       i \\in \\mathbb{N}"""
  model = read_model(tex, lambda parser: parser.vardefs())
  pyomo_output = format_variables(model)
  assert pyomo_output == "model.i = Var(domain=PositiveIntegers)"

def test_Boolean():
  tex = """vars &\\nonumber \\\\
       i \\in {0,1} , \\label{alabel}\\"""
  model = read_model(tex, lambda parser: parser.vardefs())
  pyomo_output = format_variables(model)
  assert pyomo_output == "model.i = Var(domain=Boolean)"

def test_Indexed_Boolean():
  tex = """vars &\\nonumber \\\\
       x_{i} \\in {0,1}, \\forall i \\in I """
  model = read_model(tex, lambda parser: parser.vardefs())
  pyomo_output = format_variables(model)
  assert pyomo_output == "model.x = Var(model.I, domain=Boolean)"

def test_Indexed_PositiveIntegers():
  tex = """vars
  y_{j} \\in \\mathbb{N}, \\forall j \\in J """
  model = read_model(tex, lambda parser: parser.vardefs())
  pyomo_output = format_variables(model)
  assert pyomo_output == "model.y = Var(model.J, domain=PositiveIntegers)"

def test_all_vars():
  tex = """
 \\newcommand{\\B}{\\mathcal{B}}
\\newcommand{\\bib}{b \\in \\B}
\\newcommand{\\TZ}{\\mathcal{T} \\cup \\{0\\}}
\\newcommand{\\GP}{\\mathcal{G}}
\\newcommand{\\A}{\\mathcal{A}}
\\newcommand{\\SI}{\\mathcal{S}}
\\newcommand{\\T}{\\mathcal{T}}
\\newcommand{\\OF}{\\mathcal{O}}
\\newcommand{\\C}{\\mathcal{C}}
\\newcommand{\\sis}{s \\in \\SI}
\\newcommand{\\tit}{t \\in \\T}
\\newcommand{\\aia}{a\\in \\A}
\\newcommand{\\oio}{o\\in \\OF}
\\newcommand{\\gig}{g \\in \\GP}
 \\min 0 &\\\\
 st. \\\\
vars  &\\nonumber \\\\
 &\\alpha^{t} \\geq 0 ,\\forall t \\in T  \\cup\\{0\\}\\\\
 & z^{t}_{s,g}\\in \\{0,1\\}, \\forall \\sis,\\; \\forall \\gig,\\; \\forall  t\\in \\TZ,\\label{idMGdvz}\\\\
 & y_{p}^{t} \\in \\{0,1\\}, \\forall  t \\in T  \\cup\\{0\\}, \\forall p \\in \\mathcal{P} \\\\
 & m^{t}_{s,g,b} \\geq 0 , \\forall t \\in T\\cup\\{0\\}, \\forall \\sis,  \\forall \\gig,  \\forall \\bib,  \\\\
 & incr^{t}_{s,g,b} \\geq 0 , \\forall t \\in T \\cup\\{0\\}, \\forall \\sis,  \\forall \\gig,  \\forall \\bib,  \\\\
 & decr^{t}_{s,g,b} \\geq 0 , \\forall t \\in T \\cup\\{0\\}, \\forall \\sis,  \\forall \\gig,  \\forall \\bib,  \\\\
  & m^{t}_{s,g} \\ge 0 , \\forall \\sis,\\; \\forall \\gig,\\; \\forall  t\\in \\TZ,\\label{idMGdvz}\\\\
   &       u^{t}_{a,o} \\geq 0 , \\forall \\aia,\\; \\forall  t\\in \\TZ,\\; \\forall  \\oio,  \\label{GMGdvu1}\\\\
       &  u^{t}_{a,o,s,g} \\geq 0 ,   \\forall  t\\in \\T,\\forall (a,o,s,g) \\in \\mathcal{AOSG},  \\label{def_u_filtered} \\\\
       &   \\delta^{t}_{\\sigma,c,o} \\in \\{0,1\\},  \\forall  t\\in \\T,\\; \\forall  \\sigma \\in \\mathcal{K},\\; \\forall  c \\in \\C, \\; \\forall \\oio, \\label{idMGdvdelta}\\\\
               &   \\pi^{t}_{\\sigma,c,a,o} \\geq 0, \\forall \\aia, \\; \\forall  t\\in \\T, \\; \\forall  \\sigma \\in \\mathcal{K},\\; \\forall  c \\in \\C ,\\; \\forall \\oio ,  \\label{GMGdvdeltalin}"""
  model = read_model(tex, lambda parser: parser.model())
  pyomo_output = format_model(model)
  assert pyomo_output == """model.α = Var(model.T_minus_0, domain=NonNegativeReals)
model.z = Var(model.S,model.G,model.T_minus_0, domain=Boolean)
model.y = Var(model.T_minus_0,model.P, domain=Boolean)
model.m = Var(model.T_minus_0,model.S,model.G,model.B, domain=NonNegativeReals)
model.incr = Var(model.T_minus_0,model.S,model.G,model.B, domain=NonNegativeReals)
model.decr = Var(model.T_minus_0,model.S,model.G,model.B, domain=NonNegativeReals)
model.m = Var(model.S,model.G,model.T_minus_0, domain=NonNegativeReals)
model.u = Var(model.A,model.T_minus_0,model.O, domain=NonNegativeReals)
model.u = Var(model.T,model.AOSG, domain=NonNegativeReals)
model.δ = Var(model.T,model.K,model.C,model.O, domain=Boolean)
model.π = Var(model.A,model.T,model.K,model.C,model.O, domain=NonNegativeReals)
model.objective = Objective(sense=minimize,rule=lambda model: 0)
"""