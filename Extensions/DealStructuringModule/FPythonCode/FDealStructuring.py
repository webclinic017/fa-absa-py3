from __future__ import print_function
import acm
import FUxCore

# Static data
calculationsSheetType = 'FDealSheet'
calculationsContext = acm.GetDefaultContext()
theorPriceColumnId = 'Price Theor'
businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIShell()
useCreateMappingWizardForDealInNewUnderlyingInstrument = False
globalContext = 'Global'

# #####################################################################
# createClickToBookButton
#  - Method called when creating the click to book cell button.
#  - Entry point from sheet call back
# #####################################################################
def createClickToBookButton( invokationInfo ):
    cell = invokationInfo.Parameter("Cell")	
    row = cell.RowObject()
    showButtonStatus = False	
    if row.IsKindOf(acm.FTrade):
        showButtonStatus = True
    return showButtonStatus
    
# #####################################################################
# postCreateNewVolaLandscape
# #####################################################################
def postCreateNewVolaLandscape(row, col, calcval, newUnderlying, operation):
    if useCreateMappingWizardForDealInNewUnderlyingInstrument:
        if operation.AsString() == 'insert':
            if not newUnderlying.MappedVolatilityLink().MappedInContext():
                print ('No Volatility Structure mapped to ', newUnderlying.Name())
            if not newUnderlying.MappedDividendStream().MappedInContext():
                print ('No Dividend Stream mapped to ', newUnderlying.Name())

# #####################################################################
# exeptionOccuredOnCommit
# #####################################################################  
def exeptionOccuredOnCommit( templateTrade, templateInstrument, fuxShell, failingTaskName ):
    buttonPressed = acm.UX().Dialogs().MessageBoxOKCancel( fuxShell, 'Question', failingTaskName + ':\nThis entity cannot be structured in the pricing sheet. \nOpen in Instrument Definition to book manually?')
    
    newTrade, newInstrument = CreateNewTradeAndInstrument( templateTrade, templateInstrument )
    
    newInstrument.Generic( False )
        
    InitializeUniqueIdentifiers( templateInstrument, newInstrument )
    
    if buttonPressed == 'Button1':
        acm.StartApplication( "Instrument Definition", newTrade )

# #####################################################################
# clickToBookButton
#  - Method called on Click To Book...
#  - Entry point from sheet call back
# #####################################################################
def clickToBookButton( invokationInfo ):
    activeSheet = invokationInfo.Parameter('sheet')
    fUxShell = invokationInfo.Parameter('shell')

    templateTrade = activeSheet.Selection().SelectedTrades()
    businessLogicGUIDefaultHandler.SetFUxShell( fUxShell )

    if templateTrade.Size() == 1:
        templateTrade = templateTrade[0]
        templateInstrument = templateTrade.Instrument()
        # So far only Options
        if templateInstrument.InsType() == 'Option':
            try:
                # Create a new Trade and a new Option
                newTrade, newInstrument = CreateNewTradeAndInstrument( templateTrade, templateInstrument )
                CheckAndUpdateInstrument( templateInstrument, newInstrument )
                InitializeUniqueIdentifiers( templateInstrument, newInstrument )
                newInstrument.RegisterInStorage()
                CheckAndUpdateTrade( activeSheet, templateTrade, newTrade )
                newInstrument, newTrade = SaveInstrumentAndTrade( newInstrument, newTrade )
                CreateMappingsForNewInstrument( newInstrument, invokationInfo )
                # Open the new trade in an Option Instrument Definition
                acm.StartApplication( "Instrument Definition", newTrade )
            except Exception:
                exeptionOccuredOnCommit( templateTrade, templateTrade.Instrument(), fUxShell, "Click To Book" )
        else:
            print ("Book Trade only supported on Options!")
    else:
        print ("Book Trade only supported for one trade at a time!")


