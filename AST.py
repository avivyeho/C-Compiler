import sys
from antlr4 import *
from antlr4.tree.Tree import ParseTree
from ASTClasses import *
from TestSymbolTable import SymbolTable


class AST:
    """
    self.root: the root of the tree
    """

    def __init__(self, t: ParseTree):
        """
        contents: a string, the contents of the root node
        """
        self.counter = [0]
        self.root = generateASTfromParseTree(self.counter, t)
        self.symbolTableRoot = makeSymbolTable(self)

    def toDot(self, filenaam):
        """
        filenaam:string
        voegt een graph AST toe aan de file "filenaam". Graph AST is de Dot code voor de visuele representatie van  AST
        :return: niets
        """
        f = open(filenaam, "w")
        f.write("graph AST { \n" + self.root.nodeToDot(filenaam) + "}\n")
        f.close()


"""
the following functions generate the the AST tree, with every node being an instance 
of a class derived from the Node class (in ASTClasses.py). Exactly which specific 
derived class a particular node is is dependant on the rule the node comes from  
"""


def generateASTfromParseTree(counter, t: ParseTree):
    ast_root = MainProgram(counter)

    for child in t.children:
        if not isinstance(child, TerminalNode):
            child_rule = t.parser.ruleNames[child.getRuleContext().getRuleIndex()]
            if child_rule == "startrule":
                ast_root.children.append(makeOperations(counter, ast_root, child))
        else:
            rule = t.parser.symbolicNames[child.symbol.type]
            if rule == "INCLUDE":
                ast_root.children.append(Include(counter, ast_root, child.getText()))
    return ast_root


def makeIdentifier(counter, parent_node: Node, t: ParseTree):
    node = Identifier(counter, parent_node, t.children[0].getText())
    if len(t.children) != 1:
        node.hasarraybox = True
        node.arraybox = t.children[2].getText()
    return node


def makeArray_initialize(counter, parent_node: Node, t: ParseTree):
    node = ArrayList(counter, parent_node)

    for child in t.children:
        if not isinstance(child, TerminalNode):
            node.children.append(makeFactor(counter, node, child))
    return node


def makeDeclaration(counter, parent_node: Node, t: ParseTree):
    node = Declaration(counter, parent_node)
    assignment = False
    typ = makeType(counter, None, t.children[0])
    node.children.append(makeIdentifier(counter, node, t.children[1]))
    node.children[0].type = typ.contents
    node.children[0].isConst = typ.isConst
    for i in range(2, len(t.children)):
        if not isinstance(t.children[i], TerminalNode):
            child_rule = t.parser.ruleNames[t.children[i].getRuleContext().getRuleIndex()]
            if child_rule == "assignment_expr":
                node.children.append(makeAssignmentExpression(counter, node, t.children[i]))
            elif child_rule == "array_initialize":
                node.children.append(makeArray_initialize(counter, node, t.children[i]))
            else:
                node.children.append(makeIdentifier(counter, node, t.children[i]))
    return node


def makeDeclarator(counter, parent_node: Node, t: ParseTree):
    """
    :return: returns a list of nodes
    """
    identifier = makeIdentifier(counter, parent_node, t.children[0])

    if len(t.children) == 3:
        # declarator -> identifier '=' assignment_expr
        assignment = makeAssignmentExpression(counter, parent_node, t.children[2])
        return [identifier, assignment]
    else:
        # declarator -> identifier
        return [identifier]


def makeType(counter, parent_node, t: ParseTree):
    if isinstance(t.children[0], TerminalNode):
        # declaration_specifier -> 'const' type_specifier
        node = Type(counter, parent_node, getTypeSpecifier(t.children[1]), True)

    else:
        # declaration_specifier -> type_specifier
        node = Type(counter, parent_node, getTypeSpecifier(t.children[0]), False)

    return node


def makeParameter(counter, parent_node: Node, t: ParseTree):
    node = Parameter(counter, parent_node, t.children[1].getText())
    type = makeType(counter, None, t.children[0])
    node.type = type.contents
    node.contentsIsConst = type.isConst
    return node


def makeParameterList(counter, parent_node: Node, t: ParseTree):
    node = ParameterList(counter, parent_node)

    for child in t.children:
        if not isinstance(child, TerminalNode):
            node.children.append(makeParameter(counter, node, child))
    return node


def makeTerminateStatement(counter, parent_node: Node, t: ParseTree):
    node = TerminateStatement(counter, parent_node, t.children[0].getText())
    if len(t.children) != 2:
        node.children.append(makeAssignmentExpression(counter, node, t.children[1]))
    return node


