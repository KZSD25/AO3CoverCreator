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
                if consPrint :
                    print("Date format unrecognized")

    return d

#compose filenames (and remove banned characters)
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

    return (c_title, n_filename)