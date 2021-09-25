
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
        self.name = name
        self.lemma = lemma
        self.pos = pos
        self.num_codes = 0  # number of codes using this token

    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Annotation:
    def __init__(self, name: str, tokens: list, docs: list):
        self.tokens = tokens
        self.codes = []
        self.tore_relationships = []
        self.docs = docs
        self.name = name


class DocWrapper:
    def __init__(self, document_name: str, begin_index: int, end_index: int):
        self.name = document_name
        self.begin_index = begin_index
        self.end_index = end_index


def do_tokenize_dataset(name: str, documents: list) -> Annotation:
    '''Given a list of documents, return the tokenization of these documents such that the document membership of each token can be identified
    :param text: input text
    :return:
    '''

    texts = [doc["text"] + "\n" for doc in documents]
    doc_names = [doc["id"] for doc in documents]
    documents = [DocWrapper(name, None, None) for name in doc_names]

    lemmatizer = WordNetLemmatizer()

    sentences = []  # list of lists

    for document_text in texts:
        sentences.append(sent_tokenize(document_text))  # split the document into sentences

    tokens = []
    pos_tags = []

    for doc_index, document_sentences in enumerate(sentences):
        begin = len(tokens)
        for s in document_sentences:
            # computing pos tags requires whole sentences
            sentence_tokens = word_tokenize(s)
            pos_tags.extend([get_wordnet_pos(tup[1]) for tup in pos_tag(sentence_tokens)])
            tokens.extend(sentence_tokens)  # add to existing list, remembering number of tokens in each document
        end = len(tokens)
        documents[doc_index].begin_index = begin
        documents[doc_index].end_index = end

    lemmas = [lemmatizer.lemmatize(t, pos=pos_tags[ind]).lower() if pos_tags[ind] is not None else t.lower()
              for ind, t in enumerate(tokens)]

    token_list = [Token(ind, name, lemmas[ind], pos_tags[ind]) for ind, name in enumerate(tokens)]

    return Annotation(name, token_list, documents)


