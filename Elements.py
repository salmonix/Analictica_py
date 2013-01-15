import Elements.Tokens
import Elements.Texts
import NLP.Sentencer
import NLP.Tokenizer
import NLP.Stopwords

class Elements:
    def __init__(self,sentencer='', tokenizer=' ', language='', stopwords='' ):
        self.sentencer = NLP.Sentencer( sentencer, language )
        self.tokenizer = NLP.Tokenize( tokenizer, language )
        self.tokens = Elements.Tokens()
        self.texts = Element.Texts()
        self.active = 'tokens'
        if stopwords:
            self.stopwords = NLP.Stopwords( stopwords )

    def add_data(self, source, sentence ):
        tokens=self.tokenizer.tokenize(sentence)
        self.tokens.add_token(tokens) # we need the returned value of idxs for texts
        self.texts.text( source )
        self.texts.add_token_idx( idxs )

# TODO: decide on the interface. Perhaps asking for the texts and tokens object when
# those are acting separate, and writing the convenience methods here only. But that looks 
# awkward to make this module triple faced

