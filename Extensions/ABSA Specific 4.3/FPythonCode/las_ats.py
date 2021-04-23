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
import json
import ssl
try:
    import urllib.request as urlrequest
    from urllib.error import HTTPError
    from http import client
    from urllib.parse import urlparse, quote
except ImportError:
    # Python 2
    import urllib2 as urlrequest
    from urllib.error import HTTPError
    import httplib as client
    from urlparse import urlparse
    from urllib.parse import quote

import acm
import amb
import las_product_mapping
from at_ael_variables import AelVariableHandler
from at_amba_message import AmbaMessage
from at_ats_utils import AmbConnection, get_api_config, get_param_value
from at_decorators import retry
from at_logging import getLogger
from las_util import (STATE_CHART, API_CONFIG, AGREEMENTS,
                      FPARAM_CURRENCY_TO_VAL_GROUP,
                      FPARAM_INDEX_TO_VAL_GROUP,
                      POPULATE_DEFAULTS_RETRIES,
                      DELETE_DEFAULTS_RETRIES,
                      UPDATED_FIELDS_TRIGGER_REQUEST,
                      UPDATED_FIELDS_VAL_GRP_UPDATE,
                      KerberosAuth, get_last_step,
                      get_process_for_trade,
                      is_amwi_cleared_trade)


LOGGER = getLogger(__name__)
AMB_CONNECTION = AmbConnection(ignore_instance_name=True)


ael_variables = AelVariableHandler()
ael_variables.add(
    'fparam_name',
    label='FParameters Name',
)
ael_variables.add(
    'queue_delay',
    label='Queue Delay',
    default=0,
    cls='int',
)


class InvalidMessage(Exception):
    pass


class LegalServiceApiError(Exception):
    pass


class LegalServiceMissingDataError(Exception):
    pass


@retry(LegalServiceApiError, tries=5, delay=1, logger=LOGGER)
def http_get(url):
    kerb_auth = KerberosAuth()
    request = urlrequest.Request(url, headers=kerb_auth.headers)
    try:
        response = urlrequest.urlopen(request, context=ssl._create_unverified_context())
    except HTTPError as error:
        LOGGER.info('Request failed: %s.' % url)
        if error.code == 404:
            raise LegalServiceMissingDataError('Legal data not found.')
        if KerberosAuth.is_kerberos_auth(error):
            kerb_auth.authenticate()
        raise LegalServiceApiError(str(error))
    except Exception as exc:
        raise LegalServiceApiError('Exception: %s' % str(exc))
    else:
        if response.code != client.OK:
            raise LegalServiceApiError('Failed to retrieve data, code %s.' % response.code)
    kerb_auth.respond(response)
    return json.loads(response.read())


def get_record_type(amba_message):
    business_obj = amba_message.mbf_last_object()
    if not business_obj:
        raise InvalidMessage('Missing business object.')
    return business_obj.mbf_find_object('RECORD_TYPE').mbf_get_value()


def get_acm_object(amba_message):
    business_obj = amba_message.mbf_last_object()
    if not business_obj:
        raise InvalidMessage('Missing business object.')
    record_type = business_obj.mbf_find_object('RECORD_TYPE').mbf_get_value()
    if record_type == 'Trade':
        oid = int(business_obj.mbf_find_object('TRDNBR').mbf_get_value())
        acm.PollDbEvents()
        return acm.FTrade[oid]
    if record_type == 'BusinessProcess':
        oid = int(business_obj.mbf_find_object('SEQNBR').mbf_get_value())
        acm.PollDbEvents()
        return acm.FBusinessProcess[oid]
    raise InvalidMessage('Invalid record type "%s".' % record_type)


def get_operation(amba_message):
    msg_type = amba_message.mbf_find_object('TYPE').mbf_get_value()
    type_split = msg_type.split('_')
    if len(type_split) == 2:
        return type_split[0]
    raise InvalidMessage('Missing operation "%s".' % msg_type)


def get_add_info(msg_object, addinf_spec):
    tables = msg_object.get_tables('ADDITIONALINFO')
    for table in tables:
        if ('ADDINF_SPECNBR.FIELD_NAME' in table.attributes
                and table.attributes['ADDINF_SPECNBR.FIELD_NAME']['current'] == addinf_spec):
            return table.attributes['VALUE']['current']
    return ''


