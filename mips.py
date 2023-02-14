import sys

from ASTClasses import *
from AST import *
import struct

#todo: always keep $f31 set to 0

class Mips:
    def __init__(self, AST, scopes):
        self.AST = AST
        self.symbols = {("None", "None"): "None"}
        self.scopes = scopes
        self.branch_nr = 0
        self.comp = 0
        self.floatnr = 0
        self.printnr =0
        self.prestring = ""
        self.string = ""
        self.datastring=""
        self.poststring=""
        self.return_label = ""
        self.continue_label = []
        self.break_label = []
        self.sparestring =""
        self.is_Declared = dict()
        self.poststring = ""
        self.allvar = dict()
        self.registers_in_use = {"$s0": False, "$s1": False, "$s2": False, "$s3": False, "$s4": False, "$s5": False,
                                 "$s6": False, "$s7": False}
        self.float_reg_in_use = {"$f0": False, "$f1": False, "$f2": False, "$f3": False, "$f4": False, "$f5": False,
                                 "$f6": False, "$f7": False}

    def astToMips(self, filenaam):
        self.nodeToMips(self.AST)
        f = open(filenaam, "w")
        f.write(self.datastring)
        f.write(self.prestring)
        f.write("j main\n")
        f.write(self.string)
        f.write(self.poststring)
        f.close()

    def getFreeRegister(self, type = "int"):
        if type == "int":
            for register in self.registers_in_use:
                if not self.registers_in_use[register]:
                    self.registers_in_use[register] = True
                    return register
        if type == "float":
            for i in range(32):
                if i != 12 and not self.float_reg_in_use["$f"+str(i)]:
                    self.float_reg_in_use["$f"+str(i)] = True
                    return "$f"+str(i)

    def nodeToMips(self, node: Node):
        self.datastring += "     .data\n"
        for child in self.scopes:
            scopename = child.scopename
            for key in child.symbols:
                type = child.symbols[key][0]
                is_Parameter = child.symbols[key][2]
                is_array = child.symbols[key][0]
                if "array" in is_array:
                    assign = int(child.symbols[key][3])*4
                    self.datastring += key + scopename + ":  .space" + "  " + str(assign) + "\n"
                    self.allvar[(key,scopename)] = key+scopename
                    self.is_Declared[(key, scopename)] = False

                elif key != 'printf' and key!= 'scanf' and not isinstance(child.symbols[key][2],Function):
                    ret_val = self.type(type)
                    type = ret_val[0]
                    assign = ret_val[1]
                    self.datastring += key + scopename + ":  ."+type + "  " + assign + "\n"
                    self.allvar[(key,scopename)] = key+scopename
                    self.is_Declared[(key, scopename)] = False
                    if isinstance(is_Parameter, Parameter):
                        self.is_Declared[(key, scopename)] = True

        self.prestring += "     .text \n j Global \n j main \n"
        self.prestring += "Global: \n"
        self.poststring += "exit: \n       li $v0, 10  \n       syscall"

        for child in node.children:
            if isinstance(child,Declaration):
                self.prestring += self.declaration(child,"mainprogram0")
        for child in node.children:
            if isinstance(child, AssignmentStatement):
                self.string += self.assignmentStatement(child, "mainprogram0")
            if isinstance(child, Function):
                self.string += self.function(child)

    def function(self, node):
        if node.contents != "main":
            local_scope = node.contents + str(node.ID)
            self.return_label="end{}".format(node.contents)
            string = "{}:\n".format(node.contents)
            string += "sw $fp, 0($sp)\n"   # push old frame pointer (in 0($sp) of the old stack pointer (stack pointer will be changed))
            string += "move $fp, $sp\n"     # frame pointer now points to top of stack
            string += "subu $sp, $sp, {}\n".format(str(40+4*len(node.children[0].children[0].children))) # allocate 40 bytes on stack
            string += "sw $ra, -4($fp)\n"   # store value of ra in -4($fp)
            string += "sw $s0, -8($fp)\n"   # store s registers
            string += "sw $s1, -12($fp)\n"
            string += "sw $s2, -16($fp)\n"
            string += "sw $s3, -20($fp)\n"
            string += "sw $s4, -24($fp)\n"
            string += "sw $s5, -28($fp)\n"
            string += "sw $s6, -32($fp)\n"
            string += "sw $s7, -36($fp)\n"
            # for i in range
            string += self.scope(node.children[0])
            string += "end{}:\n".format(node.contents)
            string += "lw $s0, -8($fp)\n"  # restore s registers
            string += "lw $s1, -12($fp)\n"
            string += "lw $s2, -16($fp)\n"
            string += "lw $s3, -20($fp)\n"
            string += "lw $s4, -24($fp)\n"
            string += "lw $s5, -28($fp)\n"
            string += "lw $s6, -32($fp)\n"
            string += "lw $s7, -36($fp)\n"
            string += "lw $ra, -4($fp)\n"   # get return address from frame
            string += "move $sp, $fp\n"     # get old frame pointer from current frame
            string += "lw $fp, ($sp)\n"    # restore old frame pointer
            string += "jr $ra\n"  # return to previous function
        else:
            local_scope = node.contents + str(node.ID)
            self.return_label = "exit"
            string = "{}:\n".format(node.contents)
            string += self.scope(node.children[0])
        return string


    def type(self,type):
        if type == "float" or type == "float*":
            return "float", "0.0"
        elif type == "int" or type == "int*":
            return "word", "0"
        elif type == "char":
            return "word", "'a'"

    def scope(self, node):
        string = ""
        fctscope = node.parent.contents + str(node.parent.ID)
        for child in node.children:
            if isinstance(child, IfStatement):
                string += self.ifStatement(child)
            if isinstance(child, ForLoop):
                string += self.forLoop(child)
            if isinstance(child, WhileLoop):
                string += self.whileLoop(child)
            if isinstance(child, TerminateStatement):
                string += self.terminateStatement(child, fctscope)
                if child.contents == "break" or child.contents == "return" or child.contents == "continue":
                    break
            if isinstance(child, Declaration):
                string += self.declaration(child,fctscope)
            if isinstance(child, FctCall):
                string += self.fctCall(child, fctscope)
            if isinstance(child, AssignmentStatement):
                string += self.assignmentStatement(child, fctscope)
            if isinstance(child,ParameterList):
                string+= self.fctCallparameter(child, fctscope)
        return string

    def load_store(self,type):
        if type =="int" or type == "char" or type == "int*":
            return "li","lw","sw"
        elif type =="float" or type == "float*":
            return "l.s","l.d","s.s"

    def declaration(self,node,fctscope):
        mips = ""
        type = node.children[0].type
        load_store = self.load_store(type)
        self.is_Declared[(node.children[0].contents, fctscope)] = True
        self.name_of_var_in_mips(node.children[0].contents,fctscope)
        name_identifier =self.sparestring
        self.sparestring=""
        store = load_store[2]

        if len(node.children) > 1:
            value = node.children[1]
            type = node.children[1].type
            register = "$t0"
            if type == "float":
                register="$f0"
            if isinstance(value,Constant):
                if type != "float":
                    self.name_of_var_in_mips(node.children[0].contents,fctscope)
                    mips += "       {} {}, {} \n       {} {}, {} \n".format(load_store[0],register, node.children[1].contents,store, register,self.sparestring)
                    self.sparestring =""
                else:
                    self.name_of_var_in_mips(node.children[0].contents,fctscope)

                    self.datastring += "float{}: .float {}\n".format(self.floatnr, node.children[1].contents)
                    mips += "       l.s $f0, float{}\n       {} $f0, {} \n".format(self.floatnr,store,self.sparestring)
                    self.floatnr += 1
                    self.sparestring =""

            elif isinstance(value,Identifier):
                self.name_of_var_in_mips(node.children[0].contents,fctscope)
                identifier = self.sparestring
                self.sparestring =""
                self.name_of_var_in_mips(node.children[1].contents,fctscope)
                identifier2 = self.sparestring
                self.sparestring =""
                mips += "       {} {}, {} \n       sw {}, {} \n".format(load_store[1],register,identifier2,register,identifier)
            else:
                expr = self.assignmentExpression(node.children[1],fctscope)
                mips += expr[0]
                mips += "       {} {}, {} \n".format(store,expr[1], name_identifier)
                if expr[1][1] == "s":
                    self.registers_in_use[expr[1]] = False
                else:
                    self.float_reg_in_use[expr[1]] = False

        return mips

    def condition(self, node):
        return "condition \n"

    def ifStatement(self, node):
        currentscope = node.contents + str(node.ID)
        if_statement = "# if statement\n"
        condition = self.assignmentExpression(node.children[0].children[0], str(node.contents + str(node.ID)))
        if_statement += condition[0]
        branch_nr = self.branch_nr
        self.branch_nr += 1
        if_statement += "beqz {}, else{}\n".format(condition[1], branch_nr)
        if_statement += self.scope(node.children[1])
        if_statement += "j end{}\n".format(branch_nr)
        if_statement += "else{}:\n".format(branch_nr)
        if len(node.children) > 2:
            if_statement += self.scope(node.children[2])
        if_statement += "end{}:\n".format(branch_nr)
        return if_statement


    def forLoop(self, node):
        fct_scope = str(node.contents+str(node.ID))
        for_loop = self.declaration(node.children[0].children[0], fct_scope)
        # todo: add loopvariable to symbols
        for_nr = self.branch_nr
        self.branch_nr += 1
        self.break_label.append("endforloop{}".format(for_nr))
        self.continue_label.append("increase{}\n".format(for_nr))

        for_loop += "forloop{}:\n".format(for_nr)
        condition = self.assignmentExpression(node.children[0].children[1],str(node.contents+str(node.ID)))
        for_loop += condition[0]
        for_loop += "beqz {}, endforloop{}\n".format(condition[1], for_nr)
        for_loop += self.scope(node.children[1])
        for_loop += "increase{}:\n".format(for_nr)
        for_loop += self.assignmentExpression(node.children[0].children[2], str(node.contents+str(node.ID)))[0]  # increase/decrease
        for_loop += "j forloop{}\n".format(for_nr)
        for_loop += "endforloop{}:\n".format(for_nr)
        self.continue_label.pop()
        self.break_label.pop()
        return for_loop

    def whileLoop(self, node):
        while_loop = ""
        while_nr = self.branch_nr
        self.branch_nr += 1
        self.break_label.append("endwhile{}".format(while_nr))
        self.continue_label.append("whileloop{}\n".format(while_nr))
        while_loop += "whileloop{}:\n".format(while_nr)
        condition = self.assignmentExpression(node.children[0].children[0], str(node.contents + str(node.ID)))
        while_loop += condition[0]
        while_loop += "beqz {}, endwhile{}\n".format(condition[1], while_nr)
        while_loop += self.scope(node.children[1])
        while_loop += "j whileloop{}\n".format(while_nr)
        while_loop += "endwhile{}:\n".format(while_nr)
        self.break_label.pop()
        self.continue_label.pop()
        return while_loop

    def search_node(self, scopename):
        for node in self.scopes:
            if node.scopename == scopename:
                return node
        return False

    def name_of_var_in_mips(self,variable, scope, location=0):

        if location!= 0:
            self.allvar[(variable,scope)] = str(location) + "($fp)"
            self.sparestring = self.allvar[(variable,scope)]
        elif (variable, scope) in self.allvar and self.is_Declared[(variable,scope)]:
            self.sparestring = self.allvar[(variable,scope)]
            return self.allvar[(variable,scope)]
        else:
            father = self.search_node(scope).parent.scopename
            self.name_of_var_in_mips(variable,father)

    def terminateStatement(self, node, fct_scope):
        statement = ""
        if node.contents == "continue":
            breaklabel = self.continue_label.pop()
            self.continue_label.append(breaklabel)
            statement += "j {}\n".format(breaklabel)
        elif node.contents == "return" and len(node.children) != 0:
            if isinstance(node.children[0], Constant):
                type = node.children[0].type
                contents = node.children[0].contents
                if type == "bool":
                    if contents:
                        contents = "1"
                    else:
                        contents = "0"
                if type == "char":
                    statement += "li $v0, {}\n".format(contents)
                elif type == "float":
                    self.datastring += "float{}: .float {}\n".format(self.floatnr, contents)
                    statement += "l.s $f0, float{}\n".format(self.floatnr)
                    self.floatnr += 1
                else:
                    statement += "li $v0, {}\n".format(contents)
                statement+= "j {}\n".format(self.return_label)
            else:
                expression =self.assignmentExpression(node.children[0], fct_scope)
                statement += expression[0]
                statement += "move $v0, {}\n".format(expression[1])
                statement += "j {}\n".format(self.return_label)
        elif node.contents == "return":
            statement += "li $v0, 0\n"
            statement += "j {}\n".format(self.return_label)
        elif node.contents == "break":
            breaklabel = self.break_label.pop()
            self.break_label.append(breaklabel)
            statement += "j {}\n".format(breaklabel)
        return statement

    def fctCallparameter(self, node, fct_scope):
        param = ""
        location = -40

        for i in range(len(node.children)):
            self.name_of_var_in_mips(node.children[i].contents, fct_scope,location)
            label = self.sparestring
            self.sparestring = ""
            param += "sw $t{}, {}\n".format(i, label)
            location -= 4
        return param

    def fctCall(self, node, fct_scope):
        fct_call = ""

        if node.contents == "scanf":
            for child in node.children:
                if isinstance(child,UnaryOperator):
                    to_print = child.children[0]
                    type = to_print.type
                    move = "move"
                    if type == "int":
                        code = 5
                        register = "$t0"
                        load_type = self.load_store(type)
                    elif type == "float":
                        code = 6
                        register ="$f0"
                        load_type = self.load_store(type)
                    else:
                        code = 12
                        register = "$t0"
                        load_type = self.load_store(type)

                    fct_call += "li $v0, {} \nsyscall\n".format(code)
                    self.name_of_var_in_mips(to_print.contents, fct_scope)
                    var_in_mips = self.sparestring
                    self.sparestring=""

                    if not type == "float":
                        fct_call += "move {}, $v0\n".format(register)

                    fct_call += "{} {}, {} \n".format(load_type[2],register,var_in_mips)

        elif node.contents =="printf":
            # todo: add string to .data (and get label)
            string_contents = node.children[0].contents[1:-1]
            previousIt = 0
            count = 0
            print_string = dict()
            it= string_contents.find("%")
            if it == -1:
                self.datastring += "{}_{}: 	.asciiz \"{}\"\n".format("printf" + str(self.printnr),count, string_contents)
                print_string[0]=True
            else:
                while it != -1:
                    substring = string_contents[previousIt: it]
                    if len(substring) != 0:
                        self.datastring += "{}_{}: 	.asciiz \"{}\"\n".format("printf" + str(self.printnr), count,substring)
                        print_string[count] = True
                    else:
                        print_string[count] = False
                    count+=1
                    previousIt = it+2
                    it = string_contents.find("%", it+1)
                substring = string_contents[previousIt:]
                if len(substring) != 0:
                    self.datastring += "{}_{}: 	.asciiz \"{}\"\n".format("printf" + str(self.printnr), count,substring)
                    print_string[count] = True
                else:
                    print_string[count] = False
                count += 1

            if print_string[0]:
                fct_call += "la $a0, {}\n".format("printf"+ str(self.printnr)+"_0")
                fct_call += "li $v0, 4\n"
                fct_call += "syscall\n"

            for i in range(1, len(node.children)):
                child = node.children[i]

                if child.type == "int" or child.type == "bool" or child.type == "":
                    res = self.assignmentExpression(child, fct_scope)
                    fct_call += res[0]
                    fct_call += "move $a0, {}\n".format(res[1])
                    fct_call += "li $v0, 1\n"
                    fct_call += "syscall\n"
                    self.registers_in_use[res[1]] = False
                if child.type == "float":
                    res = self.assignmentExpression(child, fct_scope)
                    fct_call += res[0]
                    fct_call += "mov.s $f12, {}\n".format(res[1])
                    fct_call += "li $v0, 2\n"
                    fct_call += "syscall\n"
                    self.float_reg_in_use[res[1]] = False
                if child.type == "char":
                    res = self.assignmentExpression(child, fct_scope)
                    fct_call += res[0]
                    fct_call += "move $a0, {}\n".format(res[1])
                    fct_call += "li $v0, 11\n"
                    fct_call += "syscall\n"
                    self.registers_in_use[res[1]] = False
                if child.type == "string":
                    self.datastring += "{}_{}: 	.asciiz {}\n".format("printf" + str(self.printnr), count,
                                                                          child.contents)
                    fct_call += "la $a0, {}_{}\n".format("printf" + str(self.printnr), count)
                    fct_call += "li $v0, 4\n"
                    fct_call += "syscall\n"
                    count += 1
                if print_string[i]:
                    fct_call += "la $a0, {}_{}\n".format("printf" + str(self.printnr), i)
                    fct_call += "li $v0, 4\n"
                    fct_call += "syscall\n"
            self.printnr += 1
        else:
            for i in range(len(node.children)):
                result = self.assignmentExpression(node.children[0], fct_scope)
                fct_call += result[0]
                fct_call += "move $t{}, {}\n".format(i, result[1])
            fct_call += "jal {}\n".format(node.contents)
        return fct_call

    def assignmentExpression(self, node,fct_scope):
        expression = ""
        register = ""
        if len(node.children) == 0:
            if isinstance(node, Constant):
                contents = node.contents
                type = node.type
                if type == "bool":
                    if contents:
                        contents = "1"
                    else:
                        contents = "0"
                if not type == "float":
                    register = self.getFreeRegister()
                if type == "char":
                    expression += "li {}, {}\n".format(register, contents)
                elif type == "float":
                    self.datastring += "float{}: .float {}\n".format(self.floatnr, contents)
                    register = self.getFreeRegister("float")
                    expression += "l.s {}, float{}\n".format(register,self.floatnr)
                    self.floatnr += 1
                else:
                    expression += "li {}, {}\n".format(register, contents)
            else:
                if not node.type == "float":
                    register = self.getFreeRegister()
                self.name_of_var_in_mips(node.contents, fct_scope)
                label = self.sparestring
                self.sparestring = ""
                if node.hasarraybox:
                    label = "{}+{}".format(label, str(int(node.arraybox) * 4))
                if node.type == "float":
                    register = self.getFreeRegister("float")
                    expression += "l.s {},{}\n".format(register, label)
                else:
                    expression += "lw {},{}\n".format(register, label)

        elif len(node.children) == 2:
            reg = []
            for child in node.children:
                ret = self.assignmentExpression(child, fct_scope)
                reg.append(ret[1])
                expression += ret[0]
            # fic return register

            if node.type == "float":
                register = self.getFreeRegister("float")
            else:
                register = self.getFreeRegister()
            if isinstance(node, AddExpr):
                if node.contents == "+":
                    if node.type == "int":
                        expression += "add {}, {}, {}\n".format(register, reg[0], reg[1])
                    else:
                        expression += "add.s {}, {}, ,{}\n".format(register, reg[0], reg[1])
                if node.contents == "-":
                    if node.type == "int":
                        expression += "sub {}, {}, {}\n".format(register, reg[0], reg[1])
                    else:
                        expression += "sub.s {}, {}, {}\n".format(register, reg[0], reg[1])
            elif isinstance(node, MultExpr):
                if node.contents == "*":
                    if node.type == "int":
                        expression += "mul {}, {}, {}\n".format(register, reg[0], reg[1])
                    else:
                        expression += "mul.s {}, {}, {}\n".format(register, reg[0], reg[1])

                if node.contents == "/":
                    if node.type == "int":
                        expression += "div {}, {}, {}\n".format(register, reg[0], reg[1])
                    else:
                        expression += "div.s {}, {}, {}\n".format(register, reg[0], reg[1])

                if node.contents == "%":
                    if node.type == "int":
                        expression += "div {}, {}\n".format(reg[0], reg[1])
                        expression += "mfhi {}\n".format(register)

            elif isinstance(node, CompExpr):
                if node.children[0].type != "float":
                    if node.contents == "<":
                        expression += "slt {}, {}, {}\n".format(register, reg[0], reg[1])
                    if node.contents == ">":
                        expression += "sgt {}, {}, {}\n".format(register, reg[0], reg[1])
                    if node.contents == "<=":
                        expression += "sle {}, {}, {}\n".format(register, reg[0], reg[1])
                    if node.contents == ">=":
                        expression += "sge {}, {}, {}\n".format(register, reg[0], reg[1])
                    if node.contents == "==":
                        expression += "seq {}, {}, {}\n".format(register, reg[0], reg[1])
                    if node.contents == "!=":
                        expression += "sne {}, {}, {}\n".format(register, reg[0], reg[1])
                else:
                    newreg = self.getFreeRegister()
                    if node.contents == "!=":
                        expression += "c.eq.s {}, {}\n".format(register, reg[0], reg[1])
                        expression += "bc1t comp{}\n".format(self.comp)
                        expression += "li {}, 1\n".format(newreg)
                        expression += "j endcomp{}\n".format(self.comp)
                        expression += "comp{}:\n".format(self.comp)
                        expression += "li {}, 0\n".format(newreg)
                        expression += "endcomp{}:\n".format(self.comp)
                        register = newreg
                        self.comp += 1
                    else:
                        if node.contents == "<":
                            expression += "c.lt.s {}, {}\n".format(reg[0], reg[1])
                        if node.contents == ">":
                            expression += "c.lt.s {}, {}\n".format(reg[1], reg[0])
                        if node.contents == "<=":
                            expression += "c.le.s {}, {}\n".format(reg[0], reg[1])
                        if node.contents == ">=":
                            expression += "c.le.s {}, {}\n".format(reg[1], reg[0])
                        if node.contents == "==":
                            expression += "c.eq.s {}, {}\n".format(reg[0], reg[1])
                        expression += "bc1f comp{}\n".format(self.comp)
                        expression += "li {}, 1\n".format(newreg)
                        expression += "j endcomp{}\n".format(self.comp)
                        expression += "comp{}:\n".format(self.comp)
                        expression += "li {}, 0\n".format(newreg)
                        expression += "endcomp{}:\n".format(self.comp)
                        register = newreg
                        self.comp += 1
            else:
                for i in range(2):
                    if node.children[i].type == "float":
                        newreg = self.getFreeRegister()
                        expression += "c.eq.s {}, $f31\n".format(reg[i])
                        expression += "bc1t comp{}\n".format(self.comp)
                        expression += "li {}, 1\n".format(newreg)
                        expression += "j endcomp{}\n".format(self.comp)
                        expression += "comp{}:\n".format(self.comp)
                        expression += "li {}, 0\n".format(newreg)
                        expression += "endcomp{}:\n".format(self.comp)
                        self.float_reg_in_use[reg[i]] = False
                        reg[i] = newreg
                        self.comp += 1
                    elif node.children[i].type == "int":
                        expression += "sne {}, {}, 0\n ".format(reg[i], reg[i])
                if isinstance(node, AndExpr):
                    expression += "and {}, {}, {}\n".format(register, reg[0], reg[1])
                if isinstance(node, OrExpr):
                    expression += "or {}, {}, {}\n".format(register, reg[0], reg[1])

            for regist in reg:
                if regist[1] == "s":
                    self.registers_in_use[regist] = False
                else:
                    self.float_reg_in_use[regist] = False


        elif isinstance(node, FctCall):
            expression+= self.fctCall(node, fct_scope)
            if node.type == "float":
                newReg = self.getFreeRegister("float")
            else:
                newReg = self.getFreeRegister()
            register = "$v0"
            if node.type == "float":
                register = "$f0"
            expression += "move {},{}\n".format(newReg, register)
            register = newReg

        elif isinstance(node, UnaryOperator):
            if node.contents == "!":
                ret = self.assignmentExpression(node.children[0], fct_scope)
                register = ret[1]
                expression += ret[0]
                expression += "beqz {}, comp{}\n".format(register, self.comp)
                expression += "li {}, 0\n".format(register)
                expression += "j endcomp{}\n".format(self.comp)
                expression += "comp{}:\n".format(self.comp)
                expression += "li {}, 1\n".format(register)
                expression += "endcomp{}:\n".format(self.comp)
                self.comp += 1
            else:
                identifier = node.children[0]
                while not isinstance(identifier, Identifier):
                    identifier = identifier.children[0]
                self.name_of_var_in_mips(identifier.contents, fct_scope)
                label = self.sparestring
                self.sparestring = ""
                if node.contents == "&":
                    register= self.getFreeRegister()
                    expression += "la {}, {}\n".format(register, label)
                else:
                    ret = self.assignmentExpression(node.children[0], fct_scope)
                    type = self.type(node.type)
                    expression += ret[0]

                    if isinstance(node.children[0],Identifier) and node.children[0].hasarraybox:
                        label = "{}+{}".format(label, str(int(node.children[0].arraybox) * 4))
                    if node.contents == "++":
                        register = ret[1]
                        reg = self.getFreeRegister()
                        if isinstance(node.children[0],UnaryOperator) and node.children[0].contents == "*" :
                            expression += "lw {}, {}\n".format(reg, label)
                            label = "0({})".format(reg)

                        if type == "float":
                            # todo: fix
                            expression += "addi.s {}, {}, 1\n".format(ret[1], ret[1])
                            expression += "sw {},{}\n".format(register, label)
                        else:
                            expression += "addi {}, {}, 1\n".format(ret[1], ret[1])
                            expression += "sw {},{}\n".format(register, label)
                        self.registers_in_use[reg] = False
                    elif node.contents == "--":
                        register = ret[1]
                        reg = self.getFreeRegister()
                        if isinstance(node.children[0], UnaryOperator) and node.children[0].contents == "*":
                            expression += "lw {}, {}\n".format(reg, label)
                            label = "0({})".format(reg)

                        if type == "float":
                            # todo: fix
                            expression += "subi {}, {}, 1\n".format(register, register)
                            expression += "sw {},{}\n".format(register, label)
                        else:
                            expression += "subi {}, {}, 1\n".format(register, register)
                            expression += "sw {},{}\n".format(register, label)
                        self.registers_in_use[reg] = False
                    #     pointers should also go here
                    elif node.contents == "*":
                        register= self.getFreeRegister()
                        expression += "lw {}, 0({})\n".format(register, ret[1])
                        self.registers_in_use[ret[1]] = False

        return expression, register

    def assignmentStatement(self, node, fct_scope):
        assigment_statement = ""
        if len(node.children) == 1:
            assigment_statement += self.assignmentExpression(node.children[0], fct_scope)[0]
        elif not isinstance(node.children[1], ArrayList):
            self.name_of_var_in_mips(node.children[0].contents, fct_scope)
            label = self.sparestring
            self.sparestring = ""
            type = node.children[0].type
            register = self.getFreeRegister()
            if node.children[0].hasarraybox:
                label = "{}+{}".format(label, str(int(node.children[0].arraybox)*4))
            else:
                while type[-1:] == "*":
                    type = type[:-1]
                    assigment_statement += "lw {}, {}\n".format(register, label)
                    label = "0({})".format(register)

            assignment =self.assignmentExpression(node.children[1], fct_scope)
            assigment_statement += assignment[0]
            return_register = assignment[1]
            if return_register[1] == "s":
                self.registers_in_use[return_register] = False
                assigment_statement += "sw {},{}\n".format(return_register, label)
            else:
                self.float_reg_in_use[return_register] = False
                assigment_statement += "s.s {},{}\n".format(return_register, label)
            self.registers_in_use[register] = False

        return assigment_statement

