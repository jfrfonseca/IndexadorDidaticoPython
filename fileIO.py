#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
José F. R. Fonseca
See Attached License file

Controls the access to the disk. Defines the class DIskAccessControl,
an object to control the disk files. Multithread-writes the files
'''

import ast
import os
import time
from linecache import getline
from threading import Thread

'''
ONLY WRITES TO THE FILE WHEN THE CACHE OF LINES TO WRITE OVERCOMES
THIS MUCH BYTES, or if it is the last batch of files to be written.
'''
FILEACCESS_THRASHOLD = 1024*1024/32

'''
CLASSES
'''
class DiskAccessControl():  # @IgnorePep8
    '''
    Control the access to the disk, being the middleware to read and write the
    index files
    '''
    def __init__(self, invertedIndexFileName, fileLen=None,
                 onMemInd=None, nameDict=None, mods=None):
        '''
        Instantiates the class as the only reference to the index files
        :param invertedIndexFileName: string, name of the index file
        :param fileLen: int, original number of lines of the index file, when
        known
        :param onMemInd: dictionary, on-memory index that translates terms
        into file positions
        :param nameDict: dictionary, on-memory index that translates the name
        of each file indexed into a hash
        into a hash
        :param mods: dictionary, side-loaded modifications to be put into the
        index manually.
        '''
        # loads the name of the index file
        self.GENERATED_INVERTED_INDEX = invertedIndexFileName

        # if there is a parameter fileLen, uses it. if not, counts the number
        # of lines in the indexFile
        if fileLen is None:
            # print "GETTING THE FILE # OF LINES!"
            lineNum = 0
            # reads every line, and counts the number of lines in the index file @IgnorePep8
            with open(self.GENERATED_INVERTED_INDEX, "r") as indFile:
                for lineNum, dummy in enumerate(indFile):
                    pass
                self.fileLength = lineNum + 1
        else:
            self.fileLength = fileLen

        # if there is a parameter onMemInd, uses it. if not, loads it from the
        # memory dump file metaindex
        if onMemInd is None:
            print "FILLING MEMORY INDEX WITH LAST SESSION'S!"
            # OnMemoryIndex: dictionary that maps WORD to HashWord
            # Loads the metaindex file into main memory, into onMemoryIndex attribute @IgnorePep8
            with open("metaIndex-"+self.GENERATED_INVERTED_INDEX, "r") as metaindex:  # @IgnorePep8
                data = metaindex.read()
                self.onMemoryIndex = ast.literal_eval(data)
        else:
            self.onMemoryIndex = onMemInd

        # if there is a parameter namesDict, uses it. if not, loads it from the
        # memory dump file namesDict, mapping a file name to its hash
        if nameDict is None:
            print "FILLING NAMES DICTIONARY WITH LAST SESSION'S!"
            # Loads the namesDict file into main memory, into namesDict attribute @IgnorePep8
            with open("namesDict-"+self.GENERATED_INVERTED_INDEX, "r") as namesDict:  # @IgnorePep8
                data = namesDict.read()
                self.namesDictionary = ast.literal_eval(data)
        else:
            self.namesDictionary = nameDict

        # if there is a parameter mods, uses it. if not, creates a new empty
        # python dictionary to retain on-memory changes to the index
        if mods is None:
            self.modifications = {}
        else:
            self.modifications = mods

    '''
    METHODS ###############################################
    '''

    def getIndexLine(self, word):
        '''
        GETS a line of the index file, containing the inverted list of the word
        provided. If inexistent, returns an empty list
        :return a list containing the index data of the word requested.
        It may be: the inverted list on the index, the modifications done
        to such list in memory, or an empty list for a new term to be indexed
        :param word: string to retrieve the index data of it, a term
        '''
        # if the word is on the onMemoryIndex, and thereby on the file index,
        if word in self.onMemoryIndex.keys():
            # retrieves the hash of the word in wrd
            wrd = self.onMemoryIndex[word]
            # if that word has already been modified, its modifications will be
            # on main memory, and do not need to be retrieved from the disk.
            if wrd not in self.modifications.keys():
                try:
                    # retrieves a list of the data in the line of the index
                    # file on disk that contains the inverted index of the
                    # word, given its hash. The value of wrd must be
                    # summed with 1 because there is no line 0 on files
                    return ast.literal_eval(getline(self.GENERATED_INVERTED_INDEX, int(wrd)+1).split(":::")[1])  # @IgnorePep8
                # prints-out eventual exceptions, as the hash searched in
                # the index file, and the data recovered from it, as a string
                # separated by "(|||)" rather than spaces
                except:
                    print wrd, "(|||)", getline(self.GENERATED_INVERTED_INDEX, int(wrd)+1)  # @IgnorePep8
            else:
                # returns the modifications to the index line, already on memory @IgnorePep8
                return self.modifications[wrd]
        # if the word searched is not in the index,
        else:
            # opens the index file, generates a new hash for the word to be
            # indexed, and writes an empty list to the index file at the
            # words's future position. Returns an empty list
            with open(self.GENERATED_INVERTED_INDEX, "a") as indFile:
                self.onMemoryIndex[word] = str(len(self.onMemoryIndex.keys()))  # @IgnorePep8
                indFile.write(self.onMemoryIndex[word]+":::"+"[]"+"\n")
            self.fileLength += 1
            return []

    def pushIntoIndexFile(self, fileIndexedName, word, wordIndexTouple):
        '''
        Pushes the preshly produced inverted list of a term into the index
        :param fileIndexedName: string, name of the file just indexed
        :param word: string, term to be pushed into the index
        :param wordIndexTouple: touple, containing the number of elements
        in the positions list, and a (integer) positions list of occurences of
        the term in the file indexed
        '''
        # gets the line of the index for the term pushed
        indexLine = self.getIndexLine(word)
        # if the file pushed has already been indexed before, recovers its
        # hash name
        if fileIndexedName in self.namesDictionary.keys():
            hashName = self.namesDictionary[fileIndexedName]
        # if not, creates a new hash for the file name, as a number
        else:
            self.namesDictionary[fileIndexedName] = hashName = str(len(self.namesDictionary.keys()))  # @IgnorePep8
        try:
            # includes the index of the new file pushed into the respective
            # line in the on memory inverted list of the term, avoiding
            # repetitions. Includes the name of the file, the number of
            # occurences and the positions the term indexed happens to occur.
            indexLine.append((hashName, wordIndexTouple[0], (list(set(wordIndexTouple[1]))), ))  # @IgnorePep8
            # includes the freshly produced new index for the term in the
            # on- memory modifications to be written on disk
            self.modifications[self.onMemoryIndex[word]] = indexLine
        # reveals an I/O error. bureaucracy
        except IndexError:
            print "Got an IndexError!"+str((word, self.onMemoryIndex[word], indexLine, ))  # @IgnorePep8

    def merge(self, outerModifications):
        '''
        Pushes provided modifications (made by another thread, for example,
        into this instance's modifications list
        :param outerModifications: dictionary, mapping terms to inverted lists,
        are modifications to the index file imported from another instance
        '''
        # for each key of the outer modifications dictionary,
        for outKey in outerModifications.keys():
            if outKey in self.modifications.keys():
                # if the key is on the current modifications list, joins the
                # contents of both lists, and sorts by the hash of the terms
                self.modifications[outKey].extend(outerModifications[outKey])
                self.modifications[outKey] = sorted(self.modifications[outKey],
                                                    key=lambda mod: int(mod[0]))  # @IgnorePep8
            # if the outer key is not on the current modifications list,
            # adds to it
            else:
                self.modifications[outKey] = outerModifications[outKey]

    def dumpMetafiles(self):
        '''
        Dumps the on-memory metafiles, the dictionaries mapping terms to file
        positions (hashes) and file names to hashes, to disk files.
        '''
        with open("metaIndex-"+self.GENERATED_INVERTED_INDEX, "w") as metaindex:  # @IgnorePep8
            metaindex.write(str(self.onMemoryIndex))
        with open("namesDict-"+self.GENERATED_INVERTED_INDEX, "w") as namesDict:  # @IgnorePep8
            namesDict.write(str(self.namesDictionary))

    def dumpMemory(self):
        '''
        Dumps the metafiles and writes the modifications to the index. It is,
        by far, the most time-costly operation on the entire program, what was
        to be expected, since it involves heavy file writting and reading.
        '''
        # Creates a new thread to write the metafiles concurrently
        metafileWriter = Thread(target=self.dumpMetafiles)
        metafileWriter.start()
        # string writting buffer, to be written on the file
        printString = ""
        # for each modification on memory, got in order, writes on the string
        # buffer, and when it gets full, writes to a temporary disk file the
        # results of merging the modification on each line of the index,
        # and the unmodified lines, ordered by the hashes of the terms
        modKeys = sorted([k for k in self.modifications.keys()])
        with open(self.GENERATED_INVERTED_INDEX, "r") as oldIndexFile:  # @IgnorePep8
            with open("TEMP_"+self.GENERATED_INVERTED_INDEX, "w+") as newIndexFile:  # @IgnorePep8
                for line in oldIndexFile:
                    # reads the data in the old index file line
                    lineNum = line.split(":::")[0]
                    # if the modifications line is to be written in the string
                    # writing buffer, because the read line was modified
                    if lineNum in modKeys:  # @IgnorePep8
                        printString += lineNum+":::"+str(self.modifications[lineNum])+"\n"  # @IgnorePep8
                    else:
                        # if the original index line is to be written on the
                        # file writing buffer, saves it
                        printString += line
                    # if the buffer is full to the threshold, writes it to
                    # the disk file
                    if len(printString) >= FILEACCESS_THRASHOLD:
                        newIndexFile.write(printString)
                        printString = ""
        # renames the old inverted Index to become a backup
        os.rename(self.GENERATED_INVERTED_INDEX, "Backup_"+str(time.time())+"_"+self.GENERATED_INVERTED_INDEX)  # @IgnorePep8
        # rename the new to replace the old one
        os.rename("TEMP_"+self.GENERATED_INVERTED_INDEX, self.GENERATED_INVERTED_INDEX)  # @IgnorePep8
        # assures that the metafile writer thread is done writing
        metafileWriter.join()
