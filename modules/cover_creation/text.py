#FUNCTIONS TO CLEAN DATES AND TEXT --------------------------------------------------

# Python Standard Library
from datetime import datetime
import re

#------------------------------------------------------------------------------------

#replace HTML entities in titles with their appropriate symbol
def HTMLCharacterSwap(t):
    t = t.replace('&amp;', '&')
    t = t.replace('&lt;', '<')
    t = t.replace('&gt;', '>')
    t = t.replace('&copy;', '©')
    t = t.replace('&reg;', '®')
    t = t.replace('&deg;', '°')
    t = t.replace('&laquo;', '«')
    t = t.replace('&raquo;', '»')

    return t

#get complete/incomplete status from a chapter count
def cleanChapters(tc) :
    com = ""
    matchNum1 = re.search(r'\d+', tc)
    matchSlash = re.search('/', tc)
    num1 = tc[matchNum1.start():matchSlash.start()]
    num2 = tc[matchSlash.start()+1:]
    num1 = num1.strip()
    num2 = num2.strip()

    if num2 == '?' or num2 != num1 :
        com = "W"
    elif num1 == num2 :
        com = "C"
    
    return com

#get a clean date from a string
def cleanDate(td) :
    match = re.search(r'\d+', td)
    td = td[match.start():match.start() + 10]
    td = td.lower()
    td = td.translate({ord(i):None for i in 'abcdefghijklmnopqrstuvwxyz()[];:"+=|?>*!@#$%^&.,'})
    td = td.replace(' ', '') #whitespace
    lastChar = td[len(td) -1:]
    if lastChar == '-' :
        td = td[0 : len(td) -1]
    td = td.replace('</', '')
    td = td.replace('<', '')
    td = td.replace('/', '-')

    return td

#change date to YYYY-MM-DD format
def switchDate(d, consPrint) :

    if re.match(r"^\d{8}$", d):
        date = datetime.strptime(d, '%m-%d-%Y')
        d = date.strftime("%Y-%m-%d")
    elif re.match(r"^\d{1,2}-", d):
        try:
            date = datetime.strptime(d, '%m-%d-%Y')
            d = date.strftime("%Y-%m-%d")
        except:
            try:
                date = datetime.strptime(d, '%m-%d-%y')
                d = date.strftime("%Y-%m-%d")
            except:
                #date/month/year
                try:
                    date = datetime.strptime(d, '%d-%m-%Y')
                    d = date.strftime("%Y-%m-%d")
                except:
                    try:
                        date = datetime.strptime(d, '%d-%m-%y')
                        d = date.strftime("%Y-%m-%d")
                    except:
                        if consPrint :
                            print("Date format unrecognized")

    return d

#compare three dates to find minimum and maximum
def compareDates(d1, d2) :
    #minDate = '' #publish date
    maxDate = '' #most recent update (d)
    d1 = switchDate(d1, False)
    d2 = switchDate(d2, False)
    dateArr = [d1, d2]
    dateArr[:] = [x for x in dateArr if x != "0101-01-01" and x != "0000-00-00"] #remove junk dates
    dateArr[:] = [x for x in dateArr if x] #remove blank values
    
    #minDate = min(dateArr)
    maxDate = max(dateArr)
    
    #print(d1, d2, d3)
    #print(minDate, maxDate)
    return maxDate

# --------------------- composing f(x) ---------------------

#compose filenames: default (and remove banned characters)
def composeFilenames(a, t, d, consPrint) :
    c_title = ""
    n_filename = ""
    t = t.translate({ord(i):None for i in '\\/<>:"|?*'})
    a = a.translate({ord(i):None for i in '\\/<>:"|?*'})
    if not d:
        c_title = a + " - " + t + '.png'
        n_filename = a + " - " + t + ".epub"
    else:
        d = switchDate(d, consPrint)
        c_title = a + " - " + t + " - " + d + '.png'
        n_filename = a + " - " + t + " - " + d + ".epub"

    return c_title, n_filename

#compose filenames: include series
def composeFilenamesSeries(a, t, d, series, consPrint) :
    #author - series (where exists) - title - date
    print(t, a, d, series, consPrint)

#compose filenames: Calibre
def composeFilenamesCalibre(a, t) :
    #name format from Calibre (title - author) / (title, the/a - author)
    print(a, t)

#compose filenames: ao3downloader
def composeFilenamesAo3Downloader(a, t) :
    print(a, t)