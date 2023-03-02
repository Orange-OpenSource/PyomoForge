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

def test_weber():
  """
  """
  tex = """min \\sum_{s \\in S} deployment\\_cost_{s} \\times is\\_deployed_{s} \\\\
s.t.
is\\_served\\_by_{c,s} \\leq is\\_deployed_{s}, \\forall s \\in S, \\forall c \\in C, (1)\\\\ % affectation
\\sum_{(c,s) \\in ServersOfClient} is\\_served\\_by_{c,s} == exactcoverage \\forall c \\in C, (2)\\\\ % exactcoverage
\\sum_{(c,s) \\in ServersOfClient} clientDemand_{c} \\times is\\_served\\_by_{c,s} \\leq serverCapacity_{s} \\times is\\_deployed_{s} \\forall s \\in S, (3) \\\\ % serverCapacity
\\sum_{(c,s) \\in ServersOfClient} clientPortDemand_{c} \\times is\\_served\\_by_{c,s} \\leq serverPortCapacity_{s} \\times is\\_deployed_{s} \\forall s \\in S, (4) \\\\ % serverPortCapacity
vars\\\\
is\\_served\\_by_{c,s} \\in {0,1}, \\forall s \\in S, \\forall c \\in C 
is\\_deployed_{s} \\in {0,1}, \\forall s \\in S
"""
  model = read_model(tex, lambda parser: parser.model())
  pyomo_output = format_model(model)
  print(pyomo_output)
  assert pyomo_output == """model.is_served_by = Var(model.S,model.C, domain=Boolean)
model.is_deployed = Var(model.S, domain=Boolean)
model.objective = Objective(sense=minimize,rule=lambda model: sum([model.deployment_cost[s] * model.is_deployed[s] for s in model.S]))
model.constraint_1 = Constraint(model.S,model.C,rule=lambda model,s,c: model.is_served_by[c,s] <= model.is_deployed[s])
model.constraint_2 = Constraint(model.C,rule=lambda model,c: sum([model.is_served_by[c,s] for (c,s) in model.ServersOfClient]) == model.exactcoverage)
model.constraint_3 = Constraint(model.S,rule=lambda model,s: sum([model.clientDemand[c] * model.is_served_by[c,s] for (c,s) in model.ServersOfClient]) <= model.serverCapacity[s] * model.is_deployed[s])
model.constraint_4 = Constraint(model.S,rule=lambda model,s: sum([model.clientPortDemand[c] * model.is_served_by[c,s] for (c,s) in model.ServersOfClient]) <= model.serverPortCapacity[s] * model.is_deployed[s])"""

