'''
Purpose:        Searches textobjects using a regular expression or normal search and prints
                out details about any matches.
Developer:      Paul Jacot-Guillarmod
CR Number:      518599

History
=======

Date            CR              Developer               Description
====            ======          ================        =============
2015-07-08     CHNG0002956652   Lawrence Mucheka        Added owner of the text object
2016-02-16     CHNG0003451385   Lawrence Mucheka        Fix search for asql associated trade filters

'''
import acm, ael
import re

def SearchText(label, name, text, pattern, regex, printLineNumbers=True):
    ''' Search text for a pattern and return list of matching lines.
    '''
    lines = text.splitlines()
    foundMatch = False     
    
    matches = []
    if printLineNumbers:
        blankLine = [' ', ' ', ' ', ' ']
    else:
        blankLine = [' ', ' ', ' ']
    
    for lineNumber, line in enumerate(lines):
        if (regex and pattern.search(line)) or (not(regex) and pattern in line):
            foundMatch = True
            if printLineNumbers:
                matches.append([label, name, lineNumber+1, line.strip()])
            else:
                matches.append([label, name, line.strip()])
    
    if foundMatch:
        matches.append(blankLine)
    return matches
    
def SearchTradeFilter(label, name, tradeFilter, pattern, regex):
    ''' Search the value of tradefilter rows for a pattern and return list of matching rows.
    '''

    foundMatch = False
    matches = []
    blankLine = [' ', ' ', ' ', ' ']
        
    ownerDescription = '[Not set]'
    owner = tradeFilter.Owner()
    if owner:
        ownerDescription = '[{0} ({1}) ({2})]'.format(owner.FullName(), owner.Name(), owner.UserGroup().Name() if owner.UserGroup() else '')  
   
    if tradeFilter.Filter():
        conditions = tradeFilter.FilterCondition() 
        for row in conditions:
            value = str(row[4])
            if value and ((regex and pattern.search(value)) or (not(regex) and pattern in value)):
                foundMatch = True
                matches.append([label, name, str(row), ownerDescription])
                
        if foundMatch:
            matches.append(blankLine)
        return matches
    else:
        return [blankLine]

def PrintTable(table):
    ''' Print a 2 dimensional array with columns formatted to be the same width.
    '''
    columnWidths = []
    # Use zip to transpose the table
    for row in zip(*table):
        columnWidths.append(max([len(str(element)) for element in row]))
        
    for row in table:
        print ' '.join([str(element).ljust(columnWidths[i]) for (i, element) in enumerate(row)])

ael_variables = [
    ['textObjectType', 'TextObject Type', 'string', ['Python Code', 'SQL Query', 'Extension Attribute', 'Trade Filter'], 'Python Code', 1, 0, 'TextObject Type', None, 1],
    ['searchPattern', 'Search Pattern', 'string', None, None, 1, 0, 'Search pattern', None, 1],
    ['regex', 'Regular Expression', 'string', ['Yes', 'No'], 'Yes', 1, 0, 'Match using a regular expression', None, 1]
]


def ael_main(parameters):
    textObject = parameters['textObjectType']
    searchPattern = parameters['searchPattern']
    isRegex = parameters['regex'] == 'Yes'
    
    if isRegex:
        pattern = re.compile(searchPattern)
    else:
        pattern = searchPattern
    
    matches = [['TextObject', 'Name', 'LineNumber', 'Text']]
    
    if textObject == 'Extension Attribute':
        matches = [['TextObject', 'Name', 'Text']]
        extensionAttributes = acm.FExtensionAttribute.Select('')
        extensionAttributes.Sort()
        
        for ea in extensionAttributes:
            text = ea.Blueprint()
            name = ea.Name()
            searchResults = SearchText('ExtensionAttribute', name, text, pattern, isRegex, False)
            if searchResults:
                matches.extend(searchResults)
    
    elif textObject == 'Trade Filter':
        matches = [['TextObject', 'Name', 'Filter Row', 'Owner']]
        tradeFilters = [(filter.Name(), filter) for filter in acm.FTradeSelection.Select('')]
        tradeFilters.sort()
        
        for name, tf in tradeFilters:
            # Tradefilter refers to deleted entities and causes fatal application error
            if name in ('IRP_All_Trades_Sales_Credit'):
                pass
            else:
                searchResults = SearchTradeFilter('TradeFilter', name, tf, pattern, isRegex)                
                if searchResults:                    
                    matches.extend(searchResults)
                    
    elif textObject == 'SQL Query':
        asqlQueries = [(query.Name(), query) for query in acm.FSQL.Select('')]
        asqlQueries.sort()
        
        for name, asql in asqlQueries:
            text = asql.Text()
            searchResults = SearchText('ASQL', name, text, pattern, isRegex, True)
            if searchResults:
                matches.extend(searchResults)
                    
    elif textObject == 'Python Code':
        ''' The extensions are looped through in hierarchical order and added to the dictionary.
            If the python module has been sub-classed at a lower level, then this code is used 
            instead of the code at a higher level.
        '''
        pyModules = {}
        for module in acm.GetDefaultContext().Modules():
            for py in module.GetAllExtensions('FPythonCode'):
                pyModules[py.Name().AsString()] = py.AsString()
        
        pythonModules = [(name, code) for name, code in pyModules.iteritems()]
        pythonModules.sort()
        
        for name, code in pythonModules:        
            searchResults = SearchText('FPythonCode', name, code, pattern, isRegex, True)
            if searchResults:
                matches.extend(searchResults)

        aelModules = [(aelCode.Name(), aelCode) for aelCode in acm.FAel.Select('')]
        aelModules.sort()
        
        for name, ael in aelModules:
            text = ael.Text()
            # ael modules also include some of the FPythonModules
            if name not in pyModules:
                searchResults = SearchText('AEL', name, text, pattern, isRegex, True)
                if searchResults:
                    matches.extend(searchResults)
    
    PrintTable(matches)
