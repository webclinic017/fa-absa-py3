import ael, string

def CalibrateDivTypes(divEst, *rest):
    divType = string.rstrip(string.lstrip(string.lower(divEst.description)))
    if (divType == "spec") or (divType == "special") or (divType == "s") or (divType == "special div"):
        divType = "Special"
    elif (divType == "final") or (divType == "f") or (divType == "fin"):
        divType = "Final"
    elif (divType == "interim") or (divType == "intrim") or (divType == "i") or (divType == "int"):
        divType = "Interim"
        
    if (divType != "Final") and (divType != "Special") and (divType != "Interim"):
        divType = "Final_" + divType
    
    return divType
