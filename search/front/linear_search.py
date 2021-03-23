import pickle
import string
import os

from os import listdir


def parse_hubs(raw_hubs):
    hub_list = [hub_str.strip().lower() for hub_str in raw_hubs.strip().replace(', ', '').split('\n')]
    return [hub for hub in hub_list if hub]

def get_relevant_documents(query, data_dir, relevant_hubs=None):
    translator = str.maketrans('', '', string.punctuation)
    query = query.lower().translate(translator)
    
    all_documents = [pickle.load(open(os.path.join(data_dir, filename), 'rb')) for filename in listdir(data_dir)]
    relevant_documents = []
    
    for document in all_documents:
        if query in document['title'].lower():
            relevant_documents.append(document)
    return relevant_documents, listdir(data_dir)