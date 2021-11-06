from unittest import TestCase

import jsonpickle

from do_nltk_downloads import do_nltk_downloads
from example_data import example_dataset
from tokenize_text import do_tokenize_dataset


class Test(TestCase):
    def test_do_tokenize_dataset(self):
        do_nltk_downloads()
        annotation = do_tokenize_dataset("example annotation", example_dataset)
        self.assertTrue(len(annotation.codes) == len(annotation.tore_relationships) == 0)
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


