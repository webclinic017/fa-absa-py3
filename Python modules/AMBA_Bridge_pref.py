#
#This file will contain all prefs in the future instead of AMBA_Bridge
#
#
#


""" The choice which messages are transferable via the AMBA_Bridge is stored in 
    dictionaries notBridgeTables and bridgeTables and parameter isTransferableDefault. 
    The choice to send a message or filtered is done by matching the message contents
    against each pattern in bridgeTables and notBridgeTables. If a pattern in bridgeTables
    matches the message the message is sent. If a pattern matches notBridgeTables the 
    message is not sent. If neither bridgeTables or notBridgeTables matches the message
    the setting in isTransferableDefault is used. 
    The pattern is matched using [<message entity>,{<attribute>=<val>,<attribute>=<val>,..}].
    For example the message "[Message][+Trade]PRICE=100[/+Trade][/Message]" matches
    the pattern ["Trade",{}] and ["Trade",{PRICE=100}] but not ["TextObject,{}] or
    ["Trade",{PREMIUM=2546}] or ["Trade",{PREMIUM=50}].
    If several patterns in bridgeTables and notBridgeTables match the message, the best
    match is used. Best match is the match that has the largest number of specified
    attributes. This means that an OTC instrument with name XXX will be matched against
    ['Instrument',{'OTC':'Yes','insid':'XXX'}] and ['Instrument',{'OTC':'Yes'}] but the 
    pattern ['Instrument',{'OTC':'Yes','insid':'XXX'}] determines if the message is sent
    or not.
    
    Correspondingly, FValidation in DEST system then prohibits any changes in 
    transferable tables. FValidation in SOURCE system prohibits changes in 
    non-transferable tables. In case it is too prohibitive, we can allow some tables 
    to be changed by adding them to the lists allowedTablesInSource and 
    allowedTablesInDest. 
    """

isTransferableDefault = 0  # 1 = yes,   0 = no
isInDebugMode = True # print more info

measurePerformance = False


#
#Tables are sent based on bridgeTables and notBridgeTables by best match
#
#Requires that the following line is used in the AMBA
#
#{{leg,payleg},{leg,nominal_at_start},{trade,price},{trade,premium},{orderBook,external_type},{YieldCurve,updat_usrnbr},{Volatility,updat_usrnbr},{Instrument,updat_usrnbr}}
#
bridgeTables = [
                ['Instrument', {}],
                ['Exotic', {}],
                ['ExoticEvent', {}],
                ['Trade', {}],
                ['YieldCurve', {}],
                ['YCSpread', {}],
                ['YCAttribute', {}],
                ['Benchmark', {}],
                ['DividendStream', {}], 
                ['DividendEstimate', {}],
                ['Dividend', {}],
                ['Volatility', {}],
                ['VolatilityCell', {}],
                ['VolatilitySkew', {}],
                ['VolBetaBenchmark', {}],
                ['VolBetaPoint', {}],
                ['VolElement', {}],
                ['VolPoint', {}],
                ['CorrelationMatrix', {}],
                ['CorrelationPoint', {}],
                ['Correlation', {}],
                ['CorrelationBenchmark', {}],
                ['CorrelationCell', {}],
                ['RiskFactorMember', {}],
                ['RiskFactorSpec', {}],
                ['RiskFactorSpecHeader', {}],
                ['AdditionalInfo', {}],
                ['AdditionalInforSpec', {}],
                ['Calendar', {}],
                ['Calendar_date', {}],
                ['Portfolio', {}],
                ['Task', {}],
                ['TaskHistory', {}],
                ['TaskSchedule', {}],
                ['InstrumentAlias', {}],
                #User data
                ['Party', {}],
                ['Agreement', {}],
                ['BrokerFeeRate', {}],
                ['Contact', {}],
                ['CreditLimit', {}],
                ['NettingRule', {}],
                ['NettingRuleLimit', {}],
                ['CurrencyPair', {}],
                ['InstrAliasType', {}]
                ]

#
notBridgeTables =  [['TextObject', {}],
                    ['Price', {}],
                    ['TradeFilter', {}],                    
                    ['Trade', {'INSADDR.INSTYPE':"INS_OPTION",'INSADDR.UND_INSTYPE':"INS_CURR"}],
                    ['Trade', {'INSADDR.INSTYPE':"Option",'INSADDR.UND_INSTYPE':"INS_CURR"}],
                    ['Instrument', {'INSTYPE':"INS_OPTION",'UND_INSTYPE':"INS_CURR"}],
                    ['Instrument', {'INSTYPE':"Option",'UND_INSTYPE':"INS_CURR"}],                    
                    ['Trade', {'TYPE':"TRADE_EXERCISE"}],
                    ['Trade', {'TYPE':"TRADE_ABANDON"}],
                    ['Trade', {'INSADDR.INSTYPE':"INS_DEPOSIT"}],
                    ['Trade', {'INSADDR.INSTYPE':"Deposit"}],
                    ['Instrument', {'INSTYPE':"INS_DEPOSIT"}],
                    ['Instrument', {'INSTYPE':"Deposit"}],                                   
                    ]

print "notBridgeTables:", notBridgeTables
print "bridgeTables:", bridgeTables


#filteredMessageFile = "/opt/front/arena/log/absa4lab_bridge/filtered.log"
filteredMessageFile = "/apps/faapplog/arena/log/jhbpcs00071n01/uat15/filtered.log"

#Change control when using FValidation properly
allowedTablesInSource = ['TextObject']
allowedTablesInDest = []

#Additional optional processing of messages
#Used for custom processing of message parts
#filtered Message Logger is for patching updates not commited properly
extraMessageProcessing = ["fixRemoveBarrierStatus", "mirrorTranslationStrip"]


#
#The date when the old Front 2 database was copied (oldest possible is 1971)
#
databaseCloneTime = "2009-11-14"
#databaseCloneTime = "1990-06-03"


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class AMBA_pref:
    """ 
        Class to easily access all preferences.
        Contains functions for customizing output.

    """
    
    def __init__(self):
            pass
                

    def dMsg(self, msg):
        global isInDebugMode
        if isInDebugMode:
            print "~>", msg

            
    def eMsg(self, msg):
        """
        Error stream out, this is to support message that
        must be altered manually on the machines.
        """
        # could also log to ael.log
        print "E>", msg
        
        

    def useANDSettings(self):
            """Setting to influence how bridge table and not bridge tables are used.
            With AND settings             
            
            """
            return True
    
    
    def extraMessageProcessing(self):
        global extraMessageProcessing
        """Additional message processing"""
        return extraMessageProcessing
    
    def databaseCloneTime(self):
            """Returns the date at which the database was cloned"""
            global databaseCloneTime
            import time
            Format = "%Y-%m-%d"
            ktime = time.mktime(time.strptime(databaseCloneTime, Format))
            return ktime
    
    
    def filterMessageFile(self):
            if("filteredMessageFile" in globals()):
               return globals()["filteredMessageFile"]
            #global filteredMessageFile 
            #return filteredMessageFile
            



