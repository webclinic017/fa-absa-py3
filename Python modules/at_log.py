'''
Created on 22 Feb 2016

@author: conicova
'''
from datetime import datetime

DEBUG = False

def log(msg, is_debug=True, print_call_stack=False):
    ''' This method is used for printing log messages.'''  
    print_msg = False
    if not is_debug:
        print_msg = True
    elif DEBUG:
        print_msg = True
    
    if print_msg:
        date_txt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print("{0}: {1}".format(date_txt, msg))
        
    if print_call_stack:
        _call_stack()

def _call_stack():
    '''Print the call stack'''
    import traceback
    for line in traceback.format_stack():
        print((line.strip()))