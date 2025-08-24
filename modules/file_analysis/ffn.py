#FANFICION DOT NET ------------------------------------------------------------------

import ebooklib
from ebooklib import epub

from ..tag_library.tag_lists import LIST_REL_OTHER

from ..cover_creation.text import compareDates
from .meta import userTagsComplete, getDate, getListComplete, getListRating, getListRelationship
from .other_publisher_last_try import getMainMetadata

#------------------------------------------------------------------------------------

def metaFFN(book, consPrint) :
    if consPrint :
        print("FFN data found")

    #vars
    warning = "C"
    relationship = []
    rating = ""
    complete = ""
    source = "FFN"
    d = ""
    #date holders for comparison
    d1, d2 = '', '' #<dc:date>, update

    #get title, author, <dc:date>
    t, a, d1 = getMainMetadata(book)

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

            #get dates
            if d2 == '' :
                d2 = getDate(pageData, d2) #most recent update/complete

            #source
            #source = "FFN"

            #warning
            #warning = "C"

            #relationship
            relationship = getListRelationship(pageData, relationship)

            #rating
            if rating == '' :
                rating = getListRating(pageData, rating)

            #complete
            if complete == '' :
                complete = getListComplete(pageData, complete)

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