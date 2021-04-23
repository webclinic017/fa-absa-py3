"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportSheetSettingsTab - Functions used by worksheet reports.
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import ael
import datetime
import re
import time
import FLogger

logger = FLogger.FLogger( 'FAReporting' )

import FRunScriptGUI

falseTrue = ['False','True']

# Python3: xrange does not exist in python3.
try:
    xrange
except NameError:
    xrange = range

class SheetSettingsTab(FRunScriptGUI.AelVariablesHandler):
    def updateAelVariables( self, index, fieldValues, sheetType ):
        """enable/disable sheet settings"""
        num_settings = len( [ item for item in self.ael_variables if item[ 0 ].startswith( sheetType ) ] )
        for idx in range( index + 1, index + num_settings ):
            self.ael_variables[ idx ][ FRunScriptGUI.Controls.ENABLED ] = falseTrue.index( fieldValues[ index ] )
        
    def portfolioSheetSettingsCB( self, index, fieldValues ):
        """disable/enable all sheet settings on tab"""
        if ( self.ael_variables ):
            self.updateAelVariables( index, fieldValues, 'FPortfolioSheet' )
        return fieldValues
    
    def tradeSheetSettingsCB( self, index, fieldValues ):
        """disable/enable all sheet settings on tab"""
        if ( self.ael_variables ):
            self.updateAelVariables( index, fieldValues, 'FTradeSheet' )
        return fieldValues

    def timeSheetSettingsCB( self, index, fieldValues ):
        """disable/enable all sheet settings on tab"""
        if ( self.ael_variables ):
            self.updateAelVariables( index, fieldValues, 'FTimeSheet' )
        return fieldValues
    
    def __init__(self, sheetSettingsBySheetType, sheetType, context, buildVariables):
        tabName = ''.join( [ 'Override Sheet Settings', '_', getSplitSheetType( sheetType ), ' Settings' ] )
        enableSheetSettings = [ '%s_overrideSheetSettings' % sheetType, tabName, 'string', falseTrue, False, 1, 0, 'Override saved sheet settings', None, 1 ]
        guiVariables=[]
        for sheetType, sheetSettings in sheetSettingsBySheetType.items():
            if sheetType == 'FPortfolioSheet':
                enableSheetSettings[ FRunScriptGUI.Controls.CB ] = self.portfolioSheetSettingsCB
            elif sheetType == 'FTradeSheet':
                enableSheetSettings[ FRunScriptGUI.Controls.CB ] = self.tradeSheetSettingsCB
            elif sheetType == 'FTimeSheet':
                enableSheetSettings[ FRunScriptGUI.Controls.CB ] = self.timeSheetSettingsCB
            else:
                logger.ELOG( 'sheet setting for sheet type < %s > not supported.' , sheetType )
                continue
            guiVariables.append( enableSheetSettings ) 
            for mangledColumnName, settingsGroup, column, defaultColumnValue, columnChoices in sheetSettings:
                if buildVariables:
                    guiVariables.append( [  mangledColumnName, 
                                            ''.join( [ str( settingsGroup ), ': ', str( column.ColumnName() ), '_', getSplitSheetType( sheetType ), ' Settings' ] ), 
                                            'string', 
                                            columnChoices, 
                                            defaultColumnValue,
                                            0,
                                            0,
                                            column.ColumnDescription(),
                                            None,
                                            0
                                          ]
                                        )

        FRunScriptGUI.AelVariablesHandler.__init__(self,guiVariables,__name__)

def getSheetSettingsBySheetType( sheetType, context ):
    """get default values and choices for sheet settings"""
    
    sheetSettingsBySheetType = { sheetType : [] }
    
    sheetDefinition = acm.Sheet().GetSheetDefinition(sheetType)
    
    settingsDialog = sheetDefinition.GetSheetSettingsSimpleFormat()
        
    for settingsGroup in settingsDialog.Keys():
        for columnId in settingsDialog[ settingsGroup ]:
            defaultColumnValue = ''
            columnChoices = None
            columns = acm.GetColumns( [ columnId ], sheetType, context )
            
            if not columns:
                continue
            column = columns[ 0 ]
            
            if column.ColumnName() in settingsDialog.Keys(): #skip group names
                continue
            
            if hasattr( column.Formatter(), 'Enumeration' ):
                columnChoices = column.Formatter().Enumeration().Enumerators()
            else:
                choicesEvaluator = column.ChoiceListSource( None, acm.CreateEBTag() )
                if choicesEvaluator:
                    columnChoices = choicesEvaluator.Value()
            
            defaultColumnValue = ''
            mangledColumnName = ''.join( [ sheetType, '_', str( column.ColumnId() ) ] )
            element_value = ( mangledColumnName, settingsGroup, column, defaultColumnValue, columnChoices )
            sheetSettingsBySheetType[ sheetType ].append( element_value )
    return sheetSettingsBySheetType

def getAelVariables( sheetTypes, context, buildVariables=True ):
    """transform sheet settings info into GUI ael variables""" 
    
    allGuiVariables = []
    allSheetSettingsBySheetType = {}
    for sheetType in sheetTypes:
        guiVariables, sheetSettingsBySheetType = getSheetSettingsVariablesBySheetType( sheetType, context, buildVariables )
        allSheetSettingsBySheetType.update( sheetSettingsBySheetType )
        allGuiVariables.append( guiVariables )
    return allGuiVariables, allSheetSettingsBySheetType

def getChoiceString( choice ):
    """return string representation of choice"""
    if hasattr( choice, 'StringKey'):
        return choice.StringKey()
    else:
        return str( choice )

def getSelectedSheetSettings( allSheetSettingsBySheetType, params ):
    """transform users choices for settings into settings dictionary"""
    
    #obtain setting values to be simulated based on default values and user overrides
    selectedSheetSettingsBySheetType = {}
    for sheetType, sheetSettings in allSheetSettingsBySheetType.items():
        selectedSheetSettings = {}
        for mangledColumnName, settingsGroup, column, defaultColumnValue, columnChoices in sheetSettings:
            columnId = str( column.ColumnId() )
            choice = None
            fieldValue = params.get( mangledColumnName )
            if columnChoices:
                columnChoices = [ getChoiceString( choice ) for choice in columnChoices ]
                try:
                    index = columnChoices.index( fieldValue )
                except ValueError as e:
                    index = -1
                if index != -1:
                    choice = columnChoices[ index ]
                else:
                    continue
            else:
                choice = params.get( mangledColumnName )
            selectedSheetSettings[ columnId ] = choice
        selectedSheetSettingsBySheetType[ sheetType ] = selectedSheetSettings
    return selectedSheetSettingsBySheetType 
    
def getSheetSettingsVariablesBySheetType( sheetType, context, buildVariables=True ):
    """transform sheet settings info into GUI ael variables"""
    sheetSettingsBySheetType = getSheetSettingsBySheetType( sheetType, context )
    guiVariables = SheetSettingsTab(sheetSettingsBySheetType,sheetType, context, buildVariables)
    guiVariables.LoadDefaultValues(__name__)
    return guiVariables, sheetSettingsBySheetType

def getSplitSheetType( sheetType ):
    """return sheet type as a string split into two parts: 'foo Sheet'"""
    strArray = re.split( '(Sheet)', sheetType[ 1: ] )
    if len( strArray ) >= 2:
        return strArray[ 0 ] + ' ' + strArray[ 1 ]
    else:
        return strArray

