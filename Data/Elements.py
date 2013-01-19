import Data.Tokens
import Data.Text
import NLP.Sentencer
import NLP.Tokenizer
import NLP.Stopwords

class Elements:
    """Object containing obj.tokens and obj.texts with some additional convenience methods on the top."""
    def __init__(self,sentencer='', tokenizer=' ', language='', stopwords='' ):
        self.sentencer = NLP.Sentencer( sentencer, language )
        self.tokenizer = NLP.Tokenize( tokenizer, language )
        self.tokens = Elements.Tokens()
        self.texts = Element.Texts()
        self.active = 'tokens'
        if stopwords:
            self.stopwords = NLP.Stopwords( stopwords )

    def add_data(self, source, sentence ):
        """Convenience method to process a sentence into the text and token containers."""
        tokens=self.tokenizer.tokenize(sentence)
        self.texts.text( source )
        self.texts.add_token_idx( self.token.add_token(tokens) )

# TODO: decide on the interface. Perhaps asking for the texts and tokens object when
# those are acting separate, and writing the convenience methods here only. But that looks 
# awkward to make this module triple faced

