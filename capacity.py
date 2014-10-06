import numpy as N
import pymatgen


class CapacityCalculator(object):
    """
    This object will compute the maximum capacity of a given compound.
    """
    def __init__(self,active_ion):
        # what is the ion which enters and leaves the cathode?
        self.active_ion = active_ion

        # get unit conversion factor
        self.compute_unit_conversion()

        # build a dictionary with all atomic masses
        # and a list of transition metals
        self.build_data()


    def get_capacity(self,compound):

        atomic_mass = 0.

        transition_metal = 0.

        # get mass and quantity of transition metals
        for symbol, number in zip(compound.list_elements, compound.list_numbers):

            atomic_mass += number*self.dict_atomic_mass[symbol]
            if symbol in self.list_transition_metal:
                transition_metal += number


        ionic_charge = cpd.composition_dict[self.active_ion]*cpd.oxidation_states_dict[self.active_ion]

        effective_atomic_charge = N.min([ ionic_charge, transition_metal ])

        capacity = effective_atomic_charge/atomic_mass*self.conversion_to_mAh_per_g

        return capacity 


    def build_data(self):

        # Build mass dictionary
        PT = pymatgen.periodic_table.PeriodicTable()

        self.list_transition_metal = []
        self.dict_atomic_mass      = {}

        for E in PT.all_elements:
            self.dict_atomic_mass[E.symbol] = E.atomic_mass

            if E.is_transition_metal:
                self.list_transition_metal.append(E.symbol)


    def compute_unit_conversion(self):
        """
        Compute, once and for all, the conversion between atomic units and 
        mAh/g.
        """
        kilo= 1e3
        hr  = 3600. # seconds

        amu_to_g   = kilo*pymatgen.amu_to_kg

        mAh        = hr/kilo # Coulomb

        e_in_mAh   = pymatgen.e/mAh

        self.conversion_to_mAh_per_g = e_in_mAh/amu_to_g

