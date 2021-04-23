""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitCorporateActions/./etc/MarkitDataMapping.py"
from __future__ import print_function
import ael, acm
import os
def IdentifySecurityID(x, d):
    return {
        d['Identifying Security ID Type']: d['Identifying Security ID'],
        d['Security ID Type']: d['Security ID'],
    }.get(x, None) 
def GetCaChoiceType(x):
    return {
        'M': 'Mandatory',
        'V': 'Voluntary',
    }.get(x, None) 
def GetCaType(x):
    return {
        'RDN': 'RightsDistribution',
        'TE': 'TenderOfferStock',
        'SS': 'SplitStock',
        'RS': 'ReverseStockSplit',
        'SD': 'StockDividend',
        'CD': 'CashDistribution',
        'LQ': 'Liquidation',
        'NC': 'NameChange',
        'DRI': 'DividendReinvestment',
        'MEM': 'MergerStock',
        'SC': 'ScripDividend',
    }.get(x, None) 
def __setTemplate(ca, template):
    if not template:
        return
    cats = ca.Templates()
    #print (cats)
    cats.Delete()
    if template is type(acm.FCorpactTemplate()):
        cat = corpact_template
    elif type(template) is type(''):
        cat = acm.FCorpactTemplate()
        cat.Name(template)
    elif type(template) is type([]):
        cat = template[0]
    if cat:
        cat.CorporateAction(ca)
        cat.Commit()
def CreateOrUpdateFCorporateAction(d):
    stock = FindIdentifyingSecurity(d)
    if stock: 
        ca = acm.FCorporateAction.Select01("externalId = '%s'" %d['CA ID'], None)
        if ca:
            #print ('Update',ca)
            UpdateFCorporateAction(d, stock.Oid())
        else:
            #print ('Create',ca)
            CreateFCorporateAction(d, stock.Oid())
def FindIdentifyingSecurity(d):        
    cusip = IdentifySecurityID('02', d)
    sedol = IdentifySecurityID('03', d)
    isin =  IdentifySecurityID('04', d)
    if sedol:
        ins_alias = acm.FInstrumentAlias.Select01('type=%d and alias = %s' % (acm.FInstrAliasType['SEDOL'].Oid(), sedol), None)
        if ins_alias:
            stock = ins_alias.Instrument()
            return stock
    if isin:
        stock = acm.FStock.Select01("isin = '%s'" %isin, None)
        return stock
    return None
def CreateFCorporateAction(d, insaddr):
    ca = acm.FCorporateAction()
    #ca.Name(str(d['Issuer Description'])+str(d['CA ID']))
    #ca.Name(d['Issuer Description'] + d['CA ID'])
    ca.Name(' '.join([d['Issuer Description'], d['CA ID']])) 
    ca.ExternalId(d['CA ID'])
    ca.Instrument(insaddr)
    ca.CaChoiceType(GetCaChoiceType(d['Voluntary/Mandatory Code']))
    ca.ExDate(d['Ex Date'].replace("/", "-"))
    ca.RecordDate(d['Record Date'].replace("/", "-"))
    ca.SettleDate(d['Payable Date'].replace("/", "-"))
    if d['Payable Date']:
        ca.SettleDate(d['Payable Date'].replace("/", "-"))
    elif d['Delisting Date']:
        ca.SettleDate(d['Delisting Date'].replace("/", "-"))
    ca.TradingBeginDate(d['Trading Begin Date'].replace("/", "-"))
    ca.TradingEndDate(d['Trading End Date'].replace("/", "-"))
    ca.WithdrawalDate(d['Withdrawal Date'].replace("/", "-"))
    #ca.LotSize(d['Odd Lot Holding Maximum'])
    ca.OldQuantity(d['Subscription Old Shares Qty'])#????
    ca.NewQuantity(d['Subscription New Shares Qty'])#????
    if d['Approved Date']:
        ca.Status('Active')
    if d['Cancelled'] == 'Y':
        ca.Status('Inactive')
    if d['Minimum Denomination']:
        ca.LotSize(d['Minimum Denomination'])
    elif d['Minimum Exercise Quantity']:
        ca.LotSize(d['Minimum Exercise Quantity'])
    ca.CashAmount(d['Event Cash Value'])#????
    ca.CashCurrency(acm.FCurrency[d['Event Cash Value Currency']])
    textObject = acm.FCustomTextObject['corporate action: ' + ca.Name()]
    if textObject:
        ca.SourceRecord(textObject)
        UpdateFPersistentTextObject(d, textObject)
    else:
        CreateFPersistentTextObject(d, 'corporate action: ' + ca.Name())
        ca.SourceRecord(acm.FPersistentText['corporate action: ' + ca.Name()])
    ca.Commit()
    __setTemplate(ca, GetCaType(d['Corporate Action Type']))
    if d['Corporate Action Type']=='CD' or d['Corporate Action Type']=='DRI':
        CreateFDividend(ca)
