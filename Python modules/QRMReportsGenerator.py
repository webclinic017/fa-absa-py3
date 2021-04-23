"""---------------------------------------------------------------------------------------------------------------
Project                 : QRM Extracts
Purpose                 : Extracts to QRM
Department and Desk     : Group Treasury - QRM
Requester               : Sifiso Musundwa
Developer               : Bandile Motha

History
=======

Date            CR                  Developer               Description
====            ======              ================        =============
2015-07-23      CHNG0002988274      Lawrence Mucheka        Added:
                                                                - functionality to combine the output based on a specified 
                                                                  set of trade filters
                                                                - automated generation capabilities
2019-10-10      PCGDEV-140          Qaqamba Ntshobane       Added a date variable
------------------------------------------------------------------------------------------------------------------"""

import acm, ael
from FSQL_functions import FirstBusinessDay
import FBDPGui

def Next_Reset(LegInfo, Day):
    end_days = []
    for v in LegInfo.resets():
        if v.start_day and v.end_day:
            if Day >= v.start_day and Day <= v.end_day:
                end_days.append(v.end_day)
        else:
            if Day >= v.cfwnbr.start_day and Day <= v.cfwnbr.end_day:
                end_days.append(v.cfwnbr.end_day)
    return min(end_days) if end_days else ''


def accumCash(LegInfo, qty, ddate):
    sum = 0
    for lg in LegInfo.cash_flows():
        if lg.end_day <= ddate :
            sum = sum + lg.projected_cf()* qty
    return sum
     
def ts(s):

    return chr(34) + str(s) + chr(34) + ","

def tsl(s):

    return chr(34) + str(s) + chr(34)
    
def td(s):
    return chr(34) + s + chr(34) + ","

fx_rates = {}
def GetLatestPrice(curr):
    if curr in fx_rates:
        return fx_rates[curr]
    else:
        price = acm.FInstrument[curr].UsedPrice(acm.Time().DateToday(), "ZAR", "SPOT")
        fx_rates[curr] = price
        return price

