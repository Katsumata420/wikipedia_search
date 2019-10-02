import MeCab


def lemmatizer(text, poses={"名詞", "動詞", "形容詞", "副詞"}):
    mecab = MeCab.Tagger()
    mecab.parse("")
    node = mecab.parseToNode(text)
    tokens = []
    while node:
        features = node.feature.split(',')
        lemma = features[6]
        pos = features[0]
        if pos in poses and lemma != "*":
            tokens.append(lemma)
        node = node.next
        
    return ' '.join(tokens)
