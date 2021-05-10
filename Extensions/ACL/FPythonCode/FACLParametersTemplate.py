""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLParametersTemplate.py"
import acm

class CommonSettings:
    ambAddress=''
    armlServiceUrl=''        
    tradeFilterQuery=None
    scalingFactor = 1e-06
    
    # sort order in the 'Ratings' choice list
    internal=1
    moodys=2
    standardAndPoors=3
    
class MessageATSSettings:
    detailedLogging=False
    receiverMBName='ACL_MESSAGE_RECEIVER'
    receiverSource='ACL_AMBA'
    senderMBName='ACL_MESSAGE_SENDER'
    senderSource='ACL_MESSAGE_ATS'
    timeoutForReplyInSeconds=10
    ambAddress=CommonSettings.ambAddress
    
class ConnectorATSSettings:
    windowsUserName='SYSTEM'
    maxMsgBufSize=131072

    class TradeATS1UserName:
        detailedLogging=False
        receiverMBName='ACL_CONNECTOR_RECEIVER'
        receiverSource='ACL_MESSAGE_ATS'
        senderMBName='ACL_CONNECTOR_SENDER'
        senderSource='ACL_CONNECTOR_ATS'
        channel='ACL_CHANNEL_1'
        numberOfRetries=5
        retryDelayBase=0.5
        ambAddress=CommonSettings.ambAddress

    '''
    class TradeATS2UserName:
        detailedLogging=False
        receiverMBName='ACL_CONNECTOR_RECEIVER'
        receiverSource='ACL_MESSAGE_ATS'
        senderMBName='ACL_CONNECTOR_SENDER'
        senderSource='ACL_CONNECTOR_ATS'
        channel='ACL_CHANNEL_2'
        numberOfRetries=5
        retryDelayBase=0.5
        ambAddress=CommonSettings.ambAddress
    '''
    
    class AdminDataATSUserName:
        detailedLogging=False
        receiverMBName='ACL_CONNECTOR_RECEIVER'
        receiverSource='ACL_MESSAGE_ATS'
        senderMBName='ACL_CONNECTOR_SENDER'
        senderSource='ACL_CONNECTOR_ATS'
        channel='FACL_ADMIN' # Exactly one Connector ATS MUST subscribe to this channel for instrument and party export to work
        numberOfRetries=5
        retryDelayBase=0.5
        ambAddress=CommonSettings.ambAddress

class SystemControlATSSettings:
    ambUser=None
    ambPassword=None
    ambAddress=CommonSettings.ambAddress
    senderMBName='ACL_SYSTEMCONTROL_SENDER'
    senderSource='ACL_SYSTEMCONTROL_ATS'
    receiverMBName='ACL_SYSTEMCONTROL_RECEIVER'
    receiverSource='ACL_CONNECTOR_ATS'
    pingInterval=60
    timeoutForReplyInSeconds=10
    armlLogDir=''
    armlLogInclude='Exception' # All, Exception, None
    dbConnectionString=''
    # Sample SQL Server Authentication
    #dbConnectionString='DRIVER={SQL Server};SERVER=MyServer;DATABASE=MyDatabase;USER ID=MyUser;PASSWORD=MyPassword'
    # Sample Windows Authentication
    #dbConnectionString='DRIVER={SQL Server};SERVER=MyServer;DATABASE=MyDatabase;TRUSTED_CONNECTION=Yes'
    
class PrimeSettings:
    senderMBName='ACL_PRIME_SENDER'
    senderSource='ACL_MESSAGE_ATS'
    receiverMBName='ACL_PRIME_RECEIVER'
    timeoutForReplyInSeconds=10
    ambUser=None
    ambPassword=None
    ambAddress=CommonSettings.ambAddress
    limitsServerUrl=''
    excludeInsDef = ['CInsDef_CURR', 'CInsDef_CREDIT_INDEX', 'CInsDef_PRICE_INDEX', 'CInsDef_RATE_INDEX']

class PartyMapping:
    # Key is ArML attribute name, value is ACM attribute name or custom method.
    properties = { 
        'Identification\Code'                           : 'Name',
        'Identification\Name'                           : 'Fullname',
        'Reference'                                     : 'FACLgetPreviousName',
        'Type'                                          : 'FACLgetType',
        'Attributes\Active'                             : 'FACLgetActive',
        'Attributes\Trading'                            : 'FACLgetTrading',
        'Classification\Customer Type'                  : 'FACLgetCustomerType',
        'Classification\Country of Risk'                : 'FACLgetCountryOfRisk',
        'Classification\Country of Incorporation'       : 'FACLgetCountryOfIncorporation',
        'Classification\Jurisdiction'                   : 'FACLgetJurisdictionCountry',
        'Hierarchy\Parents'                             : 'FACLgetParent',
        'Ratings\Internal'                              : 'FACLinternalRating',
        'Ratings\Moodys'                                : 'FACLmoodysRating',
        'Ratings\Standard and Poors'                    : 'FACLstandardAndPoorsRating'
    }
    
class CustomerBranchMapping:
    # Key is ArML attribute name, value is ACM attribute name or custom method.
    properties = { 
        'Identification\Code'                           : 'Name',
        'Identification\Name'                           : 'Fullname',
        'Reference'                                     : 'FACLgetPreviousName',
        'Type'                                          : 'FACLgetType',
        'Attributes\Active'                             : 'FACLgetActive',
        'Classification\Country'                        : 'FACLgetCountryOfRisk',
        'Hierarchy\Parent'                              : 'FACLgetParent'
    }

class InternalDepartmentMapping:
    # Key is ArML attribute name, value is ACM attribute name or custom method.
    properties = { 
        'Identification\Code'                           : 'Name',
        'Identification\Name'                           : 'Fullname',
        'Reference'                                     : 'FACLgetPreviousName',
        'Classification\Country of Residence'           : 'FACLgetCountryOfRisk',
        'Attributes\Active'                             : 'FACLgetActive',
        'Attributes\Trading Branch'                     : 'FACLgetTrading',
        'Attributes\Consolidation'                      : 'FACLgetConsolidation',
        'Type'                                          : 'FACLgetType',
        'Hierarchy\Parent'                              : 'FACLgetParent'
    }
