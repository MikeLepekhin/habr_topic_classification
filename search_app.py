from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from linear_search import *

app = Flask(__name__, template_folder='.')

@app.route('/')
def search_form():
    param_dict = request.args.to_dict()
    current_query = param_dict['q'] if 'q' in param_dict else ''
    documents = get_relevant_documents(current_query) 
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