def Lines(t, type, AsOfDay):

    line = ""
    hdrl = ""
    
    hdrl = hdrl  + ts("TRADE_NUMBER")
    line = line  + ts(t.trdnbr)
    
    hdrl = hdrl  +ts("INSTRUMENT_TYPE")
    line = line  + ts(t.insaddr.instype)
    
    hdrl = hdrl  +ts("INSTRUMENT_ID")
    line = line  + ts(t.insaddr.insid)
    
    hdrl = hdrl  +ts("STATUS")
    line = line  + ts(t.status)
    
    hdrl = hdrl  +ts("PORTFOLIO")
    line = line  + ts(t.prfnbr.prfid)
    
    hdrl = hdrl  +ts("COUNTERPARTY_ID")
    line = line +  ts(t.counterparty_ptynbr.ptynbr)
    
    hdrl = hdrl  +ts("COUNTERPARTY_NAME")
    line = line +  ts(t.counterparty_ptynbr.ptyid) 
    
    hdrl = hdrl  +ts("CASH_COLLATERAL_STATUS")
    line = line +  ts("")
    
    hdrl = hdrl  +ts("TRANSACTION_CURRENCY")
    line = line +  ts(t.curr.insid)
    
    hdrl = hdrl  +ts("SETTLEMENT_CURRENCY")
    line = line +  ts(t.curr.insid)
    
    hdrl = hdrl  +ts("FX_RATE")
    line = line +  ts(GetLatestPrice(t.curr.insid))
    
    hdrl = hdrl  + ts("CURRENT_BALANCE_LCY")
    line = line +  ts(t.mtm_value_ins())
    
    hdrl = hdrl  +ts("CURRENT_BALANCE_FCY")
    line = line +  ts(t.mtm_value_ins()) 
    
    hdrl = hdrl  +ts("NOTIONAL_BALANCE")
    line = line +  ts(t.insaddr.contr_size * t.quantity)
    
    hdrl = hdrl  +ts("ORIGINAL_TRADE_DATE")
    line = line +  ts(ael.date_from_time(t.time).to_string('%d/%m/%Y'))
    
    hdrl = hdrl  +ts("ORIGINATION_DATE")
    line = line +  ts(t.acquire_day.to_string('%d/%m/%Y') if t.acquire_day else '')
    
    hdrl = hdrl  +ts("SETTLEMENT_EFFECTIVE_DATE")
    if t.insaddr.instype == 'FRA':

    	line = line +  ts(t.maturity_date().to_string('%d/%m/%Y'))
    else: 
    	line = line +  ts(t.value_day.to_string('%d/%m/%Y'))
    
    hdrl = hdrl  +ts("CONTRACTUAL_MATURITY_DATE")
    if t.insaddr.exp_day:
        line = line +  ts(t.insaddr.exp_day.to_string('%d/%m/%Y'))        
    else:
        line = line +  ts("")        

    hdrl = hdrl  + ts("REPAYMENT_SCHEDULE_NUMBER")
    line = line +  ts("")
    
    hdrl = hdrl  +ts("ACCRUED_INTEREST")
    line = line +  ts(t.interest_accrued())

        
    if t.insaddr.instype == 'Cap' or t.insaddr.instype == 'Floor':   
        hdrl = hdrl  +ts("CAP_FLOOR_COLLAR FLAG")
        line = line +  ts(t.insaddr.instype)
    else:
        hdrl = hdrl  +ts("CAP_FLOOR_COLLAR_FLAG")
        line = line +  ts('None')
    
     
    hdrl = hdrl  + ts("CURRENT_EFFECTIVE_INTEREST_RATE")
    line = line + ts(t.price)
    
    hdrl = hdrl  +ts("CURRENT_GROSS_INTEREST_RATE")
    line = line + ts(t.price)

    hdrl = hdrl  +ts("NEXT_INTEREST_RESET_DATE")
    line = line + ts("")

    hdrl = hdrl  +ts("INTEREST_RESET_FREQUENCY")
    line = line + ts("")
    
    hdrl = hdrl  +ts("PAYMENT_CONVENTION")
    line = line + ts("")
    
    hdrl = hdrl  +ts("INITIAL_CAP_ON_INTEREST_RATE")
    if t.used_rate():
        line = line + ts(t.used_rate())
    else:   line = line + ts("")
    
    hdrl = hdrl  +ts("INITIAL_FLOOR_ON_INTEREST_RATE")
    if t.used_rate():
        line = line + ts(t.used_rate())
    else:   line = line + ts("")
    
    hdrl = hdrl  +ts("LIFETIME_CAP_ON_INTEREST_RATE")
    if t.used_rate():
        line = line + ts(t.used_rate())
    else:   line = line + ts("")
    
    hdrl = hdrl  +ts("LIFETIME_FLOOR_ON_INTEREST_RATE") 
    if t.used_rate():
        line = line + ts(t.used_rate())
    else:   line = line + ts("")
    
    hdrl = hdrl  +ts("NEXT_INTEREST_PAYMENT_DATE")
    line = line + ts("")
    
    hdrl = hdrl  +ts("PAYMENT_FREQUENCY")
    line = line + ts("") 
    
    hdrl = hdrl  +ts("NEXT_OPTION_EXERCISE_DATE") 
    line = line + ts("")
    
    hdrl = hdrl  +ts("YIELD_CURVE") 
    line = line +  ts("")
    
    hdrl = hdrl  +ts("STRIKE_PRICE") 
    line = line +  ts(t.insaddr.strike_price)
    
    hdrl = hdrl  +ts("INDUSTRY_IDENTIFIER")
    line = line + ts("")
    
    hdrl = hdrl  +ts("REGION_OF_TRANSACTION") 
    line = line + ts("South Africa")
    
    
    hdrl = hdrl  +ts("ISSUE_PRICE") 
    line = line +  ts(t.insaddr.used_price())
    
    hdrl = hdrl  +ts("UNITS_OF_UNDERLYING") 
    line = line +  ts(t.insaddr.contr_size)  
    
    hdrl = hdrl  +ts("MARKET_PRICE") 
    line = line +  ts(t.insaddr.mtm_price())
    
    hdrl = hdrl  +ts("INTERNAL_TRANSACTION_FLAG") 
    line = line +  ts(t.insaddr.rate_type)
    
    hdrl = hdrl  +ts("COUNTERPARTY_SUB_PORTFOLIO") 
    line = line +  ts(t.prfnbr.prfid)         
    

    if t.settlements(): 
    
        hdrl = hdrl  +ts("SALEPERSON_NAME") 
        line = line +  ts(t.settlements()[0].owner_usrnbr.name)
        
        hdrl = hdrl  +ts("SALEPERSON_DESCRIPTION") 
        line = line +  ts(t.settlements()[0].owner_usrnbr.name)
        
        hdrl = hdrl  +ts("SALES_INCOME") 
        line = line +  ts(t.settlements()[0].amount)
        
        hdrl = hdrl  +ts("BRAINS_FLEX_SETTLEMENT_ACCOUNT_NUMBER") 
        line = line +  ts(t.settlements()[0].acquirer_account) 
    else:
    
        hdrl = hdrl  +ts("SALEPERSON_NAME") 
        line = line +  ts("None")
        
        hdrl = hdrl  +ts("SALEPERSON_DESCRIPTION") 
        line = line +  ts("None")
        
        hdrl = hdrl  +ts("SALES_INCOME") 
        line = line +  ts("None")
        
        hdrl = hdrl  +ts("BRAINS_FLEX_SETTLEMENT_ACCOUNT_NUMBER") 
        line = line +  ts("None")
        
        
    hdrl = hdrl  +ts("CREATED_DATE") 
    line = line +  ts(ael.date_from_time(t.creat_time).to_string('%d/%m/%Y')) 
    
    hdrl = hdrl  +ts("EXECUTION_DATE") 
    line = line +  ts(t.acquire_day.to_string('%d/%m/%Y') if t.acquire_day else '')
    
    hdrl = hdrl  +ts("CUSTOMER_ADDRESS") 
    line = line +  ts(t.creat_usrnbr.email)
    
    hdrl = hdrl  +ts("GROUP_REFERENCE_NUMBER") 
    line = line + ts("")
    
    hdrl = hdrl  +ts("USER_ID_OF_OPERATOR") 
    line = line +  ts(t.creat_usrnbr.userid)
    
    
    
    
