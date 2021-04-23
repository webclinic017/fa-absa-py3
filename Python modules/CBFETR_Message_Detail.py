'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Message_Detail
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module retreives all the neccessary data required for the outgoing CBFETR
                                message.
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2012-06-25      281782          Heinrich Cronje                 Changed Country_Codes to Country Codes,
                                                                Added logic for Party Fullname,
                                                                Added Party field Name
2012-08-23      407718          Willie van der Bank             Added MOA1_SARBAUTHNO filed
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade
2014-06-19      CHNG0002144533	Melusi Maseko                   Feed through new Palladium trades for BOP reporting
2014-08-10      CHNG0002238567	Melusi Maseko                   BOPCUS ETF and Gold Enhancements
2015-03-25      BOP-15          Melusi Maseko                   NewGold & NewPlat ETF Secondary Listings change
                                                                Added parm LEGAL_ENTITY_NAME
2015-05-14      BOP-10          Melusi Maseko                   Added Country Code logic according to JIRA
2015-06-03      BOP-11          Melusi Maseko                   Allowing for exception names to be reported to ODP
2015-06-08      BOP-28          Melusi Maseko                   Added a Try-Except around the SwiftAlias logic
2015-07-22      BOP-31          Melusi Maseko                   ACCOUNT IDENTIFIER: Check if Counterparty Business Status exists first 
                                                                before checking the Counterparty Business Status name
2015-07-30      CHNG0002987375  Melusi Maseko                   Concatenate the fullname and fullname2 then trim the combination to
                                                                70 characters since we crashed the SARB on 2015-07-30 as per INC0028887321
2016-02-23      BOP-34          Melusi Maseko                   In method get_Country_Code() check if issuer exists first before checking the Issuer Country.
2016-06-20      MINT-673        Melusi Maseko                   Added EXCEPTION_PORTFOLIO for exception names
2016-07-18      MINT-733        Melusi Maseko                   Return specific Reporting Qualifier and Exception names in Non Resident and Resident elements for using specificied critera
                                                                In case there are 2x Swift Aliases, default to blank 
2016-09-27      MINT-956        Melusi Maseko                   If counterparty = BARCLAYS BANK PLC and Acquirer = IRD DESK or IRP_FX Desk then return alias = BARCGB22
                                                                If trade meets criteria in TASK 2 of JIRA http://abcap-jira/browse/MINT-956, the Reporting Qualifier must be INTERBANKy
2018-01-23      ABITFA-5077     Melusi Maseko                   Remove hard-coding of ruling section and default to blank
2018-01-23      ABITFA-5198     Melusi Maseko                   Add logic for NONBANK_EXCEPTION_PORTFOLIO and NONBANK_EXCEPTION_ACQUIRERS to report Exception names
2018-05-16      AMD-8           Melusi Maseko                   Do not send through any BoP and Sub Bop category for NONBANK_EXCEPTION_PORTFOLIO and NONBANK_EXCEPTION_ACQUIRERS
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Only instantiate the Message_Detail class with a specific money flow. All relevant detail will be retreived
    and the message detail will be available in the variable called Message_Detail.
