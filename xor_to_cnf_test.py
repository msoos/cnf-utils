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
        self.assertEqual(x.get_max_var("0"), 0)
        self.assertEqual(x.get_max_var(""), 0)
        self.assertEqual(x.get_max_var("x4 0"), 4)

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
        self.assertEqual(x.cut_up_xor_to_n("x0", 2), [["x0"], 2])
        self.assertEqual(x.cut_up_xor_to_n("x1 0", 2), [["x1 0"], 2])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 0", 2), [["x1 2 0"], 2])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 0", 5), [["x1 2 3 6 0", "x4 5 -6 0"], 6])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 6 0", 6), [["x1 2 3 7 0", "x4 5 6 -7 0"], 7])
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 6 7 0", 7), [["x1 2 3 8 0", "x4 5 -8 9 0", "x6 7 -9 0"], 9])

        #simpler
        x.cutsize = 3
        self.assertEqual(x.cut_up_xor_to_n("x1 2 3 4 5 0", 5), [["x1 2 6 0", "x3 -6 7 0", "x4 5 -7 0"], 7])

    def test_num_extra_var_needed(self):
        x = XorToCNF()
        self.assertEqual(x.num_extra_vars_cls_needed(2), [0, 2])
        self.assertEqual(x.num_extra_vars_cls_needed(3), [0, 4])
        self.assertEqual(x.num_extra_vars_cls_needed(4), [0, 8])
        self.assertEqual(x.num_extra_vars_cls_needed(5), [1, 8+4])
        self.assertEqual(x.num_extra_vars_cls_needed(6), [1, 8+8])
        self.assertEqual(x.num_extra_vars_cls_needed(7), [2, 8+8+4])

if __name__ == '__main__':
    unittest.main()