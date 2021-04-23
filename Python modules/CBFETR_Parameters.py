'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Parameters
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       Reads the config settings from CBFETR_ConfigSettings to determine PROD, UAT.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2012-06-25      281782          Heinrich Cronje                 Added field ENTITY_NAME_ABSA and ENTITY_NAME_ABSA_GOLD
                                                                to parameter list.
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade
2013-09-26	    XXXXXX		    Heinrich Cronje			        Front Arena Upgrade 2013.3. Removed Utils.LogTrace.
2014-08-10      CHNG0002238567	Melusi Maseko                   BOPCUS ETF and Gold Enhancements 
2015-03-25      BOP-15          Melusi Maseko                   Removed SARB_AUTH_APPLIC_NUMBER_GOLD
2015-05-06      BOP-10          Melusi Maseko                   Country code changes - Added EUROCLEAR BANK BIC Code
2015-06-03      BOP-13          Melusi maseko                   Ammended parameter ACCOUNT_IDENTIFIER as per JIRA
2016-06-20      MINT-673        Melusi Maseko                   Added EXCEPTION_PORTFOLIO for exception names
2016-07-18      MINT-733        Melusi Maseko                   Added additional EXCEPTION_PORTFOLIO and EXCEPTION_ACQUIRERS
2016-09-27      MINT-956        Melusi Maseko                   Added BIC CODE for BARCLAYS BANK PLC
2017-04-18      MINT-1004       Nelusi Maseko                   Default the Ruling Section from B2BIV to blank
2018-05-25      AMD-222         Melusi Maseko                   Added a list of all LCH portfolios 
2018-06-12      AMD-8	        Melusi Maseko                   Add NONBANK_EXCEPTION_PORTFOLIO 'DT Vanilla Trade Loans Non ZAR' and'Supplier Finance Non ZAR' 
                                                                Add NONBANK_EXCEPTION_ACQUIRERS 'TWC DT','TWC SF'