def makeIncrement(counter, parent_node: Node, t: ParseTree):
    if isinstance(t.children[0], TerminalNode):
        unary = UnaryOperator(counter, parent_node, t.children[0].getText())
        unary.children.append(makeIdentifier(counter, unary, t.children[1]))
    else:
        unary = UnaryOperator(counter, parent_node, t.children[1].getText())
        unary.children.append(makeIdentifier(counter, unary, t.children[0]))
    return unary

def makeForCondition(counter, parent_node: Node, t: ParseTree):
    node = ForCondition(counter, parent_node)
    rule = t.parser.ruleNames[t.children[1].getRuleContext().getRuleIndex()]
    if rule == "declaration":
        node.children.append(makeDeclaration(counter, node, t.children[1]))
    else:
        node.children.append(makeAssignmentStatement(counter, node, t.children[1]))
    node.children.append(makeCompExpr(counter, node, t.children[3]))
    node.children.append(makeIncrement(counter, node, t.children[5]))
    return node


def makeForLoop(counter, parent_node: Node, t: ParseTree):
    node = ForLoop(counter, parent_node)
    node.children.append(makeForCondition(counter, node, t.children[1]))
    node.children.append(makeScope(counter, node, t.children[2]))
    return node


def makeCondition(counter, parent_node: Node, t: ParseTree):
    node = Condition(counter, parent_node)
    node.children.append(makeAssignmentExpression(counter, node, t.children[1]))
    return node


def makeWhileLoop(counter, parent_node: Node, t: ParseTree):
    node = WhileLoop(counter, parent_node)
    node.children.append(makeCondition(counter, node, t.children[1]))
    node.children.append(makeScope(counter, node, t.children[2]))
    return node


def makeIfStatement(counter, parent_node: Node, t: ParseTree):
    node = IfStatement(counter, parent_node)
    node.children.append(makeCondition(counter, node, t.children[1]))
    node.children.append(makeScope(counter, node, t.children[2]))
    if len(t.children) == 5:
        node.children.append(makeScope(counter, node, t.children[4]))
        node.children[len(node.children)-1].isElse = True
    return node


