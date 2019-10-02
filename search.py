import sys
from pathlib import Path
from lemmatizer import lemmatizer
from elasticsearch import Elasticsearch
from pprint import pprint


client = Elasticsearch()
SEACH_SIZE = 10
INDEX_NAME = "target"
DOC_TYPE = "simple"


def main(args):
    query = input("Enter query text: ")
    print(type(query))
    
    script_query = {
        "query": {
            "match": {
                "text": lemmatizer(query),
            }
        }
    }

    script_query = {
        "query": {
            "match_all": {}
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
