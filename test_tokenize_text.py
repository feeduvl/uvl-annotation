from unittest import TestCase

import jsonpickle

from do_nltk_downloads import do_nltk_downloads
from example_data import example_dataset, example_dataset_komoot
from tokenize_text import do_tokenize_dataset

sentenceTokenisation_activated = True


class Test(TestCase):
    def test_do_tokenize_dataset_wordbased(self):
        do_nltk_downloads()
        annotation = do_tokenize_dataset(
            "example annotation", example_dataset, not sentenceTokenisation_activated)
        self.assertTrue(len(annotation.codes) == len(
            annotation.tore_relationships) == 0)
        self.assertEqual(len(annotation.docs), 14)
        self.assertEqual(len(annotation.tokens), 3171)
 
        self.assertEqual(annotation.tokens[0].pos, "r")
        self.assertEqual(annotation.tokens[1].pos, "v")
        self.assertEqual(annotation.tokens[2].pos, "")
 
        self.assertEqual(annotation.tokens[0].name, "Here")
        self.assertEqual(annotation.tokens[1].name, "is")
        self.assertEqual(annotation.tokens[2].name, "a")
 
        self.assertEqual(annotation.tokens[0].lemma, "here")
        self.assertEqual(annotation.tokens[1].lemma, "be")
        self.assertEqual(annotation.tokens[2].lemma, "a")
 
        self.assertEqual(annotation.tokens[-1].pos, "")
        self.assertEqual(annotation.tokens[-2].pos, "r")
        self.assertEqual(annotation.tokens[-3].pos, "")
 
        self.assertEqual(annotation.tokens[-1].name, ".")
        self.assertEqual(annotation.tokens[-2].name, "there")
        self.assertEqual(annotation.tokens[-3].name, "in")
 
        self.assertEqual(annotation.tokens[-1].lemma, ".")
        self.assertEqual(annotation.tokens[-2].lemma, "there")
        self.assertEqual(annotation.tokens[-3].lemma, "in")
 
    def test_do_tokenize_dataset_sentencebased(self):
        do_nltk_downloads()
        annotation = do_tokenize_dataset(
            "example annotation", example_dataset, sentenceTokenisation_activated)
        self.assertTrue(len(annotation.codes) == len(
            annotation.tore_relationships) == 0)
 
        self.assertEqual(annotation.tokens[0].pos, None)
        self.assertEqual(annotation.tokens[1].pos, None)
        self.assertEqual(annotation.tokens[2].pos, None)
 
        self.assertEqual(
            annotation.tokens[0].name, "Here is a big Moodle logo and then there are the categories here.")
        self.assertEqual(
            annotation.tokens[1].name, "Moodle is super well structured Moodle is for me.")
        self.assertEqual(
            annotation.tokens[2].name, "For example, when I Moodle be click here, I see the titles above it.")
 
        self.assertEqual(annotation.tokens[0].lemma, None)
        self.assertEqual(annotation.tokens[1].lemma, None)
        self.assertEqual(annotation.tokens[2].lemma, None)
 
        self.assertEqual(annotation.tokens[-1].pos, None)
        self.assertEqual(annotation.tokens[-2].pos, None)
        self.assertEqual(annotation.tokens[-3].pos, None)
 
        self.assertEqual(
            annotation.tokens[-1].name, "So then I can hand them in there.")
        self.assertEqual(
            annotation.tokens[-2].name, "Sometimes I have to download the materials, that means that I have them at home and then I can work on the assignments and then I can upload them there.")
        self.assertEqual(
            annotation.tokens[-3].name, "Then I look, if there is a new assignment and I look at the new assignments.")
 
        self.assertEqual(annotation.tokens[-1].lemma, None)
        self.assertEqual(annotation.tokens[-2].lemma, None)
        self.assertEqual(annotation.tokens[-3].lemma, None)
    
    def test_do_tokenize_dataset_sentencebased_komoot(self):
        do_nltk_downloads()
        annotation = do_tokenize_dataset(
            "example annotation", example_dataset_komoot, sentenceTokenisation_activated)
 
        self.assertEqual(
            annotation.tokens[0].name, "1\n###") 
        self.assertEqual(
            annotation.tokens[1].name, "This is a Komoot-Review.") 
        self.assertEqual(
            annotation.tokens[2].name, "The App is very slow.") 
        self.assertEqual(
            annotation.tokens[3].name, "This is the last sentence.") 
        self.assertEqual(
            annotation.tokens[4].name, "###")

    def test_do_tokenize_dataset_sentencebased_with_adjust_document_sentences(self):
        do_nltk_downloads()

        # test ### within text     
        x = [{"text": '''1\n### This is a ### Komoot-Review. ###''', "id": "document 1"}]        
        annotation = do_tokenize_dataset(
            "example annotation", x, sentenceTokenisation_activated)
        self.assertEqual(
            annotation.tokens[0].name, "1\n###")
        self.assertEqual(
            annotation.tokens[1].name, "This is a ### Komoot-Review.") 
        self.assertEqual(
            annotation.tokens[2].name, "###")    

        # test reviews end without dot     
        x = [{"text": '''1\n### This is a Komoot-Review ###''', "id": "document 1"}]        
        annotation = do_tokenize_dataset(
            "example annotation", x, sentenceTokenisation_activated)
        self.assertEqual(
            annotation.tokens[0].name, "1\n###")
        self.assertEqual(
            annotation.tokens[1].name, "This is a Komoot-Review ###") 

        # test beginning review with ###
        x = [{"text": '''1\n######This is a Komoot-Review. ###''', "id": "document 1"}]        
        annotation = do_tokenize_dataset(
            "example annotation", x, sentenceTokenisation_activated)
        self.assertEqual(
            annotation.tokens[0].name, "1\n###")
        self.assertEqual(
            annotation.tokens[1].name, "###This is a Komoot-Review.") 
        
       # test beginning ### (NOT komoot review)
        x = [{"text": '''###This is a Review.''', "id": "document 1"}]        
        annotation = do_tokenize_dataset(
            "example annotation", x, sentenceTokenisation_activated)
        self.assertEqual(
            annotation.tokens[0].name, "###This is a Review.") 

