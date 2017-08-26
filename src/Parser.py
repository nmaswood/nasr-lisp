from enum import Enum
import re
import pdb

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

def _is_bracketed(string):

    """
    Checks if a string is bracketed (foo)

    String -> Boolean

    """

    return string.startswith("(") and string.endswith(")")

def _split_into_units(string):

    """
    Splits a string into a function and its arguments

    (a (b c) (d)) ->  [a, (b c), (d)]

    String -> List<String>

    """

    big_buffer = []
    _buffer = []
    stack = []

    if is_bracketed(string):
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

        the_type  = Type.Expr if is_bracketed(string) else Type.Literal
        splat = split_into_units(string)
        func_name = splat[0]

        return Node(the_type, func_name, [_parse(x) for x in splat[1:]])


    if not _validate(string):
        raise ParserException("This string has mismatched parens!!!")

    trimmed = trim(string)

    return _parse(trimmed)
