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
# https://faun.pub/introduction-to-antlr-python-af8a3c603d23
from typing import Dict, List

import pprint
pp = pprint.PrettyPrinter()



conditions_map = {
    "\\leq": "<=",
    "\\geq": ">=",
    "=": "=="
}

op_map = {
    "\\times": "*",
}


def format_something(something, known_variables):
    if "left" in something:
        return format_exp(something, known_variables)
    if "func" in something and something["func"] == "sum":
        return format_sum(something, known_variables)
    if "func" in something:
        return format_func(something, known_variables)
    if "parenthesis" in something:
        return format_parenthesis(something, known_variables)
    if "model_variable" in something:
        return format_var(something, known_variables)


def format_var(var, known_variables):
    model_variable = var["model_variable"]
    # model_variable should be a str
    # However, in case of substitution, it can be a more complex expression
    if isinstance(model_variable, dict):
        return format_something(model_variable, known_variables)
    local_variables = [format_something(v, known_variables + [v])
                       for v in var["local_variables"]]
    if model_variable in known_variables or model_variable.isnumeric():
        return model_variable
    ctx_local_variables = "" if len(
        local_variables) == 0 else "[" + ",".join(local_variables) + "]"
    return "model." + model_variable + ctx_local_variables


def format_exp(exp, known_variables):
    operation = op_map[exp["op"]] if exp["op"] in op_map else exp["op"]
    return " ".join([
        format_something(exp["left"][0], known_variables),
        operation,
        format_something(exp["right"][0], known_variables)])


def format_func(func, known_variables):
    function_name = func["func"]
    args = func["args"]
    formated_args = [format_something(arg, known_variables) for arg in args]
    return function_name + "(" + ",".join(formated_args) + ")"


def format_sum(func, known_variables):
    domain = func["belong"]
    domain_variables = [v['model_variable'] for v in domain["variables"]]
    all_known_variables = known_variables + domain_variables
    if len(domain_variables) == 1:
        str_variables = domain_variables[0]
    else:
        str_variables = "(" + ",".join(domain_variables) + ")"
    return "sum([" + \
        format_something(func["expr"], all_known_variables) + \
        " for " + str_variables + " in model." + format_ensemble(domain["ensemble"]) + "])"


def format_ensemble(ensemble):
    if ensemble['type'] == 'ensemble_name':
        return ensemble['name']
    return "Boolean"


def format_parenthesis(expr, known_variables):
    return "(" + format_something(expr["parenthesis"], known_variables) + ")"


def format_constraint(constraint):
    left = constraint["left_expr"][0]
    condition = conditions_map[constraint["condition"]]
    right = constraint["right_expr"][0]
    domains = [format_ensemble(d["ensemble"]) for d in constraint["domains"]]
    variables = []
    for domain in constraint["domains"]:
        variables += [v['model_variable'] for v in domain["variables"]]
    str_variables = "" if len(variables) == 0 else "," + ",".join(variables)
    str_domains = "" if len(domains) == 0 else ",".join(
        ["model." + d for d in domains]) + ","
    indice = constraint["indice"].replace(".", "_")
    known_variables = variables
    return "model.constraint_" + indice + " = Constraint(" + str_domains +\
        "rule=lambda model" + str_variables + ": " + \
        format_something(left, known_variables) + " " + condition + \
        " " + format_something(right, known_variables) + ")"


def format_objective(objective):
    sense = "maximize" if objective["sense"] in [
        "max", "\\max"] else "minimize"
    expr = objective["expr"]
    return "model.objective = Objective(sense=" + sense + \
        ",rule=lambda model: " + format_something(expr, []) + ")"


def format_model(model):
    if "variables" in model and model["variables"] is not None:
        formatted_vars = format_variables(model["variables"]) + "\n"
    else:
        formatted_vars = ""
    return formatted_vars \
        + format_objective(model["objective"]) + "\n" \
        + "\n".join([format_constraint(c) for c in model["constraints"]])


def variables(model) -> Dict[str, List[str]]:
    known_variables = {}
    for variable_definition in model:
        if 'left_expr' in variable_definition:
            variable_name = variable_definition['left_expr'][0]['model_variable']
            ensembles = [e['ensemble']['name']
                         for e in variable_definition['domains']]
        else:
            variable_name = variable_definition['variables'][0]['model_variable']
            ensembles = [variable_definition['ensemble']['name']]
        known_variables[variable_name] = ensembles
    return known_variables


def format_variables(model):
    return "\n".join([format_variable(variable_definition) for variable_definition in model])


def format_variable(model):
    if 'left_expr' in model:
        variable_name = model['left_expr'][0]['model_variable']
        ensembles = ",".join(["model." + format_ensemble(domain["ensemble"])
                             for domain in model['domains']])
        return f"model.{variable_name} = Var({ensembles}, domain=NonNegativeReals)"
    variable_name = model['variables'][0]['model_variable']
    if 'content' in model['ensemble']:
        # Only support 'content': [0,1]
        domains = "domain=Boolean"
        ensembles = []
    else:
        ensemble_name = model['ensemble']['name']
        domains = ""
        ensembles = []
        if ensemble_name == "PositiveIntegers":
            domains = "domain=PositiveIntegers"
        else:
            ensembles = [ensemble_name]
    for domain in model['domains']:
        ensembles.append(domain['ensemble']['name'])
    joined_ensembles = ",".join(["model." + e for e in ensembles])
    separator = ""
    if joined_ensembles != "" and domains != "":
        separator = ", "
    return f"model.{variable_name} = Var({joined_ensembles}{separator}{domains})"