def makeStatement(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "if_statement":
        node = makeIfStatement(counter, parent_node, t.children[0])
    elif rule == "while_loop":
        node = makeWhileLoop(counter, parent_node, t.children[0])
    elif rule == "for_loop":
        node = makeForLoop(counter, parent_node, t.children[0])
    elif rule == "terminate_statement":
        node = makeTerminateStatement(counter, parent_node, t.children[0])
    return node


def makeFctCall(counter, parent_node: Node, t: ParseTree):
    if not isinstance(t.children[0], TerminalNode):
        node = makeFctCall(counter, parent_node, t.children[0])
    else:
        node = FctCall(counter, parent_node, t.children[0].getText())
        ampersand = False
        for i in range(1, len(t.children)):
            if isinstance(t.children[i], TerminalNode):
                rule = t.parser.symbolicNames[t.children[i].symbol.type]
                if rule == "STRING":
                    childnode = Constant(counter, node, t.children[i].getText())
                    childnode.type = "string"
                    node.children.append(childnode)
                elif rule == "AMPERSAND":
                    ampersand = True
                elif rule == "ID":
                    if ampersand:
                        ampersand = False
                        childnode = UnaryOperator(counter, node, "&")
                        childnode.children.append(Identifier(counter, childnode, t.children[i].getText()))
                    else:
                        childnode = Identifier(counter, node, t.children[i].getText())
                    node.children.append(childnode)

            else:
                child_rule = t.parser.ruleNames[t.children[i].getRuleContext().getRuleIndex()]
                if child_rule == "assignment_expr":
                    if ampersand:
                        ampersand = False
                        childnode = UnaryOperator(counter, node, "&")
                        childnode.children.append(makeAssignmentExpression(counter, childnode, t.children[i]))
                    else:
                        childnode = makeAssignmentExpression(counter, node, t.children[i])
                    node.children.append(childnode)
                if child_rule == "factor":
                    childnode = makeFactor(counter, node, t.children[i])
                    node.children.append(childnode)

    return node


def makeScope(counter, parent_node: Node, t: ParseTree, parameterlist: Node = None):
    node = Scope(counter, parent_node)
    if parameterlist is not None:
        node.children.append(parameterlist)
        parameterlist.parent = node
    for child in t.children:
        if not isinstance(child, TerminalNode):
            child_rule = t.parser.ruleNames[child.getRuleContext().getRuleIndex()]
            if child_rule == "statement":
                node.children.append(makeStatement(counter, node, child))
            elif child_rule == "declaration":
                node.children.append(makeDeclaration(counter, node, child))
            elif child_rule == "fct_call":
                node.children.append(makeFctCall(counter, node, child))
            elif child_rule == "assignment_statement":
                node.children.append(makeAssignmentStatement(counter,node, child))
    return node


def makeFunction(counter, parent_node: Node, t: ParseTree):
    child0 = t.children[0]  # (type_specifier|VOID)
    if isinstance(child0, TerminalNode):
        type = Type(counter, None, "void", False)
    else:
        type = makeType(counter, None, child0)

    if not isinstance(t.children[3], TerminalNode):
        parameterlist = makeParameterList(counter, None, t.children[3])
        ftc_scope_nr = 5
    else:
        parameterlist = ParameterList(counter)
        ftc_scope_nr = 4

    if not isinstance(t.children[ftc_scope_nr], TerminalNode):
        node = Function(counter, parent_node, t.children[1].getText(), type.contents, type.isConst)
        scope = makeScope(counter, node, t.children[ftc_scope_nr], parameterlist)
        node.children.append(scope)
    else:
        node = FunctionDeclaration(counter, parent_node, t.children[1].getText(), type.contents, type.isConst)
        node.children.append(parameterlist)
        parameterlist.parent = node
    return node


def getTypeSpecifier(t: ParseTree):
    if isinstance(t.children[0], TerminalNode):
        return t.getText()
    else:
        pointer = makePointerOperator([0], None, t.children[1])
        return getTypeSpecifier(t.children[0]) + pointer.contents


def makeAssignmentExpression(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "and_expr":
        # assignment -> and_expr
        node = makeAndExpr(counter, parent_node, t.children[0])
    return node


def makeAndExpr(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "or_expr":
        # and_expr -> or_expr
        node = makeOrExpr(counter, parent_node, t.children[0])
    else:
        # and_expr -> and_expr AND or_expr
        node = AndExpr(counter, parent_node)

        # lhs
        child = t.children[0]
        node.children.append(makeAndExpr(counter, node, child))
        #
        # if node.children[0].contents == "+":
        #     childlist = node.children[0].children
        #     node.children = childlist

        # rhs
        child = t.children[2]
        node.children.append(makeOrExpr(counter, node, child))
    return node


def makeOrExpr(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "comp_expr":
        # or_expr -> comp_expr
        node = makeCompExpr(counter, parent_node, t.children[0])
    else:
        # or_expr -> or_expr OR comp_expr
        node = OrExpr(counter, parent_node)

        # lhs
        child = t.children[0]
        node.children.append(makeOrExpr(counter, node, child))
        #
        # if node.children[0].contadd == "+":
        #     childlist = node.children[0].children
        #     node.children = childlist

        # rhs
        child = t.children[2]
        node.children.append(makeCompExpr(counter, node, child))
    return node


def makeCompExpr(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if len(t.children)==1:
        # comp_exp -> add
        node = makeAddExpr(counter, parent_node, t.children[0])
    else:
        # comp_exp -> comp_exp add
        node = CompExpr(counter, parent_node)

        node.contents = t.children[1].children[0].getText()

        # lhs
        child = t.children[0]
        node.children.append(makeAddExpr(counter, node, child))
        #
        # if node.children[0].contents == "+":
        #     childlist = node.children[0].children
        #     node.children = childlist

        # rhs
        child = t.children[2]
        node.children.append(makeAddExpr(counter, node, child))
    return node


def makeAddExpr(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "mult_expr":
        # add_expr -> mult_expr
        node = makeMultExpr(counter, parent_node, t.children[0])
    else:
        # add_expr -> add_expr add_op term
        node = AddExpr(counter, parent_node)

        node.contents = t.children[1].children[0].getText()

        # lhs
        child = t.children[0]
        node.children.append(makeAddExpr(counter, node, child))
        #
        # if node.children[0].contents == "+":
        #     childlist = node.children[0].children
        #     node.children = childlist

        # rhs
        child = t.children[2]
        node.children.append(makeMultExpr(counter, node, child))
    return node


def makeMultExpr(counter, parent_node: Node, t: ParseTree):
    rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if rule == "factor":
        # mult_expr -> factor
        node = makeFactor(counter, parent_node, t.children[0])
    else:
        # mult_expr -> mult_expr mult_op factor
        node = MultExpr(counter, parent_node)

        node.contents = t.children[1].children[0].getText()

        # lhs
        child = t.children[0]
        node.children.append(makeMultExpr(counter, node, child))

        # if node.children[0].contents == "*":
        #     childlist = node.children[0].children
        #     node.children = childlist

        # rhs
        child = t.children[2]
        node.children.append(makeFactor(counter, node, child))
    return node


def makeIDOperators( t: ParseTree):
    if isinstance(t.children[0], TerminalNode):
        return t.children[0].getText()
    else:
        pointer = makePointerOperator([0],None,t.children[0])
        return pointer.contents


def makeFactor(counter, parent_node: Node, t: ParseTree):
    if not isinstance(t.children[0], TerminalNode):
        rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
        if rule == "constant":
            # factor -> constant
            node = makeConstant(counter, parent_node, t.children[0])
        elif rule == "identifier":
            if len(t.children)>1:
                node = UnaryOperator(counter, parent_node, t.children[1].getText())
                node.children.append(makeIdentifier(counter, node, t.children[0]))
            # factor -> identifier
            else :
                node = makeIdentifier(counter, parent_node, t.children[0])
        elif rule == "id_operators":
            # factor-> id_operators ID
            node = UnaryOperator(counter, parent_node, makeIDOperators(t.children[0]))

            node.children.append(makeIdentifier(counter, node, t.children[1]))

            # rhs
        elif rule == "add_operator":
            # factor-> id_operators ID
            node = Factor(counter, parent_node)

            node.contents = t.children[0].children[0].getText()

            node.children.append(makeConstant(counter, node, t.children[1]))
        elif rule == "factor_fct_call":
            node = makeFctCall(counter, parent_node, t.children[0])
    else:
        if t.children[0].getText() == "(":
            if len(t.children) == 4:
                # factor -> '(' assignment_expr ')' '++/--'
                node = UnaryOperator(counter, parent_node, t.children[3].getText())
                node.children.append(makeAssignmentExpression(counter, node, t.children[1]))
            else:
                # factor -> '(' assignment_expr ')'
                node = makeAssignmentExpression(counter, parent_node, t.children[1])
        elif t.children[0].getText() == "!":
            # factor -> '!''(' assignment_expr ')'
            node = UnaryOperator(counter, parent_node, "!")
            node.type = "bool"
            node.children.append(makeAssignmentExpression(counter, node, t.children[2]))
        else:
            type = t.parser.symbolicNames[t.children[0].symbol.type]
            node = Constant(counter, parent_node, t.children[0].getText())
            if type == "STRING":
                node.type = "string"
            elif type == "CHAR_STR":
                node.type = "char"
    return node


def makeConstant(counter, parent_node: Node, t: ParseTree):
    node = Constant(counter, parent_node, t.children[0].getText())

    constType = t.parser.symbolicNames[t.children[0].symbol.type]
    if constType == "INT_CONSTANT":
        node.type = "int"
    elif constType == "FLOAT_CONSTANT":
        node.type = "float"
    return node


def makePointerOperator(counter, parent_node: Node, t: ParseTree):
    if isinstance(t.children[0], TerminalNode):
        node = Type(counter, None, t.children[0].getText())
    else:
        node1 = makePointerOperator(counter, None, t.children[0])
        node2 = makePointerOperator(counter, None, t.children[1])
        node = Type(counter, None, node1.contents+node2.contents)
    return node


def makeAssignmentStatement(counter, parent_node: Node, t: ParseTree):
    child_rule = t.parser.ruleNames[t.children[0].getRuleContext().getRuleIndex()]
    if child_rule == "assignment_expr":
        node = AssignmentStatement(counter, parent_node)
        node.children.append(makeAssignmentExpression(counter,node,t.children[0]))

    else:
        node = AssignmentStatement(counter, parent_node)

        if child_rule == "pointer_operator":
            type = makePointerOperator(counter, None, t.children[0])
            node.type = type.contents
            identifier_nr = 1
        else:
            identifier_nr = 0
        node.children.append(makeIdentifier(counter, node, t.children[identifier_nr]))
        child_rule = t.parser.ruleNames[t.children[identifier_nr+2].getRuleContext().getRuleIndex()]
        if child_rule == "assignment_expr":
            node.children.append(makeAssignmentExpression(counter, node, t.children[identifier_nr+2]))
        elif child_rule == "array_initialize":
            node.children.append(makeArray_initialize(counter, node, t.children[identifier_nr+2]))
    return node


def makeOperations(counter, parent_node: Node, t: ParseTree):
    child = t.children[0].children[0]
    child_rule = t.parser.ruleNames[child.getRuleContext().getRuleIndex()]
    if child_rule == "declaration":
        return makeDeclaration(counter, parent_node, child)
    elif child_rule == "function":
        return makeFunction(counter, parent_node, child)
    elif child_rule == "assignment_statement":
        return makeAssignmentStatement(counter, parent_node, child)


def makeSymbolTable(ast):
    root = ast.root
    symbol_table = SymbolTable(root)
    symbol_table.TraverseTree(root)
    symbol_table.main_in_code()


    return symbol_table
