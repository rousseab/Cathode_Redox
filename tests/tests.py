import sys
sys.path.append('../')


import unittest

from compound import Compound
from capacity import CapacityCalculator

"""
Using Test Driven Development (TDD), tests will be implemented using unittest to 
create a development framework where failure is GOOD, since I can fix it before it
becomes an intractable bug! Thus, let's fail EARLY and let's fail OFTEN!
"""

class TestingCompound(unittest.TestCase):


    def setUp(self):
        self.test_string1 = 'This is random crap in the wrong format'

        self.test_string2 = 'FeAA Al1'

        self.test_string3 = 'Na Fe P O4'

        self.test_string4 = 'Na1.1 Fe2.2 P3.3 O4.4'
 

    # Implementing the same test on different input could be done
    # more elegantly using DDT, but this is just a bit too sophisticated for
    # me right now.
    def test_compound_format_1(self):

        # Construction to insure we catch the error
        with self.assertRaises(ValueError):
            cpd = Compound(self.test_string1)

    def test_compound_format_2(self):

        # Construction to insure we catch the error
        with self.assertRaises(ValueError):
            cpd = Compound(self.test_string2)

    def test_compound_composition1(self):
        result = { 'Na' : 1., 'Fe' : 1., 'P' : 1., 'O' : 4.}
        cpd    = Compound(self.test_string3)
        self.assertEqual(cpd.composition_dict, result)

    def test_compound_oxidation_states1(self):
        result = { 'Na' : 1., 'Fe' : 2., 'P' : 5., 'O' : -2.} 
        cpd    = Compound(self.test_string3)
        self.assertEqual(cpd.oxidation_states_dict, result)

    def test_compound_oxidation_states2(self):
        # Construction to insure we catch the error
        result = None
        cpd = Compound(self.test_string4)
        self.assertEqual(cpd.oxidation_states_dict, result)

    def test_compound_disorder1(self):
        result = False
        cpd    = Compound(self.test_string3)
        self.assertEqual(cpd.is_disordered, result)

    def test_compound_disorder2(self):
        result = True
        cpd    = Compound(self.test_string4)
        self.assertEqual(cpd.is_disordered, result)


class TestingCapacityCalculator(unittest.TestCase):


    def setUp(self):


        self.tol = 1e-12
        test_string1 = 'Na Fe P O4'

        test_string2 = 'Na2 Fe O2'

        active_ion = 'Na'

        self.CC = CapacityCalculator(active_ion)

        self.cpd1 = Compound(test_string1)
        self.cpd2 = Compound(test_string2)


    def test_capacity_calculator_1(self):
        tol = 1e-12
        result = 154.20331925588297
        test  = self.CC.get_capacity(self.cpd1)

        self.assertTrue(abs(test-result) < self.tol)

    def test_capacity_calculator_2(self):
        result = 200.27509878916402
        test  = self.CC.get_capacity(self.cpd2)

        self.assertTrue(abs(test-result) < self.tol)


if __name__ == '__main__':
    unittest.main()
