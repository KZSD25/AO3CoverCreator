#USER MENUS --------------------------------------------------------------------------

# Python Standard Library
from datetime import datetime
import os, os.path, uuid
import fnmatch
import shutil
import json

#------------------------------------------------------------------------------------

# --------------------- START MENU ---------------------
def startMenu(dir) :
    #get settings
    filename = 'settings.json'
    coverType = ""
    coverEpub = False
    coverFolder = False
    fileName = ""
    consolePrint = ""
    coverMethod = ""
    with open(filename, 'r') as file :
        settings = json.load(file)
        coverType = settings['cover-type']
        coverEpub = settings['save-covers-in-epub']
        coverFolder = settings['save-covers-in-folder']
        fileName = settings['file-name']
        consolePrint = settings['console-printout']
        coverMethod = settings['cover-method']


    #program start
    print ("\n-------- Starting AO3 EPUB Cover Creator --------\n")
    print ("Place the EPUB files you want to edit in the 'Books' folder.")

    #confirm number of .epub files in folder
    confirmEpubs(dir)

    #menu tree
    loop = True
    while loop :
        #main menu
        conVar = mainMenu(coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod)

        #menu select
        if conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        elif conVar != "0" :
            coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod = mainMenuSelect(conVar, coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod)
        else :
            loop = False

    print("\nRunning program . . .")
    print("When complete, the program will save a copy of the file in the 'Copies' folder.")
    print("For any files that are not able to be processed, the program will save a copy in the 'ErrorFiles' folder.\n")

    #save JSON
    with open(filename, 'r') as f:
        settings = json.load(f)
        settings['cover-type'] = coverType
        settings['save-covers-in-epub'] = coverEpub
        settings['save-covers-in-folder'] = coverFolder
        settings['file-name'] = fileName
        settings['console-printout'] = consolePrint
        settings['cover-method'] = coverMethod

    # create randomly named temporary file (to avoid interference with other thread/asynchronous request)
    tempfile = os.path.join(os.path.dirname(filename), str(uuid.uuid4()))
    with open(tempfile, 'w') as f:
        json.dump(settings, f, indent=4)

    # remove original and rename temporary file
    os.remove(os.path.join(os.path.dirname(filename), filename)) #needed for Win
    os.rename(tempfile, filename)

    #convert settings
    if coverType == "light" :
        darkMode = False
    elif coverType == "dark" :
        darkMode = True
    if consolePrint == "full" :
        consPrint = True
    elif consolePrint == "summary" :
        consPrint = False
    if coverMethod == "calibre cover" :
        cvMethod = True
    elif coverMethod == "test method" :
        cvMethod = False

    return darkMode, coverEpub, coverFolder, fileName, consPrint, cvMethod

#start menu > confirm files in Books folder
def confirmEpubs(dir) :
    conVar = input(str(len(fnmatch.filter(os.listdir(dir), '*.epub'))) + " EPUB files found. Is this correct?".ljust(40) + "(Y)es\n")

    loop = True

    while loop :
        if conVar.lower() == "y" or conVar.lower() == "yes" :
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nThe 'Books' folder should be in the same folder as the python program. This program can only read files with '.epub' extensions.")
            conVar = input(str(len(fnmatch.filter(os.listdir(dir), '*.epub'))) + " EPUB files found. Is this correct?".ljust(40) + "(Y)es\n")

#start menu > main menu
def mainMenu(coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod) :
    
    just = 50
    print("\n-------- Main Menu --------")
    conVar = input("0) Run Program\n1) Change Cover Type".ljust(just + 14) + coverType + "\n2) Save Cover in EPUB (warning)".ljust(just) + str(coverEpub) + "\n3) Save Cover PNG in Covers Folder".ljust(just) + str(coverFolder) + "\n4) Change File Name Format (wip)".ljust(just) + fileName + "\n5) Change Terminal Print Detail".ljust(just) + consolePrint + "\n6) Change Cover Save Method".ljust(just) + coverMethod + "\nQ) Quit\n")
    
    sel = -1
    try :
        sel = int(conVar)
    except Exception as e :
        sel = -1
    
    loop = True

    while loop :
        if conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        elif sel >= 0 and sel <= 6:
            loop = False
        else:
            print("\nInput not recognized")
            conVar = input("Please enter a number 0 through 6\n")
            try :
                sel = int(conVar)
            except Exception as e :
                sel = -1

    return conVar

#start menu > main menu > main menu select
def mainMenuSelect(conVar, coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod) :

    match conVar :
        case "1" :
            coverType = menuChangeCoverType(coverType)
        case "2" :
            coverEpub = menuSaveCoverEpub(coverEpub, coverMethod)
        case "3" :
            coverFolder = menuSaveCoverFolder(coverFolder)
        case "4" :
            fileName = menuFileNameFormat(fileName)
        case "5" :
            consolePrint = menuChangePrintDetail(consolePrint)
        case "6" :
            coverMethod = menuChangeCoverMethod(coverMethod)

    return coverType, coverEpub, coverFolder, fileName, consolePrint, coverMethod