def get_updated_fields(msg_object, fields_dict):
    updates = []
    if (msg_object.parent_table.attributes['STATUS']['current'] 
                in ('BO Confirmed', 'BO-BO Confirmed')
            and not get_add_info(msg_object, 'CCPclearing_process').startswith('LCH')):
        # Only AMWI clearing trades are considered in 'BO Confirmed' or 'BO-BO Confirmed'
        return []
    for table in msg_object.get_tables():
        if not table.operation:
            continue
        if table.name not in fields_dict:
            continue
        if table.name == 'TRADE':
            if table.operation != 'UPDATE':
                continue
            for field in fields_dict[table.name]:
                if (field in table.attributes 
                        and table.attributes[field]['operation'] == 'UPDATE'):
                    if (field == 'TIME'
                        and table.attributes[field]['current'][:10] 
                            == table.attributes[field]['previous'][:10]):
                        continue
                    LOGGER.info('Update processing triggerd by %s %s update.'
                                % (table.name, field))
                    updates.append((table.name, field))
        elif table.name == 'ADDITIONALINFO':
            try:
                field = table.attributes['ADDINF_SPECNBR.FIELD_NAME']['current']
            except KeyError:
                continue
            if field in fields_dict[table.name]:
                LOGGER.info('Update processing triggerd by %s %s update.'
                             % (table.name, field)) 
                updates.append((table.name, field))
    return updates


def discount_index_updated(updated_fields):
    return (len(updated_fields) == 1 
            and updated_fields[0] == ('ADDITIONALINFO', 'LAS_Discount_Index'))


