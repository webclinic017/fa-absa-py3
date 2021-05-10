
import acm
import sys

def addInfoSumFunction(tradesInPosition, addInfoName):
    sum=0
    
    for t in tradesInPosition.AsArray():
        if t.add_info(addInfoName):
            sum = sum + float(t.add_info(addInfoName))
    return sum
