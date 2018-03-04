import os
import math
import matplotlib.pyplot as plt

#tokenizes every file in the directory
#puts all the tokens in the dict_of_word
#counts number of all words(not size of dictionary)
def tokenize(path, dict_of_word2, min_word = 0) :
    lfiles = os.listdir(path)
    dict = {}
    dict_of_word = {}
    count = 0
    for file in lfiles:
        if file[0] == '.':
            continue
        fd = open(path + file, 'r')
        dict[count] = fd.read()
        dict[count] = dict[count].replace("<br />", " ")
        dict[count] = dict[count].split()
        for elem in dict[count]:
            elem = ''.join(char_ for char_ in elem if char_.isalpha())  # é
            elem = elem.lower()
            if elem in dict_of_word.keys():
                dict_of_word[elem] += 1
            else:
                dict_of_word[elem] = 1
        count += 1
        fd.close()

    count = 0
    for elem in dict_of_word:
        count += dict_of_word[elem]
        if (dict_of_word[elem] > min_word):
            dict_of_word2[elem] = dict_of_word[elem]

    dict_of_word.clear()
    return count
    #for elem in dict_of_word2:
    #    print(elem, dict_of_word2[elem])


def test(path, vec_b, vec_g, size_neg, size_pos, dict_s):
    lfiles = os.listdir(path)
    good = 0
    bad = 0
    for file in lfiles:
        if file[0] == '.':
            continue
        p1 = 0
        p2 = 0
        f = open(path + file);
        for elem in f.read().split():
            elem = ''.join(char_ for char_ in elem if char_.isalpha())  # é
            elem = elem.lower()
            if elem in vec_b.keys():
                p1 += math.log(vec_b[elem])
            else:
                p1 += math.log(1 / (size_neg + dict_s))
            if elem in vec_g.keys():
                p2 += math.log(vec_g[elem])
            else:
                p2 += math.log(1 / (size_pos + dict_s))
        f.close()
        if p1 > p2:
            bad += 1
        else:
            good += 1
    return good, bad


OX = [i for i in range(0, 200, 5)]
OY = []
for i in range(0, 200, 5):
    print('i = ', i)
    dict_of_word_bad = {}
    dict_of_word_good = {}
    size_neg = tokenize("/Users/kononykhindanil/Downloads/aclImdb/train/neg/", dict_of_word_bad, i)
    size_pos = tokenize("/Users/kononykhindanil/Downloads/aclImdb/train/pos/", dict_of_word_good, i)

    print (dict_of_word_bad.__len__(), dict_of_word_good.__len__())
    #for elem in dict_of_word_bad:
    #    print (dict_of_word_bad[elem], elem)
    #print("\n\n\n\n")
    #for elem in dict_of_word_good:
    #    print (dict_of_word_good[elem], elem)

    dict_of_word = {}
    c = 0
    for elem1 in dict_of_word_bad:
        c += 1
        dict_of_word[elem1] = dict_of_word_bad[elem1]

    for elem in dict_of_word_good:
        if elem in dict_of_word.keys():
            dict_of_word[elem] += dict_of_word_good[elem]
        else:
            c += 1
            dict_of_word[elem] = dict_of_word_good[elem]

    print(size_neg, size_pos, c)
    vec_bad = {}
    for elem in dict_of_word_bad:
        vec_bad[elem] = dict_of_word_bad[elem] / size_neg

    vec_good = {}
    for elem in dict_of_word_good:
        vec_good[elem] = dict_of_word_good[elem] / size_pos

    path = "/Users/kononykhindanil/Downloads/aclImdb/train/pos/"
    (x, y) = test(path, vec_bad, vec_good, size_neg, size_pos, c)
    s = x
    print(x, y)
    path = "/Users/kononykhindanil/Downloads/aclImdb/train/neg/"
    (z, d) = test(path, vec_bad, vec_good, size_neg, size_pos, c)
    s += d
    print(z, d)
    print(s / 25000)
    OY.append(s/25000)

plt.scatter(OX, OY)
plt.show()