"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Helper functions and classes used in the solution.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
"""
import datetime

import acm

from at_addInfo import save
from statements_params import STATE_CHART


def first_day_of_month(acm_date):
    return acm.Time.FirstDayOfMonth(acm_date)


def last_day_of_month(acm_date):
    first_of_month = first_day_of_month(acm_date)
    first_of_next_month = acm.Time.DateAddDelta(first_of_month, 0, 1, 0)
    return acm.Time.DateAddDelta(first_of_next_month, 0, 0, -1)


def first_day_of_week(acm_date):
    return acm.Time.FirstDayOfWeek(acm_date)


def last_day_of_week(acm_date):
    first_of_week = first_day_of_week(acm_date)
    return acm.Time.DateAddDelta(first_of_week, 0, 0, 6)


def date_to_dt(acm_date, hour=0, minute=0, second=0):
    return datetime.datetime(*acm.Time.DateToYMD(acm_date), 
                             hour=hour, minute=minute, second=second)


def format_date(acm_date, pattern):
    dt_date = date_to_dt(acm_date)
    return dt_date.strftime(pattern)


def float_to_percent(input):
    if not input:
        return 0.0
    return 100 * float(input)


def float_ignore_none(input):
    if not input:
        return 0.0
    return float(input)


def int_allow_blank(input):
    if input == '':
        return ''
    return int(input)


def get_param_value(ext_name, param_name):
    ext_obj = acm.GetDefaultContext().GetExtension(acm.FParameters, 
                                                   acm.FObject, ext_name)
    if not ext_obj:
        raise RuntimeError('FParameters extension "%s" not found.' % ext_name)
    params = ext_obj.Value()
    value = params.At(param_name)
    if value is None:
        raise RuntimeError('Parameter "%s" not found in FParameters "%s".'
                           % (param_name, ext_name))
    return str(value)


def get_steps(bp, state_name):
    return [step for step in bp.Steps() if step.State().Name() == state_name]


def get_first_step(bp, state_name):
    steps = get_steps(bp, state_name)
    if not steps:
        return None
    return sorted(steps, key=lambda x: x.CreateTime())[0]


def get_last_step(bp, state_name):
    steps = get_steps(bp, state_name)
    if not steps:
        return None
    return sorted(steps, key=lambda x: x.CreateTime())[-1]


def can_user_force(bp, state_name):
    if bp.CurrentStep().State().Name() == state_name:    
        error_msg = 'Not possible, business process is already in "%s".' % state_name
        return False, error_msg
    error_msg = 'User not allowed to force to "%s".' % state_name
    if state_name == 'Pending Calculation':
        return True, ''
    elif state_name == 'Pending Send':
        if get_last_step(bp, 'Sent'):
            return True, ''
        error_msg = "Not possible, documents haven't been sent yet."
    return False, error_msg


class StatementConfig(object):
    
    def __init__(self, process_class, event, ins_type, trade_query, 
                 product=None, additional_trade_query='', 
                 state_chart=STATE_CHART, period=None, always_new_bp=False):
        self.process_class = process_class
        self.event = event
        self.ins_type = ins_type
        self.product = product
        self.trade_query = trade_query
        self.additional_trade_query = additional_trade_query
        self.state_chart = state_chart
        self.period = period
        self.always_new_bp = always_new_bp
    
    def _matches_contact_rule(self, rule):
        return (rule.EventChlItem() and rule.EventChlItem().Name() == self.event
                and ((self.product and rule.ProductTypeChlItem().Name() == self.product) 
                     or (rule.ProductTypeChlItem() == self.product)) 
                and rule.InsType() == self.ins_type)
    
    def _matches_contact(self, contact):
        for rule in contact.ContactRules():
            if self._matches_contact_rule(rule):
                return True
        return False
    
    def _get_period_start(self, acm_date):
        if self.period == 'Month':
            return first_day_of_month(acm_date)
        if self.period == 'Week':
            return first_day_of_week(acm_date)
        return acm_date
    
    def _get_period_end(self, acm_date):
        if self.period == 'Month':
            return last_day_of_month(acm_date)
        if self.period == 'Week':
            return last_day_of_week(acm_date)
        return acm_date
    
    def _matches_bp(self, bp):
        if not bp.StateChart() == self.state_chart:
            return False
        if not bp.AdditionalInfo().BP_Event() == self.event:
            return False
        if not bp.AdditionalInfo().BP_InsType() == self.ins_type:
            return False
        if not bp.AdditionalInfo().BP_ProductType() == self.product:
            return False
        return True
    
    def matches(self, entity):
        if entity.IsKindOf(acm.FBusinessProcess):
            return self._matches_bp(entity)
        if entity.IsKindOf(acm.FContact):
            return self._matches_contact(entity)
        if entity.IsKindOf(acm.FContactRule):
            return self._matches_contact_rule(entity)
        return False
    
    def create_bp(self, contact, val_date, **kwargs):
        party = contact.Party()
        acm.BeginTransaction()
        try:
            bp = acm.BusinessProcess.InitializeProcess(party, self.state_chart)
            bp.RegisterInStorage()
            bp.Commit()
            save(bp, 'BP_Event', self.event)
            if self.ins_type:
                save(bp, 'BP_InsType', self.ins_type)
            if self.product:
                save(bp, 'BP_ProductType', self.product)
            save(bp, 'BP_ValuationDate', val_date)
            save(bp, 'BP_ExternalId', str(contact.Oid()))
            if 'start_date' in kwargs:
                save(bp, 'BP_FromDate', kwargs['start_date'])
            if 'end_date' in kwargs:
                save(bp, 'BP_ToDate', kwargs['end_date'])
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            raise
        return bp 
    
    def find_bps(self, contact, val_date):
        party = contact.Party()
        query = acm.CreateFASQLQuery('FBusinessProcess', 'AND')
        query.AddAttrNode('StateChart.Name', 'EQUAL', 
                          self.state_chart.Name())
        query.AddAttrNode('Subject_seqnbr', 'EQUAL', party.Oid())
        query.AddAttrNode('AdditionalInfo.BP_Event', 'EQUAL', self.event)
        query.AddAttrNode('AdditionalInfo.BP_InsType', 'EQUAL', self.ins_type)
        query.AddAttrNode('AdditionalInfo.BP_ProductType', 'EQUAL', self.product)
        if self.period in ('Month', 'Week'):
            period_start = self._get_period_start(val_date)
            period_end = self._get_period_end(val_date)
            query.AddAttrNode('AdditionalInfo.BP_ValuationDate', 'GREATER_EQUAL', period_start)
            query.AddAttrNode('AdditionalInfo.BP_ValuationDate', 'LESS_EQUAL', period_end)
        else:
            query.AddAttrNode('AdditionalInfo.BP_ValuationDate', 'EQUAL', val_date)
        query.AddAttrNode('AdditionalInfo.BP_ExternalId', 'EQUAL', str(contact.Oid()))
        bps = query.Select()
        return bps
    
    def find_contact_rules(self, frequency=''):
        query = 'eventChlItem="%s"' % self.event
        if self.ins_type:
            query += ' and insType="%s"' % self.ins_type
        if self.product:
            query += ' and productTypeChlItem="%s"' % self.product
        contact_rules = list(acm.FContactRule.Select(query))
        if not frequency:
            return contact_rules
        return [rule for rule in contact_rules 
                if rule.Contact().AdditionalInfo().Comm_Freq() 
                and frequency in rule.Contact().AdditionalInfo().Comm_Freq()]
    
    def init_process(self, bp):
        return self.process_class(bp, self)
    
    def is_bp_valid(self, bp):
        return self.process_class.is_valid(bp)
    
