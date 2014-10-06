#================================================================================
#
# A simple example to see how things run
#
#================================================================================
import sys
sys.path.append('../')


from compound import Compound
from capacity import CapacityCalculator


compound_string = 'Na Fe P O4'
compound_string = 'Fe Na O4 Ti'
#compound_string = 'Na Fe'
#compound_string = 'Na2 Fe O2'

cpd = Compound(compound_string)

CC = CapacityCalculator('Na')

capacity = CC.get_capacity(cpd)

print capacity
