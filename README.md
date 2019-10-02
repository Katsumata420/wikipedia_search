# wikipedia_search
文書集合からwikipediaの似た記事を取得する。
参考論文：Topic Sensitive Attention on Generic Corpora Corrects Sense Bias in Pretrained Embeddings

## 手順
1. `$ docker-compose up` を行い、elasticsearchを起動する
  - `$curl http://127.0.0.1:9200/_cat/health`で結果が返ってくれば、起動成功

2. `$ create_index_and_register_doc_wiki.py /path/to/wikipedia_corups` を実行し、ソースコーパスのindexを作成
  - wikipediaのdumpfileをwikiextractorでjsonに変更したものを想定
  - フィールドの変更等indexの設定変更を行う場合は `index_wiki.json`を編集する
  
3. `create_index_and_register_doc_target.py /path/to/target_corpus` を実行し、ターゲットコーパスのindexを作成
  - 1文書1ファイルのテキストデータを想定
  - フィールドの変更等indexの設定変更を行う場合は `index_target.json`を編集する

4. `get_threshold.py /path/to/target_corpus` を実行し、閾値のスコアを取得する

5. `get_source_subset.py /path/to/target_corpus` を実行し、ソースコーパスの内、類似している文書のidとtitleを取得する

## その他
- lemmatizer.py: mecabで原形を取得するためのスクリプト

### 設定ファイル
docker-compose.yml: elastic-searchのdockerの設定ファイル
index_target.json: target corpusのindexの設定ファイル
index_wiki.json: source corpusのindexの設定ファイル
