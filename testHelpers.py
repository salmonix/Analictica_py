

def recall_text(elements, by='id'):
    texts = elements.sentences
    tokens = elements.tokens

    text_iter = None
    if by == 'id':
        text_iter = texts.get_sentences_by_id()
    elif by == 'object':
        text_iter = texts.get_sentences_by_object()
    elif by == 'name':
        text_iter = texts.get_sentences_by_name()

    for sentences in text_iter:
        recalled_text = []
        for s in sentences:
            recalled_text.append(s)

        print ('TEXT by ' + by)
        print (recalled_text)

def print_tokens(tokens):
    for t in tokens.tokens:
        print('name: ' + t.name + ' | idx: ' + str(t.idx) + ' | freq: ' + str(t.freq) + ' | S: ' + str(t.Space))
        print('co_occurrence' + str(t.co_occurrence))
        print('prob.: ' + str(t.probability) + ' entropy: ' + str(t.shannon) + "\n")

def print_PMI(tokens):
    tokens = tokens.tokens
    for t in tokens:
        result = []
        for c in t.co_occurrence.keys():
            PMI = t.PMI(tokens[c])
            result.append(str(c) + ': ' + str(PMI))
        print ('PMI: %s -> %s' % (t.idx , '  '.join(result)))
