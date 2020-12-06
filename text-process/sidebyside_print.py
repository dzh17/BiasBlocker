# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:11:38 2020

@author: tahir
"""

def print_sidebyside(s1,s2):
    
    maxChars = 75
    maxLength = max(len(s1),len(s2))

    s1 = s1.ljust(maxLength," ")
    s2 = s2.ljust(maxLength," ")

    s1 = [s1[i:i+maxChars] for i in range(0,len(s1),maxChars)]
    s2 = [s2[i:i+maxChars] for i in range(0,len(s2),maxChars)]

    for elem1, elem2 in zip(s1,s2):
        print(elem1.ljust(maxChars," "), end="    ")
        print(elem2)
        
    return
