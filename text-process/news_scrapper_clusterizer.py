# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:16:49 2020

@author: tahir
"""

from nltk.stem import WordNetLemmatizer
import newspaper
from datetime import date
from clean_enhance import *

def scrapper(URL):
    
    content = newspaper.Article(URL)
    content.download()
    content.parse()
    content.nlp()
    #print(content.text)
    current_content = content.text
    pd = content.publish_date
    
    return [current_content,pd.year,pd.month,pd.day]

def clusterizer(current_content,cluster_descript,true_k):
    

    norm_current_content = clean(current_content)

    num_common = 0  
    total_scores = []

 
    for k in range(true_k):
        for word in norm_current_content:
            if word in cluster_descript[f"{k}"]:
                num_common += 1 
        total_scores.append(num_common)

    max_score = max(total_scores)
    cluster_num = total_scores.index(max_score)
    
    return [norm_current_content,cluster_num]