#start menu > main menu > submenu: change cover type
def menuChangeCoverType(coverType) :
    conVar = input("\nCover Type".ljust(43) + "Saved Setting: " + coverType + "\n     1) Light Mode: covers are white with black text\n     2) Dark Mode: covers are dark gray with white text\n")

    loop = True

    while loop :
        if "light" in conVar.lower() or conVar == "1" :
            coverType = "light"
            loop = False
        elif "dark" in conVar.lower() or conVar == "2" :
            coverType = "dark"
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nInput not recognized")
            conVar = input("Please enter '1' for Light Mode Covers or '2' for Dark Mode Covers.\n")

    if coverType == "dark" :
        print("Dark Mode Covers selected")
    elif coverType == "light" :
        print("Light Mode Covers selected")

    return coverType

#start menu > main menu > submenu: save cover in epub
def menuSaveCoverEpub(coverEpub, coverMethod) :
    if coverMethod == "calibre cover" :
        warning = "\nWARNING: this will overwrite existing covers\n         this only works for files with a cover already (like Calibre's default cover)\n     "
    elif coverMethod == "test method" :
        warning = "\nWARNING: this may compromise the integrity of the epub\n         the test method has been selected, which will attempt to save the cover images to the epub file directly\n     "

    conVar = input("\nSave Cover in EPUB".ljust(43) + "Saved Setting: " + str(coverEpub) + warning + "1) Yes: created covers will save as 'cover.jpg' in the EPUB metadata\n     2) No: created covers will not save in the EPUB\n")

    loop = True

    while loop :
        if "yes" in conVar.lower() or conVar == "1" :
            coverEpub = True
            loop = False
        elif "no" in conVar.lower() or conVar == "2" :
            coverEpub = False
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nInput not recognized")
            conVar = input("Please enter '1' for Yes or '2' for No.\n")

    if coverEpub :
        print("Covers will save in EPUB")
    else :
        print("Covers will not save in EPUB")
    
    return coverEpub

#start menu > main menu > submenu: save covers in folder
def menuSaveCoverFolder(coverFolder) :
    conVar = input("\nSave Cover PNG in Covers Folder".ljust(43) + "Saved Setting: " + str(coverFolder) + "\n     1) Yes: created covers will save as PNGs in the Covers folder\n     2) No: created covers will not save in the Covers folder\n")

    loop = True

    while loop :
        if "yes" in conVar.lower() or conVar == "1" :
            coverFolder = True
            loop = False
        elif "no" in conVar.lower() or conVar == "2" :
            coverFolder = False
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nInput not recognized")
            conVar = input("Please enter '1' for Yes or '2' for No.\n")

    if coverFolder :
        print("Covers will save in Covers folder")
    else :
        print("Covers will not save in Covers folder")
    
    return coverFolder

#start menu > main menu > submenu: change file name format
def menuFileNameFormat(fileName) :

    print("Work in Progress")
    #author - title - date
    #author - series (where exists) - title - date
    #keep name format of files
    #name format from Calibre (title - author) / (title, the/a - author)
    #name format from ao3downloader ()

    return fileName

#start menu > main menu > submenu: change printout detail
def menuChangePrintDetail(consolePrint) :
    conVar = input("\nChange Terminal Print Detail".ljust(43) + "Saved Setting: " + consolePrint + "\n     1) Full: the console will print out all details when running the program (useful for bug reports)\n     2) Summary: the console will only print the file number and file name it is working on\n")

    loop = True

    while loop :
        if "full" in conVar.lower() or conVar == "1" :
            consolePrint = "full"
            loop = False
        elif "summary" in conVar.lower() or conVar == "2" :
            consolePrint = "summary"
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nInput not recognized")
            conVar = input("Please enter '1' for Full Details or '2' for Summary Details.\n")

    if consolePrint == "full" :
        print("Console will print all details")
    elif consolePrint == "summary" :
        print("Console will print only a summary")
    
    return consolePrint

#start menu > main menu > submenu: change cover method
def menuChangeCoverMethod(coverMethod) :
    conVar = input("\nChange Cover Method".ljust(43) + "Saved Setting: " + coverMethod + "\n     1) Calibre Cover: use when placeholder covers already exist, such as a Calibre default cover (recommended)\n     2) Test Method: try to save covers when a placeholder cover does not exist (still under development, but can be tested)\n")

    loop = True

    while loop :
        if "calibre" in conVar.lower() or conVar == "1" :
            coverMethod = "calibre cover"
            loop = False
        elif "test" in conVar.lower() or conVar == "2" :
            coverMethod = "test method"
            loop = False
        elif conVar.lower() == "q" or conVar.lower() == "quit" :
            quit()
        else:
            print("\nInput not recognized")
            conVar = input("Please enter '1' for Calibre Cover or '2' for Test Method.\n")

    if coverMethod == "calibre cover" :
        print("Program will save new covers over existing covers")
    elif coverMethod == "test method" :
        print("Program will try to save covers without a pre-existing cover")
    
    return coverMethod

# --------------------- END MENU ---------------------
def endMenu(error_list) :
    if len(error_list) > 0:
        print("\nPrinting Error List . . .")
        with open('error_list_' +  datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt', 'w') as file:
            file.write('\n'.join(error_list))
        print("\nSome files could not be processed. Please check the 'ErrorFiles' folder.")
    else:
        print("No files were caught in the error list")

    print("\nAll Files Complete")
    print("Check the 'Copies' folder for completed EPUB files")

#file error message (file could not be processed)
def errorMessage(e, errMsg, filename, error_list, dir, error) :
    print(e)
    print(errMsg)
    print("File: " + filename)
    error_list.append(filename)
    shutil.copy(dir + "/" + filename, error + "/" + filename)

    return error_list