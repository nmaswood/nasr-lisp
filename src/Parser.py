from enum import Enum
import re
import pdb

__all__ = ['Type', "Node", "parse"]

Type = Enum('Type', 'Literal Expr')

class Node():

    def __init__(self, _type, val, children = None):

        self.type = _type
        self.value = val
        self.children = children or []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

def validate(string):

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

def trim(string):

    string = string.replace("\n", "")
    string = ' '.join(string.split())
    string = string.split()

    return ' '.join(string)

def is_bracketed(string):

    return string.startswith("(") and string.endswith(")")

def split_into_units(string):

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

    def _parse(string):

        the_type  = Type.Expr if is_bracketed(string) else Type.Literal
        splat = split_into_units(string)
        func_name = splat[0]

        return Node(the_type, func_name, [_parse(x) for x in splat[1:]])

    trimmed = trim(string)

    return _parse(trimmed)
