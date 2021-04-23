from __future__ import print_function
"""----------------------------------------------------------------------------
Module
    FRunScriptGUI - Module with code used by the run script gui.

    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.
    
DESCRIPTION
    Create a run script gui without callback's, loading and saving default values from/to FParameters:

        import FRunScriptGUI
        ael_variables=FRunScriptGUI.AelVariablesHandler([['first','string','string', None, '', 1, 0, 'Enter a string?', None, 1],
                                                            ['save','Save defaults','int',[True,False],False,1,0,'Save the default values?',None,True]])
        ael_variables.LoadDefaultValues(__name__)
        def ael_main(parameters):
            if parameters['save']:
                FRunScriptGUI.SaveDefaultValues(__name__,parameters,['save']) # save all parameters but the "Save defaults" checkbox.
            print (parameters)

    Create a run script gui with callback:

        import FRunScriptGUI

        class MyRunScript(FRunScriptGUI.AelVariablesHandler):
            def callback(self,index, fieldValues):
                print (fieldValues[index])
                return fieldValues
            def __init__(self):
                vars=[['first','On Off','string', [1,0], 0, 1, 0, 'Should it be turned on?', self.callback, 1]]
                FRunScriptGUI.AelVariablesHandler.__init__(self,vars)

        ael_variables=MyRunScript()

        def ael_main(parameters):
            print (parameters)

----------------------------------------------------------------------------"""
import acm

class Controls( object ):
    NAME                 = 0 #internal name
    TEXT                 = 1 #GUI Text
    TYPE                 = 2 #object type
    VALUES               = 3 #valid values
    DEFAULT              = 4 #default
    MANDATORY            = 5 #mandatory
    MULTI                = 6 #multiple selection
    TIP                  = 7 #floating tip
    CB                   = 8 #callback
    ENABLED              = 9 #enabled
    
