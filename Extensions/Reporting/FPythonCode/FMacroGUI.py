from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FMacroGUI - Open a GUI to enter Macro values

    (c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

DESCRIPTION


MAJOR REVISIONS
2007-05-18  Richard L   Open a new GUI for the ASQL macros.
-------------------------------------------------------------------------------------------------------"""
import acm
import ael
import re
import FLogger

logger = FLogger.FLogger('FAReporting')

import FRunScriptGUI
truefalse=('False', 'True')
def searchMacros(querytext):
    """FASQLReport Retrieve all macro names from the ASQL query. A dictionary ("set") is returned that contains the macro
    names as keys and all occurrences of the macros as values."""
    r = re.compile(r'.*?(/\*.*?\*/)', re.DOTALL) # Find comments
    for found in r.findall(querytext):
        querytext=querytext.replace(found, '') # And delete them

    p = re.compile(r"@[_\w{<>=~=;.,\-/'\[ &\*]*[}\]\Z]|"r"@[_\w]*")   # match complete macro
    ps = re.compile(r"@[_\w]*") #[ \r\n\[{]")                  # match only macro name
    set = {}
    macrosDict = [set.setdefault(ps.match(e).group()[1:], []).append(e) for e in p.findall(querytext)] #return a dictionary with macros
    return set

def getAelVariables(tabname):
    """ Get ael_variables that need to be suplied to generate macro GUI, scripts
        should extend their ael_variables with this list
    """
    return FRunScriptGUI.AelVariablesHandler([['macros', 'Macros'+tabname, 'string', [], None, 0, 0, 'FMACROGUI variable1=value:variable2=value', None, 1],
            ['useMacroGUI', 'Use Macro GUI'+tabname, 'string', truefalse, 'False', 1, 0, 'Should the extended Macro GUI be used?', None, 1]
            ])

def get_query_text(query_name):
    """FASQLReport Retrieve the SQL text for a named query, RETURNS None if query not found"""
    text_obj = ael.TextObject.read('type="SQL Query" and name="%s"' % query_name )
    if text_obj:
        return text_obj.get_text()
    else:
        return None


def split_macrostring(macrostring, macros):
    """Split a string like '@variable1=value1:@variable2=value2' or 'variable1=value1:variable2=value2' """
    for macro in macrostring.split(":"):
        try:
            mac, var=macro.split("=")
            mac=mac.strip()
            var=var.strip()
        except:
            mac=var=''
        if ',' in var:
            var=var.split(",")
            tmp=[]
            for v in var:
                v = v.strip()
                if v:
                    tmp.append(v)
            var=tmp
        if mac and var:
            if mac.startswith('@'): mac=mac[1:]
            macros[mac]=var

def listentries(macro):
    # FASQLReport Build the pulldown for the macro and return the values in a list
    rese=re.compile(r"(\w*)\.(\w*) ?(where .*)?")
    list=[]
    try:
        if macro.startswith(";"): macro=macro[1:]
        sel=rese.findall(macro)
        if sel:
            sel=sel[0]
            if sel[2]:
                asql="select distinct %s from %s %s order by 1"%(sel[1], sel[0], sel[2])
                asql=asql.replace('"', "'")
            else:
                asql="select distinct %s from %s order by 1"%(sel[1], sel[0])
            query=ael.asql(asql)
            list=[q[0] for q in query[1][0]]
        else:
            for le in macro.split(','):
                if le and le not in list:
                    eval("list.append(%s)"%le.strip())
    except Exception as e:
        logger.ELOG("Can not interpret choices: %s, %s", e, macro )
    return list

def valType(value):
    value = value.strip()
    try:
        if len(value) > 1 and value[0] == "'" and value.endswith("'"):
            return value
    except Exception:
        pass
        
    try:
        tmp = str(float(value))
        if tmp.endswith(".0"):
            tmp = tmp[:-2]
        return tmp
    except ValueError:
        pass

    asqlDates = ['bigdate', 'firstdayofmonth', 'firstdayofquarter', 'firstdayofweek',\
                'firstdayofyear', 'now', 'smalldate', 'today', 'tomorrow', 'yesterday', "''"]

    if value.isdigit() or value.lower() in asqlDates:
        return value
    else:
        return "'%s'"%str(value)# if macro value is non numeric include in quotes

def valTypeQuoted(value):
    v = valType(value)
    if len(v) > 0 and v[0] != "'" and not ael.is_asql_built_in(v):
        v = "'%s'" % v
    return v

def mapMacros(mInput, macs):
    """ FASQLReport Get all macro values from input and macro names from query and create two lists:
    valueList containing a list of all macro values in the same sequence as macro names will appear in
    macroList: this list contains all macro names, including names that occur more than once in the
    query source."""

    macroList=[]
    valueList=[]
    for mkey, mitems in macs.items():
        for m in mitems:
            if m not in macroList:
                macroList.append(m)
                valTypeFunc = valTypeQuoted if (m.find('{') > -1) else valType
                value=mInput[mkey]
                if isinstance(value, tuple) or isinstance(value, list) or (hasattr(value, 'IsKindOf') and value.IsKindOf(acm.FIndexedCollection)):
                    val=''
                    for en in list(value):
                        val=val + ',' + valTypeFunc(en)
                    value=val[1:]
                else:
                    value = valTypeFunc(value)

                valueList.append(value)
    return macroList, valueList

def macro_gui(query_name, defaults):
    """FASQLReport Build up ael_variables for the custom gui"""
    macro_variables=[]

    query_text = get_query_text(query_name)
    """ FCA1050
        Extended variable syntax:
            @VariableName{DefaultValue(s); TypeInformation}

        where the "DefaultValue(s)"-syntax is

            string [, string, string,...]

        and the "TypeInformation"-syntax is

            record.field[*][WHERE field = Value] | 'string'[, 'string','string',...][*]

        where "[]" means "optional" and an "*" makes it possible to make more than one
        selection (the value(s) chosen is/are appended).
    """

    df = re.compile(r"@[_\w]*?[{\[]([^;]*)(;?.*)[}\]]")
    if query_text:
        macros = searchMacros(query_text)
        rest=''
        for var, deff in macros.items():
            try:
                default=df.match(deff[0]).group(1)
            except:
                default=''

            if defaults.get(var, ''):
                default=defaults.get(var)

            if '[' in deff:
                strtype='int'
                default=int(default)
            else:
                strtype='string'

            if type(default) == type([]):
                default=','.join(default)
            #print ("def",default)

            try:
                rest=df.match(deff[0]).group(2)
                list=listentries(rest)
            except:
                list=''

            if '*' in rest:
                many=True
            else:
                many=False

            macro_variables.append( [var, var.replace('_', ' '), strtype, list, default, True, many, None, None, True] )
        #['InternalName','Gui Text_Context text','string',[True, False],True,None,False,'Ballon tips text.',callbackCb,None],
        #[0]=internal name                      [2]=object type       [4]=Default [6]=Multiple             [8]=callback
        #               [1]=GUI Text                      [3]=valid values   [5]=Mandatory [7]=Ballon tips              [9]=enabled/disabled
    macro_variables.sort()
    return macro_variables

def use_standard_macro_dialog(params, queryName, macros, function):
    fsql = acm.FSQL[queryName] if queryName else None
    if not fsql:
        return False

    if fsql.HasMacros():
        fInformationManagerQueryMacros = None
        providedMacros = acm.FInformationManagerQueryMacros()
        providedMacros.PopulateFromQuery(fsql)
        if macros:
            providedMacros.SetMacroValuesByName(macros)

        if params['useMacroGUI']=='True':
            shell = acm.UX.SessionManager().Shell()
            fInformationManagerQueryMacros = acm.UX.Dialogs().GetInformationManagerQueryMacros(shell, fsql, providedMacros)
            if not fInformationManagerQueryMacros:
                return True
        else:
            fInformationManagerQueryMacros = providedMacros

        queryMacros = fInformationManagerQueryMacros.GetMacroNames()
        if queryMacros:
            for m in queryMacros:
                # the macro name key must be a python string to work in the rest of the code
                macros[str(m)] = fInformationManagerQueryMacros.GetMacroValueByName(m)
            function(params, macros)
    else:
        function(params, None)        
    return True

def use_python_macro_gui(params, queryName, macros, function, block_rerun):
    global ael_variables, ael_gui_parameters
    macro_variables=macro_gui(queryName, macros)
    windowCaption='%s:Enter Macros'%queryName
    if block_rerun:
        for app in acm.ApplicationList():
            if str(app.StringKey()) == windowCaption:
                app.Activate()
                acm.Log("The MacroGUI is already open")
                return

    if not macro_variables:
        function(params, None)
    else:
        ael_variables=FRunScriptGUI.AelVariablesHandler (macro_variables)
        ael_gui_parameters = {
            'windowCaption':'%s:Enter Macros'%queryName,
            'runButtonLabel':'&&Run Report',
            'hideExtraControls':1 }

        acm.RunModuleWithParametersAndData( 'FMacroGUI', acm.GetDefaultContext(), (params, function))

def start_macro_gui(params,queryName,macros,function,block_rerun=False):
    if not use_standard_macro_dialog(params, queryName, macros, function):
        use_python_macro_gui(params, queryName, macros, function, block_rerun)

def ael_main_ex(macros, addData):
    """ run from the MacroGUI with the values filled"""
    aelvars, function=addData['customData']
    function(aelvars, macros)
