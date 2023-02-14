class Node:
    """
    self.contents: a string, contents of this node
    self.parent: Node, parent of this node
    self.children: list of Nodes, with list items being the children in order from left to right
    self.ID: int, a unique ID
    """

    def __init__(self, counter, parent=None, contents=""):
        self.contents = contents
        self.parent = parent
        self.children = []
        self.ID = counter[0]
        counter[0] += 1

    def nodeToDot(self, filenaam):
        """
        filenaam:string
        voegt de node en haar kinderen toe aan de file "filenaam"in Dot code voor de visuele representatie van AST
        """
        type_string = str(type(self))
        begin = int(type_string.find("."))
        end = int(type_string.find(">"))
        label = type_string[begin + 1: end - 1] + ":\n"
        label += str(self)
        outputString = "\t" + str(self.ID) + "[label=\"" + label + "\"];\n"
        if self.parent is not None:
            outputString += "\t" + str(self.parent.ID) + "--" + str(self.ID) + ";\n"
        for child in self.children:
            outputString += child.nodeToDot(filenaam)
        return outputString

    def __str__(self):
        label = ""
        if isinstance(self, Identifier):
            if self.isConst:
                label += "const "
            label += self.type + " "+self.contents
            if self.hasarraybox:
                label += "[" + str(self.arraybox) + "]"
        elif isinstance(self, Function):
            if self.isConst:
                label += "const "
            label += self.type + " " + self.contents
        elif isinstance(self, Parameter):
            if self.isConst:
                label += "const "
            label += self.type + " " + self.contents
        elif isinstance(self, Scope):
            if self.isElse:
                label += "Else-"
            label += self.contents
        elif isinstance(self, Constant):
            contents = self.contents
            quote = contents.find("\"")
            while quote != -1:
                if quote == 0:
                    contents = contents[1:]
                elif quote == len(contents)-1:
                    contents = contents[:len(contents)-1]
                else:
                    contents = contents[:quote-1] + contents[quote+1:]
                quote = contents.find("\"", quote-1)
            label += contents
        else:
            label += self.contents
        return label


class MainProgram(Node):
    """
    children : (Include)? operations+

    where operations = one of the following : Declaration, Function, AssignmentStatement
    """
    def __init__(self, counter, parent=None, contents="mainprogram"):
        super().__init__(counter, parent, contents)


class Include(Node):
    def __init__(self, counter, parent=None, contents="include"):
        super().__init__(counter, parent, contents)


class Declaration(Node):
    """
    children: Identifier assignment
            | Identifier

    where
    assignment = one of the following:  AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Constant, FctCall, Identifier,
                                        UnaryOperator, Factor

    both Identifier and the Assignment have self.type
    """
    def __init__(self, counter, parent=None, contents="Declaration"):
        super().__init__(counter, parent, contents)


class Identifier(Node):
    """
    has no children
    """
    def __init__(self, counter, parent=None, contents="ID"):
        super().__init__(counter, parent, contents)
        self.type = ""
        self.hasarraybox = False
        self.arraybox = 0
        self.isConst = False


class Function(Node):
    """
    children: (Scope)?
    """
    def __init__(self, counter, parent=None, contents="printf", returntype="void", isconstreturn=False):
        super().__init__(counter, parent, contents)
        self.type = returntype
        self.isConst = isconstreturn

class FunctionDeclaration(Node):
    """
    children: (Scope)?
    """
    def __init__(self, counter, parent=None, contents="functionDeclaration", returntype="void", isconstreturn=False):
        super().__init__(counter, parent, contents)
        self.type = returntype
        self.isConst = isconstreturn


class AndExpr(Node):
    """
    children: expression1 expression2

    where
    expression1 = one of the following: AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall,
                                        Identifier, UnaryOperator
    and
    expression2 = one of the following: OrExpr, CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall, Identifier,
                                        UnaryOperator

    both children have self.type
    """
    def __init__(self, counter, parent=None, contents="AND"):
        super().__init__(counter, parent, contents)
        self.type = ""


class OrExpr(Node):
    """
    children: expression1 expression2

    where
    expression1 = one of the following: OrExpr, CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall, Identifier,
                                        UnaryOperator
    and
    expression2 = one of the following: CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall, Identifier,
                                        UnaryOperator

    both children have self.type
    """
    def __init__(self, counter, parent=None, contents="OR"):
        super().__init__(counter, parent, contents)
        self.type = ""


class CompExpr(Node):
    """
    children: expression1 expression2

    where
    expression1 = one of the following: CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall, Identifier,
                                        UnaryOperator
    and
    expression2 = one of the following: AddExpr, MultExpr, Factor, Constant, FctCall, Identifier, UnaryOperator

    both children have self.type
    """
    def __init__(self, counter, parent=None, contents=""):
        super().__init__(counter, parent, contents)
        self.type = ""