# #####################################################################
# createNewInstrument
#  - Method called on Create New Instrument...
#  - Entry point from sheet call back
# #####################################################################
def createNewInstrument( invokationInfo ):
    activeSheet = invokationInfo.Parameter('sheet')
    fUxShell = invokationInfo.Parameter('shell')

    businessLogicGUIDefaultHandler.SetFUxShell( fUxShell )

    instruments = activeSheet.Selection().SelectedInstruments()
    if instruments.Size() == 1:
        templateInstrument = instruments[0]
        if templateInstrument.InsType() == 'Option':
            try:
                newInstrument = acm.FOption()
                newInstrument.Apply( templateInstrument )
                InitializeUniqueIdentifiers( templateInstrument, newInstrument )
                newInstrument.RegisterInStorage()
                newInstrument, newTrade = SaveInstrumentAndTrade( newInstrument )
                CreateMappingsForNewInstrument( newInstrument, invokationInfo )
                acm.StartApplication( "Instrument Definition", newInstrument )
            except Exception as e:
                exeptionOccuredOnCommit( None, templateInstrument, fUxShell, "Create New Instrument" )
        else:
            print ("Create New Instrument only supported on Options!")
    else:
        print ("Only one instrument can be created at a time!")


# #####################################################################
# CheckAndUpdateInstrument
#  - Method called on Click To Book
#  - Verifies and updates the instrument Strike Type
# #####################################################################
def CheckAndUpdateInstrument( templateInstrument, newInstrument ):
    # Always update properties using the decorators
    newInstrumentDecorator = acm.FOptionDecorator( newInstrument, businessLogicGUIDefaultHandler )
    # To make trade in instrument - Strike Type must be Absolute
    newInstrumentDecorator.StrikeType('Absolute')
    # To make trade - instrument should not be generic
    newInstrumentDecorator.Generic( False )

# #####################################################################
# FindColumnByName
#  - Traverse columns to find specified Column
# #####################################################################
def FindColumnByName( gridColumnIterator, columnName ):
    while gridColumnIterator:
        if gridColumnIterator.GridColumn().ColumnId().AsString() == columnName:
            return gridColumnIterator
        gridColumnIterator = gridColumnIterator.Next()
        
# #####################################################################
# CalculatedValueFromCell
#  - Traverse the current row to find specified Column and return Value
# #####################################################################
def CalculatedValueFromCell( activeSheet, columnId ):
    gridColumnIterator = activeSheet.GridBuilder().GridColumnIterator().First()
    rowTreeIterator = activeSheet.Selection().SelectedCell().Tree().Iterator()
    gridColumnIterator = FindColumnByName( gridColumnIterator, columnId )
    valuationCell = activeSheet.GetCell( rowTreeIterator, gridColumnIterator )    
    if valuationCell:
        return valuationCell.Value()
    else:
        return 0

# #####################################################################
# SuggestNewTradePriceIfZero
#  - Suggest a new trade price if the current trade price is zero
# #####################################################################
def SuggestNewTradePriceIfZero( activeSheet, trade ):
    newTradePrice = CalculatedValueFromCell( activeSheet, theorPriceColumnId )
    if not newTradePrice or not newTradePrice.IsNumber():
        calc_space = acm.Calculations().CreateCalculationSpace( calculationsContext, calculationsSheetType )
        newTradePrice = calc_space.CalculateValue( trade, theorPriceColumnId )
    if newTradePrice and newTradePrice.IsNumber():
        return newTradePrice.Number()
    return 0.0
    
# #####################################################################
# ChecckAndUpdateTrade
#  - Method called on Click To Book
#  - Verifies and updates the trade status and the trade price
# #####################################################################

def ValidateTheoreticalPriceCalculationAndThrowException( activeSheet, trade ):
    calc_space = acm.Calculations().CreateCalculationSpace( calculationsContext, calculationsSheetType )
    newTradePrice = calc_space.CalculateValue( trade, theorPriceColumnId )


