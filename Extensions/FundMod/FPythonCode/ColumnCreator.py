
import acm


class ColumnCreator(object):

    NAMESPACE = None
    PARAMETERS = None
    LABEL = None
    FORMAT = None
    LOGGER = None
    TREE_DEPENDENT_POST_PROCESSING = None

    def __init__(self, eii):
        self.shell = eii.Parameter('shell')
        self.activeSheet = eii.ExtensionObject().ActiveSheet()
        self.column = self.GetColumn()
        self.context = self.GetContext()
        self.columnId = self.GetColumnId()
        self.module = self.GetModule()
	self.attrs = []
        
    def GetColumnId(self):
        return str(self.column.ColumnId()) if self.column else None
        
    def GetContext(self):
        return self.column.Context() if self.column else None
    
    def GetColumn(self):
        selectedCell = self.activeSheet.Selection().SelectedCell()
        return selectedCell.Column() if selectedCell else None
    
    def GetColumnDefinition(self, extype='FColumnDefinition', cls='FTradingSheet'):
        try:
            definition = self.context.GetExtension(extype, cls, self.columnId).Value()
            return definition.Clone()
        except StandardError as err:
            self.LOGGER.error(err)
        
    def GetParameters(self):
        try:
            return self.context.GetAllExtensions(
                acm.FParameters, 
                self.PARAMETERS
                )[0].Value()
        except Exception:
            return None

    @staticmethod
    def ModuleName(name):
        if not name:
            return acm.UserName()
        if name.lower() in ('user',):
            return acm.UserName()
        elif name.lower().startswith('org'):
            return acm.Organisation().Name()
        return name
    
    @staticmethod
    def CapsFirst(attr):
	return ''.join((attr[0].upper(), attr[1:]))

    def CreateExtensionAttribute(self, extensionId, attr):
        raise NotImplementedError
    
    def SaveExtensionColumn(self, id, columnDefinition):
        self.context.EditImport('FColumnDefinition', columnDefinition)
        self.context.AddMember(id, 'FColumnDefinition', 'sheet columns', 'portfoliosheet')

    def SaveExtensionAttribute(self):
	for attr in self.attrs:
            self.context.EditImport('FExtensionAttribute', attr)
                
    def SaveExtensions(self, id, columnDefinition, extensionId, attr):
        """create column definition in database"""
        try:
            self.context.AddModule(self.module)
            self.SaveExtensionColumn(id, columnDefinition)
            if self.ShouldCreateExtensionAttribute(extensionId):
                self.CreateExtensionAttribute(extensionId, attr)
                self.SaveExtensionAttribute()
            self.module.Commit()
            return True
        except Exception as e:
            acm.UX().Dialogs().MessageBoxInformation(
                self.shell, 
                'Could not commit module.\nReason: %s' % str(e)
                )
            return False

    def ShouldCreateExtensionAttribute(self, extensionId):
        return extensionId and (extensionId != self.OldExtensionAttribute())

    def OldExtensionAttribute(self):
        return str(self.column.ExtensionAttribute())

    def IsValidColumn(self):
        if not self.context:
            acm.UX().Dialogs().MessageBoxInformation(
                self.shell, 
                'Please select a column and try again.')        
            return False
        elif self.column.Method():
            acm.UX().Dialogs().MessageBoxInformation(
                self.shell, 
                ('Mehod columns are not supported. '
                'Please select an extension attribute column and try again.'))
            return False
        return True
        
    def GetModule(self):
        param = self.GetParameters()
        moduleName = (
            self.ModuleName(param.GetString('Module'))
            if param
            else acm.UserName()
            )
        return acm.FExtensionModule[moduleName]
        
    def AppendParametersFixedValues(self, columnDefinition):
        parametersFixedValues = str(columnDefinition.At('ParametersFixedValues', '')).split(';')
        parametersFixedValues.extend(self.NewParametersFixedValues())
        return ';'.join(filter(None, parametersFixedValues))
        
    def NewParametersFixedValues(self):
        return list()
        
    def CreateColumnDefintion(self, newId, newAttributeId):
        try:
            columnDefinition = self.GetColumnDefinition()
            columnDefinition.Name(':'.join(('FTradingSheet', newId)))
            columnDefinition.AtPut('ExtensionAttribute', newAttributeId)
            columnDefinition.AtPut('LabelList', self.NewColumnLabel())
            columnDefinition.AtPut('Format', self.NewColumnFormat())
            columnDefinition.AtPut('TreeDependentPostProcessing', self.NewColumnTreeDependentPostProcessing())
            columnDefinition.AtPut('ParametersFixedValues', self.AppendParametersFixedValues(columnDefinition))
            columnDefinition.AtPut('Name', newId)
            return columnDefinition.AsString()
        except StandardError as err:
            self.LOGGER.error(err)
        
    def NewAttributePreffix(self):
        return self.NAMESPACE.lower()
    
    def NewColumnPreffix(self):
        return self.NAMESPACE
        
    def NewColumnLabel(self):
	return ' '.join((str(self.column.Label()), 
            self.__class__.LABEL or self.__class__.NAMESPACE))

    @classmethod
    def NewColumnFormat(cls):
        return cls.FORMAT or str()
    
    @classmethod
    def NewColumnTreeDependentPostProcessing(cls):
        return cls.TREE_DEPENDENT_POST_PROCESSING or str()
            
    def NewColumnId(self):
        return ' '.join((self.NewColumnPreffix(), 
	    str(self.column.ColumnName())))
	    
    def NewAttributeId(self, attr):
        return ''.join((self.NewAttributePreffix(),
    	    self.CapsFirst(attr)))
    
    def CreateColumn(self):
        newId = self.NewColumnId()
        attr = self.OldExtensionAttribute()
        newAttributeId = self.NewAttributeId(attr)
        newColumnDefinition = self.CreateColumnDefintion(newId, newAttributeId)
        if self.SaveExtensions(newId, newColumnDefinition, newAttributeId, attr):
            columnCreators = acm.GetColumnCreators(newId, self.context)
            referenceColumnCreator = self.column.Creator()
            referenceColumnCreators = self.activeSheet.ColumnCreators()
            referenceColumnCreators.InsertAfter(referenceColumnCreator, 
                columnCreators.At(0))
            self.LOGGER.info(
                "Column '%s' created in context %s and module %s.",
                newId,
                self.context.Name(),
                self.module.Name()
                )

