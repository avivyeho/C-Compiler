# Generated from MyGrammar.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser

# This class defines a complete generic visitor for a parse tree produced by MyGrammarParser.

class MyGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyGrammarParser#mainprogram.
    def visitMainprogram(self, ctx:MyGrammarParser.MainprogramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#startrule.
    def visitStartrule(self, ctx:MyGrammarParser.StartruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#operations.
    def visitOperations(self, ctx:MyGrammarParser.OperationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#function.
    def visitFunction(self, ctx:MyGrammarParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#parameter_list.
    def visitParameter_list(self, ctx:MyGrammarParser.Parameter_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#fct_scope.
    def visitFct_scope(self, ctx:MyGrammarParser.Fct_scopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#parameter.
    def visitParameter(self, ctx:MyGrammarParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#fct_call.
    def visitFct_call(self, ctx:MyGrammarParser.Fct_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#statement.
    def visitStatement(self, ctx:MyGrammarParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#if_statement.
    def visitIf_statement(self, ctx:MyGrammarParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#while_loop.
    def visitWhile_loop(self, ctx:MyGrammarParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#for_loop.
    def visitFor_loop(self, ctx:MyGrammarParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#terminate_statement.
    def visitTerminate_statement(self, ctx:MyGrammarParser.Terminate_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#condition.
    def visitCondition(self, ctx:MyGrammarParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#increment.
    def visitIncrement(self, ctx:MyGrammarParser.IncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#for_condition.
    def visitFor_condition(self, ctx:MyGrammarParser.For_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#scope.
    def visitScope(self, ctx:MyGrammarParser.ScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#declaration.
    def visitDeclaration(self, ctx:MyGrammarParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#assignment_statement.
    def visitAssignment_statement(self, ctx:MyGrammarParser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#declaration_specifier.
    def visitDeclaration_specifier(self, ctx:MyGrammarParser.Declaration_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#type_specifier.
    def visitType_specifier(self, ctx:MyGrammarParser.Type_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#pointer_operator.
    def visitPointer_operator(self, ctx:MyGrammarParser.Pointer_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#assignment_expr.
    def visitAssignment_expr(self, ctx:MyGrammarParser.Assignment_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#and_expr.
    def visitAnd_expr(self, ctx:MyGrammarParser.And_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#or_expr.
    def visitOr_expr(self, ctx:MyGrammarParser.Or_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#comp_expr.
    def visitComp_expr(self, ctx:MyGrammarParser.Comp_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#add_expr.
    def visitAdd_expr(self, ctx:MyGrammarParser.Add_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#mult_expr.
    def visitMult_expr(self, ctx:MyGrammarParser.Mult_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#factor_fct_call.
    def visitFactor_fct_call(self, ctx:MyGrammarParser.Factor_fct_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#factor.
    def visitFactor(self, ctx:MyGrammarParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#array_initialize.
    def visitArray_initialize(self, ctx:MyGrammarParser.Array_initializeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#comp_operator.
    def visitComp_operator(self, ctx:MyGrammarParser.Comp_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#id_operators.
    def visitId_operators(self, ctx:MyGrammarParser.Id_operatorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#add_operator.
    def visitAdd_operator(self, ctx:MyGrammarParser.Add_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#mult_operator.
    def visitMult_operator(self, ctx:MyGrammarParser.Mult_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#constant.
    def visitConstant(self, ctx:MyGrammarParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#identifier.
    def visitIdentifier(self, ctx:MyGrammarParser.IdentifierContext):
        return self.visitChildren(ctx)



del MyGrammarParser