class AelVariablesHandler(list):

    class Variable(list):
        """ Wrapper class for an ael variable. """
        def __init__(self, r, i):
            self[:] = r
            self.sequenceNumber = i
            self.mandatory = ((len(r) <= Controls.MANDATORY) or r[Controls.MANDATORY])
            self.oldTooltip = (len(r) > Controls.TIP) and r[Controls.TIP] or ''

        def isEnabled(self):
            try:
                return self[Controls.ENABLED]
            except IndexError:
                return 1

        def isMandatory(self):
            return self[Controls.MANDATORY]

        def hasCallback(self):
            try:
                return self[Controls.ENABLED]
            except IndexError:
                return False

        def enable(self, enabled, disabledTooltip=None):
            enabled = enabled and enabled != '0' and 1 or 0
            old_enabled = len(self) > Controls.ENABLED and self[Controls.ENABLED]
            try:
                self[Controls.ENABLED] = enabled
            except IndexError:
                while len(self) < 10:
                    # Need to add some entries to be able to set the 9:th.
                    self.append(None)
            self[Controls.ENABLED] = enabled
            self[Controls.MANDATORY] = self.mandatory and enabled and self.mandatory
            if enabled:
                    self[Controls.TIP] = self.oldTooltip
            else:
                if old_enabled:
                    self.oldTooltip = self[Controls.TIP]
                self[Controls.TIP] = disabledTooltip

        def set(self, fieldValues, value):
            fieldValues[self.sequenceNumber] = value
            return fieldValues

        def callback(self, fieldValues):
            return self[Controls.CB](self.sequenceNumber, fieldValues)

        def callbackIfEnabled(self, fieldValues):
            if self.isEnabled() and self.hasCallback():
                return self.callback(fieldValues)
            return fieldValues

    def LoadDefaultValues(self,*names):
        for FParameter in names:
            p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', FParameter)
            try:
                template = p.Value()
            except AttributeError:
                continue
            for k in template.Keys():
                k = str(k)
                if hasattr(self, k):
                    row=getattr(self, k)
                    if type(row[Controls.TYPE]) == type(acm.FFileSelection()):
                        if row[Controls.TYPE].PickDirectory():
                            row[Controls.TYPE].SelectedDirectory=str(template.At(k))
                        else:
                            if str(template.At(k)).endswith(('\\', ':')) or '/' in str(template.At(k)):
                                row[Controls.TYPE].SelectedFile=''
                            else:
                                row[Controls.TYPE].SelectedFile=str(template.At(k))
                    else:
                        row[4]=str(template.At(k))

    def FileSelectionCB(self, index, fieldValues):
        """ Set the internal Selected[Directory|File] in the FFileSelection object, this way the [...] button
            stays in sync with the textfield """
        row=self.ael_variables[index]
        try:
            if row[Controls.TYPE].PickDirectory():
                row[Controls.TYPE].SelectedDirectory=str(fieldValues[index])
            else:
                if str(fieldValues[index]).endswith(('\\', ':')) or '/' in str(fieldValues[index]):
                    row[Controls.TYPE].SelectedFile=''
                else:
                    row[Controls.TYPE].SelectedFile=str(fieldValues[index])
        except AttributeError:
            pass
        return fieldValues
    
    def createVariable(self, row):
        """ Factory of Variables. """
        row = self.Variable(row, len(self))
        if hasattr(self, row[Controls.NAME].replace(' ', '_')):
            raise LookupError("RunScriptGUI Variable %s does already exist"%row[Controls.NAME].replace(' ', '_'))
        setattr(self, row[Controls.NAME].replace(' ', '_'), row)
        # If no Callback set, set the default FileSelectionCB
        if len(row) > 8 and not row[Controls.CB] and type(row[Controls.TYPE]) == type(acm.FFileSelection()):
            row[Controls.CB]=self.FileSelectionCB

        self.append(row)
        return row

    def getParams(self):
        params={}
        for row in self.ael_variables:
            params[row[Controls.NAME]]=row[Controls.DEFAULT]
        return params
        
    def add(self, ael_variables):
        for row in ael_variables:
            self.createVariable(row)

    def extend(self, ael_tab):
        for row in ael_tab:
            if hasattr(self, row[Controls.NAME].replace(' ', '_')):
                raise LookupError("RunScriptGUI Variable %s does already exist"%row[Controls.NAME].replace(' ', '_'))
            setattr(self, row[Controls.NAME].replace(' ', '_'), row)
        list.extend(self, ael_tab)
        setattr(ael_tab, 'ael_variables', self)
        #ael_variables.ael_variables = self

    def __init__(self, ael_variables, name='FRunScriptGuiParameters'):
        for row in ael_variables:
            self.createVariable(row)
        setattr(self, 'ael_variables', self)
        self.name = name

def SaveDefaultValues(name,parameters,ignore=None):
    context = acm.GetDefaultContext()
    updateString = None
    for key, val in parameters.iteritems():
        if not ignore or (key not in ignore):
            if type(val) == type([]) or type(val) == type(()):
                val=",".join(val)
            if not updateString:
                updateString = "FObject:%s =\n" % (name)
            updateString+="%s=%s\n"%(key.replace(' ', '_'), val)
    if updateString:
        context.EditImport('FParameters', updateString)
        module = context.EditModule()
        module.Commit()

defaultFileFilter="XML Files (*.xml)|*.xml|CSV Files (*.csv)|*.csv|Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"

def InputFileSelection(FileFilter=defaultFileFilter):
    # Prepare selection for retrieving an existing file
    input_file_selection = acm.FFileSelection()
    input_file_selection.FileFilter = FileFilter
    input_file_selection.PickExistingFile(True)
    return input_file_selection

def OutputFileSelection(FileFilter=defaultFileFilter):
    # Prepare selection for getting filename to save to
    output_file_selection = acm.FFileSelection()
    output_file_selection.FileFilter = FileFilter
    output_file_selection.PickExistingFile(False)
    return output_file_selection

def DirectorySelection():
    # Prepare selection for retrieving a directory
    dir_selection = acm.FFileSelection()
    dir_selection.PickDirectory(True)
    return dir_selection

def runScriptValue(field):    
    """ Return value on form suitable for displaying in Run Script GUI. """
    if hasattr(field, 'IsKindOf') and field.IsKindOf('FArray'):
        return field.AsString().replace(']', '').replace('[', '').replace('\'', '')        
    else:
        return None
