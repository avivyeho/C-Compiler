# Generated from MyGrammar.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser

# This class defines a complete listener for a parse tree produced by MyGrammarParser.
class MyGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by MyGrammarParser#mainprogram.
    def enterMainprogram(self, ctx:MyGrammarParser.MainprogramContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#mainprogram.
    def exitMainprogram(self, ctx:MyGrammarParser.MainprogramContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#startrule.
    def enterStartrule(self, ctx:MyGrammarParser.StartruleContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#startrule.
    def exitStartrule(self, ctx:MyGrammarParser.StartruleContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#operations.
    def enterOperations(self, ctx:MyGrammarParser.OperationsContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#operations.
    def exitOperations(self, ctx:MyGrammarParser.OperationsContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#function.
    def enterFunction(self, ctx:MyGrammarParser.FunctionContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#function.
    def exitFunction(self, ctx:MyGrammarParser.FunctionContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#parameter_list.
    def enterParameter_list(self, ctx:MyGrammarParser.Parameter_listContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#parameter_list.
    def exitParameter_list(self, ctx:MyGrammarParser.Parameter_listContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#fct_scope.
    def enterFct_scope(self, ctx:MyGrammarParser.Fct_scopeContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#fct_scope.
    def exitFct_scope(self, ctx:MyGrammarParser.Fct_scopeContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#parameter.
    def enterParameter(self, ctx:MyGrammarParser.ParameterContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#parameter.
    def exitParameter(self, ctx:MyGrammarParser.ParameterContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#fct_call.
    def enterFct_call(self, ctx:MyGrammarParser.Fct_callContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#fct_call.
    def exitFct_call(self, ctx:MyGrammarParser.Fct_callContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#statement.
    def enterStatement(self, ctx:MyGrammarParser.StatementContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#statement.
    def exitStatement(self, ctx:MyGrammarParser.StatementContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#if_statement.
    def enterIf_statement(self, ctx:MyGrammarParser.If_statementContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#if_statement.
    def exitIf_statement(self, ctx:MyGrammarParser.If_statementContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#while_loop.
    def enterWhile_loop(self, ctx:MyGrammarParser.While_loopContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#while_loop.
    def exitWhile_loop(self, ctx:MyGrammarParser.While_loopContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#for_loop.
    def enterFor_loop(self, ctx:MyGrammarParser.For_loopContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#for_loop.
    def exitFor_loop(self, ctx:MyGrammarParser.For_loopContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#terminate_statement.
    def enterTerminate_statement(self, ctx:MyGrammarParser.Terminate_statementContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#terminate_statement.
    def exitTerminate_statement(self, ctx:MyGrammarParser.Terminate_statementContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#condition.
    def enterCondition(self, ctx:MyGrammarParser.ConditionContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#condition.
    def exitCondition(self, ctx:MyGrammarParser.ConditionContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#increment.
    def enterIncrement(self, ctx:MyGrammarParser.IncrementContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#increment.
    def exitIncrement(self, ctx:MyGrammarParser.IncrementContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#for_condition.
    def enterFor_condition(self, ctx:MyGrammarParser.For_conditionContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#for_condition.
    def exitFor_condition(self, ctx:MyGrammarParser.For_conditionContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#scope.
    def enterScope(self, ctx:MyGrammarParser.ScopeContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#scope.
    def exitScope(self, ctx:MyGrammarParser.ScopeContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#declaration.
    def enterDeclaration(self, ctx:MyGrammarParser.DeclarationContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#declaration.
    def exitDeclaration(self, ctx:MyGrammarParser.DeclarationContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#assignment_statement.
    def enterAssignment_statement(self, ctx:MyGrammarParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#assignment_statement.
    def exitAssignment_statement(self, ctx:MyGrammarParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#declaration_specifier.
    def enterDeclaration_specifier(self, ctx:MyGrammarParser.Declaration_specifierContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#declaration_specifier.
    def exitDeclaration_specifier(self, ctx:MyGrammarParser.Declaration_specifierContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#type_specifier.
    def enterType_specifier(self, ctx:MyGrammarParser.Type_specifierContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#type_specifier.
    def exitType_specifier(self, ctx:MyGrammarParser.Type_specifierContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#pointer_operator.
    def enterPointer_operator(self, ctx:MyGrammarParser.Pointer_operatorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#pointer_operator.
    def exitPointer_operator(self, ctx:MyGrammarParser.Pointer_operatorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#assignment_expr.
    def enterAssignment_expr(self, ctx:MyGrammarParser.Assignment_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#assignment_expr.
    def exitAssignment_expr(self, ctx:MyGrammarParser.Assignment_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#and_expr.
    def enterAnd_expr(self, ctx:MyGrammarParser.And_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#and_expr.
    def exitAnd_expr(self, ctx:MyGrammarParser.And_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#or_expr.
    def enterOr_expr(self, ctx:MyGrammarParser.Or_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#or_expr.
    def exitOr_expr(self, ctx:MyGrammarParser.Or_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#comp_expr.
    def enterComp_expr(self, ctx:MyGrammarParser.Comp_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#comp_expr.
    def exitComp_expr(self, ctx:MyGrammarParser.Comp_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#add_expr.
    def enterAdd_expr(self, ctx:MyGrammarParser.Add_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#add_expr.
    def exitAdd_expr(self, ctx:MyGrammarParser.Add_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#mult_expr.
    def enterMult_expr(self, ctx:MyGrammarParser.Mult_exprContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#mult_expr.
    def exitMult_expr(self, ctx:MyGrammarParser.Mult_exprContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#factor_fct_call.
    def enterFactor_fct_call(self, ctx:MyGrammarParser.Factor_fct_callContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#factor_fct_call.
    def exitFactor_fct_call(self, ctx:MyGrammarParser.Factor_fct_callContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#factor.
    def enterFactor(self, ctx:MyGrammarParser.FactorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#factor.
    def exitFactor(self, ctx:MyGrammarParser.FactorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#array_initialize.
    def enterArray_initialize(self, ctx:MyGrammarParser.Array_initializeContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#array_initialize.
    def exitArray_initialize(self, ctx:MyGrammarParser.Array_initializeContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#comp_operator.
    def enterComp_operator(self, ctx:MyGrammarParser.Comp_operatorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#comp_operator.
    def exitComp_operator(self, ctx:MyGrammarParser.Comp_operatorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#id_operators.
    def enterId_operators(self, ctx:MyGrammarParser.Id_operatorsContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#id_operators.
    def exitId_operators(self, ctx:MyGrammarParser.Id_operatorsContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#add_operator.
    def enterAdd_operator(self, ctx:MyGrammarParser.Add_operatorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#add_operator.
    def exitAdd_operator(self, ctx:MyGrammarParser.Add_operatorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#mult_operator.
    def enterMult_operator(self, ctx:MyGrammarParser.Mult_operatorContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#mult_operator.
    def exitMult_operator(self, ctx:MyGrammarParser.Mult_operatorContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#constant.
    def enterConstant(self, ctx:MyGrammarParser.ConstantContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#constant.
    def exitConstant(self, ctx:MyGrammarParser.ConstantContext):
        pass


    # Enter a parse tree produced by MyGrammarParser#identifier.
    def enterIdentifier(self, ctx:MyGrammarParser.IdentifierContext):
        pass

    # Exit a parse tree produced by MyGrammarParser#identifier.
    def exitIdentifier(self, ctx:MyGrammarParser.IdentifierContext):
        pass



del MyGrammarParser