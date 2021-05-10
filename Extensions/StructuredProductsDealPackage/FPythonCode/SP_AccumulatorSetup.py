
# Setup method used by both the deal package and the custom
# instrument definition

def Setup(definitionSetUp):
    # Accumulator specific setup
    from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp, ContextLinkSetUp
    definitionSetUp.AddSetupItems(
                        ChoiceListSetUp(
                            list='ValGroup', 
                            entry='AccDec', 
                            descr='Accumulator'
                            ),
                        ChoiceListSetUp(
                            list='Valuation Extension', 
                            entry='accDecModelDesc', 
                            descr='Accumulator'
                            ),
                        ChoiceListSetUp(
                            list='StructureType', 
                            entry='Accumulator', 
                            descr='Accumulator'
                            ),
                        ChoiceListSetUp(
                            list        = 'ValuationProcess',
                            entry       = 'LogNorm',
                            descr       = 'LogNorm'
                            ),
                        ChoiceListSetUp(
                            list        = 'ValuationProcess',
                            entry       = 'LocalVolatility',
                            descr       = 'LocalVolatility'
                            ),
                        ContextLinkSetUp(
                            context='Global',
                            type='Valuation Extension',
                            name='accDecModelDesc',
                            mappingType='Val Group',
                            chlItem='AccDec'
                            ),
                        AddInfoSetUp( 
                            recordType='Instrument',
                            fieldName='AccumulatorLeverage',
                            dataType='Double',
                            description='Leverage for an accumulator product',
                            dataTypeGroup='Standard',
                            subTypes=['Option'],
                            defaultValue=2.0,
                            mandatory=False
                            ),
                        AddInfoSetUp( 
                            recordType='Instrument',
                            fieldName='sp_RollingPeriod',
                            dataType='String',
                            description='Frequency of date schedule',
                            dataTypeGroup='Standard',
                            subTypes=['Option'],
                            defaultValue=None,
                            mandatory=False
                            ),
                        AddInfoSetUp( 
                            recordType='Instrument',
                            fieldName='sp_PayDayMethod',
                            dataType='BusinessDayMethod',
                            description='Business Day Method for calculating delivery dates',
                            dataTypeGroup='Enum',
                            subTypes=['Option'],
                            defaultValue='Following',
                            mandatory=False
                            ),
                        AddInfoSetUp(
                            recordType      = 'Instrument',
                            fieldName       = 'ValuationProcess',
                            dataType        = 'ChoiceList',
                            description     = 'ValuationProcess',
                            dataTypeGroup   = 'RecordRef',
                            subTypes        = ['Option'],
                            defaultValue    = 'LogNorm',
                            mandatory       = False
                            ),
                        AddInfoSetUp( 
                            recordType='Instrument',
                            fieldName='StructureType',
                            dataType='ChoiceList',
                            description='StructureType',
                            dataTypeGroup='RecordRef',
                            subTypes=[],
                            defaultValue=None,
                            mandatory=False
                            ))
