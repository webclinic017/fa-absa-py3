"""-----------------------------------------------------------------------------
PURPOSE              :  SBL amendment process to record all Trade, Instrument, 
                        and Settlement updates done by the OPS SecLend and 
                        PCG Collateral user groups.
REQUESTER, DEPATMENT :  Jennitha Jugnath, PTS
PROJECT              :  SBL onto FA
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-05-26  CHG0102232     Libor Svoboda       Initial implementation
"""
import datetime
import os


import acm
import amb
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_amba_message import AmbaMessage
from at_ats_utils import AmbConnection, XmlOutput
from sbl_amends_util import FPARAM_NAME, AmendmentSource, OutputConverter


LOGGER = getLogger(__name__)
AMB_CONNECTION = AmbConnection(FPARAM_NAME)

OUTPUT_FILE = 'SBL_Amendments_{:%Y-%m-%d}.xml'
OUTPUT_DIR = '/services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
ATS_PARAMS = {
    'path': OUTPUT_PATH,
}
OUTPUT = {}


ael_variables = AelVariableHandler()
ael_variables.add(
    'output_dir',
    label='Output Directory',
    default=OUTPUT_DIR,
)
ael_variables.add(
    'output_file',
    label='Output File',
    default=OUTPUT_FILE,
)


def init_output(msg_date):
    dt = datetime.datetime(*acm.Time.DateToYMD(msg_date))
    output_path = ATS_PARAMS['path'].format(dt)
    output = XmlOutput()
    output.init_file(output_path)
    OUTPUT[msg_date] = output
    LOGGER.info('Init output file %s' % output_path)


def write_to_output(xml_string, msg_date):
    if not msg_date in OUTPUT:
        init_output(msg_date)
    OUTPUT[msg_date].write(xml_string)


class MessageProcessor(object):
    
    def __init__(self, msg_object):
        self._msg_object = msg_object
        self._table_name = msg_object.table_name
        self._operation = msg_object.operation
        self._table = msg_object.parent_table
    
    def _get_table_attr(self, field_name, state='current'):
        return self._table.attributes[field_name][state]
    
    def _get_oid(self):
        if self._table_name == 'TRADE':
            return int(self._get_table_attr('TRDNBR'))
        if self._table_name == 'INSTRUMENT':
            return int(self._get_table_attr('INSADDR'))
        if self._table_name == 'SETTLEMENT':
            return int(self._get_table_attr('SEQNBR'))
        msg = 'Invalid table "%s", TRADE, INSTRUMENT or SETTLEMENT expected.' % self._table_name
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    def process(self):
        LOGGER.info('ATS Worker - processing started - %s.' % acm.Time.TimeNow())
        oid = self._get_oid()
        LOGGER.info('%s %s: %s' % (self._table_name, self._operation, oid))
        if oid < 0:
            LOGGER.info('Ignoring object with negative Oid.')
            return
        source = AmendmentSource(oid, self._msg_object)
        source.check_differences()
        if not source.differences:
            LOGGER.info('Ignoring object, no differences found.')
            return
        output_converter = OutputConverter(source)
        output_converter.create_output()
        xml_string = output_converter.get_string()
        write_to_output(xml_string, source.msg_date)
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


def start():
    AMB_CONNECTION.connect()
    init_output(acm.Time.DateToday())


def start_ex(params):
    output_path = os.path.join(params['output_dir'], params['output_file'])
    ATS_PARAMS['path'] = output_path
    start()


def stop():
    for output in list(OUTPUT.values()):
        output.close_file()
        LOGGER.info('%s closed at %s.' % (output.get_path(), acm.Time.TimeNow()))


def work():
    while not AMB_CONNECTION.queue.empty():
        event, channel_number, amb_message_number = AMB_CONNECTION.queue.get()
        LOGGER.info('Started processing: %s' % amb_message_number)
        message_buffer = amb.mbf_create_buffer_from_data(event.data_p)
        amba_message = message_buffer.mbf_read()
        msg_object = AmbaMessage(amba_message)
        try:
            msg_processor = MessageProcessor(msg_object)
            msg_processor.process()
        except: 
             LOGGER.exception('Message processing failed.')
        amb.mb_queue_accept(channel_number, event, str(amb_message_number))
        amba_message.mbf_destroy_object()
        message_buffer.mbf_destroy_buffer()
        LOGGER.info('Processing done: %s' % amb_message_number)
    
    if AMB_CONNECTION.disconnected and AMB_CONNECTION.queue.empty():
        AMB_CONNECTION.connect()
