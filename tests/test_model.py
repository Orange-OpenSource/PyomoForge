###
# #%L
# Tex2Pyomo
# 
# Module name: com.orange.common:tex2pyomo
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
from tex2pyomo.format import format_model
from tex2pyomo.parse import read_model

def test_bin_packing():
  """
    Problème de bin-packing (https://fr.wikipedia.org/wiki/Probl%C3%A8me_de_bin_packing):
     - un nombre 1 , 2 , … , m de boîtes de taille C, ensemble J
     - une liste 1 , 2 , … , n d'articles i de taille c_{i}, ensemble I.

    On cherche à trouver le rangement valide pour tous ces articles qui minimise le nombre de boîtes utilisées.
    Pour qu'un rangement soit valide, la somme des tailles des articles affectés à une boîte doit être inférieure ou égale à C.
    Pour décrire une solution, on peut utiliser un codage binaire pour indiquer dans quelle boîte j chaque objet i est rangé.
     - La variable x_{{ij}} vaudra 1 si l'article i est rangé dans la boîte j et 0 sinon.
     - La variable binaire y_{j} est égale à 1 si la boîte j est utilisée, 0 sinon.

     La première inégalité signifie qu'on ne peut dépasser la taille d'une boîte pour un rangement.
     La deuxième inégalité impose à tous les objets d'être rangés dans une boîte et une seule. 
  """
  tex = """min \\sum_{j \\in J} y_{j}
s.t.
\\sum_{i \\in I} c_{i} * x_{i,j} \\leq C * y_{j} \\forall j \\in J, (1)
\\sum_{j \\in J} x_{i,j} = 1 \\forall i \\in I, (2)
vars
y_{j} \\in \\mathbb{N}, \\forall j \\in J 
x_{i,j} \\in \\mathbb{N}, \\forall i \\in I, \\forall j \\in J 
"""
  model = read_model(tex, lambda parser: parser.model())
  pyomo_output = format_model(model)
  print(pyomo_output)
  assert pyomo_output == """model.y = Var(model.J, domain=PositiveIntegers)
model.x = Var(model.I,model.J, domain=PositiveIntegers)
model.objective = Objective(sense=minimize,rule=lambda model: sum([model.y[j] for j in model.J]))
model.constraint_1 = Constraint(model.J,rule=lambda model,j: sum([model.c[i] * model.x[i,j] for i in model.I]) <= model.C * model.y[j])
model.constraint_2 = Constraint(model.I,rule=lambda model,i: sum([model.x[i,j] for j in model.J]) == 1)"""

  print("""from pyomo.environ import *
model = ConcreteModel()
model.C = 5
model.J = RangeSet(1, 3)
model.I = RangeSet(1, 6)
model.c = Param(model.I, initialize=[2, 2, 2, 2, 2, 2])
model.i = Var(model.I, model.J, domain=PositiveIntegers)
model.y = Var(model.J, domain=PositiveIntegers)
""" + pyomo_output + """
solver = SolverFactory('cbc')
solver.solve(model)
model.write()
  """)

def test_ignore_formating():
  """
    Ignore formating like align
  """
  tex = """\\begin{align*}
min \\sum_{j \\in J} y_{j} & \\\\
s.t. & \\\\
 & \\sum_{i \\in I} c_{i} * x_{i,j} \\leq C * y_{j} & \\forall j \\in J, & (1) \\\\
 & \\sum_{j \\in J} x_{i,j} = 1 & \\forall i \\in I, & (2) \\\\
\\end{align} 
"""
  pyomo_output = format_model(read_model(tex, lambda parser: parser.model()))
  assert pyomo_output == """model.objective = Objective(sense=minimize,rule=lambda model: sum([model.y[j] for j in model.J]))
model.constraint_1 = Constraint(model.J,rule=lambda model,j: sum([model.c[i] * model.x[i,j] for i in model.I]) <= model.C * model.y[j])
model.constraint_2 = Constraint(model.I,rule=lambda model,i: sum([model.x[i,j] for j in model.J]) == 1)"""

  print("""from pyomo.environ import *
model = ConcreteModel()
model.C = 5
model.J = RangeSet(1, 3)
model.I = RangeSet(1, 6)
model.c = Param(model.I, initialize=[2, 2, 2, 2, 2, 2])
model.i = Var(model.I, model.J, domain=PositiveIntegers)
model.y = Var(model.J, domain=PositiveIntegers)
""" + pyomo_output + """
solver = SolverFactory('cbc')
solver.solve(model)
model.write()
  """)

def test_real_case():
  tex = """\\begin{align}
 \\min 0 & \\\\
 st. & \\\\
&  m^t_{s,g} =\\sum\\limits_{b \\in B} m^t_{s,g,b}, \\forall t \\in TZ,  \\forall s \\in S, \\forall g \\in G  \\label{summ_4_31} \\\\
\\end{align} 
"""
  pyomo_output = format_model(read_model(tex, lambda parser: parser.model()))
  assert pyomo_output == """model.objective = Objective(sense=minimize,rule=lambda model: 0)
model.constraint_summ_4_31 = Constraint(model.TZ,model.S,model.G,rule=lambda model,t,s,g: model.m[t,s,g] == sum([model.m[t,s,g,b] for b in model.B]))"""