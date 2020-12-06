import json


def read_data(path):
    
    data = ""
    with open(path,'r',encoding="utf8") as json_file:
        data = json.load(json_file)
    return data

def get_dictionary(news):
    
    title_content_dict = {}
    i = 0

    for i in range(0,len(news)):
        title_content_dict.update({news[i]["title"]:news[i]["content"]})
    
    return title_content_dict   

