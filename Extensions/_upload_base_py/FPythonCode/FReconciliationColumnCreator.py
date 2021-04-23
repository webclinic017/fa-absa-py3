""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationColumnCreator.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationColumnCreator -

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import string
import collections

import acm
import FAssetManagementUtils
import FReconciliationDataTypeHandler

logger = FAssetManagementUtils.GetLogger()

def MakeColumnId(name, namespace):
    return ' '.join((str(namespace), str(name))).translate(None, '=')

class ExtensionObject(object):

    TYPE = r'FExtensionAttribute'
    TEMPLATE = '%s:%s=\n%s\n'

    def __init__(self, name, className='FObject', isMethodColumn=False, value=None):
        self._name = name
        self._className = className
        self._isMethodColumn = isMethodColumn
        self._value = value

    def __str__(self):
        return self.Definition()

    def Name(self):
        return self._name

    def ExtensionType(self):
        return self.TYPE

    def ClassName(self):
        return self._className
        
    def IsMethodColumn(self):
        return self._isMethodColumn

    def Definition(self):
        return self.TEMPLATE % (self.ClassName(), self.Name(), self._GetValue())

    @staticmethod
    def BuildAttributeName(name, namespace=''):
        # Attribute name is camelcase with punctuation and spaces removed
        attributeName = namespace + name
        assert(attributeName)
        attributeName = attributeName[0].lower() + attributeName[1:]
        return attributeName.translate(None, string.punctuation + ' ')
        
    def _GetValue(self):
        return self._value

    def Groups(self):
        return []
        

class InternalExtensionAttribute(ExtensionObject):
    """Represents a Front Arena extension attribute"""

    TYPE = 'FExtensionAttribute'

    def __init__(self, name, className, sheetType, columnId, existingExtAttr):
        super(InternalExtensionAttribute, self).__init__(name, className)
        self._sheetType = sheetType
        self._columnId = columnId
        self._existingExtAttr = existingExtAttr
        
    def ClassName(self):
        className = super(InternalExtensionAttribute, self).ClassName()
        if className == 'FPortfolioInstrumentAndTrades':
            return 'FInstrumentAndTrades' #
        return className
        
    def _GetValue(self):
        if self.ClassName() == 'FBusinessProcess':
            fields = [
                'py("FReconciliationColumns", context).',
                'GetAttributeFromCalcSpace(object,',
                '"%s",' % self._sheetType,
                '"%s")' % self._columnId
                ]
            return ''.join(fields)
        else:
            fields = ["%s" % self._existingExtAttr]
            return ''.join(fields)

class ExternalExtensionAttribute(ExtensionObject):
    """Represents an external extension attribute"""

    TYPE = 'FExtensionAttribute'
    SUFFIX = 'External'

    def __init__(self, name, namespace, className):
        attributeName = self.BuildAttributeName(name, ''.join((namespace, self.SUFFIX)))
        super(ExternalExtensionAttribute, self).__init__(attributeName, className)
        self._attributeName = name
        
    def _GetValue(self):
        fields = [
            'py("FReconciliationColumns",',
            'context).',
            'GetAttributeFromExternalValues(',
            'object,',
            '"%s")' % self._attributeName
            ]
        return ''.join(fields)
        
class AbsoluteExtensionAttribute(ExtensionObject):
    """Represents an extension attribute for absolute deviation"""

    TYPE = 'FExtensionAttribute'

    def __init__(self, name, namespace, className, extAttrFa,
        extAttrExt, isMethodColumn=False):
        attributeName = self.BuildAttributeName(name, namespace)
        super(AbsoluteExtensionAttribute, self).__init__(
            attributeName, className, isMethodColumn)
        self._attributeName = name
        self._extAttrExt = extAttrExt
        self._extAttrFa = extAttrFa
        
    def _GetValue(self):
        absoluteBlock = [
                'double(%s)' % self._extAttrFa,
                '-%s' % self._extAttrExt
                ]
        if self.IsMethodColumn() and\
           self.ClassName() in ('FBusinessProcess'):
            fields = [
                'select(object.Subject.Subject,',
                'default->',
                ''.join(absoluteBlock),
                ',',
                'nil->nil)'
                ]
            return ''.join(fields)
        return ''.join(absoluteBlock)


