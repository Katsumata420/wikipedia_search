import sys
import numpy as np
from pathlib import Path
from lemmatizer import lemmatizer
from elasticsearch import Elasticsearch
from pprint import pprint

client = Elasticsearch()
INDEX_NAME = "wikipedia"
SIZE = 1


def main(args):
    input_dir = Path(args[1])
    input_files = list(input_dir.glob('**/*.txt'))

    len_all = len(input_files)
    scores = dict()
    for i, input_file in enumerate(input_files):
        title = input_file.stem
        query = ''
        print(title)
        with input_file.open(mode='r') as f:
            for line in f:
                query += line.strip()
                query += " "

        lemma_query = lemmatizer(query)
        script_query = {
            "query": {
                "more_like_this": {
                    "fields": ["text"],
                    "like": lemma_query,
                    "min_term_freq": 1,
                    "max_query_terms": 500,
                    "min_doc_freq": 1
                }
            }
        }

        response = client.search(index=INDEX_NAME,
                                 body=script_query,
                                 size=SIZE,
                                 request_timeout=60)

        for hit in response['hits']['hits']:
            hit_title = hit['_source']['title']
            if hit_title == title:
                continue
            score = hit['_score']
            if hit_title in scores:
                scores[hit_title] += score
            else:
                scores[hit_title] = score

    scores_val = sorted(scores.values())
    print("hits: {}/{}".format(len(scores_val), len_all))
    coef = 0.1
    threshold_index = int(coef * len(scores_val))
    
    threshold_score = scores_val[threshold_index]
    with open('threshold_score.txt', 'w') as f:
        print(threshold_score, file=f)


if __name__ == '__main__':
    args = sys.argv
    main(args)
