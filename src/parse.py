class Node():

    def __init__(self, val, children = None):

        self.val = val
        self.children = [] or children

class AST():
    def __init__(self):
        pass

def is_paren_balanced(string):

    stack = []
    for letter in string:

        if letter == '(':
            stack.insert(0,'(')
        elif letter == ')':

            if not stack:
                return False

            letter_prime = stack.pop()

            if letter_prime ==  ')':
                return False

    return not stack

"""




def parse(string):


    _buffer = []
    just_saw_left_paren = False
    for letter in string:


        if just_saw_left_paren =
        if letter == "(":
            just_saw_left_paren = True
            pass
        elif letter == ")":











(defun triple (X)
  (* 3 X))
"""


