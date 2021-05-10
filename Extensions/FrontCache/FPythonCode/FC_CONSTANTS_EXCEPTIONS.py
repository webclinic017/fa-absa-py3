'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CONSTANTS_EXCEPTIONS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This modules store the exception constants for FrontCache
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
'''----------------------------------------------------------------------------------------------------------
Class containing all the generic properties for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_CONSTANTS_EXCEPTIONS(object):
    def __init__(self):
        self._SAVE_DATA_NOT_IMPLEMENTED_ERROR = "Method 'SaveData' not implemented"
        self._CREATE_SQL_PARAMETERS = 'Could not create SQL parameters'
        self._CREATE_THE_SETTLEMENT = 'Could not create the Settlement'
        self._CREATE_THE_PORTFOLIO = 'Could not create the Portfolio'
        self._CREATE_THE_INSTRUMENT = 'Could not create the Instrument'
        self._CREATE_THE_TRADE = 'Could not create the trade'
        self._F_SETTLEMENT_INSTANCE = 'The settlement static container does not contain a valid FSettlement instance'
        self._F_PORTFOLIO_INSTANCE = 'The portfolio static container does not contain a valid FPortfolio instance'
        self._F_INSTRUMENT_INSTANCE = 'The instrument static container does not contain a valid FInstrument instance'
        self._NOT_HAVE_SERIALIZED_DATA = 'The settlement static container does not have serialized data'
        self._THE_SQL_DATA_PROVIDER__S = 'Could not get the SQL data provider. %s'
        self._REGISTER_THE_BATCH__S = 'Could not register the batch. %s'
        self._TRACKER_AS_STARTED__S = 'Could not update the request tracker as started. %s'
        self._TRACKER_AS_COMPLETED__S = 'Could not update the request tracker as completed. %s'
        self._COLLECTION_TRACKER__S = 'Could not update the request collection tracker. %s'
        self._SAVE_THE_TRADES__S = 'Could not build and save the trades. %s'
        self._SAVE_THE_SETTLEMENTS__S = 'Could not build and save the settlements. %s'
        self._SINGLETON_IS_ALLOWED_ = 'Only one instance of FC_CALCULATION_SINGLETON is allowed!'
        self._CALCULATION_SINGLETON__S = 'Could not create the calculation singleton. %s'
        self._DYNAMIC_CALCULATIONS = 'No workbooks configured for dynamic calculations'
        self._COLUMNS_FOR_SHEET_S__S = 'Could not load the columns for sheet %s.  %s'
        self._CONTAINS_NO_COLUMNS = 'The sheet %s contains no columns'
        self._WORKSPACE_WORKSHEETS_MUST_BE_UNIQUE = 'The worksheetCalcSpace dictionary already has a sheet named %s, Front Cache worksheet names across all workbooks must be unique'
        self._WORKSHEETS_MUST_BE_UNIQUE = 'The worksheetColumns dictionary already has a sheet named %s, Front Cache worksheet names across all workbooks must be unique'
        self._WORKBOOKS_MUST_BE_UNIQUE = 'The worksheet dictionary already has a sheet named %s, Front Cache worksheet names accross all workbooks must be unique'
        self._NOT_LOAD_WORKBOOK_S = 'Could not load workbook %s'
        self._THE_GLOBAL_VALUE_S_ = 'No calc space was provided to simulate the global value %s.'
        self._THE_FOLLOWING_ERROR_S_ = 'Worksheet %s could not be cleared due to the following error: %s.'
        self._VALUES_FOR_SHEET_S__S = 'Could not get the calculated values for sheet %s. %s'
        self._SPACE_FOUND_FOR_SHEET_ = 'No calculation space found for sheet '
        self._COLUMNS_FOUND_FOR_SHEET_ = 'No worksheet columns found for sheet '
        self._PASSED_FOR_CALCULATION = 'No object or tree proxy passed for calculation'
        self._CREATE_SQL_PARAMETERS_FAILED = 'Could not create sql parameters. %s'
        self._REQUEST_END_FAILED__S = 'Update in updateBatchRequestEnd failed. %s'
        self._TRACKER_FAILED__S = 'Update batch tracker failed. %s'
        self._BATCH_TRACKER_FAILED__S = 'Create batch tracker failed. %s'
        self._REQUEST_ENTITY_FAILED__S = 'Create request entity failed. %s'
        self._MUST_BE_PROVIDED = 'A valid request message instance must be provided'
        self._FC_TRD_DATA_TYPE_MUST_BE_PROVIDED = 'A valid FC_DATA_TRD instance must be provided'
        self._TYPE_S_IS_NOT_SUPPORTED = "Serialization type '%s' is not supported"
        self._FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED = 'A valid FC_DATA_STL instance must be provided'
        self._TYPE_IS_REQUIRED = 'Serialization type is required'
        self._VALID_WS_MUST_BE_PROVIDED = 'A valid worksheet name must be provided'
        self._NO_TOP_LEVEL_NODE_TREE_PROXY = 'Could not get the top level node tree proxy'
        self._NO_FIRST_CHILD_NODE_TREE_PROXY = 'Could not get the first child node tree proxy'
        self._METHOD_GETFOBJECT_NOT_IMPLEMENTED = "Method 'GetFObject' not implemented"
        self._WS_NAME_NOT_SET = 'The worksheet name was not set'
        self._VALID_FTREEPROXY_MUST_BE_PROVIDED = 'A valid FTreeProxy instance must be provided'
        self._CREATE_REQ_COLL_TRACKER_FAILED_S = 'Create request collection tracker failed. %s'
        self._UPDATE_REQ_COLL_TRACKER_START_FAILED_S = 'Update request collection tracker start failed. %s'
        self._UPDATE_REQ_TRACKER_START_FAILED_S = 'Update request tracker start failed. %s'
        self._UPDATE_REQ_END_FAILED_S = 'Update request end failed. %s'
        self._COULD_NOT_GET_REQ_TRACKER_RESULT = 'Could not get the request tracker result. %s'
        self._COULD_NOT_CALC_STATIC_ATTR_S = 'Could not calculate the Static Attributes for settlement %s with the following error: %s'
        self._COULD_NOT_CALC_SCALAR_ATTR_S = 'Could not calculate the Scalar Attributes for settlement %s with the following error: %s'
        self._COULD_NOT_CALC_SENSITIVITY_WB  = 'Could not calculate the Sensitivity Workbook for object(%s) %s with the following error: %s'
        self._STL_NOT_FOUND = 'Settlement %s not found'
        self._INNER_STL_CONTAINER_DNE = 'Inner settlement container does not exist'
        self._VALID_FSTL_INSTANCE_MUST_BE_PROVIDED = 'A valid FSettlement instance must be provided'
        self._TRD_STATIC_CONTAINS_NO_VALID_FTRADE_INSTANCE ='The trade static container does not contain a valid FTrade instance'
        self._TRD_STATIC_CONTAINER_NO_SERIALIZED_DATA = 'The trade static container does not have serialized data'
        self._COULD_NOT_CALC_STATIC_ATTR_TRADE = 'Could not calculate the Static Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_SCALAR_ATTR_TRADE = 'Could not calculate the Scalar Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_INTS_ATTR_TRADE = 'Could not calculate the Instrument Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_LEG_ATTR_TRADE = 'Could not calculate the Leg Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_UNDER_INSTR_ATTR_TRADE = 'Could not calculate the Underlying Instrument Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_MONF_ATTR_TRADE = 'Could not calculate the MoneyFlow Attributes for trade %s with the following error: %s'
        self._COULD_NOT_CALC_SCA_ATTR_TRADE = 'Could not calculate the Sales Credit Attributes for trade %s with the following error: %s'
        self._INNER_TRADE_DNE = 'Inner trade container does not exist'
        self._TRADE_S_NOT_FOUND = 'Trade %s not found'
        self._VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED = 'A valid FTrade instance must be provided'
        self._VALID_FINSTRTREEPROXY_MUST_BE_PROVIDED = 'A valid fInstrumentTreeProxy must be provided'
        self._VALID_FLEGTREEPROXY_MUST_BE_PROVIDED = 'A valid fLegTreeProxy must be provided'
        self._COULD_NOT_SERIALIZE_THE_CALC_RESULT = 'Could not serialize the calculation results. %s'
        self._COULD_NOT_GET_THE_SQL_CONNECTION_S = "Could not get the SQL connection for '%s'. %s"
        self._EXECUTE_NO_RETURN_FAILED_S = 'executeNoReturn failed with error - %s'
        self._EXECUTE_FAILED_S = 'execute failed with error - %s'
        self._EXECUTE_SCALAR_FAILED = 'executeScalar failed with error - %s'
        self._EXECUTE_MANY_FAILED = 'execute many failed with error - %s'
        self._EXECUTE_NO_RETURN_IN_TX_FAILED_S = 'executeNoReturnInTransaction failed with error - %s'
        self._EXECUTE_IN_TX_FAILED_S = 'execute in transaction failed with error - %s'
        self._EXECUTE_MANY_IN_TX_FAILED_S = 'execute many in transaction failed with error - %s'
        self._COMMIT_FAILED_S = 'commit failed with error - %s'
        self._ROLLBACK_FAILED_S = 'rollback failed with error - %s'
        self._VALID_FMONEYF_TREEPROXY_MUST_BE_PROVIDED = 'A valid fMoneyflowTreeProxy must be provided'
        self._HANDLER_CLASS_OVERRIDE_HANDLER_METHOD = 'The handler class needs to override the initialise method!'
        self._HANDLER_CLASS_OVERRIDE_CREATEAMBWRITER_METHOD = 'The handler class needs to override the createAMBWriter method!'
        self._WORKER_VARIABLE_S_IS_NOT_INSTANTIATED = 'The worker variable in module %s is not instantiated. The ATS will not be able to process any messages.'
        self._WORKER_VARIABLE_IN_S_IS_NOT_INSTANTIATED_STOP = 'The worker variable in module %s is not instantiated. The ATS will not be able to process stop gracefully.'
        self._AMB_READER_RECEIVED_DISCONNECT_EVENT = 'The AMB reader received a disconnect event.\nThe ATS will not be able to continue reading from the AMB.'
        self._COULD_NOT_LOG_ATS_HEADER_INFO_S = 'Could not log ATS Header information in module %s.'
        self._COULD_NOT_LOAD_WRITER_HANDLERS_S = 'Could not load all the Writer Handlers in module %s.'
        self._COULD_NOT_INITIALIZE_WRITER_HANDLERS = 'Could not load initialize all the Writer Handlers in module %s.'
        self._COULD_NOT_CREATE_AMB_READER_S = 'Could not create the AMB reader in module %s.'
        self._COULD_NOT_CREATE_HEART_BEAT_S = 'Could not create a Heart Beat in module %s.'
        self._COULD_NOT_COMPLETE_ATS_START_HEADER_INFO_S = 'Could not complete the ATS start-up header information in module %s.'
        self._COULD_NOT_CLOSE_AMB_CONNECTIONS_NORMALLY_S = 'Could not close the AMB connections normally in module %s.'
        self._COULD_NOT_STOP_PROCESS_HEART_BEAT_S = 'Could not stop the Process Heart Beat in module %s.'
        self._COULD_NOT_STOP_SYSTEM_HEART_BEAT_S = 'Could not stop the System Heart Beat in module %s.'
        self._COULD_NOT_READ_FIRST_MSG_FROM_AMB_S = 'Could not read the first message from the AMB queue in module %s.'
        self._COULD_NOT_READ_AMBA_MSG_DATA = 'Could not read the AMBA message data in module %s.'
        self._COULD_NOT_MAP_INCOMING_AMBA_MSG_TO_AN_INCOMING_MSG_OBJ_S = 'Could not map the incoming AMBA message to an Icoming Message Object in module %s.'
        self._COULD_NOT_PROCESS_INCOMING_AMBA_MSG_OR_MSG_OBJ = 'Could not process in incoming AMBA message/incoming Message Object in module %s.'
        self._COULD_NOT_DETERMINE_IF_SHOULD_CONTINUE = 'Could not determine if the incoming AMBA message/incoming Message Object in module %s should continue.'
        self._COULD_NOT_CREATE_OUTGOING_MSG_OBJ_S = 'Could not create the Outgoing Message Objects in module %s.'
        self._COULD_NOT_MAP_OUTGOING_MSG_OBJS_TO_OUTGOING_AMBA_MSG_S = 'Could not map the outgoing message objects to outgoing AMBA messages in module %s.'
        self._COULD_NOT_GENERATE_OUTGOING_AMBA_MSG_S = 'Could not generate the outgoing AMBA messages in module %s.'
        self._COULD_NOT_POST_OUTGOING_AMBA_MSG_TO_AMB_S = 'Could not post the outgoing AMBA messages to the AMB in module %s.'
        self._COULD_NOT_ACCEPT_PROCESSED_MSG_FROM_AMB_QUEUE_S = 'Could not accept the processed message from the AMB queue in module %s.'
        self._COULD_NOT_CHECK_MEMORY_THRESHHOLD_S = 'Could not check the memory threashhold in module %s.'
        self._COULD_NOT_POST_MSG_WITH_TYPE_S_AND_SUBJECT_S_TO_THE_AMB_S = 'Could not post the followig message with Type %s and Subject %s to the AMB: %s'
        self._AMB_READER_CONNECTION_COULD_NOT_HAVE_BEEN_EST = 'The AMB Reader Connection could not have been established for the following details:\nAMB Host and Post %s:%s\nReceiver MB Name %s\nSubscription(s) %s'
        self._ATS_WORKER_IMPLEMENT_PROCESS_INCOMING_AMBA_MESSAGE = 'ATS Worker needs to implement method processIncommingAMBAMessage'
        self._ATS_WORKER_IMLPEMENT_MAP_INCOMING_AMBA_MSG_TO_INCOMING_MSG_OBJ = 'ATS Worker needs to implement method mapIncomingAMBAMessageToIncomingMessageObject'
        self._ATS_WORKER_IMPLEMENT_CREATE_OUTGOING_MSG_OBJ = 'ATS Worker needs to implement method createOutgoingMessageObjects'
        self._COULD_NOT_EXECUTE_BUFFER_MBF_READ_S = 'Could not execute Buffer MBF Read on message %s in module %s'
        self._COULD_NOT_EXCEPT_MSG_S_FROM_AMB = 'Could not accept message %s from the AMB.'
        self._COULD_NOT_GET_TRADE_INDEX_BATCHES_S = 'Could not get the trade index batches. %s'
        self._AMB_READER_WRITER_CONNECTIONS_COULD_NOT_BE_CLOSED = 'The AMB Reader and Writer(s) Connection to the AMB could not be closed normally in module %s'
        self._VALID_INSTANCE_OF_WORKBOOK_SHEET_MUST_BE_PROVIDED = 'A valid instance of a workbook sheet must be provided'
        self._WORKSHEETS_OF_TYPE_S_NOT_SUPPORTED = "Worksheets of type %s is not supported. Only sheets of type FTradeSheet, FPortfolioSheet, FSettlementSheet and FMoneyFlowSheet allowed"
        self._VALID_FOBJECT_INSTANCE_MUST_BE_PROVIDED = 'A valid fObject instance must be provided'
        self._INNER_CALC_SPACE_NOT_CREATED = 'The inner calcSpace was not created'
        self._AMB_WRITER_CONNECTTION_COULD_NOT_HAVEN_BEEN_EST = 'The AMB Writer Connection could not have been established for the following details:\nAMB Host and Post %s:%s\nSender MB Name %s\Subject %s'
        self._AMB_WRITER_RECEIVED_DISCONNECT_EVENT = 'The AMB writer received a disconnect event.\nThe ATS will not be able to continue writing to the AMB.'
        self._COL_CALC_S_FAILED = "Column calculation for column '%s' on %s object with id '%s' failed. Reason: %s"
        self._CONFIRMATION_FAILED = 'Confirmation failed %s'
        self._CONTROL_MEASURE_FAILED = 'Control Measure creation failed %s'
        self._MESSAGE_STATE_INFO_FAILED = 'Failed to retrieve the last processed messageid.'
        self._HEARTBEAT_COMPONENT_IS_NONE = 'Heartbeat component is None, ats will restart.'

    @property
    def HEARTBEAT_COMPONENT_IS_NONE(self):
        return self._HEARTBEAT_COMPONENT_IS_NONE

    @property
    def MESSAGE_STATE_INFO_FAILED(self):
        return self._MESSAGE_STATE_INFO_FAILED

    @property
    def CONTROL_MEASURE_FAILED(self):
        return self._CONTROL_MEASURE_FAILED

    @property
    def CONFIRMATION_FAILED(self):
        return self._CONFIRMATION_FAILED

    @property
    def COL_CALC_S_FAILED(self):
        return self._COL_CALC_S_FAILED

    @property
    def AMB_WRITER_CONNECTTION_COULD_NOT_HAVEN_BEEN_EST(self):
        return self._AMB_WRITER_CONNECTTION_COULD_NOT_HAVEN_BEEN_EST

    @property
    def AMB_WRITER_RECEIVED_DISCONNECT_EVENT(self):
        return self._AMB_WRITER_RECEIVED_DISCONNECT_EVENT

    @property
    def VALID_INSTANCE_OF_WORKBOOK_SHEET_MUST_BE_PROVIDED(self):
        return self._VALID_INSTANCE_OF_WORKBOOK_SHEET_MUST_BE_PROVIDED

    @property
    def WORKSHEETS_OF_TYPE_S_NOT_SUPPORTED(self):
        return self._WORKSHEETS_OF_TYPE_S_NOT_SUPPORTED

    @property
    def VALID_FOBJECT_INSTANCE_MUST_BE_PROVIDED(self):
        return self._VALID_FOBJECT_INSTANCE_MUST_BE_PROVIDED

    @property
    def INNER_CALC_SPACE_NOT_CREATED(self):
        return self._INNER_CALC_SPACE_NOT_CREATED

    @property
    def AMB_READER_RECEIVED_DISCONNECT_EVENT(self):
        return self._AMB_READER_RECEIVED_DISCONNECT_EVENT

    @property
    def COULD_NOT_LOG_ATS_HEADER_INFO_S(self):
        return self._COULD_NOT_LOG_ATS_HEADER_INFO_S

    @property
    def COULD_NOT_LOAD_WRITER_HANDLERS_S(self):
        return self._COULD_NOT_LOAD_WRITER_HANDLERS_S

    @property
    def COULD_NOT_INITIALIZE_WRITER_HANDLERS(self):
        return self._COULD_NOT_INITIALIZE_WRITER_HANDLERS

    @property
    def COULD_NOT_CREATE_AMB_READER_S(self):
        return self._COULD_NOT_CREATE_AMB_READER_S

    @property
    def COULD_NOT_CREATE_HEART_BEAT_S(self):
        return self._COULD_NOT_CREATE_HEART_BEAT_S

    @property
    def COULD_NOT_COMPLETE_ATS_START_HEADER_INFO_S(self):
        return self._COULD_NOT_COMPLETE_ATS_START_HEADER_INFO_S

    @property
    def COULD_NOT_CLOSE_AMB_CONNECTIONS_NORMALLY_S(self):
        return self._COULD_NOT_CLOSE_AMB_CONNECTIONS_NORMALLY_S

    @property
    def COULD_NOT_STOP_PROCESS_HEART_BEAT_S(self):
        return self._COULD_NOT_STOP_PROCESS_HEART_BEAT_S

    @property
    def COULD_NOT_STOP_SYSTEM_HEART_BEAT_S(self):
        return self._COULD_NOT_STOP_SYSTEM_HEART_BEAT_S

    @property
    def COULD_NOT_READ_FIRST_MSG_FROM_AMB_S(self):
        return self._COULD_NOT_READ_FIRST_MSG_FROM_AMB_S

    @property
    def COULD_NOT_READ_AMBA_MSG_DATA(self):
        return self._COULD_NOT_READ_AMBA_MSG_DATA

    @property
    def COULD_NOT_MAP_INCOMING_AMBA_MSG_TO_AN_INCOMING_MSG_OBJ_S(self):
        return self._COULD_NOT_MAP_INCOMING_AMBA_MSG_TO_AN_INCOMING_MSG_OBJ_S

    @property
    def COULD_NOT_PROCESS_INCOMING_AMBA_MSG_OR_MSG_OBJ(self):
        return self._COULD_NOT_PROCESS_INCOMING_AMBA_MSG_OR_MSG_OBJ

    @property
    def COULD_NOT_DETERMINE_IF_SHOULD_CONTINUE(self):
        return self._COULD_NOT_DETERMINE_IF_SHOULD_CONTINUE

    @property
    def COULD_NOT_CREATE_OUTGOING_MSG_OBJ_S(self):
        return self._COULD_NOT_CREATE_OUTGOING_MSG_OBJ_S

    @property
    def COULD_NOT_MAP_OUTGOING_MSG_OBJS_TO_OUTGOING_AMBA_MSG_S(self):
        return self._COULD_NOT_MAP_OUTGOING_MSG_OBJS_TO_OUTGOING_AMBA_MSG_S

    @property
    def COULD_NOT_GENERATE_OUTGOING_AMBA_MSG_S(self):
        return self._COULD_NOT_GENERATE_OUTGOING_AMBA_MSG_S

    @property
    def COULD_NOT_POST_OUTGOING_AMBA_MSG_TO_AMB_S(self):
        return self._COULD_NOT_POST_OUTGOING_AMBA_MSG_TO_AMB_S

    @property
    def COULD_NOT_ACCEPT_PROCESSED_MSG_FROM_AMB_QUEUE_S(self):
        return self._COULD_NOT_ACCEPT_PROCESSED_MSG_FROM_AMB_QUEUE_S

    @property
    def COULD_NOT_CHECK_MEMORY_THRESHHOLD_S(self):
        return self._COULD_NOT_CHECK_MEMORY_THRESHHOLD_S

    @property
    def COULD_NOT_POST_MSG_WITH_TYPE_S_AND_SUBJECT_S_TO_THE_AMB_S(self):
        return self._COULD_NOT_POST_MSG_WITH_TYPE_S_AND_SUBJECT_S_TO_THE_AMB_S

    @property
    def AMB_READER_CONNECTION_COULD_NOT_HAVE_BEEN_EST(self):
        return self._AMB_READER_CONNECTION_COULD_NOT_HAVE_BEEN_EST

    @property
    def ATS_WORKER_IMPLEMENT_PROCESS_INCOMING_AMBA_MESSAGE(self):
        return self._ATS_WORKER_IMPLEMENT_PROCESS_INCOMING_AMBA_MESSAGE

    @property
    def ATS_WORKER_IMLPEMENT_MAP_INCOMING_AMBA_MSG_TO_INCOMING_MSG_OBJ(self):
        return self._ATS_WORKER_IMLPEMENT_MAP_INCOMING_AMBA_MSG_TO_INCOMING_MSG_OBJ

    @property
    def ATS_WORKER_IMPLEMENT_CREATE_OUTGOING_MSG_OBJ(self):
        return self._ATS_WORKER_IMPLEMENT_CREATE_OUTGOING_MSG_OBJ

    @property
    def COULD_NOT_EXECUTE_BUFFER_MBF_READ_S(self):
        return self._COULD_NOT_EXECUTE_BUFFER_MBF_READ_S

    @property
    def COULD_NOT_EXCEPT_MSG_S_FROM_AMB(self):
        return self._COULD_NOT_EXCEPT_MSG_S_FROM_AMB

    @property
    def COULD_NOT_GET_TRADE_INDEX_BATCHES_S(self):
        return self._COULD_NOT_GET_TRADE_INDEX_BATCHES_S

    @property
    def AMB_READER_WRITER_CONNECTIONS_COULD_NOT_BE_CLOSED(self):
        return self._AMB_READER_WRITER_CONNECTIONS_COULD_NOT_BE_CLOSED

    @property
    def WORKER_VARIABLE_S_IS_NOT_INSTANTIATED(self):
        return self._WORKER_VARIABLE_S_IS_NOT_INSTANTIATED

    @property
    def WORKER_VARIABLE_IN_S_IS_NOT_INSTANTIATED_STOP(self):
        return self._WORKER_VARIABLE_IN_S_IS_NOT_INSTANTIATED_STOP

    @property
    def VALID_FMONEYF_TREEPROXY_MUST_BE_PROVIDED(self):
        return self._VALID_FMONEYF_TREEPROXY_MUST_BE_PROVIDED

    @property
    def HANDLER_CLASS_OVERRIDE_HANDLER_METHOD(self):
        return self._HANDLER_CLASS_OVERRIDE_HANDLER_METHOD

    @property
    def HANDLER_CLASS_OVERRIDE_CREATEAMBWRITER_METHOD(self):
        return self._HANDLER_CLASS_OVERRIDE_CREATEAMBWRITER_METHOD

    @property
    def ROLLBACK_FAILED_S(self):
        return self._ROLLBACK_FAILED_S

    @property
    def COMMIT_FAILED_S(self):
        return self._COMMIT_FAILED_S

    @property
    def EXECUTE_MANY_IN_TX_FAILED_S(self):
        return self._EXECUTE_MANY_IN_TX_FAILED_S

    @property
    def EXECUTE_IN_TX_FAILED_S(self):
        return self._EXECUTE_IN_TX_FAILED_S

    @property
    def EXECUTE_NO_RETURN_IN_TX_FAILED_S(self):
        return self._EXECUTE_NO_RETURN_IN_TX_FAILED_S

    @property
    def EXECUTE_MANY_FAILED(self):
        return self._EXECUTE_MANY_FAILED

    @property
    def EXECUTE_SCALAR_FAILED(self):
        return self._EXECUTE_SCALAR_FAILED

    @property
    def EXECUTE_FAILED_S(self):
        return self._EXECUTE_FAILED_S

    @property
    def EXECUTE_NO_RETURN_FAILED_S(self):
        return self._EXECUTE_NO_RETURN_FAILED_S

    @property
    def COULD_NOT_GET_THE_SQL_CONNECTION_S(self):
        return self._COULD_NOT_GET_THE_SQL_CONNECTION_S

    @property
    def COULD_NOT_SERIALIZE_THE_CALC_RESULT(self):
        return self._COULD_NOT_SERIALIZE_THE_CALC_RESULT

    @property
    def VALID_FLEGTREEPROXY_MUST_BE_PROVIDED(self):
        return self._VALID_FLEGTREEPROXY_MUST_BE_PROVIDED

    @property
    def VALID_FINSTRTREEPROXY_MUST_BE_PROVIDED(self):
        return self._VALID_FINSTRTREEPROXY_MUST_BE_PROVIDED

    @property
    def VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED(self):
        return self._VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED

    @property
    def TRADE_S_NOT_FOUND(self):
        return self._TRADE_S_NOT_FOUND

    @property
    def INNER_TRADE_DNE(self):
        return self._INNER_TRADE_DNE

    @property
    def COULD_NOT_CALC_SCA_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_SCA_ATTR_TRADE

    @property
    def COULD_NOT_CALC_MONF_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_MONF_ATTR_TRADE

    @property
    def COULD_NOT_CALC_UNDER_INSTR_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_UNDER_INSTR_ATTR_TRADE

    @property
    def COULD_NOT_CALC_LEG_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_LEG_ATTR_TRADE

    @property
    def COULD_NOT_CALC_INTS_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_INTS_ATTR_TRADE

    @property
    def COULD_NOT_CALC_SCALAR_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_SCALAR_ATTR_TRADE

    @property
    def COULD_NOT_CALC_STATIC_ATTR_TRADE(self):
        return self._COULD_NOT_CALC_STATIC_ATTR_TRADE

    @property
    def TRD_STATIC_CONTAINER_NO_SERIALIZED_DATA(self):
        return self._TRD_STATIC_CONTAINER_NO_SERIALIZED_DATA

    @property
    def TRD_STATIC_CONTAINS_NO_VALID_FTRADE_INSTANCE(self):
        return self._TRD_STATIC_CONTAINS_NO_VALID_FTRADE_INSTANCE

    @property
    def CREATE_THE_TRADE(self):
        return self._CREATE_THE_TRADE

    @property
    def VALID_FSTL_INSTANCE_MUST_BE_PROVIDED(self):
        return self._VALID_FSTL_INSTANCE_MUST_BE_PROVIDED

    @property
    def INNER_STL_CONTAINER_DNE(self):
        return self._INNER_STL_CONTAINER_DNE

    @property
    def STL_NOT_FOUND(self):
        return self._STL_NOT_FOUND

    @property
    def COULD_NOT_CALC_SCALAR_ATTR_S(self):
        return self._COULD_NOT_CALC_SCALAR_ATTR_S

    @property
    def COULD_NOT_CALC_STATIC_ATTR_S(self):
        return self._COULD_NOT_CALC_STATIC_ATTR_S

    @property
    def COULD_NOT_CALC_SENSITIVITY_WB(self):
        return self._COULD_NOT_CALC_SENSITIVITY_WB

    @property
    def COULD_NOT_GET_REQ_TRACKER_RESULT(self):
        return self._COULD_NOT_GET_REQ_TRACKER_RESULT

    @property
    def UPDATE_REQ_END_FAILED_S(self):
        return self._UPDATE_REQ_END_FAILED_S

    @property
    def UPDATE_REQ_TRACKER_START_FAILED_S(self):
        return self._UPDATE_REQ_TRACKER_START_FAILED_S

    @property
    def UPDATE_REQ_COLL_TRACKER_START_FAILED_S(self):
        return self._UPDATE_REQ_COLL_TRACKER_START_FAILED_S

    @property
    def CREATE_REQ_COLL_TRACKER_FAILED_S(self):
        return self._CREATE_REQ_COLL_TRACKER_FAILED_S

    @property
    def VALID_FTREEPROXY_MUST_BE_PROVIDED(self):
        return self._VALID_FTREEPROXY_MUST_BE_PROVIDED
    @property
    def WS_NAME_NOT_SET(self):
        return self._WS_NAME_NOT_SET
    @property
    def METHOD_GETFOBJECT_NOT_IMPLEMENTED(self):
        return self._METHOD_GETFOBJECT_NOT_IMPLEMENTED
    @property
    def NO_FIRST_CHILD_NODE_TREE_PROXY(self):
        return self._NO_FIRST_CHILD_NODE_TREE_PROXY
    @property
    def NO_TOP_LEVEL_NODE_TREE_PROXY(self):
        return self._NO_TOP_LEVEL_NODE_TREE_PROXY
    @property
    def VALID_WS_MUST_BE_PROVIDED(self):
        return self._VALID_WS_MUST_BE_PROVIDED
    @property
    def SAVE_DATA_NOT_IMPLEMENTED_ERROR(self):
        return self._SAVE_DATA_NOT_IMPLEMENTED_ERROR
    @property
    def CREATE_SQL_PARAMETERS(self):
        return self._CREATE_SQL_PARAMETERS
    @property
    def CREATE_THE_SETTLEMENT(self):
        return self._CREATE_THE_SETTLEMENT
    @property
    def CREATE_THE_PORTFOLIO(self):
        return self._CREATE_THE_PORTFOLIO
    @property
    def CREATE_THE_INSTRUMENT(self):
        return self._CREATE_THE_INSTRUMENT
    @property
    def F_SETTLEMENT_INSTANCE(self):
        return self._F_SETTLEMENT_INSTANCE
    def F_PORTFOLIO_INSTANCE(self):
        return self._F_PORTFOLIO_INSTANCE
    def F_INSTRUMENT_INSTANCE(self):
        return self._F_INSTRUMENT_INSTANCE
    @property
    def NOT_HAVE_SERIALIZED_DATA(self):
        return self._NOT_HAVE_SERIALIZED_DATA
    @property
    def THE_SQL_DATA_PROVIDER_S(self):
        return self._THE_SQL_DATA_PROVIDER__S
    @property
    def REGISTER_THE_BATCH_S(self):
        return self._REGISTER_THE_BATCH__S
    @property
    def TRACKER_AS_STARTED_S(self):
        return self._TRACKER_AS_STARTED__S
    @property
    def TRACKER_AS_COMPLETED_S(self):
        return self._TRACKER_AS_COMPLETED__S
    @property
    def COLLECTION_TRACKER_S(self):
        return self._COLLECTION_TRACKER__S
    @property
    def SAVE_THE_TRADES_S(self):
        return self._SAVE_THE_TRADES__S
    @property
    def SAVE_THE_SETTLEMENTS_S(self):
        return self._SAVE_THE_SETTLEMENTS__S
    @property
    def SINGLETON_IS_ALLOWED(self):
        return self._SINGLETON_IS_ALLOWED_
    @property
    def CALCULATION_SINGLETON_S(self):
        return self._CALCULATION_SINGLETON__S
    @property
    def DYNAMIC_CALCULATIONS(self):
        return self._DYNAMIC_CALCULATIONS
    @property
    def COLUMNS_FOR_SHEET_S_S(self):
        return self._COLUMNS_FOR_SHEET_S__S
    @property
    def CONTAINS_NO_COLUMNS(self):
        return self._CONTAINS_NO_COLUMNS
    @property
    def WORKSPACE_WORKSHEETS_MUST_BE_UNIQUE(self):
        return self._WORKSPACE_WORKSHEETS_MUST_BE_UNIQUE
    @property
    def WORKSHEETS_MUST_BE_UNIQUE(self):
        return self._WORKSHEETS_MUST_BE_UNIQUE
    @property
    def WORKBOOKS_MUST_BE_UNIQUE(self):
        return self._WORKBOOKS_MUST_BE_UNIQUE
    @property
    def NOT_LOAD_WORKBOOK_S(self):
        return self._NOT_LOAD_WORKBOOK_S
    @property
    def THE_GLOBAL_VALUE_S(self):
        return self._THE_GLOBAL_VALUE_S_
    @property
    def THE_FOLLOWING_ERROR_S(self):
        return self._THE_FOLLOWING_ERROR_S
    @property
    def VALUES_FOR_SHEET_S_S(self):
        return self._VALUES_FOR_SHEET_S__S
    @property
    def SPACE_FOUND_FOR_SHEET(self):
        return self._SPACE_FOUND_FOR_SHEET_
    @property
    def COLUMNS_FOUND_FOR_SHEET(self):
        return self._COLUMNS_FOUND_FOR_SHEET_
    @property
    def PASSED_FOR_CALCULATION(self):
        return self._PASSED_FOR_CALCULATION
    @property
    def CREATE_SQL_PARAMETERS_FAILED(self):
        return self._CREATE_SQL_PARAMETERS_FAILED
    @property
    def REQUEST_END_FAILED_S(self):
        return self._REQUEST_END_FAILED__S
    @property
    def TRACKER_FAILED_S(self):
        return self._TRACKER_FAILED__S
    @property
    def BATCH_TRACKER_FAILED_S(self):
        return self._BATCH_TRACKER_FAILED__S
    @property
    def REQUEST_ENTITY_FAILED_S(self):
        return self._REQUEST_ENTITY_FAILED__S
    @property
    def MUST_BE_PROVIDED(self):
        return self._MUST_BE_PROVIDED
    @property
    def FC_TRD_DATA_TYPE_MUST_BE_PROVIDED(self):
        return self._FC_TRD_DATA_TYPE_MUST_BE_PROVIDED
    @property
    def TYPE_S_IS_NOT_SUPPORTED(self):
        return self._TYPE_S_IS_NOT_SUPPORTED
    @property
    def FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED(self):
        return self._FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED
    @property
    def TYPE_IS_REQUIRED(self):
        return self._TYPE_IS_REQUIRED


