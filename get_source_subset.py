import sys
import os
import random
import pickle
from pathlib import Path
from lemmatizer import lemmatizer
from elasticsearch import Elasticsearch
from pprint import pprint

import fugashi
import ipadic

client = Elasticsearch()
INDEX_NAME = "wikipedia"
SIZE = 100

is_random = True
random_size = 1000

def main(args):
    input_dir = Path(args[1])
    input_files = list(input_dir.glob('**/*.txt'))
    # input_files = list(input_dir.glob('**/*.html'))
    with open('threshold_score.txt', 'r') as f:
        for line in f:
            threshold_score = float(line.strip())
    if is_random:
        input_files = random.sample(input_files, random_size)

    dic_dir = ipadic.DICDIR
    mecabrc = os.path.join(dic_dir, "mecabrc")
    mecab_option = f'-d "{dic_dir}" -r "{mecabrc}" '
    tokenizer = fugashi.GenericTagger(mecab_option)

    print(f"threshold: {threshold_score}")
    scores = dict()
    for i, input_file in enumerate(input_files):
        title = input_file.stem
        query = ''
        print(title)
        with input_file.open(mode='r') as f:
            for line in f:
                query += line.strip()
                query += " "

        lemma_query = lemmatizer(query, tokenizer)
        script_query = {
            "query": {
                "more_like_this": {
                    "fields": ["text"],
                    "like": lemma_query,
                    "min_term_freq": 1,
                    "max_query_terms": 5000,
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
            hit_id = hit['_source']['id']
            identifier = (hit_id, hit_title)
            if hit_title == title:
                continue
            score = hit['_score']
            if identifier in scores:
                scores[identifier] += score
            else:
                scores[identifier] = score

    candidate = set()
    with open('wiki_subset.csv', 'w') as f:
        for k, v in scores.items():
            if v > threshold_score:
                print("{},{}".format(k[0], k[1]))
                print("{},{}".format(k[0], k[1]), file=f)
                candidate.add(k)

    with open('wiki_subset.pkl', 'wb') as f:
        pickle.dump(candidate, f)


if __name__ == '__main__':
    args = sys.argv
    main(args)
