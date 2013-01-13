class Text_container:
    """Text container: stores the text transformed into sequences of token index numbers."""
    def __init__(self):
        self.text=[]
        self.pos=0

    def next_unit(self):
    # append only if the actual position is filled
        if self.text[ self.pos ] and len( self.text ):
            self.text.append([])
            self.pos  +=1

    def prev_unit(self):
        self.pos -= 1

    def append_token(self,token):
        self.text[ self.pos ].append( token )

    def return_text(self,Tokens=None):
    """returns the text using the reference list ( Tokens object ) if any."""
        pass

# TODO: we need to store - and also pass - the source name
# because later we may want to retrieve it
