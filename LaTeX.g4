/*
 ANTLR4 LaTeX Math Grammar

 Ported from latex2sympy by @augustt198 https://github.com/augustt198/latex2sympy See license in
 LICENSE.txt
 */

/*
 After changing this file, it is necessary to run `python setup.py antlr` in the root directory of
 the repository. This will regenerate the code in `sympy/parsing/latex/_antlr/*.py`.
 */

grammar LaTeX;

// options {
// 	language = Python2;
// }

WS: [ \t\r\n]+ -> skip;
THINSPACE: ('\\,' | '\\thinspace') -> skip;
MEDSPACE: ('\\:' | '\\medspace') -> skip;
THICKSPACE: ('\\;' | '\\thickspace') -> skip;
QUAD: '\\quad' -> skip;
QQUAD: '\\qquad' -> skip;
NEGTHINSPACE: ('\\!' | '\\negthinspace') -> skip;
NEGMEDSPACE: '\\negmedspace' -> skip;
NEGTHICKSPACE: '\\negthickspace' -> skip;
CMD_LEFT: '\\left' -> skip;
CMD_RIGHT: '\\right' -> skip;

IGNORE:
	(
		'\\vrule'
		| '\\vcenter'
		| '\\vbox'
		| '\\vskip'
		| '\\vspace'
		| '\\hfil'
		| '\\*'
		| '\\-'
		| '\\.'
		| '\\/'
		| '\\"'
		| '\\('
		| '\\='
		| '&'
		| '\\begin{align*}'
		| '\\begin{align}'
		| '\\end{align}'
		| '\\\\'
		| '%' ~[\r\n]*
		| '\\limits'
		| '\\nonumber \\\\\n'
	) -> skip;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
CUP: '\\cup';
MINUS: '\\setminus';

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACE_LITERAL: '\\{';
R_BRACE_LITERAL: '\\}';
L_BRACKET: '[';
R_BRACKET: ']';

BAR: '|';

R_BAR: '\\right|';
L_BAR: '\\left|';

L_ANGLE: '\\langle';
R_ANGLE: '\\rangle';
FUNC_LIM: '\\lim';
LIM_APPROACH_SYM:
	'\\to'
	| '\\rightarrow'
	| '\\Rightarrow'
	| '\\longrightarrow'
	| '\\Longrightarrow';
FUNC_INT: '\\int';
FUNC_SUM: '\\sum';
FUNC_PROD: '\\prod';

FUNC_EXP: '\\exp';
FUNC_LOG: '\\log';
FUNC_LN: '\\ln';
FUNC_SIN: '\\sin';
FUNC_COS: '\\cos';
FUNC_TAN: '\\tan';
FUNC_CSC: '\\csc';
FUNC_SEC: '\\sec';
FUNC_COT: '\\cot';

FUNC_ARCSIN: '\\arcsin';
FUNC_ARCCOS: '\\arccos';
FUNC_ARCTAN: '\\arctan';
FUNC_ARCCSC: '\\arccsc';
FUNC_ARCSEC: '\\arcsec';
FUNC_ARCCOT: '\\arccot';

FUNC_SINH: '\\sinh';
FUNC_COSH: '\\cosh';
FUNC_TANH: '\\tanh';
FUNC_ARSINH: '\\arsinh';
FUNC_ARCOSH: '\\arcosh';
FUNC_ARTANH: '\\artanh';

FUNC_MIN: '\\min';
FUNC_MAX: '\\max';

L_FLOOR: '\\lfloor';
R_FLOOR: '\\rfloor';
L_CEIL: '\\lceil';
R_CEIL: '\\rceil';

FUNC_SQRT: '\\sqrt';
FUNC_OVERLINE: '\\overline' | '\\bar';
FUNC_UNDERLINE: '\\underline';
FUNC_TILDE: '\\tilde';
FUNC_MATHCAL: '\\mathcal';
FUNC_MATHBB: '\\mathbb';

FUNC_FORMAT:
	FUNC_OVERLINE
	| FUNC_UNDERLINE
	| FUNC_TILDE
	;

CMD_TIMES: '\\times';
CMD_CDOT: '\\cdot';
CMD_DIV: '\\div';
CMD_FRAC: '\\frac';
CMD_BINOM: '\\binom';
CMD_DBINOM: '\\dbinom';
CMD_TBINOM: '\\tbinom';

CMD_MATHIT: '\\mathit';

CMD_TOKEN: '\\newcommand';

UNDERSCORE: '_';
CARET: '^';
COLON: ':';
ESCAPED_UNDERSCORE: '\\_';

