import pickle
import string

from os import listdir


def parse_hubs(raw_hubs):
    hub_list = [hub_str.strip().lower() for hub_str in raw_hubs.strip().replace(', ', '').split('\n')]
    return [hub for hub in hub_list if hub]

def get_relevant_documents(query, relevant_hubs=None):
    translator = str.maketrans('', '', string.punctuation)
    query = query.lower().translate(translator)
    filenames = sorted(listdir('clean_files'))

    all_documents = [pickle.load(open(f'clean_files/{filename}', 'rb')) for filename in filenames]
    relevant_documents = []
    
    for document in all_documents:
        if query in document['title'].lower():
            relevant_documents.append(document)
    return relevant_documents, filenames
