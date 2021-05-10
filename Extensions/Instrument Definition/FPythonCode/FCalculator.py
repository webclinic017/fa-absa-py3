import acm
import FUxCore

# #####################################################################
# InitializeUniqueIdentifiers
#  - Method called on PerformBookTrade
#  - Remove unique identifiers from instrument
# #####################################################################
def InitializeUniqueIdentifiers( templateInstrument, newInstrument ):
    name = newInstrument.Name()
    newInstrument.InitializeUniqueIdentifiers()
    if acm.FInstrument[name]:
         newInstrument.Name(templateInstrument.SuggestName())
    else:
        newInstrument.Name = name
        
    if newInstrument.Decompositions():
        newInstrument.Decompositions().Clear()


# #####################################################################
# SaveInstrumentAndTrade
#  - Commits an instrument and a optional trade to the database.
#  - Deletes any instrument aliases to avoid database-duplicates.
# #####################################################################
def SaveInstrumentAndTrade( instrument, trade=None ):
    try:
        acm.BeginTransaction()
        instrument.Commit()
        if trade:
            trade.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        raise


# #####################################################################
# PerformBookTrade
# Main routine that creates a new instrument and initializes a new
# trade with quantity and price from the calculator. The new instrument
# is opened in a new instrument definition window.
# #####################################################################
def PerformBookTrade( eii ):
    calculator = eii.ExtensionObject()
    if "CalculatorConfiguration" == calculator.GetConfigurationKey():
        verifyInstrumentId = acm.GetDefaultValueFromName( acm.GetDefaultContext(), "CInsDefAppFrame", "calculatorBookTradeVerifyInstrumentId" );

        calculator.UpdatePricingEntity()
        templateInstrument = calculator.EditInstrument()
        
        try:
            if( templateInstrument.InsType() == 'Option' ):
                newInstrument = acm.FOption()
            elif (templateInstrument.InsType() == 'Warrant' ):
                newInstrument = acm.FWarrant()
            newInstrument.Apply( templateInstrument )
            InitializeUniqueIdentifiers( templateInstrument, newInstrument )

            if "True" == verifyInstrumentId:
                builder = CreateLayout()
                customDlg = confirmInstrumentNameDialog()
                customDlg.m_instrumentName = newInstrument.Name()
                newInstrumentName = acm.UX().Dialogs().ShowCustomDialogModal( calculator.Shell(), builder, customDlg )
                if None == newInstrumentName:
                    newInstrument.Delete()
                    return
                else:
                    newInstrument.Name( newInstrumentName )
            SaveInstrumentAndTrade( newInstrument )
            insdef = acm.StartApplication( "Instrument Definition", newInstrument )
        except Exception as e:
            raise Exception( "No instrument saved." )

        newTrade = insdef.EditTrade()
        quantity = calculator.GetPricingCellValue( "Calculator Quantity" )
        if quantity:
            newTrade.Quantity( quantity )
        price = calculator.GetPricingCellValue( "Calculator Price Theor" )
        if price and price.IsNumber():
            newTrade.Price( price )
            newTrade.UpdatePremium( True )
        insdef.ShowTradePane( True )
    else:
        acm.UX().Dialogs().MessageBoxInformation( calculator.Shell(), "Book Trade action is only applicable for the Calculator." )

class confirmInstrumentNameDialog ( FUxCore.LayoutDialog ):
    def __init__( self ):
        self.m_nameEdit = 0
        self.m_fuxDlg = 0
        self.m_instrumentName = 0
        
    def HandleApply( self ):
        name = str( self.m_nameEdit.GetData() )
        if len( name ):
            existingInstrument = acm.FInstrument[ name ]
            if None == existingInstrument:
                return name
            else:
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), "Instrument name is not unique.")
        return None
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( "Confirm Instrument Name" )
        self.m_nameEdit = layout.GetControl( "name" )
        self.m_nameEdit.SetData( self.m_instrumentName )

def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox("None")
    b.  AddInput("name", "Name", 39, 39, 39)
    b.  BeginHorzBox("None")
    b.    AddFill()
    b.    AddButton("ok", "OK")
    b.    AddButton("cancel", "Cancel")
    b.  EndBox()
    b.EndBox()
    return b