-------------------------------------------------------------------------------------------------------------
DESCRIPTION OF PARAMETERS:

    INTEGRATION Config Settings:        NOTE: DO NOT change the integration settings. Updates need to be made in the config file.
    
        atsName                             :       Name of the ATS that will be running.
        environment                         :       T or P. Where T is test data and P is droduction data.
        FAEnvironment                       :       Describes the Front Arena environemtn, DEV, UAT, PRD or DR.
        ambAddress                          :       Host and the port of the AMB where the connections will be made to.
        senderMBName                        :       Sender channel name that will post messages to the AMB.
        senderSource                        :       Source that the messages will be posted to so that external systems
                                                    can subscribe to the them.
        receiverMBName                      :       Receiver channel name that will be used to receive messages from the AMB.
        receiverSource                      :       Source that would be subscribed to when receiving messages from the AMB via the
                                                    receiver channel.
        requestServiceAddress               :       The NET.TCP Address of the Request Service.

    SYSTEM Defined Variables:           NOTE: DO NOT change the System Defined Variables.
    
        CALC_SPACE                          :       Calculation space that will be used for calculations. The FMoneyFlowSheet is used.

        MEMORY_THRESHOLD                    :       Threshold used to determine when the ATS should be restarted.
        
        SYSTEM_USER_GROUPS                  :       Integration Process, System Processes. If a trade is booked by one the these users,
                                                    the signatures on the message will default to Front Arena and not the trader id.
                                                
    CONSTANTS:                          NOTE: Change these veriables only when instructed from SARB
    
        FUNCTIONS - Constants/Variables used by functions to determine field values.
        
            ACCOUNT_IDENTIFIER              :       Describes the type of foreign account.

            ABSA_BIC_CODE                   :       BIC Code of ABSA BANK LIMITED

            GB_BIC_CODE                     :       BIC Code of BARCLAYS BANK PLC
                    
            CURRENCY_DECIMAL_DEFAULT        :       Default decimal places to be used during rounding. (format_Projected_Money_Flow)
            
            CURRENCY_DECIMAL_OVERRIDE       :       Defines the amount of decimals per currency if different from default rounding. 
                                                    (format_Projected_Money_Flow)
                                                    
            CUSTOMS_CLIENT_NBR              :       The Customs Client Number of the relevant individual exported/importer.
                                                    
            ENTITY_NAME_ABSA                :       Entity name that will be used for all Acquirer's Fullname on the message on non Gold Transactions.

            AFRICA_ENTITY_NAME_ETF          :       Entity name that will be used for ETFs in AFRICAN CURRENCIES
            
            IMPORT_CONTROL_NUMBER_GOLD      :       Import Control Number used for Gold Curr Trades.
            
            IMPORT_CONTROL_NUMBER_PLATINUM  :       Import Control Number used for Platinum Curr Trades.
            
            NON_REPORTABLE_CATEGORIES       :       List of categories that represents NON REPORTABLE transactions.
            
            RULINGS_SECTION_DEFAULT         :       Relevant section in the Exchange Control Rulings. Default value for ABSA
            
            SARB_AUTH_APPLIC_NUMBER_GOLD    :       Financial Surveillance Department approval number for Gold Transactions.
            
            SARB_AUTH_REF_NUMBER_GOLD       :       e-Docx Number where the Financial Surveillance Department approved an application.
                                                    
            SARB_AUTH_APPLIC_NUMBER_ETF    :       The authorization application number should be the stated values for those specific stated currencies
            
            SARB_AUTH_REF_NUMBER_ETF        :       The authorization reference should be the stated values for those specific stated currencies

            SYSTEM_TRADER_NAME              :       If the trader of a trade is part of SYSTEM_USER_GROUPS then the signature will be
                                                    set to this variable. (get_Trader)
                                                    
            UCR                             :       UCR code in respect to Gold Exports.





            EUROCLEARBANK_BIC_CODE          :       BIC Code of EUROCLEAR BANK

            AFRICAN_CURRENCIES              :       List of African Currencies used to define ETF Categories.

            ENTITY_NAME_ABSA_GOLD           :       Entity name that will be used for all Acquirer's Fullname on the message on Gold Transactions.

            REGISTRATION_NBR_ETF            :       The registration number that will be used for ETFs in AFRICAN CURRENCIES
            
            FUNDING_INSTYPE_OVERRIDES       :       Funding Instypes on Deposits that requires an override of the deposit category mapping.
            
            GOLD_CAT201_PARTIES             :       Parties that should be reported as category 201 for Gold transactions.
            
            MERCHANDISE_EXPORT_CATEGORY     :       To define Location Qualifier for merchandise exports

            MERCHANDISE_IMPORT_CATEGORY     :       To define Location Qualifier for merchandise imports

            MONEYFLOW_TYPE_EXCLUSION        :       List of money Flow types that should not be reported on.
            
            PRECIOUS_METALS_CURRENCIES      :       List of all the Precious Metal Currencies that should be reported.
            
            PREVENT_COUNTERPARTY            :       List of Party Names that will be excluded from selection for Money Flows.

            REGISTRATION_NBR_DEFAULT        :       Default registration number

            REGISTRATION_NBR_ETF            :       Default registration number used for ETFs
                                    
            VALID_CURRENCIES                :       Currencies that are valid to do reporting on.

            EXCEPTION_PORTFOLIO             :       Valid Portfolios for Exception Name

			LCH_PORTFOLIOS                  :       List of all LCH portfolios 
            
			NONBANK_EXCEPTION_PORTFOLIO     :       Valid Portfolios for non-bank Counterparties

            NONBANK_EXCEPTION_ACQUIRERS     :       Valid Acquirers for non-bank Counterparties
            
