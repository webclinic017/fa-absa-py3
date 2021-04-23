"""Source a list of credit facilities from the ACM system and allow trader to select an appropriate facility pre-deal.
"""
import json
import requests

import acm
import FLogger
import FUxCore


CONFIG_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'CreditFacilitySelection').Value()
LOGGER = FLogger.FLogger(__name__, int(CONFIG_PARAMS['Front_Log_Verbosity'].Text()))

ACM_CONNECTION_ERROR = 'SYSTEM_ERROR'
ACM_NO_FACILITIES_RETURNED = 'NO FACILITY AVAILABLE'


class CreditFacilitySelection(FUxCore.LayoutDialog):
    def __init__(self, facility_data, facility_counterparty, trade_counterparty):
        self._facility_data = facility_data
        self._facility_counterparty = facility_counterparty
        self._trade_counterparty = trade_counterparty
        self._combo_facility_list = None
        self._lbl_FACILITYID_value = None
        self._lbl_DESCRIPTION_value = None
        self._lbl_FACILITYACTIVE_value = None
        self._lbl_STARTDATE_value = None
        self._lbl_EXPIRYDATE_value = None
        self._lbl_FACILITYAMOUNT_value = None
        self._lbl_FACILITYCURRENCY_value = None
        self._lbl_error_message = None
        self._lbl_party_from_trade_value = None
        self._lbl_override_with_party_value = None
        self._btn_change_party = None

    def create_layout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddSeparator()
        b.  AddLabel('lbl_instruction', 'Select the appropriate credit facility for the trade.')
        b.  BeginHorzBox()
        b.    BeginVertBox()
        b.      AddLabel('lbl_party_from_trade_Label', 'Trade Counterparty:', 100)
        b.      AddLabel('lbl_override_with_party_Label', 'ACM Party:', 100)
        b.    EndBox()
        b.    BeginVertBox()
        b.      AddLabel('lbl_party_from_trade_Value', '', 250)
        b.      AddLabel('lbl_override_with_party_Value', '', 250)
        b.        AddButton('btn_change_party', '   Change ACM Party   ', False, True)
        b.      EndBox()
        b.  EndBox()
        b.  BeginHorzBox()
        b.    BeginVertBox('EtchedIn')
        b.      AddList('combo_facility_list', -1, -1, 50, -1)
        b.    EndBox()
        b.    BeginHorzBox('EtchedIn')
        b.      BeginVertBox()
        b.        AddLabel('lbl_FACILITYID', 'Facility Id:')
        b.        AddLabel('lbl_DESCRIPTION', 'Description:')
        b.        AddLabel('lbl_FACILITYACTIVE', 'Active:')
        b.        AddLabel('lbl_STARTDATE', 'Start date:')
        b.        AddLabel('lbl_EXPIRYDATE', 'Expriy date:')
        b.        AddLabel('lbl_FACILITYAMOUNT', 'Facility amount:')
        b.        AddLabel('lbl_FACILITYCURRENCY', 'Facility currency:')
        b.      EndBox()
        b.      AddFill()
        b.      BeginVertBox()
        b.        AddLabel('lbl_FACILITYID_Value', '', 300)
        b.        AddLabel('lbl_DESCRIPTION_Value', '', 300)
        b.        AddLabel('lbl_FACILITYACTIVE_Value', '', 300)
        b.        AddLabel('lbl_STARTDATE_Value', '', 300)
        b.        AddLabel('lbl_EXPIRYDATE_Value', '', 300)
        b.        AddLabel('lbl_FACILITYAMOUNT_Value', '', 300)
        b.        AddLabel('lbl_FACILITYCURRENCY_Value', '', 300)
        b.      EndBox()
        b.    AddFill()
        b.    EndBox()
        b.  EndBox()
        b.  AddSeparator()
        b.  BeginHorzBox()
        b.    AddLabel('lbl_error_message', '', 300)
        b.    AddFill()
        b.    AddButton('ok', 'Continue')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()

        return b

    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        self.dialog.Caption('ACM Facility Selection')

        self._lbl_FACILITYID_value = layout.GetControl('lbl_FACILITYID_Value')
        self._lbl_DESCRIPTION_value = layout.GetControl('lbl_DESCRIPTION_Value')
        self._lbl_FACILITYACTIVE_value = layout.GetControl('lbl_FACILITYACTIVE_Value')
        self._lbl_STARTDATE_value = layout.GetControl('lbl_STARTDATE_Value')
        self._lbl_EXPIRYDATE_value = layout.GetControl('lbl_EXPIRYDATE_Value')
        self._lbl_FACILITYAMOUNT_value = layout.GetControl('lbl_FACILITYAMOUNT_Value')
        self._lbl_FACILITYCURRENCY_value = layout.GetControl('lbl_FACILITYCURRENCY_Value')
        self._lbl_party_from_trade_value = layout.GetControl('lbl_party_from_trade_Value')
        self._lbl_override_with_party_value = layout.GetControl('lbl_override_with_party_Value')

        self._combo_facility_list = layout.GetControl('combo_facility_list')
        self._lbl_error_message = layout.GetControl('lbl_error_message')
        self._btn_change_party = layout.GetControl('btn_change_party')
        
        #Initialise controls 
        self.populate_facility_control()
        self._lbl_party_from_trade_value.SetData(self._trade_counterparty.Name())
        self._lbl_override_with_party_value.SetData(self._facility_counterparty.Name())
        
        #add call back event handlers
        self._combo_facility_list.AddCallback('SelectionChanged', self.on_facility_seletion_change, None)
        self._btn_change_party.AddCallback('Activate', self.on_change_party_click, None)
    
    def populate_facility_control(self):
        self.clear_facility_details()
        self._combo_facility_list.Clear()
        
        key_list = [facility_id for facility_id in self._facility_data.keys()]

        if not key_list:
            key_list.append('NONE')
        self._combo_facility_list.Populate(sorted(key_list))

    def get_error_message_colour(self):
        colour = acm.GetDefaultContext().GetExtension('FColor', acm.FColor, 'Error_Red')
        return colour.Value()

    def clear_facility_details(self):
        self._lbl_FACILITYID_value.SetData('')
        self._lbl_DESCRIPTION_value.SetData('')
        self._lbl_FACILITYACTIVE_value.SetData('')
        self._lbl_STARTDATE_value.SetData('')
        self._lbl_EXPIRYDATE_value.SetData('')
        self._lbl_FACILITYAMOUNT_value.SetData('')
        self._lbl_FACILITYCURRENCY_value.SetData('')
        self._lbl_error_message.SetData('')

    def on_change_party_click(self, cd, data):
        """ Event handler to override the selected counterparty for facility lookup.
        """
        del cd
        del data
        
        new_party = acm.UX().Dialogs().SelectObjectsInsertItems(acm.UX().SessionManager().Shell(), acm.FParty, False)
        if new_party:
            self._facility_counterparty = new_party
            facility_data = ACMWebCallHelpers.get_ACM_credit_facility_data(self._facility_counterparty)
            self._facility_data = facility_data
            self._lbl_override_with_party_value.SetData(self._facility_counterparty.Name())
            self.populate_facility_control()
            self._lbl_override_with_party_value.SetColor('Text', self.get_error_message_colour())

    def on_facility_seletion_change(self, cd, data):
        """ Event handler to display the selected facility details in the details panel
        """
        del cd
        del data

        self.clear_facility_details()
        selected_facility_id = self._combo_facility_list.GetSelectedItem().GetData()
        selected_facility_detail = self._facility_data[selected_facility_id]

        try:
            self._lbl_FACILITYID_value.SetData('{0}'.format(selected_facility_detail['FACILITYID']))
            self._lbl_DESCRIPTION_value.SetData('{0}'.format(selected_facility_detail['FACILITYPRODUCTDESCRIPTION']))
            self._lbl_FACILITYACTIVE_value.SetData('{0}'.format(selected_facility_detail['FACILITYACTIVE']))
            self._lbl_STARTDATE_value.SetData('{0}'.format(selected_facility_detail['STARTDATE']))
            self._lbl_EXPIRYDATE_value.SetData('{0}'.format(selected_facility_detail['EXPIRYDATE']))
            self._lbl_FACILITYAMOUNT_value.SetData('{0}'.format(selected_facility_detail['FACILITYAMOUNT']))
            self._lbl_FACILITYCURRENCY_value.SetData('{0}'.format(selected_facility_detail['FACILITYCURRENCY']))
        except:
            LOGGER.ELOG('ACM Facility Selection: Incomplete data received from ACM. Please contact the ACM support team.')

    def HandleApply(self):
        if self._combo_facility_list.GetSelectedItem():
            return self._combo_facility_list.GetSelectedItem().GetData()
        else:
            self._lbl_error_message.SetData('*Please select a credit facility.')
            self._lbl_error_message.SetColor('Text', self.get_error_message_colour())
            return None