# #####################################################################
# ChecckAndUpdateTrade
#  - Method called on Click To Book
#  - Verifies and updates the trade status and the trade price
# #####################################################################
def CheckAndUpdateTrade( activeSheet, templateTrade, newTrade ): 
    # Always update properties using the decorators
    newTradeDecorator = acm.FTradeLogicDecorator( newTrade, businessLogicGUIDefaultHandler )
    # Make sure setup is correct
    ValidateTheoreticalPriceCalculationAndThrowException( activeSheet, templateTrade )
    # Trade Price should default to Theoretical Price if not entered manually in pricing sheet
    if templateTrade.Price() == 0.0 and templateTrade.Premium() == 0.0:
        newTradePrice = SuggestNewTradePriceIfZero( activeSheet, templateTrade )
        newTradeDecorator.Price( newTradePrice )
    # Trade status should be Simulated by default
    newTradeDecorator.Status('Simulated')
            

# #####################################################################"
# InitializeUniqueIdentifiers"
#  - Method called on Click To Book and on Create New Instrument..."
#  - Remove unique identifiers from instrument"
# #####################################################################"
def InitializeUniqueIdentifiers( templateInstrument, newInstrument ):
    newInstrument.InitializeUniqueIdentifiers()
    newInstrument.Name( templateInstrument.SuggestName() )


# #####################################################################
# SaveInstrumentAndTrade
#  - Commits an instrument and a optional trade to the database.
#  - Deletes any instrument aliases to avoid database-duplicates.
# #####################################################################
def SaveInstrumentAndTrade( instrument, trade=None ):
    newInstrumentDecorator = acm.FOptionDecorator( instrument, businessLogicGUIDefaultHandler )
    newInstrument = newInstrumentDecorator.SaveNewInstrument() 
    if trade:
        trade.Instrument( newInstrument )        
        trade.Commit()
    return newInstrument, trade

# #####################################################################
# CreateNewTradeAndInstrument
#  - Create new Trade and Instrument that are available in the dh
# #####################################################################
def CreateNewTradeAndInstrument( templateTrade, templateInstrument ):
    newTrade = acm.FTrade()
    newInstrument = acm.FOption()
    newInstrument.Apply( templateInstrument )
    if templateTrade:
        newTrade.Apply( templateTrade ) 
        newTrade.ContractTrdnbr( 0 )
        newTrade.ConnectedTrdnbr( 0 )
    newInstrument = newInstrument.CloneAndSimulateRecursive()
    newTrade = newTrade.CloneAndSimulateRecursive()
    newTrade.Instrument( newInstrument )
    if templateInstrument.Exotic():
        newExotic = acm.FExotic()
        newExotic.Apply( templateInstrument.Exotic() )
        newInstrument.ExoticType( templateInstrument.ExoticType() )
        newExotic.Instrument( newInstrument )
        newExotic.CloneAndSimulateRecursive()
        
    return newTrade, newInstrument
    
# #####################################################################
# CreateMappingsForNewInstrument
# #####################################################################
def CreateMappingsForNewInstrument( newInstrument, invokationInfo ):

    if useCreateMappingWizardForDealInNewUnderlyingInstrument:
        underlying = newInstrument.Underlying()
        startWizard = 0
        if underlying:
            if not underlying.MappedVolatilityLink().MappedInContext():
                startWizard = 1
            if not underlying.MappedDividendStream().MappedInContext():
                startWizard += 2
                
        StartDialog( invokationInfo, startWizard, newInstrument )

# #####################################################################
# #####################################################################
# 
# Optional FUX based Volatility and Dividend Stream Creation Wizard
#
# This part is enabled by changing the setting 
#    'useCreateMappingWizardForDealInNewUnderlyingInstrument'
#
# #####################################################################
# #####################################################################