'''

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
configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'CBFETR_Config_Settings')
config = xml.parseString(configuration)

for element in config.getElementsByTagName('Environment'):
    if element.getAttribute('ArenaDataServer').find(envSetting) >= 0:
        environment = element
        break
else:   
    Utils.Log(True, 'ERROR: Could not find configuration settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find configuration settings for %s.' % arenaDataServer)

try:
    atsName = element.getElementsByTagName('ATSName')[0].firstChild.data
    
    ambAddress = element.getElementsByTagName('Host')[0].firstChild.data + ':' + element.getElementsByTagName('Port')[0].firstChild.data

    environment = element.getElementsByTagName('Environment')[0].firstChild.data
    
    FAEnvironment = element.getElementsByTagName('FAEnvironment')[0].firstChild.data
    
    senderMBName = element.getElementsByTagName('SenderName')[0].firstChild.data

    senderSource = element.getElementsByTagName('SenderSource')[0].firstChild.data
    
    receiverMBName = element.getElementsByTagName('ReceiverName')[0].firstChild.data

    receiverSource = [element.getElementsByTagName('ReceiverSource')[0].firstChild.data]
    
    requestServiceAddress = element.getElementsByTagName('RequestServiceAddress')[0].firstChild.data
except:
    Utils.Log(True, 'ERROR: Could not find environment settings for %s.' % arenaDataServer)
    raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

'''----------------------------------------------------------------------------------------------------------
SYSTEM Defined Variables - User should NOT updated variables below.
----------------------------------------------------------------------------------------------------------'''

CALC_SPACE = acm.FCalculationSpaceCollection().GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())

MEMORY_THRESHOLD = 800000

SYSTEM_USER_GROUPS = [494, 495]

'''----------------------------------------------------------------------------------------------------------
CONSTANTS - User should updated variables only from instructions via SARB or Business.
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
                    FUNCTIONS - Constants used by functions to determine field values.