class RelativeExtensionAttribute(ExtensionObject):
    """Represents an extension attribute for relative deviation"""

    TYPE = 'FExtensionAttribute'

    def __init__(self, name, namespace, className, extAttrFa,
        extAttrExt, isMethodColumn=False):
        attributeName = self.BuildAttributeName(name, namespace)
        super(RelativeExtensionAttribute, self).__init__(
            attributeName, className, isMethodColumn)
        self._attributeName = name
        self._extAttrExt = extAttrExt
        self._extAttrFa = extAttrFa
        
    def _GetValue(self):
        relativeBlock = [
                '(double(%s)' % self._extAttrFa,
                '-%s)/' % self._extAttrExt,
                '%s' % self._extAttrExt,
                ]
        if self.IsMethodColumn() and\
           self.ClassName() in ('FBusinessProcess'):
            fields = [
                'select(object.Subject.Subject,',
                'default->',
                ''.join(relativeBlock),
                ',',
                'nil->nil)'
                ]
            return ''.join(fields)
        return ''.join(relativeBlock)
        

class ColumnDefinition(ExtensionObject):
    """Represents a column definition"""

    TYPE = 'FColumnDefinition'

    def __init__(self, name, namespace, extensionAttribute, parentColumn, groups=None,
        comparison=False, groupLabel=None, label=None, columnType=None,
        columnAppearance=None, columnFormat=None, columnClass=None, isMethodColumn=False):
        namespaceFormatted = ' '.join((namespace, columnType)) if columnType else namespace
        columnId = MakeColumnId(name, namespaceFormatted)
        super(ColumnDefinition, self).__init__(columnId, 'FTradingSheet', isMethodColumn)
        self._columnName = name
        self._namespace = namespace
        self._extensionAttribute = extensionAttribute
        self._parentColumn = parentColumn
        self._label = label or self._columnName
        self._groupLabel = self._GroupLabel(comparison, groupLabel)
        self._columnAppearance = columnAppearance
        self._groups = groups if groups else []
        self._format = columnFormat or str()
        self._columnClass = columnClass or str()
        self.nameFormatted = ' '.join((name, columnType)) if columnType else name        
    
    def _GroupLabel(self, comparison, groupLabel):
        if not comparison:
            return 'External Values - ' + self._namespace
        return (groupLabel or self._columnName) + ' - ' + self._namespace
        
    def _GetValue(self):
        fields = [
            'ExtensionAttribute=%s\n' % self._extensionAttribute,
            'InitialWidth=100\n',
            'GroupLabel=%s\n' % self._groupLabel,
            'Name=%s\n' % self.nameFormatted,
            'LabelList=%s\n' % self._label,
            'Format=%s\n' % self._format,
            'Access=ReadOnly\n'
            ]
        if self._columnAppearance:
            fields.append('ColumnAppearance=%s\n' % self._columnAppearance.Name())
        if self._columnClass:
            fields.append('Class=%s\n' % self._columnClass)
        if self._parentColumn and not self._isMethodColumn:
            fields.append('InheritsFrom=%s\n' % self._parentColumn)
        return ''.join(fields)

    def Groups(self):
        return self._groups
        

class ColumnAppearance(ExtensionObject):
    """Represents a column appearance"""

    TYPE = 'FColumnAppearance'
    CLASS = 'FObject'

    def __init__(self, name, extensionAttribute, namespace):
        name = ' '.join((namespace, name, 'Colour'))
        super(ColumnAppearance, self).__init__(name)
        self._extensionAttribute = extensionAttribute

    def _GetValue(self):
        fields = [
            'Bkg1=Yellow:0;Yellow:0\n',
            'BkgExtensionAttribute=%s\n' % self._extensionAttribute.Name(),
            'BkgIntervals=Bkg1\n',
            ]
        return ''.join(fields)

class BkgExtensionAttribute(ExtensionObject):

    TYPE = 'FExtensionAttribute'
    SUFFIX = 'Bkg'

    def __init__(self, extensionAttribute, extensionAttributeFA, dataType):
        self.extensionAttribute = extensionAttribute
        name = ''.join((extensionAttribute.Name(), self.SUFFIX))
        super(BkgExtensionAttribute, self).__init__(name)
        self.extensionAttributeFA = extensionAttributeFA
        self.dataType = dataType
        
    def _GetValue(self):
        comparisonBlock = [
            'default->switch(',
            'py("FReconciliationValueMapping",',
            'context).',
            'CompareValuePair(%s,' % self.extensionAttributeFA,
            '%s,' % self.extensionAttribute.Name(),
            '"%s"),' % self.dataType,
            'true->1,',
            'default->0))'
            ]
        fields = [
            'select(%s,' % self.extensionAttribute.Name(),
            'default->select(object.IsKindOf("FBusinessProcess"),',
            'true->select(object.Subject.Subject,',
            ''.join(comparisonBlock),
            ',',
            ''.join(comparisonBlock),
            ')'
            ]
        return ''.join(fields)


