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
from pyomoforge.format import format_model
from pyomoforge.parse import read_model

def test_command_substitution():
  tex = """
\\newcommand{\\SI}{\\mathcal{S}}
\\newcommand{\\GP}{\\mathcal{G}}
\\newcommand{\\gig}{g \\in \\GP}
\\newcommand{\\TZ}{\\mathcal{T} \\cup \\{0\\}}
\\newcommand{\\sis}{s \\in \\SI}
\\begin{align}
 \\min 0 & \\\\
 st. & \\\\
&  incr^t_{s,g,b} \\geq m^t_{s,g,b} - m^{t-1}_{s,g,b},  \\forall t \\in \\TZ,  \\forall \\sis, \\forall \\gig, \\forall  b\\in \\mathcal{B} \\label{eqincr_4_32}\\\\
\\end{align} 
"""
  pyomo_output = format_model(read_model(tex, lambda parser: parser.model()))
  assert pyomo_output == """model.objective = Objective(sense=minimize,rule=lambda model: 0)
model.constraint_eqincr_4_32 = Constraint(model.T_minus_0,model.S,model.G,model.B,rule=lambda model,t,s,g,b: model.incr[t,s,g,b] >= model.m[t,s,g,b] - model.m[t - 1,s,g,b])"""

def test_command_substitution_in_sum():
  tex = """
\\newcommand{\\SI}{\\mathcal{S}}
\\newcommand{\\GP}{\\mathcal{G}}
\\newcommand{\\gig}{g \\in \\GP}
\\newcommand{\\TZ}{\\mathcal{T} \\cup \\{0\\}}
\\newcommand{\\sis}{s \\in \\SI}
\\begin{align}
 \\min 0 & \\\\
 st. & \\\\
&  u^{t}_{a,o} = \\sum\\limits_{\\gig} \\sum_{\\sis} u^{t}_{a,o,s,g}, \\forall t \\in T, \\forall a \\in A, \\forall o \\in O, (4.42)\\\\
\\end{align} 
"""
  pyomo_output = format_model(read_model(tex, lambda parser: parser.model()))
  assert pyomo_output == """model.objective = Objective(sense=minimize,rule=lambda model: 0)
model.constraint_4_42 = Constraint(model.T,model.A,model.O,rule=lambda model,t,a,o: model.u[t,a,o] == sum([sum([model.u[t,a,o,s,g] for s in model.S]) for g in model.G]))"""
