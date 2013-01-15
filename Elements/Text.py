import array

class Textlist:
    """Text container: stores the text transformed into sequences of token index numbers.
    """
    def __init__(self):
        self.text={}
        self.active=''

    def text(self, source):
        """Start a new text unit."""
        if self.text[source]:
            return self.text[source]

        self.text[source] = array.array('L') # we use long ints
        self.active = source

    def add_token_idx(self,idx):
         self.text[ self.active ].append(idx)

    def get_text(self,text=[]):
        """Returns a title, text_array tuple for the given text titles. If nothing is passed returns for all."""
        if text == []:   # this is perlish because we can make it an iterator on hash which might be better
            text = self.text.keys()
            for i in text:
                yield (i, self.text[i])