#*************
    
    if len(t.insaddr.legs()) == 2:
        hdrl = hdrl  +ts("LEG1_NUMBER")
        line = line +  ts(t.insaddr.legs()[0].legnbr)
        
        hdrl = hdrl  +ts("LEG1_INTEREST_DAY_COUNT_BASIS")
        line = line + ts(t.insaddr.legs()[0].daycount_method)
        
        hdrl = hdrl  +ts("LEG1_PAYLEG") 
        line = line +  ts(bool(t.insaddr.legs()[0].payleg)).upper()
        
        hdrl = hdrl  +ts("LEG1_TYPE") 
        line = line +  ts(t.insaddr.legs()[0].type)

        
#*************    
        hdrl = hdrl  + ts("LEG1_AMORTISATION_TYPE")
        line = line + ts(t.insaddr.legs()[0].amort_type)
            
        hdrl = hdrl  +ts("LEG1_AMORTIZATION_RATE") 
        line = line + ts(t.insaddr.legs()[0].annuity_rate)    
            
        hdrl = hdrl  +ts("LEG1_GROSS_MARGIN")
        line = line +  ts(t.insaddr.legs()[0].spread)
            
        hdrl = hdrl  +ts("LEG1_FLOAT_REF")
        line = line +  ts(t.insaddr.legs()[0].display_id('float_rate'))
         
        hdrl = hdrl  +ts("LEG1_NEXT_RESET")
        if Next_Reset(t.insaddr.legs()[0], AsOfDay):
            line = line +  ts(Next_Reset(t.insaddr.legs()[0], AsOfDay).to_string('%d/%m/%Y'))
        else: 
            line = line +  ts("")
           
        hdrl = hdrl  +ts("LEG1_RATE")
        if t.insaddr.legs()[0].type == "Float":
            line = line +  ts(t.insaddr.legs()[0].float_rate.used_price())
        else:
            line = line +  ts(t.insaddr.legs()[0].fixed_rate)
            
        hdrl = hdrl  +ts("LEG1_ROLLING_PERIOD")
        line = line +  ts(t.insaddr.legs()[0].rolling_period)
        
        
        hdrl = hdrl  +ts("LEG1_PAYMENT_METHOD")
        line = line +  ts(t.insaddr.legs()[0].pay_day_method)
            
        hdrl = hdrl  +ts("LEG1_CURRENT_BALANCE")
        if t.insaddr.instype == 'Bond':
		line = line +  ts(t.mtm_value_ins())
	else:
	    line = line +  ts(accumCash(t.insaddr.legs()[0], t.quantity, AsOfDay))
             
        hdrl = hdrl  +ts("LEG1_NOMINAL")
        line = line +  ts(t.insaddr.contr_size * t.quantity)
            
        hdrl = hdrl  +ts("LEG1_CURRENCY")
        line = line +  ts(t.insaddr.legs()[0].curr.insid)
        
        
        
        hdrl = hdrl  +ts("LEG2_NUMBER")
        line = line +  ts(t.insaddr.legs()[1].legnbr)
        
        hdrl = hdrl  +ts("LEG2_INTEREST_DAY_COUNT_BASIS")
        line = line + ts(t.insaddr.legs()[1].daycount_method)
        
        hdrl = hdrl  +ts("LEG2_PAYLEG") 
        line = line +  ts(bool(t.insaddr.legs()[1].payleg)).upper()

        hdrl = hdrl  +ts("LEG2_TYPE") 
        line = line +  ts(t.insaddr.legs()[1].type)
        
        hdrl = hdrl  + ts("LEG2_AMORTISATION_TYPE")
        line = line + ts(t.insaddr.legs()[1].amort_type)
            
        hdrl = hdrl  +ts("LEG2_AMORTIZATION_RATE") 
        line = line + ts(t.insaddr.legs()[1].annuity_rate)    

            
        hdrl = hdrl  +ts("LEG2_GROSS_MARGIN")
        line = line +  ts(t.insaddr.legs()[1].spread)
        
        hdrl = hdrl  +ts("LEG2_FLOAT_REF")
        line = line +  ts(t.insaddr.legs()[1].display_id('float_rate'))
        
        hdrl = hdrl  +ts("LEG2_NEXT_RESET")
        if Next_Reset(t.insaddr.legs()[1], AsOfDay):
            line = line +  ts(Next_Reset(t.insaddr.legs()[1], AsOfDay).to_string('%d/%m/%Y'))
        else:
            line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_RATE")
        
        if t.insaddr.legs()[1].type == 'Float':
            line = line +  ts(t.insaddr.legs()[1].float_rate.used_price())
        else:
            line = line +  ts(t.insaddr.legs()[1].fixed_rate)
            
        hdrl = hdrl  +ts("LEG2_ROLLING_PERIOD")
        line = line +  ts(t.insaddr.legs()[1].rolling_period)
        
        hdrl = hdrl  +ts("LEG2_PAYMENT_METHOD")
        line = line +  ts(t.insaddr.legs()[1].pay_day_method)
            
        hdrl = hdrl  +ts("LEG2_CURRENT_BALANCE")
        line = line +  ts(accumCash(t.insaddr.legs()[1], t.quantity, AsOfDay))
            
        hdrl = hdrl  +ts("LEG2_NOMINAL")
        line  = line + ts(t.insaddr.contr_size * t.quantity)
           
        hdrl = hdrl  +ts("LEG2_CURRENCY")
        line = line +  ts(t.insaddr.legs()[1].curr.insid)            
            
  

        
    elif len(t.insaddr.legs()) == 1:
    
        hdrl = hdrl  +ts("LEG1_NUMBER")
        line = line +  ts(t.insaddr.legs()[0].legnbr)
        
        hdrl = hdrl  +ts("LEG1_INTEREST_DAY_COUNT_BASIS")
        line = line + ts(t.insaddr.legs()[0].daycount_method)
        
        hdrl = hdrl  +ts("LEG1_PAYLEG") 
        line = line +  ts(bool(t.insaddr.legs()[0].payleg)).upper()
        
        hdrl = hdrl  +ts("LEG1_TYPE") 
        line = line +  ts(t.insaddr.legs()[0].type)
        
        
