#FANFICFARE -------------------------------------------------------------------------

import re

import ebooklib
from ebooklib import epub

from ..cover_creation.text import HTMLCharacterSwap
from .meta import getSourcePublisher, getListRelationship, getTagsRelationship, getListWarning, getListRating, getListComplete

#------------------------------------------------------------------------------------

#FanFicFare has the most comprehensive EPUB creation for fanfic, and includes almost all necessary elements
#FanFicFare should be searched for first in order to take advantage of its .opf file

def metaFanFicFare(book, consPrint) :

    if consPrint :
        print ("FanFicFare tags found")

    # get book metadata
    a = book.get_metadata('DC', 'creator')[0][0]
    t = book.get_metadata('DC', 'title')[0][0]
    d = book.get_metadata('DC', 'date')[0][0]

    t = HTMLCharacterSwap(t)
    d_array = book.get_metadata('DC', 'date')

    #most recent updated date (FFF only)
    for date in d_array:
        if date[1] == {'{http://www.idpf.org/2007/opf}event': 'modification'} :
            d = date[0]

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

            if item.get_name() == "OEBPS/title_page.xhtml" :

                pageData = item.get_content() #in bytes
                pageData = pageData.decode("utf-8") #convert byte to string

                #warning
                if warning == '' :
                    warning = getListWarning(pageData, warning, source)

                #FFN tags, also in <dc:subject>
                #genre = re.search(r'genre:.*?<br/>', pageData.lower()) #get string of Genre: [. . . ] <br/>, with the first known instance of <br/>

                #relationship
                relationship = getListRelationship(pageData, relationship)

                #rating
                if rating == '' :
                    rating = getListRating(pageData, rating)
                    if 'WARNING: This story contains mature' in pageData:
                        #wattpad's mature
                        rating = "M"

                #complete
                if complete == '' :
                    complete = getListComplete(pageData, complete)

    #relationship (AO3 tags)
    relationship = getTagsRelationship(book, relationship)

    return (source, relationship, warning, rating, complete, t, a, d)