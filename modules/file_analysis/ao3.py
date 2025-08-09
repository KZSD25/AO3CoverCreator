#ARCHIVE OF OUR OWN ----------------------------------------------------------------

import ebooklib
from ebooklib import epub

from ..cover_creation.text import HTMLCharacterSwap, cleanChapters
from .meta import getAO3Complete, getAO3Rating, getAO3Relationship, getAO3Warning

#------------------------------------------------------------------------------------

#AO3-created EPUB
def metaAO3(book, warning, relationship, rating, complete, source, consPrint) :
    if consPrint :
        print ("AO3 tags found")

    # get book metadata
    a = book.get_metadata('DC', 'creator')[0][0]
    t = book.get_metadata('DC', 'title')[0][0]
    d = book.get_metadata('DC', 'date')[0][0]
    #tags = book.get_metadata('DC', 'subject') # rating
    
    t = HTMLCharacterSwap(t)
    if "T" in d:
        d = d.split('T', 1)[0]

    print ("File: " + a + " - " + t + " - " + d)

    warning = ""
    relationship = []
    rating = ""
    complete = ""
    source = "AO3"

    # get tag information
    for item in book.get_items():
            
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # print(item.get_name()) #page filename
                # print(item.get_content()) #all content of file

                pageData = item.get_content() #in bytes
                pageData = pageData.decode("utf-8") #convert byte to string

                #warning
                warning = getAO3Warning(pageData, warning)

                #relationship
                relationship = getAO3Relationship(pageData, relationship)
                
                #rating
                rating = getAO3Rating(pageData, rating)
                
                #complete
                if complete == '' :
                    complete = getAO3Complete(pageData)

    return (source, relationship, warning, rating, complete, t, a, d)