class BusinessProcessWorker(object):
    
    state_chart = STATE_CHART
    
    def __init__(self, bp):
        self._bp = bp
        self._trade = bp.Subject()
        self._log_str = 'Trade %s (process %s)' % (self._trade.Oid(), self._bp.Oid())
    
    @staticmethod
    def force_to_state(bp, state, reason=''):
        try:
            bp.ForceToState(state, reason)
            bp.Commit()
        except:
            LOGGER.exception('Process %s failed to force to "%s".' 
                             % (bp.Oid(), state))
            raise
        LOGGER.info('Process %s successfully forced to "%s".' 
                    % (bp.Oid(), state))
    
    @staticmethod
    def handle_event(bp, event, params=None):
        try:
            bp.HandleEvent(event, params)
            bp.Commit()
        except:
            LOGGER.exception('Process %s failed to handle event "%s".' 
                             % (bp.Oid(), event))
            raise
        LOGGER.info('Process %s handled event "%s" successfully.' 
                    % (bp.Oid(), event))
    
    @staticmethod
    def get_url(trade_date, party_id, product_id, trade_id=None):
        url = '%s/api/ISDA/%s/%s/%s' % (API_CONFIG['address'], trade_date, 
                                        party_id, quote(product_id, safe=''))
        if trade_id:
            url += '?faId=%s' % trade_id
        return url
    
    @staticmethod
    def get_product(trade):
        return las_product_mapping.get_product(trade)
    
    @staticmethod
    def convert_to_params(las_data):
        agreements = las_data['isdaAgreements']
        defaults = acm.FDictionary()
        defaults['ISDA'] = ''
        defaults['CSA'] = ''
        defaults['IM'] = ''
        defaults['Discount_Index'] = ''
        options = acm.FDictionary()
        indices = acm.FDictionary()
        for agreement in agreements:
            isda = acm.FDictionary()
            csa = acm.FList()
            if agreement['default']:
                defaults['ISDA'] = str(agreement['name'])
            for csa_agreement in agreement['vmAgreements']:
                discount_index = acm.FList()
                csa.AddLast(str(csa_agreement['name']))
                if csa_agreement['default'] and agreement['default']:
                    defaults['CSA'] = str(csa_agreement['name'])
                for factor in csa_agreement['discountFactors']:
                    discount_index.AddLast(str(factor['factor']))
                    if factor['default'] and csa_agreement['default'] and agreement['default']:
                        defaults['Discount_Index'] = str(factor['factor'])
                indices[str(csa_agreement['name'])] = discount_index
            isda['CSA'] = csa
            im = acm.FList()
            for im_agreement in agreement['imAgreements']:    
                im.AddLast(str(im_agreement['name']))
                if im_agreement['default'] and agreement['default']:
                    defaults['IM'] = str(im_agreement['name'])
            isda['IM'] = im
            options[str(agreement['name'])] = isda
        params = acm.FDictionary()
        params['defaults'] = defaults
        params['options'] = options
        params['indices'] = indices
        return params
    
    @staticmethod
    def val_group_update_applicable(trade):
        instrument = trade.Instrument()
        trades = acm.FTrade.Select('instrument="%s" and status '
                                   'in ("FO Confirmed", "BO Confirmed", "BO-BO Confirmed")'
                                   % instrument.Name())
        if not trades:
            return True
        trade_count = len(trades)
        if trade_count > 2:
            return False
        if trade_count == 2:
            return (trades[0].MirrorTrade() 
                    and trades[0].MirrorTrade() == trades[1].MirrorTrade())
        return True
    
    def _request_las_data(self):
        trade_date = self._trade.TradeTime()[:10]
        party_id = self._trade.Counterparty().Oid()
        product_id = self.get_product(self._trade)
        url = self.get_url(trade_date, party_id, product_id, self._trade.Oid())
        try:
            return http_get(url)
        except:
            LOGGER.error('%s: Failed to get LAS data for %s, party %s, product %s.'
                         % (self._log_str, trade_date, party_id, product_id))
            raise
    
    def _clear_add_infos(self):
        clone = self._trade.Clone()
        for add_info in clone.AddInfos()[:]:
            if add_info.AddInf().Name() in AGREEMENTS.values():
                LOGGER.info('%s: Clearing add info %s.' 
                            % (self._log_str, add_info.AddInf().Name()))
                clone.AddInfos().Remove(add_info)
        self._trade.Apply(clone)
        self._trade.Commit()
    
    def _process_data_request(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        las_data = None
        data_not_found = False
        error_msg = 'Data not received.'
        try:
            las_data = self._request_las_data()
        except LegalServiceMissingDataError as error:
            error_msg = str(error)
            LOGGER.exception('%s: Failed to request data.' % self._log_str)
            data_not_found = True
        except Exception as exc:
            error_msg = str(exc)
            LOGGER.exception('%s: Failed to request data.' % self._log_str)
        if data_not_found:
            self.force_to_state(self._bp, 'Data Not Received', error_msg)
            return
        if not las_data:
            self.force_to_state(self._bp, 'Request Failed', error_msg)
            return
        LOGGER.info('%s: Data requsted successfully.' % self._log_str)
        params = self.convert_to_params(las_data)
        self.handle_event(self._bp, 'Success', params)
    
    def _process_data_received(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        self.handle_event(self._bp, 'Populate Defaults')
    
    def _process_data_not_received(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        self.handle_event(self._bp, 'Delete Defaults')
    
    def _process_populate_defaults(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        error_msg = ''
        data_step = get_last_step(self._bp, 'Data Received')
        params = data_step.DiaryEntry().Parameters()
        defaults = params['defaults']
        if not defaults:
            error_msg = 'Defaults not found.'
            LOGGER.error('%s: %s' % (self._log_str, error_msg))
            self.force_to_state(self._bp, 'Defaults Update Failed', error_msg)
            return
        image = self._trade.StorageImage()
        try:
            for data_type, add_info_name in AGREEMENTS.iteritems():
                current_value = getattr(self._trade.AdditionalInfo(), add_info_name)()
                if defaults[data_type]:
                    LOGGER.info('%s: Populating default %s: %s.' 
                                % (self._log_str, data_type, defaults[data_type]))
                    setattr(image.AdditionalInfo(), add_info_name, defaults[data_type])
                elif current_value:
                    LOGGER.info('%s: No default %s received, clearing current add info %s.' 
                                % (self._log_str, data_type, add_info_name))
                    for add_info in image.AddInfos()[:]:
                        if add_info.AddInf().Name() == add_info_name:
                            image.AddInfos().Remove(add_info)
            image.Commit()
        except Exception as exc:
            error_msg = str(exc)
            LOGGER.exception('%s: Failed to populate defaults.' % self._log_str)
        if error_msg:
            self.force_to_state(self._bp, 'Defaults Update Failed', error_msg)
            return
        LOGGER.info('%s: Defaults populated successfully.' % self._log_str)
        if ((defaults['Discount_Index'] or is_amwi_cleared_trade(self._trade))
                and self.val_group_update_applicable(self._trade)):
            self.handle_event(self._bp, 'Update Val Group')
        else:
            self.handle_event(self._bp, 'Success')
    
    def _process_delete_defaults(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        error_msg = ''
        clone = self._trade.Clone()
        for add_info in clone.AddInfos()[:]:
            if add_info.AddInf().Name() in AGREEMENTS.values():
                LOGGER.info('%s: Clearing add info %s.' 
                            % (self._log_str, add_info.AddInf().Name()))
                clone.AddInfos().Remove(add_info)
        try:
            self._trade.Apply(clone)
            self._trade.Commit()
        except Exception as exc:
            error_msg = str(exc)
            LOGGER.exception('%s: Failed to delete defaults.' % self._log_str)
        if error_msg:
            self.force_to_state(self._bp, 'Defaults Delete Failed', error_msg)
            return
        LOGGER.info('%s: Defaults deleted successfully.' % self._log_str)
        self.handle_event(self._bp, 'Success')
    
    def _get_val_group_name(self):
        if is_amwi_cleared_trade(self._trade):
            currency = self._trade.Instrument().Currency().Name()
            return get_param_value(FPARAM_CURRENCY_TO_VAL_GROUP, currency)
        discount_index = getattr(self._trade.AdditionalInfo(), AGREEMENTS['Discount_Index'])()
        return get_param_value(FPARAM_INDEX_TO_VAL_GROUP, discount_index)
    
    def _process_update_val_group(self):
        # Only logging in this step, actual val group updates planned for the next phase.
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        current_val_grp_name = (self._trade.Instrument().ValuationGrpChlItem().Name() 
                                if self._trade.Instrument().ValuationGrpChlItem() else '')
        LOGGER.info('%s: Current val group "%s".' 
                    % (self._log_str, current_val_grp_name))
        try:
            val_grp_name = self._get_val_group_name()
        except:
            error_msg = 'Failed to get val group name.'
            LOGGER.exception('%s: %s' % (self._log_str, error_msg))
        else:
            LOGGER.info('%s: Selected val group "%s".' 
                        % (self._log_str, val_grp_name))
        LOGGER.info('%s: Val group update applicable: %s.'
                    % (self._log_str, self.val_group_update_applicable(self._trade)))
        self.handle_event(self._bp, 'Success')
    
    def _process_defaults_update_failed(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        visited_states = [state.Name() for state in reversed(self._bp.VisitedStates())]
        data_received_index = 0
        try:
            data_received_index = visited_states.index('Data Received')
        except ValueError:
            LOGGER.warning('%s: Cannot retry, "Data Received" step not found.' 
                           % self._log_str)
            return
        current_update_count = visited_states[:data_received_index].count('Populating Defaults')
        if current_update_count > POPULATE_DEFAULTS_RETRIES:
            LOGGER.info('%s: Not retrying again, already tried %s times.' 
                        % (self._log_str, current_update_count))
            return
        LOGGER.info('%s: Tried to update defaults %s times, retrying...' 
                    % (self._log_str, current_update_count))
        self.handle_event(self._bp, 'Retry')
    
    def _process_defaults_delete_failed(self):
        LOGGER.info('%s: Processing state "%s".' 
                    % (self._log_str, self._bp.CurrentStep().State().Name()))
        visited_states = [state.Name() for state in reversed(self._bp.VisitedStates())]
        data_not_received_index = 0
        try:
            data_not_received_index = visited_states.index('Data Not Received')
        except ValueError:
            LOGGER.warning('%s: Cannot retry, "Data Not Received" step not found.' 
                           % self._log_str)
            return
        current_update_count = visited_states[:data_not_received_index].count('Deleting Defaults')
        if current_update_count > DELETE_DEFAULTS_RETRIES:
            LOGGER.info('%s: Not retrying again, already tried %s times.' 
                        % (self._log_str, current_update_count))
            return
        LOGGER.info('%s: Tried to delete defaults %s times, retrying...' 
                    % (self._log_str, current_update_count))
        self.handle_event(self._bp, 'Retry')
    
    def process(self):
        if self._bp.StateChart() != self.state_chart:
            return
        current_state = self._bp.CurrentStep().State().Name()
        if current_state == 'Requesting Legal Data':
            self._process_data_request()
        elif current_state == 'Data Received':
            self._process_data_received()
        elif current_state == 'Data Not Received':
            self._process_data_not_received()
        elif current_state == 'Populating Defaults':
            self._process_populate_defaults()
        elif current_state == 'Deleting Defaults':
            self._process_delete_defaults()
        elif current_state == 'Updating Val Group':
            self._process_update_val_group()
        elif current_state == 'Defaults Update Failed':
            self._process_defaults_update_failed()
        elif current_state == 'Defaults Delete Failed':
            self._process_defaults_delete_failed()


class TradeWorker(object):
    
    state_chart = STATE_CHART
    
    def __init__(self, trade):
        self._trade = trade
    
    @staticmethod
    def move_process(bp, new_state):
        BusinessProcessWorker.force_to_state(bp, new_state)
    
    def _init_process(self):
        bp = get_process_for_trade(self._trade, self.state_chart)
        if bp:
            return bp
        try:
            bp = acm.BusinessProcess.InitializeProcess(self._trade, self.state_chart)
            bp.Commit()
        except:
            LOGGER.exception('Failed to initialize process for trade %s.' % self._trade.Oid())
            raise
        LOGGER.info('Initialized process %s for trade %s.' % (bp.Oid(), self._trade.Oid()))
        return bp
    
    def process(self):
        bp = self._init_process()
        self.move_process(bp, 'Requesting Legal Data')


class TradeWorkerUpdateValGroup(TradeWorker):
    
    def process(self):
        bp = get_process_for_trade(self._trade, self.state_chart)
        if not bp:
            LOGGER.info('Business process not found for trade %s.' % self._trade.Oid())
            return
        if not bp.CurrentStep().IsInEndState():
            LOGGER.info('Current step "%s" is not an end state.' % bp.CurrentStateName())
            return
        discount_index = getattr(self._trade.AdditionalInfo(), AGREEMENTS['Discount_Index'])()
        if not discount_index:
            LOGGER.info('Add info %s not populated on trade %s.' 
                        % (AGREEMENTS['Discount_Index'], self._trade.Oid()))
            return
        if not BusinessProcessWorker.val_group_update_applicable(self._trade):
            LOGGER.info('Val group update not applicable for trade %s.' % self._trade.Oid())
            return
        self.move_process(bp, 'Updating Val Group')


def start():
    AMB_CONNECTION.connect()


def start_ex(params):
    fparam_name = params['fparam_name']
    LOGGER.info('Using FParameters "%s".' % fparam_name)
    AMB_CONNECTION.fparam_name = fparam_name
    queue_delay = params['queue_delay']
    if queue_delay:
        LOGGER.info('Using delayed queue by %s seconds.' % queue_delay)
        AMB_CONNECTION.init_delayed_queue(queue_delay)
    start()


def get_worker(amba_message):
    record_type = get_record_type(amba_message)
    if record_type == 'Trade':
        operation = get_operation(amba_message)
        if operation == 'INSERT':
            acm_object = get_acm_object(amba_message)
            return TradeWorker(acm_object)
        if operation == 'UPDATE':
            msg_object = AmbaMessage(amba_message)
            if get_updated_fields(msg_object, UPDATED_FIELDS_TRIGGER_REQUEST):
                acm_object = get_acm_object(amba_message)
                return TradeWorker(acm_object)
            if get_updated_fields(msg_object, UPDATED_FIELDS_VAL_GRP_UPDATE):
                acm_object = get_acm_object(amba_message)
                return TradeWorkerUpdateValGroup(acm_object)
    elif record_type == 'BusinessProcess':
        acm_object = get_acm_object(amba_message)
        try:
            acm_version_id = acm_object.VersionId()
        except:
            acm_version_id = 0
        msg_object = AmbaMessage(amba_message)
        try:
            msg_version_id = int(msg_object.parent_table.attributes['VERSION_ID']['current'])
        except:
            msg_version_id = 0
        LOGGER.info('ACM object version ID: %s' % acm_version_id)
        LOGGER.info('MSG object version ID: %s' % msg_version_id)
        if msg_version_id < acm_version_id:
            LOGGER.warning('Message Version ID lower than ACM object, skipping message...')
            return None
        return BusinessProcessWorker(acm_object)
    return None


def work():
    while not AMB_CONNECTION.queue.empty():
        event, channel_number, amb_message_number = AMB_CONNECTION.queue.get()
        LOGGER.info('Started processing: %s' % amb_message_number)
        message_buffer = amb.mbf_create_buffer_from_data(event.data_p)
        amba_message = message_buffer.mbf_read()
        try:
            worker_object = get_worker(amba_message)
            if worker_object:
                worker_object.process()
        except:
             LOGGER.exception('Message processing failed: %s.' 
                              % amba_message.mbf_object_to_string())
        amb.mb_queue_accept(channel_number, event, str(amb_message_number))
        amba_message.mbf_destroy_object()
        message_buffer.mbf_destroy_buffer()
        LOGGER.info('Processing done: %s' % amb_message_number)
    
    if AMB_CONNECTION.disconnected and AMB_CONNECTION.queue.empty():
        AMB_CONNECTION.connect()
