from sys import path as sys_path
from os import path as os_path
import unittest
import sys
from unittest import mock

sys.path.append('../src')
sys_path.append(os_path.abspath('../src'))

import Parser
class ParserTest(unittest.TestCase):

    """
    Verifies the functionality of the JTR rule parser
    """

    def setUp(self):
        pass

    def test_validate(self):

        self.assertTrue(Parser._validate("(())"))
        self.assertTrue(Parser._validate(""))
        self.assertTrue(Parser._validate("()"))
        self.assertTrue(Parser._validate('")()()()()"()'))
        self.assertFalse(Parser._validate("("))
        self.assertFalse(Parser._validate("(("))
        self.assertFalse(Parser._validate("))"))

    def test_validate(self):

        res = Parser._trim("young and       rich    ")
        self.assertEqual(res, "young and rich")


    def test_split_into_units(self):
        pass

if __name__ == "__main__":

    parser_suite = unittest.TestLoader().loadTestsFromTestCase(ParserTest)
    parser_runner = unittest.TextTestRunner()
    parser_runner.run(parser_suite)
