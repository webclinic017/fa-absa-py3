'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Parameters
PROJECT                 :       PACE MM
PURPOSE                 :       Reeds the config settings from PACE_MM_ConfigSettings to determine PROD, UAT.
                                User defined veriables are alse set here.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer         Requester              Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje   PACE MM Project        Initial Implementation
2012-02-28      XXXXXX          Heinrich Cronje   IT                     Sybase Exodus. Determine the environment first to
                                                                         get the correct settings to use.
2012-11-22      603220          Heinrich Cronje   Linton Behari-Ram      PACE MM EOY Deployment
2013-09-26      XXXXXX          Heinrich Cronje   IT                     Fornt Arena UPgrade 2013.3. Remove
                                                                         Utils.LogTrace
2014-09-23                      Matthias Riedel   BARX Non ZAR Project   Added Valid currencies and Funding Instrument type                                                                       
2015-04-29                      Kirsten Good      BARX Non ZAR Project   Set Funding instype for Non ZAR CALL_DEPOSIT = 'Non Zar CFC'
-------------------------------------------------------------------------------------------------------------
DESCRIPTION OF PARAMETERS:

    USER Defined Variables:
    
        VALID_TRADE_STATUS                      :       Trade statuses that will be considered for processing.
        CANCELLATION_TRADE_STATUS               :       Trade statuses that will be used to generate cancellation messages.
        VALID_INSTRUMENT_TYPE                   :       Instrument types that will be considered for processing.
        VALID_ACQUIRER                          :       Acquirers that will be considered for processing.
        VALID_CALL_LEG_TYPE                     :       Leg types that will be considered for Call Account processing.
        VALID_CURRENCIES                        :       Currencies that will be considered for processing.
        FIXED_TERM_DEPOSIT_PORTFOLIO            :       Portfolio that will be used for new Fixed Term Deposits.
        FIXED_TERM_DEPOSIT_FUNDING_INSTYPE      :       Funding Instype that will be used for new Fixed Term Deposits.
        CALL_DEPOSIT_PORTFOLIO                  :       Portfolio that will be used for new Call Deposits.
        CALL_DEPOSIT_FUNDING_INSTYPE            :       Funding Instype that will be used for new Call Deposits.
        CALL_DEPOSIT_REGION                     :       Call Region that will be used for new Call Deposits.
        NOTICE_CALL_DEPOSIT                     :       Funding Instypes for Notice Call Deposits that should be restricted from
                                                        message flows.

    SYSTEM Subscription Values:
    
        subscriptionTablesADS           :       Messages on the specified tables will be considered for processing.
                                                These messages will be created from the ADS.
                                                NOTE: These tables should be the same tables as specified in the AMBA ini.
        subscriptionExternalSource      :       The source of messages that an external system (NOT ADS) will post to the AMB
                                                that should be considered for processing.
    
    INTEGRATION Config Settings:        NOTE: DO NOT change the integration settings. Updates need to be made in the config file.
    
        ambAddress                      :       Host and the port of the AMB where the connections will be made to.
        receiverMBName                  :       Receiver channel name that will receive messages from the AMB.
        receiverSource                  :       Source that will be subscribed to. This should be the same as 
                                                specified in the AMBA ini.
        senderMBName                    :       Sender channel name that will post messages to the AMB.
        senderExternalSource            :       Source that the messages will be posted to so that external systems
                                                can subscribe to the them.
        atsName                         :       Name of the ATS that is running. This will be used to Stop, Start or Restart the ATS from code.
                                                
    SUBSCRIPTION LISTS:
    
        adsSubscriptionList             :       Create a subscription list for messages from the ADS using the
                                                receiverSource and the subscriptionTablesADS. The items in the
                                                list will be used for the subjects of the messages coming from
                                                the ADS.
        subscriptionSourceList          :       Create a subscription list for messages fromt he ADS as well as
                                                any external system that is specified int he parameters.
