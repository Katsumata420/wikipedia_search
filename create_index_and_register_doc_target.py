import os
import sys
import json

from lemmatizer import lemmatizer
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from joblib import Parallel, delayed

import ipadic
import fugashi

client = Elasticsearch()
BATCH_SIZE = 1000
INDEX_NAME_TARGET = "twitter_covid"  # target-domain name
       
        
def index_batch(docs):
    requests = Parallel(n_jobs=-1)([delayed(get_request)(doc) for doc in docs])
    bulk(client, requests)


def get_request(doc):
    return {"_op_type": "index",
            "_index": INDEX_NAME_TARGET,
            "text": doc['text'],
            "title": doc['title'],
            "id": doc['id']
            }


def main(args):
    input_dir = Path(args[1])
    input_files = list(input_dir.glob("**/*.txt"))
    # input_files = list(input_dir.glob("**/*.html"))

    client.indices.delete(index=INDEX_NAME_TARGET, ignore=[404])
    with open("index_target.json") as index_file:
        source = index_file.read().strip()
        client.indices.create(index=INDEX_NAME_TARGET, body=source)

    dic_dir = ipadic.DICDIR
    mecabrc = os.path.join(dic_dir, "mecabrc")
    mecab_option = f'-d "{dic_dir}" -r "{mecabrc}" '
    tokenizer = fugashi.GenericTagger(mecab_option)
    
    docs = []
    count = 0
    len_all = len(input_files)
    for i, input_file in enumerate(input_files):
        doc = dict()
        doc['id'] = i
        doc['title'] = input_file.stem
        doc['text'] = ''
        with input_file.open(mode='r') as f:
            for line in f:
                doc['text'] += lemmatizer(line.strip(), tokenizer)

        docs.append(doc)
        count += 1
        
        if count % BATCH_SIZE == 0:
            index_batch(docs)
            docs = []
            print(f"Indexed {count} documents. {100.0*count/len_all}%")
    
    if docs:
        index_batch(docs)
        print("Indexed {} documents.".format(count))
    
            
if __name__ == "__main__":
    args = sys.argv
    main(args)
