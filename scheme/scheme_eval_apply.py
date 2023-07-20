import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # 在每个Pair中
        operator = scheme_eval(first, env)  # 首先得到操作函数,这是一个procedure
        # 然后对于每个操作数，他们都要先要找到自己的作用函数，再作用自己才是对当前操作函数有效的操作数值
        operands = rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(operator, operands, env)  # 最终返回结果
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
        assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        schemelist_to_pylist = []
        ptr = args
        while ptr is not nil:
            schemelist_to_pylist.append(ptr.first)
            ptr = ptr.rest
        # print(schemelist_to_pylist)
        if procedure.need_env == True:
            schemelist_to_pylist.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            # 这个用法我不是很明白，是看说明是这么个意思，感觉就是传入变参
            return procedure.py_func(*schemelist_to_pylist)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError(
                'incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # 现在此处的procedure就是lambda整体
        # 首先是在lambda所在帧创建用户define的表达式，注意看args就是一系列的参数值，因此创建子帧绑定
        child_fram = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, child_fram)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        fram = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, fram)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # replace this with lines of your own code
    ptr = expressions
    if ptr == nil:  # 这是个特殊情况，直接nil，需要单独处理
        return None
    while ptr.rest != nil:
        tmp = scheme_eval(ptr.first, env)
        ptr = ptr.rest
    return scheme_eval(ptr.first, env)  # 返回最后一个式子的返回值即可
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        # 这个尾递归我直接抄了，EC确实不想再想了。hh
        # 大致意思就是在常量空间下实现eval操作
        # 尾递归是指递归语句是最后一个操作
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env)
        return result
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
