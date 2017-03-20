import unittest
import string

class KwiqTester(unittest.TestCase):
    def test_find_one(self):
        self.assertEqual(kwiq('suppose','Word is something about word, I suppose it is word'),
                         [['about word, I', 'suppose', 'it is word']])
        self.assertEqual(kwiq('suppose','Word is something about word, I suppose it is word',num=2),
                         [['word, I', 'suppose', 'it is']])
    def test_find_several(self):
        self.assertEqual(kwiq('word','Word is something about word, I suppose it is word'),
                         [['', 'Word', 'is something about'], ['is something about', 'word,', 'I suppose it'],
                          ['suppose it is', 'word', '']])
    def test_find_none(self):
        self.assertEqual(kwiq('dog','Word is something about word, I suppose it is word'),[])
                         

def kwiq(word,text,num=3):
    """
    extract words with contexts.
    
    Args:
        word: word to search for
        text: where to search the word
        num: number of words in context (3 by default)

    Returns:
       a list of lists: [[left context, word, right context], ...]
    """
    contexts = []
    text_list = text.split()
    for i,w in enumerate(text_list):
        new = w.strip(string.punctuation).lower()
        if new == word:
            contexts.append([' '.join(text_list[i-num:i]),w,
                             ' '.join(text_list[i+1:i+num+1])])
    return contexts

def to_table(table):
    """
    turn table of words with contexts into the string in kwic format.

    Args:
       table: a list of lists: [[left context, word, right context], ...]

    Returns:
        res: a string representation with necessary spaces and ends of line
    """
    if not table:
        return ''
    maxlen = max([len(row[0]) for row in table])
    lenw = max([len(row[1]) for row in table])
    res = ''
    for row in table:
        res += row[0] + ' '*(maxlen-len(row[0])+3) +\
               row[1] + ' '*(lenw-len(row[1])+3) + row[2] + '\n'
    return res


print(to_table(kwiq('word','Word is something about word, I suppose it is word',num=4)))
unittest.main()
