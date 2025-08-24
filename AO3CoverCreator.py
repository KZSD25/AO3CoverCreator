# -- Library Requirements --
# Pillow 11.3.0 - https://pypi.org/project/pillow/
# EbookLib 0.18 - https://pypi.org/project/EbookLib/
# ebookmeta 1.2.11 - https://pypi.org/project/ebookmeta/

# Python Standard Library
#from datetime import datetime
#from zipfile import ZipFile
#from bs4 import BeautifulSoup, Tag
#import shutil
#import re
#import io
#import uuid
#import json
import warnings
import os, os.path
import fnmatch
import sys

# Add libraries directory to module search path
parent_dir = os.path.abspath(os.path.dirname('AO3CoverCreator.py'))
lib_dir = os.path.join(parent_dir, 'libraries')
sys.path.append(lib_dir)

# in './libraries'
from ebooklib import epub

# in ./modules
#from modules.tag_library.tag_lists import LIST_COMPLETE, LIST_INCOMPLETE, LIST_RATING_E, LIST_RATING_G, LIST_RATING_M, LIST_RATING_T, LIST_REL_OTHER, LIST_WARNING_C, LIST_WARNING_W, LIST_WARNING_N

#functions
from modules.menu import startMenu, endMenu, errorMessage
from modules.cover_creation.cover import saveCover
from modules.file_analysis.fanficfare import metaFanFicFare
from modules.file_analysis.ao3 import metaAO3
from modules.file_analysis.ffn import metaFFN
from modules.file_analysis.other_publisher_last_try import metaOtherPublisher, metaLastTry

#---------------------------------------------------------------------------------------------

#variables
dir = './Books'
save = './Copies'
covers = './Covers'
error = './ErrorFiles'
error_list = []

#settings
darkMode = False
coverEpub = False
coverFolder = False
fileName = ""
consPrint = False
cvMethod = False

darkMode, coverEpub, coverFolder, fileName, consPrint, cvMethod = startMenu(dir)

totalFiles = len(fnmatch.filter(os.listdir(dir), '*.epub'))
currentFile = 0

#ebooklib's unnecessary warnings - comment out if bug fixes are necessary
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

#iterate through all EPUB files in ./Books
for filename in fnmatch.filter(os.listdir(dir), '*.epub'):
    currentFile += 1
    errMsg = ""

    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = ""

    #try reading file into ebooklib
    try :
        print ("Reading file " + str(currentFile) + " of " + str(totalFiles) + " . . .")
        book = epub.read_epub(dir + "/" + filename)

        if consPrint:
            print ("Checking identifier . . .")

        #find source with identifier
        try:
            
            #fanficfare
            if 'fanficfare' in book.get_metadata('DC', 'identifier')[0][0] :
                
                #get metadata
                source, relationship, warning, rating, complete, t, a, d = metaFanFicFare(book, consPrint)

                #create cover and save files
                saveCover(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder, cvMethod)
            
            #ffn
            elif 'fanfiction.net' in book.get_metadata('DC', 'identifier')[0][0].lower() :
                #get metadata
                source, relationship, warning, rating, complete, t, a, d = metaFFN(book, consPrint)

                #create cover and save files
                saveCover(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder, cvMethod)
            
            else:
                raise ValueError("No known identifier found")

        #find source with publisher
        except Exception as e:
            if consPrint :
                print(e)
                print("Checking publisher . . .")
                print ("Checking for AO3 tags . . .")

            try:
                #ao3
                if book.get_metadata('DC', 'publisher')[0][0] == 'Archive of Our Own' :
                    #get metadata
                    source, relationship, warning, rating, complete, t, a, d = metaAO3(book, consPrint)
                    
                    #create cover and save files
                    saveCover(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder, cvMethod)

                #non-AO3 publisher
                else:
                    if consPrint :
                        print("AO3 tags not found")

                    #Not AO3
                    try:
                        #get metadata
                        source, relationship, warning, rating, complete, t, a, d = metaOtherPublisher(book, consPrint)

                        #create cover and save files
                        saveCover(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder, cvMethod)

                    #meta error
                    except Exception as e:
                        errMsg = "File is not a recognized EPUB - check file's metadata"
                        error_list = errorMessage(e, errMsg, filename, error_list, dir, error)

            #no publisher, try to find any metadata
            except Exception as e:
                if consPrint :
                    print(e) #print error for testing
                    print("No publisher found")
                
                #last try to compose file
                try:
                    #get metadata
                    source, relationship, warning, rating, complete, t, a, d = metaLastTry(book, consPrint)

                    #create cover and save files
                    saveCover(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder, cvMethod)
                        
                #last error
                except Exception as e:
                    errMsg = "No metadata found"
                    error_list = errorMessage(e, errMsg, filename, error_list, dir, error)
    
    #file cannot be read
    except Exception as e:
        errMsg = "EPUB file could not be read"
        error_list = errorMessage(e, errMsg, filename, error_list, dir, error)

    print("\nFile Complete\n")

endMenu(error_list)

# TODO: Console progress bar:  "Reading / Editing / Saving EPUB 1 of 30 . . ." | "1 Book Completed" | "2 Books Completed" | . . .

# EPUB Notes : content.opf/book.opf/epb.opf
#<dc:title></dc:title> = fic title
#<dc:creator></dc:creator> = fic author
#<dc:date></dc:date> = fic date OR download date
#<dc:publisher></dc:publisher> = AO3, FFN, WTT
#<dc:identifier></dc:identifier> = can be many identifier elements; UUID, Calibre data, original URL
#     <dc:identifier opf:scheme="URL"> = original URL
#<dc:contributor></dc:contributor> = Calibre data
#<dc:source></dc:source> = original URL
#<dc:language></dc:language> = language of fic, lowercase abbreviation (English = en)
#<dc:description></dc:description> = fic description
#<dc:subject></dc:subject> can be many subject elements; tags