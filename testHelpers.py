

def recall_text(elements):
    texts = elements.sentences
    tokens = elements.tokens
    text_iter = texts.get_sentences()

    for sentences in text_iter:
        recalled_text_id = []
        recalled_text = []
        for s in sentences:
            recalled_text_id.append(s)
            recalled_text.append(tokens.tokens[s].name)
        print (recalled_text_id)
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
