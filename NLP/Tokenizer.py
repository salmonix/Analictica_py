import re
from nltk.tokenize.punkt import PunktWordTokenizer

class Tokenizer:
    def __init__(self, tokenizer='PunktWord', stopwords=''):
        if tokenizer == 'PunktWord':
            self.tokenizer = PunktWordTokenizer()

    def get_tokens(string):
        return self.tokenizer.tokenize(string)
