#FUNCTIONS TO CREATE A COVER --------------------------------------------------------

# Python Standard Library
import shutil
import re
import io

# in './libraries'
import PIL
from PIL import Image, ImageDraw, ImageFont
import ebooklib
from ebooklib import epub
import ebookmeta

from .text import composeFilenames

#------------------------------------------------------------------------------------

#detects if the text has Japanese, Chinese, or Korean characters
def detectLanguage(f1, f2) :
    #[一-龠ぁ-ゔァ-ヴーａ-ｚＡ-Ｚ０-９々〆〤]+ jpn
    #/[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]/ jpn + chn
    #\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f\u3131-\uD79D jpn + chn + kor
    #rKanji = u'[\u4E00-\u9FFF]+' # == u'[一-龠々]+'
    #rHiragana = u'[\u3040-\u309Fー]+' # == u'[ぁ-んー]+'
    #rKatakana = u'[\u30A0-\u30FF]+' # == u'[ァ-ヾ]+'
    # rJPN = u'[\u3040-\u30ff\uff66-\uff9f]'
    # rCHN = u'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]'
    # rKOR = u'[\u3131-\uD79D]' #r'^[가-힣]+'
    # jpn = False
    # kor = False
    # chn = False
    rCJK = u'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f\u3131-\uD79D]'
    checkCJK = False

    # if re.search(rJPN, f1, re.U) or re.search(rJPN, f2, re.U) :
    #     jpn = True

    # if re.search(rCHN, f1, re.U) or re.search(rCHN, f2, re.U) :
    #     chn = True

    # if re.search(rKOR, f1, re.U) or re.search(rKOR, f2, re.U) :
    #     kor = True

    if re.search(rCJK, f1, re.U) or re.search(rCJK, f2, re.U) :
        checkCJK = True

    return checkCJK

#returns an array of string broken into lengths >= 1100 (max text width of the page)
def dynamicCoverText(t, font):
    t_array = []
    linewidth = 0

    if t == "" :
        t_array.append("")

    container = t.split()
    holdArray = []

    for i in range(len(container)) :
        holdArray.append(container[i])
        linewidth = font.getlength(' '.join(holdArray))

        #if last word, double-check not over 1100px length
        if i == len(container) - 1 :
            if linewidth >= 1100 :
                del holdArray[-1]
                t_array.append(' '.join(holdArray))
                holdArray.clear()
                holdArray.append(container[i])

            t_array.append(' '.join(holdArray))

        #cut when words go over 1100px in length
        elif linewidth >= 1100 :
            del holdArray[-1]
            t_array.append(' '.join(holdArray))
            holdArray.clear()
            holdArray.append(container[i])
    
    return t_array

