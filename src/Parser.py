from enum import Enum
import re
import pdb
from Functions import Functions

Type = Enum('Type', 'Literal Expr')
class ParserException(Exception):
    pass





class Node():

    """
    Unit representation of the AST

    type
        Type enum
    val
        String value of the node
    children
        arguments of node
    """

    def __init__(self, node_type, val, children = None):

        self.type = node_type
        self.value = val
        self.children = children or []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
    def __repr__(self):
        return (str(self))
    def eval(self):

        def _eval(node,defn = False):


            if node.type == Type.Literal and not defn:
                if _is_var and defn:
                   if node.value not in Functions.defined_vars:
                       return  str(node.value)
                if _is_quoted(node.value):
                    return str(node.value)
                elif '.' in node.value:
                    return float(node.value)
                elif node.value.isdigit():
                    return int(node.value)

                return Functions.defined_vars[node.value]

            expr_function = Functions.functions[node.value]

            args = [_eval(x, True) for x in node.children]

            if args[0] in {'defn'}:
                return expr_function(*args)

            return expr_function(*args)

        return _eval(self)

def _validate(string):

    """
    Ensures that parens are equally balanced

    String -> Bool
    """

    stack = []
    left_paren = False
    for letter in string:
        if letter == '"':
            left_paren = not left_paren

        if left_paren:
            continue

        if letter == '(':
            stack.insert(0,'(')
        elif letter == ')':

            if not stack:
                return False

            letter_prime = stack.pop()

            if letter_prime ==  ')':
                return False

    return not stack

def _trim(string):

    """

    Removes strings and excess newline characters
    String -> String

    """

    string = string.replace("\n", "")
    string = ' '.join(string.split())
    string = string.split()

    return ' '.join(string)


def _is_wrapped(string, char1, char2):

    """
    Checks if a string is wrapped by chars
    String -> String  -> String ->  Boolean
    """

    return string.startswith(char1) and string.endswith(char2)

def _is_quoted(string):

    """

    Checks if a string is bracketed (foo)

    String -> Boolean

    """
    return _is_wrapped(string, '"', '"')

def _is_bracketed(string):

    """
    Checks if a string is bracketed (foo)

    String -> Boolean

    """

    return _is_wrapped(string, '(', ')')

def _is_var(string):

    return not string.replace(".", '').isdigit() and not _is_quoted(string)

def _split_into_units(string):

    """
    Splits a string into a function and its arguments

    (a (b c) (d)) ->  [a, (b c), (d)]

    String -> List<String>

    """

    big_buffer = []
    _buffer = []
    stack = []

    if _is_bracketed(string):
        string = string[1:-1]

    saw_left_quote = False
    for idx, letter in enumerate(string):
        _buffer.append(letter)

        if letter == '"':
            saw_left_quote = not saw_left_quote

        if not saw_left_quote:

            if letter == " " and not stack:
                big_buffer.append(''.join(_buffer))
                _buffer = []

            if letter == "(":
                if not stack:
                    _buffer = _buffer[:-1]
                    big_buffer.append(''.join(_buffer))
                    _buffer = ['(']
                stack.append("(")
            elif letter == ")":
                stack.pop(0)

    if _buffer:
        big_buffer.append(''.join(_buffer))

    return [token.strip() for token in big_buffer if token]

def parse(string):

    """

    Parses a string, if possible into an AST
    String -> Node

    """

    def _parse(string):

        the_type  = Type.Expr if _is_bracketed(string) else Type.Literal
        splat = _split_into_units(string)
        func_name = splat[0]

        return Node(the_type, func_name, [_parse(x) for x in splat[1:]])


    if not _validate(string):
        raise ParserException("This string has mismatched parens!!!")

    trimmed = _trim(string)

    return _parse(trimmed)

s = '(def x 10)'
res = parse(s)
print (res.eval())

s = '(+ 1 (+ 2.7 3 x))'

res = parse(s)

print (res)
print (res.eval())


