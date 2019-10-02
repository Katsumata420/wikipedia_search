import sys
from pathlib import Path
from lemmatizer import lemmatizer
from elasticsearch import Elasticsearch
from pprint import pprint


client = Elasticsearch()
SEACH_SIZE = 10
INDEX_NAME = "wikipedia"
DOC_TYPE = "simple"


def main(args):
    target = input("Enter query index: ")
    
    script_query = {
        "query": {
            "more_like_this": {
                "fields": ["text"],
                "like": [{"_index": target, "_id": "uBF5Z20B1-sPJ8-evmR0"}],
                "min_term_freq": 1,
                "max_query_terms": 30,
                "min_doc_freq": 1
            }
        }
    }
    
    response = client.search(index=INDEX_NAME,
                             body=script_query,
                             _source=False,
                             size=5)
    pprint(response)


if __name__ == '__main__':
    args = sys.argv
    main(args)
