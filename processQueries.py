#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Jose F. R. Fonseca
See Attached License file
'''
import sys
import ast
import unicodedata
import string
from linecache import getline

'''
SETTINGS
'''
# name of the inverted index to be consulted, and optionally its relative,
# unix-style location
GENERATED_INVERTED_INDEX = "invertedIndex.dat"

# list of string common terms not to be indexed - stopwords
STOPWORDS = [
             # Arquivo de Stopwords extraido de https://gist.github.com/alopes/5358189 @IgnorePep8
             'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um',
             'para', 'e', 'com', 'nao', 'uma', 'os', 'no',
             'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi',
             'ao', 'ele', 'das', 'tem', 'a', 'se', 'sua', 'o',
             'ser', 'quando', 'muito', 'ha', 'nos', 'ja',
             'esta', 'e', 'tambem', 'so', 'pelo',
             'pela', 'ate', 'isso', 'ela', 'entre', 'era', 'depois',
             'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me',
             'esse', 'eles', 'estao', 'voce', 'tinha', 'foram',
             'essa', 'num', 'nem', 'suas', 'me', 'as', 'minha',
             'tem', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual',
             'sera', 'nos', 'tenho', 'lhe', 'deles', 'essas',
             'esses', 'pelas', 'este', 'fosse', 'dele', 't', 'te',
             'voces', 'vos', 'lhes', 'meus', 'minhas', 'te',
             'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas',
             'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela',
             'aqueles', 'aquelas', 'isto', 'aquilo', 'esto', 'esta',
             'estamos', 'estao', 'estive', 'esteve', 'estivemos',
             'estiveram', 'estava', 'estavamos', 'estavam', 'estivera',
             'estiveramos', 'esteja', 'estejamos', 'estejam', 'estivesse',
             'estivessemos', 'estivessem', 'estiver', 'estivermos',
             'estiverem', 'hei', 'ha', 'havemos', 'hao', 'houve',
             'houvemos', 'houveram', 'houvera', 'houveramos', 'haja',
             'hajamos', 'hajam', 'houvesse', 'houvessemos',
             'houvessem', 'houver', 'houvermos', 'houverem', 'houverei',
             'houvera', 'houveremos', 'houverao', 'houveria',
             'houveríamos', 'houveriam', 'so', 'somos',
             'sao', 'era', 'eramos', 'eram', 'fui', 'foi',
             'fomos', 'foram', 'fora', 'foramos', 'seja', 'sejamos',
             'sejam', 'fosse', 'fossemos', 'fossem', 'for', 'formos',
             'forem', 'serei', 'sera', 'seremos', 'serao',
             'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos',
             'tem', 'tinha', 'tínhamos', 'tinham', 'tive',
             'teve', 'tivemos', 'tiveram', 'tivera', 'tiveramos',
             'tenha', 'tenhamos', 'tenham', 'tivesse', 'tivessemos',
             'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'tera',
             'teremos', 'terao', 'teria', 'teríamos', 'teriam',
             # Stopwords extraidas de http://www.ranks.nl/stopwords
             'about', 'above', 'after', 'again', 'against', 'all',
             'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be',
             'because', 'been', 'before', 'being', 'below', 'between',
             'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't",
             'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
             'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had',
             "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
             'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers',
             'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd",
             "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it',
             "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't",
             'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
             'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves',
             'out', 'over', 'own', 'same', "shan't", 'she', "she'd",
             "she'll", "she's", 'should', "shouldn't", 'so', 'some',
             'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
             'them', 'themselves', 'then', 'there', "there's", 'these',
             'they', "they'd", "they'll", "they're", "they've", 'this',
             'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
             'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've",
             'were', "weren't", 'what', "what's", 'when', "when's",
             'where', "where's", 'which', 'while', 'who', "who's",
             'whom', 'why', "why's", 'with', "won't", 'would',
             "wouldn't", 'yo', "yo'd", "yo'll", "yo're", "yo've",
             'your', 'yours', 'yourself', 'yourselves']


'''
METHODS ###################################################
'''


def remove_accents(data):
    '''
    Removes special characters and accents of the provided string, by
    replacing them using the scheme NFKD. Puts all the words in lower case.
    Reads the input string as utf-8
    :return cleaned string
    :param data: string to be cleaned
    '''
    return ''.join(x for x in unicodedata.normalize('NFKD', data.decode('utf-8')) if x in string.ascii_letters).lower()  # @IgnorePep8


def getDataOfWord(hashWord):
    '''
    recovers the iverted index of the hash term provided, as a inverted list
    :return a list, inverted list in the index for the searched term.
    :param hashWord: string, hash of the word to be recovered
    '''
    return ast.literal_eval(getline(GENERATED_INVERTED_INDEX, int(hashWord)+1).split(":::")[1])  # @IgnorePep8


if __name__ == '__main__':
    # OnMemoryIndex: WORD: HashWord
    # reads the on memory index disk dump provided by the indexer, as a
    # dictionary to translate words into index file positions
    with open("metaIndex-"+GENERATED_INVERTED_INDEX, "r") as metaindex:  # @IgnorePep8
        data = metaindex.read()
        onMemoryIndex = ast.literal_eval(data)

    # reads the on memory index disk dump provided by the indexer, as a
    # dictionary to translate names of files into hashes
    with open("namesDict-"+GENERATED_INVERTED_INDEX, "r") as namesDict:  # @IgnorePep8
        data = namesDict.read()
        namesDictionary = ast.literal_eval(data)

    # reverses the file names dictionary, to map a hash to a file name
    reverseNamesDict = {}
    for name in namesDictionary.keys():
        reverseNamesDict[namesDictionary[name]] = name

    # reads the query as a list of the command-line strings, excluding
    # the name of the program
    query = sys.argv[1:]
    # normalizes the query terms, removes stopwords and single-character
    # words, and getting it to lower case. The normalized resutls are in a
    # ordered list of strings
    query = [str(remove_accents(wrd)) for wrd in query
             if wrd not in STOPWORDS
             and len(wrd) > 1]
    # buffer stores the temporary query results
    results = []
    connect = "or"
    # print "Performing query "+str(query)
    # for each term in the query list of terms, read two by two,
    for queryTermInd in range(0, len(query), 2):
        try:
            # recovers the inverted index of the term in the query
            firstArgLine = getDataOfWord(onMemoryIndex[query[queryTermInd]])
        except KeyError:
            # if the term is not in the index, then it is considered a term of no results! @IgnorePep8
            print "term not in index! :::"+str(query[queryTermInd])
            firstArgLine = []
            pass
        # translates the hashes of the files recovered by the query to file names @IgnorePep8
        localResults = [reverseNamesDict[docTouple[0]] for docTouple in firstArgLine]  # @IgnorePep8
        # if the query contains an OR or AND, merges or ANDs the results
        # up to this moment with the results of the current term
        if connect == "or":
            results = list(set(results + localResults))
        if connect == "and":
            results = list(set(results).intersection(localResults))
        # reads the connection term (AND or OR) next to the current term in the
        # query. That is wy we need a zero-connector, an OR, before starting
        if queryTermInd < len(query)-1:
            connect = query[queryTermInd+1]
    # prints all the results
    for res in results:
        print res