fragment WS_CHAR: [ \t\r\n];
DIFFERENTIAL: 'd' WS_CHAR*? ([a-zA-Z] | '\\' [a-zA-Z]+);

LETTER: [a-zA-Z\u03B1-\u03C9\u0391-\u03A9'] | ESCAPED_UNDERSCORE;
fragment DIGIT: [0-9];
NUMBER:
	DIGIT+ (',' DIGIT DIGIT DIGIT)*
	| DIGIT* (',' DIGIT DIGIT DIGIT)* '.' DIGIT+;
WORD: LETTER (LETTER | NUMBER)*;

EQUAL: (('&' WS_CHAR*?)? '=') | ('=' (WS_CHAR*? '&')?);
NEQ: '\\neq';

LT: '<';
LTE: ('\\leq' | '\\le' | LTE_Q | LTE_S);
LTE_Q: '\\leqq';
LTE_S: '\\leqslant';

GT: '>';
GTE: ('\\geq' | '\\ge' | GTE_Q | GTE_S);
GTE_Q: '\\geqq';
GTE_S: '\\geqslant';

BANG: '!';

SYMBOL: '\\' [a-zA-Z]+;

atom: WORD 
  | LETTER
	| SYMBOL
	| NUMBER
	| DIFFERENTIAL
	| FUNC_MATHCAL L_BRACE atom R_BRACE // Cosmetic functions
	| FUNC_MATHBB L_BRACE atom R_BRACE // Real/Integer domains
	// | mathit
	// | bra
	// | ket
	;

// bra: L_ANGLE expr (R_BAR | BAR);
// ket: (L_BAR | BAR) expr R_ANGLE;

condition: EQUAL | LT | LTE | GT | GTE | NEQ;


// mathit: CMD_MATHIT L_BRACE mathit_text R_BRACE;
// mathit_text: LETTER*;

sequence_of_atoms: expr  (',' sequence_of_atoms)? ;

func_format: (FUNC_OVERLINE | FUNC_UNDERLINE | FUNC_TILDE) L_BRACE base = expr R_BRACE;

exp: (var | func_format exposants);

expr_with_parenthesis: L_PAREN expr R_PAREN;

expr: 
	expr_with_parenthesis
	| left=expr op=(MUL | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV | COLON | ADD | SUB) right=expr
	| func_no_sub_sup
	| func
	| exp
	;

ens: ens_name=atom ((CUP | SUB | MINUS) ens)? | (L_BRACE | '\\{') atom (',' atom)* (R_BRACE | '\\}');
var: atom exposants;

subexpr: UNDERSCORE (atom | expr | L_BRACE sequence_of_atoms R_BRACE);
supexpr: CARET (atom | expr | L_BRACE sequence_of_atoms R_BRACE);
exposants: supexpr? subexpr? | subexpr? supexpr?;

sequence_of_variables: var  (',' sequence_of_variables)? ;
variables: var | L_PAREN sequence_of_variables R_PAREN;
belong: ((variables '|')? variable=variables '\\in' ensemble=ens | symbol=SYMBOL) (',' domains)? (',' indice)?;
domain: '\\forall' variable=variables ('\\in' ensemble=ens)?;

domains: 
	domain 
	| domain (',' domains);

label: (atom | '_' | '-' | ':')+;

indice: L_PAREN ind=NUMBER R_PAREN | '\\label' L_BRACE label R_BRACE ;

constraint: left=expr condition right=expr ','? domains? ','? indice?;

objective: sense=('min' | 'max' | '\\min' | '\\max') expr;

content: atom | belong | ens | expr;
command: CMD_TOKEN L_BRACE name=SYMBOL R_BRACE L_BRACE content R_BRACE;

commands: command*;

vardefs: 'vars' (constraint | belong )*;

model: commands objective ('s.t.' | 'st.') constraint* vardefs;


// math: relation;

// relation:
// 	relation (EQUAL | LT | LTE | GT | GTE | NEQ) relation
// 	| expr;

equality: expr EQUAL expr;

// expr: additive;

// additive: additive (ADD | SUB) additive | mp;

// // mult part
// mp:
// 	mp (MUL | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV | COLON) mp
// 	| unary;

// mp_nofunc:
// 	mp_nofunc (
// 		MUL
// 		| CMD_TIMES
// 		| CMD_CDOT
// 		| DIV
// 		| CMD_DIV
// 		| COLON
// 	) mp_nofunc
// 	| unary_nofunc;

// unary: (ADD | SUB) unary | postfix+;

// unary_nofunc:
// 	(ADD | SUB) unary_nofunc
// 	| postfix postfix_nofunc*;

// postfix: exp postfix_op*;
// postfix_nofunc: exp_nofunc postfix_op*;
// postfix_op: BANG | eval_at;

// eval_at:
// 	BAR (eval_at_sup | eval_at_sub | eval_at_sup eval_at_sub);

// eval_at_sub: UNDERSCORE L_BRACE (expr | equality) R_BRACE;

// eval_at_sup: CARET L_BRACE (expr | equality) R_BRACE;

// sequence_of_atoms: atom  (',' sequence_of_atoms)? ;

// exp: 
// 	exp CARET (atom | L_BRACE expr R_BRACE ) subexpr? # CaretExp
// 	| comp                                            # CompExp
// 	;

// exp_nofunc:
// 	exp_nofunc CARET (atom | L_BRACE expr R_BRACE) subexpr?
// 	| comp_nofunc;

// comp:
// 	group
// 	| abs_group
// 	| func
// 	| atom
// 	| frac
// 	| binom
// 	| floor
// 	| ceil;

// comp_nofunc:
// 	group
// 	| abs_group
// 	| atom
// 	| frac
// 	| binom
// 	| floor
// 	| ceil;

// group:
// 	L_PAREN expr R_PAREN
// 	| L_BRACKET expr R_BRACKET
// 	| L_BRACE expr R_BRACE
// 	| L_BRACE_LITERAL expr R_BRACE_LITERAL;

// abs_group: BAR expr BAR;

// atom: (LETTER | SYMBOL) subexpr?
// 	| NUMBER
// 	| DIFFERENTIAL
// 	| mathit
// 	| bra
// 	| ket;

// bra: L_ANGLE expr (R_BAR | BAR);
// ket: (L_BAR | BAR) expr R_ANGLE;

// mathit: CMD_MATHIT L_BRACE mathit_text R_BRACE;
// mathit_text: LETTER*;

frac:
	CMD_FRAC L_BRACE upper = expr R_BRACE L_BRACE lower = expr R_BRACE;

binom:
	(CMD_BINOM | CMD_DBINOM | CMD_TBINOM) L_BRACE n = expr R_BRACE L_BRACE k = expr R_BRACE;

floor: L_FLOOR val = expr R_FLOOR;
ceil: L_CEIL val = expr R_CEIL;

func_normal:
	FUNC_EXP
	| FUNC_LOG
	| FUNC_LN
	| FUNC_SIN
	| FUNC_COS
	| FUNC_TAN
	| FUNC_CSC
	| FUNC_SEC
	| FUNC_COT
	| FUNC_ARCSIN
	| FUNC_ARCCOS
	| FUNC_ARCTAN
	| FUNC_ARCCSC
	| FUNC_ARCSEC
	| FUNC_ARCCOT
	| FUNC_SINH
	| FUNC_COSH
	| FUNC_TANH
	| FUNC_ARSINH
	| FUNC_ARCOSH
	| FUNC_ARTANH
	| FUNC_MIN
	| FUNC_MAX
	;

func_no_sub_sup:
	FUNC_SUM UNDERSCORE L_BRACE sumdomain = belong R_BRACE base = expr
	;

func:
	func_normal (subexpr? supexpr? | supexpr? subexpr?) (
		L_PAREN func_arg R_PAREN
		// | func_arg_noparens
	)
	// | (LETTER | SYMBOL) subexpr? // e.g. f(x)
	| L_PAREN args R_PAREN
	// | FUNC_INT (subexpr supexpr | supexpr subexpr)? (
	// 	additive? DIFFERENTIAL
	// 	| frac
	// 	| additive
	// )
	| FUNC_SQRT (L_BRACKET root = expr R_BRACKET)? L_BRACE base = expr R_BRACE
	// | (FUNC_SUM | FUNC_PROD) (subeq supexpr | supexpr subeq) mp
	// | FUNC_LIM limit_sub mp
	;

args: (expr ',' args) | expr;

limit_sub:
	UNDERSCORE L_BRACE (LETTER | SYMBOL) LIM_APPROACH_SYM expr (
		CARET L_BRACE (ADD | SUB) R_BRACE
	)? R_BRACE;

func_arg: expr | (expr ',' func_arg);
// func_arg_noparens: mp_nofunc;

// subexpr: UNDERSCORE (atom | L_BRACE expr R_BRACE | L_BRACE sequence_of_atoms R_BRACE );
// supexpr: CARET (atom | L_BRACE expr R_BRACE);

subeq: UNDERSCORE L_BRACE equality R_BRACE;
supeq: UNDERSCORE L_BRACE equality R_BRACE;