'''

'''----------------------------------------------------------------------------------------------------------
USER Defined Variables - User can updated variables below.
----------------------------------------------------------------------------------------------------------'''
import acm

VALID_TRADE_STATUS = ['BO Confirmed', 'BO-BO Confirmed', 'Void']

CANCELLATION_TRADE_STATUS = ['Void']

VALID_INSTRUMENT_TYPE = ['Deposit']

VALID_ACQUIRER = ['Funding Desk', 'Money Market Desk']

VALID_CALL_LEG_TYPE = ['Call Fixed Adjustable']

FIXED_TERM_DEPOSIT_PORTFOLIO = 'Term_Unallocated_Pace'

CALL_DEPOSIT_PORTFOLIO = 'Call_Unallocated_Pace'

CALL_DEPOSIT_REGION = 'INST GAUTENG'

NOTICE_CALL_DEPOSIT = ['Call 32 Day notice', 'Call 63 Day notice', 'Call 93 Day notice', 'Call 185 Day notice', 'Call 277 Day notice', 'Call 360 Day notice']

FUNDING_INSTYPE = acm.FDictionary()
# First field is called by "currency == 'ZAR'" 
FUNDING_INSTYPE[True, 'FIXED_TERM_DEPOSIT']='FDE'
FUNDING_INSTYPE[True, 'CALL_DEPOSIT']='Call Deposit NonDTI'
FUNDING_INSTYPE[False, 'FIXED_TERM_DEPOSIT']='Non Zar Deposit'
FUNDING_INSTYPE[False, 'CALL_DEPOSIT']='Non Zar CFC'

VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION = acm.FDictionary()
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['AUD'] = ('AUD Sydney', 'Act/365', 'Money Market Desk')
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['EUR'] = ('EUR Euro', 'Act/360', 'Money Market Desk')
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['GBP'] = ('GBP London', 'Act/365', 'Money Market Desk')
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['JPY'] = ('JPY Tokyo', 'Act/360', 'Money Market Desk')
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['USD'] = ('USD New York', 'Act/360', 'Money Market Desk')
VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION['ZAR'] = ('ZAR Johannesburg', 'Act/365', 'Funding Desk')

VALID_CURRENCIES = VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION.Keys()

'''----------------------------------------------------------------------------------------------------------
SYSTEM Subscription Values - Update variables below only if a new ADS table is added or a new External system.
----------------------------------------------------------------------------------------------------------'''

subscriptionTablesADS = ['INSTRUMENT', 'TRADE']

subscriptionExternalSource = ['MMG_PACE_MM']

'''----------------------------------------------------------------------------------------------------------
INTEGRATION Config Settings - User should NOT update parameters below.
----------------------------------------------------------------------------------------------------------'''

import acm
import xml.dom.minidom as xml
import FOperationsUtils as Utils

environment = None
arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()

'''===========================================================================================================
                                        Get Environment Setting Name
==========================================================================================================='''
environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
environmentSetting = xml.parseString(environmentSettings)
host = environmentSetting.getElementsByTagName('Host')
environment = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]

if len(environment) != 1:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

envSetting = str(environment[0].getAttribute('Setting'))

'''===========================================================================================================
                                            Get Environment Settings