'''
import acm, ael
import CBFETR_Parameters as Params
from CBFETR_Category_Selection import CBFETR_Category_Selection as CategorySelect

def getCashAnalysisColumnValue(moneyFlow, columnName):
    return Params.CALC_SPACE.CalculateValue(moneyFlow, columnName)
    
def formatCashAnalysisColumnValue(moneyFlow, columnName):
    columnValue = getCashAnalysisColumnValue(moneyFlow, columnName)
    try:
        return columnValue.Name()
    except:
        try:
            return columnValue.Value().Number()
        except:
            try:
                return columnValue.Oid()
            except:
                return columnValue

def format_Projected_Money_Flow(moneyFlow, columnName):
    currency = moneyFlow.Currency().Name()
    projected = formatCashAnalysisColumnValue(moneyFlow, columnName)
    
    try:
        decimal = int(Params.CURRENCY_DECIMAL_OVERRIDE[currency])
    except:
        decimal = int(Params.CURRENCY_DECIMAL_DEFAULT)
    
    return round(projected, decimal)

class Message_Detail():
    def __init__(self, moneyFlow):
        if moneyFlow == None:
            self.MoneyFlow = None
            self.Trade = None
            self.Instrument = None
            self.Acquirer = None
            self.Counterparty = None
            self.Category_Class = None
        else:
            self.MoneyFlow = moneyFlow
            self.Trade = self.MoneyFlow.Trade()
            self.Instrument = self.Trade.Instrument()
            self.Acquirer = self.MoneyFlow.Acquirer()
            self.Counterparty = self.MoneyFlow.Counterparty()
            self.Category_Class = CategorySelect(self.MoneyFlow, self.Trade)

        self.Message_Detail = None
        self.getMessageDetail()

    '''---------------------------------------------------------
                    Money Flow Function
    ---------------------------------------------------------'''
    def get_Account_BIC(self, account):
        try:
            accBIC = account.Bic().Name()
        except:
            accBIC = ''
            
        return accBIC

    def get_Acocunt_Number(self, account):
        try:
            accNbr = account.Account()
        except:
            accNbr = ''
        
        return accNbr

    def getMoneyFlow(self, amount):
        flow = 'OUT'
        if amount > 0:
            flow = 'IN'
        return flow

    def get_Trader(self):
        trader = self.MoneyFlow.Trade().Trader()
        if trader and trader.UserGroup():
            if trader.UserGroup().Oid() in Params.SYSTEM_USER_GROUPS:
                trader = Params.SYSTEM_TRADER_NAME
            else:
                trader = trader.Name()
            
        return trader

    def get_Country_Code(self, country, field, account):
        cl_list = acm.FChoiceList.Select("list = 'Country Codes' name = '%s'" %country.upper())
        insType = self.Instrument.InsType()
        code = ''

        if len(cl_list) == 1:             
            country_code = cl_list[0].Description()
            issuer = self.Instrument.Issuer()
        
            if insType in ('Bond', 'FRN') and (issuer and issuer.Country()=='ZA') and self.Category_Class.Category not in Params.NON_REPORTABLE_CATEGORIES \
            and self.Instrument.IssuingPayingAgent() and self.Instrument.IssuingPayingAgent().Name() == 'EUROCLEAR BANK':
                    code = Params.EUROCLEARBANK_BIC_CODE[4:6]

            if field == 'LOCATION_COUNTRY':
                if country_code == 'ZA' or self.Category_Class.Category in Params.NON_REPORTABLE_CATEGORIES:
                    code = ''
                else:
                    code = cl_list[0].Description()
                    
            if field == 'COUNTRY':
                if country_code == 'ZA':
                    code = self.get_Account_BIC(account)[4:6]
                else:
                    code = cl_list[0].Description()

        if code == 'ZA':
            return ''
        else:
            return code
    
    def get_Reporting_Qualifier(self):
        if self.Category_Class.Category in Params.NON_REPORTABLE_CATEGORIES:
            #Removed for AMD 359 and 357
            #if (self.Trade.Portfolio().Name() in Params.EXCEPTION_PORTFOLIOS) \
            #    and (self.Counterparty.BusinessStatus() and self.Counterparty.BusinessStatus().Name() == 'Interbank') \
            #         and (self.Acquirer and self.Acquirer.Name() == 'Money Market Desk'):
            #    return 'INTERBANK'
            #MINT-956 - If trade meets criteria below, the Reporting Qualifier must be INTERBANK
            #elif (self.Acquirer and self.Acquirer.Name() in ('IRD DESK','IRP_FX Desk','NLD DESK')) \
            #    and self.Trade.Portfolio().Name() in ('LTFX','STIRT - FRA FLO','VOE','JN_FX Options','Africa_Curr') \
            #        and self.MoneyFlow.Instrument().InsType() in ('CurrSwap','Swap','Premium'):
            #    return 'INTERBANK'
            if (self.Counterparty.BusinessStatus() and self.Counterparty.BusinessStatus().Name() == 'Interbank') and (self.Acquirer and self.Acquirer.Name() not in Params.TWC_ACQUIRERS):
                return 'INTERBANK'
            else:
                return 'NON REPORTABLE'

        elif self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS  and self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS:
            return 'INTERBANK'
        else:
            return 'BOPCUS'
    
    def is_Gold_Import_Export(self):
        if self.Category_Class.Gold_Import or self.Category_Class.Gold_Export:
            return True
        return False

    def is_Platinum_Import_Export(self):
        if self.Category_Class.Platinum_Import or self.Category_Class.Platinum_Export:
            return True
        return False
        
    def is_Silver_Import_Export(self):
        if self.Category_Class.Silver_Import or self.Category_Class.Silver_Export:
            return True
        return False
        
    def is_Palladium_Import_Export(self):
        if self.Category_Class.Palladium_Import or self.Category_Class.Palladium_Export:
            return True
        return False

    def is_Import_Export_Transaction(self):
        if self.is_Gold_Import_Export() or self.is_Platinum_Import_Export() or self.is_Silver_Import_Export() or self.is_Palladium_Import_Export():
            return True
        return False
    
    def get_Originating_Bank(self, moneyFlowDirection, account):
        originatingBank = ''

        if moneyFlowDirection == 'OUT':
            originatingBank = Params.ABSA_BIC_CODE
        else:
            if moneyFlowDirection == 'IN':
                #MINT-956 - If counterparty = BARCLAYS BANK PLC and Acquirer = IRD DESK or IRP_FX Desk then return alias = BARCGB22
                if self.MoneyFlow.Counterparty().Name() == 'BARCLAYS BANK PLC' and (self.Acquirer and self.Acquirer.Name() in ('IRD DESK', 'IRP_FX')):
                    originatingBank = Params.GB_BIC_CODE

                elif self.Trade.Counterparty().BusinessStatus() and self.Trade.Counterparty().BusinessStatus().Name() == 'Interbank':
                    try:#BOP-28 - In case there are 2 Swift Aliases, use the Counterparty Name --N\A
                        #JIRA 733 - In case there are 2 Swift Aliases, default to blank
                        originatingBank = self.MoneyFlow.Counterparty().SwiftAlias()
                    except:
                        originatingBank = ''
                else:
                    originatingBank = self.get_Account_BIC(account)

        return originatingBank
    
    def get_Receiving_Bank(self, moneyFlowDirection, account):
        receivingBank = ''

        if moneyFlowDirection == 'IN':
            receivingBank = Params.ABSA_BIC_CODE
        else:
            if moneyFlowDirection == 'OUT':
                #MINT-956 - If counterparty = BARCLAYS BANK PLC and Acquirer = IRD DESK or IRP_FX Desk then return alias = BARCGB22
                if self.MoneyFlow.Counterparty().Name() == 'BARCLAYS BANK PLC' and (self.Acquirer and self.Acquirer.Name() in ('IRD DESK', 'IRP_FX')):
                    receivingBank = Params.GB_BIC_CODE

                elif self.Trade.Counterparty().BusinessStatus() and self.Trade.Counterparty().BusinessStatus().Name() == 'Interbank':
                    try:#BOP-28 - In case there are 2 Swift Aliases, use the Counterparty Name
                        receivingBank = self.MoneyFlow.Counterparty().SwiftAlias()
                    except:
                        receivingBank = self.Counterparty.Name()
                else:
                    receivingBank = self.get_Account_BIC(account)

        return receivingBank
    
    def get_Correspondent_Bank(self, account):
        return self.get_Account_BIC(account)
    
    def get_Country_Code_From_BIC(self, BIC_Code, moneyFlowDirection, field, account):

        if field == 'ORIGINATING_COUNTRY':
            return self.get_Original_transaction_Country_Code(BIC_Code, moneyFlowDirection, 'OUT', 'IN', account)

        if field == 'RECEIVING_COUNTRY':
            return self.get_Original_transaction_Country_Code(BIC_Code, moneyFlowDirection, 'IN', 'OUT', account)

        if field == 'CORRESPONDENT_COUNTRY':
            if BIC_Code:
                return BIC_Code[4:6]
        return ''

    def get_Original_transaction_Country_Code(self, BIC_Code, mfDirection, direction1, direction2, account):
        code = ''

        if mfDirection == direction1:
            return 'ZA'
        else:
            if mfDirection == direction2:
                if BIC_Code and (self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS)  and (self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS):
                     return BIC_Code[4:6]

                #MINT-956 - If counterparty = BARCLAYS BANK PLC and Acquirer = IRD DESK or IRP_FX Desk then return alias = BARCGB22
                elif self.MoneyFlow.Counterparty().Name() == 'BARCLAYS BANK PLC' and (self.Acquirer and self.Acquirer.Name() in ('IRD DESK', 'IRP_FX')):
                    code = Params.GB_BIC_CODE[4:6]

                elif self.Trade.Counterparty().BusinessStatus() and self.Trade.Counterparty().BusinessStatus().Name() == 'Interbank':
                    try:#BOP-28 - In case there are 2 Swift Aliases, use the Counterparty Name
                        code = self.MoneyFlow.Counterparty().SwiftAlias()[4:6]
                    except:
                        code = ''
            else:
                    code = self.get_Account_BIC(account)[4:6]

        
        if code == 'ZA' and self.Category_Class.Category not in Params.NON_REPORTABLE_CATEGORIES:
            return ''
        else:
            return code
    
    def get_Trading_Name(self):
        if self.is_Import_Export_Transaction():
            return Params.ENTITY_NAME_ABSA_GOLD
        else:
            return Params.ENTITY_NAME_ABSA

    def get_Year(self):
        try:
            date = ael.date(self.MoneyFlow.PayDate())
        except:
            date = ael.date_today()
        
        return date.to_string('%Y')
        
    def get_Last_Digit_Of_Year(self):
        stringDate = self.get_Year()
        length = len(stringDate)
        
        return stringDate[length - 1]
    
    def replace_String(self, stringValue, stringToReplace, replaceValue):
        return stringValue.replace(stringToReplace, replaceValue)
    
    def get_UCR_Code(self, moneyFlowDirection):
        if moneyFlowDirection == 'IN':
            lastDigitOfYear = self.get_Last_Digit_Of_Year()
            value = Params.UCR
            value = self.replace_String(value, 'Year', lastDigitOfYear)
            value = self.replace_String(value, 'CCN', Params.CUSTOMS_CLIENT_NBR)
            return value
        return ''
    
    def get_Rulings_Sections(self, moneyFlowDirection):
        # ABITFA-5077: Remove hard-coding of ruling section and default to blank
        return Params.RULINGS_SECTION_DEFAULT
    
    def is_Listed_Instrument(self):
        insType = self.Instrument.InsType()
        if insType in ('Stock', 'Bond', 'ETF'):
            if self.Instrument.Isin():
                return True
        return False
    
    def is_Bank(self):
        businessStatus = self.Counterparty.BusinessStatus()
        if businessStatus:
            businessStatusUpper = businessStatus.Name().upper()
            if businessStatusUpper.__contains__('BANK'):
                return True
        return False
    
    def get_BOP_Category(self):
        category = self.Category_Class.Category

        # AMD-8: Do not send through any BoP and Sub Bop category for NONBANK_EXCEPTION_PORTFOLIO and NONBANK_EXCEPTION_ACQUIRERS
        if self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS  and self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS:
            return ''
        elif self.Trade.Acquirer and self.Trade.Acquirer().Name() == 'Gold Desk':
            return ''
        else:
            return category

    def get_Sub_BOP_Category(self):
        if not self.MoneyFlow:
            return ''
        
        category = self.Category_Class.Category

        # AMD-8: Do not send through any BoP and Sub Bop category for NONBANK_EXCEPTION_PORTFOLIO and NONBANK_EXCEPTION_ACQUIRERS
        if self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS  and self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS:
            return ''

        elif self.Trade.Acquirer and self.Trade.Acquirer().Name() == 'Gold Desk':
            return ''            
        elif category == '109':
            if self.is_Silver_Import_Export():
                return '01'
            elif self.is_Gold_Import_Export():
                return '02'
            elif self.is_Platinum_Import_Export() or self.is_Palladium_Import_Export():
                return '03'
                
        elif category == '309':
            return '08'

        elif category in ('601', '603'):
            if self.is_Listed_Instrument() or (self.Instrument.InsType() == 'ETF' and self.MoneyFlow.Type() =='Premium'):
                return '01'
            else:
                return '02'
        elif category in ('610', '611', '612'):
            if is_Bank():
                return '03'
            else:
                return '04'
        elif category in ('701', '702', '703'):
            return '02'
        else:
            return ''
    
    def get_Reportable_Indicator(self):
        if self.get_Reporting_Qualifier() == 'NON REPORTABLE':
            return 'NR'
        return 'RP'

    def get_Legal_Entity_Name (self):
        if self.Instrument.InsType() == 'ETF' and self.MoneyFlow.Currency().Name() in Params.AFRICAN_CURRENCIES and self.Trade.Acquirer().Name() == 'Gold Desk':
            return Params.AFRICA_ENTITY_NAME_ETF
        else:
            return Params.ENTITY_NAME_ABSA
 
    def get_Registration_Number (self):
        if self.Instrument.InsType() == 'ETF' and self.MoneyFlow.Currency().Name() in Params.AFRICAN_CURRENCIES and self.Trade.Acquirer().Name() == 'Gold Desk':
            return Params.REGISTRATION_NBR_ETF
        else:
            return Params.REGISTRATION_NBR_DEFAULT

   
    def get_SARB_Auth_Applic_Number(self):
        if self.Category_Class.Category in Params.NON_REPORTABLE_CATEGORIES:
            return ''
        elif self.Instrument.InsType() == 'ETF' and self.MoneyFlow.Currency().Name() in Params.AFRICAN_CURRENCIES and self.MoneyFlow.Type()=='Premium':
            if self.Trade.Portfolio().Name().upper().__contains__('NEWPLAT'):
                return Params.SARB_AUTH_APPLIC_NUMBER_ETF_PLAT[self.MoneyFlow.Currency().Name()]  
            elif self.Trade.Portfolio().Name().upper().__contains__('NEWGOLD'):
                try:
                    return Params.SARB_AUTH_APPLIC_NUMBER_ETF_GOLD[self.MoneyFlow.Currency().Name()]       
                except:
                    return ''
            else:
                return ''
        else:
            return ''

    
    def get_SARB_Auth_Reference_Number(self):
        if self.Category_Class.Category in Params.NON_REPORTABLE_CATEGORIES:
            return ''
        elif self.Instrument.InsType() == 'ETF' and self.MoneyFlow.Currency().Name() in Params.AFRICAN_CURRENCIES and self.MoneyFlow.Type()=='Premium':
            if self.Trade.Portfolio().Name().upper().__contains__('NEWPLAT'):
                return Params.SARB_AUTH_REF_NUMBER_ETF_PLAT[self.MoneyFlow.Currency().Name()]  
            elif self.Trade.Portfolio().Name().upper().__contains__('NEWGOLD'):
                try:
                    return Params.SARB_AUTH_REF_NUMBER_ETF_GOLD[self.MoneyFlow.Currency().Name()]       
                except:
                    return ''
            else:
                return ''
        else:
            return ''

    def get_ExceptionName(self):
        exception = ''

        if (self.Trade.Portfolio().Name() in Params.EXCEPTION_PORTFOLIOS and (self.Counterparty.BusinessStatus() and self.Counterparty.BusinessStatus().Name() == 'Interbank') and (self.Acquirer and self.Acquirer.Name() in Params.EXCEPTION_ACQUIRERS)) \
        or (self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS  and self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS):
            exception = 'NOSTRO INTERBANK'
        elif (self.Acquirer and (self.Acquirer.Name() == 'COLLATERAL DESK' or self.Acquirer.Name() == 'MONEY MARKET DESK')) and (self.get_Reporting_Qualifier() == 'INTERBANK'):
            exception = 'NOSTRO INTERBANK'
        else:
            exception

        return exception

    def get_Account_Identifier(self, account):
        if self.MoneyFlow and self.Counterparty:
            currency = self.MoneyFlow.Currency().Name()
            foreignPartyChoiceList = self.Counterparty.Free2ChoiceList()
            if foreignPartyChoiceList:

                if currency == 'ZAR'and foreignPartyChoiceList.Name()=='Yes':
                    if self.Counterparty.BusinessStatus() and self.Counterparty.BusinessStatus().Name() == 'Interbank':
                        return Params.ACCOUNT_IDENTIFIER[5]#VOSTRO
                    else:
                        return Params.ACCOUNT_IDENTIFIER[1]#NON RESIDENT RAND
                else:
                    if currency != 'ZAR' and foreignPartyChoiceList.Name()=='Yes' and self.get_Account_BIC(account)[4:6] == 'ZA' and not self.Counterparty.BusinessStatus() or \
                        (self.Counterparty.BusinessStatus() and self.Counterparty.BusinessStatus().Name() != 'Interbank') :
                            return Params.ACCOUNT_IDENTIFIER[4]#NON RESIDENT FCA
                    else:
                            return Params.ACCOUNT_IDENTIFIER[2]#NON RESIDENT OTHER 
            else:
                return Params.ACCOUNT_IDENTIFIER[3]#RES FOREIGN BANK ACCOUNT
        return ''
    



    def get_Import_Control_Number(self, moneyFlowDirection):
        if moneyFlowDirection == 'OUT':
            if self.is_Gold_Import_Export():
                return Params.IMPORT_CONTROL_NUMBER_GOLD
            elif self.is_Platinum_Import_Export():
                return Params.IMPORT_CONTROL_NUMBER_PLATINUM
        return ''
   
    def get_BOPCUS_Detail(self):
        bopcus_detail = {}
        
        #FINSURV - Constants in the FINSURV section based on the Transaction of the BOPCUS XSD.
        bopcus_detail['CUSTOMS_CLIENT_NBR'] = Params.CUSTOMS_CLIENT_NBR
        bopcus_detail['ENVIRONMENT'] = Params.environment
                
        return bopcus_detail
        
    def get_Party_Detail(self, party):
        party_detail = {}
        
        party_detail['ADDRESS'] = ''
        party_detail['ADDRESS2'] = ''
        party_detail['CITY'] = ''
        party_detail['LOCATION_COUNTRY'] = ''
        party_detail['FULLNAME'] = ''
        party_detail['FULLNAME2'] = ''
        party_detail['ZIPCODE'] = ''
        
        if party:
            fullName = party.Fullname()+' '+party.Fullname2()
            party_detail['ADDRESS'] = party.Address()
            party_detail['ADDRESS2'] = party.Address2()
            party_detail['LOCATION_COUNTRY'] = self.get_Country_Code(party.Country(), 'LOCATION_COUNTRY', '')
            party_detail['CITY'] = party.City()
            party_detail['FULLNAME'] = fullName[0:70]
            party_detail['FULLNAME2'] = ''
            party_detail['ZIPCODE'] = party.ZipCode()
            
        return party_detail

    def get_AccountforCorrespondence(self):       
        acc = self.MoneyFlow.AcquirerAccount()
        
        if self.Trade.Portfolio().Name() in Params.NONBANK_EXCEPTION_PORTFOLIOS  and self.Acquirer and self.Acquirer.Name() in Params.NONBANK_EXCEPTION_ACQUIRERS:
            acc = self.MoneyFlow.CounterpartyAccount()
        else:
             acc

        return acc

    def get_MoneyFlow_Detail(self):
        moneyFlow_detail = {}
        
        moneyFlow_detail['ACCOUNT_IDENTIFIER'] = ''
        moneyFlow_detail['ACQUIRER_NAME'] = ''
        moneyFlow_detail['ACQ_ACC_NBR'] = ''
        moneyFlow_detail['AMOUNT'] = ''
        moneyFlow_detail['BOP_CATEGORY'] = ''
        moneyFlow_detail['CORRESPONDENT_BANK'] = ''
        moneyFlow_detail['CORRESPONDENT_COUNTRY'] = ''
        moneyFlow_detail['COUNTRY'] = ''
        moneyFlow_detail['CP_ACC_NBR'] = ''
        moneyFlow_detail['CURRENCY'] = ''
        moneyFlow_detail['EXCEPTION'] = ''
        moneyFlow_detail['FLOW_DIRECTION'] = ''
        moneyFlow_detail['IMPORT_CONTROL_NUMBER'] = ''
        moneyFlow_detail['IS_IMPORT_EXPORT_TRANSACTION'] = ''
        moneyFlow_detail['LEGAL_ENTITY_NAME'] = ''
        moneyFlow_detail['ORIGINATING_BANK'] = ''
        moneyFlow_detail['ORIGINATING_COUNTRY'] = ''
        moneyFlow_detail['PAY_DATE'] = ''
        moneyFlow_detail['RECEIVING_BANK'] = ''
        moneyFlow_detail['RECEIVING_COUNTRY'] = ''
        moneyFlow_detail['REGISTRATION_NUMBER'] = ''
        moneyFlow_detail['REPORTING_QUALIFIER'] = ''
        moneyFlow_detail['RULINGS_SECTION'] = ''
        moneyFlow_detail['SARB_AUTH_APPLIC_NUMBER'] = ''
        moneyFlow_detail['SARB_AUTH_REFERENCE_NUMBER'] = ''
        moneyFlow_detail['SUB_BOP_CATEGORY'] = ''
        moneyFlow_detail['TRADE_ID'] = ''
        moneyFlow_detail['TRADING_NAME'] = ''
        moneyFlow_detail['TRADER'] = ''
        moneyFlow_detail['UCR'] = ''
        
        if self.MoneyFlow:
            acqAccount = self.MoneyFlow.AcquirerAccount()
            cpAccount = self.MoneyFlow.CounterpartyAccount()
            corrAccount = self.get_AccountforCorrespondence()
            projected = format_Projected_Money_Flow(self.MoneyFlow, 'Cash Analysis Projected')
            moneyFlowDirection = self.getMoneyFlow(projected)
            correspondent_Bank = self.get_Correspondent_Bank(corrAccount)
            originating_Bank = self.get_Originating_Bank(moneyFlowDirection, cpAccount)
            receiving_Bank = self.get_Receiving_Bank(moneyFlowDirection, cpAccount)
            cpty = self.Counterparty
            
            moneyFlow_detail['ACCOUNT_IDENTIFIER'] = self.get_Account_Identifier(cpAccount)
            moneyFlow_detail['ACQUIRER_NAME'] = self.Acquirer.Name()
            moneyFlow_detail['ACQ_ACC_NBR'] = self.get_Acocunt_Number(acqAccount)
            moneyFlow_detail['AMOUNT'] = abs(projected)
            moneyFlow_detail['BOP_CATEGORY'] = self.get_BOP_Category()
            moneyFlow_detail['CORRESPONDENT_BANK'] = correspondent_Bank
            moneyFlow_detail['CORRESPONDENT_COUNTRY'] = self.get_Country_Code_From_BIC(correspondent_Bank, moneyFlowDirection, 'CORRESPONDENT_COUNTRY', cpAccount)
            moneyFlow_detail['COUNTRY'] = self.get_Country_Code(cpty.Country(), 'COUNTRY', cpAccount)
            moneyFlow_detail['CP_ACC_NBR'] = self.get_Acocunt_Number(cpAccount)
            moneyFlow_detail['CURRENCY'] = self.MoneyFlow.Currency().Name()
            moneyFlow_detail['EXCEPTION'] = self.get_ExceptionName()
            moneyFlow_detail['FLOW_DIRECTION'] = moneyFlowDirection
            moneyFlow_detail['IMPORT_CONTROL_NUMBER'] = self.get_Import_Control_Number(moneyFlowDirection)
            moneyFlow_detail['IS_IMPORT_EXPORT_TRANSACTION'] = self.is_Import_Export_Transaction()
            moneyFlow_detail['LEGAL_ENTITY_NAME'] = self.get_Legal_Entity_Name()
            moneyFlow_detail['ORIGINATING_BANK'] = originating_Bank
            moneyFlow_detail['ORIGINATING_COUNTRY'] = self.get_Country_Code_From_BIC(originating_Bank, moneyFlowDirection, 'ORIGINATING_COUNTRY', cpAccount)
            moneyFlow_detail['PAY_DATE'] = self.MoneyFlow.PayDate()
            moneyFlow_detail['RECEIVING_BANK'] = receiving_Bank
            moneyFlow_detail['RECEIVING_COUNTRY'] = self.get_Country_Code_From_BIC(receiving_Bank, moneyFlowDirection, 'RECEIVING_COUNTRY', cpAccount)
            moneyFlow_detail['REGISTRATION_NUMBER'] = self.get_Registration_Number()
            moneyFlow_detail['REPORTABLE_IND'] = self.get_Reportable_Indicator()
            moneyFlow_detail['REPORTING_QUALIFIER'] = self.get_Reporting_Qualifier()
            moneyFlow_detail['RULINGS_SECTION'] = self.get_Rulings_Sections(moneyFlowDirection)
            moneyFlow_detail['SARB_AUTH_APPLIC_NUMBER'] = self.get_SARB_Auth_Applic_Number()
            moneyFlow_detail['SARB_AUTH_REFERENCE_NUMBER'] = self.get_SARB_Auth_Reference_Number()
            moneyFlow_detail['SUB_BOP_CATEGORY'] = self.get_Sub_BOP_Category()
            moneyFlow_detail['TRADING_NAME'] = self.get_Trading_Name()
            moneyFlow_detail['TRADER'] = self.get_Trader()
            moneyFlow_detail['UCR'] = self.get_UCR_Code(moneyFlowDirection)
            
            if self.Trade:
                moneyFlow_detail['TRADE_ID'] = self.Trade.Oid()
            
        return moneyFlow_detail
    
    def getMessageDetail(self):
        bopcusDetail = self.get_BOPCUS_Detail()
        counterpartyDetail = self.get_Party_Detail(self.Counterparty)
        moneyFlowDetail = self.get_MoneyFlow_Detail()

        bopcusSection = [('BOPCUS', bopcusDetail)]
        moneyFlowSection = [('MONEY_FLOW', moneyFlowDetail)]
        counterpartySection = [('COUNTERPARTY', counterpartyDetail)]
        
        self.Message_Detail = [bopcusSection, moneyFlowSection, counterpartySection]
