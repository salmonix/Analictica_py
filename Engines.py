from Modules.Abacus import sema_attr # TODO: exactly what? 

class Attraction(object):
    def __init__(self, elements): # here we should check if 'elements' is an Elements instance
        self.elements = elements

    def receive_sentence( data ):
        for i in data:
            self.elements = process_sentence( data ) # so here we added a new sentence
            self.elements.entropy('shannon')  # recalc shannon
            # here we need the sentence, so take it
            sen = self.elements.texts.last() # TODO : implement it some way - maybe direct
            self.calculate_attraction( sen )
