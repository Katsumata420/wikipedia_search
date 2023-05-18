"""
wiki_subset.csv の順に、上位 n 件の titles を抽出する処理
"""

import argparse
import json
from typing import Any, Dict, List


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-csv", required=True)
    parser.add_argument("--input-titles", "-i", required=True)
    parser.add_argument("--output-nbest-titles", "-o", required=True)
    parser.add_argument("--n-best", default=100, type=int)
    return parser.parse_args()


def load_wiki_csv(file_path: str) -> List[str]:
    titles = []
    with open(file_path) as i_f:
        for line in i_f:
            line = line.strip()
            titles.append(line.split(",", 1)[1])
    return titles


def load_titles_with_nbest(input_titles_path: str, loaded_wiki_titles: List[str], n_best: int) -> List[Dict[str, Any]]:
    # load title file
    data = {}
    with open(input_titles_path) as i_f:
        for line in i_f:
            line = line.strip()
            sample = json.loads(line)
            data[sample["title"]] = sample

    # n_best 用のフィルタデータを作成する
    nbest_data = []
    for loaded_wiki_title in loaded_wiki_titles:
        sample = data.get(loaded_wiki_title)
        if sample is not None:
            nbest_data.append(sample)
            if len(nbest_data) == n_best:
                break
    return nbest_data


def save_titles(nbest_data: List[Dict[str, Any]], file_path: str) -> None:
    with open(file_path, "w") as o_f:
        for sample in nbest_data:
            output_line = json.dumps(sample, ensure_ascii=False)
            o_f.write(output_line + "\n")
    

def main():
    args = get_args()
    loaded_titles = load_wiki_csv(args.wiki_csv)
    nbest_titles = load_titles_with_nbest(args.input_titles, loaded_titles, args.n_best)
    print(f"nbest titles size: {len(nbest_titles)}")
    save_titles(nbest_titles, args.output_nbest_titles)

if __name__ == "__main__":
    main()
