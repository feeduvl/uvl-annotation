from nltk import word_tokenize, sent_tokenize, pos_tag, download
from nltk.stem import WordNetLemmatizer
import json
from nltk.corpus import wordnet
import re


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    if treebank_tag.startswith('R'):
        return wordnet.ADV
    return ""


class Token:
    def __init__(self, index: int, name: str, lemma: str, pos: str):
        # for convenience, set this attribute here so that it appears as 'null' on the client-side
        self.index = index
        self.name = name
        self.lemma = lemma
        self.pos = pos
        self.num_name_codes = 0  # number of codes using this token which have a non-empty name
        self.num_tore_codes = 0

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


def do_tokenize_dataset(name: str, documents: list, sentenceTokenizationEnabledForAnnotation: bool) -> Annotation:
    '''Given a list of documents, return the tokenization of these documents such that the document membership of each token can be identified

    :param name: Name of the dataset
    :param documents: List, that contains the documents (these include for example the text)
    :param sentenceTokenizationEnabledForAnnotation: Boolean, that says if has to be returned a sentence-based or word-based annotation

    :return: Word-based Annotation or Sentence-based Annotation
    '''

    texts = [doc["text"] + "\n" for doc in documents]
    doc_names = [doc["id"] for doc in documents]
    documents = [DocWrapper(name, None, None) for name in doc_names]

    if not sentenceTokenizationEnabledForAnnotation:
        return tokenize_word_based(name, texts, documents)
    else:
        return tokenize_sentence_based(name, texts, documents)


def tokenize_word_based(name: str, texts: list, documents: list) -> Annotation:
    """
    Using the name, texts and documents as input, create a word-based annotation.

    :param name: Name of the dataset
    :param texts: List, that contains the texts of the dataset
    :param documents: List, that contains DocWrapper objects

    :return: Word-based Annotation
    """

    lemmatizer = WordNetLemmatizer()
    document_sentences = []
    tokens = []
    pos_tags = []

    print("texts: ", texts)

    for document_text in texts:
        # split the document into document_sentences
        print("document_text: ", document_text)
        document_sentences.append(sent_tokenize(document_text))
    for doc_index, document_sentence in enumerate(document_sentences):
        begin = len(tokens)
        for s in document_sentence:
            # computing pos tags requires whole sentences
            sentence_tokens = word_tokenize(s)

            pos_tags.extend([get_wordnet_pos(tup[1])
                            for tup in pos_tag(sentence_tokens)])
            # add to existing list, remembering number of tokens in each document
            tokens.extend(sentence_tokens)
        end = len(tokens)
        documents[doc_index].begin_index = begin
        documents[doc_index].end_index = end

    lemmas = [lemmatizer.lemmatize(t, pos=pos_tags[ind]).lower() if pos_tags[ind] != "" else t.lower()
              for ind, t in enumerate(tokens)]

    token_list = [Token(ind, name, lemmas[ind], pos_tags[ind])
                  for ind, name in enumerate(tokens)]

    return Annotation(name, token_list, documents)


def tokenize_sentence_based(name: str, texts: list, documents: list) -> Annotation:
    """
    Using the name, texts and documents as input, create a sentence-based annotation.

    :param name: Name of the dataset
    :param texts: List, that contains the texts of the dataset
    :param documents: List, that contains DocWrapper objects

    :return: Sentence-based Annotation
    """

    document_sentences = []
    tokens = []

    for document_text in texts:
        #print("document_text: ", document_text)
        document_sentences.append(
            adjust_document_sentences(sent_tokenize(document_text)))
    for doc_index, document_sentence in enumerate(document_sentences):
        begin = len(tokens)
        for sentence in document_sentence:
            # add to existing list, remembering number of tokens in each document
            tokens.append(sentence)
        end = len(tokens)
        documents[doc_index].begin_index = begin
        documents[doc_index].end_index = end

    token_list = [Token(ind, name, None, None)
                  for ind, name in enumerate(tokens)]

    return Annotation(name, token_list, documents)


def adjust_document_sentences(document_sentences: list) -> list:
    """
    For example, in the "Komoot_AppReview" dataset, at the beginning of each review there is the rating followed by three "#" 
    like for example "4###". In sentence-based tokenization, "4###" is included in the first sentence of the review, that is 
    "4###<FirstSentence>". Here, "4###<FirstSentence>" is splitted into "4###" and "<FirstSentence>".

    :param name: List, that contains the document sentences.

    :return: List, that contains the adjusted document sentences.
    """

    adjusted_document_sentences = []
    for idx, document_sentence in enumerate(document_sentences):
        #print("document_sentence: ", document_sentence)
        if idx == 0 and re.match(r'^[0-9]\n###', document_sentence):
            # Split the first sentence based on the pattern
            s1, s2 = re.split(r'(?<=[0-9]\n###)', document_sentence, maxsplit=1)
            # Remove leading whitespace from the second part
            s2 = s2.strip()
            # Append both parts to the adjusted_document_sentences list
            adjusted_document_sentences.extend([s1, s2])
        else:
            adjusted_document_sentences.append(document_sentence)

    return adjusted_document_sentences
