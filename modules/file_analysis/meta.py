#FUNCTIONS TO ANALYZE FILES ---------------------------------------------------------

# Python Standard Library
import re

from ..tag_library.tag_lists import LIST_COMPLETE, LIST_INCOMPLETE, LIST_RATING_E, LIST_RATING_G, LIST_RATING_M, LIST_RATING_T, LIST_REL_OTHER, LIST_REL_FF, LIST_REL_FM, LIST_REL_MM, LIST_REL_MULTI, LIST_WARNING_C, LIST_WARNING_W#, LIST_WARNING_N
from ..tag_library.user_tag_lists import LIST_USER_TAGS_COMPLETE, LIST_USER_TAGS_RATING
from ..cover_creation.text import cleanDate, cleanChapters

#------------------------------------------------------------------------------------

#get most recent complete or update date from page contents
def getDate(pageData, d) :
    td = ""
    
    if 'updated:' in pageData.lower() :
        loc = pageData.lower().find('updated:')
        end = loc + 35
        td = pageData[loc:end]
        td = cleanDate(td)
    elif 'last updated on:' in pageData.lower() :
        loc = pageData.lower().find('last updated on:')
        end = loc + 35
        td = pageData[loc:end]
        td = cleanDate(td)
    elif 'published:' in pageData.lower() :
        loc = pageData.find('Published:')
        end = loc + 35
        td = pageData[loc:end]
        td = cleanDate(td)
    elif 'published on:' in pageData.lower() :
        loc = pageData.lower().find('published on:')
        end = loc + 35
        td = pageData[loc:end]
        td = cleanDate(td)

    if d == "" or len(td) > 4 :
        d = td

    return d

#get complete status from master list compared against page contents
def getListComplete(pageData, complete) :
    for listCom in LIST_COMPLETE :
        if listCom in pageData.lower() :
            #complete
            complete = "C"
            break
    if complete == "" :
        for listIncom in LIST_INCOMPLETE :
            if listIncom in pageData.lower() :
                #incomplete / work in progress
                complete = "W"
                break
    
    return complete

#get rating from master list compared against page contents
def getListRating(pageData, rating) :
    for listE in LIST_RATING_E :
        if listE in pageData.lower() :
            #explicit
            rating = "E"
            break
    if rating == "" :
        for listM in LIST_RATING_M :
            if listM in pageData.lower() :
                #mature
                rating = "M"
                break
    if rating == "" :
        for listT in LIST_RATING_T :
            if listT in pageData.lower() :
                #teen
                rating = "T"
                break
    if rating == "" :
        for listG in LIST_RATING_G :
            if listG in pageData.lower() :
                #gen
                rating = "G"
                break

    return rating

#get relationship based on AO3 tag or master list compared against page contents
def getListRelationship(pageData, relationship) :
    
    if 'archiveofourown.org/tags/gen">' in pageData.lower() :
        #Gen
        relationship.append("Gen")

    for listR in LIST_REL_FF :
        if listR in pageData.lower() :
            #Other
            relationship.append("F/F")
            break
    for listR in LIST_REL_MM :
        if listR in pageData.lower() :
            #Other
            relationship.append("M/M")
            break
    for listR in LIST_REL_MULTI :
        if listR in pageData.lower() :
            #Other
            relationship.append("Multi")
            break
    for listR in LIST_REL_FM :
        if listR in pageData.lower() :
            #Other
            relationship.append("F/M")
            break
    for listR in LIST_REL_OTHER :
        if listR in pageData.lower() :
            #Other
            relationship.append("Other")
            break

    return relationship

#get warning from master list compared against page contents
def getListWarning(pageData, warning, source) :
    if source == "FFN" or source == "WTT" :
        warning = "C" #FFN and wattpad do not use warnings, and so is 'Creator chose not to...' by default
    if warning == "" :
        for listW in LIST_WARNING_W :
            if listW in pageData.lower() :
                warning = "W"
                break
    if warning == "" :
        for listC in LIST_WARNING_C :
            if listC in pageData.lower() :
                warning = "C"
                break

    return warning

#get AO3, FFN, or WTT from page contents
def getSource(pageData, source) :
    if 'fanfiction.net' in pageData.lower() :
        source = "FFN"
    elif 'archiveofourown.org' in pageData.lower() :
        source = "AO3"
    elif 'wattpad' in pageData.lower() :
        source = "WTT"

    return source

#get AO3, FFN, or WTT from publisher metadata
def getSourcePublisher(book) :
    src = ""

    if 'fanfiction.net' in book.get_metadata('DC', 'publisher')[0][0].lower() :
        src = "FFN"
    elif 'archiveofourown.org' in book.get_metadata('DC', 'publisher')[0][0].lower() :
        src = "AO3"
    elif 'wattpad.com' in book.get_metadata('DC', 'publisher')[0][0].lower() :
        src = "WTT"
    
    return src