# #####################################################################
# Custom Dialog Class
# #####################################################################
class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_doubleVolaCtrl = None
        self.m_nameVolaCtrl = None
        self.m_currencyCtrl = None
        self.m_contextCtrl = None
        self.m_saveVolaStructureCtrl = None
        self.m_okBtn = None
        self.m_activeSheet = None
        self.m_currentVolaCtrl = None
        self.m_createVolaButtonCtrl = None
        self.m_currentDivStreamCtrl = None
        self.m_createAndMapDivStreamButtonCtrl = None
        self.m_nameDivStreamCtrl = None
        self.m_amountDivStreamCtrl = None
        self.m_exDivDayDivStreamCtrl = None
        self.m_payDayDivStreamCtrl = None
        self.m_recordDayDivStreamCtrl = None
        self.m_saveDivStream = None
        self.m_volaStructureCreateStatus = 0
        self.m_divStreamCreateStatus = 0
        
# #####################################################################
    def HandleApply( self ):
        return 1
        
# #####################################################################
    def ServerUpdate( self, sender, aspectSymbol, parameter ):
        # Update the Pay Day for the Dividend Stream based on the Ex Div Day.
        if parameter == self.m_exDivDayDivStreamCtrl:
            if aspectSymbol.AsString() == 'ControlValueChanged':
                if self.m_exDivDayDivStreamCtrl.GetValue():
                    exDivDay = self.m_exDivDayDivStreamCtrl.GetValue()
                    modDate = acm.Time().DateAddDelta( exDivDay, 0, 0, self.m_newInstrument.SpotBankingDaysOffset()-1 )
                    modDate = self.m_newInstrument.Currency().Calendar().ModifyDate( None, None, modDate, 'Following' )
                    self.m_payDayDivStreamCtrl.SetValue(modDate)
                    self.m_recordDayDivStreamCtrl.SetValue(modDate)
    
# #####################################################################        
    def UpdateControls( self ):
        # Change behaviour in order to support Vola Open or Create
        if self.m_newInstrument.Underlying().MappedVolatilityLink().MappedInContext():
            self.m_currentVolaCtrl.SetData( self.m_newInstrument.Underlying().MappedVolatilityLink().Link().VolatilityStructure() )
            self.m_createVolaButtonCtrl.Label('Open')
        else:
            self.m_currentVolaCtrl.SetData( '' )

        # Change behaviour in order to support DivStream Open or Create
        if self.m_newInstrument.Underlying().MappedDividendStream().MappedInContext():
            self.m_currentDivStreamCtrl.SetData( self.m_newInstrument.Underlying().MappedDividendStream().Parameter() )
            self.m_createAndMapDivStreamButtonCtrl.Label('Open')
        else:
            self.m_currentDivStreamCtrl.SetData( '' )

        # Update visibility logics for Vola controls
        self.m_doubleVolaCtrl.Visible(self.m_volaStructureCreateStatus)
        self.m_nameVolaCtrl.Visible(self.m_volaStructureCreateStatus)
        self.m_currencyCtrl.Visible(self.m_volaStructureCreateStatus)
        self.m_saveVolaStructureCtrl.Visible(self.m_volaStructureCreateStatus)
        
        # Update visibility logics for DivStream controls
        self.m_nameDivStreamCtrl.Visible(self.m_divStreamCreateStatus)
        self.m_amountDivStreamCtrl.Visible(self.m_divStreamCreateStatus)
        self.m_exDivDayDivStreamCtrl.Visible(self.m_divStreamCreateStatus)
        self.m_payDayDivStreamCtrl.Visible(self.m_divStreamCreateStatus)
        self.m_recordDayDivStreamCtrl.Visible(self.m_divStreamCreateStatus)
        self.m_saveDivStream.Visible(self.m_divStreamCreateStatus)
        
        self.m_contextCtrl.Visible(self.m_volaStructureCreateStatus or self.m_divStreamCreateStatus)