#************
        hdrl = hdrl  + ts("LEG1_AMORTISATION_TYPE")
        line = line + ts(t.insaddr.legs()[0].amort_type)
            
        hdrl = hdrl  +ts("LEG1_AMORTIZATION_RATE") 
        line = line + ts(t.insaddr.legs()[0].annuity_rate)    
            
        hdrl = hdrl  +ts("LEG1_GROSS_MARGIN")
        line = line +  ts(t.insaddr.legs()[0].spread)
            
        hdrl = hdrl  +ts("LEG1_FLOAT_REF")
        line = line +  ts(t.insaddr.legs()[0].display_id('float_rate'))
        
        hdrl = hdrl  +ts("LEG1_NEXT_RESET")
        if Next_Reset(t.insaddr.legs()[0], AsOfDay):
            line = line +  ts(Next_Reset(t.insaddr.legs()[0], AsOfDay).to_string('%d/%m/%Y'))
        else:
            line = line +  ts("")
        
            
        hdrl = hdrl  +ts("LEG1_RATE")
        if t.insaddr.legs()[0].type == 'Float':
            line = line +  ts(t.insaddr.legs()[0].float_rate.used_price())
        else:
            line = line +  ts(t.insaddr.legs()[0].fixed_rate)
            
        hdrl = hdrl  +ts("LEG1_ROLLING_PERIOD")
        line = line +  ts(t.insaddr.legs()[0].rolling_period)
        
        hdrl = hdrl  +ts("LEG1_PAYMENT_METHOD")
        line = line +  ts(t.insaddr.legs()[0].pay_day_method)
            
        hdrl = hdrl  +ts("LEG1_CURRENT_BALANCE")
        line = line +  ts(accumCash(t.insaddr.legs()[0], t.quantity, AsOfDay))
            
        hdrl = hdrl  +ts("LEG1_NOMINAL")
        line = line +  ts(t.insaddr.contr_size * t.quantity)
            
        hdrl = hdrl  +ts("LEG1_CURRENCY")
        line = line +  ts(t.insaddr.legs()[0].curr.insid)            
  
        
        hdrl = hdrl  +ts("LEG2_NUMBER")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_INTEREST_DAY_COUNT_BASIS")
        line = line + ts("")
            
        hdrl = hdrl  +ts("LEG2_PAYLEG") 
        line = line +  ts("")

        hdrl = hdrl  +ts("LEG2_TYPE") 
        line = line +  ts("")
            
        hdrl = hdrl  + ts("LEG2_AMORTISATION_TYPE")
        line = line + ts(" ")

        hdrl = hdrl  +ts("LEG2_AMORTIZATION_RATE") 
        line = line + ts("")    
    
        hdrl = hdrl  +ts("LEG2_GROSS_MARGIN")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_FLOAT_REF")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_NEXT_RESET")
        line = line +  ts("")    
        
        hdrl = hdrl  +ts("LEG2_RATE")
        line = line +  ts("None")
            
        hdrl = hdrl  +ts("LEG2_ROLLING_PERIOD")
        line = line +  ts("")
       
        hdrl = hdrl  +ts("LEG2_PAYMENT_METHOD")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_CURRENT_BALANCE")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_NOMINAL")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_CURRENCY")
        line = line +  ts("")        
            
        
        
    elif len(t.insaddr.legs()) == 0:

        hdrl = hdrl  +ts("LEG1_NUMBER")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG1_INTEREST_DAY_COUNT_BASIS")
        line = line + ts("")
        
        hdrl = hdrl  +ts("LEG1_PAYLEG") 
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG1_TYPE") 
        line = line +  ts("")
        
        hdrl = hdrl  + ts("LEG1_AMORTISATION_TYPE")
        line = line + ts(" ")
        
        hdrl = hdrl  +ts("LEG1_AMORTIZATION_RATE") 
        line = line + ts("")    

            
        hdrl = hdrl  +ts("LEG1_GROSS_MARGIN")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG1_FLOAT_REF")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG1_NEXT_RESET")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG1_RATE")
        line = line +  ts("None")
            
        hdrl = hdrl  +ts("LEG1_ROLLING_PERIOD")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG1_PAYMENT_METHOD")
        line = line +  ts("")
 
        hdrl = hdrl  +ts("LEG1_CURRENT_BALANCE")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG1_NOMINAL")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG1_CURRENCY")
        line = line +  ts("")
        
