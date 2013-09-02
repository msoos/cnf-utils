#!/usr/bin/env python

import unittest
from xor_to_cnf_class import *

class TestSequenceFunctions(unittest.TestCase):

    #def setUp(self):
        ##do_something_expensive_for_all_sets_of_tests()
        #print "hello"

    def test_max_var_cls(self):
        x = XorToCNF()
        self.assertEqual(x.get_max_var("1 2 3 0"), 3)
        self.assertEqual(x.get_max_var("1 0"), 1)
        self.assertEqual(x.get_max_var("-2 -3 -4 0"), 4)

    def test_to_xor_simple(self):
        x = XorToCNF()
        self.assertEqual(x.to_xor_simple("x1 0", True), ["1 0"])
        self.assertEqual(x.to_xor_simple("x-1 0", True), ["-1 0"])

        self.assertEqual(x.to_xor_simple("x1 0", False), ["-1 0"])
        self.assertEqual(x.to_xor_simple("x-1 0", False), ["1 0"])

        #1 = 2
        self.assertEqual(x.to_xor_simple("x1 2 0", False), ["-1 2 0", "1 -2 0"])
        self.assertEqual(x.to_xor_simple("x1 -2 0", True), ["1 -2 0", "-1 2 0"])

        #1 != 2
        self.assertEqual(x.to_xor_simple("x1 2 0", True), ["1 2 0", "-1 -2 0"])
        self.assertEqual(x.to_xor_simple("x1 -2 0", False), ["-1 -2 0", "1 2 0"])

        #1 + 2 + 3 = 0
        self.assertEqual(x.to_xor_simple("x1 2 3 0", False), ["-1 2 3 0", "1 -2 3 0", "1 2 -3 0", "-1 -2 -3 0"])

    def test_cut_xor(self):
        x = XorToCNF()
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 0", 5), [["x1 2 3 6 0", "x4 5 6 0"], 6])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 6 0", 6), [["x1 2 3 7 0", "x4 5 6 7 0"], 7])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 6 7 0", 7), [["x1 2 3 8 0", "x4 5 8 9 0", "x6 7 9 0"], 9])

        #simpler
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 0", 5, 2), [["x1 2 6 0", "x3 6 7 0", "x4 5 7 0"], 7])

if __name__ == '__main__':
    unittest.main()