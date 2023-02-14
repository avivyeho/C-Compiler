import sys

from ASTClasses import *
from AST import *
import struct

class LLVM:
    def __init__(self, AST,scopes):
        self.current_loop = ""
        self.register_nr = 0
        self.nr_if = 0
        self.nr_for = 0
        self.nr_while = 0
        self.string_nr = 0
        self.prestring =""
        self.string = ""
        self.poststring = ""
        self.sparestring =""
        self.AST = AST
        self.symbols = {("None", "None"): "None"}
        self.scopes = scopes
        self.printf = False
        self.scanf = False

    def findRegisterFromSymbols(self, identifier):
        return self.symbols.get(identifier)

    def addRegisterToSymbols(self, identifier, scope, register):
        self.symbols[identifier, scope] = register

    def astToLLVM(self, filenaam):
        self.nodeToLLVM(self.AST)
        f = open(filenaam, "w")
        f.write(self.prestring)
        f.write(self.string)
        f.write(self.poststring)
        f.close()

    def TraverseTree(self, node):
        for child in node.children:
            self.nodeToLLVM(child)
            self.TraverseTree(child)

    def nodeToLLVM(self, node: Node):
        for child in node.children:
            if isinstance(child, Declaration):
                self.prestring += self.Global_declaration(child)
            if isinstance(child, AssignmentStatement):
                self.string += self.assignmentStatement(child)
            if isinstance(child, Function):
                self.string += self.function(child)
        if self.printf:
            self.poststring += "\n declare i32 @printf(i8*, ...)\n"
        if self.scanf:
            self.poststring += "declare i32 @__isoc99_scanf(i8*, ...) \n"

    def find_reg(self,node,parent):
        if (node, parent) in self.symbols:
            return self.symbols[node,parent]
        else:
            return False

    def search_node(self, scopename):
        for node in self.scopes:
            if node.scopename == scopename:
                return node
        return False

    def alloca_variables(self,current_scope):
        for key, value in current_scope.symbols.items():
            if key != 'printf' and key !='scanf':
                type = value[0]
                name = key
                self.sparestring += "%{} = alloca {}, align {} \n".format(self.register_nr, self.type(type)[0], self.type(type)[1])
                self.addRegisterToSymbols(name, current_scope.scopename, "%"+str(self.register_nr))
                self.register_nr +=1

        next_scope = self.search_node_child(current_scope)
        if next_scope is not False:
            self.alloca_variables(next_scope)

    def search_node_child(self,scope_father):
        for x in self.scopes:
            if x.parent == scope_father:
                return x
        return False



    def function(self, node):
        local_scope = node.contents + str(node.ID)
        length = len(node.children[0].children[0].children)
        self.register_nr = length+1
        string2=""
        if node.contents == "main":
            string2 += "%1 = alloca i32, align 4\n"
            string2 += "store i32 0, i32* %1, align 4\n"
            self.register_nr+=1

        string = "define {} @{}(".format(self.type(node.type)[0], node.contents)
        for child in node.children[0].children[0].children:
            string += self.type(child.type)[0]
            if child != node.children[0].children[0].children[length-1]:
                string += ','

        string += ") {\n"
        x = self.search_node(local_scope)
        self.alloca_variables(x)
        string+=string2
        string2=""
        string += self.sparestring
        self.sparestring = " "
        output_scope = self.scope(node.children[0])
        string += output_scope[0]
        if not output_scope[1]:
            if node.type == "void":
                string += "ret void\n"
            else:
                string += "\n ret i32 0\n"
        string += "}\n"
        self.register_nr = 0
        return string

    def float_to_hex(self, f):
        flt = struct.pack('>d',float(f))
        return "0x" + flt.hex()

    def Global_declaration(self, node):
        llvm_type = self.type(node.children[0].type)[0]
        llvm_align = self.type(node.children[0].type)[1]

        if len(node.children) == 1:
            glob = "common"
            assigned_value ='0'
        else:
            assigned_value = self.assigned_value(llvm_type, node.children[1])
            if not str(assigned_value).isdigit() and '*' not in llvm_type:
                assigned_value = "@"+assigned_value

            glob = "constant" if node.children[0].isConst and '*' not in llvm_type else "global"

        string = "@{} = {} {} {} , align {} \n ".format(node.children[0].contents, glob, llvm_type, assigned_value, llvm_align)

        self.symbols[node.children[0].contents, node.parent.contents+str(node.parent.ID)] = "@"+node.children[0].contents

        return string

    def scope(self, node):
        string = ""
        has_return = False
        fct_scope = node.parent.contents + str(node.parent.ID)
        for child in node.children:
            if isinstance(child, IfStatement):
                string += self.ifStatement(child)
            if isinstance(child, ForLoop):
                string += self.forLoop(child)
            if isinstance(child, WhileLoop):
                string += self.whileLoop(child)
            if isinstance(child, TerminateStatement):
                string += self.terminateStatement(child, fct_scope)
                if child.contents == "return":
                    has_return = True
                if child.contents == "break" or child.contents == "return":
                    break
            if isinstance(child, Declaration):
                string += self.declaration(child,fct_scope)
            if isinstance(child, FctCall):
                string += self.fctCall(child, fct_scope)
            if isinstance(child, AssignmentStatement):
                string += self.assignmentStatement(child, fct_scope)
        return string, has_return

    def find_var_in_scope(self,id,scope):
            x = self.find_reg(id,scope)
            if x:
                self.sparestring =x
                return x

            father = (self.search_node(scope)).parent
            if father:
                return self.find_var_in_scope(id,father.scopename)

    def declaration(self,node,parent):
        """
        parent = name of parent + id
        node = Declaration node
        """
        llvm = ""
        if len(node.children) > 1:
            value = node.children[1]
            llvm_type = self.type(node.children[0].type)[0]
            llvm_align = self.type(node.children[0].type)[1]
            curr_reg = self.find_reg(node.children[0].contents,parent)
            if isinstance(value,Constant):
                value = self.assigned_value(llvm_type,node.children[1])
                llvm += "store {} {}, {}* {}, align {} \n".format(llvm_type,value,llvm_type,curr_reg,llvm_align)
            elif isinstance(value,Identifier):
                self.find_var_in_scope(value.contents,parent)
                par_reg = self.sparestring
                llvm += "%{} = load {}, {}* {}, align {} \n".format(self.register_nr,llvm_type,llvm_type,par_reg,llvm_align)
                llvm += "store {} %{}, {}* {}, align {} \n".format(llvm_type,self.register_nr,llvm_type,curr_reg,llvm_align)
                self.sparestring =""
                self.register_nr += 1
            elif isinstance(value,UnaryOperator):
                self.find_var_in_scope(node.children[1].children[0].contents,parent)
                reg = self.sparestring
                llvm += "store {} {}, {}* {}, align {} \n".format(llvm_type,reg,llvm_type,curr_reg,llvm_align)
                self.sparestring =""
            else:
                result = self.assignmentExpression(node.children[1], parent)
                llvm += result[0]
                llvm += "store {} %{}, {}* {}, align {} \n".format(llvm_type, result[1], llvm_type, curr_reg, llvm_align)

        return llvm

    def get_comp_expr(self,x):
        if x == "==":
            return "eq"

    def condition(self, node):
        print(node)

        return "condition \n"

    def ifStatement(self, node):
        if_statement = ""
        if_statement += self.assignmentExpression(node.children[0].children[0],str(node.contents+str(node.ID)))[0]
        if_nr = self.nr_if
        self.nr_if += 1
        branch = "br i1 %{}, label %{}, label %".format(self.register_nr-1, self.register_nr, if_nr)
        statement = ";if label:\n".format(self.register_nr-1)
        self.register_nr += 1
        statement += self.scope(node.children[1])[0]
        branch_2 = "br label %".format(if_nr)
        statement_2 = ";else label {}:\n".format(self.register_nr)
        branch += "{}\n".format(self.register_nr)
        self.register_nr += 1
        if len(node.children) > 2:
            statement_2 += self.scope(node.children[2])[0]
        statement_2 += "br label %{}\n".format(self.register_nr)
        branch_2 += "{}\n".format(self.register_nr)
        statement_2 += ";if-end label {}:\n".format(self.register_nr)
        self.register_nr += 1
        if_statement += branch + statement + branch_2 + statement_2
        return if_statement

    def unaryOperator(self, node):
        return "unary operator\n"

    def forLoop(self, node):
        for_loop = ""
        for_loop += self.declaration(node.children[0].children[0], (node.contents+str(node.ID)))
        for_nr = self.nr_for
        self.nr_for += 1
        self.current_loop = "increase{}".format(for_nr)
        for_loop += "; start for loop:\n"
        startloop = self.register_nr
        for_loop += "br label %{}\n".format(self.register_nr)
        self.register_nr += 1
        for_loop += self.assignmentExpression(node.children[0].children[1],str(node.contents+str(node.ID)))[0]
        branchinstruction = "br i1 %{}, label %{}, label %".format(self.register_nr-1, self.register_nr)
        for_loop_2 = ";label {}:\n".format(self.register_nr)
        self.register_nr += 1
        for_loop_2 += self.scope(node.children[1])[0]
        for_loop_2 += "br label %{}\n".format(self.register_nr)
        for_loop_2 += ";label {}:\n".format(self.register_nr)
        self.register_nr += 1
        for_loop_2 += self.assignmentExpression(node.children[0].children[2],str(node.contents+str(node.ID)))[0]
        for_loop_2 += "br label %{}\n".format(startloop)
        for_loop_2 += "; label {}:\n".format(self.register_nr)
        branchinstruction += "{}\n".format(self.register_nr)
        self.register_nr += 1
        for_loop += branchinstruction
        for_loop += for_loop_2
        return for_loop

    def whileLoop(self, node):
        while_loop = ""
        while_loop += "br label %{}\n".format(self.register_nr)
        while_loop += "; while_start label {}:\n".format(self.register_nr)
        whilestart = self.register_nr
        self.current_loop = whilestart
        self.register_nr += 1
        while_loop += self.assignmentExpression(node.children[0].children[0],str(node.contents+str(node.ID)))[0]
        branch = "br i1 %{}, label %{}, label %".format(self.register_nr-1, self.register_nr)
        while_2 = "; while true label {}:\n".format(self.register_nr)

        self.register_nr += 1
        while_2 += self.scope(node.children[1])[0]
        while_2 += "br label %{}\n".format(whilestart)
        while_2 += "; label {}:\n".format(self.register_nr)
        branch += "{}\n".format(self.register_nr)
        self.register_nr += 1
        while_loop += branch + while_2
        return while_loop

    def terminateStatement(self, node, fct_scope):
        statement = ""
        if node.contents == "continue":
            statement += "br label %{}\n".format(self.current_loop)
            self.register_nr += 1
        elif node.contents == "return" and len(node.children) !=0:
            if isinstance(node.children[0], Constant):
                type = self.type(node.children[0].type)
                statement += "ret {} {}\n".format(type[0], node.children[0].contents)
            else:
                statement += self.assignmentExpression(node.children[0], fct_scope)[0]
                type = self.type(node.children[0].type)
                statement += "ret {} %{}\n".format(type[0], str(self.register_nr-1))
        elif node.contents == "return":
            statement += "ret void\n"
        return statement

    def fctCallparameter(self, node, fct_scope):
        param = ""
        fct_call_list = []
        if node.contents == "scanf":
            result = self.assignmentExpression(node.children[0], fct_scope)
            param += result[0]
            fct_call_list.append(result[1])
        else:
            for child in node.children:
                result = self.assignmentExpression(child,fct_scope)
                param += result[0]
                fct_call_list.append(result[1])

        return param, fct_call_list

    def fctCall(self, node, fct_scope):
        fct_call = ""
        result = self.fctCallparameter(node, fct_scope)
        fct_call += result[0]
        fct_call_registers = result[1]
        type = self.type(node.type)
        if node.contents =="printf":
            self.printf =True
            fct_call += "%{} = call i32 (i8*, ...) @printf(".format(self.register_nr)
        elif node.contents == "scanf":
            self.scanf =True
            fct_call += "%{} = call i32 (i8*, ...) @__isoc99_scanf(".format(self.register_nr)
        elif node.type == "void":
            fct_call += "call {} @{}(".format(type[0], node.contents)
            self.register_nr-=1
        else:
            fct_call += "%{} = call {} @{}(".format(self.register_nr, type[0], node.contents)
        self.register_nr += 1
        for i in range(0,len(node.children)):
            if (node.contents =="printf" or node.contents =="scanf") and i == 0:
                loc = self.find_var_in_scope(node.children[0].contents, self.AST.contents+str(self.AST.ID))
                fct_call+= "i8* getelementptr inbounds ([{} x i8], [{} x i8]* {}, i32 0, i32 0),".format(fct_call_registers[i], fct_call_registers[i], loc)
                self.sparestring = ""
            elif not node.contents == "scanf":
                childtype = self.type(node.children[i].type)[0]
                if node.contents == "printf" and childtype == "float":
                    childtype = "double"
                fct_call+= " {} %{},".format(childtype, fct_call_registers[i])
            else:
                childtype = self.type(node.children[i].type)[0]
                self.find_var_in_scope(node.children[i].children[0].contents, fct_scope)
                fct_call+= " {} {},".format(childtype, self.sparestring)
                self.sparestring = ""
        if (len(node.children)>0):
            fct_call = fct_call[0:-1]
        fct_call += ")\n"
        return fct_call

    def assignmentExpression(self, node, fct_scope):
        expression =""
        if len(node.children) == 0:
            if isinstance(node, Constant):
                type = self.type(node.type)
                if node.type == "string" and (node.parent.contents == "printf" or node.parent.contents == "scanf"):
                    length = len(node.contents)-1
                    contents = node.contents
                    found = contents.find("\\n")
                    while found !=-1:
                        contents = contents[0:found] + "\\0A" + contents[found+2:len(contents)]
                        found = contents.find("\n", found)
                        length -=1
                    contents = contents[1:-1]
                    contents += "\\00"
                    self.prestring += "@.str{} =  constant [{} x i8] c\"{}\", align 1\n".format(self.string_nr, length, contents)
                    self.addRegisterToSymbols(node.contents, self.AST.contents+str(self.AST.ID) , "@.str"+str(self.string_nr))
                    self.string_nr += 1
                    return "", length
                else:
                    contents = self.assigned_value(type[0],node)
                    expression += "%{} = alloca {}, align {}\n".format(self.register_nr, type[0], type[1])
                    expression += "store {} {}, {}* %{}, align {}\n".format(type[0], contents, type[0], self.register_nr,type[1])
                    self.register_nr += 1
                    expression += "%{} = load {}, {}* %{}, align {}\n".format(self.register_nr, type[0], type[0], self.register_nr-1,
                                                               type[1])
            else:
                self.find_var_in_scope(node.contents, fct_scope)
                type = self.type(node.type)
                expression += "%{} = load {}, {}* {}, align {}\n".format(self.register_nr, type[0], type[0], self.sparestring, type[1])
                self.sparestring =""


        elif len(node.children)==2:
            reg = []
            type = self.type(node.type)
            for child in node.children:
                ret = self.assignmentExpression(child, fct_scope)
                reg.append(ret[1])
                expression += ret[0]
            if isinstance(node, AddExpr):
                if node.contents == "+":
                    if (node.type == "int"):
                        expression += "%{} = add {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])
                    else:
                        expression += "%{} = fadd {} %{}, %{}\n".format(self.register_nr, type[0], reg[0], reg[1])
                if node.contents == "-":
                    if (node.type == "int"):
                        expression += "%{} = sub {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])
                    else:
                        expression += "%{} = fsub {} %{}, %{}\n".format(self.register_nr, type[0], reg[0], reg[1])
            if isinstance(node, MultExpr):
                if node.contents == "*":
                    if (node.type == "int"):
                        expression += "%{} = mul {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])
                    else:
                        expression += "%{} = fmul {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])

                if node.contents == "/":
                    if (node.type == "int"):
                        expression += "%{} = sdiv {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])
                    else:
                        expression += "%{} = fdiv {} %{}, %{}\n".format(self.register_nr,type[0], reg[0], reg[1])

                if node.contents == "%":
                    if (node.type == "int"):
                        expression += "%{} = srem {} %{}, %{}\n".format(self.register_nr, type[0], reg[0], reg[1])


            if isinstance(node,AndExpr):
                type_lhs = node.children[0].type
                type_rhs = node.children[1].type
                if type_rhs == "int":
                    expression += "%{} = icmp ne i32 %{}, {}\n".format(self.register_nr, reg[1], 0)
                    reg[1] = self.register_nr
                    self.register_nr +=1
                elif type_lhs =="int":
                    expression += "%{} = icmp ne i32 %{}, {}\n".format(self.register_nr, reg[0], 0)
                    reg[0] = self.register_nr
                    self.register_nr +=1
                expression += "%{} = and {} %{}, %{}\n".format(self.register_nr, "i1", reg[0], reg[1])
            if isinstance(node,OrExpr):
                expression += "%{} = or {} %{}, %{}\n".format(self.register_nr, "i1", reg[0], reg[1])
            if isinstance(node,CompExpr):
                if "float" in expression:
                    x = self.decide_compr_expr("float",node.contents)
                    type = "float"
                else:
                    x =self.decide_compr_expr("i32",node.contents)
                    type ="i32"
                cmprtype = x[0]
                cmprexpr = x[1]
                expression += "%{} = {} {} {} %{}, %{}\n".format(self.register_nr, cmprtype, cmprexpr,type, reg[0], reg[1])


        elif isinstance(node, FctCall):
            expression += self.fctCall(node,fct_scope)


        elif isinstance(node, UnaryOperator):
            type = self.type(node.type)
            reg = self.find_var_in_scope(node.children[0].contents, fct_scope)
            if node.contents == "++":
                ret = self.assignmentExpression(node.children[0], fct_scope)
                type = self.type(node.children[0].type)
                expression += ret[0]
                expression += "%{} = add {} %{}, 1\n".format(self.register_nr, type[0], ret[1])
                expression += "store {} %{}, {}* {}\n".format(type[0], self.register_nr, type[0], reg)
            elif node.contents == "--":
                type = self.type(node.children[0].type)
                ret = self.assignmentExpression(node.children[0], fct_scope)
                expression += ret[0]
                expression += "%{} = sub {} %{}, 1\n".format(self.register_nr, type[0], ret[1])
                expression += "store {} %{}, {}* {}\n".format(type[0], self.register_nr, type[0], reg)
        #     pointers should also go here
            elif node.contents == "*":
                ret = self.assignmentExpression(node.children[0], fct_scope)
                expression += ret[0]
                type = self.type(node.type)
                expression += "%{} = load {}, {}* %{}, align {}\n".format(self.register_nr, type[0], type[0],ret[1], type[1])


        self.register_nr+=1
        if node.parent.contents == "printf" and node.type == "float":
            expression+= "%{} = fpext float %{} to double\n".format(self.register_nr, self.register_nr-1)
            self.register_nr += 1
        return expression, self.register_nr-1

    def decide_compr_expr(self,type,expr):
        if type =="float":
            if expr =="<":
                return "fcmp","olt"
            elif expr == ">":
                return "fcmp" ,"ogt"
            elif expr == "<=":
                return "fcmp" ,"ole"
            elif expr == ">=":
                return "fcmp" ,"oge"
            elif expr == "==":
                return "fcmp" ,"oeq"
            elif expr == "!=":
                return "fcmp" ,"one"
        else:
            if expr =="<":
                return "icmp","slt"
            elif expr == ">":
                return "icmp" ,"sgt"
            elif expr == "<=":
                return "icmp","sle"
            elif expr == ">=":
                return "icmp" ,"sge"
            elif expr == "==":
                return "icmp" ,"eq"
            elif expr == "!=":
                return "icmp" ,"ne"


    def assignmentStatement(self, node, fct_scope):
        assigment_statement = ""
        if len(node.children) == 1:
            assigment_statement += self.assignmentExpression(node.children[0], fct_scope)[0]
        elif not isinstance(node.children[1], ArrayList):
            assigment_statement += self.assignmentExpression(node.children[1], fct_scope)[0]
            type = self.type(node.children[0].type)
            self.sparestring = self.find_var_in_scope(node.children[0].contents, fct_scope)
            assigment_statement += "store {} %{}, {}* {}, align {}\n".format(type[0], self.register_nr-1, type[0], self.sparestring, type[1])
            self.sparestring = ""
        return assigment_statement

    def type(self, type):
        if type == "int":
            return "i32", "4"
        elif type == "float":
            return "float", "4"
        elif type == "char":
            return "i8", "1"
        elif type == "void":
            return "void", "0"
        elif type == "int*":
            return "i32*", "8"
        elif type == "float*":
            return "float*", "8"
        elif type == "char*" or type=="string":
            return "i8*", "8"
        elif type == "&int":
            return "i32*", "8"

    def assigned_value(self, type, node):

        if type == "i32" or str(node.contents).isalpha():
            return node.contents
        elif type == "float":
            return self.float_to_hex(node.contents)
        elif type == "i8":
            return ord(node.contents[1])
