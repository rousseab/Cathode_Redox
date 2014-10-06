import unittest

from Cathode_Redox.compound import Compound

"""
Using Test Driven Development (TDD), tests will be implemented using unittest to 
create a development framework where failure is GOOD, since I can fix it before it
becomes an intractable bug! Thus, let's fail EARLY and let's fail OFTEN!
"""

class TestingCompound(unittest.TestCase):

    test_string1 = 'This is random crap in the wrong format'

    test_string2 = 'Fe1 Na2 Al3'

    test_string3 = 'Fe1.1 P2.1 O14'

    test_string4 = 'Mn1.1 Na2.1 O12 Co'
 
    def test_compound_format(self):
        cpd    = Compound(test_string1)
        self.assertRaises(ValueError)

if __name__ == '__main__':
    unittest.main()
