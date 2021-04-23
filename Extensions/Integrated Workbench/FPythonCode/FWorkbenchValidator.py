""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FWorkbenchValidator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWorkbenchValidator

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

#pylint: disable-msg=E1101

import acm
from FParameterValidator import ParameterValidator, ParameterTreeValidator
from FHandler import Handler
import FPanel
import FSheetPanel
import FWorkbookPanel
import FMultiSheetPanel


class WorkbenchValidator(ParameterTreeValidator):

    DO_NOT_EXPAND = ('Commit', 'Name', 'Dispatcher', 'Type')


    sourceDict = {'Workbench':['Workbench'],
                  'Handlers':['Handler'],
                  'Views':['View'],
                  'DockWindows':['TabbedPanel', 'Panel', 'SheetPanel', 'MultiSheetPanel'],
                  'DefaultPanel':['Panel', 'SheetPanel', 'MultiSheetPanel'],
                  'Main':['WorkbookPanel'],
                  'Sheets':['Sheet']
                 }
    sourceDict['PositionRelativeTo'] = sourceDict['DockWindows']


    @classmethod
    def ValidateRecursively(cls, parameter, rootSource='Workbench'):
        return super(WorkbenchValidator, cls).ValidateRecursively(parameter, rootSource)



    @classmethod
    def GetType(cls, parameter):
        if isinstance(parameter, (str)):
            return 'StringData'
        elif isinstance(parameter, (int)):
            return 'IntData'
        elif isinstance(parameter, (bool)):
            return 'BoolData'
        else:
            if not hasattr(parameter, 'ValidationType'):
                return None
            elif isinstance(parameter.ValidationType(), str):
                return parameter.ValidationType()
            else:
                return parameter.ValidationType().Name()

    @classmethod
    def ValidTypesForSource(cls, sourceChain):
        lastSource = sourceChain[-1]
        try:
            return WorkbenchValidator.sourceDict[lastSource]
        except KeyError:
            return None

    @classmethod
    def ValidateStringData(cls, _):
        return []

    @classmethod
    def ValidateIntData(cls, _):
        return []

    @classmethod
    def ValidateBoolData(cls, _):
        return []

    @classmethod
    def ValidateWorkbench(cls, parameter):
        errors = cls._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))

        errors.extend(WorkbenchValidator._ValidateListAttribute(parameter, 'Views', allowEmpty=False, required=True))
        errors.extend(WorkbenchValidator._ValidateListAttribute(parameter, 'Handlers', allowEmpty=True, required=True))
        return errors

    @classmethod
    def ValidateView(cls, parameter):
        errors = cls._ErrorList(parameter, None)

        if not hasattr(parameter, 'Application'):
            errors.AddError('Views requires an "Application" attribute')
        else:
            if not parameter.Application() in cls._StartableApplications():
                errors.AddError('The application attribute needs to be a startable prime application')

        errors.extend(ParameterValidator._ValidateListAttribute(parameter, 'DockWindows',
                                                                allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Main',
                                                            allowEmpty=False, required=True))
        return errors

    @classmethod
    def ValidateHandler(cls, parameter):
        errors = cls._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))
        errors.extend(WorkbenchValidator._ValidateModule(parameter, Handler, allowEmpty=False, required=True))
        return errors

    @classmethod
    def ValidatePanel(cls, parameter):
        errors = cls._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Type',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Caption', allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Position',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'ShowInitially',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'PositionRelativeTo',
                                                            allowEmpty=False, required=False))
        errors.extend(WorkbenchValidator._ValidateModule(parameter, FPanel.Panel,
                                                         allowEmpty=False, required=True))

        return errors

    @classmethod
    def ValidateTabbedPanel(cls, parameter):
        errors = ParameterValidator._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Type',
                                                            allowEmpty=False, required=True))

        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Position',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'PositionRelativeTo',
                                                            allowEmpty=False, required=False))

        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'DefaultPanel',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateListAttribute(parameter, 'DockWindows',
                                                                allowEmpty=False, required=True))
        return errors

    @classmethod
    def ValidateSheetPanel(cls, parameter):
        errors = ParameterValidator._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))
        errors.extend(cls.ValidatePanel(parameter))
        errors.extend(cls._ValidateColumns(parameter, 'Columns', 'SheetType',
                                           allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Grouper',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'SheetTemplate',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'SheetType',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Type',
                                                            allowEmpty=True, required=True))
        errors.extend(WorkbenchValidator._ValidateModule(parameter, FSheetPanel.SheetPanel,
                                                         allowEmpty=False, required=False))

        return errors

    @classmethod
    def ValidateMultiSheetPanel(cls, parameter):
        errors = ParameterValidator._ErrorList(parameter, None)
        errors.extend(cls._ValidateSelfIsFParameter(parameter))
        errors.extend(cls.ValidatePanel(parameter))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Type',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateListAttribute(parameter, 'Sheets',
                                                                allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Orientation',
                                                            allowEmpty=True, required=True))
        # FIX enum check
        errors.extend(WorkbenchValidator._ValidateModule(parameter, FMultiSheetPanel.MultiSheetPanel,
                                                         allowEmpty=True, required=True))
        return errors

    @staticmethod
    def ValidateWorkbookPanel(parameter):
        errors = ParameterValidator._ErrorList(parameter, None)
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Type',
                                                            allowEmpty=True, required=True))
        errors.extend(WorkbenchValidator._ValidateModule(parameter, FWorkbookPanel.WorkbookPanel,
                                                         allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'IsShared',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Workbook',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateListAttribute(parameter, 'Sheets',
                                                                allowEmpty=False, required=True))

        return errors

    @staticmethod
    def ValidateSheet(parameter):
        errors = ParameterValidator._ErrorList(parameter, None)
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Columns',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'Grouper',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'SheetTemplate',
                                                            allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'SheetType',
                                                            allowEmpty=False, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'IsShared', allowEmpty=True, required=True))
        errors.extend(ParameterValidator._ValidateAttribute(parameter, 'IncludeRows',
                                                            allowEmpty=True, required=True))
        return errors

    @classmethod
    def _ValidateSelfIsFParameter(cls, parameter):
        errors = cls._ErrorList(parameter, None)
        if isinstance(parameter, str):
            errors.AddError('Value "{0}" needs a FParameter'.format(parameter))
        return errors



    @classmethod
    def _ValidateColumns(cls, parameter, attributeName='Columns', sheetTypeAttribute=None, allowEmpty=True, required=True):
        errors = ParameterValidator._ErrorList(parameter, None)
        if required and not hasattr(parameter, attributeName):
            errors.AddError('{0} parameter requires "{1}"'.format(parameter.Name(), attributeName))
            return errors
        attribute = getattr(parameter, attributeName)()
        if not isinstance(attribute, str):
            attribute = attribute.Name()
        sheetTypeName = None
        if hasattr(parameter, sheetTypeAttribute):
            sheetTypeName = getattr(parameter, sheetTypeAttribute)
        if not allowEmpty and not attribute == '':
            context = acm.GetDefaultContext()
            try:
                sheetTypeClass = getattr(acm, sheetTypeName)
            except AttributeError:
                errors.AddError('Invalid sheet type "{0}"'.format(sheetTypeName))
                return errors
            columnExtension = context.GetExtension(acm.FExtensionAttribute, sheetTypeClass, attribute)
            if columnExtension is None:
                errors.AddError('Cant find FExtensionAttribute "{0}:{1}"'.format(sheetTypeName, attribute))
        return errors

    @staticmethod
    def _ValidateModule(parameter, baseClass=None, allowEmpty=False, required=True):
        errors = ParameterValidator._ErrorList(parameter, None)
        if not required and not hasattr(parameter, 'Module'):
            return errors
        if required and not hasattr(parameter, 'Module'):
            errors.AddError('{0} parameter requires "Module"'.format(parameter.Name()))
            return errors
        if allowEmpty and parameter.Module() == '':
            return errors
        module = None
        try:
            moduleName = parameter.Module()
            module = __import__(moduleName)
        except Exception:
            errors.AddError('Unable to load Module {0}'.format(moduleName))
            return errors
        classPointer = None
        try:
            classPointer = getattr(module, parameter.Name())
        except AttributeError:
            errors.AddError('Module {0} needs to include class named {1}'.format(moduleName, parameter.Name()))
            return errors
        if not issubclass(classPointer, baseClass):
            errors.AddError('Class {0} needs to be an instance of {1}'.format(parameter.Name(), baseClass.__name__))
        return errors

    @classmethod
    def _StartableApplications(cls):
        startableApplications = []
        for appName in acm.GetDomain('enum(ApplicType)').Enumerators().Sort():
            if acm.UX().SessionManager().IsStartableApplication(appName):
                startableApplications.append(appName)
        return startableApplications
