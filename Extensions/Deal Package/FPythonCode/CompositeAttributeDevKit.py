from CompositeAttributeBase import CompositeAttributeBase

class CompositeAttributeDefinition(CompositeAttributeBase):
    ''' Interface for Composite Attribute definitions'''
    
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Override methods below  =====v=v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def OnInit(self, *args, **kwargs):
        ''' Called when creating an instance of CompositeAttributeDefinition

            Example:
                def OnInit(self, objMapping):
                    self._objMapping = objMapping
                
                def Attributes(self):
                    return {'quantity' : Object( objMapping=self._objMapping )}
        '''
    
    def Attributes(self):
        ''' Return a dictionary of attributes.

            Example:
                def Attributes(self):
                    return {'counterparty' : Str(    label='Counterparty',
                                                     domain='FCounterParty'),

                            'type'         : Str(    defaultValue=self.DefaultType(),
                                                     label='Type',
                                                     domain='enum(PaymentType)'),

                            'amount'       : Float(  label='Amount' )
                           }
        '''
        return {} 
    
    def OnOpen(self):
        ''' Called on open '''
        
    def OnNew(self):
        ''' Called on new '''
        
    def GetLayout(self):
        ''' Return layout of Composite Attribute. Should be used with UniqueLayout.

            Example:
                def GetLayout(self):
                    return self.UniqueLayout(""" 
                                             hbox(;
                                                myAttributeX;
                                                myAttributeY;
                                             );
                                             """)
        '''
        return CompositeAttributeBase.GetLayout(self)
    
    def IsValid(self, exceptionAccumulator, aspect):
        ''' Override this method if Pre-Save Validation should be applied.
            - use exceptionAccumulator object to append validation errors
              e.g.: 
                    if (aTrade.Counterparty() == None):
                        exceptionAccumulator('Missing Counterparty')
            - aspect is used to indicate if instrument package of both packages are validated
              Valid values for aspect are enum(IsValidAspect) as:
              "DealPackage", used to validate both deal package and instrument package
              "InstrumentPackage", used to validate only the instrument package
            - if no validation errors are added to the exceptionAccumulator
              the validation is successful and the save will be successful
        '''
        
    @classmethod
    def SetUp(cls, definitionSetUp):
        ''' Override this class method to specify additional data needed for deployment, 
            e.g. Additional Info, Choice List, Context Link, Custom Methods. See the 
            Deal Package Examples module for more information .
            
            definitionSetUp:
                Call the method AddSetupItems to add a specification of the 
                additional data needed. E.g:
                                
                definitionSetUp.AddSetupItems( AddInfoSetUp( recordType='DealPackage',
                                                            fieldName='DPEx_Beta',
                                                            dataType='Double',
                                                            description='DealPackageExample Double Test',
                                                            dataTypeGroup='Standard',
                                                            subTypes=[],
                                                            defaultValue=None,
                                                            mandatory=False ) )
        '''
        pass
    
    def AttributeOverrides(self, overrideAccumulator):
        ''' Important: Do not call super-classes. That is handled automatically.
        
            Override this method in order to modify meta data on attributes of
            this composite attribute.
            
            overrideAccumulator:
                Call the object in order to add overrides of meta data on attributes.
                The argument should be a dictionary with,
                    Key: Name of attribute
                    value: Dict where,
                            Key: Meta data key
                            Value: Meta data to be added/replaced
                                
                
            Example:
                def AttributeOverrides(self, overrideAccumulator)
                    # Important: Do not call super-classes. That is handled automatically.
                    overrideAccumulator(
                        {'attrName': dict(label='My New Label',
                                          onChanged=self.UniqueCallback('@MyAdditionalCallback')),
                         'compositeAttrName_attrName2': dict(visible=False)
                        }
                    )
        '''
        pass
    
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Override methods above  =====^=^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Do not override methods below =v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def UniqueCallback(self, name):
        ''' Gives callback unique name prefixed with "compositeAttributeInstanceName_" '''
        return CompositeAttributeBase.UniqueCallback(self, name)
    
    def SetAttribute(self, name, value, silent=False):
        return CompositeAttributeBase.SetAttribute(self, name, value, silent)
    
    def GetAttribute(self, name):
        return CompositeAttributeBase.GetAttribute(self, name)
        
    def GetAttributeMetaData(self, attrName, metaKey):
        return CompositeAttributeBase.GetAttributeMetaData(self, attrName, metaKey)
        
    def GetAttributeMetaDataKeys(self, attrName):
        return CompositeAttributeBase.GetAttributeMetaDataKeys(self, attrName)        
        
    def GetMethod(self, methodName):
        ''' Get method from owner '''
        return CompositeAttributeBase.GetMethod(self, methodName)
        
    def HasMethod(self, methodName):
        ''' Returns True if owner implements a method called methodName '''
        return CompositeAttributeBase.HasMethod(self, methodName)

    def UniqueLayout(self, layoutString):
        ''' Gives layout unique attribute names prefixed with "compositeAttributeInstanceName_" '''
        return CompositeAttributeBase.UniqueLayout(self, layoutString)
        
    def IsShowModeDetail(self, *args):
        return CompositeAttributeBase.IsShowModeDetail(self, args)

    def CloseDialog(self):
        return CompositeAttributeBase.CloseDialog(self)

    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Do not override methods above =^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====

    # *- That's all folks... -*
