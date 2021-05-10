""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionRounding.py"
import acm
import math
from FBDPCurrentContext import Logme

epsilon = 1e-10

def RoundQuantityDown(quantity, decimals):
    Logme()('FCorpActionRounding RoundQuantityDown Initial Quantity %+06.12f' %(quantity), 'INFO')
    if quantity < 0:
        quantity = math.ceil(quantity - epsilon)
    else:
        quantity = math.floor(quantity + epsilon)
    
    Logme()('FCorpActionRounding RoundQuantity Rounded Quantity %+06.12f' %(quantity), 'INFO')
    return quantity


def RoundQuantityUp(quantity, decimals):
    Logme()('FCorpActionRounding RoundQuantityUp Initial Quantity %+06.12f' %(quantity), 'INFO')
    if quantity < 0:
        quantity = math.floor(quantity + epsilon)
    else:
        quantity = math.ceil(quantity - epsilon)
    
    Logme()('FCorpActionRounding RoundQuantity Rounded Quantity %+06.12f' %(quantity), 'INFO')
    return quantity
