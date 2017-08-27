from functools import reduce
import operator

def _add(*args):
    return sum (args)

def _mult(*args):

    return reduce(operator.mul, args, 1)

def _def_bang(*args):

    Functions.defined_vars[args[0]] = int(args[1])
    print ("BANG")

class Functions():

    functions = {
            '+': _add,
            '*': _mult,
            'def': _def_bang
    }

    defined_vars = {

    }

    custom_functions = {

    }
