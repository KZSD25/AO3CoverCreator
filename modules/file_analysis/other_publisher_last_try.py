#OTHER PUBLISHER --------------------------------------------------------------------

import ebooklib
from ebooklib import epub

from ..cover_creation.text import HTMLCharacterSwap, compareDates
from .meta import getSourcePublisher, userTagsComplete, getDate, getListComplete, getListRating, getListRelationship, getListWarning, getSource, getAO3Complete

#------------------------------------------------------------------------------------

#Other Publisher
def metaOtherPublisher(book, consPrint) :
    #vars
    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = ""
    d = ""
    #date holders for comparison
    d1, d2 = '', '' #<dc:date>, update

    #get title, author, <dc:date>
    t, a, d1 = getMainMetadata(book)

    #source
    source = getSourcePublisher(book)

    # get tag information
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            
            #get metadata from item > pageData
            d2, source, warning, relationship, rating, complete = getMetaFromPageData(item, d2, source, warning, relationship, rating, complete, consPrint)
    
    #complete (user-added tags)
    if complete == "" :
        try:
            complete = userTagsComplete(book)
        except Exception  as e:
            if consPrint :
                print(e)
    
    #get dates
    d = compareDates(d1, d2)

    return (source, relationship, warning, rating, complete, t, a, d)

#Last Try
def metaLastTry(book, consPrint) :
    #vars
    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = ""
    d = ""
    #date holders for comparison
    d1, d2 = '', '' #<dc:date>, update

    #get title, author, <dc:date>
    t, a, d1 = getMainMetadata(book)

    # get tag information
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            
            #get metadata from item > pageData
            d2, source, warning, relationship, rating, complete = getMetaFromPageData(item, d2, source, warning, relationship, rating, complete, consPrint)

    #complete (user-added tags)
    if complete == "" :
        try:
            complete = userTagsComplete(book)
        except Exception  as e:
            if consPrint :
                print(e)

    #get dates
    d = compareDates(d1, d2)

    return (source, relationship, warning, rating, complete, t, a, d)

# ------------------------------------------------------------------------------------

#get author, title, and u<dc:date>
def getMainMetadata(book) :
    # get book metadata
    a = book.get_metadata('DC', 'creator')[0][0] #author
    t = book.get_metadata('DC', 'title')[0][0] #title
    
    t = HTMLCharacterSwap(t)

    #get d1
    try :
        d1 = book.get_metadata('DC', 'date')[0][0]
        d1 = d1.replace("/", "-")
        if "T" in d1:
            d1 = d1.split('T', 1)[0]
    except :
        d1 = ''
    
    print ("File: " + a + " - " + t)

    return t, a, d1

#get metadata from page contents
def getMetaFromPageData(item, d2, source, warning, relationship, rating, complete, consPrint) :
    # introduction.xhtml or cover.xtml or title.xtml == item.get_name().lower()
    # print(item.get_name()) #page filename
    # print(item.get_content()) #all content of file

    pageData = item.get_content() #usually in bytes
    try :
        pageData = pageData.decode("utf-8") #convert byte to string
    except Exception as e:
        if consPrint :
            print(e)

    #get dates
    if d2 == '' :
        d2 = getDate(pageData, d2) #most recent update/complete

    #source
    if source == '' :
        source = getSource(pageData, source)

    #warning
    if warning == '' :
        warning = getListWarning(pageData, warning, source)

    #relationship
    relationship = getListRelationship(pageData, relationship)
    
    #rating
    if rating == '' :
        rating = getListRating(pageData, rating)

    #complete
    if complete == '' :
        complete = getListComplete(pageData, complete)
    if complete == '' :
        complete = getAO3Complete(pageData)

    return d2, source, warning, relationship, rating, complete