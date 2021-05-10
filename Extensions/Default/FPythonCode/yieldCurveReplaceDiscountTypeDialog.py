
from ReplaceDiscountTypeBase import show
from ReplaceDiscountTypeBase import main

def ael_custom_dialog_show( shell, params ):
    return show( shell, params )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    return main( parameters, dictExtra, 'yield curve discounting type' )