#get relationship from AO3 tags compared against subject metadata
def getTagsRelationship(book, relationship) :
    tags = book.get_metadata('DC', 'subject') # tags
    
    for tag in tags :
        if tag[0] == 'F/F' :
            #F/F
            relationship.append("F/F")
        if tag[0] == 'M/M' :
            #M/M
            relationship.append("M/M")
        if tag[0] == 'Multi' :
            #Multi
            relationship.append("Multi")
        if tag[0] == 'Gen' :
            #Gen
            relationship.append("Gen")
        if tag[0] == 'F/M' :
            #F/M
            relationship.append("F/M")
        # if tag[0] == 'Other' : # possible to have an "other" tag and not mean a relationship
        #     #Other
        #     relationship.append("Other")
    
    return relationship

#get complete status from AO3 tags compared against page contents
def getAO3Complete(pageData) :
    #determines incomplete from 0/?
    incompleteReg = r"Chapters: \d*?/\?"
    complete = ""

    try : #trying Chapters: 0/0 because some old FF savers didn't have /total
        if re.findall(incompleteReg, pageData) :
            #incomplete / work in progress
            complete = "W"
        if 'Chapters:' in pageData :
            #determines complete from 0/0
            loc = pageData.find('Chapters:')
            end = loc + 20
            tc = pageData[loc:end]
            complete = cleanChapters(tc)

    except :
        if 'Completed:' in pageData :
            #complete
            complete = "C"
        elif 'Updated:' in pageData :
            #incomplete / work in progress
            complete = "W"
        elif 'Completed:' not in pageData and 'Updated:' not in pageData and 'Chapters:' not in pageData :
            #one chapter work, complete
            complete = "C"

    return complete

#get rating from AO3 tags compared against page contents
def getAO3Rating(pageData, rating) :
    if 'archiveofourown.org/tags/explicit">' in pageData.lower() :
        #explicit
        rating = "E"
    elif 'archiveofourown.org/tags/mature">' in pageData.lower() :
        #mature
        rating = "M"
    elif 'archiveofourown.org/tags/teen%20and%20up%20audiences">' in pageData.lower() or 'archiveofourown.org/tags/teen and up audiences">' in pageData.lower() :
        #teen
        rating = "T"
    elif 'archiveofourown.org/tags/general%20audiences">' in pageData.lower() or 'archiveofourown.org/tags/general audiences">' in pageData.lower() :
        #gen
        rating = "G"
    #<a href="https://archiveofourown.org/tags/Not%20Rated/"> no rating

    return rating

#get relationship from AO3 tags compared against page contents
def getAO3Relationship(pageData, relationship) :
    if 'archiveofourown.org/tags/f*s*f">' in pageData.lower() :
        #F/F
        relationship.append("F/F")
    if 'archiveofourown.org/tags/m*s*m">' in pageData.lower() :
        #M/M
        relationship.append("M/M")
    if 'archiveofourown.org/tags/multi">' in pageData.lower() :
        #Multi
        relationship.append("Multi")
    if 'archiveofourown.org/tags/gen">' in pageData.lower() :
        #Gen
        relationship.append("Gen")
    if 'archiveofourown.org/tags/f*s*m">' in pageData.lower() :
        #F/M
        relationship.append("F/M")
    if 'archiveofourown.org/tags/other">' in pageData.lower() :
        #Other
        relationship.append("Other")

    return relationship

#get warning from AO3 tags compared against page contents
def getAO3Warning(pageData, warning) :
    if ('archiveofourown.org/tags/graphic%20depictions%20of%20violence">' in pageData.lower()) or ('archiveofourown.org/tags/major%20character%20death">' in pageData.lower()) or ('archiveofourown.org/tags/rape*s*non-con">' in pageData.lower()) or ('archiveofourown.org/tags/underage">' in pageData.lower()) or ('archiveofourown.org/tags/graphic depictions of violence">' in pageData.lower()) or ('archiveofourown.org/tags/major character death">' in pageData.lower()) :
        #warning
        warning = "W"
    elif 'archiveofourown.org/tags/choose%20not%20to%20use%20archive%20warnings">' in pageData.lower() or 'archiveofourown.org/tags/choose not to use archive warnings">' in pageData.lower() :
        #chose not to use (and no warnings)
        warning = "C"
    #archiveofourown.org/tags/No%20Archive%20Warnings%20Apply"> no warning

    return warning

#get complete status from list of user tags compared against subject metadata
def userTagsComplete(book) :
    user_complete = ""

    tags = book.get_metadata('DC', 'subject')
    for tag in tags :
        for list_u_c in LIST_USER_TAGS_COMPLETE :
            if tag[0] == list_u_c[0] :
                user_complete = list_u_c[1]

    return user_complete

#get rating from list of user tags compared against subject metadata
def userTagsRating(book) :
    user_rating = ""

    tags = book.get_metadata('DC', 'subject')
    for tag in tags :
        for list_u_r in LIST_USER_TAGS_RATING :
            if tag[0] == list_u_r[0] :
                user_rating = list_u_r[1]

    return user_rating