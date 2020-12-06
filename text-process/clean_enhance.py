import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize          
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
import spacy
sp = spacy.load('en_core_web_lg')


stop_words = stopwords.words('english')
stop_words.extend(['The','A','An'])
stop_words = set(stop_words)


def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def lemmatizing(data):
    
    lem = nltk.WordNetLemmatizer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + lem.lemmatize(w)
    return new_text

def stemmatizer(data):
    
    stemmer = PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text


def POS_NER_cleaner(txt,sp):
        
    sp_txt = sp(txt)
    new_txt = sp_txt.text
    clean_txt = ""  
    necc_ents = ['PERSON','NORP','FAC','ORG','GPE','EVENT']
  
    for ent in sp_txt.ents: 
        if ent.label_ in necc_ents:
            clean_txt = clean_txt + ' ' + ent.text
            new_txt = new_txt.replace(ent.text,'')
            #print(ent.text, ent.start_char, ent.end_char, ent.label_) 
        
    new_txt = sp(new_txt)   
    for word in new_txt:
        if word.pos_ == 'NOUN' or word.pos_ == 'VERB' :
            clean_txt = clean_txt + " " + word.text
            # print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')

    return clean_txt

def correct_aze_cities(txt):
    
    cities = {"Stepanakert":"Khankendi","Martuni":"Khojavend","Martakert":"Aghdara","Shushi":"Shusha","Berdzor":"Lachin","Karvachar":"Kalbajar","Artsakh":"Nagorno-Karabakh"}

    txt_tok = word_tokenize(txt)
    for word in txt_tok:
        if word in list(cities.values()): continue
        elif word in list(cities.keys()):
            txt = txt.replace(word,cities[word])
                
    return txt


def clean(data):
    #data = convert_lower_case(data)
    data = remove_punctuation(data) 
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = correct_aze_cities(data)
    data = POS_NER_cleaner(data,sp)
    data = stemmatizer(data)

    temp_lst = word_tokenize(data)
    temp_lst = list(set(temp_lst))
    data = ""
    for word in temp_lst:
        data = data + " " + word
        
    return data


# def clean_enhance_text(text):
#     syns = []
#     ants = []
    
#     #print(f"Step 0: all words in the passage are {word_tokenize(text)} \n\n\n")
#     clear_text = clean(text)
#     enhance = list(set([w for w in word_tokenize(clear_text)]))
    
#     for word in enhance:
#         for synset in wn.synsets(word): 
#             for syn in synset.lemmas(): 
#                 syns.append(syn.name()) 
            
#                 if syn.antonyms(): 
#                     ants.append(syn.antonyms()[0].name()) 
                    
#     syns.extend(ants)               
#     syns_ants = list(set(syns))
#     syns_ants_str = ""
#     for word in syns_ants:
#         syns_ants_str = syns_ants_str + " " + word 
#     syns_ants_str = clean(syns_ants_str)
#     syns_ants = [word for word in word_tokenize(syns_ants_str)]
    
#     enhance.extend(syns_ants)
#     cleaned_enhanced_text = ""
#     for word in enhance:
#         cleaned_enhanced_text = cleaned_enhanced_text + " " + word 

#     return cleaned_enhanced_text