==========================================================================================================='''

configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'PACE_MM_Config_Settings')
config = xml.parseString(configuration)

for element in config.getElementsByTagName('Environment'):
    if element.getAttribute('ArenaDataServer').find(envSetting) >= 0:
        environment = element
        break
else:   
    Utils.Log(True, 'ERROR: Could not find configuration settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find configuration settings for %s.' % arenaDataServer)


try:
    ambAddress = element.getElementsByTagName('Host')[0].firstChild.data + ':' + element.getElementsByTagName('Port')[0].firstChild.data

    receiverMBName = element.getElementsByTagName('ReceiverName')[0].firstChild.data

    receiverSource = element.getElementsByTagName('ReceiverSource')[0].firstChild.data

    senderMBName = element.getElementsByTagName('SenderName')[0].firstChild.data

    senderExternalSource = element.getElementsByTagName('SenderSource')[0].firstChild.data
    
    atsName = element.getElementsByTagName('ATSName')[0].firstChild.data
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

MESSAGE_EVENT_CODES = {     'FIXED_TERM_DEPOSIT_NEW_'                       : 'MMEV0001S',
                            'FIXED_TERM_DEPOSIT_ACKNOWLEDGE_NEW'            : 'MMEV0002S',
                            'FIXED_TERM_DEPOSIT_NOT_ACKNOWLEDGE_NEW'        : 'MMEV0003S',
                            'FIXED_TERM_DEPOSIT_CANCEL_NEW'                 : 'MMEV0004S',
                            'FIXED_TERM_DEPOSIT_ACKNOWLEDGE_CANCEL'         : 'MMEV0005S',
                            'FIXED_TERM_DEPOSIT_NOT_ACKNOWLEDGE_CANCEL'     : 'MMEV0006S',
                            'FIXED_TERM_DEPOSIT_AMENDMENT_NEW'              : 'MMEV0007S',
                            'FIXED_TERM_DEPOSIT_EOD_INTEREST_'              : 'MMEV0008S',
                            'CALL_DEPOSIT_NEW_'                             : 'MMEV0009S',
                            'CALL_DEPOSIT_ACKNOWLEDGE_NEW'                  : 'MMEV00010S',
                            'CALL_DEPOSIT_NOT_ACKNOWLEDGE_NEW'              : 'MMEV00011S',
                            'CALL_DEPOSIT_DEPOSIT_'                         : 'MMEV00012S',
                            'CALL_DEPOSIT_ACKNOWLEDGE_DEPOSIT'              : 'MMEV00013S',
                            'CALL_DEPOSIT_NOT_ACKNOWLEDGE_DEPOSIT'          : 'MMEV00014S',
                            'CALL_DEPOSIT_WITHDRAWAL_'                      : 'MMEV00015S',
                            'CALL_DEPOSIT_ACKNOWLEDGE_WITHDRAWAL'           : 'MMEV00016S',
                            'CALL_DEPOSIT_NOT_ACKNOWLEDGE_WITHDRAWAL'       : 'MMEV00017S',
                            'CALL_DEPOSIT_INTEREST_REINVESTMENT_'           : 'MMEV00018S',
                            'CALL_DEPOSIT_CANCEL_NEW'                       : 'MMEV00019S',
                            'CALL_DEPOSIT_ACKNOWLEDGE_CANCEL'               : 'MMEV00020S',
                            'CALL_DEPOSIT_NOT_ACKNOWLEDGE_CANCEL'           : 'MMEV00021S',
                            'CALL_DEPOSIT_CANCEL_DEPOSIT'                   : 'MMEV00022S',
                            'CALL_DEPOSIT_CANCEL_WITHDRAWAL'                : 'MMEV00023S',
                            'CALL_DEPOSIT_CANCEL_INTEREST_REINVESTMENT'     : 'MMEV00024S',
                            'CALL_DEPOSIT_AMENDMENT_DEPOSIT'                : 'MMEV00025S',
                            'CALL_DEPOSIT_AMENDMENT_WITHDRAWAL'             : 'MMEV00026S',
                            'CALL_DEPOSIT_AMENDMENT_INTEREST_REINVESTMENT'  : 'MMEV00027S',
                            'CALL_DEPOSIT_EOD_INTEREST_'                    : 'MMEV00028S',
                            'CALL_DEPOSIT_AMENDMENT_NEW'                    : 'MMEV00029S'}
                            
PACE_MM_EVENT_ID = acm.FDictionary()

'''----------------------------------------------------------------------------------------------------------
SUBSCRIPTION LISTS - User should not change code below.
----------------------------------------------------------------------------------------------------------'''

adsSubscriptionList = []
for dbTable in subscriptionTablesADS:
    adsSubscriptionList.append(receiverSource + '/' + dbTable)
adsSubscriptionList

subscriptionSourceList = []
for ADS_Table in adsSubscriptionList:
    subscriptionSourceList.append(ADS_Table)
for externalSource in subscriptionExternalSource:
    subscriptionSourceList.append(externalSource)
