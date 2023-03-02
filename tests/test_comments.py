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
from tex2pyomo.format import format_model, format_constraint
from tex2pyomo.parse import read_model

def test_ignore_comment():
  tex = """\\max 0 % this is a comment!
st.
"""
  pyomo_output = format_model(read_model(tex, lambda parser: parser.model()))
  assert pyomo_output == "\nmodel.objective = Objective(sense=maximize,rule=lambda model: 0)\n"

def test_ignore_text_formatting():
  tex = """m^{t}_{s,g} \\leq \\overline{M}_{g} && \\nonumber \\\\
    * z^{t}_{s,g} \\forall t \\in T, \\forall s \\in S, \\forall g \\in G, (4.38)"""
  pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
  assert pyomo_output == "model.constraint_4_38 = Constraint(" +\
"model.T,model.S,model.G," +\
"rule=lambda model,t,s,g: model.m[t,s,g] <= model.M_[g] * model.z[t,s,g])"

# def test_ignore_text_formatting2():
#   tex = """  & u^{t}_{a,o} = u^{t-1}_{a,o} + \\NUoa && \\nonumber \\\\
#    & - \\sum_{\\sigma \\in \\mathcal{K}} \\sum_{c \\in \\C} f_{\\sigma,c,o} \\; * \\pi^{t}_{\\sigma,c,a,o}\\forall a \\in A,\\; \\forall  t\\in \\T,\\; \\forall o \\in O, \\label{GMGuserdynamic_4_47}\\\\"""
#   pyomo_output = format_constraint(read_model(tex, lambda parser: parser.constraint())[0])
#   assert pyomo_output == "model.constraint_4_38 = Constraint(" +\
# "model.T,model.S,model.G," +\
# "rule=lambda model,t,s,g: model.m[t,s,g] <= model.M_[g] * model.z[t,s,g])"