""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FManualFillDialog.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FManualFillDialog

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Dialog for entering a manual fill on a sales order
-------------------------------------------------------------------------------------------------"""
import acm
import FUxCore
import FOrderUtils

class ManualFillDialog(FUxCore.LayoutDialog):
    
    def __init__(self, order, shell):
        self.m_bindings = None
        self._order = order
        self.shell = shell
        self.remainingQuantityCtrl = None
        self.fillPriceCtrl = None
        self.counterPtyCtrl = None
        self.tradeTimeCtrl = None
        self.m_okBtn = None
        self.InitControls()
    
    def ValidateQuantity(self):
        if self.remainingQuantityCtrl.GetValue() > self._order.RemainingQuantity():
            raise Exception('Fill quantity is greater than remaining quantity on order')
        if self.remainingQuantityCtrl.GetValue() <= 0:
            raise Exception('Quantity must be greater than zero')
            
    def ValidatePrice(self):
        if self.fillPriceCtrl.GetValue() <= 0:
            raise Exception('Price must be greater than zero')
        
    def ValidateCounterparty(self):
        if not self.counterPtyCtrl.GetValue():
            raise Exception('Counterparty must be selected')

    def HandleApply(self):
        try:
            self.ValidateQuantity()
            self.ValidatePrice()
            self.ValidateCounterparty()
        except Exception as e:
            acm.UX().Dialogs().MessageBoxInformation(self.shell, e.message)
        else:
            handler = FOrderUtils.AsOrderHandler(self._order)
            matchOrderHandler = FOrderUtils.CreateMatchOrderHandler(handler,
                                                                    self.remainingQuantityCtrl.GetValue(),
                                                                    self.fillPriceCtrl.GetValue(),
                                                                    self.counterPtyCtrl.GetValue(),
								    'Manual Fill',
                                                                    self.tradeTimeCtrl.GetValue())
            if matchOrderHandler:
                completion = acm.Trading().CreateCommandCompletion(self.shell, 'MatchOrder')
                try:
                    matchOrderHandler.Send(completion)
                except Exception as e:
                    acm.UX().Dialogs().MessageBoxInformation(self.shell, 'There was an error matching this order {0}'.format(e))
            return 1
    
    def UpdateControls(self):
        if self._order.PriceCondition().Name() == 'Unlimited':
            self.fillPriceCtrl.SetValue(0)
        else:
            self.fillPriceCtrl.SetValue(self._order.PriceLimitDouble())
        self.remainingQuantityCtrl.SetValue(self._order.RemainingQuantity())
        self.tradeTimeCtrl.SetValue(acm.Time.TimeNow())
                
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Manual Fill')
        self.m_okBtn = layout.GetControl("ok")
        self.m_bindings.AddLayout(layout)
        self.UpdateControls()
    
    def InitControls(self):
        parties = acm.FParty.Select('notTrading = False and type in ("Counterparty", "Broker")').SortByProperty('StringKey')
        formatter = acm.Get('formats/Imprecise')
                
        ctyPtyPopulator = acm.FChoiceListPopulator()
        ctyPtyPopulator.SetChoiceListSource(parties)
                
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.fillPriceCtrl = self.m_bindings.AddBinder('fillPriceCtrl', acm.GetDomain('double'), acm.Get('formats/DetailedShowZero'))
        self.remainingQuantityCtrl = self.m_bindings.AddBinder('remainingQuantityCtrl', acm.GetDomain('double'), acm.Get('formats/Imprecise'))
        self.counterPtyCtrl = self.m_bindings.AddBinder('counterPtyCtrl', acm.GetDomain('string'), None, ctyPtyPopulator)
        self.tradeTimeCtrl = self.m_bindings.AddBinder('tradeTimeCtrl', acm.GetDomain('datetime'),  None)
        
    def CreateLayout(self):
        label = str(self._order)
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginHorzBox('EtchedIn', 'Order')
        b. AddLabel('OrderInfo', label)
        b. EndBox()
        b. BeginVertBox('EtchedIn', 'Manual Fill')
        self.remainingQuantityCtrl.BuildLayoutPart(b, 'Quantity')
        self.fillPriceCtrl.BuildLayoutPart(b, 'Match Price')
        self.counterPtyCtrl.BuildLayoutPart(b, 'Counterparty')
        self.tradeTimeCtrl.BuildLayoutPart(b, 'Trade Time')
        b. EndBox()
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
