from copy import deepcopy
import numpy as N
import pymatgen

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

		self.string = string.strip()[7:]

		self.formula = self.string.replace('-','')

		self.file_number = string.strip()[:7]

		self.dict   = {}

		self.extract_composition()

		self.list_elements = self.dict.keys()
		self.list_numbers  = self.dict.values()

	def get_nice_formatted_formula(self,oxidation_state, alkaline):
		formula = ''

		found_alkali = False		
		for el, n in zip(self.list_elements, self.list_numbers):
			if el == alkaline:
				formula += ' %s%i : '%(alkaline,n)
				found_alkali  = True
				break

		if not found_alkali:
			formula += ' %s%i : '%(alkaline,0)


		for el, n in zip(self.list_elements, self.list_numbers):

			EL = pymatgen.Element(el)
			if EL.is_transition_metal:
				ox = oxidation_state[el]
				formula += ' %s%+i '%(el,ox)

		return formula

	def extract_composition(self):

		split_formula_string = self.string.replace('-','').split()

		for ss in split_formula_string: 
			element, number = self.parse_element(ss)
			self.dict[element] = number
		
	def parse_element(self,str):

		if len(str) == 1:
			element = str[0]
		elif str[1].isalpha():
			element = str[0:2]
		else:
			element = str[0]

		rest = str[len(element):]

		if len(rest) == 0:
			number = 1.0
		else:
			number = float(rest)

		return element, number

	def test_elements_in_dictionary(self,dic_elements):

		all_found = True
		for element in self.list_elements:
			if not dic_elements.has_key(element):

				all_found = False
				break

		return all_found 

	def build_redox_tree(self,dic_elements):

		Tree    = [[]]
		numbers = []

		for element, number in zip(self.list_elements, self.list_numbers):

			list_oxidations = dic_elements[element]

			list_charges = number*list_oxidations 

			oldTree = deepcopy(Tree)
			Tree    = []

			for list in oldTree:
				for charge in list_charges: 
					new_list = N.append(list,charge)
					Tree.append(new_list)

		self.Tree = deepcopy(Tree)
		del(Tree)
		del(oldTree)

	def find_oxidation_states(self):

		self.list_oxidation_states = []

		for branch in self.Tree:
			if N.sum(branch) == 0:
				list_oxidation_states = branch/self.list_numbers

				dic_oxidation_state = {}	

				for element, oxidation_state in zip(self.list_elements,list_oxidation_states):
					dic_oxidation_state[element] = oxidation_state 

		
				self.list_oxidation_states.append(dic_oxidation_state)