class ExtensionCreator(object):

    EXT_MOD = '_ReconciliationColumns_'

    def __init__(self, extensions, module=None, createColumnDefinitions=True):
        self.defaultContext = acm.GetDefaultContext()
        self.extensions = extensions
        self.extMod = module
        self.createColumnDefinitions = createColumnDefinitions

    @classmethod
    def DefaultModuleName(cls):
        return cls.EXT_MOD

    def CreateExtensionModule(self):
        """create extension module"""
        self.extMod = (
                self.extMod or 
                acm.FExtensionModule[self.DefaultModuleName()]
                )
        if not self.extMod:
            try:
                self.extMod = acm.FExtensionModule()
                self.extMod.Name(self.EXT_MOD)
                self.extMod.Commit()
                logger.debug("Created FExtensionModule %s", self.DefaultModuleName())
            except RuntimeError:
                logger.error("Failed to create FExtensionModule %s", self.DefaultModuleName())
                raise

    def AddModuleToContext(self):
        """add ext_mod to context"""
        if self.extMod not in self.defaultContext.Modules():
            self.defaultContext.AddModule(self.extMod)
            logger.debug(
                    "Added FExtensionModule %s to default context",
                    self.extMod.Name())
            try:
                self.defaultContext.Commit()
            except RuntimeError:
                logger.error("Failed to add new extension module to default context")
                raise
                
    def AddColumnToGroup(self, extName, group='businessprocesssheet'):
        self.extMod.AddMember(
                extName,
                'FColumnDefinition',
                'sheet columns',
                group)
            
    def CommitModule(self):
        self.extMod.Commit()

    def CreateExtensionDefinition(self):
        """create column definition in database"""
        self.CreateExtensionModule()
        self.AddModuleToContext()
        for ext in self.extensions:
            if not self.createColumnDefinitions and ext.ExtensionType() == 'FColumnDefinition':
                continue
            self.RemoveExtension(self.extMod, ext.ExtensionType(),
                                 ext.ClassName(), ext.Name())
        for ext in self.extensions:
            if not self.createColumnDefinitions and ext.ExtensionType() == 'FColumnDefinition':
                continue
            self.InsertExtension(self.defaultContext, self.extMod,
                                 ext.ExtensionType(), ext.Name(), ext.Definition(), ext.Groups())
        self.CommitModule()

    @staticmethod
    def RemoveExtension(extMod, extType, extClass, extName):
        """remove extension into extension module"""
        extMod.RemoveExtension(extType, extClass, extName)

    def InsertExtension(self, extContext, extMod, extType, extName,
            text, groups):
        """insert extension into extension module"""
        extContext.EditImport(extType, text, True, extMod)
        if extType in ('FColumnDefinition'):
            self.AddColumnToGroup(extName)

    def Run(self):
        try:
            self.CreateExtensionDefinition()
            logger.debug('Reconciliation columns created')
        except Exception as err:
            logger.error("Failed to create extensions: %s", str(err), exc_info=True)

