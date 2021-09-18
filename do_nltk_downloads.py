'''
Run this script once before using tokenizer
'''
from nltk import download

def do_nltk_downloads():
    download('punkt')
    download('averaged_perceptron_tagger')
    download("wordnet")
