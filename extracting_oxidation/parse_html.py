from bs4 import BeautifulSoup
import yaml
import numpy as N
import os


def extract_oxidation_dictionary():


    #The file oxnotabl.html was obtained from http://www.thecatalyst.org/oxnotabl.html
    filename = os.path.dirname(os.path.abspath(__file__))+'/oxnotabl.html'

    html_doc = open(filename,'r')

    # load the soup!
    soup = BeautifulSoup(html_doc)

    # The data we seek to extract is stored in a table. Let's find all the rows of this table
    rows =soup.findAll('tr') # tr seems to label rows 

    # The first row is made up of headers, which we don't need
    oxidation_dictionary = {}

    for row in rows[1:]:

        # let's find all items within the row
        for item in row.find_all('td'):

            # Is this an element? the element names are in bold
            if item.find('b') == None:
                # Not an element! Skip the rest
                continue

            element = str(item.b.string)

            # The most likely oxidation states are in red, and thus 
            # have a "font" property
            list_oxidation = []
            for f in item.find_all('font'):
                text = f.get_text()
                for o in text.replace('+',' +').replace('-',' -').split():
                    list_oxidation.append(int(o))

            oxidation_dictionary[element] = list(N.sort(N.array(list_oxidation)))


    # Correct a few TM oxidation states
    oxidation_dictionary['Ti'] = [2,3,4]
    oxidation_dictionary['V']  = [2,3,4,5]
    oxidation_dictionary['Cr'] = [2,3,5,6]
    oxidation_dictionary['Mn'] = [2,3,4,5,6,7]
    oxidation_dictionary['Fe'] = [2,3,4,6]
    oxidation_dictionary['Co'] = [2,3,4]
    oxidation_dictionary['Ni'] = [2,3]
    oxidation_dictionary['Cu'] = [1,2,3]
    oxidation_dictionary['Zn'] = [2,3]

    return oxidation_dictionary
