
import acm
import FUxCore
import string
import xml.etree.ElementTree as ET

try:
    import FTradeSheetColumnCustom
except Exception as e:
    pass

def get_business_process_from_trade(obj, state_chart=None):
    #This will only for trade sheet which returns FTradeRow
    if obj.IsKindOf(acm.FTradeRow):
        trade = obj.Trade()
    else:
        trade = obj
    bpr = None
    if trade:
        bprs = acm.BusinessProcess.FindBySubjectAndStateChart(trade, state_chart)
        if bprs:
            bpr = bprs.First()
    return bpr

def get_state_chart_set_on_column(col):
    return col.Creator().Configuration().ParamDict().At('columnParameters').At('StateChart').Name()

def get_acm_version():
    """ Get the acm version"""
    return float(".".join(acm.ShortVersion().strip(string.ascii_letters) \
                          .split(".")[0:2]))

class ShowBPRMenuItem(FUxCore.MenuItem):
    """This menu item is for viewing the business process linked to trade object"""
    def __init__(self, extObj):
        self._extObj = extObj

    def Enabled(self):
        return True

    def Applicable(self):
        try:
            self.active_sheet = self._extObj.ActiveSheet()
            acm_object = None
            for cell in self.active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    acm_object = cell.RowObject()
                    break
            if acm_object.IsKindOf(acm.FTradeRow):
                trade = acm_object.Trade()
            else:
                trade = acm_object
            bprs = acm.BusinessProcess.FindBySubjectAndStateChart(trade, None)
            if bprs:
                return True
        except Exception as e:
            #print "Exception occurred in ShowBPRMenuItem.Applicable:  : %s"%str(e)
            pass
        return False

    def Invoke(self, _eii):
        self._show_bpr()

    def _show_bpr(self):
        try:
            for cell in self.active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    acm_object = cell.RowObject()
                    bpr = get_business_process_from_trade(acm_object)
                    if bpr:
                        acm.StartApplication("Business Process Details", bpr)
        except Exception as e:
            print(("Exception occurred in ShowBPRMenuItem._show_bpr : %s"%str(e)))

class ShowBPRFromColumnMenuItem(FUxCore.MenuItem):
    """This menu item is for viewing the business process linked to trade object from parameterized column"""
    def __init__(self, extObj):
        self._extObj = extObj


    def Enabled(self):
        return True

    def Applicable(self):
        try:
            self.active_sheet = self._extObj.ActiveSheet()
            if get_acm_version() >= 2017.4:
                acm_object = None
                for cell in self.active_sheet.Selection().SelectedCells():
                    acm_object = cell.RowObject()
                    break
                if acm_object.IsKindOf(acm.FTradeRow):
                    trade = acm_object.Trade()
                else:
                    trade = acm_object
                bprs = acm.BusinessProcess.FindBySubjectAndStateChart(trade, None)
                if bprs:
                    return True
        except Exception as e:
            #print "Exception occurred in ShowBPRFromColumnMenuItem.Applicable:  : %s"%str(e)
            pass
        return False

    def Invoke(self, _eii):
        self._show_bpr()

    def _show_bpr(self):
        try:
            for cell in self.active_sheet.Selection().SelectedCells():
                acm_object = cell.RowObject()
                bpr = get_business_process_from_trade(acm_object)
                if bpr:
                    acm.StartApplication("Business Process Details", bpr)
        except Exception as e:
            #print("Exception occurred in ShowBPRFromColumnMenuItem._show_bpr : %s"%str(e))
            pass



