
"""-------------------------------------------------------------------------------------------------------
MODULE
    Frpdb2 - Wrapper module for rpdb2.py module. Used for embedded debugging in PRIME using the Winpdb 
    debugger ( www.winpdb.org ). Function source_provider_ads is designed to be used as a callback function
    for the source_provider parameter for rpdb2.start_embedded_debugger. It returns source code for 
    FPythonCode and FAel modules. In addition Frpdb2 overriddes the function winlower so that module
    names are not modified.
    
-------------------------------------------------------------------------------------------------------"""

import os
import acm

def winlower( path ):
    """dummy winlower to force rpdb2 to leave filename as is"""
    return path

import rpdb2
rpdb2.winlower = winlower
from rpdb2 import *

class FPythonCodeNotFoundError( Exception ): pass
class FAelModuleNotFoundError( Exception ): pass

def get_fpython_code_source( modulename ):
    ext = acm.GetDefaultContext().GetExtension( "FPythonCode", "FObject", modulename )
    if not ext:
        raise FPythonCodeNotFoundError( "FPython code not found" )
    source = trim_source( ext.AsString() )
    return source
	
def trim_source( source ):
    declarationIndex = source.find( '\n' ) + 1
    source = source[ declarationIndex: ]
    source = source.replace( "\n¤","" )
    source = source.replace( "...","" ) 
    return source

def get_fael_module_source( modulename ):
    module = acm.FAel[ modulename ]
    if not module:
        raise FAelModuleNotFoundError( "Ael Module not found" )
    source = module.Text()
    return source

def get_module_name( filename ):
    filename = str( filename )
    splitname = filename.split( '/' )
    if len( splitname ) == 2 and splitname[ 0 ][ 0 ] == "[" and splitname[ 0 ][ -1 ] == "]":
        context_info, modulename = splitname
    else:
        modulename = filename
    return modulename

def source_provider_ads( filename ):
    modulename = get_module_name( filename )
    acm.Log( "Winpdb searching for source in < %s >" % ( modulename ) ) 
    source = "" 
    try:
        source = get_fpython_code_source( modulename ) 
    except FPythonCodeNotFoundError as err:
        try:
            source = get_fael_module_source( modulename )
        except FAelModuleNotFoundError as err:
            f = None
            try:
                modulename = os.path.normpath( modulename )
                f = open( modulename, "r" )
                source = f.read()
            except IOError as err:
                raise IOError( SOURCE_NOT_AVAILABLE )
            finally:
                if f:
                    f.close()
    return source 

def debug_prime( password ):
    start_embedded_debugger( password, source_provider=source_provider_ads )
