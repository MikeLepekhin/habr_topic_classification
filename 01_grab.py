from bs4 import BeautifulSoup
from multiprocessing import Pool
import numpy as np
from os import listdir
import pickle
import requests


def download_document(pid):
    """ Download and process a Habr document and its comments """
    # выгрузка документа
    r = requests.get('https://habrahabr.ru/post/' + str(pid) + '/')
    # парсинг документа
    soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
    doc = {}
    doc['id'] = pid
    if not soup.find("span", {"class": "post__title-text"}):
        # такое бывает, если статья не существовала или удалена
        doc['status'] = 'title_not_found'
    else:
        doc['status'] = 'ok'
        doc['title'] = soup.find("span", {"class": "post__title-text"}).text
        doc['text'] = soup.find("div", {"class": "post__text"}).text
        doc['time'] = soup.find("span", {"class": "post__time"}).text
        doc['hubs'] = soup.find("ul", {"class": "post__hubs"}).text
        doc['likes'] = soup.find("span", {"class": "voting-wjt__counter"}).text
    
    if 'hubs' in doc:    
        # сохранение результата в отдельный файл
        clean_filename = r'clean_files/' + str(pid) + '.pkl'
        with open(clean_filename, 'wb') as f:
            pickle.dump(doc, f)
        
        html_filename = r'html_files/' + str(pid) + '.pkl'
        with open(html_filename, 'w') as html_out:
            html_out.write(r.text)
            
def main():
    print("### parsing started")
    
    with Pool(10) as p:
        docs = p.map(download_document, np.arange(150000, 500000))
        
    print("### parsing finished")
        
if __name__ == '__main__':
    main()