import unittest
from tokenize_text import do_tokenize_text
from do_nltk_downloads import do_nltk_downloads

example_text = '''Python includes a number of data types that are used to distinguish a particular type of data. For example, Python strings are used to represent text-based data, and integers can represent whole numbers. When you’re programming, you may want to convert values between different data types so you can work with them in different ways.

One common operation is to convert a Python string to an integer or an integer to a string. Python includes built-in methods that can be used to perform these conversions'''


class TestTokenize(unittest.TestCase):
    def test_tokenize_text(self):
        do_nltk_downloads()
        ret = do_tokenize_text(example_text)
        print(*ret, sep='\n')


if __name__ == '__main__':
    unittest.main()