class AddExpr(Node):
    """
    children: expression1 expression2

    where
    expression1 = one of the following: AddExpr, MultExpr, Factor, Constant, FctCall, Identifier, UnaryOperator
    and
    expression2 = one of the following: MultExpr, Factor, Constant, FctCall, Identifier, UnaryOperator

    both children have self.type
    """
    def __init__(self, counter, parent=None, contents="Arithmetic expression"):
        super().__init__(counter, parent, contents)
        self.type = ""


class MultExpr(Node):
    """
    children: expression1 expression2

    where
    expression1 = one of the following: MultExpr, Factor, Constant, FctCall, Identifier, UnaryOperator
    and
    expression2 = one of the following: Factor, Constant, FctCall, Identifier, UnaryOperator

    both children have self.type
    """
    def __init__(self, counter, parent=None, contents="Term"):
        super().__init__(counter, parent, contents)
        self.type = ""


class Factor(Node):
    """
    children: Constant
    """
    def __init__(self, counter, parent=None, contents="Factor"):
        super().__init__(counter, parent, contents)
        self.type = ""


class Constant(Node):
    """
    no children
    """
    def __init__(self, counter, parent=None, contents="constant"):
        super().__init__(counter, parent, contents)
        self.type = ""


class ParameterList(Node):
    """
    children: (Parameter)+
    """
    def __init__(self, counter, parent=None, contents="parameters"):
        super().__init__(counter, parent, contents)


class ArrayList(Node):
    """
    children: (factor)+

    with
    factor = one of the following: Constant, Identifier, UnaryOperator, Factor, FctCall

    all these children have self.type
    """
    def __init__(self, counter, parent=None, contents="array list"):
        super().__init__(counter, parent, contents)


class Parameter(Node):
    """
    no children
    """
    def __init__(self, counter, parent=None, contents="parameter"):
        super().__init__(counter, parent, contents)
        self.type = ""
        self.isConst = False


class Scope(Node):
    """
    children: (scopeitem)+

    (if this scope is child of a Function, the first child will be a Parameterlist

    where
    scopeitem = one of the following: IfStatement, ForLoop, WhileLoop, TerminateStatement, Declaration, Fct_Call, AssignmentStatement

    if isElse == True, this is the second Scope child of the IfStatement parent, the else scope
    """
    def __init__(self, counter, parent=None, contents="block"):
        super().__init__(counter, parent, contents)
        self.isElse = False


class IfStatement(Node):
    """
    children: Condition Scope
            | Condition Scope Scope(with isElse True)
    """
    def __init__(self, counter, parent=None, contents="if_statement"):
        super().__init__(counter, parent, contents)


class AssignmentStatement(Node):
    """
    children:   assignmentExpression
                | Identifier assigmentExpr
                | Identifier ArrayList
#todo here
    where assignmentexpr = one of the following: AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Factor, Constant, FctCall,
                                                Identifier, UnaryOperator
    """
    def __init__(self, counter, parent=None, contents="assignment statement"):
        super().__init__(counter, parent, contents)


class ForLoop(Node):
    """
    children: ForCondition Scope
    """
    def __init__(self, counter, parent=None, contents="for"):
        super().__init__(counter, parent, contents)


class WhileLoop(Node):
    """
    children: Condition Scope
    """
    def __init__(self, counter, parent=None, contents="while"):
        super().__init__(counter, parent, contents)


class ForCondition(Node):
    """
    children: Declaration comparison UnaryOperator
    """
    def __init__(self, counter, parent=None, contents="condition"):
        super().__init__(counter, parent, contents)


class Condition(Node):
    """
    children: assignment

    where
    assignment = one of the following:  AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Constant, FctCall, Identifier,
                                        UnaryOperator, Factor
    """
    def __init__(self, counter, parent=None, contents="condition"):
        super().__init__(counter, parent, contents)


class TerminateStatement(Node):
    """
    children: (assignment)?

    where
    assignment = one of the following:  AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Constant, FctCall, Identifier,
                                        UnaryOperator, Factor
    """
    def __init__(self, counter, parent=None, contents="terminate"):
        super().__init__(counter, parent, contents)


class FctCall(Node):
    """
    children: (argument)+

    argument = one of the following: AndExpr, OrExpr, CompExpr, AddExpr, MultExpr, Constant, FctCall, Identifier,
                                     UnaryOperator, Factor

    the contents of this node is the identifier with which the function is called
    """
    def __init__(self, counter, parent=None, contents="function call"):
        super().__init__(counter, parent, contents)
        self.type = ""


class UnaryOperator(Node):
    """
    children: (Identifier)?
    """
    def __init__(self, counter, parent=None, contents="unary operator"):
        super().__init__(counter, parent, contents)
        self.type = ""


class Type(Node):
    """
        Type node will not be found in the AST tree, it's used to make it though
    """
    def __init__(self, counter, parent=None, contents="Type", isconst = False):
        super().__init__(counter, parent, contents)
        self.isConst = isconst