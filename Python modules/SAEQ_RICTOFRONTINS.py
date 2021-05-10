import ael

def removeNums(str):
    text = list(str)
    revisedStr = ""
    for item in text:
        try:
            i = int(item)
        except:
            revisedStr += item
    return revisedStr.strip()

def ReformatRICString(instr, RIC, *rest):
    return RIC.split()[1]
    
def IsInstrumentNeeded(instr, *rest):
    tmpReturn = instr.insid

    baseInsName = removeNums(instr.insid)
    if baseInsName != tmpReturn:
        tmpReturn = "-1"
        
    return tmpReturn
