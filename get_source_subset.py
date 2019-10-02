import sys
import pickle
from pathlib import Path
from lemmatizer import lemmatizer
from elasticsearch import Elasticsearch
from pprint import pprint


client = Elasticsearch()
INDEX_NAME = "wikipedia"
SIZE = 2000


def main(args):
    input_dir = Path(args[1])
    input_files = list(input_dir.glob('**/*.txt'))
    with open('threshold_score.txt', 'r') as f:
        for line in f:
            threshold_score = float(line.strip())

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

        lemma_query = lemmatizer(query)
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
                                 request_timeout=30)

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
                print("{}, {}".format(k[0], k[1]))
                print("{}, {}".format(k[0], k[1]), file=f)
                candidate.add(k)

    with open('wiki_subset.pkl', 'wb') as f:
        pickle.dump(candidate, f)


if __name__ == '__main__':
    args = sys.argv
    main(args)
