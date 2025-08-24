#ARCHIVE OF OUR OWN ----------------------------------------------------------------

import ebooklib
from ebooklib import epub

from ..cover_creation.text import compareDates
from .meta import getAO3Complete, getAO3Rating, getAO3Relationship, getAO3Warning, getDate
from .other_publisher_last_try import getMainMetadata

#------------------------------------------------------------------------------------

def metaAO3(book, consPrint) :
    if consPrint :
        print ("AO3 tags found")

    #vars
    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = "AO3"
    d = ""
    #date holders for comparison
    d1, d2 = '', '' #<dc:date>, update

    t, a, d1 = getMainMetadata(book)

    # get tag information
    for item in book.get_items():
            
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # print(item.get_name()) #page filename
                # print(item.get_content()) #all content of file

                pageData = item.get_content() #in bytes
                pageData = pageData.decode("utf-8") #convert byte to string

                #get dates
                if d2 == '' :
                    d2 = getDate(pageData, d2) #most recent update/complete

                #warning
                if warning == '' :
                    warning = getAO3Warning(pageData, warning)

                #relationship
                relationship = getAO3Relationship(pageData, relationship)
                
                #rating
                if rating == '' :
                    rating = getAO3Rating(pageData, rating)
                
                #complete
                if complete == '' :
                    complete = getAO3Complete(pageData)

    #get dates
    d = compareDates(d1, d2)

    return (source, relationship, warning, rating, complete, t, a, d)