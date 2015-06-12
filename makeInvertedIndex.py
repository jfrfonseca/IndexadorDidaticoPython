#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Jose F. R. Fonseca
See Attached License file
'''
from parseDocument import getContentsOfFile
import unicodedata
import string
from fileIO import DiskAccessControl

'''
SETTINGS
'''
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
CONSTANTS
'''
# file number to begin reading the database file from, integer
FILE_OFFSET = 0
# max number of files to be read and indexed, integer
FILE_LIMIT = 1000000000
# name of the uncompressed database file to be read, string
DATABASE_ITEM = "pagesRICompressed0"
# relative, unix-style location of the database file to be read and indexed,
# as a string
DATABASE_FILE = "corpusExample/"+DATABASE_ITEM
# relative, unix-style location of the index of the database file to be read
# and indexed, as a string. THe index file must be formatted as the index to
# the WT10g database
DATABASE_INDEX_FILE = "corpusExample/indexToCompressedColection.txt"
# name of the inverted index file to be generated, and optionally its relative,
# unix-style location
GENERATED_INVERTED_INDEX = "invertedIndex.dat"


'''
METHODS ###################################################
'''


def remove_accents(data):
    '''
    Removes special characters and accents of the provided string, by
    replacing them using the scheme NFKD. Puts all the words in lower case.
    :return cleaned string
    :param data: string to be cleaned
    '''
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()  # @IgnorePep8


def indexTheFile(fileTouple):
    '''
    Indexes a single file, given the file touple. Surprisingly cost-efficient
    :return a touple containing the name of the file, and a dictionary
    mapping each term in the file to the positions of its occurrences.
    :param fileTouple: a touple that contains the name of the file to be read,
    the position it begins on the database file, and the position it ends. It
    also includes a boolean saying if the file is HTML
    '''
    # dictionary that will map each term in the file to the number and
    # positions it occurs on the file
    invertedIndexOfFile = {}
    # reads the database file, and returns its contents as a list of touples
    # relating a string to a position in the file just read
    data = getContentsOfFile(DATABASE_FILE, fileTouple[1], fileTouple[2], fileTouple[3]) # @IgnorePep8
    # for each touple returned
    for dat in data:
        # separates the string of the touple into a list of words, cleaned of special characters @IgnorePep8
        wordsInLine = [str(remove_accents(wrd)) for wrd in dat[0].split(" ")] # @IgnorePep8
        # removes the monosillabic words and stopwords from the list
        wordsList = [str(wrd) for wrd in wordsInLine
                     if wrd not in STOPWORDS
                     and len(wrd) > 1]
        # for each remaining word in the words list
        for word in wordsList:
            # if the word - term - is already on the index of the current file
            if word in invertedIndexOfFile.keys():
                # retrieves the existing indexed data of the term
                newList = invertedIndexOfFile[word][1]
                # appends the freshly produced lsit of positions to the
                # retrieved data
                newList.append(dat[1])
                # saves the number of times a word occurs in the file and its
                # positions to the recently produced index
                invertedIndexOfFile[word] = invertedIndexOfFile[word][0] + 1, newList  # @IgnorePep8
            # if the term is not on the index, adds a new key, being it the
            # term, and the list of occurences
            else:
                invertedIndexOfFile[word] = 1, [dat[1]]
    return (fileTouple[0], invertedIndexOfFile, )


'''
RUNTIME ###################################################
'''


if __name__ == '__main__':
    # list of files to be indexed
    files2index = []
    print "Indexer Starting"
    # object that controls disk access to the index file
    storage = DiskAccessControl(GENERATED_INVERTED_INDEX)

    print "Gathering files still to index"
    # opens the database index file, and reads each line of it, counting
    # the number of lines
    with open(DATABASE_INDEX_FILE, "r") as indexFile:
        for currentFileNum, fileLine in enumerate(indexFile.read().splitlines()):  # @IgnorePep8
            # if the current line is inside the window determined in the
            # settings session of this file,
            if currentFileNum >= FILE_OFFSET and currentFileNum < FILE_LIMIT:
                line = fileLine.split(" ")
                # if the line relates to the file specified by the settings
                # session of this document,
                if line[1] == DATABASE_ITEM:
                    # determines if a file is not HTML/PHP by removing files
                    # with other extensions
                    isHTML = all([ext not in str(line[0]) for ext in [".doc", ".sfw"]])  # @IgnorePep8
                    # appens in the list of files to be indexed the description
                    # of the file just analized
                    files2index.append((line[0], int(line[2]), int(line[3]), isHTML, ))  # @IgnorePep8
    # This part of the code performs the indexing of the given files
    # in the touple list files2index
    print "Done gathering "+str(len(files2index))+" files to index. Start file indexing"  # @IgnorePep8
    # for each file in the list of files to be indexed, calls the function
    # that indexes the file, and saves the indexes into a list of dictionaries,
    # named "many indexed". This short line does the hard work of the program,
    # explores parallelism in a Parallel cPython-enabled system, and is NOT the
    # most time-consuming operation of the program, iven in sequential mode
    # doSomethingComplicated()  # 1 line.  #Explain It: 5 full lines. Python Rocks! @IgnorePep8
    manyIndexed = [indexTheFile(fileTouple) for fileTouple in files2index]
    print "Files indexed. Now, merging the indexes generated"
    # for each file indexed, retrieves its name and index of terms
    for indexTouple in manyIndexed:
        fileName = indexTouple[0]
        invertedIndexOfFile = indexTouple[1]
        # gets a sorted list that has the terms in the file as hash strings
        wordKeys = sorted(invertedIndexOfFile.keys())
        # for each term in the file
        for word in wordKeys:
            # pushes the new occurences oif each term into the index file on
            # disk. This is, BY FAR, the most time-consuming operation in this
            # system. And it is called O(100*(1.25*900*N_DOCUMENTS)^0.7) times
            # per execution of the program, being 900 a rough estimate of the
            # number of words in each document, and the overall formula the
            # worst case scenario of the Heap's Law of new terms, considering
            # that each document will overwrite 25% of the terms in the index
            storage.pushIntoIndexFile(fileName, word, invertedIndexOfFile[word])  # @IgnorePep8

    print "------Final Dumping of Memory"
    # dumps the memory back to disk, saving the index file and the metaindexes.
    # fairly costly operation, but not as much as the push into the index.
    storage.dumpMemory()
    print "ALL DONE!"
