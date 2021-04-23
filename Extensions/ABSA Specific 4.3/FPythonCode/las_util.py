"""-----------------------------------------------------------------------------
PURPOSE              :  Legal Agreement Service (LAS) integration
DEVELOPER            :  Libor Svoboda
REQUESTER            :  Victor Mofokeng (CRT desk)
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-11-26  CHG0140652     Libor Svoboda       Initial implementation
2021-02-03  CHG0149970     Libor Svoboda       Add delayed queue
"""
import acm
from at_ats_utils import get_param_value, get_api_config
from at_classes import Singleton
from at_decorators import pickle_and_memoize
from at_logging import getLogger


LOGGER = getLogger(__name__)
STATE_CHART = acm.FStateChart['LegalAgreementService']
FPARAM_PARAMS = 'LAS_Params'
FPARAM_INDEX_TO_VAL_GROUP = 'LAS_IndexToValGroupMapping'
FPARAM_CURRENCY_TO_VAL_GROUP = 'LAS_CurrencyToValGroupMapping'
API_CONFIG = get_api_config(FPARAM_PARAMS)
POPULATE_DEFAULTS_RETRIES = 3
DELETE_DEFAULTS_RETRIES = 3
AMWI_USERS = [user.strip() for user 
              in get_param_value(FPARAM_PARAMS, 'AmwiUsers').split(',') if user]
