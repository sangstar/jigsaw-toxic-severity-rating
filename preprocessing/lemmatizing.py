import nltk
from nltk.tag.stanford import StanfordPOSTagger
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


mappings = {}
mappings['JJ'] = 'a'
mappings['JJR'] = 'a'
mappings['JJS'] = 'a'
mappings['NN'] = 'n'
mappings['NNS'] = 'n'
mappings['NNP'] = 'n'
mappings['NNPS'] = 'n'
mappings['RB'] = 'r'
mappings['RBR'] = 'r'
mappings['RBS'] = 'r'
mappings['VB'] = 'v'
mappings['VBD'] = 'v'
mappings['VBG'] = 'v'
mappings['VBN'] = 'v'
mappings['VBP'] = 'v'
mappings['VBZ'] = 'v'

def get_POSTagger():
    _path_to_model = 'stanford-postagger/models/english-bidirectional-distsim.tagger'
    _path_to_jar = 'stanford-postagger/stanford-postagger.jar'
    st = StanfordPOSTagger(model_filename=_path_to_model, path_to_jar=_path_to_jar)
    return st

def POS_tag(tokens):
    st = get_POSTagger()
    return st.tag(tokens.split())

def get_proper_lemma(word, POS):
    try:
        mappings[POS]
        return lemmatizer.lemmatize(word, pos = mappings[POS])
    except KeyError:
        return lemmatizer.lemmatize(word)

def lemmatize_doc(doc):
    tags = POS_tag(doc)
    lemmatized_doc = ""
    for tuples in tags:
        lemmatized_doc += get_proper_lemma(tuples[0], tuples[1]) + " "
    return lemmatized_doc[:-1]