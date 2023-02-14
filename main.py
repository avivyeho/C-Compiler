import sys
from antlr4 import *
from ANTLRoutput import *
from AST import *
from LLVM import *
from mips import *


class KeyPrinter(MyGrammarListener):
    def exitR(self, ctx):
        for child in ctx.getChildren():
           print(child.getText()+'v')


def main(argv):

    input_stream = FileStream(argv[1])
    lexer = MyGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MyGrammarParser(stream)
    tree = parser.mainprogram()
    ast = AST(tree)
    filename = argv[1][0:-2]
    if len(argv) > 2 and argv[2] == "--with_ast_output":
        ast.toDot(filename+".dot")
    for i in range(2,len(argv)):
        if argv[i] == "--llvm":
            llvm_code = LLVM(ast.root, ast.symbolTableRoot.nodes)
            llvm_code.astToLLVM(filename + ".ll")
        if argv[i] == "--mips":
            mips_code = Mips(ast.root, ast.symbolTableRoot.nodes)
            mips_code.astToMips(filename + ".asm")




if __name__ == '__main__':
    main(sys.argv)
