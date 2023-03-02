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
from tex2pyomo.format import format_ensemble

def test_format_ensemble_with_a_name():
  ensemble = {'type': 'ensemble_name', 'name': 'T'}
  res = format_ensemble(ensemble)
  assert res == 'T'

def test_format_ensemble_with_a_boolean_domain():
  ensemble = {'content': ['0', '1'], 'type': 'ensemble_definition'}
  res = format_ensemble(ensemble)
  assert res == "Boolean"