class ShowPublishMenuItem(FUxCore.MenuItem):
    """This menu item is for viewing the Publish event on trade object"""
    def __init__(self, extObj):
        self._extObj = extObj
        self.bpr = None

    def Enabled(self):
        if self.bpr and self.bpr.CanHandleEvent('report'):
            return True
        else:
            return False

    def Applicable(self):
        try:
            self.active_sheet = self._extObj.ActiveSheet()
            for cell in self.active_sheet.Selection().SelectedCells():
                if cell.IsHeaderCell():
                    acm_object = cell.RowObject()
                    #fire 'Report' event if it can handle
                    state_chart_name = get_trads_state_chart_name()
                    state_chart = acm.FStateChart[state_chart_name]
                    bpr = get_business_process_from_trade(acm_object, state_chart)
                    if bpr:
                        self.bpr = bpr
                        return True
        except Exception as e:
            #print "Exception occurred in _publish : %s"%str(e)
            pass
        return False

    def Invoke(self, _eii):
        self._publish()

    def _publish(self):
        try:
            if self.bpr and self.bpr.CanHandleEvent('report'):
                self.bpr.HandleEvent('report', None, None)
                self.bpr.Commit()
        except Exception as e:
            print(("Exception occurred in _publish : %s"%str(e)))


def create_show_bpr_menuitemtrade(eii):
    return ShowBPRMenuItem(eii)

def create_show_publish_menuitemtrade(eii):
    return ShowPublishMenuItem(eii)

def create_show_bpr_from_column_menuitemtrade(eii):
    return ShowBPRFromColumnMenuItem(eii)

def WasPublished(trade):
    '''Traverses the related busienss process steps to check if business process has ever been
       in Published state, if it has then returns True.'''
    try:
        if trade:
            bpr_for_trade = get_business_process_from_trade(trade)
            if bpr_for_trade:
                if 'Published' in [v_state.Name() for v_state in bpr_for_trade.VisitedStates()]:
                    return True
    except Exception as e:
        pass
        #print 'Exception in WasPublished : %s '%str(e)
    return False

def get_param_value_from(param_name, bpr, bpr_step):
    entry = bpr.Diary().GetEntry(bpr, bpr_step)
    params = entry.Parameters()
    return params.At(param_name, "")

'''def set_parameter_to_current_step(param_name, data_dict, business_process):
    if business_process:
        try:
            business_process_clone = business_process.Clone()
            current_step = business_process_clone.CurrentStep()
            current_entry = current_step.DiaryEntry()
            current_entry.Parameters().AtPut(param_name, data_dict)
            current_entry.Commit()
            business_process_clone.Diary().PutEntry(business_process, business_process.CurrentStep(), current_entry)
            business_process.Apply(business_process_clone)
            business_process.Commit()
        except Exception, e:
            print 'Exception in setting parameter <%s : %s> to BusinessProcess <%s>'%(param_name, data_dict, business_process.Oid())

def set_param_value(param_name, data_dict, business_process, business_process_step):
    if business_process and business_process_step:
        try:
            business_process_clone = business_process.Clone()
            current_step = business_process_step
            current_entry = current_step.DiaryEntry()
            current_entry.Parameters().AtPut(param_name, data_dict)
            current_entry.Commit()
            business_process_clone.Diary().PutEntry(business_process, business_process.CurrentStep(), current_entry)
            business_process.Apply(business_process_clone)
            business_process.Commit()
        except Exception, e:
            print 'Exception in setting parameter <%s : %s> to BusinessProcess <%s> on BusinessProcess step <%s>'%(param_name, data_dict, business_process.Oid(), business_process_step.EventName())'''



def get_fix_param_value(fix_param, trade_obj):
    try:
        val = []
        bpr = get_business_process_from_trade(trade_obj)
        fix_msg_as_xml = get_param_value_from('FIXMSG', bpr, bpr.CurrentStep())
        dom_obj = ET.fromstring(fix_msg_as_xml)
        for each_field in dom_obj.iter('field'):
            if each_field.attrib.get('name', None) == fix_param:
                CustomMethod = 'get_' + str(fix_param) + '_string_from_value'
                if hasattr(FTradeSheetColumnCustom, CustomMethod):
                    func = getattr(FTradeSheetColumnCustom, CustomMethod)
                    val.append(func(each_field.text))
                else:
                    val.append(each_field.text)

    except Exception as e:
        #print e
        pass
    if len(val) > 1:
        return val
    elif len(val) == 1:
        return val[0]
    elif not val:
        return ''
    return ''



