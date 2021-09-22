import unittest

import jsonpickle

from tokenize_text import do_tokenize_dataset
from do_nltk_downloads import do_nltk_downloads
from example_data import example_dataset


class TestTokenize(unittest.TestCase):
    def test_tokenize_text(self):
        do_nltk_downloads()
        ret = jsonpickle.encode(do_tokenize_dataset(example_dataset))
        # app.logger.debug("Returning: "+ret)
        print("Returning: " + ret)
        return ret


if __name__ == '__main__':
    unittest.main()