# Leg2 ==========================================Leg2 
        hdrl = hdrl  +ts("LEG2_NUMBER")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_INTEREST_DAY_COUNT_BASIS")
        line = line + ts("")
        
        hdrl = hdrl  +ts("LEG2_PAYLEG") 
        line = line +  ts("")

        hdrl = hdrl  +ts("LEG2_TYPE") 
        line = line +  ts("")
        
        hdrl = hdrl  + ts("LEG2_AMORTISATION_TYPE")
        line = line + ts(" ")
        
        hdrl = hdrl  +ts("LEG2_AMORTIZATION_RATE") 
        line = line + ts("")    
    
        hdrl = hdrl  +ts("LEG2_GROSS_MARGIN")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_FLOAT_REF")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_NEXT_RESET")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_RATE")
        line = line +  ts("None")
            
        hdrl = hdrl  +ts("LEG2_ROLLING_PERIOD")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_PAYMENT_METHOD")
        line = line +  ts("")
        
        hdrl = hdrl  +ts("LEG2_CURRENT_BALANCE")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_NOMINAL")
        line = line +  ts("")
            
        hdrl = hdrl  +ts("LEG2_CURRENCY")
        line = line +  ts("")
# Leg2 ==========================================Leg2 

    hdrl = hdrl  +ts("MANUAL_CASHFLOW")
    if t.insaddr.legs():
        line = line +  ts(t.insaddr.legs()[0].manually_edited_cf())
    else: 
        line = line +  ts("0")

    hdrl = hdrl  +ts("ASOFDATE")
    line = line +  tsl(AsOfDay.to_string('%d/%m/%Y'))

    if type == 'h':
        return hdrl + "\n"
    else:
        return line + "\n"
        

