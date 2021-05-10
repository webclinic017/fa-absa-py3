""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/templates/FSwiftXMLTemplates.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftXMLTemplates

DESCRIPTION
    This module consists of a base XML template which is used in both
    Confirmation and Settlement XML templates.
    Changes to this module require a restart of both the
    Confirmation ATS and the Documentation ATS.
----------------------------------------------------------------------------"""

baseXML_template = '''
    <SWIFT file = "FSwiftMTBase">
        <acmInit function ='Init'/>
        <CODEWORD_NEWLINE><acmCode function ='GetCodewordNewline'/></CODEWORD_NEWLINE>
        <NARRATIVE_SEPARATOR><acmCode function ='GetNarrativeSeparator'/></NARRATIVE_SEPARATOR>
        <SWIFT_MESSAGE_TYPE><acmCode function ='GetSwiftMessageType'/></SWIFT_MESSAGE_TYPE>
        <VERSION><acmCode function ='GetVersion' ignoreUpdate ='True'/></VERSION>
    </SWIFT>
'''

def GetBaseXMLTemplate():
    return baseXML_template

