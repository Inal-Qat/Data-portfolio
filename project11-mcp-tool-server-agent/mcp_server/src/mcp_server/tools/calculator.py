import ast
import operator as op

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def safe_eval(expression: str) -> float:
    """
    Safely evaluate arithmetic expressions.
    Allowed: + - * / ** % and parentheses.
    """
    node = ast.parse(expression, mode="eval").body
    return _eval(node)


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        return _ALLOWED_OPERATORS[type(node.op)](
            _eval(node.left), _eval(node.right)
        )

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))

    raise ValueError("Unsupported expression")