def UpdateFCorporateAction(d, insaddr):
    ca = acm.FCorporateAction.Select01("externalId = '%s'" %d['CA ID'], None)
    if ca:
        ca_clone = ca.Clone()
        #ca_clone.Name('New Name Update')
        #ca_clone.Name(' '.join(d['Issuer Description'].split('  ')[:2]) + d['CA ID'])
        #ca_clone.Name(str(d['CA ID']) + str(d['Issuer Description']))
        #ca_clone.Name(d['Issuer Description'] + d['CA ID'])
        ca_clone.Name(' '.join([d['Issuer Description'], d['CA ID']])) 
        ca_clone.Instrument(insaddr)
        ca_clone.CaChoiceType(GetCaChoiceType(d['Voluntary/Mandatory Code']))
        ca_clone.ExDate(d['Ex Date'].replace("/", "-"))
        ca_clone.RecordDate(d['Record Date'].replace("/", "-"))
        ca_clone.SettleDate(d['Payable Date'].replace("/", "-"))
        if d['Payable Date']:
            ca_clone.SettleDate(d['Payable Date'].replace("/", "-"))
        elif d['Delisting Date']:
            ca_clone.SettleDate(d['Delisting Date'].replace("/", "-"))
        ca_clone.TradingBeginDate(d['Trading Begin Date'].replace("/", "-"))
        ca_clone.TradingEndDate(d['Trading End Date'].replace("/", "-"))
        ca_clone.WithdrawalDate(d['Withdrawal Date'].replace("/", "-"))
        #ca_clone.LotSize(d['Odd Lot Holding Maximum'])
        ca_clone.OldQuantity(d['Subscription Old Shares Qty'])#????
        ca_clone.NewQuantity(d['Subscription New Shares Qty'])#????
        if d['Approved Date']:
            ca_clone.Status('Active')
        if d['Cancelled'] == 'Y':
            ca_clone.Status('Inactive')
        if d['Minimum Denomination']:
            ca_clone.LotSize(d['Minimum Denomination'])
        elif d['Minimum Exercise Quantity']:
            ca_clone.LotSize(d['Minimum Exercise Quantity'])
        ca_clone.CashAmount(d['Event Cash Value'])#????
        ca_clone.CashCurrency(acm.FCurrency[d['Event Cash Value Currency']])
        textObject = ca_clone.SourceRecord()
        if textObject:
            UpdateFPersistentTextObject(d, textObject)
        else:
            textObject = acm.FCustomTextObject['corporate action: ' + ca.Name()]
            if textObject:
                ca_clone.SourceRecord(textObject)
                UpdateFPersistentTextObject(d, textObject)
            else:
                CreateFPersistentTextObject(d, 'corporate action: ' + ca.Name())
                ca_clone.SourceRecord(textObject)
        ca.Apply( ca_clone )
        ca.Commit()
        __setTemplate(ca, GetCaType(d['Corporate Action Type']))  
        #if ca.Templates():
        #    print (ca.Name(),ca.Templates()[0].Name())
        #    if ca.Templates()[0].Name()=='CashDistribution' or ca.Templates()[0].Name()=='DividendReinvestment':
        #        print ('Dividend table')
        if d['Corporate Action Type']=='CD' or d['Corporate Action Type']=='DRI':
            CreateOrUpdateFDividend(ca)