# #####################################################################
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Valuation Parameter Creation' )
        self.m_okBtn = layout.GetControl("ok")
        self.m_bindings.AddLayout(layout)
          
        self.m_currentVolaCtrl = layout.GetControl('currentVolaCtrl')
        self.m_createVolaButtonCtrl = layout.GetControl('createVolaButtonCtrl')
        self.m_createVolaButtonCtrl.AddCallback( "Activate", OnCreateVolaButtonClicked, self )
        self.m_currentDivStreamCtrl = layout.GetControl('currentDivStreamCtrl')
        self.m_createAndMapDivStreamButtonCtrl = layout.GetControl('createAndMapDivStreamButtonCtrl')
        self.m_createAndMapDivStreamButtonCtrl.AddCallback( "Activate", OnCreateAndMapDivStreamClicked, self )
        self.m_nameVolaCtrl = layout.GetControl('nameVolaCtrl')
        self.m_saveVolaStructureCtrl = layout.GetControl('saveVolaStructure')
        self.m_saveVolaStructureCtrl.AddCallback( "Activate", OnSaveVolaButtonClicked, self )
        self.m_nameDivStreamCtrl = layout.GetControl('nameDivStreamCtrl')
        self.m_saveDivStream = layout.GetControl('saveDivStream')
        self.m_saveDivStream.AddCallback( "Activate", OnSaveDivStreamButtonClicked, self )
        
        self.m_currencyCtrl.SetValue(self.m_newInstrument.Currency())
        self.m_contextCtrl.SetValue( globalContext )
        self.m_nameVolaCtrl.SetData('Vola ' + self.m_newInstrument.Underlying().Name())
        self.m_nameDivStreamCtrl.SetData('DivStream ' + self.m_newInstrument.Underlying().Name())

        self.m_amountDivStreamCtrl.SetValue('0')
        self.m_exDivDayDivStreamCtrl.SetValue('')
        self.m_payDayDivStreamCtrl.SetValue('')
        self.m_recordDayDivStreamCtrl.SetValue('')
        
        defaultVolaValue = CalculatedValueFromCell(self.m_activeSheet, 'Portfolio Volatility')
        if defaultVolaValue:
            self.m_doubleVolaCtrl.SetValue( defaultVolaValue * 100 )
        else:
            self.m_doubleVolaCtrl.SetValue( 40 )

        self.m_currentVolaCtrl.Editable( False )
        self.m_currentDivStreamCtrl.Editable( False )

        self.UpdateControls()
    
# #####################################################################        
    def InitControls( self, invokationInfo, newInstrument ):
        context = [globalContext, 'User']
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        
        self.m_doubleVolaCtrl = self.m_bindings.AddBinder( 'doubleCtrl', acm.GetDomain('double'), None )
        self.m_currencyCtrl = self.m_bindings.AddBinder( 'currInsCtrl', acm.GetDomain('FCurrency'), None )
        self.m_contextCtrl = self.m_bindings.AddBinder( 'contextCtrl', acm.GetDomain('string'), None, context )

        self.m_amountDivStreamCtrl = self.m_bindings.AddBinder( 'amountDivStreamCtrl', acm.GetDomain('double'), None )
        self.m_exDivDayDivStreamCtrl = self.m_bindings.AddBinder( 'exDivDayDivStreamCtrl', acm.GetDomain('date'), None )
        self.m_payDayDivStreamCtrl = self.m_bindings.AddBinder( 'payDayDivStreamCtrl', acm.GetDomain('date'), None)
        self.m_recordDayDivStreamCtrl = self.m_bindings.AddBinder( 'recordDayDivStreamCtrl', acm.GetDomain('date'), None )

        self.m_activeSheet = invokationInfo.Parameter('sheet')
        self.m_newInstrument = newInstrument

