from copy import deepcopy
import numpy as N
import pymatgen
import sys, os

from extracting_oxidation.parse_html import extract_oxidation_dictionary

# Useful global objects from pyatgen
PT = pymatgen.periodic_table.ALL_ELEMENT_SYMBOLS

# Build the dictionary of all possible oxidation states for all the elements

"""
# ---> PYMATGEN GIVES MANY UNLIKELY OXIDATION STATES <----
# use the values provided by pymatgen
 oxidation_dictionary = {}
for symbol in PT:
    El = pymatgen.Element(symbol)
    oxidation_dictionary[symbol] =  El.oxidation_states
"""

oxidation_dictionary = extract_oxidation_dictionary()

class Compound(object):
    """
    Contains the formula for a compound, and computes the likely redox states for transition
    metals within this compound.
    """

    def __init__(self,compound_string):
        """
            input: 
                - compound_string: should be of the form 'Am Bn Cp ...', where A,B,C,... are element symbol, and
                                    m,n,p, ... are real numbers.  
        """

        self.string = compound_string



        self.composition_dict = {}

        self.extract_composition()
        self.find_oxidation_states()
        self.get_nice_formatted_formula()

    def extract_composition(self):
        """
        Take the input string and decompose it into elements/composition.
        Make sure the format of the string is correct. 
        """
        split_formula_string = self.string.split()

        # This could be implemented as a @property. 
        # I may do that later...

        tol = 1e-8
        self.is_disordered = False
        for ss in split_formula_string: 
            element, number = self.parse_element(ss)
            self.composition_dict[element] = number

            if abs(number - N.round(number)) > tol:
                self.is_disordered = True


    def parse_element(self,str):
        """
        Extract the element and number from a string.
        The expected format is either 'Ax', or 'ABx', where A (AB) represents
        an element, and x is a number. Any other format indicates an erroneous input.
        """

        # Extract what should be an element symbol
        if len(str) > 1:
            if str[1].isalpha():
                element_symbol = str[0:2]
            else:                
                element_symbol = str[0]
        else:                
            element_symbol = str[0]

        # Check that this is indeed an element
        if element_symbol not in PT:
            raise ValueError('Parsed symbol not recognized as an element')

        # process what is left of the string
        rest = str[len(element_symbol):]

        if len(rest) == 0:
            rest = '1'
        try:
            number = float(rest)
        except:
            raise ValueError('Parsed occupation not recognized as a number')

        return element_symbol, number


    def find_oxidation_states(self):
        """
        This routine will build all redox states for the compound, in order
        to identify possible redox states of elements in compound.

        The implementation below is surely not very efficient. However,
        this is not an exercise in computer science; I want to get to 
        useable results asap.
        """
        # initialize the data structure which will contain all the 
        # potential redox states
        oldTree = [ [] ]

        # let's keep track of the order in which the elements
        # appear in the loop below. The actual order is not important,
        # but we must consistently use the same order when treating the data.
        self.list_elements = []
        self.list_numbers  = []

        # iterate over all elements in the compound
        for element, number in self.composition_dict.iteritems():

            self.list_elements.append(element)
            self.list_numbers.append(number)

            # extract the possible oxidation states from global dictionary
            oxidations = N.array(oxidation_dictionary[element])

            # convert these elemental states to the actual charge of this element in the compound
            charges = number*oxidations 

            # keep track of what we had at the last iteration

            # build an updated tree for this iteration
            Tree    = []
            for list in oldTree:
                for charge in charges: 
                    new_list = N.append(list,charge)
                    Tree.append(new_list)

            oldTree = deepcopy(Tree)

        # The Tree structure now contains all possible combination of oxidation states
        # We must now find the physical ones, namely the charge zero combination
        self.oxidation_states_dict = {}

        tol = 1e-8

        number_of_solutions = 0

        for branch in Tree:
            if N.abs(N.sum(branch)) < tol:
                number_of_solutions +=1 

                oxidation_states = branch/self.list_numbers
                for el, ox in zip(self.list_elements,oxidation_states):
                    self.oxidation_states_dict[el] =  ox

        
        if number_of_solutions == 0:
            self.oxidation_states_dict =  None

        if number_of_solutions > 1:
            self.multiple_redox_solutions = True
        else:
            self.multiple_redox_solutions = False 

            #raise(ValueError,'More than one oxidation state found!')


    def get_nice_formatted_formula(self):
        """
        Return the name of the compound in a nice format
        """

        self.formula = ''

        tol = 1e-8

        for el, n in zip(self.list_elements, self.list_numbers):

            str = '%s'%el

            if N.abs(n - 1.) < tol:
                str += ' '
            elif N.abs(n - N.round(n)) < tol:
                str += '%i '%n
            else: 
                str += '%4.3f '%n

            self.formula += str