def CreateFPersistentTextObject(d, name):
    textObject = acm.FCustomTextObject()
    textObject.Name(name)
    textObject.SubType('Customizable')
    textObject.Text(str({k: v for k, v in d.items() if v.lstrip()}))
    textObject.Commit()
def UpdateFPersistentTextObject(d, textObject):
    textObject_clone = textObject.Clone() 
    textObject_clone.Text(str({k: v for k, v in d.items() if v.lstrip()}))
    textObject.Apply(textObject_clone) 
    textObject.Commit()
#D2
def CreateOrUpdateFCorporateActionChoice(d):
    ca = acm.FCorporateAction.Select01("externalId = '%s'" %d['CA ID'], None)
    if ca:
        ca_choices = ca.CaChoices()
        if ca_choices:
            choiceName = ' '.join([d['Option Number'], d['Option Action'], d['Option Text'][:25]])
            ca_choice = acm.FCorporateActionChoice.Select01("choiceName='%s' and corpAction='%d'" %(choiceName.strip(), ca.Oid()), None)
            if ca_choice:
                if ca_choice in ca_choices:
                    UpdateFCorporateActionChoice(d, ca)
            else:
                CreateFCorporateActionChoice(d, ca)
        else:
            CreateFCorporateActionChoice(d, ca)
def CreateFCorporateActionChoice(d, ca):
    cac = acm.FCorporateActionChoice()
    choiceName = ' '.join([d['Option Number'], d['Option Action'], d['Option Text'][:25]])
    cac.ChoiceName(choiceName)
    cac.IsDefault({'Y': True, 'N': False}.get(d['Default Option Indicator'], False))
    cac.CorpAction(ca)
    textObject = acm.FCustomTextObject['caChoice: ' + ca.Name() + ' ' + d['Option Number']]
    print(textObject)
    if textObject:
        cac.ChoiceRecord(textObject)
        UpdateFPersistentTextObject(d, textObject)
    else:
        CreateFPersistentTextObject(d, 'caChoice: ' + ca.Name() + ' ' + d['Option Number'])
        cac.ChoiceRecord(acm.FPersistentText['caChoice: ' + ca.Name() + ' ' + d['Option Number']])
    cac.Commit() 
def UpdateFCorporateActionChoice(d, ca):
    choiceName = ' '.join([d['Option Number'], d['Option Action'], d['Option Text'][:25]])
    cac = acm.FCorporateActionChoice.Select01("choiceName='%s' and corpAction='%d'" %(choiceName.strip(), ca.Oid()), None)
    if cac:
        cac_clone = cac.Clone()
        cac_clone.IsDefault({'Y': True, 'N': False}.get(d['Default Option Indicator'], False))
        textObject = cac_clone.ChoiceRecord()
        if textObject:
            UpdateFPersistentTextObject(d, textObject)
        else:
            textObject = acm.FCustomTextObject['caChoice: ' + ca.Name() + ' ' + d['Option Number']]
            if textObject:
                cac_clone.ChoiceRecord(textObject)
                UpdateFPersistentTextObject(d, textObject)
            else:
                CreateFPersistentTextObject(d, 'caChoice: ' + ca.Name() + ' ' + d['Option Number'])
                cac_clone.ChoiceRecord(acm.FPersistentText['caChoice: ' + ca.Name() + ' ' + d['Option Number']])
        #textObject = acm.FCustomTextObject['caChoice: ' + ca.Name() + ' ' + d['Option Number']]
        #cac_clone.ChoiceRecord(textObject)
        cac.Apply( cac_clone )
        cac.Commit()
        cac.CaPayouts().Delete()
