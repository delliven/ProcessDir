import os
from pathlib import Path
import sys, csv
from datetime import datetime

strCurrentPath = os.path.dirname(__file__) ## Gets the current directory to find the config file
val = input("Enter the Directory to process:")
newfilename= strCurrentPath + "\\unknown_file_list" +  datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"


headerList = []
def processFilesinDir(folderName):
    try:
         filenameList = []
         for rootDir, mainDir, eachFile in os.walk(folderName):
            for file in eachFile:
                filenameList.append(os.path.join(rootDir, file))

         dictHeader = {}
         with open(strCurrentPath + "\\Config.txt", "r") as f: ##Opens the config file that has the header mapping
            for line in f:
                (key, val) = line.split(":")
                dictHeader[key] = val.replace("\n", "")

        
         for filename in filenameList:
            chkValue = False
            if "." not in filename: ## Rename only the files that don't have an extension
                with open(filename, "rb") as getFile:
                    headerData =  getFile.read(4).hex().upper()
                if (dictHeader.get(headerData)):
                    chkValue = True
                else:
                    addUnknownheaderInfo(headerData)    
                getFile.close()
                if (chkValue):
                    os.rename(filename, filename + "." + dictHeader.get(headerData))                
                    chkValue = False
    except Exception as error:
           print("An exception has occured.", error)
            

def addUnknownheaderInfo(headerData):
    if not headerList:
        headerList.append(headerData)
    elif not headerData in headerList:
            headerList.append(headerData)

def saveHeadertocsv(headerList):
    newfilename= strCurrentPath + "\\unknown_file_list_" +  datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
    newFile = open(newfilename, 'w')
    for strHdr in headerList:
        newFile.write(strHdr + "\n")
    newFile.close()

if os.path.exists(val):
    processFilesinDir(val)
    if not headerList == []:
        saveHeadertocsv(headerList)
    else:
        print("No unknown headers found.")
else:
    print("path does not exist")