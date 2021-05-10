'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CONSTANTS_LOGGER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This modules store the logger constants for FrontCache
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
'''----------------------------------------------------------------------------------------------------------
Class containing all the generic properties for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_CONSTANTS_LOGGER(object):
    def __init__(self):
        self._BATCH_COMPLETE_RESPONSE_ = 'Batch %s complete processed, all requests processed, send batch complete response.'
        self._S_END = '%s_END'
        self._THE_FOLLOWING_ERROR_S_ = 'Worksheet %s could not be cleared due to the following error: %s.'
        self._BATCH_COMPLETE_S = 'Is Batch Complete: %s'
        self._REQUEST_COMPLETE_S = 'Is Request Complete: %s'
        self._COLLECTION_TRACKER_ID_S_ = 'Updating Request Collection Tracker ID %s.'
        self._BATCH_I_OF_I_I_ITEMS_ = 'processing batch %i of %i (%i items)'
        self._COMPLETE_RESPONSE_ = 'Request processed, all collection batches done, send request complete response.'
        self._PROCESSED_I_ERRORS_ = 'Collection batch %i done (%i processed, %i errors)'
        self._CALL_IN_MODULE_S_ERROR_S = 'Could not create sql parameters for the updateBatchRequestEndSql call in module %s: Error: %s'
        self._COULD_NOT_RETRIEVE_UPDAT_TIME_TAG = 'Could not retrieve the UPDAT_TIME tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_SEQNBR_TAG = 'Could not retrieve the SEQNBR tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_THE_STL_TAG = 'Could not retrieve the SETTLEMENT tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_INSID_TAG = 'Could not retrieve the INSID tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_INSADDR_TAG = 'Could not retrieve the INSADDR tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_INSTRUMENT_TAG = 'Could not retrieve the INSTRUMENT tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_THE_TRDBR = 'Could not retrieve the TRDNBR tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_TRADE_TAG = 'Could not retrieve the TRADE tag from the incoming AMBA message.'
        self._NO_SETTLEMENT_LIST = 'No SETTLEMENT List could be retrieved from the incoming AMBA message. Cannot retreive the Update Time and Update User Id.'
        self._NO_INSTRUMENT_LIST = 'No INSTRUMENT List could be retrieved from the incoming AMBA message. Cannot retreive the Update Time and Update User Id.'
        self._NO_TRADE_LIST = 'No TRADE List could be retrieved from the incoming AMBA message. Cannot retreive the Update Time and Update User Id.'
        self._COULD_NOT_RETRIEVE_THE_TYPE_TAG = 'Could not retrieve the TYPE tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_TXNBR = 'Could not retrieve the TXNBR tag from the incoming AMBA message.'
        self._INCOMING_AMBA_MESSAGE_ = 'Could not retrieve the SOURCE tag from the incoming AMBA message.'
        self._THE_SELECTION_TYPE_IS_NOT_IMPLEMENTED = 'The Selection Type %s is not implemented in module %s. No data was selected to pass onto the Collection ATS.'
        self._NO_SCOPE_NAME_NUMBER_SUPPLIER = 'No Scope Name and Scope Number were supplied for the Selection Type %s in module %s. No data was selected to pass onto the Collection ATS.'
        self._COULD_NOT_GET_SQL_CONNECTION = "Could not get the SQL connection for '%s'. Retry atempt number: %i."
        self._COULD_NOT_RETRIEVE_DATA_TAG_FROM_INCOMMING_AMBA_MSG = 'Could not retreive the DATA tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_AMBA_TXNBR_FROM_INCOMING_AMBA_MSG = 'Could not retreive the AMBA_TXNBR from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_BATCH_ID_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the BATCH_ID tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_IS_EOD_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the IS_EOD tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_IS_DATE_TODAY_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the IS_DATE_TODAY tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REPORT_DATE_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive REPORT_DATE tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_REQUEST_DATETIME_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_DATETIME tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_EVENT_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_EVENT_TYPE tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_ID_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_ID tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_SOURCE_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_SOURCE tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_TYPE_TAG_FROM_THE_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_TYPE tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_USER_ID_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the REQUEST_USER_ID tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_SCOPE_NAME_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the SCOPE_NAME tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_SCOPE_NUMBER_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the SCOPE_NUMBER tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_THE_TOPIC_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the TOPIC tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_REQUEST_BATCH_COUNT_TAG_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_BATCH_COUNT tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_THE_REQUEST_BATCH_NO_TAG_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_BATCH_NO tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_REQUEST_BATCH_START_INDEX_TAG_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_BATCH_START_INDEX tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_REQUEST_BATCH_END_INDEX_TAG_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_BATCH_END_INDEX tag from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_REQUEST_BATCH_TRADE_COUNT_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_BATCH_TRADE_COUNT from the incoming AMBA message.'
        self._COULD_NOT_RETREIVE_REQUEST_COLLECTION_TRACKER_ID_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_COLLECTION_TRACKER_ID from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_REQUEST_COLLECTION_PRIMARY_KEYS_FROM_INCOMING_AMBA_MSG = 'Could not retreive the REQUEST_COLLECTION_PRIMARY_KEYS from the incoming AMBA message.'
        self._COULD_NOT_RETRIEVE_EXPECTED_OBJ_COUNT_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the EXPECTED_OBJECT_COUNT tag from the incoming AMBA message in module %s.'
        self._COULD_NOT_RETRIEVE_RESPONSE_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S = 'Could not retreive the RESPONSE_TYPE tag from the incoming AMBA message in module %s.'
        self._STARTING_ATS_S_AT_S = 'Starting the ATS %s at %s'
        self._AMB_WRITER_CONNECTION_EST = 'AMB Writer(s) Conection Established.'
        self._AMB_READER_CONNECTION_EST = 'AMB Reader Conection Established.'
        self._HEART_BEAT_PROCESS_TIMER_STARTED_S = 'Heart Beat Process Timer started at %s'
        self._STOPPING_ATS_S = 'Stopping the ATS at %s'
        self._STOPPING_HEART_BEAT_PROCESS_S = 'Stopping the Process Heart Beat at %s'
        self._STOPPING_SYSTEM_HEAR_BEAT_S = 'Stopping the System Heart Beat at %s'
        self._MSG_QUEUE_START_UP_DEPTH_I = 'Message Queue on Start Up: Depth %i'
        self._ATS_STARTED_AT_S = 'ATS started at %s'
        self._ATS_NAME_S = ' ATS Name                              : %s'
        self._PLATFORM_S = ' Platform                              : %s'
        self._PROCESS_ID_S = ' Process Id                            : %s'
        self._RESTART_ON_MEMORY_THRESHOLD_S = ' Restart on memory threshold           : %s'
        self._MEMORY_THRESHOLD_S = ' Memory Threshold                      : %s KB'
        self._SETTING_UP_AMBA_CONNECTIONS = 'Setting up AMB connections... '
        self._AMBA_HOST_S = ' AMB Host            :                 %s'
        self._AMB_READER_S = ' AMB Reader          :                 %s'
        self._AMB_READER_SUBJECTS_S = ' AMB Reader subjects :                 %s'
        self._ATS_STARTUP_COMPLETE = '*** ATS Startup Complete.'
        self._AMB_READER_CONNECTION_TO_AMB_CLOSED = 'AMB Reader Connection to the AMB is now closed.'
        self._AMB_SENDER_CONN_TO_AMB_CLOSED_S = 'AMB Sender Connection to the AMB is now closed for writer posting Message Type %s.'
        self._CURRENT_VIRTUAL_MEMORY_USAGE_S_EXCEEDS_MEMORY_THRESHOLD_S = 'Current virtual memory usage %s exceeds the memory threshold of %s KB, forcing a restart...'
        self._MSG_EVENT_RECEIVED_S = 'Message event received. (messageId:%s)'
        self._MSG_RECEIVED_AMB_FORMAT_S = 'Message received in AMB format:\n%s'
        self._MSG_ACCEPTED_I = 'Message accepted (messageId:%i)'
        self._S_MSG_REMAINING_IN_QUEUE = '%s messages remaining in the queue'
        self._CLOSING_BOTH_AMB_READER_WRITER_CONNECTIONS_AMB = 'Closing both the AMB Reader and Writer Connections to the AMB.'
        self._S_TRADES_FOUND = '%i trades found'
        self._S_INSTRUMENT_FOUND = '%i instrument found'
        self._S_PORTFOLIO_FOUND = '%i portfolio found'
        self._I_BATCHES_CREATED_I = '%i batch(s) created (maxBatchSize:%i)'

    @property
    def S_TRADES_FOUND(self):
        return self._S_TRADES_FOUND

    @property
    def S_INSTRUMENT_FOUND(self):
        return self._S_INSTRUMENT_FOUND

    @property
    def S_PORTFOLIO_FOUND(self):
        return self._S_PORTFOLIO_FOUND

    @property
    def I_BATCHES_CREATED_I(self):
        return self._I_BATCHES_CREATED_I

    @property
    def AMB_WRITER_CONNECTION_EST(self):
        return self._AMB_WRITER_CONNECTION_EST

    @property
    def AMB_READER_CONNECTION_EST(self):
        return self._AMB_READER_CONNECTION_EST

    @property
    def HEART_BEAT_PROCESS_TIMER_STARTED_S(self):
        return self._HEART_BEAT_PROCESS_TIMER_STARTED_S

    @property
    def STOPPING_ATS_S(self):
        return self._STOPPING_ATS_S

    @property
    def STOPPING_HEART_BEAT_PROCESS_S(self):
        return self._STOPPING_HEART_BEAT_PROCESS_S

    @property
    def STOPPING_SYSTEM_HEAR_BEAT_S(self):
        return self._STOPPING_SYSTEM_HEAR_BEAT_S

    @property
    def MSG_QUEUE_START_UP_DEPTH_I(self):
        return self._MSG_QUEUE_START_UP_DEPTH_I

    @property
    def ATS_STARTED_AT_S(self):
        return self._ATS_STARTED_AT_S

    @property
    def ATS_NAME_S(self):
        return self._ATS_NAME_S

    @property
    def PLATFORM_S(self):
        return self._PLATFORM_S

    @property
    def PROCESS_ID_S(self):
        return self._PROCESS_ID_S

    @property
    def RESTART_ON_MEMORY_THRESHOLD_S(self):
        return self._RESTART_ON_MEMORY_THRESHOLD_S

    @property
    def MEMORY_THRESHOLD_S(self):
        return self._MEMORY_THRESHOLD_S

    @property
    def SETTING_UP_AMBA_CONNECTIONS(self):
        return self._SETTING_UP_AMBA_CONNECTIONS

    @property
    def AMBA_HOST_S(self):
        return self._AMBA_HOST_S

    @property
    def AMB_READER_S(self):
        return self._AMB_READER_S

    @property
    def AMB_READER_SUBJECTS_S(self):
        return self._AMB_READER_SUBJECTS_S

    @property
    def ATS_STARTUP_COMPLETE(self):
        return self._ATS_STARTUP_COMPLETE

    @property
    def AMB_READER_CONNECTION_TO_AMB_CLOSED(self):
        return self._AMB_READER_CONNECTION_TO_AMB_CLOSED

    @property
    def AMB_SENDER_CONN_TO_AMB_CLOSED_S(self):
        return self._AMB_SENDER_CONN_TO_AMB_CLOSED_S

    @property
    def CURRENT_VIRTUAL_MEMORY_USAGE_S_EXCEEDS_MEMORY_THRESHOLD_S(self):
        return self._CURRENT_VIRTUAL_MEMORY_USAGE_S_EXCEEDS_MEMORY_THRESHOLD_S

    @property
    def MSG_EVENT_RECEIVED_S(self):
        return self._MSG_EVENT_RECEIVED_S

    @property
    def MSG_RECEIVED_AMB_FORMAT_S(self):
        return self._MSG_RECEIVED_AMB_FORMAT_S

    @property
    def MSG_ACCEPTED_I(self):
        return self._MSG_ACCEPTED_I

    @property
    def S_MSG_REMAINING_IN_QUEUE(self):
        return self._S_MSG_REMAINING_IN_QUEUE

    @property
    def CLOSING_BOTH_AMB_READER_WRITER_CONNECTIONS_AMB(self):
        return self._CLOSING_BOTH_AMB_READER_WRITER_CONNECTIONS_AMB

    @property
    def COULD_NOT_RETRIEVE_EXPECTED_OBJ_COUNT_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_EXPECTED_OBJ_COUNT_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_RESPONSE_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_RESPONSE_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def STARTING_ATS_S_AT_S(self):
        return self._STARTING_ATS_S_AT_S

    @property
    def COULD_NOT_RETRIEVE_DATA_TAG_FROM_INCOMMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_DATA_TAG_FROM_INCOMMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_AMBA_TXNBR_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_AMBA_TXNBR_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_THE_BATCH_ID_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_BATCH_ID_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_IS_EOD_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_IS_EOD_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_IS_DATE_TODAY_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_IS_DATE_TODAY_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REPORT_DATE_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REPORT_DATE_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_REQUEST_DATETIME_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_DATETIME_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_EVENT_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_EVENT_TYPE_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_ID_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_ID_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_SOURCE_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_SOURCE_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_TYPE_TAG_FROM_THE_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_TYPE_TAG_FROM_THE_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_USER_ID_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_USER_ID_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_SCOPE_NAME_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_SCOPE_NAME_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_SCOPE_NUMBER_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_SCOPE_NUMBER_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_RETRIEVE_THE_TOPIC_TAG_FROM_INCOMING_AMBA_MSG_S(self):
        return self._COULD_NOT_RETRIEVE_THE_TOPIC_TAG_FROM_INCOMING_AMBA_MSG_S

    @property
    def COULD_NOT_GET_SQL_CONNECTION(self):
        return self._COULD_NOT_GET_SQL_CONNECTION
        
    @property
    def NO_SCOPE_NAME_NUMBER_SUPPLIER(self):
        return self._NO_SCOPE_NAME_NUMBER_SUPPLIER
        
    @property
    def THE_SELECTION_TYPE_IS_NOT_IMPLEMENTED(self):
        return self._THE_SELECTION_TYPE_IS_NOT_IMPLEMENTED
        
    @property    
    def BATCH_COMPLETE_RESPONSE(self):        
        return self._BATCH_COMPLETE_RESPONSE_
        
    @property    
    def S_END(self):        
        return self._S_END
        
    @property    
    def THE_FOLLOWING_ERROR_S(self):        
        return self._THE_FOLLOWING_ERROR_S_
        
    @property        
    def BATCH_COMPLETE_S(self):        
        return self._BATCH_COMPLETE_S
        
    @property    
    def REQUEST_COMPLETE_S(self):        
        return self._REQUEST_COMPLETE_S
        
    @property    
    def COLLECTION_TRACKER_ID_S(self):        
        return self._COLLECTION_TRACKER_ID_S_
        
    @property    
    def BATCH_I_OF_I_I_ITEMS(self):        
        return self._BATCH_I_OF_I_I_ITEMS_
        
    @property    
    def COMPLETE_RESPONSE(self):        
        return self._COMPLETE_RESPONSE_
        
    @property    
    def PROCESSED_I_ERRORS(self):        
        return self._PROCESSED_I_ERRORS_
        
    @property    
    def CALL_IN_MODULE_S_ERROR_S(self):        
        return self._CALL_IN_MODULE_S_ERROR_S
        
    @property    
    def COULD_NOT_RETRIEVE_UPDAT_TIME_TAG(self):        
        return self._COULD_NOT_RETRIEVE_UPDAT_TIME_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_SEQNBR_TAG(self):        
        return self._COULD_NOT_RETRIEVE_SEQNBR_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_THE_STL_TAG(self):        
        return self._COULD_NOT_RETRIEVE_THE_STL_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_INSID_TAG(self):        
        return self._COULD_NOT_RETRIEVE_INSID_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_INSADDR_TAG(self):        
        return self._COULD_NOT_RETRIEVE_INSADDR_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_INSTRUMENT_TAG(self):        
        return self._COULD_NOT_RETRIEVE_INSTRUMENT_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_THE_TRDBR(self):        
        return self._COULD_NOT_RETRIEVE_THE_TRDBR
        
    @property    
    def COULD_NOT_RETRIEVE_TRADE_TAG(self):        
        return self._COULD_NOT_RETRIEVE_TRADE_TAG
        
    @property    
    def NO_SETTLEMENT_LIST(self):        
        return self._NO_SETTLEMENT_LIST
        
    @property    
    def NO_INSTRUMENT_LIST(self):        
        return self._NO_INSTRUMENT_LIST
        
    @property    
    def NO_TRADE_LIST(self):        
        return self._NO_TRADE_LIST
        
    @property    
    def COULD_NOT_RETRIEVE_THE_TYPE_TAG(self):        
        return self._COULD_NOT_RETRIEVE_THE_TYPE_TAG
        
    @property    
    def COULD_NOT_RETRIEVE_TXNBR(self):        
        return self._COULD_NOT_RETRIEVE_TXNBR
        
    @property    
    def INCOMING_AMBA_MESSAGE(self):        
        return self._INCOMING_AMBA_MESSAGE_        

    @property
    def COULD_NOT_RETRIEVE_REQUEST_BATCH_COUNT_TAG_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_BATCH_COUNT_TAG_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_THE_REQUEST_BATCH_NO_TAG_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_THE_REQUEST_BATCH_NO_TAG_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_REQUEST_BATCH_START_INDEX_TAG_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_BATCH_START_INDEX_TAG_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_REQUEST_BATCH_END_INDEX_TAG_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_BATCH_END_INDEX_TAG_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_REQUEST_BATCH_TRADE_COUNT_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_BATCH_TRADE_COUNT_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETREIVE_REQUEST_COLLECTION_TRACKER_ID_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETREIVE_REQUEST_COLLECTION_TRACKER_ID_FROM_INCOMING_AMBA_MSG

    @property
    def COULD_NOT_RETRIEVE_REQUEST_COLLECTION_PRIMARY_KEYS_FROM_INCOMING_AMBA_MSG(self):
        return self._COULD_NOT_RETRIEVE_REQUEST_COLLECTION_PRIMARY_KEYS_FROM_INCOMING_AMBA_MSG


