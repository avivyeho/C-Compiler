grammar MyGrammar;

mainprogram     : (INCLUDE)? startrule+ EOF;

startrule       : operations
                ;

operations      : declaration SEMICOLON
                | assignment_statement SEMICOLON
                | function
                ;

function        : (declaration_specifier|VOID) ID LEFT_PAREN (parameter_list)? RIGHT_PAREN (fct_scope| SEMICOLON)
                ;

parameter_list  : parameter (COMMA parameter)*
                ;

fct_scope       : LEFT_BRACKET (statement| declaration SEMICOLON | fct_call SEMICOLON | assignment_statement SEMICOLON)* RIGHT_BRACKET
                ;

parameter       : declaration_specifier ID
                ;

fct_call        : PRINTF LEFT_PAREN STRING ((COMMA assignment_expr)+)? RIGHT_PAREN
                | SCANF LEFT_PAREN STRING (COMMA AMPERSAND ID)+ RIGHT_PAREN
                | factor_fct_call
                ;


statement       : if_statement
                | while_loop
                | for_loop
                | terminate_statement
                ;

if_statement    : IF condition scope (ELSE scope)?
                ;

while_loop      : WHILE condition scope
                ;

for_loop        : FOR for_condition scope
                ;

terminate_statement
                : BREAK SEMICOLON
                | CONTINUE SEMICOLON
                | RETURN (assignment_expr)? SEMICOLON
                ;

condition       : LEFT_PAREN assignment_expr RIGHT_PAREN
                ;

increment       : (INCR|DECR) identifier
                | identifier  (INCR|DECR)
                ;


for_condition   : LEFT_PAREN (declaration|assignment_statement) SEMICOLON comp_expr SEMICOLON increment RIGHT_PAREN
                ;

scope           : LEFT_BRACKET (declaration SEMICOLON | fct_call SEMICOLON | statement | assignment_statement SEMICOLON)* RIGHT_BRACKET
                ;

declaration     : declaration_specifier identifier ((COMMA identifier)*?)
                | declaration_specifier identifier ASSIGNMENT (assignment_expr|array_initialize)
                ;

assignment_statement
                : (pointer_operator)? identifier ASSIGNMENT (assignment_expr|array_initialize)
                | assignment_expr
                ;

declaration_specifier
                : CONST type_specifier
                | type_specifier
                ;

type_specifier  : INT
                | FLOAT
                | CHAR
                | type_specifier pointer_operator
                ;

pointer_operator
                : MULT // POINTER
                | AMPERSAND
                | MULT MULT
                ;

assignment_expr : and_expr
                ;

and_expr        : or_expr
                | and_expr AND or_expr
                ;

or_expr         : comp_expr
                | or_expr OR comp_expr
                ;


comp_expr       : add_expr
                | add_expr comp_operator add_expr
                ;

add_expr        : mult_expr
                | add_expr add_operator mult_expr
                ;

mult_expr       : factor
                | mult_expr mult_operator factor
                ;

factor_fct_call : ID LEFT_PAREN (assignment_expr (COMMA assignment_expr)*)? RIGHT_PAREN
                ;

factor          : (NOT)? LEFT_PAREN assignment_expr RIGHT_PAREN (INCR|DECR)?
                | STRING | CHAR_STR
                | (id_operators)? identifier (INCR|DECR)?
                | (add_operator)? constant
                | factor_fct_call
                ;

array_initialize
                : LEFT_BRACKET factor( COMMA factor)* RIGHT_BRACKET
                ;

comp_operator   : LESS
                | GREATER
                | EQUAL
                | GREATER_EQUAL
                | LESS_EQUAL
                | N_EQUAL
                ;


id_operators    : INCR
                | DECR
                | PLUS
                | MIN
                | NOT
                | MULT
                | AMPERSAND
                ;


add_operator    : PLUS
                | MIN
                ;

mult_operator   : MULT
                | DIV
                | MOD
                ;

constant
                : INT_CONSTANT
                | FLOAT_CONSTANT
                ;

identifier      : ID (LEFT_SQUARE INT_CONSTANT RIGHT_SQUARE)?
                ;


// ----------------------------------------------------------------
INT : 'int' ;
FLOAT : 'float' ;
CHAR : 'char' ;
CONST : 'const' ;
VOID : 'void';
INCLUDE: '#include <stdio.h>';

LEFT_PAREN : '(' ;
RIGHT_PAREN : ')' ;
LEFT_BRACKET : '{' ;
RIGHT_BRACKET : '}' ;
LEFT_SQUARE : '[';
RIGHT_SQUARE : ']';


SEMICOLON : ';' ;
COMMA : ',' ;
STRING: '"' .*? '"';
CHAR_STR: '\'' . '\'';

ASSIGNMENT : '=' ;
PRINTF : 'printf' ;
SCANF: 'scanf';

EQUAL : '==';
N_EQUAL : '!=';

LESS : '<';
LESS_EQUAL : '<=';
GREATER : '>';
GREATER_EQUAL : '>=';

INCR : '++' ;
DECR : '--' ;

PLUS : '+';
MIN : '-' ;
DIV   : '/' ;
NOT : '!';
MOD : '%' ;
MULT : '*' ;
AMPERSAND : '&' ;


OR  : 'or' | '||' ;
AND : 'and' | '&&' ;

IF  : 'if' ;
ELSE : 'else' ;
WHILE : 'while' ;
FOR   : 'for' ;

BREAK : 'break';
CONTINUE : 'continue' ;
RETURN   : 'return' ;

ID : [a-zA-Z_][a-zA-Z0-9_]*;
INT_CONSTANT : [0-9][0-9]*;
FLOAT_CONSTANT : [0-9]* '.' [0-9]+;

MULTI_COMMENT : '/*' .*? '*/' -> skip;
SINGLE_COMMENT: '//' .*? '\n' -> skip;
WS: [ \n\t\r]+ -> skip;