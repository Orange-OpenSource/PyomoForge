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
from pyomoforge.format import format_constraint
from pyomoforge.parse import read_model
import pytest

def test_constraint_4_38():
  tex = "m^{t}_{s,g} \\leq \\overline{M}_{g} * z^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.38)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_38 = Constraint(" +\
"model.T,model.S,model.G," +\
"rule=lambda model,t,s,g: model.m[t,s,g] <= model.M_[g] * model.z[t,s,g])"

def test_constraint_4_39():
  # TODO: it should be "t \\in T-{0}" to avoid index out-of-range exception
  tex = "m^{t-1}_{s,g} \\leq m^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.39)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_39 = Constraint(" +\
"model.T,model.S,model.G," +\
"rule=lambda model,t,s,g: model.m[t - 1,s,g] <= model.m[t,s,g])"

def test_constraint_4_40():
  # TODO "M^0" instead of "M0"
  # TODO "(g,b) \\in GB" instead of "\\forall g \\in G, \\forall b \\in B", not all combinaisons are possible
  tex = "mb^{\\overline{t}}_{s,g,b} \\leq M^{0}_{s,g,b} + \\overline{M}_{g} \\times InvM_{g} \\forall s \\in S, \\forall g \\in G, \\forall b \\in B, (4.40)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_40 = Constraint(" +\
"model.S,model.G,model.B," +\
"rule=lambda model,s,g,b: model.mb[model.t_,s,g,b] <= model.M[0,s,g,b] + model.M_[g] * model.InvM[g])"

def test_constraint_4_41():
  tex = "z^{\\overline{t}}_{s,g} \\leq Z^{0}_{s,g} + InvA_{g} \\forall s \\in S, \\forall g \\in G, (4.41)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_41 = Constraint(" +\
"model.S,model.G," +\
"rule=lambda model,s,g: model.z[model.t_,s,g] <= model.Z[0,s,g] + model.InvA[g])"

