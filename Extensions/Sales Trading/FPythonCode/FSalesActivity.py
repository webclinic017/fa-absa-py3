""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesActivity.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesTrading

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from DealPackageDevKit import CompositeAttributeDefinition, CalcVal, Str, Float, Object, CounterpartyChoices, DealPackageChoiceListSource
from DealPackageUtil import IsFObject
from EditableObjectDevKit import EditableObjectDefinition

try:
    import FSalesActivityUtils
except ImportError:
    print('Built-in module "Sales Trading" is required for the Sales Activity deal package.')
    raise


class SalesActivityPanel(CompositeAttributeDefinition):

    def OnInit(self, salesActivity='SalesActivity', **kwargs):
        self._salesActivityFunc = salesActivity
        self._contacts = DealPackageChoiceListSource()
        self._instruments = DealPackageChoiceListSource()

    def Attributes(self):
        return {
            'type':             Object( label='Type',
                                        objMapping='SalesActivity.Type',
                                        defaultValue='Order',
                                        onChanged=self.UniqueCallback('@OnTypeChanged'),
                                        choiceListSource=self.UniqueCallback('@TypeChoices') ),
            'counterparty':     Object( label='Counterparty',
                                        objMapping='SalesActivity.Counterparty',
                                        choiceListSource=CounterpartyChoices(),
                                        onChanged=self.UniqueCallback('@OnCounterpartyChanged') ),
            'contact':             Str( label='Contact',
                                        objMapping=self.UniqueCallback('Contact'),
                                        choiceListSource=self.UniqueCallback('@ContactChoices') ),
            'insType':             Str( label='Ins Type',
                                        choiceListSource=self.UniqueCallback('@InstrumentTypeChoices'),
                                        onChanged=self.UniqueCallback('@OnInstrumentTypeChanged') ),
            'instrument':       Object( label='Instrument',
                                        objMapping='SalesActivity.Instrument',
                                        mandatory=self.UniqueCallback('@IsMandatory'),
                                        choiceListSource=self.UniqueCallback('@InstrumentChoices'),
                                        onChanged=self.UniqueCallback('@OnInstrumentChanged') ),
            'nominal':           Float( label='Nominal',
                                        objMapping=self.UniqueCallback('Nominal'),
                                        formatter='InstrumentDefinitionNominal',
                                        visible=self.UniqueCallback('@NominalVisible'),
                                        enabled=self.UniqueCallback('@NominalEnabled') ),
            'orderType':        Object( label='Order Type',
                                        objMapping='SalesActivity.OrderType',
                                        defaultValue='IOI',
                                        visible=self.UniqueCallback('@OrderTypeVisible') ),
            'priceAdjType':     Object( label='Nuke Option',
                                        objMapping='SalesActivity.PriceAdjustmentType',
                                        visible=self.UniqueCallback('@PriceAdjTypeVisible'),
                                        defaultValue='Delta Nuke' ),
            'askPrice':          Float( label='Ask Price',
                                        objMapping='SalesActivity.BaseAskPrice',
                                        formatter='InstrumentDefinitionStrikePrice',
                                        visible=self.UniqueCallback('@AskPriceVisible') ),
            'bidPrice':          Float( label=self.UniqueCallback('@BidPriceLabel'),
                                        objMapping='SalesActivity.BaseBidPrice',
                                        formatter='InstrumentDefinitionStrikePrice',
                                        visible=self.UniqueCallback('@BidPriceVisible'),
                                        enabled=self.UniqueCallback('@BidPriceEnabled') ),
            'undPrice':          Float( label='Und Price',
                                        objMapping='SalesActivity.BaseUnderlyingPrice',
                                        formatter='InstrumentDefinitionStrikePrice',
                                        visible=self.UniqueCallback('@UndPriceVisible'),
                                        enabled=self.UniqueCallback('@UndPriceEnabled') ),
            'delta':             Float( label='Delta',
                                        objMapping='SalesActivity.BaseDelta',
                                        formatter='VolatilityPercentShowZero',
                                        visible=self.UniqueCallback('@DeltaVisible'),
                                        enabled=self.UniqueCallback('@DeltaEnabled') ),
            'volatility':        Float( label='Volatility',
                                        objMapping='SalesActivity.Volatility',
                                        formatter='VolatilityPercentShowZero',
                                        visible=self.UniqueCallback('@VolatilityVisible'),
                                        enabled=self.UniqueCallback('@VolatilityEnabled') ),
            'fxRate':            Float( label=self.UniqueCallback('@FxRateLabel'),
                                        objMapping='SalesActivity.FXRate',
                                        formatter='FXRate',
                                        visible=self.UniqueCallback('@FxRateVisible'),
                                        enabled=self.UniqueCallback('@FxRateEnabled') ),
            'salesPerson':      Object( label='Sales Person',
                                        objMapping='SalesActivity.SalesPerson' ),
            'trade':           CalcVal( label='Trade',
                                        calcMapping='SalesActivity:FSalesActivitySheet:Sales Activity Trade',
                                        visible=self.UniqueCallback('@TradeVisible'),
                                        enabled=False ),
            'activityTime':     Object( label='Activity Time',
                                        objMapping="SalesActivity.ActivityTime", 
                                        domain = "time" ),
            'diary':            Object( label='Diary',
                                        objMapping='SalesActivity.Diary',
                                        domain='FSalesActivityDiary',
                                        visible=False ),
            'underlyingTrade':  Object( label='underlyingTrade',
                                        objMapping='SalesActivity.Trade',
                                        visible=False )
        }

    def GetLayout(self):
        return self.LayoutFromExtensionValue('CustomLayout_SalesActivity')

    # *************************************************
    # Object/Value Mapping

    def AskPriceDefaultValue(self, *args):
        return self.CalculateValue('proposedAskPrice')

    def AskPriceVisible(self, *args):
        return self.IsPriceRequest()

    def BidPriceDefaultValue(self, *args):
        return self.CalculateValue('defaultBidPrice')

    def BidPriceEnabled(self, *args):
        return not self.IsVegaNuke()

    def BidPriceLabel(self, *args):
        return 'Bid Price' if self.IsPriceRequest() else 'Price'

    def BidPriceVisible(self, *args):
        return not self.IsHolder() and self.HasInstrument()

    def ContactChoices(self, *args):
        return self._contacts

    def Contact(self, name = None):
        if name is None:
            if self.SalesActivity().Contact():
                return self.SalesActivity().Contact().StringKey()
            else:
                return None
        else:
            self.SalesActivity().Contact = self.GetContact(name)

    def GetContact(self, contactName):
        if contactName and self.GetAttribute('counterparty'):
            for contact in self.GetAttribute('counterparty').Contacts():
                if contact.StringKey() == contactName:
                    return contact
        return None

    def DeltaDefaultValue(self, *args):
        return self.CalculateValue('referenceUserDelta')

    def DeltaEnabled(self, *args):
        return self.DeltaVisible() and not self.IsVegaNuke()

    def DeltaVisible(self, *args):
        try:
            return not self.IsHolder() and self.HasUnderlying()
        except AttributeError:
            return False

    def FxRateDefaultValue(self, *args):
        return self.CalculateValue('liveFXRateFormatted')

    def FxRateEnabled(self, *args):
        return not self.IsVegaNuke() and self.IsDualCurrencyInstrument()

    def FxRateLabel(self, *args):
        if self.IsDualCurrencyInstrument():
            return FSalesActivityUtils.FXRateLabel(self.instrument)
        return 'FX Rate'
            
    def FxRateVisible(self, *args):
        try:
            return not self.IsHolder() and self.IsDualCurrencyInstrument()
        except AttributeError:
            return False

    def InstrumentChoices(self, *args):
        return self._instruments

    def InstrumentTypeChoices(self, *args):
        return acm.FEnumeration['enum(InsType)'].EnumeratorStringsSkipFirst()

    def IsMandatory(self, *args):
        return True

    def Nominal(self, nominal = None):
        if self.GetAttribute('instrument'):
            if nominal is None:
                return self.SalesActivity().Nominal()
            else:
                self.SalesActivity().Nominal(nominal)

    def NominalVisible(self, *args):
        return self.HasInstrument()

    def NominalEnabled(self, *args):
        return self.NominalVisible() and not self.IsPriceRequest()

    def OrderTypeVisible(self, *args):
        return self.IsOrder() or self.IsTrade()

    def IsConvertible(self):
        return self.GetAttribute('insType') == 'Convertible'

    def PriceAdjTypeVisible(self, *args):
        return (self.IsOrder() or self.IsTrade()) and self.IsConvertible()

    def SalesActivity(self):
        return self.GetMethod(self._salesActivityFunc)()

    def TradeVisible(self, *args):
        return self.IsTrade()

    def TypeChoices(self, *args):
        return acm.FEnumeration['enum(SalesActivityType)'].EnumeratorStringsSkipFirst()

    def UndPriceDefaultValue(self, *args):
        return self.CalculateValue('originalUnderlyingPrice')

    def UndPriceEnabled(self, *args):
        return self.UndPriceVisible() and not self.IsVegaNuke()

    def UndPriceVisible(self, *args):
        try:
            return not self.IsHolder() and self.HasUnderlying()
        except AttributeError:
            return False

    def VolatilityEnabled(self, *args):
        return self.IsVegaNuke()
        
    def VolatilityVisible(self, *args):
        return not self.IsHolder() and self.HasInstrument()

    # *************************************************
    # Changed Callbacks

    def OnCounterpartyChanged(self, name, oldValue, newValue, *args):
        self.UpdateContactChoices(newValue)
        self.SetAttribute('contact', None)

    def OnInstrumentTypeChanged(self, name, oldValue, newValue, *args):
        self.UpdateInstrumentChoices(newValue)
        self.SetAttribute('instrument', None)

    def OnInstrumentChanged(self, name, oldValue, newValue, *args):
        if self.GetAttribute('instrument'):
            self.SalesActivity().Quantity(1)
            self.SetAttribute('nominal', self.SalesActivity().Nominal())
        self.SetDefaultValues()

    def OnTypeChanged(self, name, oldValue, newValue, *args):
        if newValue != 'Price Request':
            self.SetAttribute('askPrice', 0)
        if newValue not in ['Order', 'Trade', ]:
            self.SetAttribute('priceAdjType', 'None')
            self.SetAttribute('orderType', 'None')

    # *************************************************
    # State information

    def IsDeltaNuke(self):
        return self.GetAttribute('priceAdjType') == 'Delta Nuke'

    def IsDualCurrencyInstrument(self):
        ins = self.GetAttribute('instrument')
        if ins and ins.Underlying():
            return ins.Currency() != ins.Underlying().Currency()
        return False

    def IsHolder(self):
        return self.GetAttribute('type') == 'Holder'

    def IsOrder(self):
        return self.GetAttribute('type') == 'Order'

    def IsPriceRequest(self):
        return self.GetAttribute('type') == 'Price Request'

    def IsTrade(self):
        return self.GetAttribute('type') == 'Trade'

    def IsVegaNuke(self):
        return self.GetAttribute('priceAdjType') == 'Vega Nuke'

    def HasInstrument(self):
        return self.GetAttribute('instrument') is not None

    def HasUnderlying(self):
        ins = self.GetAttribute('instrument')
        try:
            return ins.Underlying() is not None or ins.Instruments().Size() > 0
        except AttributeError:
            return False

    # *************************************************
    # Initialisation Methods

    def InitialiseNewAttributes(self):
        self.SetAttribute('type', 'Order')
        self.SetAttribute('insType', 'Convertible')
        self.SetAttribute('activityTime', acm.Time.RealTimeNow())
        self.SetAttribute('salesPerson', acm.User())

    def InitialiseAttributes(self):
        self.InitialiseInsType()
        self.InitialiseContacts()

    def InitialiseContacts(self):
        if self.GetAttribute('counterparty'):
            self.UpdateContactChoices()

    def InitialiseInsType(self):
        ins = self.GetAttribute('instrument')
        if ins:
            self.SetAttribute('insType', ins.InsType(), silent=True)
            self.UpdateInstrumentChoices()

    # *************************************************
    # Misc. Util Methods

    def CalculateValue(self, attributeName):
        return FSalesActivityUtils.GetCalculatedValue(
                    self.SalesActivity().DecoratedObject(), attributeName)

    def LayoutFromExtensionValue(self, extensionName):
        layout = acm.GetDefaultContext().GetExtension(
            'FExtensionValue', acm.FObject, extensionName).Value()
        return self.UniqueLayout(layout)

    def UpdateContactChoices(self, party=None):
        party = party or self.GetAttribute('counterparty')
        self._contacts.Clear()
        if party:
            contacts = party.Contacts()
            self._contacts.AddAll([c.StringKey() for c in contacts])

    def UpdateInstrumentChoices(self, insType=None):
        insType = insType or self.GetAttribute('insType')
        self._instruments.Clear()
        if insType:
            instruments = acm.FInstrument.Select('insType=' + insType)
            self._instruments.AddAll(sorted([i for i in instruments if not i.IsExpired()]))

    def SetDefaultValues(self):
        self.SetDefaultValue('askPrice', self.AskPriceDefaultValue())
        self.SetDefaultValue('bidPrice', self.BidPriceDefaultValue())
        if self.IsDualCurrencyInstrument():
            self.SetDefaultValue('fxRate', self.FxRateDefaultValue())
        self.SetDefaultValue('activityTime', acm.Time.TimeNow())
        self.SetDerivativeDefaultValues()
        self.SetPriceAdjustmentType()


    def SetDefaultValue(self, attributeName, value):
        if FSalesActivityUtils.IsValidNumber(value):
            if IsFObject(value, acm.FDenominatedValue):
                value = value.Number()
            self.SetAttribute(attributeName, value)

    def SetDerivativeDefaultValues(self):
        try:
            if self.HasUnderlying():
                self.SetDefaultValue('undPrice', self.UndPriceDefaultValue())
                self.SetDefaultValue('delta', self.DeltaDefaultValue())
        except AttributeError:
            pass

    def SetPriceAdjustmentType(self):
        if self.IsConvertible():
            self.SetAttribute('priceAdjType', 'Delta Nuke')
        else:
            self.SetAttribute('priceAdjType', 'None')


class SalesActivityDefinition(EditableObjectDefinition):

    salesActivityPanel = SalesActivityPanel(salesActivity='SalesActivity')

    def SalesActivity(self):
        return self.Object()

    # *************************************************
    # Deal Package Interface Methods

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_SalesActivity")

    def OnNew(self):
        self.salesActivityPanel.InitialiseNewAttributes()

    def OnOpen(self):
        if not self.Object().DecoratedObject().Originator().IsInfant():
            self.salesActivityPanel.InitialiseAttributes()
        else:
            self.salesActivityPanel.InitialiseNewAttributes()

    def OnSave(self, config):
        if config.DealPackage() == "SaveNew":
            diary = self.Object().DecoratedObject().Diary()
            if diary and diary.IsStorageImage():
                diary.StorageSetNew()