from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FTranslator - Module to handle translation of strings 
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module is intended to translate ascii strings to other
    strings that may be utf8. It's primary use is within the reporting
    framework to do locale specific translations for report output.

VERSIONS

    2005-06-28 Daniel Roos - Production version in 3.2 originally as 
                             FDictionaryTranslator
    2008-07-03 Matthew Schaefer - Extended with Translator classes for use in 
                                  4.2 reporting as processing hook

----------------------------------------------------------------------------"""

import codecs
import re

class DictFileParseError( Exception ): pass

class FDictionaryTranslator( dict ):
    """Generate translation dictionary from file and/or arguments
    
        File format:
            Acceptable line forms:
              1. original_word --> translated_word (note --> can be changed in constructor )
              2. lines starting with # are comments
    """
    def __init__( self, translation_list=None, separator="-->", translation_dict=None ):
        """Initialize FDictionaryTranslator instance
        
        Arguments:
          translation_list  -- list of strings containing containing original_word <separator> translated_word pairs
          separator         -- separator used in file
          translation_dict  -- dictionary containing original_word:translated_word pairs

        """
        dict.__init__( self )
        self.translation_dict = translation_dict if translation_list != None else {}
        self.translation_list = translation_list if translation_list != None else [] 
        self.separator = separator
        self.freshen()
        
    def freshen( self ):
        """Reload dictionary data form file"""
        self.clear()
        self.update( self.translation_dict )
        firstline = True
        for linenum, linetext in enumerate( self.translation_list ):
            if firstline:                        
                linetext = linetext.lstrip( codecs.BOM_UTF8 )
                firstline = False
            linetext = linetext.strip()
            try:
                if len( linetext ) == 0 or linetext[ 0 ] == '#':
                    pass # ignore comments and blank lines
                else:
                    words = linetext.split( self.separator )
                    if len( words ) == 2:
                        fromword, toword = words[ 0 ].strip(), words[ 1 ].strip()
                        if fromword in self:
                            raise DictFileParseError( "Duplicate word" )
                        self[ fromword ] = unicode( toword, 'utf-8' )
                    else:
                        raise DictFileParseError( "Bad format" )
            except DictFileParseError as msg:
                print (msg)
                print ("   line=", linenum, "   text=", linetext)
        
class FMakeTranslator( object ):
    """Performs arbitrary substring substitions using from:to pairs in dictionary in a single pass"""
    
    def __init__( self, translation_dict ):
        self.translation_dict = translation_dict
        self.rx = self.make_rx()
    
    def make_rx( self ):
        return re.compile( '|'.join( map( re.escape, self.translation_dict ) ) )
    
    def one_xlat( self, match ):
        return self.translation_dict[ match.group(0) ]
    
    def __call__( self, text ):
        return self.rx.sub( self.one_xlat, text )

class FMakeTranslatorWholeWords( FMakeTranslator ):
    """Performs whole word substitions"""
    
    def make_rx( self ):
        return re.compile( r'\b%s\b' % r'\b|\b'.join( map( re.escape, self.translation_dict ) ) )




# Unit test code
if __name__ == '__main__':    

    testfilename = "c:\\dicttetfile.txt"
    f = open(testfilename, 'w')    
    f.write("# a comment\n")
    f.write("gris --> pig\n")
    f.write("anka -->   duck   \n")
    f.write("word with space   --> something else \n")
    f.write("a mallformed line\n")
    f.close()
    d = FDictionaryTranslator([testfilename])
    assert d['gris'] == 'pig'
    d.freshen()
    assert d['anka'] == 'duck'
    assert d['word with space'] == 'something else'

    f = open(testfilename, 'w')    
    f.write("# a comment\n")
    f.write("gris --> pig\n")
    f.write("anka -->   duck   \n")
    f.write("BOND1 -->   BANANA   \n")
    f.write("word with space   --> something else \n")
    f.write("a mallformed line\n")
    f.close()
    d = FDictionaryTranslator([testfilename])
    t = FMakeTranslatorWholeWords( d )
    out = t( "<BOND1>" )
    assert out == "<BANANA>"
    
    d = FDictionaryTranslator( translation_dict={ "BOND1" : "APPLE" } )
    t = FMakeTranslatorWholeWords( d )
    out = t( "<BOND1>" )
    assert out == "<APPLE>"
    print ("all passed")
