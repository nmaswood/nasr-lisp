from sys import path as sys_path
from os import path as os_path
import unittest
import sys
from unittest import mock

sys.path.append('../src')
sys_path.append(os_path.abspath('../src'))

import parse

class ParserTest(unittest.TestCase):

    """
    Verifies the functionality of the JTR rule parser
    """

    def setUp(self):
        pass

    def test_util(self):
        self.assertTrue(parse.is_paren_balanced("(())"))
        self.assertTrue(parse.is_paren_balanced(""))
        self.assertTrue(parse.is_paren_balanced("()"))
        self.assertFalse(parse.is_paren_balanced("("))
        self.assertFalse(parse.is_paren_balanced("(("))
        self.assertFalse(parse.is_paren_balanced("))"))


if __name__ == "__main__":

    parser_suite = unittest.TestLoader().loadTestsFromTestCase(ParserTest)
    parser_runner = unittest.TextTestRunner()
    parser_runner.run(parser_suite)
