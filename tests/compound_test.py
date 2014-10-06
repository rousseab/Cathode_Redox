import sys
sys.path.append('../')

import unittest

from compound import Compound

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

    def test_compound_composition2(self):
        result = { 'Na' : 1.1, 'Fe' : 2.2, 'P' : 3.3, 'O' : 4.4}
        cpd    = Compound(self.test_string4)
        self.assertEqual(cpd.composition_dict, result)


    def test_compound_oxidation_states1(self):
        result = []
        cpd    = Compound(self.test_string4)
        self.assertEqual(cpd.list_oxidation_states, result)



if __name__ == '__main__':
    unittest.main()