def get_status_text_value(trade_obj):
    try:
        bpr = get_business_process_from_trade(trade_obj)
        status_text = get_param_value_from('StatusText', bpr, bpr.CurrentStep())
        return status_text
    except Exception as e:
        #print e
        pass
    return ''

def get_operation_name_from_bpr_context(bpr_context):
    """ Get operation name from bpr context"""
    operation_name = ''
    if bpr_context:
        event_name = bpr_context.Event().Name()
        sc_name = bpr_context.CurrentState().StateChart().Name()
        operation_name = 'BPR_' + sc_name + '_' + event_name
    return operation_name
# ------------------------------------------------------------------------------

def get_operation_component_type():
    """ Get Operation component type"""
    componentTypes = acm.FEnumeration['enum(ComponentType)']
    return componentTypes.Enumeration('Operation')

def user_has_operation_permission(user, operation):
    """ Returns True if user has permission else False"""
    return user.IsAllowed(operation, get_operation_component_type())

def operation_exists(operation):
    """ Returns true if given operation exists else False"""
    is_operation_exist = True
    compType = 'Operation'
    queryString = 'name=\'%s\' and type=\'%s\'' % (operation, compType)
    op = acm.FComponent.Select01(queryString, '')
    if op == None:
        is_operation_exist = False
    return is_operation_exist

def has_user_rights(operationName):
    """ Check if the calling user has the permission to perform operation"""
    has_right = True
    if operation_exists(operationName):
        if not user_has_operation_permission(acm.User(), operationName):
            has_right = False
    return has_right

def get_trads_state_chart_name():
    try:
        fparam = 'TRADSStateChart'
        state_chart_extension = 'TRADSStateChartName'
        ext_context = acm.FExtensionContext[acm.GetDefaultContext().Name()]
        param_object = ext_context.GetExtension('FParameters',
                                                'FObject', fparam)
        if param_object:
            return str(param_object.Value().At(state_chart_extension))
    except Exception:
        return None

def set_owner(acm_object, acm_owner, doCommit = True):
    if acm_object and acm_object.Owner() != acm_owner:
        # print 'The owner is being updated from <%s> to <%s>'%(acm_object.Owner().Name(), acm_owner.Name())
        acm_object.Owner = acm_owner
        if doCommit:
            acm_object.Commit()

def update_business_process_owner(business_process, owner = '', doCommit = True):
    """Updates BusinessProcess and its diary owner with the owner of its Subject or with the user provided owner
    Input :
        ACM FBusinessProcess object
        Name of owner - If provided the Business and diary owner will get set to this value
        doCommit - Default is True. Set/Pass it as False only when API is being called from BusinessProcess callbacks.
            When set as True, the API will perform commit transaction on BusinessProcess object.
            When set as False, the API will just set the owner to BusinessProcess object and will not commit it.
    """
    bpr_subject = None
    try:
        if business_process and business_process.IsKindOf('FBusinessProcess'):
            bpr_subject = business_process.Subject()
    except:
        print('Invalid Input. Provide valid ACM BusinessProcess object')
        return

    bpr_diary = business_process.Diary()
    convert_owner = None
    if owner:
        try:
            convert_owner = acm.FUser[owner]
            if not convert_owner:
                print('Invalid owner. Provide valid ACM FUser name')
                return
        except:
            print('Invalid owner. Provide valid ACM FUser name')
            return
    elif bpr_subject:
        if bpr_subject.RecordType() == 'ReconciliationItem':
            convert_owner = bpr_subject.Subject().Owner()  # Subject of ReconciliationItem
        else:
            convert_owner = bpr_subject.Owner()  # Subject of BusinessProcess

    try:
        if convert_owner:
            set_owner(bpr_diary, convert_owner, doCommit)
            set_owner(business_process, convert_owner, doCommit)
    except Exception as e:
        print(('Error while setting BusinessProcess Owner : %s'%str(e)))