----------------------------------------------------------------------------------------------------------'''

ACCOUNT_IDENTIFIER = {1 : 'NON RESIDENT RAND',  #Foreign Party Currency ZAR
                    2 : 'NON RESIDENT OTHER',   #Foreign Party Currency Not ZAR
                    3 : 'RES FOREIGN BANK ACCOUNT', #Local Party Currency Not ZAR
                    4 : 'NON RESIDENT FCA',
                    5 : 'VOSTRO'}

ABSA_BIC_CODE = 'ABSAZAJJ'

GB_BIC_CODE = 'BARCGB22'

EUROCLEARBANK_BIC_CODE = 'MGTCBEBE'

AFRICA_ENTITY_NAME_ETF = 'NEWGOLD ISSUER LIMITED'

CURRENCY_DECIMAL_DEFAULT = '2'

CURRENCY_DECIMAL_OVERRIDE = {'JPY' : '0'}

CUSTOMS_CLIENT_NBR = '01192884'

ENTITY_NAME_ABSA = 'ABSA BANK LIMITED'

ENTITY_NAME_ABSA_GOLD = 'ABSA GOLD DESK'

IMPORT_CONTROL_NUMBER_GOLD = 'XXX201301070000413'
            
IMPORT_CONTROL_NUMBER_PLATINUM  = 'XXX201305030014547'
            
NON_REPORTABLE_CATEGORIES = ['900']

REGISTRATION_NBR_DEFAULT = '198600479406'

REGISTRATION_NBR_ETF = '2004/014199/06'

RULINGS_SECTION_DEFAULT = ''

RULINGS_SECTION_ETF_CASH = 'B.14(H)(i)'

RULINGS_SECTION_PRECIOUS_METALS = 'B.1(C)'

SARB_AUTH_APPLIC_NUMBER_GOLD = ''

SARB_AUTH_REF_NUMBER_GOLD = ''

SARB_AUTH_APPLIC_NUMBER_ETF_GOLD = { 'GHS' : '5089',

                                    'NGN' : '5086',
                                    'BWP' : '11604',
                                    'MUR' : '5266'}

SARB_AUTH_REF_NUMBER_ETF_GOLD = {'GHS' : '2011-040651',
                                'NGN' : '2011-040650',
                                'BWP' : '2009-069566',
                                'MUR' : '2013-000065'}

SARB_AUTH_APPLIC_NUMBER_ETF_PLAT = { 'BWP' : '1344'}

SARB_AUTH_REF_NUMBER_ETF_PLAT = {'BWP' : '2014-011316'}

SYSTEM_TRADER_NAME = 'FRONT_ARENA'

UCR = 'YearZACCNGOLDDESK'


AFRICAN_CURRENCIES = ['BWP', 'GHS', 'KES', 'LSL', 'MUR', 'MWK', 'MZN', 'NAD', 'NGN', 'SZL', 'TZS', 'UGX', 'ZMK', 'ZMW']

FUNDING_INSTYPE_OVERRIDES = ['FDC', 'FDE', 'FDI', 'FLI', 'FTL']

GOLD_CAT201_PARTIES = ['BARCLAYS BANK PLC', 'BARCLAYS BNK PLC GERMISTON']

MERCHANDISE_EXPORT_CATEGORY = ['100', '101', '102', '103', '104', '105', '111', '112', '113', '114', '116', '201']

MERCHANDISE_IMPORT_CATEGORY = ['100', '101', '102', '103', '104', '105', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '201', '203']

MONEYFLOW_TYPE_EXCLUSION = ['Redemption Amount', 'Security Nominal', 'Stand Alone Payment', 'End Security', 'Aggregate Security', 'Aggregate Cash', 'Interest Reinvestment', 'Credit Default']

PRECIOUS_METALS_CURRENCIES = ['XAG', 'XAU', 'XPT', 'XPD']

PREVENT_COUNTERPARTY = ['JSE']

VALID_CURRENCIES = ['AED', 'AUD', 'BWP', 'CAD', 'CHF', 'CZK', 'DKK', 'EUR', 'GBP', 'GHS', 'HKD', 'HUF', 'ILS', 'INR', 'JPY', 'KES', 'KWD', 'LSL', 'MUR', 'MWK', 'MXN', 'MZN', 'NAD', 'NGN', 'NOK', 'NZD', 'PKR', 'PLN', 'QAR', 'SAR', 'SEK', 'SGD', 'SZL', 'THB', 'TRY', 'TZS', 'UGX', 'USD', 'ZAR', 'ZMK', 'ZMW']

EXCEPTION_PORTFOLIOS = ['Africa TES Fundpool', 'NZ Fundpool', 'NZ Structural Deposits', 'Non Zar Mismatch2', 'LTFX', 'STIRT - FRA FLO', 'VOE', 'JN_FX Options', 'Africa_Curr']
EXCEPTION_ACQUIRERS = ['Money Market Desk', 'IRD DESK', 'NLD DESK', 'IRP_FX Desk']

LCH_PORTFOLIOS = ['NZ FV LCH', 'IRM LCH', 'LTnonzar-LCH', 'NZ FI LCH', 'LTFX_LCH', 'CD_DCRM_RTB_RATES_LCH', 'FI_Options_LCH', 'FI OIS_LCH', 'ERM_IRP_LCH', 'CD_LCH', 'BESA Investment_LCH', 'Africa LCH', 'Treasury External LCH', 'Swap Flow_LCH', 'STIRT - FRA FLO LCH']

NONBANK_EXCEPTION_ACQUIRERS = ['TWC DT', 'TWC SF']
NONBANK_EXCEPTION_PORTFOLIOS = ['DT Vanilla Trade loans Non ZAR', 'Supplier Finance Non ZAR']

TWC_ACQUIRERS = ['TWC SF', 'TWC NON RECOURSE RECEIVABLES', 'TWC FIT', 'TWC STCF', 'TWC DT', 'TWC OPEN ACCOUNT']
