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
from pyomoforge.format import format_objective
from pyomoforge.parse import read_model

def test_objective():
  tex = "min (\\sum_{t \\in T} \\sum_{σ \\in K} \\sum_{c \\in C} \\sum_{a \\in A} \\sum_{o \\in OminusNO} σ * f_{σ,c,o} * π^{t}_{σ,c,a,o}) + (\\sum_{s \\in S} \\sum_{g \\in G} CM_{g} * (m^{\\overline{t}}_{s,g} - M^{0}_{s,g})) + (\\sum_{s \\in S} \\sum_{g \\in G} CA_{g} * (z^{\\overline{t}}_{s,g} - Z^{0}_{s,g}))"
  pyomo_output = format_objective(read_model(tex, lambda parser: parser.objective())[0])
  assert pyomo_output == "model.objective = Objective(" +\
"sense=minimize," +\
"rule=lambda model: (sum([sum([sum([sum([sum([σ * model.f[σ,c,o] * model.π[t,σ,c,a,o] for o in model.OminusNO]) for a in model.A]) for c in model.C]) for σ in model.K]) for t in model.T])) +" +\
" (sum([sum([model.CM[g] * (model.m[model.t_,s,g] - model.M[0,s,g]) for g in model.G]) for s in model.S])) +" +\
" (sum([sum([model.CA[g] * (model.z[model.t_,s,g] - model.Z[0,s,g]) for g in model.G]) for s in model.S])))"

def test_objective_maximize():
  tex = "max 0"
  pyomo_output = format_objective(read_model(tex, lambda parser: parser.objective())[0])
  assert pyomo_output == "model.objective = Objective(" +\
"sense=maximize," +\
"rule=lambda model: 0)"

def test_objective_min_max_formated():
  tex = "\\max 0"
  pyomo_output = format_objective(read_model(tex, lambda parser: parser.objective())[0])
  assert pyomo_output == "model.objective = Objective(" +\
"sense=maximize," +\
"rule=lambda model: 0)"