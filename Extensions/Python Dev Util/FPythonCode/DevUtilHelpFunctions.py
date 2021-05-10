import acm
import os

def SaveToFile(fileName, text) :
    file = open(fileName, 'w')
    file.write(text)
    file.close()

def FindFilePath(startDir, searchForFile):
    if startDir:
        for root, dirs, files in os.walk(startDir):
            for file in files:
                if file == searchForFile:
                    return os.path.join(root, '')
    return None
    
