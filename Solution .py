# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:46:09 2022

@author: aryan
"""

import re
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""
    
    return re.findall('[A-Z][a-z]+', simple_string)

    # YOUR CODE HERE
    # raise NotImplementedError()
    
    
text=r'''Everyone has the following fundamental freedoms:
    (a) freedom of conscience and religion;
    (b) freedom of thought, belief, opinion and expression, including freedom of the press and other media of communication;
    (c) freedom of peaceful assembly; and
    (d) freedom of association.'''

import re
pattern = "\(.\)"
print(len(re.findall(pattern,text)))

x = re.search('A', s)