import sys

from ASTClasses import *
from SymbolTableClasses import *


def assignTypeCheck(type1, type2):
    if (type1 == "float" and type2 == "int") or (type1 == "int" and type2 == "float"):
        return True
    if type1 == type2:
        return True
    if type1[-1] == "*":
        if type2[0] == "&":
            return assignTypeCheck(type1[0:-1],type2[1:])
        else:
            return False
    return False

def isNumberCharacter(c):
    if c == "0" or c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9":
        return True
    else:
        return False

def compareTypeCheck(type1, type2):
    if type1 == type2:
        return True
    return False


def typeIsNumber(type1, type2):
    if not (type1 == "int" or type1 == "float") or not (type2 == "int" or type2 == "float"):
        return None
    if type1 == "float" or type2 == "float":
        return "float"
    else:
        return "int"


class SymbolTable:
    def __init__(self, node: Node, parent=None):
        self.root = STNode(node.contents +str(node.ID), None)
        self.current_scope = self.root.scopename
        self.nodes = [self.root]

    def insert(self,parent, key, type, const, node):
        node_parent = self.search_node(parent)
        if self.check(node_parent,key) is None:
            node_parent.symbols[key] = [type, const, node]
            return True
        else:
            return False

    def insertForFunctions(self,parent, key, type, const, node, list):
        node_parent = self.search_node(parent)
        if self.check(node_parent,key) is None:
            node_parent.symbols[key] = [type, const, node, list, "function"]
            return True
        else:
            return False

    def insertArray(self,parent, key, type, const, node, arraylength):
        node_parent = self.search_node(parent)
        if self.check(node_parent,key) is None:
            node_parent.symbols[key] = [type, const, node, arraylength, "array"]
            return True
        else:
            return False

    def check(self,node, key):
        """
        if this key is already in use, returns [type, const, node]
        else returns None
        """
        return node.symbols.get(key)

    def check_in_scope(self, node, key):
        """
        checks if a given key already exists in a previous scope, return True, [type,const,node]
        else returns False
        """
        while node is not None:
            if self.check(node,key) is not None:
                return True, node.symbols[key]
            node = node.parent
        return False

    def search_or_add_Declaration(self,name,type, parameters,insert=False):
        if not self.root.fct_declarations.get(name):
            if insert:
                self.root.fct_declarations[name] = [type,parameters]
            return False
        else:
            return self.root.fct_declarations[name]

    def check_while_or_loop(self, node, content):
        while node.parent:
            if isinstance(node, STwhilestatement) or isinstance(node, STforloop):
                return True
            else:
                node = node.parent
        print("error: " + content+ " statement not within loop", file=sys.stderr)

    def search_node(self, scopename):
        for node in self.nodes:
            if node.scopename == scopename:
                return node

        return False

    def TraverseTree(self,node):
        for child in node.children:
            self.createSymbolTable(child)
            self.TraverseTree(child)

    def check_declaration_Mismatch(self,exists,node, types, string):

        if exists[0] != node.type:
            print("error: " + string + " of " + node.contents + " with wrong return type", file=sys.stderr)
        elif len(exists[1]) != len(types):
            print("error: " + string + " of " + node.contents + " with wrong amount of parameters", file=sys.stderr)
        else:
            for x, y in zip(types, exists[1]):
                if x != y:
                    print("error: " + string + " of " + node.contents + " with wrong parameter type", file=sys.stderr)
                    break

    def main_in_code(self):
        for x in self.root.symbols:
            if "main" in x:
                return True
        print("error: undefined reference to `main'", file=sys.stderr)

    def createSymbolTable(self, node):

        #what is the current_scope

        if isinstance(node.parent, Scope) or isinstance(node.parent, ForCondition):
            self.current_scope = node.parent.parent.contents + str(node.parent.parent.ID)
        else:
            self.current_scope = node.parent.contents + str(node.parent.ID)

        if isinstance(node,Declaration):
            if node.children[0].isConst and len(node.children) == 1:
                print("error: uninitialized const " + node.children[0].contents, file=sys.stderr)
            elif node.children[0].hasarraybox:  # for the declaration of an array
                if not self.insertArray(self.current_scope, node.children[0].contents, node.children[0].type+"array",
                                 node.children[0].isConst, node, node.children[0].arraybox):
                    print("error: redeclaration of " + node.children[0].contents, file=sys.stderr)

            elif not self.insert(self.current_scope, node.children[0].contents, node.children[0].type, node.children[0].isConst, node):
                print("error: redeclaration of " + node.children[0].contents, file=sys.stderr)

            if len(node.children) == 2:
                if isinstance(node.children[1], ArrayList):
                    for child in node.children[1].children:
                        if child.type == "":
                            self.findTypeOfRHS(child, self.current_scope)
                        if not assignTypeCheck(node.children[0].type, child.type):
                            print("types do not match in declaration of " + node.children[0].contents +": "+node.children[0].type+ " "+child.type, file=sys.stderr)

                else:
                    if node.children[1].type == "":
                        self.findTypeOfRHS(node.children[1],self.current_scope)
                    # check the types of both sides of the assignment
                    if not assignTypeCheck(node.children[0].type, node.children[1].type):
                        print("types do not match in declaration of " + node.children[0].contents+ ": "+node.children[0].type + " "+node.children[1].type, file=sys.stderr)

        if isinstance(node, Function):
            name = str(node.contents)
            types = []
            for x in node.children[0].children[0].children:
                types.append(str(x.type))
            if not self.insertForFunctions(self.root.scopename, name, node.type, node.isConst, node, types):
                print("error: redefinition of '" + node.contents + "' function", file=sys.stderr)
            else:
                fctnode = STFunction(node.contents+str(node.ID), self.root, node.type)
                fctnode.types = types
                self.nodes.append(fctnode)

            exists = self.search_or_add_Declaration(node.contents,node.type,types)
            if exists:
                self.check_declaration_Mismatch(exists, node, types, "definition")

            has_return = False
            for x in node.children[0].children:
                if x.contents == "return" and len(x.children) !=0:
                    has_return = True
            if not has_return and node.type != 'void' and node.contents != "main":
                print("error: '" + node.contents + "' function has no return value", file=sys.stderr)
            elif node.type == "void" and has_return:
                print("error: return-statement with a value, in function returning 'void'", file=sys.stderr)

        if isinstance(node,ParameterList) and isinstance(node.parent,Scope):
            for child in node.children:
                if not self.insert(self.current_scope, child.contents, child.type, child.contentsIsConst, child):
                    print("error: redefinition of parameter '" + child.contents + "' in function ", file=sys.stderr)

        if isinstance(node, UnaryOperator):
            self.findTypeOfRHS(node.children[0], self.current_scope)

        if isinstance(node, CompExpr):
            self.findTypeOfRHS(node.children[0], self.current_scope)
            self.findTypeOfRHS(node.children[1], self.current_scope)

        if isinstance(node,AssignmentStatement):
            self.findTypeOfRHS(node.children[0], self.current_scope)
            if not len(node.children) == 1:
                self.findTypeOfRHS(node.children[1], self.current_scope)
                if not assignTypeCheck(node.children[0].type, node.children[1].type):

                    print("types do not match in declaration of " + node.children[0].contents, file=sys.stderr)

                for child in node.children:
                    if isinstance(child, Identifier):
                        check = self.check_in_scope(self.search_node(self.current_scope), child.contents)
                        if not check:
                            print("error: '" + child.contents + "' was not declared in this scope", file=sys.stderr)
                        elif check[1][1]:
                            print("error: '" + child.contents + "' is a const variable", file=sys.stderr)

        if isinstance(node,TerminateStatement):
            if node.contents == "break" or node.contents == "continue":
                current_node = self.search_node(self.current_scope)
                self.check_while_or_loop(current_node,node.contents)

            if node.contents == "return" and len(node.children) != 0:
                ancestor = node.parent
                while not isinstance(ancestor, Function):
                    ancestor= ancestor.parent
                self.findTypeOfRHS(node.children[0],self.current_scope)
                if ancestor.type !="void" and not assignTypeCheck(ancestor.type, node.children[0].type):
                    print("error: type of return-statement(" + node.children[0].type + ") is incompatible with the type of the function(" + ancestor.type + ")", file=sys.stderr)

            length = len(node.parent.children)
            if node.parent.children[length-1] != node:
                print("error: unreachable code after " + node.contents, file=sys.stderr)

        if isinstance(node, IfStatement):
            ifnode = STifstatement(node.contents + str(node.ID), self.search_node(self.current_scope))
            self.nodes.append(ifnode)

        if isinstance(node, WhileLoop):
            whilenode = STwhilestatement(node.contents + str(node.ID), self.search_node(self.current_scope))
            self.nodes.append(whilenode)

        if isinstance(node, ForLoop):
            fornode = STforloop(node.contents + str(node.ID), self.search_node(self.current_scope))
            self.nodes.append(fornode)


        if isinstance(node,Condition):
            self.findTypeOfRHS(node.children[0], self.current_scope)
            if node.children[0].type != "bool":
                print("error: the condition of a " + node.parent.contents + " should evaluate to a boolean, not " + node.children[0].type, file=sys.stderr)
            for x in node.children[0].children:
                if isinstance(x,Identifier):
                    if not self.check_in_scope(self.search_node(self.current_scope), x.contents):
                        print("error: '" + x.contents + "' was never defined before", file=sys.stderr)


        if isinstance(node, FunctionDeclaration):
            types = []
            for x in node.children[0].children:
                types.append(x.type)
            exists = self.search_or_add_Declaration(node.contents, node.type,types,True)
            if exists:
                self.check_declaration_Mismatch(exists, node, types, "definition")
            else:
                checkinscope =[]
                for x in node.children[0].children:
                    if x.contents in checkinscope:
                        print("error: '" + x.contents + "' was already defined before", file=sys.stderr)
                        break
                    else:
                        checkinscope.append(x.contents)

        if isinstance(node, FctCall) and isinstance(node.parent, Scope):
            self.checkFctCall(node, self.current_scope)

    def checkPrintAndScan(self, node, scopename):
        node.type = "void"
        amp_if_scan = ""
        if node.contents == "scanf":
            amp_if_scan = "&"
        string = node.children[0].contents
        percent = string.find('%')
        i = 1
        while percent != -1:
            type_to_check = string[percent + 1:percent + 2]
            while isNumberCharacter(type_to_check[-1]):
                type_to_check = string[percent+1:percent + len(type_to_check)+2]
            if len(node.children) != i:
                self.findTypeOfRHS(node.children[i], scopename)
                type_of_factor = node.children[i].type
                correct = True
                if len(type_to_check) > 1:
                    if type_of_factor[-5:] == "array" and type_to_check[-1] == "s" and isinstance(node.children[i], UnaryOperator):
                        check = self.check_in_scope(self.search_node(scopename), node.children[i].children[0].contents)
                        if type_to_check[0:len(type_to_check)-1] == check[1][3]:
                            type_of_factor = type_of_factor[0:-5] + "*"
                            type_to_check = type_to_check [-1]
                        else:
                            correct = False
                    else:
                        correct = False
                elif type_of_factor[-5:] == "array":
                    type_of_factor = type_of_factor[0:-5] + "*"
                if (type_to_check == "d" or type_to_check == "i") and not (
                        type_of_factor == amp_if_scan + "int" or type_of_factor == amp_if_scan + "char"):
                    correct = False
                elif (type_to_check == "s") and not (
                        type_of_factor == amp_if_scan + "char*" or type_of_factor == amp_if_scan + "string"):
                    correct = False
                elif (type_to_check == "c") and not (
                        type_of_factor == amp_if_scan + "char" or type_of_factor == amp_if_scan + "int"):
                    correct = False
                elif (type_to_check == "f") and not (
                        type_of_factor == amp_if_scan + "int" or type_of_factor == amp_if_scan + "float"):
                    correct = False
                if not correct:
                    print("error: type '" + node.children[
                        i].type + "' is incompatible with '" + type_to_check + "' as flag in " + node.contents,
                          file=sys.stderr)
                if not (
                        type_to_check == "s" or type_to_check == "d" or type_to_check == "i" or type_to_check == "c" or type_to_check == "f"):
                    print("error: cannot use '" + type_to_check + "' as an flag in" + node.contents, file=sys.stderr)
                i += 1
                percent = string.find('%', percent + 1)
            else:
                print("error: too few arguments for format", file=sys.stderr)
                break
        if i < len(node.children):
            print("error: too many arguments for format", file=sys.stderr)

    def checkFctCall(self, node, scopename):
        check = self.check_in_scope(self.search_node(scopename), node.contents)
        if node.contents == "printf" or node.contents == "scanf":
            self.checkPrintAndScan(node,scopename)
        else:
            if not check:
                print("error: '" + node.contents + "' was not defined before it was used", file=sys.stderr)
                node.type = "?"
            else:
                node.type = check[1][0]
                argumentTypes = check[1][3]
                if len(node.children) == len(argumentTypes):
                    for i in range(len(node.children)):
                        self.findTypeOfRHS(node.children[i], scopename)
                        if not assignTypeCheck(argumentTypes[i],node.children[i].type):
                            print("error: type of arguments of function call '" + node.contents + "'does not match it's declaration", file=sys.stderr)
                else:
                    print("error: type of arguments of function call'" + node.contents + "' does not match it's declaration", file=sys.stderr)

    def findTypeOfRHS(self, node, scopename):
        if isinstance(node, FctCall):
            self.checkFctCall(node, scopename)

        if len(node.children) == 0 and (isinstance(node, Identifier)) :
            if node.type == "":
                check = self.check_in_scope(self.search_node(scopename), node.contents)
                if not check:
                    print("error: '" + node.contents + "' was not declared before it was used", file=sys.stderr)
                    node.type = "?"
                elif node.hasarraybox and len(check[1]) == 3: # and array identifier has an extra element in it's list in symbols
                    print("error: cannot access element [" + node.arraybox +"] of '"+ node.contents +"', '" + node.contents +"' is not an array", file=sys.stderr)
                elif node.hasarraybox:
                    if node.arraybox > check[1][3]:
                        print("error: cannot access element [" + node.arraybox + "] of '" + node.contents + "', out of bounds", file=sys.stderr)
                    node.type = check[1][0][:-5]
                else:
                    node.type = check[1][0]
        elif len(node.children) == 2:
            self.findTypeOfRHS(node.children[0],scopename)
            self.findTypeOfRHS(node.children[1],scopename)

            if isinstance(node, AndExpr) or isinstance(node, OrExpr):
                if not (node.children[0].type == "bool" and node.children[0].type == "bool"):
                    print("error: " + node.contents + " can only be used with booleans, not with " + node.children[0].type + " and " + node.children[1].type, file=sys.stderr)
                node.type = "bool"

            if isinstance(node, CompExpr):
                number = typeIsNumber(node.children[0].type,node.children[1].type)
                if number is None:
                    print("error: cannot compare " + node.children[0].type + " to " + node.children[1].type, file=sys.stderr)
                node.type = "bool"

            if isinstance(node, AddExpr):
                type = typeIsNumber(node.children[0].type, node.children[1].type)
                if type is None:
                    add = "add "
                    if node.contents == "-":
                        add = "subtract "
                    print("error: cannot " + add + node.children[0].type + " and " + node.children[1].type, file=sys.stderr)
                node.type = type

            if isinstance(node, MultExpr):
                type = typeIsNumber(node.children[0].type, node.children[1].type)
                if type is None:
                    mult = "multiply "
                    if node.contents == "/":
                        mult = "divide "
                    print("error: cannot " + mult + node.children[0].type + " and " + node.children[1].type, file=sys.stderr)
                node.type = type

        elif isinstance(node, UnaryOperator):
            self.findTypeOfRHS(node.children[0], scopename)
            if node.contents == "&":
                node.type = "&" + node.children[0].type
            if node.contents == "*":
                if node.children[0].type[-1] == "*":
                    node.type = node.children[0].type[0:-1]
                else:
                    print("error: cannot use unary operator * on identifier (" +node.children[0].contents +") of type " + node.children[0].type, file=sys.stderr)

        # else:
        #     print("ERROR: Lotte!!! check findTypeOfRHS")




