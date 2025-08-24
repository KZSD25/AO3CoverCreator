# AO3CoverCreator

The AO3 Cover Creator is a command line python program that takes EPUB files and creates a cover. The program:
* Uses the command prompt as the UI
* Reads EPUB files in the 'Books' folder
* Creates a copy of the EPUB file in the 'Copies' folder, renaming: "[author] - [title] - [update date].epub"
* Creates a cover with the original posting site, title, author, and AO3-like tag symbols for rating, pairing, archive warning, and completeness
* If the EPUB already has a cover (such as the Calibre default cover), save the generated PNG image cover into the copied EPUB file
* Creates a list of files that the program could not read, and copies the files into the 'ErrorList' folder

The program is designed for the EPUB files that are downloaded directly from AO3. The program can accommodate some other sources of EPUB, such as EPUBs created from the FanFicFare Calibre plugin. Not every EPUB file is fully supported.


## Requirements

* Python v3 (or above)
* Pillow 11.3.0 (https://pypi.org/project/pillow/)
* EbookLib 0.18 (https://pypi.org/project/EbookLib/)
* ebookmeta 1.2.11 (https://pypi.org/project/ebookmeta/)
* os, re, io, sys, bs4, json, uuid, shutil, fnmatch, datetime, zipfile, warnings (Python Standard Library)


## Tested OSes

* Windows 10
* Linux Mint 22

It may be possible to run on other machines, but it has not been tested.


## Installation Requirements

1. For Python, please search how to install, or follow the instructions found here: https://realpython.com/installing-python/
2. Pillow, EbookLib, and ebookmeta are included in the AO3CoverCreator program, and do not need to be installed
3. The Python Standard Library will usually be included in your python installation


## Downloading the Program

Download the "Source code.zip", under Assets, in [releases](https://github.com/KZSD25/AO3CoverCreator/releases)


## Running the Program

1. Extract the .zip file and place the 'AO3CoverCreator' folder somewhere on your computer. Do not remove or re-name any files or folders that are inside.

2. Place EPUB files in the 'Books' folder. It is recommended that you copy-paste files into the folder, and keep your original files safe.
     * The 'Books' folder is the only place the program will look for files
     * The program will only read EPUB files--files that end in ".epub"

3) Open the command console/terminal (in the Windows search bar, search "cmd")

4) In the command console, navigate to the 'AO3CoverCreator' folder

5) Run the python file by pasting the following into the command console, depending on the OS and python installation type:

* Windows (version 1)

`py AO3CoverCreator.py`

* Windows (version 2)

`python AO3CoverCreator.py`

* Linux / MacOS

`python3 AO3CoverCreator.py`

6) A message should appear: "Starting AO3 EPUB Cover Creator"

7) Follow the prompts as they appear, typing into the command console

8) When done, a message should appear: "All Files Complete"

9) To exit the program while in the menu, type "q" or "quit"


## Preparing EPUB Files to Save the Covers Directly into the EPUB Files:

If an EPUB file does not have a cover image, the simplest way to mass-prepare EPUBs with cover images is to use Calibre (https://calibre-ebook.com)

1) Open Calibre

2) Upload EPUB files into Calibre - it is recommended you create a new library, so that you do not interfere with your other books

3) Select the EPUB files in Calibre

4) Click the down arrow next to "Edit metadata", then click "Edit metadata in bulk"

5) Under "Change cover", click "Generate default cover"

6) Click "OK"

7) Select the EPUB files in Calibre, again

8) Click the down arrow next to "Save to disk", then click "Save to disk in single folder"

9) Navigate to the 'Books' folder in the AO3CoverCreator, click "Select folder"

10) (optional) The OPF and JPG files can be deleted from the 'Books' folder in the AO3CoverCreator


## TODO:

1) Saving the created cover directly into the EPUB file without needing to have a cover, first
2) If a cover already exists, add new cover in addition to original cover (do not overwrite original cover)
3) Testing the program on Mac and Windows 11
4) Adding more support for non-AO3 EPUB sources
5) Adding more support for FanFicFare EPUBs
6) Check support for Cyrillic characters (and other languages)
7) Update EbookLib in 'libraries' to current version (0.19) and adjust code as needed