class ColumnCreator(object):

    SUFFIX = 'Diff'

    def __init__(self, reconSpec, groups, module=None):
        self.reconSpec = reconSpec
        self.groups = groups
        self.context = acm.GetDefaultContext()
        self.namespace = None
        self.module = module
        self.createColumnDefinitions = self.reconSpec.CreateColumnDefinitions()

    def AddComparisonColumnAbsolute(self, extensions, extAttrInt, extAttr,
            columnId, isMethodColumn, parentColumn):
        name = ' '.join((columnId, self.SUFFIX, 'Absolute'))
        for cls in self.GetClassesFromGroups(self.groups):
            absExtAttr = AbsoluteExtensionAttribute(name, self.namespace,
                    cls, extAttrInt, extAttr.Name(), isMethodColumn)
            extensions.append(absExtAttr)
        absColumnDef = ColumnDefinition(name, self.namespace, absExtAttr.Name(),
                parentColumn, groups=self.groups, comparison=True, groupLabel=columnId, label=self.SUFFIX,
                columnFormat='FullPrecision', isMethodColumn=isMethodColumn)
        extensions.append(absColumnDef)

    def AddComparisonColumnRelative(self, extensions, extAttrInt, extAttr,
            columnId, isMethodColumn, parentColumn):
        name = ' '.join((columnId, self.SUFFIX, 'Relative'))
        for cls in self.GetClassesFromGroups(self.groups):
            relExtAttr = RelativeExtensionAttribute(name, self.namespace,
                    cls, extAttrInt, extAttr.Name(), isMethodColumn)
            extensions.append(relExtAttr)
        relColumnDef = ColumnDefinition(name, self.namespace, relExtAttr.Name(),
                parentColumn, groups=self.groups, comparison=True, groupLabel=columnId,
                label=''.join((self.SUFFIX, '(%)')), columnFormat='Percent', isMethodColumn=isMethodColumn)
        extensions.append(relColumnDef)

    def AddComparisonColumns(self, extensions, extAttrInt, extAttr, columnId,
            _format, isMethodColumn, parentColumn):
        self.AddComparisonColumnAbsolute(extensions, extAttrInt, extAttr,
                columnId, isMethodColumn, parentColumn)
        self.AddComparisonColumnRelative(extensions, extAttrInt, extAttr,
                columnId, isMethodColumn, parentColumn)
        
    def CreateInternalExtension(self, extensions, extAttrInt, columnId, columnFormat, parentColumn, ourExtAttrIntName, isMethodColumn):
        columnName = MakeColumnId(columnId, ' '.join((self.namespace, 'Internal')))
        
        for cls in self.GetClassesFromGroups(self.groups):
            extensionAttribute = InternalExtensionAttribute(ourExtAttrIntName, cls, self.reconSpec.SheetType(), columnName, extAttrInt)
            extensions.append(extensionAttribute)
        
        extColumnDef = ColumnDefinition(columnId, self.namespace, extensionAttribute.Name(), parentColumn,
                self.groups, comparison=True, label='Ours', columnType='Internal', columnFormat=columnFormat, isMethodColumn=isMethodColumn)
        extensions.append(extColumnDef)
        
    def _GetInternalExtension(self, extAttrFa, isMethodColumn, extensions):
        if isMethodColumn:
            attrName = ExtensionObject.BuildAttributeName(
                extAttrFa.lstrip('object.'), self.namespace)
            for cls in self.GetClassesFromGroups(self.groups):
                if cls not in ("FBusinessProcess"):
                    extAttrInt = ExtensionObject(attrName,
                        className=cls, value=extAttrFa)
                    extensions.append(extAttrInt)
            return attrName
        return extAttrFa

    def ExtensionsToCreate(self, extensions, columnId):
        # pylint: disable-msg=E1101
        for cls in self.GetClassesFromGroups(self.groups):
            extAttrExt = ExternalExtensionAttribute(columnId, self.namespace, cls)
            extensions.append(extAttrExt)
        if self.IsComparisonNeeded(columnId):
            datatype = self.GetDataType(columnId)
            cp = self.FrontArenaColumnProperties(columnId)
            extAttrInt = self._GetInternalExtension(cp.attribute, cp.ismethod, extensions)
            
            ourExtAttrIntName = ExtensionObject.BuildAttributeName(columnId, ''.join((str(self.namespace), 'Internal')))
            
            self.CreateInternalExtension(extensions, extAttrInt, columnId, cp.format, cp.parentcolumn, ourExtAttrIntName, cp.ismethod)
            
            bkgExtAttr = BkgExtensionAttribute(extAttrExt, ourExtAttrIntName, datatype)
            extensions.append(bkgExtAttr)
            columnAppearance = ColumnAppearance(columnId, bkgExtAttr, self.namespace)
            extensions.append(columnAppearance)
            columnDef = ColumnDefinition(columnId, self.namespace, extAttrExt.Name(),
                parentColumn=cp.parentcolumn, groups=self.groups, comparison=True, label='Theirs', columnType='External',
                columnAppearance=columnAppearance, columnFormat=cp.format, isMethodColumn=cp.ismethod)
            if self.IsComparisonColumnNeeded(datatype):
                self.AddComparisonColumns(extensions, ourExtAttrIntName, extAttrExt,
                    columnId, cp.format, cp.ismethod, cp.parentcolumn)
        else:
            columnDef = ColumnDefinition(columnId, self.namespace,
                extAttrExt.Name(), parentColumn=None, groups=self.groups)
        extensions.append(columnDef)
        return extensions


    def IsComparisonNeeded(self, columnId):
        mappingValues = self.reconSpec.ValueMapping()
        return bool(acm.FSymbol(columnId) in mappingValues.Keys())

    @staticmethod
    def IsComparisonColumnNeeded(datatype):
        dataHandler = FReconciliationDataTypeHandler.FDataTypeHandler(datatype)
        return dataHandler.IsNumericDataType()

    def GetFrontArenaColumn(self, columnId):
        mappingValues = self.reconSpec.ValueMapping()
        return mappingValues.At(acm.FSymbol(columnId))

    @staticmethod
    def GetClassesFromGroups(groups):
        groupClassMapping = {
            'tradesheet': 'FTradeRow',
            'businessprocesssheet': 'FBusinessProcess',
            'portfoliosheet': 'FInstrumentAndTrades',
            'settlementsheet': 'FSettlement',
            'dealsheet': 'FTradeRow',
            'journalsheet': 'FJournal',
        }
        return [cls for (group, cls) in groupClassMapping.items() if group in groups]

    @staticmethod
    def GetColumnProperties(column):
        properties = [
                'attribute',
                'columnclass',
                'format',
                'ismethod',
                'parentcolumn'
                ]
        ColumnProperties = collections.namedtuple(
                'ColumnProperties',
                ','.join(properties)
               )
        context = acm.GetDefaultContext()
        isMethodColumn = False
        definitions = context.GetAllExtensions('FColumnDefinition', 'FTradingSheet', True, True)
        columnValue = None
        columnDefinitionName = column
        while columnDefinitionName and not columnValue:
            try:
                columnDefinition = [c for c in definitions if c.Name() in (columnDefinitionName,)][0]
                columnValue = columnDefinition.At('ExtensionAttribute')
                columnClass = columnDefinition.At('Class')
                columnFormat = columnDefinition.At('Format')
                if not columnValue:
                    method = columnDefinition.At('Method')
                    if method:
                        isMethodColumn = True
                        columnValue = 'object.' + ((str(columnClass) + '.') if columnClass else '') + str(method)
                if columnValue:
                    return ColumnProperties(
                                attribute=columnValue,
                                columnclass=columnClass,
                                format=columnFormat,
                                ismethod=isMethodColumn,
                                parentcolumn=column)
                columnDefinitionName = columnDefinition.At('InheritsFrom')
            except IndexError:
                raise IndexError('Column %s could not be found!' % columnDefinitionName)

    def GetDataType(self, columnid):
        dataTypeMapping = self.reconSpec.DataTypeMapping()
        return dataTypeMapping.GetString(columnid)

    def FrontArenaColumnProperties(self, columnId):
        column = self.GetFrontArenaColumn(columnId)
        return self.GetColumnProperties(column)
        
    def CreateColumnsFromExternalValues(self):
        externalValues = self.reconSpec.DataTypeMapping()
        self.namespace = self.reconSpec.Name()
        extensions = []
        for columnId in externalValues.Keys():
            columnId = str(columnId)
            # Generate extensions
            extensions = self.ExtensionsToCreate(extensions, columnId)
        if extensions:
            extensionCreator = ExtensionCreator(extensions, self.module, self.createColumnDefinitions)
            extensionCreator.Run()
            
    def Run(self):
        self.CreateColumnsFromExternalValues()
        

