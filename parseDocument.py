#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Jose F. R. Fonseca
See Attached License file

######################################################
    THIS MODULE PARSES THE CONTENTS OF THE DATABASE FILE
######################################################
'''
import zlib
from HTMLParser import HTMLParser


'''
Constants
'''
# If the database must be decompressed before being read
COMPRESSED = False

# Used to identify a non-empty HTML TAG
CHARS = ["a", "b", "c", "d", "e",
         "f", "g", "h", "i", "j", "k",
         "l", "m", "n", "o", "p", "q",
         "r", "s", "t", "u", "v", "w",
         "x", "y", "z"]

# Used to normalize the contents of the files in Portuguese @IgnorePep8
DECODINGS = [("Ã ", "à", ),
             ("Ã¡", "á", ),
             ("Ã³", "ó", ),
             ("Ã§", "ç", ),
             ("Ã£", "ã", ),
             ("Ã¢", "â", ),
             ("Ãº", "ú", )]

# Symbols to be removed from the text string
STRIP_OUT = ["\t", ":", ";", ",", ".", "'",
             "$", "=", "+", "!", "?", "@",
             "#", "%", "&", "*", "-", "\n",
             "[", "]", "(", ")", "_", "\\",
             '''/''', '''{''', "}",
             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# list of HTML TAGs that do not contain useful data
TAGS_TO_IGNORE = ["script", "head"]


'''
Classes
'''


class MyHTMLParser(HTMLParser):
    '''
    Class that parses the HTML data provided
    The only method that should be called externally is "parseHTML"
    '''
    # Class Attributes
    keep = True  # if the data inside of a TAG should be stored
    inBody = False  # boolean if the data read is inside of the body of the document @IgnorePep8
    block = ""  # text of the HTML TAG to be blocked, w.a.
    parsedDat = []  # list of all the data parsed in the file

    def handle_starttag(self, tag, attrs):  # @UnusedVariable
        '''
        Handles the event of finding a new HTML TAG in the data provided
        Decides if the data in the found tag should be stored
        :param tag: the text of the TAG just found
        :param attrs: the attributes of the TAG just found
        '''
        if tag == "body":
            self.inBody = True
        if tag in TAGS_TO_IGNORE:
            self.keep = False
            self.block = tag
        else:
            self.keep = True

    def handle_endtag(self, tag):
        '''
        Decides if a tag data space ended
        :param tag: tag just read
        '''
        if tag in TAGS_TO_IGNORE and tag == self.block:
            self.keep = True
            self.block = ""

    def handle_data(self, data):
        '''
        handles the data inside a accepted TAG
        :param data: the data of the tag just read
        '''
        curOffset = self.getpos()
        # checks if the data is valid
        if self.keep and self.inBody\
                and data is not None\
                and any(chara in data for chara in CHARS):
            # remove invalid characters from the file
            for toRemove in STRIP_OUT:
                data = data.lower()
                data = data.replace(toRemove, " ")
                data = data.replace("  ", " ")
                data = data.strip(" ")
            # if there still are data left, stores it in the data list
            if data != "":
                self.parsedDat.append((data, curOffset[0], ))

    def parseHTML(self, htmlString):
        '''
        parses the content of the provided string
        :return a list of parsed lines of data from the file
        :param htmlString: string of HTML text to be parsed
        '''
        self.feed(htmlString)
        return self.parsedDat


'''
Methods
'''


def parseDOCfile(rawData):  # @UnusedVariable
    '''
    Stub to ignore a non-html file. Simply returns an empty list
    :return an empty list
    :param rawData: the raw data of the file to be parsed
    '''
    return []


def parseFile(fileObj, offset, fileEnd, isHTMLfile):
    '''
    Parses a file specified by the Offsets
        Opens and de-compresses the file from the database
        Decides if the file is HTML or DOC
    :return a list of lines of the file, lines that contains the parsed data
    :param fileObj: fileObject to the database file
    :param offset: start of the desired file
    :param fileEnd: end of the desired file
    '''
    # goes to the appropriate position in the database file,
    # and recovers the data of the file to be parsed, unzipping it
    fileObj.seek(offset)
    dat = fileObj.read(fileEnd-offset)
	# If the database file is flattened (compressed), decompresses it before
	# reading, and decode as latin-1 characters
	if COMPRESSED:
		rawData = zlib.decompress(dat).decode("latin-1")
	else:
    	rawData = dat.decode("latin-1")
    # If the recovered data is HTML, parses it as HTML. if not, pares as DOC
    # and returns the parsed results as a list
    if isHTMLfile:
        parser = MyHTMLParser()
        parser.parsedDat = []
        return parser.parseHTML(rawData)
    else:
        return parseDOCfile(rawData)


def getContentsOfFile(fileName, offset, fileEnd, isHTMLfile):
    '''
    Wrapper method for this script file.
    Receives the coordinates of a data file in the database,
    opens the database, extracts and parses the data, and
    :return a list of lines of parsed data
    :param fileName: name of the file in the database
    :param offset: position of begin of the currently parsed data
    :param fileEnd: position of ending of the parsed data
    :param isHTMLfile: boolean informing if the data to be parsed is HTML
    '''
    with open(fileName, 'rb') as dataFile:
        return parseFile(dataFile, offset, fileEnd, isHTMLfile)