HEADERS= {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
AGREEMENTS = {
    # LAS document type: trade add info
    'ISDA': 'LAS_ISDA_Agreement',
    'IM': 'LAS_IM_Agreement',
    'CSA': 'LAS_CSA_Agreement',
    'Discount_Index': 'LAS_Discount_Index',
}
UPDATED_FIELDS_TRIGGER_REQUEST = {
    'TRADE': (
        'TIME',
        'COUNTERPARTY_PTYNBR',
    ),
    'ADDITIONALINFO': (
        'Funding_Instype',
        'MM_Instype',
        'InsOverride',
    ),
}
UPDATED_FIELDS_VAL_GRP_UPDATE = {
    'ADDITIONALINFO': (
        'LAS_Discount_Index',
    ),
}


@pickle_and_memoize
def get_amba_params(param_name):
    values = get_param_value(FPARAM_PARAMS, param_name)
    param_values = [value.strip() for value 
                    in values.split(',') if value]
    LOGGER.info('Selected %s: %s.' 
                % (param_name, ', '.join(param_values)))
    return param_values


def get_steps(bp, state_name):
    return [step for step in bp.Steps() if step.State().Name() == state_name]


def get_last_step(bp, state_name):
    steps = get_steps(bp, state_name)
    if not steps:
        return None
    return sorted(steps, key=lambda x: x.CreateTime())[-1]


def is_amwi_cleared_trade(trade):
    return (trade.CreateUser() and trade.CreateUser().Name() in AMWI_USERS
            and trade.AdditionalInfo().CCPclearing_process().startswith('LCH'))


def get_add_info_values(trade_oid):
    acm.PollDbEvents()
    values = {add_info_name:None for add_info_name in AGREEMENTS.values()}
    bp = acm.FBusinessProcess.Select01('stateChart=%s and subject_seqnbr=%s and subject_type="Trade"' 
                                       % (STATE_CHART.Oid(), trade_oid), None)
    if not bp:
        LOGGER.debug('LAS: Could not find business process for trade %s.' % trade_oid)
        return values
    visited_states = [state.Name() for state in reversed(bp.VisitedStates())]
    data_received_index = 0
    try:
        data_received_index = visited_states.index('Data Received')
    except ValueError:
        LOGGER.debug('LAS: No data received for trade %s.' % trade_oid)
        return values
    data_not_received_index = len(visited_states)
    try:
        data_not_received_index = visited_states.index('Data Not Received')
    except ValueError:
        pass
    if data_received_index < data_not_received_index:
        data_step = get_last_step(bp, 'Data Received')
        params = data_step.DiaryEntry().Parameters()
        defaults = params['defaults']
        for data_type, add_info_name in AGREEMENTS.iteritems():
            if defaults[data_type]:
                values[add_info_name] = defaults[data_type]
    return values


def get_process_for_trade(trade, state_chart=STATE_CHART):
    if not trade:
        return None
    bps = acm.BusinessProcess.FindBySubjectAndStateChart(trade, state_chart)
    if bps:
        return bps[0]
    return None


def sender_modify(msg, subject):
    # ael_sender_modify AMBA hook
    send_to_amb = (msg, subject)
    msg_type = msg.mbf_find_object('TYPE').mbf_get_value()
    business_obj = msg.mbf_last_object()
    if not business_obj:
        msg_str = msg.mbf_object_to_string()
        LOGGER.warning('Sender modify: Invalid message %s' % msg_str)
        return None
    record_type = business_obj.mbf_find_object('RECORD_TYPE').mbf_get_value()
    if record_type == 'Trade':
        cpty_type = business_obj.mbf_find_object('COUNTERPARTY_PTYNBR.TYPE')
        if cpty_type and cpty_type.mbf_get_value() == 'Intern Dept':
            return None
        try:
            userid = business_obj.mbf_find_object('CREAT_USRNBR.USERID').mbf_get_value()
            grpid = business_obj.mbf_find_object('CREAT_USRNBR.GRPNBR.GRPID').mbf_get_value()
            acquirer = business_obj.mbf_find_object('ACQUIRER_PTYNBR.PTYID').mbf_get_value()
            status = business_obj.mbf_find_object('STATUS').mbf_get_value()
        except AttributeError:
            msg_str = msg.mbf_object_to_string()
            LOGGER.warning('Sender modify: Field missing, invalid message %s' % msg_str)
            return None
        if ((userid in get_amba_params('BookingUsersManual')
                    or grpid in get_amba_params('BookingGroupsManual'))
                and acquirer in get_amba_params('Acquirers')
                and status in get_amba_params('BookingStatusManual')):
            return send_to_amb
        if (userid in get_amba_params('BookingUsersFeed')
                and acquirer in get_amba_params('Acquirers')
                and status in get_amba_params('BookingStatusFeed')):
            return send_to_amb
        if (userid in get_amba_params('AmwiUsers')
                and acquirer in get_amba_params('Acquirers')
                and status in get_amba_params('AmwiUpdateStatus')):
            return send_to_amb
    if record_type == 'BusinessProcess':
        if 'UPDATE' not in msg_type:
            return None
        state_chart = business_obj.mbf_find_object('STATE_CHART_SEQNBR.NAME').mbf_get_value()
        if state_chart != STATE_CHART.Name():
            return None
        current_state = business_obj.mbf_find_object('CURRENT_STATE_NAME').mbf_get_value()
        if current_state in get_amba_params('DelayedStates'):
            return None
        return send_to_amb
    return None


def delayed_sender_modify(msg, subject):
    # ael_sender_modify AMBA hook
    send_to_amb = (msg, subject)
    msg_type = msg.mbf_find_object('TYPE').mbf_get_value()
    business_obj = msg.mbf_last_object()
    if not business_obj:
        msg_str = msg.mbf_object_to_string()
        LOGGER.warning('Sender modify: Invalid message %s' % msg_str)
        return None
    record_type = business_obj.mbf_find_object('RECORD_TYPE').mbf_get_value()
    if record_type == 'BusinessProcess':
        if 'UPDATE' not in msg_type:
            return None
        state_chart = business_obj.mbf_find_object('STATE_CHART_SEQNBR.NAME').mbf_get_value()
        if state_chart != STATE_CHART.Name():
            return None
        current_state = business_obj.mbf_find_object('CURRENT_STATE_NAME').mbf_get_value()
        if current_state in get_amba_params('DelayedStates'):
            return send_to_amb
    return None


class KerberosAuth(object, metaclass=Singleton):
    
    service = 'HTTP'
    
    def __init__(self):
        try:
            from urllib.parse import urlparse
        except ImportError:
            # Python 2
            from urlparse import urlparse
        self.headers = HEADERS
        self._context = None
        self._principal = API_CONFIG['principal']
        kerb_host = urlparse(API_CONFIG['address']).hostname
        self._kerb_spn = '%s@%s' % (self.service, kerb_host)
    
    @staticmethod
    def is_kerberos_auth(response):
        return (response.code == 401 
                and 'WWW-Authenticate' in response.info() 
                and 'negotiate' in response.info()['WWW-Authenticate'].lower())
    
    def authenticate(self):
        try:
            import kerberos as kerb
        except ImportError:
            import winkerberos as kerb
        _, self._context = kerb.authGSSClientInit(self._kerb_spn, 
                                                  principal=self._principal)
        kerb.authGSSClientStep(self._context, '')
        token = kerb.authGSSClientResponse(self._context)
        self.headers['Authorization'] = 'Negotiate ' + token
    
    def _clean(self, token):
        try:
            import kerberos as kerb
        except ImportError:
            import winkerberos as kerb
        kerb.authGSSClientStep(self._context, token)
        kerb.authGSSClientClean(self._context)
        self._context = None
    
    def respond(self, response):
        if 'WWW-Authenticate' in response.info():
            auth_split = response.info()['WWW-Authenticate'].split()
            if auth_split and auth_split[0].lower() == 'negotiate':
                if self._context:
                    self._clean(auth_split[1])
                self.authenticate()
