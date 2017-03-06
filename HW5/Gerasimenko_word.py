import json
import re
from collections import Counter


class Word:
    def __init__(self, **params):
        vars(self).update(params)

    def __repr__(self):
        return str(vars(self))
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__


def get_words(filename):
    wordarray = []
    text = open(filename,'r',encoding='utf-8-sig')
    for line in text:
        obj = json.loads(line)
        if re.search('\\w',obj['text']) is not None and obj['text'] != '\s':
            wordarray.append(obj)
    return wordarray


def wordform_dict(wordform):
    wfd = {}
    wfd['text'] = wordform['text']
    wfd['num_analyses'] = len(wordform['analysis'])
    if wordform['analysis']:
        lemmas = [x['lex'] for x in wordform['analysis']]
        wfd['lemma'] = select_most_freq(*lemmas)
        POS = [re.search('^(\\w*?)[,=]',x['gr']).group(1) for x in wordform['analysis']]
        wfd['POS'] = select_most_freq(*POS)
    else:
        wfd['lemma'] = None
        wfd['POS'] = None
    return wfd


def select_most_freq(*args):
    most_freq = Counter(args).most_common(1)[0][0]
    return most_freq


def unique_wordlist():
    words = get_words('python_mystem.json')
    word_objects = []
    for word in words:
        wf = Word(**wordform_dict(word))
        if wf not in word_objects:
            word_objects.append(wf)
    return word_objects


wordlist = unique_wordlist()
print('number of unique wordforms:',len(wordlist))
