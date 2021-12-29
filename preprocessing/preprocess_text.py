from preprocessing.lemmatizing import lemmatize_doc
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
import numpy as np

nltk.download('stopwords')
symbols = list(string.punctuation + "®")
stops = stopwords.words('english')
full_stops = stops + symbols

print('symbols: ', symbols)

def strip_symbols(doc): 
    tokens = doc.split(" ")
    new_tokens = []
    for token in tokens:
        if token != "":
            new_token = token
            for symbol in symbols:
                if symbol in token:
                    new_token = new_token.replace(symbol," ")
            new_token = new_token.split(" ")
            new_tokens.append(new_token)
    tokens = flatten_irregular_list(new_tokens)
    return tokens

def flatten_irregular_list(li):
    returnArray = []
    for vals in li:
        if isinstance(vals, list):
            for val in vals:
                returnArray.append(val)
        else:
            returnArray.append(vals)
    return returnArray


def pre_process_text(doc):
    doc = doc.lower()
    tokens = strip_symbols(doc)
    output = ""
    for token in tokens:
        if token not in full_stops and token.isalpha():
                output += token.lower() + " "
    return lemmatize_doc(output[:-1])