# #####################################################################        
    def CreateLayout( self, startWizard ):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.  BeginVertBox('None')
        b.    BeginVertBox('EtchedIn', 'Mapped Parameters')
        b.      BeginHorzBox('None')        
        b.        AddInput('currentVolaCtrl', 'Mapped Volatility', 20, 20)
        b.        AddButton('createVolaButtonCtrl', 'Create >>')
        b.      EndBox()
        b.      BeginHorzBox('None')
        b.        AddInput('currentDivStreamCtrl', 'Mapped Dividend Stream', 20, 20)
        b.        AddButton('createAndMapDivStreamButtonCtrl', 'Create >>')
        b.      EndBox()
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddSpace(50)
        b.      AddFill()
        b.      AddButton('ok', 'OK')
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('None')
        #VOLA
        b.    BeginVertBox('EtchedIn', 'Volatility Structure')
        b.      AddInput('nameVolaCtrl', 'Name')
        self.m_doubleVolaCtrl.BuildLayoutPart(b, 'Volatility Value')
        self.m_currencyCtrl.BuildLayoutPart(b, 'Currency')
        b.    EndBox()
        #DIVSTREAM
        b.    BeginVertBox('EtchedIn', 'Dividend Stream')
        b.      AddInput('nameDivStreamCtrl', 'Name')
        self.m_exDivDayDivStreamCtrl.BuildLayoutPart(b, 'Ex Div Day')
        self.m_recordDayDivStreamCtrl.BuildLayoutPart(b, 'Record Day')        
        self.m_payDayDivStreamCtrl.BuildLayoutPart(b, 'Pay Day')
        self.m_amountDivStreamCtrl.BuildLayoutPart(b, 'Amount')
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Context Mapping')
        self.m_contextCtrl.BuildLayoutPart(b, 'Map in Context')        
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddSpace(50)
        b.      AddFill()
        #VOLA
        b.      AddButton('saveVolaStructure', 'Save Vol')
        #DIVSTREAM
        b.      AddButton('saveDivStream', 'Save Div')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()

        return b
        
# #####################################################################
    def CreateAndMapVolaStructure( self ):
        # Create a Volatiltiy Landscape
        # Add and/or change Set methods to modify Vola Landscape Creation
        newVolaStruct = acm.FBenchmarkVolatilityStructure()
        newVolaStruct.Name(self.m_nameVolaCtrl.GetData())
        newVolaStruct.StructureType( 'Benchmark' )
        newVolaStruct.RiskType('Equity Vol')
        newVolaStruct.StrikeType( 'Absolute' )
        newVolaStruct.InterpolationMethod('Hermite')
        newVolaStruct.DeltaAtmDefinition('Spot')
        newVolaStruct.DeltaTerm('Pct of foreign')
        newVolaStruct.DomesticHolidayWeight(1.0);
        newVolaStruct.DomesticWeekendWeight(1.0);
        newVolaStruct.ForeignHolidayWeight(1.0);
        newVolaStruct.ForeignWeekendWeight(1.0);
        newVolaStruct.VolatilityValueType('Relative');
        newVolaStruct.AbsUnderlyingMaturity(1);
        newVolaStruct.Framework('Black & Scholes');
        newVolaStruct.UseUnderlyingMarketPrice(1);
        newVolaStruct.Currency(self.m_currencyCtrl.GetValue())
        newVolaStruct.InsertPoint(self.m_newInstrument, self.m_doubleVolaCtrl.GetValue()/100.0)
        newVolaStruct.ReferenceInstrument( self.m_newInstrument.Underlying() )
        newVolaStruct.Commit()
        
        # Map Vola Landscape to User or Global
        # Change here if default Context no called Global
        mapInContextName = self.m_contextCtrl.GetValue()
        mapInContext = None
        if mapInContextName == 'User':
            mapInContext = acm.FContext[acm.UserName()]
        if not mapInContext:
            mapInContext = acm.FContext[globalContext]
            
        contextLink = acm.FContextLink()
        contextLink.Context(mapInContext)
        contextLink.Currency(self.m_newInstrument.Underlying().Currency())
        contextLink.Instrument(self.m_newInstrument.Underlying())
        contextLink.Type('Volatility')
        contextLink.Name(newVolaStruct.Name())
        contextLink.MappingType('Instrument')

        contextLink.Commit()
        
