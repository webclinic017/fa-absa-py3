"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentProcessingParameters
    
DESCRIPTION
    This module contains parameters used to configure document processing functionality
    within Front Arena.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-02-05      FAOPS-741       Cuen Edwards            Kgomotso Gumbo          Replaced pre-settlement advice event listener with task.
2020-04-20      FAOPS-702       Joash Moodley                                   XLS Broker Note Generation via business process.
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Added Support for SBL Security Loans
                                                                                Confirmations
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Relocated list of subscribed tables from ATS module
                                                                                DocumentProcessingMain.
2020-05-08      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Addition of SARB security transfer instructions.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import BrokerNoteBulkGeneral
from BrokerNoteBulkEventHandler import BrokerNoteBulkEventHandler
from BrokerNoteBulkProcessor import BrokerNoteBulkProcessor
from DocumentBusinessProcessEventHandler import DocumentBusinessProcessEventHandler
import EnvironmentFunctions
import PreSettlementAdviceGeneral
from PreSettlementAdviceProcessor import PreSettlementAdviceProcessor
import SecurityLoanGeneral
from SecurityLoanNewTradeEventHandler import SecurityLoanNewTradeEventHandler
from SecurityLoanNewTradeProcessor import SecurityLoanNewTradeProcessor
import SARBSecurityTransferInstructionGeneral
from SARBSecurityTransferInstructionProcessor import SARBSecurityTransferInstructionProcessor


ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_document_processing_parameter('Host'),
    amb_port=EnvironmentFunctions.get_document_processing_parameter('Port'),
    amb_login=EnvironmentFunctions.get_document_processing_parameter('Login')
)

receiverMBName = EnvironmentFunctions.get_document_processing_parameter('ReceiverName')

receiverSource = EnvironmentFunctions.get_document_processing_parameter('ReceiverSource')

event_tables = [
    'BUSINESSPROCESS',
    'INSTRUMENT',
    'TRADE',
    'PARTY'
]

state_chart_names = [
    PreSettlementAdviceGeneral.get_advice_state_chart_name(),
    BrokerNoteBulkGeneral.get_broker_note_state_chart_name(),
    SecurityLoanGeneral.get_state_chart_name(),
    SARBSecurityTransferInstructionGeneral.get_instruction_state_chart_name()
]

event_name_to_processor_map = {
    'Pre-settlement Advice': PreSettlementAdviceProcessor(),
    'Broker Note Bulk': BrokerNoteBulkProcessor(),
    'SecurityLoan Confirmation': SecurityLoanNewTradeProcessor(),
    'SARB Security Transfer From CD': SARBSecurityTransferInstructionProcessor(),
    'SARB Security Transfer To CD': SARBSecurityTransferInstructionProcessor()
}

event_handlers = [
    DocumentBusinessProcessEventHandler(),
    BrokerNoteBulkEventHandler(),
    SecurityLoanNewTradeEventHandler()
]