def GenerateHeader(headerMap, fileRoot):
    """ 
        Generates the header file for all the transactional files. 
        The header file contains count of trades for each file 
    """

    if headerMap:
        fileName = 'constreasuryhdr.done'
        fullFileName = '{0}{1}'.format(fileRoot, fileName)
        try:
            headerfile = open(fullFileName, 'w')         
            map(lambda key: 
                headerfile.write('{0}{1}'.format(key, headerMap[key]) + '\n'), headerMap.keys()) 
            
            print 'Wrote secondary output to: %s' %(fullFileName)                                  
        except Exception, e:
            print 'Error writing output to: %s' %(fullFileName), e
        finally:
            headerfile.close()
            

def GenerateMain(root, treasuryFilters, cibFilters, validStatuses, asOfDate, headerMap):
    """ 
        Generates the transactional files based on the input Trade filters  
    """ 
    
    fileFilterMap = {
                        'constreasury':('.csv', treasuryFilters),                                
                        'cib_download':('.csv', cibFilters)
                    }

    for key in fileFilterMap.keys(): 
        ext = fileFilterMap[key][0]       
        name = '{0}{1}'.format(key, ext)
        dateInclusiveName = '{0}_{1}{2}'.format(key, asOfDate.to_string('%Y%m%d'), ext)
        fullName = '{0}{1}'.format(root, name)

        outfile = open(fullName, 'w')
        try:            
            isHeaderWritten = False
            totalRecordCount = 0
            for tradeFilter in fileFilterMap[key][1]:
                trades = ael.TradeFilter[tradeFilter].trades()
                totalRecordCount += len(trades)
            
                if(not isHeaderWritten):
                    outfile.write(Lines(trades[0], "h", asOfDate))
                    isHeaderWritten = True

                map(lambda trade: outfile.write(Lines(trade, "l", asOfDate)), 
                    filter(lambda t:t.status in validStatuses, trades))                 
                headerMap.update({dateInclusiveName:'|{0}'.format(totalRecordCount)})
            
            print 'Wrote secondary output to: %s' %(fullName)
        except Exception, e:
            print 'Error writing output to: %s' %(fullName), e         
        finally:
            outfile.close()
            

ael_variables = FBDPGui.DefaultVariables(
                ['fileRoot', 'File Root', 
                    'string', None, '/services/frontnt/Task/', 1, 0, '', None, 1],
                ['treasuryTradeFilters', 'Treasury Trade Filters(CSV)', 
                    'string', None, 'QRM_CIB_SWAP,QRM_2', 1, 0, '', None, 1],
                ['cibTradeFilters', 'CIB Trade Filters(CSV)', 
                    'string', None, 'cib_download_Megan,QRM_CIB2', 1, 0, '', None, 1],
                ['tradeStatuses', 'Trade Statuses(CSV)', 
                    'string', None, 'FO Confirmed,BO Confirmed,BO-BO Confirmed', 
                        1, 0, '', None, 1],
                ['asOfDate', 'As of Date',
                    'date', None, ael.date_today(), 
                        1, 0, '', None, 1]
                )

def ael_main(dict):
    """ Main method """

    try:
        fileRoot = dict['fileRoot']
        treasuryFilters = dict['treasuryTradeFilters'].split(',')
        cibFilters = dict['cibTradeFilters'].split(',')
        validStatuses = dict['tradeStatuses'].split(',')
        asOfDate = dict['asOfDate']
    except:
        return 'Could not get parameter values!'

    headerMap = {}

    GenerateMain(fileRoot, treasuryFilters, cibFilters, validStatuses, asOfDate, headerMap)
    GenerateHeader(headerMap, fileRoot)
