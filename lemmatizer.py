import fugashi
import ipadic

import os
import functools

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation

def lemmatizer(text, mecab, poses={"名詞", "動詞", "形容詞", "副詞"}):
    split_punc2 = functools.partial(split_punctuation, punctuations=r"。!?")
    concat_tail_te = functools.partial(concatenate_matching, former_matching_rule=r"^(?P<result>.+)(て)$", remove_former_matched=False)
    segmenter = make_pipeline(normalize, split_newline, concat_tail_te, split_punc2)

    """
    dic_dir = ipadic.DICDIR
    mecabrc = os.path.join(dic_dir, "mecabrc")
    mecab_option = f'-d "{dic_dir}" -r "{mecabrc}" '
    mecab = fugashi.GenericTagger(mecab_option)
    """
    mecab.parse("")
    sents = [s for s in segmenter(text)]
    tokens = []
    for sent in sents:
        nodes = mecab(sent)
        for node in nodes:
            features = node.feature
            lemma = features[6]
            pos = features[0]
            if pos in poses and lemma != "*":
                tokens.append(lemma)
        
    return ' '.join(tokens)
