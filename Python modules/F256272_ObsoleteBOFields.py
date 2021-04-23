"""----------------------------------------------------------------------------
MODULE
    F256272_ObsoleteBOFields
	
    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This AEL module scans all ASQL queries and AEL modules for references to
    fields in the Trade, SettleInstruction and Account tables that have become
    obsolete following FRONT ARENA 2.0 and 2.1.

    The obsolete fields are defined in three lists at the top of the module:
    tradeFields, settleFields and accountFields.

    By setting the printLineNumber variable to 1, the line for which a match
    has been found is printed together with the line number.

    It is possible to search only one specified ASQl query or AEL module by
    defining the searchThisModule variable.
    
----------------------------------------------------------------------------"""
import ael, re

#### Customizable variables ####
printLineNumber = 0
searchThisModule = ''

tradeFields = ['rec1_accnbr', 'rec2_accnbr', 'pay1_accnbr', 'pay2_accnbr']
settleFields = ['money_us_accnbr', 'money_cp_accnbr', 'sec_us_accnbr',
                'sec_cp_accnbr']
accountFields = ['depository2', 'depository3', 'depository4',
		 'swift2', 'swift3', 'swift4']

#### End of customizable variables ####

def codeModules(tType='AEL'):
    if tType=='AEL': altType = 'AEL Module'  # Changed name in FRONT ARENA 2.1
    else: altType = ''
    try:
        codemods = ael.TextObject.select('type="%s"'%tType)
        if not codemods: ael.TextObject.select('type="%s"'%altType)
    except: 
        codemods = ael.TextObject.select("type='%s'"%altType)
    return codemods

def asqlModules():
    return codeModules('SQL Query')

def aelModules():
    return codeModules('AEL')

def searchTextObject(astring,mods=aelModules,linnbr=0,mod=''):
    'Search through all text code for all of a certain string'

    found = 0
    strcmp = re.compile('.*'+astring+'.*')
    for to in mods():
	if mod and to.name != mod: continue
	txt = to.get_text()
	if strcmp.search(txt):
            if not found:
                print 'Reference to', astring, 'found in:'
                found = 1
	    print '---', to.name
	    if linnbr:
	    	n=0
	    	txtmass = txt.split('\n')
		for line in txtmass:
		    n=n+1
		    if strcmp.search(line):
		    	print '%3d:'%n, line
    if not found:
        print 'No reference to', astring, 'found'


print 40*'-'
for (name, table) in [('Trade', tradeFields), ('SettleInstruction', settleFields),
                     ('Account', accountFields)]:
    for (typ, mods) in [('ASQL', asqlModules), ('AEL', aelModules)]:
        if searchThisModule != '':
            print 'Searching', searchThisModule, 'for obsolete', name, 'fields'
        else:
            print 'Searching', typ, 'modules for obsolete', name, 'fields'
        for field in table:
            searchTextObject(field, mods, printLineNumber, searchThisModule)
        print 40*'.'
print 'Done.'