class ACMWebCallHelpers:
    """ Static class to wrap some helper functions to connect and retrieve the facilities 
        data from the ACM system.
    """
    @classmethod
    def initialise_facility_data_dictionary(cls):
        default_data = {
            'Not Applicable': {
                'FACILITYID': 'Not Applicable',
                'FACILITYPRODUCTDESCRIPTION': '',
                'FACILITYACTIVE': '',
                'STARTDATE': '',
                'EXPIRYDATE': '',
                'FACILITYAMOUNT': '',
                'FACILITYCURRENCY': '',
            }
        }    
        return default_data
    
    @classmethod
    def get_no_facilities_returned_data_item(cls):
        return {
                'FACILITYID': ACM_NO_FACILITIES_RETURNED,
                'FACILITYPRODUCTDESCRIPTION': '',
                'FACILITYACTIVE': '',
                'STARTDATE': '',
                'EXPIRYDATE': '',
                'FACILITYAMOUNT': '',
                'FACILITYCURRENCY': '',
            }
        

    @classmethod
    def get_login_from_principal(cls, principal_username, principal_name):
        query = "user='%s' and principal='%s' and type='Custom 1'" % (principal_username, principal_name)
        acm_password_set = acm.FPrincipalUser.Select(query)

        if acm_password_set:
            return acm_password_set[0].Password()
        else:       
            LOGGER.ELOG('ACM Facility Selection: Config error, no principal found.')
            return None
    
    @classmethod
    def get_facility_counterparty_id(cls, trade):
        if trade.Instrument().Issuer():
            return trade.Instrument().Issuer()
        else: 
            return trade.Counterparty()

    @classmethod
    def get_ACM_credit_facility_data(cls, counterparty):
        facility_data = cls.initialise_facility_data_dictionary()
        
        base_url = CONFIG_PARAMS['WebService_Base_URL'].Text()
        username = CONFIG_PARAMS['WebService_Username'].Text()
        
        principal_username = CONFIG_PARAMS['Front_ACM_Principal_User'].Text()
        principal_name = CONFIG_PARAMS['Front_ACM_Principal'].Text()
        password = cls.get_login_from_principal(principal_username, principal_name)

        if counterparty.AdditionalInfo().BarCap_SMS_CP_SDSID():
            full_url = '{0}&counterpartyid={1}'.format(base_url, counterparty.AdditionalInfo().BarCap_SMS_CP_SDSID())
            LOGGER.LOG('ACM Get Facilities URL: %s' % full_url)

            try:
                request_data = requests.get(full_url, auth=(username, password), verify=False)
                data = json.loads(request_data.text)
                
                if data:
                    for facility in data:
                        facility_data[str(facility['FACILITYID'])] = facility
                else:
                    facility_data[ACM_NO_FACILITIES_RETURNED] = cls.get_no_facilities_returned_data_item()
        
            except Exception, ex:
                error_message = 'ACM Facility Selection: Error retrieving credit facility from ACM. Exception: %s' % ex
                LOGGER.ELOG(error_message)
                return ACM_CONNECTION_ERROR
        else:
            error_message = 'ACM Facility Selection: ACM system counterparty Id not specified on the trade Counterparty'
            LOGGER.ELOG(error_message)

        return facility_data