#create a cover image using Pillow
def createCoverImage(source, relationship, warning, rating, complete, t, a, darkMode) :

    #create image with tag information
    cover = Image.open("./images/_cover.png")
    if darkMode :
        cover = Image.open("./images/_coverDark.png")
    warning_tile = Image.open("./images/_nowarning.png")
    relationship_tile = Image.open("./images/_norelationship.png")
    rating_tile = Image.open("./images/_norating.png")
    complete_tile = Image.open("./images/_nocomplete.png")
    source_tile = Image.open("./images/_empty.png")

    #source
    if source == "AO3" :
        source_tile = Image.open("./images/_ao3.png")
    elif source == "FFN" :
        source_tile = Image.open("./images/_ffn.png")
    elif source == "WTT" :
        source_tile = Image.open("./images/_wtt.png")

    #relationship
    if (len(relationship)) > 1 or "Multi" in relationship :
        relationship_tile = Image.open("./images/_foursquare.png")
    elif "F/F" in relationship :
        relationship_tile = Image.open("./images/_wlw.png")
    elif "M/M" in relationship :
        relationship_tile = Image.open("./images/_mlm.png")
    elif "F/M" in relationship :
        relationship_tile = Image.open("./images/_flm.png")
    elif "Other" in relationship :
        relationship_tile = Image.open("./images/_other.png")
    elif "Gen" in relationship :
        relationship_tile = Image.open("./images/_genromance.png")

    #warning
    if warning == "W" :
        warning_tile = Image.open("./images/_contentwarning.png")
    elif warning == "C" :
        warning_tile = Image.open("./images/_creatordidnotselectwarning.png")
    
    #rating
    if rating == "E" :
        rating_tile = Image.open("./images/_explicit.png")
    elif rating == "M" :
        rating_tile = Image.open("./images/_mature.png")
    elif rating == "T" :
        rating_tile = Image.open("./images/_teen.png")
    elif rating == "G" :
        rating_tile = Image.open("./images/_general.png")
        
    #complete
    if complete == "C" :
        complete_tile = Image.open("./images/_complete.png")
    elif complete == "W" :
        complete_tile = Image.open("./images/_incomplete.png")

    #compose cover tiles
    cover.paste(warning_tile, (0, 0), warning_tile)
    cover.paste(relationship_tile, (0, 0), relationship_tile)
    cover.paste(rating_tile, (0, 0), rating_tile)
    cover.paste(complete_tile, (0, 0), complete_tile)
    cover.paste(source_tile, (0, 0), source_tile)

    #language
    CJK = detectLanguage(t, a)
    fontFile = './images/bahnschrift.ttf'
    if CJK:
        fontFile = './images/SourceHanMono-Regular.otf'
    
    #compose title
    draw = ImageDraw.Draw(cover)
    font = ImageFont.truetype(font=fontFile, size=120)
    font_a = ImageFont.truetype(font=fontFile, size=90)
    text_color = (0, 0, 0)
    if darkMode:
        text_color = (255, 255, 255)
    #OLD: total width to work with: 486px
    #OLD: start coords (50, 630)
    #new: total width to work with: 1100
    text = t
    auth = a
    title_width = 0
    author_width = 0
    sz = 120

    #dynamic title
    if font.getlength(t) > (5 * 1100) and font.getlength(t) <= (7 * 1100) :
        font = ImageFont.truetype(font=fontFile, size=100)
        sz = 100
    elif font.getlength(t) > (7 * 1100) :
        font = ImageFont.truetype(font=fontFile, size=80)
        sz = 80
    t_array = dynamicCoverText(t, font)
    text = '\n'.join(t_array)

    for item in t_array :
        if font.getlength(item) > title_width :
            title_width = font.getlength(item)

    #dynamic author
    a_array = dynamicCoverText(a, font_a)
    auth = '\n'.join(a_array)

    for item in a_array :
        if font_a.getlength(item) > author_width :
            author_width = font_a.getlength(item)
    
    new_width = (1200 - title_width) / 2
    new_a_width = (1200 - author_width) / 2
    draw.multiline_text((new_width, 800), text, fill=text_color, font=font, align='center')
    draw.multiline_text((new_a_width, 860 + (len(t_array)*sz)), auth, fill=text_color, font=font_a, align='center')

    return cover

#create cover file, new EPUB file, and save cover to EPUB metadata (only works when cover image already exists)
def createCoverFile(source, relationship, warning, rating, complete, t, a, d, darkMode, covers, filename, dir, save, consPrint, coverEpub, coverFolder) :
    if consPrint :
        print("Creating cover . . .")
                
    cover = createCoverImage(source, relationship, warning, rating, complete, t, a, darkMode)

    if consPrint and coverFolder :
        print("Saving files . . .")

    #cover.show()

    #TODO: SAVE COVER IMAGE WITHOUT PLACEHOLDER COVER

    #remove non-filename characters and save files
    coverTitle, new_filename = composeFilenames(a, t, d, consPrint)
    if coverFolder :
        cover.save(covers + '/' + coverTitle, format='PNG')
    shutil.copy(dir + "/" + filename, save + "/" + new_filename)

    if consPrint and coverEpub :
        print("Setting cover to copied EPUB . . .".ljust(40) + "(this will only work if a cover image already exists)")
    
    if coverEpub :
        #convert cover img to byte array
        byteArr = io.BytesIO()
        cover.save(byteArr, format='PNG')
        byteArr = byteArr.getvalue()

        meta = ebookmeta.get_metadata(save + "/" + new_filename)

        #TODO: GET ORIGINAL cover.jpg DATA AND SAVE AS NEW IMAGE IN meta AS cover_original.jpg

        meta.cover_image_data = byteArr #byte array
        meta.cover_media_type = "image/png"
        meta.cover_file_name = coverTitle

        ebookmeta.set_metadata(save + "/" + new_filename, meta)  # Set epub metadata from Metadata class

    #close the PIL cover image
    cover.close()

#save file if both coverEpub and coverFolder are False
def saveCopyEpub(t, a, d, filename, dir, save, consPrint) :
    #remove non-filename characters and save files
    coverTitle, new_filename = composeFilenames(a, t, d, consPrint)
    shutil.copy(dir + "/" + filename, save + "/" + new_filename)