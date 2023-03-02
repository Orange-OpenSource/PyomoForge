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
import pprint
from antlr4 import CommonTokenStream, InputStream
from latex.LaTeXLexer import LaTeXLexer
from latex.LaTeXParser import LaTeXParser
from latex.LaTeXVisitor import LaTeXVisitor
import re
import random
import string

pp = pprint.PrettyPrinter()

mathcal_pattern = re.compile('\\\\mathcal{([^}]*)}')
mathbb_pattern = re.compile('\\\\mathbb{([^}]*)}')


def remove_mathcal(atom):
    groups = mathcal_pattern.match(atom)
    if groups is None:
        return atom
    return groups.group(1)


class PyomoVisitor(LaTeXVisitor):
    def __init__(self):
        LaTeXVisitor.__init__(self)
        self.stack = []
        self.commands = {
            "\\alpha": "α",
            "\\delta": "δ",
            "\\omega": "ω",
            "\\Omega": "Ω",
            "\\pi": "π",
            "\\sigma": "σ",
        }

    def visitObjective(self, ctx: LaTeXParser.ObjectiveContext):
        return [{
            "sense": ctx.sense.text,
            "expr": ctx.expr().accept(self)[0],
        }]

    def substitute(self, input_atom: str):
        groups = mathbb_pattern.match(input_atom)
        if groups is not None:
            return "PositiveIntegers"
        atom = remove_mathcal(input_atom)
        atom = atom.replace("'", "_prime")
        atom = atom.replace("\\_", "_")
        while isinstance(atom, str) and atom in self.commands:
            atom = self.commands[atom]
        return atom

    def visitAtom(self, ctx: LaTeXParser.AtomContext):
        atom = self.substitute(ctx.getText())
        while isinstance(atom, str) and atom in self.commands:
            atom = self.commands[atom]
        return [atom]

    def visitEns(self, ctx: LaTeXParser.EnsContext):
        if ctx.ens_name is None:
            return [{
                'type': 'ensemble_definition',
                'content': [atom.accept(self)[0] for atom in ctx.atom()]
            }]
        atom = ctx.ens_name.accept(self)[0]
        # Case T \ {0}
        if ctx.CUP() is not None:
            right = ctx.ens().accept(self)[0]
            removed_elements = "_".join(right['content'])
            return [{
                'type': 'ensemble_name',
                'name': atom + '_minus_' + removed_elements
            }]
        if isinstance(atom, dict) and "type" in atom:
            return [atom]
        return [{
            'type': 'ensemble_name',
            'name': atom
        }]

    def visitExpr(self, ctx: LaTeXParser.ExprContext):
        if ctx.op is not None:
            res = {
                "left": ctx.left.accept(self),
                "op": ctx.op.text,
                "right": ctx.right.accept(self),
            }
            return [res]
        return self.visitChildren(ctx)

    def visitExpr_with_parenthesis(self, ctx: LaTeXParser.Expr_with_parenthesisContext):
        return [{
            "parenthesis": ctx.expr().accept(self)[0],
        }]

    # Visit a parse tree produced by LaTeXParser#subexpr.
    def visitSubexpr(self, ctx: LaTeXParser.SubexprContext):
        if ctx.atom() is not None:
            return [{'model_variable': ctx.atom().accept(self)[0], 'local_variables': []}]
        if ctx.expr() is not None:
            return ctx.expr().accept(self)[0]
        return ctx.sequence_of_atoms().accept(self)

    # Visit a parse tree produced by LaTeXParser#supexpr.
    def visitSupexpr(self, ctx: LaTeXParser.SupexprContext):
        if ctx.atom() is not None:
            return [{'model_variable': ctx.atom().accept(self)[0], 'local_variables': []}]
        if ctx.expr() is not None:
            return ctx.expr().accept(self)
        return ctx.sequence_of_atoms().accept(self)

    def visitExposants(self, ctx: LaTeXParser.ExposantsContext):
        local_variables = []
        if ctx.supexpr() is not None:
            sup = ctx.supexpr().accept(self)
            local_variables += sup
        if ctx.subexpr() is not None:
            sub = ctx.subexpr().accept(self)
            local_variables += sub
        return local_variables

    def visitVar(self, ctx: LaTeXParser.VarContext):
        model_variable = ctx.atom().accept(self)[0]
        if isinstance(model_variable, dict) and (
                "model_variable" in model_variable or "variables" in model_variable):
            # Atom (like \gig) has been substituted by more complex structure (like g \in G)
            return [model_variable]
        local_variables = ctx.exposants().accept(self)
        return [{
            "model_variable": model_variable,
            "local_variables": local_variables
        }]

    def visitExp(self, ctx: LaTeXParser.ExpContext):
        if ctx.var() is not None:
            return ctx.var().accept(self)
        model_variable = ctx.func_format().accept(self)
        local_variables = ctx.exposants().accept(self)
        exp = {
            "model_variable": model_variable[0],
            "local_variables": local_variables
        }
        return [exp]

    def visitCondition(self, ctx: LaTeXParser.ConditionContext):
        return ctx.getText()

    def visitIndice(self, ctx: LaTeXParser.IndiceContext):
        if ctx.label() is not None:
            labels = ctx.label().accept(self)
            return "_".join(labels).replace('-', '_').replace(":", "_")
        return ctx.ind.text

    def visitConstraint(self, ctx: LaTeXParser.ConstraintContext):
        left_expr = ctx.left.accept(self)
        condition = ctx.condition().accept(self)
        right_expr = ctx.right.accept(self)
        ctx_domains = ctx.domains()
        domains = [] if ctx_domains is None else ctx_domains.accept(self)
        if ctx.indice() is None:
            indice = 'no_indice_' + \
                ''.join(random.choice(string.ascii_lowercase)
                        for i in range(8))
        else:
            indice = ctx.indice().accept(self)
        return [{
            "left_expr": left_expr,
            "condition": condition,
            "right_expr": right_expr,
            "domains": domains,
            "indice": indice,
        }]

    def visitCommand(self, ctx: LaTeXParser.CommandContext):
        name = ctx.name.text
        content = ctx.content().accept(self)[0]
        self.commands[name] = content

    def visitFunc_format(self, ctx: LaTeXParser.Func_formatContext):
        if ctx.getChild(0) in [ctx.FUNC_OVERLINE(), ctx.FUNC_UNDERLINE()]:
            res = self.visitChildren(ctx)
            return [res[0]["model_variable"] + "_"]
        if ctx.getChild(0) in [ctx.FUNC_OVERLINE(), ctx.FUNC_UNDERLINE()]:
            res = self.visitChildren(ctx)
            return ["tilde_" + res[0]["model_variable"]]
        return self.visitChildren(ctx)

    def visitFunc(self, ctx: LaTeXParser.FuncContext):
        if ctx.func_normal() is not None:
            function_name = ctx.func_normal().getText()
            function_name = function_name.replace("\\", "")
            return [{
                "func": function_name,
                "args": ctx.func_arg().accept(self),
            }]
        return self.visitChildren(ctx)

    def visitFunc_no_sub_sup(self, ctx: LaTeXParser.Func_no_sub_supContext):
        if ctx.getChild(0) == ctx.FUNC_SUM():
            return [{
                "func": "sum",
                "belong": ctx.belong().accept(self)[0],
                "expr": ctx.expr().accept(self)[0],
            }]
        return self.visitChildren(ctx)

    def visitDomain(self, ctx: LaTeXParser.DomainContext):
        # Case \forall \sis
        # We expect the variable to be a macro and to be extended
        if ctx.ensemble is None:
            return ctx.variable.accept(self)
        ensemble = ctx.ensemble.accept(self)
        return [{
            "variables": ctx.variable.accept(self),
            "ensemble": ensemble[0],
        }]

    def visitBelong(self, ctx: LaTeXParser.BelongContext):
        if ctx.symbol is not None:
            return [self.substitute(ctx.symbol.text)]
        ensemble = ctx.ensemble.accept(self)
        domains = []
        if ctx.domains() is not None:
            domains = ctx.domains().accept(self)
        return [{
            "variables": ctx.variable.accept(self),
            "ensemble": ensemble[0],
            "domains": domains,
        }]

    def visitModel(self, ctx: LaTeXParser.ModelContext):
        # Force commands to be visited
        # Commands is internally used for substituting macros by their values
        ctx.commands().accept(self)
        vardefs = ctx.vardefs()
        variables = [] if vardefs is None else vardefs.accept(self)
        return {
            "objective": ctx.objective().accept(self)[0],
            "constraints": [c.accept(self)[0] for c in ctx.constraint()],
            "variables": variables,
        }

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            return nextResult
        if nextResult is None:
            return aggregate
        return aggregate + nextResult


def read_model(tex, f_model):
    """Parse a TeX content to a model

    Args:
        tex (str): _description_
        f_model (function): function to indicate from which token to start

    Returns:
        _type_: _description_
    """
    input_stream = InputStream(tex)
    lexer = LaTeXLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LaTeXParser(stream)
    tree = f_model(parser)
    visitor = PyomoVisitor()
    return visitor.visit(tree)