def predeal_acm_credit_facility_check(shell, params):
    """ On trade save entry-point from GValidation
    """
    credit_facility_selection_enabled = CONFIG_PARAMS['Front_Credit_facility_selection_enabled']
    if credit_facility_selection_enabled.Text().lower() == 'false':
        LOGGER.WLOG('ACM Facility Selection: Functionality disabled.')
        return params

    trade_qualifying_query_folder_name = CONFIG_PARAMS['Front_Trade_qualifying_query_folder']
    
    data = params.At('initialData')
    modified_trade = data.At('editObject')
    
    query_folder = acm.FStoredASQLQuery[trade_qualifying_query_folder_name.Text()]
    
    if query_folder:
        if query_folder.Query().IsSatisfiedBy(modified_trade):
            
            facility_counterparty = ACMWebCallHelpers.get_facility_counterparty_id(modified_trade)
            facility_data = ACMWebCallHelpers.get_ACM_credit_facility_data(facility_counterparty)

            if facility_data == ACM_CONNECTION_ERROR:
                message = 'Error connecting to the ACM system. Please notify IT.'
                acm.UX().Dialogs().MessageBox(shell, 'Error', message, 'OK', None, None, 'Button1', 'None', 'ACM Facility Selection')
                modified_trade.AdditionalInfo().PM_ACMFacilityID(ACM_CONNECTION_ERROR)
                return params
            else:
                current_facilicty_id_on_trade = modified_trade.AdditionalInfo().PM_ACMFacilityID()
                
                if current_facilicty_id_on_trade and current_facilicty_id_on_trade != ACM_NO_FACILITIES_RETURNED and current_facilicty_id_on_trade in facility_data:
                    # If facility id already stamped on trade and validated for counterparty, continue
                    # without prompting the trader to select the facility.
                    LOGGER.LOG('ACM Facility Selection: Credit facilty already manually set by trader: %s' % current_facilicty_id_on_trade)
                    return params
                else:
                    dialog = CreditFacilitySelection(facility_data, facility_counterparty, modified_trade.Counterparty())
                    dialog_result = acm.UX().Dialogs().ShowCustomDialogModal(acm.UX().SessionManager().Shell(), dialog.create_layout(), dialog)

                    if dialog_result:
                        LOGGER.LOG('ACM Facility Selection: Selected credit facilty: %s' % dialog_result)
                        modified_trade.AdditionalInfo().PM_ACMFacilityID(dialog_result)
                        return params
                    else:
                        return None
        else:
            LOGGER.LOG('ACM Facility Selection: Trade does not qualify, skip facility selection.')
    else:
        LOGGER.ELOG('ACM Facility Selection: Query folder does not exist.')
    
    return params
