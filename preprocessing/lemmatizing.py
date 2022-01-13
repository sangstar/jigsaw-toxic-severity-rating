import nltk
from nltk.tag.stanford import StanfordPOSTagger
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


lemmatizer = WordNetLemmatizer()

_path_to_model = 'stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = 'stanford-postagger/stanford-postagger.jar'
st = StanfordPOSTagger(model_filename=_path_to_model, path_to_jar=_path_to_jar, java_options = '-Xmx4G')


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

def prevent_memory_bloat(tokens):
    # This isn't a great workaround as its eliminating information for the sake of memory. Try and look in to either
    # increasing available java memory or something else
    # It also stops in the middle of a comment
    sensor = tokens.split(" ")
    print('len tokens:', len(tokens))
    if len(set(sensor)) < 3 and len(tokens) > 500:
        return " ".join(sensor[:15])

    elif len(tokens) > 1000:
        print('too many tokens for memory')
        return tokens[:800]
    #elif len(tokens) > 500:
    #    print('spam flagged. Reducing size for memory')
    #    return tokens[:250]
    else:
        return tokens



def POS_tag(tokens):
    #tokens = prevent_memory_bloat(tokens)
    #print('tokens: ', tokens)
    token_list = tokens.split()
    try:
        return st.tag(sorted(set(token_list), key = token_list.index))
    except OSError:
        print('resorting to nltk pos tagging.')
        return nltk.pos_tag(sorted(set(token_list), key = token_list.index))



def get_proper_lemma(word, POS):
    wn.ensure_loaded()
    try:
        mappings[POS]
        return lemmatizer.lemmatize(word, pos = mappings[POS])
    except KeyError:
        return lemmatizer.lemmatize(word)

def lemmatize_doc(doc):
    tags = POS_tag(doc)
    #print('tags to lemmatize: ', tags)
    lemmatized_doc = ""
    for tuples in tags:
        lemmatized_doc += get_proper_lemma(tuples[0], tuples[1]) + " "
    return lemmatized_doc[:-1]