import argparse
import json
import os
import pickle
import time

import traceback

import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

INDEX_NAME = 'habrhabr_posts'
CONFIG = 'configs/'
FILES = '/tmp/clean_files'

def json_load(fp):
    with open(fp, 'r') as f:
        d = json.load(f)
    return d


def create_index(client, args):
    """Creates an index in Elasticsearch if one isn't already there."""
    mapping = json_load(os.path.join(args.config, 'mapping.json'))
    settings = json_load(os.path.join(args.config, 'analyzer.json'))

    body = {**mapping[INDEX_NAME], **settings[INDEX_NAME]}

    client.indices.create(
        index=INDEX_NAME,
        body=body
    )


def generate_actions():
    """
    Generator of insert queries
    """
    response = {
        '_index' : INDEX_NAME,
        '_type' : '_doc',
        '_id' : "0",
        '_source' : {
            'title' : "",
            'text' : "",
            'hubs' : ""
        }
    }

    for filename in os.listdir(FILES):
        one_file = pickle.load(open(os.path.join(FILES, filename), 'rb'))
        response['_id'] = str(one_file['id'])
        response['_source'] = {
            'title' : one_file['title'],
            'text' : one_file['text'],
            'hubs' : one_file['hubs']
        }
        yield response


def main(args):
    while True:
        try:
            client = Elasticsearch(['http://elasticsearch:9200/'], timeout=30, max_retries=10, retry_on_timeout=True)
            index_exists = client.indices.exists(index=INDEX_NAME)
            break   
        except Exception as e:
            print('Elastic connection failed')
            print(e)
            # traceback.print_stack()
            time.sleep(1)


    if index_exists:
        client.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    
    print("Creating an index...")
    create_index(client, args)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=len(os.listdir(FILES)))
    successes = 0
    for ok, action in streaming_bulk(
            client=client, index=INDEX_NAME, actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, len(os.listdir(FILES))))
    # else:
    #     print("Index already exists.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='train')
    parser.add_argument('--config', type=str, help='config dir', default=CONFIG)
    args = parser.parse_args()
    main(args)
