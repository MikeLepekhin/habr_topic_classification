import pickle

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from linear_search import *
from os import listdir

app = Flask(__name__, template_folder='templates', static_folder='templates')

def parse_hubs(raw_hubs):
    hub_list = [hub_str.strip().lower() for hub_str in raw_hubs.strip().replace(', ', '').split('\n')]
    return [hub for hub in hub_list if hub]

def get_like_value(like_str):
    if like_str == '0':
        return 0
    if len(like_str) == 1:
        return 1 if like_str == '+' else -1
    if like_str[0] != '+':
        return -int(like_str[1:])
    return int(like_str[1:])

@app.route('/')
def search_form():
    param_dict = request.args.to_dict()
    current_query = param_dict['q'].strip() if 'q' in param_dict else ''
    current_cat = param_dict['cat'].strip().lower() if 'cat' in param_dict else ''
    
    documents, filenames = get_relevant_documents(current_query) 
    for document, filename in zip(documents, filenames):
        document["doc_id"] = filename[:filename.find('.')]

    for document in documents:
        document["hubs"] = parse_hubs(document["hubs"])
    if current_cat:
        documents = [document for document in documents if current_cat in document['hubs']]

    results_num = len(documents)
    
    DOCUMENTS_PER_PAGE = 10
    pages_num = results_num // DOCUMENTS_PER_PAGE + (results_num % DOCUMENTS_PER_PAGE != 0) 
    current_page_id = int(param_dict['page']) if 'page' in param_dict else 1
    min_doc_id = (current_page_id - 1) * 10
    max_doc_id = min(current_page_id * 10, results_num)


    full_path = request.full_path.replace('?&', '?')
    
    if 'page' in param_dict:
        full_path = full_path.replace(f'page={param_dict["page"]}', 'page=[PAGE_NUM]')
    else:
        full_path += "&page=[PAGE_NUM]"

    return render_template("search.html", query=current_query, results_num=results_num, pages_num=pages_num, 
                           current_page_id=current_page_id, full_path=full_path, 
                           documents=documents[min_doc_id:max_doc_id])


@app.route('/send_request', methods=['POST'])
def redirect_to_results():
    query = request.form['query']
    return redirect(f'/?q={query}')

@app.route('/view_doc')
def view_doc():
    param_dict = request.args.to_dict()
    current_doc = param_dict['id'].strip() if 'id' in param_dict else ''
    
    try:
        print(listdir('clean_files'))
        document = pickle.load(open(f'clean_files/{current_doc}.pkl', 'rb'))
    except:
        return render_template("view_doc.html", document=None)

    document["doc_id"] = current_doc
    document["hubs"] = parse_hubs(document["hubs"])
    return render_template("view_doc.html", document=document)