@pytest.mark.skip("")
def test_constraint_4_42():
  tex = "u^{t}_{a,o} = \\sum_{g \\in G} \\sum_{s in S} u^{t}_{a,o,s,g}, \\forall t \\in T, \\forall a \\in A, \\forall o \\in O, (4.42)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == """model.constraint_4_42 = Constraint(
model.T,model.A,model.O,
rule=lambda model,t,a,o: model.u_tao[t,a,o] == LinearExpression(
    linear_coefs=[1 for s in model.S for g in model.G],
    linear_vars=[model.u_taosg[t,o,(s,a,g)]
                  for s in model.S for g in model.G if (s, a, g) in model.SAG]
)"""

def test_constraint_4_43():
  tex = "\\sum_{a \\in A} \\sum_{s \\in S} utaosg^{t}_{a,o,s,g} \\leq CP_{o,g} \\times \\sum_{a \\in A} \\overline{U}^{t}_{a,o} \\forall t \\in T, \\forall g \\in G, \\forall o \\in O, (4.43)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_43 = Constraint(" +\
"model.T,model.G,model.O," +\
"rule=lambda model,t,g,o: sum([sum([model.utaosg[t,a,o,s,g] for s in model.S]) for a in model.A]) <= model.CP[o,g] * sum([model.U_[t,a,o] for a in model.A]))"

def test_constraint_4_46():
  tex = "\\sum_{o \\in G} \\sum_{a \\in A} D^{t}_{o,g} \\times utaosg^{t}_{a,o,s,g} \\leq CAP_{g} \\times m^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.46)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_46 = Constraint(" +\
"model.T,model.S,model.G," +\
"rule=lambda model,t,s,g: sum([sum([model.D[t,o,g] * model.utaosg[t,a,o,s,g] for a in model.A]) for o in model.G]) <= model.CAP[g] * model.m[t,s,g])"

def test_constraint_4_48():
  tex = "u^{t}_{a,NO} = u^{t-1}_{a,NO} + N^{t}_{NO} \\times UTOT^{t-1}_{a} + \\sum_{o \\in OminusNO} \\sum_{σ \\in K} \\sum_{c \\in C} f_{σ,c,o} * π^{t}_{σ,c,a,o} \\forall t \\in Tminus0, \\forall a \\in A, (4.48)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_48 = Constraint(" +\
"model.Tminus0,model.A," +\
"rule=lambda model,t,a: model.u[t,a,model.NO] == model.u[t - 1,a,model.NO] + model.N[t,model.NO] * model.UTOT[t - 1,a] + sum([sum([sum([model.f[σ,c,o] * model.π[t,σ,c,a,o] for c in model.C]) for σ in model.K]) for o in model.OminusNO]))"

def test_constraint_4_49():
  tex = "\\sum_{s \\in S} \\sum_{a \\in A}  u^{\\overline{t}}_{a,NO,s,NG} \\geq \\underline{QoE} \\times \\sum_{a \\in A} UTOT^{\\overline{t}}_a, (4.49)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_49 = Constraint(" +\
"rule=lambda model: sum([sum([model.u[model.t_,a,model.NO,s,model.NG] for a in model.A]) for s in model.S]) >= model.QoE_ * sum([model.UTOT[model.t_,a] for a in model.A]))"

def test_constraint_4_50():
  tex = "α^\\overline{t} \\geq  \\underline{α}, (4.50)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_50 = Constraint(" +\
"rule=lambda model: model.α[model.t_] >= model.α_)"

def test_constraint_4_51():
  tex = "\\sum_{σ \\in K} \\sum_{c \\in C} δ^{t}_{σ,c,o} = 1 \\forall t \\in T, \\forall o \\in O, (4.51)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_51 = Constraint(" +\
"model.T,model.O," +\
"rule=lambda model,t,o: sum([sum([model.δ[t,σ,c,o] for c in model.C]) for σ in model.K]) == 1)"

def test_constraint_4_52():
  tex = "\\sum_{σ \\in K} δ^{t}_{σ,c,o} \\leq 1 + U_{c} - α^{t-1} \\forall t \\in T, \\forall o \\in O, \\forall c \\in C, (4.52)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_52 = Constraint(" +\
"model.T,model.O,model.C," +\
"rule=lambda model,t,o,c: sum([model.δ[t,σ,c,o] for σ in model.K]) <= 1 + model.U[c] - model.α[t - 1])"

def test_constraint_4_53():
  tex = "\\sum_{σ \\in K} δ^{t}_{σ,c,o} \\leq 1 + α^{t-1} - L_{c} \\forall t \\in T, \\forall o \\in O, \\forall c \\in C, (4.53)"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_53 = Constraint(" +\
"model.T,model.O,model.C," +\
"rule=lambda model,t,o,c: sum([model.δ[t,σ,c,o] for σ in model.K]) <= 1 + model.α[t - 1] - model.L[c])"

def test_constraint_ignore_limits():
  tex = "m^t_{s,g} =\\sum\\limits_{b \\in B} m^t_{s,g,b}, \\forall t \\in TZ,  \\forall s \\in S, \\forall g \\in G  \\label{summ_4_31}  "
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_summ_4_31 = Constraint(model.TZ,model.S,model.G,rule=lambda model,t,s,g: model.m[t,s,g] == sum([model.m[t,s,g,b] for b in model.B]))"

def test_partial_definition():
  tex = "u_{a,o}^{t}= \\sum_{(s,g) | (a,o,s,g) \\in \\mathcal{AOSG}}  u_{a,o,s,g}^{t},   \\forall a \\in A,  \\forall  t \\in \\mathcal{T}, \\forall o \\in O, \\label{idMGlink_4_42_filteredsum_version}"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_idMGlink_4_42_filteredsum_version = Constraint(model.A,model.T,model.O,rule=lambda model,a,t,o: model.u[t,a,o] == sum([model.u[t,a,o,s,g] for (a,o,s,g) in model.AOSG]))"

def test_tuple_variables():
  tex = "u_{a,o,s,g}^{t} \\leq E_{a,s,g} * u^t_{a,o} ,  \\forall  t \\in \\mathcal{T} , \\forall  (a,o,s,g) \\in \\mathcal{AOSG}\\label{geoservice_4_45_filtered-forall_version}"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_geoservice_4_45_filtered_forall_version = Constraint(model.T,model.AOSG,rule=lambda model,t,a,o,s,g: model.u[t,a,o,s,g] <= model.E[a,s,g] * model.u[t,a,o])"

def test_function():
  tex = "z^{\\bar{t}}_{s,g} \\leq \\max(Z^0_{s,g} , InvA_g)  , \\forall s \\in S,  \\forall g \\in G \\label{idMGinvrule2_4_41_maxi_version}"
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_idMGinvrule2_4_41_maxi_version = Constraint(model.S,model.G,rule=lambda model,s,g: model.z[model.t_,s,g] <= max(model.Z[0,s,g],model.InvA[g]))"