# #####################################################################        
    def CreateAndMapDivStream( self ):
        # Create a Dividend Stream
        # Add and/or change Set methods to modify Div Stream Creation
        newDivStream = acm.FDividendStream()
        newDivStream.Name(self.m_nameDivStreamCtrl.GetData())
        newDivStream.Instrument(self.m_newInstrument.Underlying())
        newDivStream.DividendsPerYear(1)
        newDivStream.AnnualGrowth(0)
        newDivStream.Commit()

        newDivEst = acm.FDividendEstimate()
        newDivEst.Amount(self.m_amountDivStreamCtrl.GetValue())
        newDivEst.Currency(self.m_newInstrument.Underlying().Currency())
        newDivEst.ExDivDay(self.m_exDivDayDivStreamCtrl.GetValue())
        newDivEst.PayDay(self.m_payDayDivStreamCtrl.GetValue())
        newDivEst.RecordDay(self.m_recordDayDivStreamCtrl.GetValue())
        newDivEst.Instrument(self.m_newInstrument.Underlying())
        newDivEst.TaxFactor(1)
        newDivEst.DividendStream(newDivStream)
        newDivEst.Commit()

        # Map Div Stream to User or Global
        # Change here if default Context no called Global
        mapInContextName = self.m_contextCtrl.GetValue()
        mapInContext = None
        if mapInContextName == 'User':
            mapInContext = acm.FContext[acm.UserName()]
        if not mapInContext:
            mapInContext = acm.FContext[globalContext]
            
        contextLink = acm.FContextLink()
        contextLink.Context(mapInContext)
        contextLink.Instrument(self.m_newInstrument.Underlying())
        contextLink.Type('Dividend Stream')
        contextLink.Name(newDivStream.Name())
        contextLink.MappingType('Instrument')
        
        contextLink.Commit()

# #####################################################################
# Enable Create or Open Vola Button Clicked
# #####################################################################
def OnCreateVolaButtonClicked( self, cd ):
    if self.m_newInstrument.Underlying().MappedVolatilityLink().MappedInContext():
        acm.StartApplication("Volatility Manager", self.m_newInstrument.Underlying().MappedVolatilityLink().Link().VolatilityStructure())
    else:
        self.m_volaStructureCreateStatus = not self.m_volaStructureCreateStatus
    self.UpdateControls()
    
# #####################################################################
# Enable Create or Open Dividend Stream Button Clicked
# #####################################################################
def OnCreateAndMapDivStreamClicked( self, cd ):
    if self.m_newInstrument.Underlying().MappedDividendStream().MappedInContext():
        acm.StartApplication("Dividend Estimation", self.m_newInstrument.Underlying().MappedDividendStream().Parameter())
    else:
        self.m_divStreamCreateStatus = not self.m_divStreamCreateStatus
    self.UpdateControls()
   
# #####################################################################
# Save Volatility Button Clicked
# ##################################################################### 
def OnSaveVolaButtonClicked( self, cd ):
    self.m_volaStructureCreateStatus = 0
    self.m_createVolaButtonCtrl.Label('Open')
    self.CreateAndMapVolaStructure()
    self.UpdateControls()
    
# #####################################################################
# Save Dividend Stream Button Clicked
# #####################################################################
def OnSaveDivStreamButtonClicked( self, cd ):
    self.m_divStreamCreateStatus = 0
    self.CreateAndMapDivStream()
    self.UpdateControls()

# #####################################################################
# Start FUX Dialog for Volatility and Dividend Stream Creation
# #####################################################################
def StartDialog( invokationInfo, startWizard, newInstrument ):
    if startWizard:
        shell = invokationInfo.ExtensionObject().Shell()
        customDlg = myCustomDialog()
        customDlg.InitControls(invokationInfo, newInstrument)
        acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(startWizard), customDlg )


