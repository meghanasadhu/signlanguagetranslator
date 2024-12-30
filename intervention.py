import os
import difflib
from nltk.corpus import wordnet

def datalist():
    mylist = os.listdir(os.getcwd() + '/static/text_to_sign_videos')
    ls = []
    for x in mylist:
        ls.append(os.path.splitext(x)[0])
    return ls


def similarWords(word):
    max_similarity = 0
    ls = datalist()
    print(ls)
    #ls.remove('cartoonize')
    return difflib.get_close_matches(word, ls)
