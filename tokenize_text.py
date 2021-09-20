
from nltk import word_tokenize, sent_tokenize, pos_tag, download
from nltk.stem import WordNetLemmatizer
import json
from nltk.corpus import wordnet


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


class Token:
    def __init__(self, index: int, name: str, lemma: str, pos: str):
        # for convenience, set this attribute here so that it appears as 'null' on the client-side
        self.index = index
        self.token_cluster = None
        self.name = name
        self.lemma = lemma
        self.pos = pos

    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def do_tokenize_text(text: str) -> list:
    '''
    Tokenize a text according to the annotator API.
    :param text: input text
    :return:
    '''

    lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(text)
    sentence_tokens = [word_tokenize(s) for s in sentences]  # list of lists

    # computing pos tags requires whole sentences
    pos_tags = [get_wordnet_pos(tup[1]) for s in sentence_tokens for tup in pos_tag(s)]

    tokens = [t for s in sentence_tokens for t in s]

    lemmas = [lemmatizer.lemmatize(t, pos=pos_tags[ind]) if pos_tags[ind] is not None else t
              for ind, t in enumerate(tokens)]

    ret = [Token(ind, name, lemmas[ind], pos_tags[ind]) for ind, name in enumerate(tokens)]
    return ret


