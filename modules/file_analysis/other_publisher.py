#OTHER PUBLISHER --------------------------------------------------------------------

import ebooklib
from ebooklib import epub

from ..cover_creation.text import HTMLCharacterSwap
from .meta import getSourcePublisher, userTagsComplete, getDate, getListComplete, getListRating, getListRelationship, getListWarning, getSource, getAO3Complete

#------------------------------------------------------------------------------------

def metaOtherPublisher(book, warning, relationship, rating, complete, source, consPrint) :
    # get book metadata
    a = book.get_metadata('DC', 'creator')[0][0]
    t = book.get_metadata('DC', 'title')[0][0]
    try:
        d = book.get_metadata('DC', 'date')[0][0]
        d = d.replace("/", "-")
    except:
        d = ''

    t = HTMLCharacterSwap(t)
    if "T" in d:
        d = d.split('T', 1)[0]

    print ("File: " + a + " - " + t)

    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = ""

    #source
    source = getSourcePublisher(book)

    # get tag information
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:

            # print(item.get_name()) #page filename
            # print(item.get_content()) #all content of file

            pageData = item.get_content() #usually in bytes
            try :
                pageData = pageData.decode("utf-8") #convert byte to string
            except Exception as e:
                if consPrint :
                    print(e)

            #get date
            d = getDate(pageData, d)

            #source
            source = getSource(pageData, source)

            #warning
            warning = getListWarning(pageData, warning, source)

            #relationship
            relationship = getListRelationship(pageData, relationship)
            
            #rating
            rating = getListRating(pageData, rating)

            #complete
            complete = getListComplete(pageData, complete)
            if complete == '' :
                complete = getAO3Complete(pageData)
    
    #complete (user-added tags)
    if complete == "" :
        try:
            complete = userTagsComplete(book)
        except Exception  as e:
            if consPrint :
                print(e)
        
    return (source, relationship, warning, rating, complete, t, a, d)