#D3
def CreateOrUpdateFCorporateActionPayout(d):
    ca = acm.FCorporateAction.Select01("externalId = '%s'" %d['CA ID'], None)
    if ca:
        ca_choices = ca.CaChoices()
        if ca_choices:
            ca_choice = FindCaChoice(ca_choices, d['Option Number'])
            if ca_choice:
                print('CreateOrUpdateFCorporateActionPayout')
                #print (ca_choice)
                #print (ca.Name(),ca_choice.ChoiceName())
                cac_clone = ca_choice.Clone()
                ca_choice.CashCurrency(acm.FCurrency[d['Currency Code']])
                if cac_clone.Name().split(' ', 2)[1] == 'CASH':
                    cac_clone.CashAmount(d['Payout Amount'])
                elif cac_clone.Name().split(' ', 2)[1] == 'SECU':
                    cac_clone.StockAmount(d['Payout Rate'])
                ca_choice.Apply( cac_clone )
                ca_choice.Commit()
                ca_clone = ca.Clone()
                ca_clone.OldQuantity(d['Old Shares'])#????
                ca_clone.NewQuantity(d['New Shares'])#????
                ca.Apply( ca_clone )
                ca.Commit()
                div = ca.Dividend()
                if div:
                    div_clone = div.Clone()
                    div_clone.Amount(d['Payout Gross Amount'])
                    #div_clone.TaxFactor(d['Withholding Tax Rate'])
                    div_clone.TaxFactor(1)
                    div.Apply( div_clone )
                    div.Commit()
                #if ca.Templates():
                #    print (ca.Name(),ca.Templates()[0].Name())
                #    if ca.Templates()[0].Name()=='CashDistribution' or ca.Templates()[0].Name()=='DividendReinvestment':
                #        print ('Dividend table')
                cap = acm.FCorporateActionPayout()
                cap.CaChoice(ca_choice)
                #cap.AddInfoValue('PayoutName',' '.join([d['CA ID'], d['Payout Status'], d['Option Number'], d['Payout Number'], d['Payout Type']])) 
                cap.PayoutRate(d['Payout Rate'])
                cap.PayoutAmount(d['Payout Amount'])
                cap.PayoutNetAmount(d['Payout Net Amount'])
                print('net', d['Payout Net Amount'])
                print('gross', d['Payout Gross Amount'])
                cap.PayoutGrossAmount(d['Payout Gross Amount'])
                cap.Currency(acm.FCurrency[d['Currency Code']])
                cap.Price(d['Price'])
                cap.Fee(d['Fee'])
                cap.FeeCurrency(acm.FCurrency[d['Fee Currency']])
                textObject = acm.FCustomTextObject['caPayout: ' + ca.Name() + ' ' + d['Payout Status'] + ' ' + d['Option Number']]
                if textObject:
                    cap.SourceRecord(textObject)
                    UpdateFPersistentTextObject(d, textObject)
                else:
                    CreateFPersistentTextObject(d, 'caPayout: ' + ca.Name() + ' ' + d['Payout Status'] + ' ' + d['Option Number'])
                    cap.SourceRecord(acm.FPersistentText['corporate action: ' + ca.Name()])
                cap.Commit()
                #ca_choice.CashCurrency(acm.FCurrency[d['Currency Code']])
def FindCaChoice(ca_choices, optionNumber):
    for ca_choice in ca_choices:
        if ca_choice.Name().split(' ', 1)[0] == optionNumber:
            return ca_choice
    return None
#Dividend 
def CreateFDividend(ca):
    #print (ca)
    div = acm.FDividend()
    div.ExDivDay(ca.ExDate())
    div.RecordDay(ca.RecordDate())
    div.PayDay(ca.SettleDate())
    div.Description(ca.Name())
    div.Instrument(ca.Instrument())
    div.Currency(ca.Instrument().Currency())
    div.Commit()
    ca_clone = ca.Clone()
    ca_clone.Dividend(div)
    ca.Apply( ca_clone )
    ca.Commit()
def UpdateFDividend(ca, div):
    div_clone = div.Clone()
    div_clone.ExDivDay(ca.ExDate())
    div_clone.RecordDay(ca.RecordDate())
    div_clone.PayDay(ca.SettleDate())
    div_clone.Description(ca.Name())
    div.Apply( div_clone )
    div.Commit()
def CreateOrUpdateFDividend(ca):
    div = ca.Dividend()
    if div:
        UpdateFDividend(ca, div)
    else:
        CreateFDividend(ca)
#to be continued...