def Formatted(name):
    name = str(name)
    for tag in ('Internal', 'External'):
        if tag in name:
            return name.replace(' ' + tag, '')
    for suffix in ('Absolute', 'Relative'):
        if suffix in name:
            return name.replace(' Diff' + suffix, '')
    return name

def GetExtensionsFromContext(groupItem):
    context = acm.GetDefaultContext()
    return context.GetAllExtensions(
            'FColumnDefinition',
            'FTradingSheet',
            False,
            False,
            'sheet columns',
            groupItem)

def GetExtensionsFromModule(module):
    return module.GetAllExtensions('FColumnDefinition')

def ColumnExtensions(groupItem, container=None): 
    columnExtensions = (
            GetExtensionsFromModule(container) 
            if container else
            GetExtensionsFromContext(groupItem)
            )
    return set([str(c.Name()) for c in columnExtensions])

def ColumnExtensionsFormatted(groupItem, container=None): 
    columnExtensions = (
            GetExtensionsFromModule(container) 
            if container else
            GetExtensionsFromContext(groupItem)
            )
    return set([Formatted(c.Name()) for c in columnExtensions])

def CreateColumns(reconSpec, module=None):
    groupItem = acm.Sheet.GetSheetDefinition(reconSpec.SheetType()).GroupItemName()
    columnCreator = ColumnCreator(
            reconSpec,
            ['businessprocesssheet', groupItem],
            module)
    columnCreator.Run()