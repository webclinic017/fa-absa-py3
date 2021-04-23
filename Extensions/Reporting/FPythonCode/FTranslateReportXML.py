"""----------------------------------------------------------------------------
MODULE
    FTranslateReportXML - Module to handle translation of strings 
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module contains a post XML processing hook used
    within the reporting framework to do locale specific translations 
    for report output.

VERSIONS

    2008-07-03 Matthew Schaefer -   Production version for use in 4.2 reporting 
                                    as processing hook

----------------------------------------------------------------------------"""

import traceback
import acm
import FDictionaryTranslator

translation_dict = {} # { 'ThVal' : "&#22823;&#23478;&#22909;" }

def get_translation_list():
    translations = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', 'TranslationFile' )
    if not translations:
        raise Exception( 'Extension value TranslationFile does not exist!' )
    translation_list = translations.Value().split('\n')
    return translation_list

def translate_xml( report, report_params, xml_string ):
    try:
        xml_string = xml_string.replace( '\xa0', ' ' )  #codecs and unicode() can't handle non-breaking spaces
        d = FDictionaryTranslator.FDictionaryTranslator( translation_list=get_translation_list(), translation_dict=translation_dict )
        t = FDictionaryTranslator.FMakeTranslatorWholeWords( d )
        xml_string = t( xml_string )
    except Exception as e:
        traceback.print_exc()
        raise e
    return xml_string

