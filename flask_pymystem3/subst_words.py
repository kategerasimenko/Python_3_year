import json
import pymorphy2
from collections import defaultdict
import random
from nltk import word_tokenize
import re


p = pymorphy2.MorphAnalyzer()

def create_pos():
    """
    create the file which is used later
    """

    d = defaultdict(set)
    with open ('lemmas.txt','r',encoding='utf-8-sig') as f:
        for line in f.readlines():
            anas = p.parse(line.strip())
            for ana in anas:
                a_lemma = ana.normalized
                if a_lemma.tag.POS == 'INFN':
                    d['VERB'].add(a_lemma.word)
                d[a_lemma.tag.POS].add(a_lemma.word)
    d = {key:list(value) for key,value in d.items()}
    with open ('lemmas_POS.txt','w',encoding='utf-8-sig') as f:
        f.write(json.dumps(d,ensure_ascii=False,indent=2))

#create_pos()

def inflect_random(word,d):
    not_changing = {'PREP','CONJ','PRCL'}
    ana_needed = p.parse(word)[0].tag
    new_gr = ana_needed.grammemes
    new_word = None
    iteration = 0
    if ana_needed.POS not in not_changing:
        while new_word is None and iteration < 50:
            lemma = random.choice(d[ana_needed.POS])
            anas_lemma = p.parse(lemma)
            ana_lemma = [x for x in anas_lemma
                         if x.tag.POS == ana_needed.POS or
                         (ana_needed.POS == 'VERB' and x.tag.POS == 'INFN')]
            if ana_lemma:
                new_word = ana_lemma[0].inflect(new_gr)
            iteration += 1
    if new_word is None:
        return word
    else:
        return new_word.word



def change_words(sentence):
    d = json.load(open('lemmas_POS.txt','r',encoding='utf-8-sig'))
    words = word_tokenize(sentence)
    result = []
    for word in words:
        digit =  re.search('[0-9]',word)
        if re.search('\\w',word) is not None and digit is None:
            result.append(' '+inflect_random(word,d))
        elif digit is not None:
            result.append(' '+word)
        else:
            result.append(word)
    return ''.join(result).strip()


