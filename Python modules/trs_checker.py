'''
:Author: Andreas Bayer <Andreas.Bayer@absacapital.com; Andreas.Bayer@d-fine.de>
:Version: 0.1, 2014-03-04
:Summary: Functionality for finding missing or wrong TRS fixings

History
=======
2014-03-04 Andreas Bayer, created
2014-04-01 Andreas Bayer, discussed with Irfaan Karim and amended script accordingly
'''

import acm
import at_time
import math
import csv
import traceback
import sys
import FLogger
import os.path
from at_time import acm_date
from string import Template
from trs_checker_config import email_template, table_row_template, table_template

ael_gui_parameters = {
    'windowCaption' : 'Check Total Return Swaps'
}
                      
ael_variables = [
    ['mode', 'Query Mode', 'string', ['missing dividends', 
                                      'missing dividend scalings',
                                      'missing fixings',
                                      'wrong nominal scalings',
                                      'wrong initial price fixings',
                                      'all error types'], 'missing fixings', 1],
    ['trades', 'Trades Selection', 'FTrade', None, None, 0, 1, 'Global One trade selection.', None, 1],
    ['include', 'Include Instruments', 'string', ['include all instruments',
                                                  'include all positions'], 'include all positions', 1],
    ['show_expired', 'Show Expired', 'int', [0, 1], 0, 1],
    ['output_mode', 'Output Mode', 'string', ['To Console',
                                              'To File',
                                              'email'], 'email', 1],
    ['recipient', 'Recipient', 'string', None, '', 0],
    ['output_file', 'Output File', 'string', None, 1, 0],
    ['log_directory', 'Log Directory', 'string', None, '', 1, 0],
    ['log_level', 'Log Level', 'string', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], 'INFO', 1, 0]
]

LOGGER = None
LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':3, 'ERROR':4}

class Incidents(list):
    '''A special list that can put it's contents into an xhtml template and send it 
    out as mail'''
    
    def __init__(self, params):
        super(Incidents, self).__init__()
        self.params = params
        self.__registered_checkers = set()
    
    def register_checker(self, checker):
        '''Register a checker class.'''
        if issubclass(checker, ResetChecker):
            self.__registered_checkers.add(checker)
    
    def write_to_console(self):
        '''Only for debugging purposes'''
        for incident in self:
            print incident
    
    def _get_incident_dict(self):
        res = {}
        for checker_class in self.__registered_checkers:
            res[checker_class.__name__] = []
        
        for incident in self:
            res[incident['checker_class'].__name__].append(incident)
        return res
    
    def _get_mail_string(self):
        '''fills an html mail template with its contents
        TODO: split logic into several functions to improve overview.'''
        
        incident_classification = self._get_incident_dict()
        
        tables_string = []
        for incident_class in self.__registered_checkers:
            table_template_obj=Template(table_template)
            #construct html table showing the trs problems in the Incidents list
            table_rows=[]
            #used for switching the css classes in subsequent table rows
            odd_even = 0
            for incident in incident_classification[incident_class.__name__]:
                row_template=Template(table_row_template)
                
                if odd_even:
                    css_class = 'evenrow'
                else:
                    css_class = 'oddrow'
                    
                row = row_template.safe_substitute({
                        'instrument': incident['instrument'],
                        'leg_type': incident['leg_type'],
                        'cash_flow_type': incident['cash_flow_type'],
                        'reset_type': incident['reset_type'],
                        'issue_description': incident['incident_type'],
                        'rowclass': css_class
                })
                table_rows.append(row)
                
                odd_even = (odd_even+1) %2
            
            #print incident_class.error_type, type(incident_class.error_type)
            #print table_rows, type(table_rows)
            table = table_template_obj.safe_substitute({
                'table_rows': ''.join(table_rows),
                'issue_type': incident_class.error_type
            })
            tables_string.append(table)
        #fill the rest of the mail template
        mail = Template(email_template)
        mail = mail.safe_substitute({
                    'tables': ''.join(tables_string),
               })
        return mail
        
    def __iadd__(self, other):
        '''Incidents += Incidents should give another Incidents object, not a list'''
        if type(other) == Incidents:
            for elem in other:
                self.append(elem)
            return self
        else:
            super(Incidents, self).__iadd__(other)
    
    def write_to_file(self):
        email_html = self._get_mail_string()
        try:
            with open(self.params['output_file'], 'w') as f:
                f.write(email_html)
        except Exception, e:
            LOGGER.ELOG('Error when opening file %s. Traceback: %s' % (
                self.params['output_file'], repr(traceback.extract_stack())))
        
    def send_as_email(self):
        '''Send incidents as email. Uses COM for Windows. Mainly used for
        debugging on local machine, for backend usage, use file mode and ask RTB to send 
        the html output as body of an email. Removed previously contained mailx call for unix.
        COM is used to reduce any security warnings, that can occur, when using pythons
        Smtp and emailing modules.'''
        
        email_html = self._get_mail_string()
        email_subject = 'Test TRS Checker: %s' % (self.params['mode'])
        #try to send message via outlook com object 
        try:
            if sys.platform == 'win32':
                import win32com.client as win32
                outlook = win32.Dispatch('outlook.application')
                mail = outlook.CreateItem(0)
                mail.To = self.params['recipient']
                mail.Subject = email_subject
                mail.BodyFormat = 3
                mail.HTMLBody  = email_html
                if self.params['output_file']:
                    try:
                        olMSG = 2
                        mail.saveAs(self.params['output_file'], olMSG)
                    except Exception, e:
                        LOGGER.ELOG('Error: Email could not be saved.')
                        
                mail.send
                LOGGER.LOG('Mail has been successfully sent via outlook com object.')
                return
        except Exception, e:
            LOGGER.ELOG('Error: Message could not be send via outlook com object. Traceback: %s' % (
                            repr(traceback.extract_stack())))
        
        try:
            if self.params['output_file']:
                write_to_file()
                LOGGER.LOG('Mail has been saved in %s' % self.params['output_file'])
            else:
                LOGGER.LOG('No output file specified.')
            return
        except Exception, e:
            LOGGER.ELOG('Error: Message could not be created. Traceback: %s' % (
                            repr(traceback.extract_stack())))
            
class ResetChecker(object):
    '''Abstract super class for all reset checker types. Defines interface and
    a bunch of methods, used by different reset checker types.'''
    
    REPORT_COLUMNS = {
        'instrument': 'Instrument Name', 
        'leg': 'Leg Number', 
        'leg_type': 'Leg Type', 
        'cash_flow': 'Cash Flow Number', 
        'cash_flow_type': 'Cash Flow Type',
        'cash_flow_start_date': 'Cash Flow Start Date', 
        'cash_flow_end_date': 'Cash Flow End Date', 
        'cash_flow_pay_day': 'Cash Flow Pay Day',
        'reset': 'Reset Number',
        'reset_type': 'Reset Type',
        'reset_start_date': 'Reset Start Date',
        'reset_end_date': 'Reset End Date',
        'reset_day': 'Reset Day',
        'incident_type': 'Error Type'
    }
    
    def __init__(self, instr, params, *args, **kwargs):
        self.instrument = instr
        self.params = params
        #Format of an incident entry in the incident list:
        # {
        # 'instrument': ,
        # 'leg': ,
        # 'leg_type': ,
        # 'cash_flow': ,
        # 'cash_flow_type':
        # 'cash_flow_start_date': ,
        # 'cash_flow_end_date': ,
        # 'cash_flow_pay_day': ,
        # 'reset_type': ,
        # 'reset_start_date': ,
        # 'reset_end_date': ,
        # 'reset_day':,
        # 'incident_type'
        #}
        self._incidents = Incidents(self.params)
        self.valid_trades = self._get_valid_trades()
        
        has_valid_trades = (self.valid_trades.Size() > 0)
        if self._is_expired() and not bool(params['show_expired']):
            raise NotInSearchScopeException('TRS %s is expired.' % self.instrument.Name())
        if not has_valid_trades and params['include'] == 'include all positions':
            raise NotInSearchScopeException('TRS %s has no positions.' % self.instrument.Name())
    
    def check(self, *args, **kwargs):
        '''Abstract method, needs to be implemented by all concrete reset checkers'''
        raise NotImplementedError()
    
    def get_incidents(self):
        return self._incidents
    
    def stamp_incidents(self):
        for incident in self._incidents:
            incident['checker_class'] = self.__class__
            
    def _is_expired(self):
        tr_leg = self._get_total_return_leg()
        if tr_leg == None:
            raise InvalidInstrumentException('TRS %s has no total return leg.' % self.instrument.Name())
        if at_time.to_datetime(tr_leg.EndDate()) >= at_time.to_datetime(acm.Time().DateToday()):
            return False
        else:
            return True
    
    def _get_dividends(self, instrument):
        dividends = acm.FList()
        if instrument.Class().IsSubtype(acm.FCombination):
            for comb_map in acm.FCombInstrMap.Select('combination=%s'%instrument.Oid()):
                instr = comb_map.Instrument()
                dividends.AddAll(self._get_dividends(instr))
        else:
            dividends.AddAll(instrument.Dividends())
        return dividends    
        
    def _get_valid_trades(self):
        fasql_query = acm.CreateFASQLQuery(acm.FTrade, "AND")
        fasql_query.AddAttrNodeString('Instrument.Name', self.instrument.Name(), 'EQUAL')
        fasql_query.AddAttrNodeString('Status', 'Simulated', 'NOT_EQUAL')
        fasql_query.AddAttrNodeString('Status', 'Void', 'NOT_EQUAL')
        return fasql_query.Select()
        
    def _get_total_return_leg(self):
        tr_leg = None
        legs = self.instrument.Legs()
        for leg in legs:
            if leg.LegType() == 'Total Return':
                tr_leg = leg
        return tr_leg
    
    def _get_funding_leg(self):
        '''funding_leg = None
        legs = self.instrument.Legs()
        for leg in legs:
            if leg.LegType() in ['Float', 'Fixed']:
                funding_leg = leg'''
        return self.instrument.TotalReturnFundingLeg()
    
    def _get_legs_of_type(self, leg_type):
        legs_of_type = []
        legs = self.instrument.Legs()
        for leg in legs:
            if leg.LegType == leg_type:
                legs_of_type.append()
        return legs_of_type
    
    def _get_dividend_cashflows(self):
        dividend_cfs = []
        legs = self.instrument.Legs()
        for leg in legs:
            cfs = leg.CashFlows()
            for cf in cfs:
                if cf.CashFlowType() == 'Dividend':
                    dividend_cfs.append(cf)
        return dividend_cfs
    
    def _get_dividends_comparator(self):
        def dividends_comparator(dividend1, dividend2):
            if at_time.to_datetime(dividend1.ExDivDay()) < at_time.to_datetime(dividend2.ExDivDay()):
                return -1
            elif at_time.to_datetime(dividend1.ExDivDay()) > at_time.to_datetime(dividend2.ExDivDay()):
                return 1
            else:
                return 0
        return dividends_comparator
    
    def _get_cash_flow_comparator(self):
        def cash_flow_comparator(cf1, cf2):
            if at_time.to_datetime(cf1.EndDate()) < at_time.to_datetime(cf2.EndDate()):
                return -1
            elif at_time.to_datetime(cf1.EndDate()) > at_time.to_datetime(cf2.EndDate()):
                return 1
            else:
                return 0
        return cash_flow_comparator
    
    def _get_reset_comparator(self):
        def reset_comparator(reset1, reset2):
            if at_time.to_datetime(reset1.Day()) < at_time.to_datetime(reset2.Day()):
                return -1
            elif at_time.to_datetime(reset1.Day()) < at_time.to_datetime(reset2.Day()):
                return 1
            else:
                return 0
        return reset_comparator
    
    def _get_current_cf(self):
        tr_leg = self._get_total_return_leg()
        cash_flows = sorted(tr_leg.CashFlows(), cmp=self._get_cash_flow_comparator())
        current_cash_flow = None
        for cf in cash_flows:
            if at_time.to_datetime(cf.EndDate()) > at_time.to_datetime(acm.Time().DateToday()):
                current_cash_flow = cf
                break
        return current_cash_flow
                
    def _get_relevant_dividends(self):
        '''returns all dividends that fall in the current and future cash flow periods'''
        tr_leg = self._get_total_return_leg()
        dividends = self._get_dividends(tr_leg.FloatRateReference())
        dividends = sorted(dividends, cmp=self._get_dividends_comparator(), reverse=True)
        relevant = []
        current_cash_flow = self._get_current_cf()
        if current_cash_flow:
            min_date = current_cash_flow.StartDate()
            for dividend in dividends:
                if ( (at_time.to_datetime(dividend.ExDivDay()) > at_time.to_datetime(tr_leg.StartDate())) and
                     (at_time.to_datetime(dividend.ExDivDay()) >= at_time.to_datetime(min_date)) and
                     (at_time.to_datetime(dividend.ExDivDay()) <= at_time.to_datetime(tr_leg.EndDate()))):
                    relevant.append(dividend)
                elif (at_time.to_datetime(dividend.ExDivDay()) < at_time.to_datetime(tr_leg.StartDate())):
                    break
        return relevant
        
    def _has_reset_of_type(self, cf, reset_type):
        has_resets = False
        for reset in self._get_resets_of_type(cf, reset_type):
            if reset.ResetType() == reset_type:
                has_resets = True
                break
        return has_resets
    
    def _get_resets_of_type(self, cash_flow, reset_type):
        resets = acm.FReset.Select('cashFlow=%s resetType="%s"' % (cash_flow.Oid(), reset_type))
        return resets
    
    def _has_unfixed_resets(self, cash_flow, reset_type):
        has_unfixed_resets = False
        for reset in self._get_resets_of_type(cash_flow, reset_type):
            if reset.FixingValue() == 0.0 or reset.FixingValue == -1.0:
                has_unfixed_resets = True
                break
        return has_unfixed_resets
    
    def _get_unfixed_resets(self, cash_flow, reset_type):
        unfixed_resets = []
        for reset in self._get_resets_of_type(cash_flow, reset_type):
            if reset.FixingValue() == 0.0 or reset.FixingValue == -1.0:
                unfixed_resets.append(reset)
        return unfixed_resets

class DividendScalingChecker(ResetChecker):
    '''Looks for missing dividend scalings'''
    
    error_type = 'missing dividend scalings'
    
    def __init__(self, instr, params):
        super(DividendScalingChecker, self).__init__(instr, params)
        
    def _has_dividend_scalings(self):
        '''returns if dividend scalings are generated for a certain total
        return swap instrument'''
        
        has_dividend_scalings = False
        tr_leg = self._get_total_return_leg()
        if not tr_leg:
            LOGGER.ELOG('%s has no total return leg.' % self.instrument.Name())
            return False
        if (tr_leg.FloatRateReference() and 
            tr_leg.IndexRef() and
            tr_leg.FloatRateReference().Name() != tr_leg.IndexRef().Name() and 
            tr_leg.NominalScaling() in ['Price', 'Initial Price', 'None']):
            has_dividend_scalings = True
        elif (tr_leg.FloatRateReference() and
              tr_leg.IndexRef() and
              tr_leg.FloatRateReference().Name() == tr_leg.IndexRef().Name() and 
              tr_leg.NominalScaling() in ['Initial Price', 'None']):
            has_dividend_scalings = True
        return has_dividend_scalings

    def check(self, *args, **kwargs):
        dividend_cfs = self._get_dividend_cashflows()
        if self._has_dividend_scalings():
            for cf in dividend_cfs:
                if self._has_unfixed_resets(cf, 'Dividend Scaling'):
                    unfixed_resets = self._get_unfixed_resets(cf, 'Dividend Scaling')
                    for reset in unfixed_resets:
                        self._incidents.append({
                            'instrument': self.instrument.Name(),
                            'leg': cf.Leg().Oid(),
                            'leg_type': cf.Leg().LegType(),
                            'cash_flow': cf.Oid(),
                            'cash_flow_type': cf.CashFlowType(),
                            'cash_flow_start_date': cf.StartDate(),
                            'cash_flow_end_date': cf.EndDate(),
                            'cash_flow_pay_day': cf.PayDate(),
                            'reset': reset.Oid(),
                            'reset_type': reset.ResetType(),
                            'reset_start_date': reset.StartDate(),
                            'reset_end_date': reset.EndDate(),
                            'reset_day': reset.Day(),
                            'incident_type': 'Missing Dividend Scaling Fixing'
                        })
                        
                elif not self._has_reset_of_type(cf, 'Dividend Scaling'):
                    self._incidents.append({
                        'instrument': self.instrument.Name(),
                        'leg': cf.Leg().Oid(),
                        'leg_type': cf.Leg().LegType(),
                        'cash_flow': cf.Oid(),
                        'cash_flow_type': cf.CashFlowType(),
                        'cash_flow_start_date': cf.StartDate(),
                        'cash_flow_end_date': cf.EndDate(),
                        'cash_flow_pay_day': cf.PayDate(),
                        'reset': 'N/A',
                        'reset_type': 'N/A',
                        'reset_start_date': 'N/A',
                        'reset_end_date': 'N/A',
                        'reset_day': 'N/A',
                        'incident_type': 'Missing Dividend Scaling Reset'
                    })

class MissingDividendsChecker(ResetChecker):
    '''Finds missing dividend cashflows. Only looks for dividends during the current
    current and future cash flows, since older cash flows could regularly pop up as errors, 
    e.g. when only the equity index weightings of an equity index changed, which would be not
    an error. Such entries should disappear when entering the next cash flow period to keep the
    error report as clean as possible.'''
    
    error_type = 'missing dividend cash flows'
    
    def __init__(self, instr, params):
        super(MissingDividendsChecker, self).__init__(instr, params)
    
    def _get_pay_day_comparator(self):
        def pay_day_comparator(obj1, obj2):
            if at_time.to_datetime(obj1.PayDay()) < at_time.to_datetime(obj2.PayDay()):
                return -1
            if at_time.to_datetime(obj1.PayDay()) > at_time.to_datetime(obj2.PayDay()):
                return 1
            else:
                return 0
                
        return pay_day_comparator
        
    def _get_pay_date_comparator(self):
        def pay_date_comparator(obj1, obj2):
            if at_time.to_datetime(obj1.PayDate()) < at_time.to_datetime(obj2.PayDate()):
                return -1
            if at_time.to_datetime(obj1.PayDate()) > at_time.to_datetime(obj2.PayDate()):
                return 1
            else:
                return 0
                
        return pay_date_comparator
        
    def check(self, *args, **kwargs):
        dividends = self._get_relevant_dividends()
        tr_leg = self._get_total_return_leg()
        valid_dividend_cash_flows = True
        #for dividend in dividends:
        #    query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        #    query.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', self.instrument.Oid())
        #    query.AddAttrNode('StartDate', 'EQUAL', dividend.ExDivDay())
        #    query.AddAttrNode('EndDate', 'EQUAL', dividend.RecordDay())
        #    query.AddAttrNode('CashFlowType', 'EQUAL', 'Dividend')
        #    cash_flows = query.Select()
        #    #cash_flows = acm.FCashFlow.Select('startDate="%s" endDate="%s" leg="%s" cashFlowType="Dividend"' % (
        #    #dividend.ExDivDay(), dividend.RecordDay(), tr_leg.Oid()))
        #    
        #    #dividend.ExDivDay(), dividend.RecordDay(), tr_leg.Oid())
        #    if cash_flows.Size() == 0 and not tr_leg.PassingType() in ('None', 'Custom'):
        #        valid_dividend_cash_flows = False
        current_cash_flow = self._get_current_cf()
        if not current_cash_flow:
            return
        
        min_date = current_cash_flow.StartDate()
        query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        query.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', self.instrument.Oid())
        query.AddAttrNode('CashFlowType', 'EQUAL', 'Dividend')
        query.AddAttrNode('StartDate', 'GREATER_EQUAL', min_date)
        query.AddAttrNode('StartDate', 'GREATER', tr_leg.StartDate())
        div_cash_flows =query.Select()

        if (len(div_cash_flows) != len(dividends) and not tr_leg.PassingType() in ('None', 'Custom')):
            valid_dividend_cash_flows = False

        if not valid_dividend_cash_flows:
            self._incidents.append({
                    'instrument': self.instrument.Name(),
                    'leg': tr_leg.Leg().Oid(),
                    'leg_type': tr_leg.Leg().LegType(),
                    'cash_flow': 'N/A',
                    'cash_flow_type': 'N/A',
                    'cash_flow_start_date': 'N/A',
                    'cash_flow_end_date': 'N/A',
                    'cash_flow_pay_day': 'N/A',
                    'reset': 'N/A',
                    'reset_type': 'N/A',
                    'reset_start_date': 'N/A',
                    'reset_end_date': 'N/A',
                    'reset_day': 'N/A',
                    'incident_type': 'Wrong number of dividends'
                })
        
class InitialPriceChecker(ResetChecker):
    '''All cash flows of initial price bookings should be scaled with the initial price'''
    
    error_type = 'wrong fixings on initial price bookings'
    
    def __init__(self, instr, params):
        super(InitialPriceChecker, self).__init__(instr, params)
        tr_leg = self._get_total_return_leg()
        funding_leg = self._get_funding_leg()
        
        if not (tr_leg.NominalScaling() == 'Initial Price' or 
                funding_leg == 'Initial Price'):
            raise NotInSearchScopeException('TRS %s is not scaled to initial price.' % self.instrument.Name())
        
    def _check_cash_flows(self, cash_flows, initial_price):
        for cf in cash_flows:
            nominal_scaling = acm.FReset.Select('cashFlow=%s resetType="Nominal Scaling"' % cf.Oid())
            valid = True
            message = ''
            if nominal_scaling.Size() == 0:
                valid = False
                message = 'Missing nominal scaling for cash flow %s' % cf.Oid()
                reset = ''
                reset_type = ''
                reset_start_date = ''
                reset_end_date = ''
                reset_day = ''
            elif nominal_scaling.Size() > 1:
                valid = False
                message = 'Cash flow %s has more than one nominal scaling.' % cf.Oid()
                reset = [reset.Oid() for reset in nominal_scaling]
                reset_type = [reset.ResetType() for reset in nominal_scaling]
                reset_start_date = [reset.StartDate() for reset in nominal_scaling]
                reset_end_date = [reset.EndDate() for reset in nominal_scaling]
                reset_day = [reset.Day() for reset in nominal_scaling]
            elif nominal_scaling.Size() == 1 and abs(nominal_scaling.At(0).FixingValue() - initial_price) >= math.pow(10, -2):
                valid = False
                message = 'Wrong nominal scaling fixing in cash flow %s, expected %s got %s.' % (cf.Oid(), initial_price, nominal_scaling.At(0).FixingValue())
                reset = nominal_scaling.At(0).Oid()
                reset_type = nominal_scaling.At(0).ResetType()
                reset_start_date = nominal_scaling.At(0).StartDate()
                reset_end_date = nominal_scaling.At(0).EndDate()
                reset_day = nominal_scaling.At(0).Day()
            if not valid:
                self._incidents.append({
                    'instrument': self.instrument.Name(),
                    'leg': cf.Leg().Oid(),
                    'leg_type': cf.Leg().LegType(),
                    'cash_flow': cf.Oid(),
                    'cash_flow_type': cf.CashFlowType(),
                    'cash_flow_start_date': cf.StartDate(),
                    'cash_flow_end_date': cf.EndDate(),
                    'cash_flow_pay_day': cf.PayDate(),
                    'reset': reset,
                    'reset_type': reset_type,
                    'reset_start_date': reset_start_date,
                    'reset_end_date': reset_end_date,
                    'reset_day': reset_day,
                    'incident_type': message
                })
    
    def check(self, *args, **kwargs):
        tr_leg = self._get_total_return_leg()
        funding_leg = self._get_funding_leg()
        tr_leg_initial_price = tr_leg.InitialIndexValue()
        funding_leg_initial_price = funding_leg.InitialIndexValue()
        
        if tr_leg.NominalScaling() == 'Initial Price':
            cash_flows = tr_leg.CashFlows()
            self._check_cash_flows(cash_flows, tr_leg_initial_price)
        if funding_leg.NominalScaling() == 'Initial Price':
            cash_flows = funding_leg.CashFlows()
            self._check_cash_flows(cash_flows, funding_leg_initial_price)

class MissingResetChecker(ResetChecker):
    '''Looks for missing historical fixings'''
    
    error_type = 'missing historical resets'
    
    def __init__(self, instr, params):
        super(MissingResetChecker, self).__init__(instr, params)

    def check(self, *args, **kwargs):
        query = acm.CreateFASQLQuery('FReset', 'AND')
        query.AddAttrNode('CashFlow.Leg.Instrument.Name', 'EQUAL', self.instrument.Name())
        query.AddAttrNode('Day', 'LESS', acm.Time().DateToday())
        historic_fixings = query.Select()
        for fixing in historic_fixings:
            if not fixing.IsFixed():
                self._incidents.append({
                    'instrument': self.instrument.Name(),
                    'leg': fixing.CashFlow().Leg().Oid(),
                    'leg_type': fixing.CashFlow().Leg().LegType(),
                    'cash_flow': fixing.CashFlow().Oid(),
                    'cash_flow_type': fixing.CashFlow().CashFlowType(),
                    'cash_flow_start_date': fixing.CashFlow().StartDate(),
                    'cash_flow_end_date': fixing.CashFlow().EndDate(),
                    'cash_flow_pay_day': fixing.CashFlow().PayDate(),
                    'reset': fixing.Oid(),
                    'reset_type': fixing.ResetType(),
                    'reset_start_date': fixing.StartDate(),
                    'reset_end_date': fixing.EndDate(),
                    'reset_day': fixing.Day(),
                    'incident_type': 'Missing fixing.'
                })

class PriceTRSChecker(ResetChecker):
    '''On price bookings, the funding leg is manually scaled with the fixed value of the TR leg, 
    which usually fixes earlier.'''
    
    error_type = 'wrong fixings on price bookings'
    
    def __init__(self, instr, params):
        super(PriceTRSChecker, self).__init__(instr, params)
        
        tr_leg = self._get_total_return_leg()
        funding_leg = self._get_funding_leg()
        if not (tr_leg.NominalScaling() == 'Price' and
                funding_leg.NominalScaling() == 'Price'):
            raise NotInSearchScopeException('TRS %s is not scaled to initial price.' % self.instrument.Name())
    
    def _match_nominal_scaling(self, nominal_scaling, tr_nominal_scalings):
        pay_date = nominal_scaling.CashFlow().PayDate()
        match = None
        for tr_scaling in sorted(tr_nominal_scalings, cmp=self._get_reset_comparator()):
            if (at_time.to_datetime(tr_scaling.CashFlow().StartDate()) < at_time.to_datetime(pay_date) and
                at_time.to_datetime(tr_scaling.CashFlow().PayDate()) >= at_time.to_datetime(pay_date)):
                match = tr_scaling
                break
        return match
    
    def _check_values(self, tr_nominal_scalings, funding_nominal_scalings):
        tr_leg = self._get_total_return_leg()
        funding_leg = self._get_funding_leg()
        
        
        for nominal_scaling in funding_nominal_scalings:
            tr_nominal_scaling = self._match_nominal_scaling(nominal_scaling, tr_nominal_scalings)
            #print nominal_scaling.CashFlow().Oid(), 'dbg', tr_nominal_scaling.CashFlow().Oid()
            #print nominal_scaling.FixingValue(), tr_nominal_scaling.FixingValue()
            if not tr_nominal_scaling:
                self._incidents.append({
                    'instrument': self.instrument.Name(),
                    'leg': [tr_leg.Oid(), funding_leg.Oid()],
                    'leg_type': [tr_leg.LegType(), funding_leg.LegType()],
                    'cash_flow': 'N/A',
                    'cash_flow_type': 'N/A',
                    'cash_flow_start_date': 'N/A',
                    'cash_flow_end_date': 'N/A',
                    'cash_flow_pay_day': 'N/A',
                    'reset': 'N/A',
                    'reset_type': 'N/A',
                    'reset_start_date': 'N/A',
                    'reset_end_date': 'N/A',
                    'reset_day': 'N/A',
                    'incident_type': 'No matching total return cash flow.'
                })
                
            elif tr_nominal_scaling and abs(nominal_scaling.FixingValue() - tr_nominal_scaling.FixingValue()) > math.pow(10, -2):
                self._incidents.append({
                    'instrument': self.instrument.Name(),
                    'leg': [tr_leg.Oid(), funding_leg.Oid()],
                    'leg_type': [tr_leg.LegType(), funding_leg.LegType()],
                    'cash_flow': [tr_nominal_scaling.CashFlow().Oid(), nominal_scaling.CashFlow().Oid()],
                    'cash_flow_type': [tr_nominal_scaling.CashFlow().CashFlowType(), nominal_scaling.CashFlow().CashFlowType()],
                    'cash_flow_start_date': [tr_nominal_scaling.CashFlow().StartDate(), nominal_scaling.CashFlow().StartDate()],
                    'cash_flow_end_date': [tr_nominal_scaling.CashFlow().EndDate(), nominal_scaling.CashFlow().EndDate()],
                    'cash_flow_pay_day': [tr_nominal_scaling.CashFlow().PayDate(), nominal_scaling.CashFlow().PayDate()],
                    'reset': [tr_nominal_scaling.Oid(), nominal_scaling.Oid()],
                    'reset_type': [tr_nominal_scaling.ResetType(), nominal_scaling.ResetType()],
                    'reset_start_date': [tr_nominal_scaling.StartDate(), nominal_scaling.StartDate()],
                    'reset_end_date': [tr_nominal_scaling.EndDate(), nominal_scaling.EndDate()],
                    'reset_day': [tr_nominal_scaling.Day(), nominal_scaling.Day()],
                    'incident_type': 'Wrong fixing values on funding leg.'
                })
            
    def check(self, *args, **kwargs):
        tr_leg = self._get_total_return_leg()
        funding_leg = self._get_funding_leg()
        
        query = acm.CreateFASQLQuery(acm.FReset, 'AND')
        query.AddAttrNode('ResetType', 'EQUAL', 'Nominal Scaling')
        query.AddAttrNode('CashFlow.Leg.Oid', 'EQUAL', tr_leg.Oid())
        tr_nominal_scalings = query.Select()
        
        query = acm.CreateFASQLQuery(acm.FReset, 'AND')
        query.AddAttrNode('ResetType', 'EQUAL', 'Nominal Scaling')
        query.AddAttrNode('CashFlow.Leg.Oid', 'EQUAL', funding_leg.Oid())
        funding_nominal_scalings = query.Select()
        
        self._check_values(tr_nominal_scalings, funding_nominal_scalings)
    
class NotInSearchScopeException(Exception):
    def __init__(self, msg):
        super(NotInSearchScopeException, self).__init__(msg)
        
class InvalidInstrumentException(Exception):
    def __init__(self, msg):
        super(InvalidInstrumentException, self).__init__(msg)

def _init_logging(params):
    global LOGGER
    LOGGER = FLogger.FLogger('TRS Checker')
    LOGGER.Reinitialize(
        level=LOG_LEVEL[params['log_level']], 
        keep=False, 
        logOnce=False, 
        logToConsole=False, 
        logToPrime=True, 
        logToFileAtSpecifiedPath=os.path.join(params['log_directory'], 
            'TRS Checker_%s.log' % acm_date('TODAY')
        ), 
        filters=None)

def _init_incidents(params):
    incidents = Incidents(params)
    incidents.register_checker(DividendScalingChecker)
    incidents.register_checker(MissingDividendsChecker)
    incidents.register_checker(InitialPriceChecker)
    incidents.register_checker(MissingResetChecker)
    incidents.register_checker(PriceTRSChecker)
    
    return incidents

def _get_instruments(params):
    considered_trs = set()
    
    for trade in params['trades']:
        trs = trade.Instrument()
        if trs.Name() in considered_trs:
            continue
        elif not trs.Class().IsSubtype(acm.FTotalReturnSwap):
            continue
        considered_trs.add(trs.Name())
        
    return considered_trs

def _get_trs_checkers(params):
    '''return a list of relevant checkers'''
    checkers = []
    if params['mode'] == 'missing dividend scalings':
        checker = DividendScalingChecker
        checkers.append(checker)
    elif params['mode'] == 'missing dividends':
        checker = MissingDividendsChecker
        checkers.append(checker)
    elif params['mode'] == 'wrong initial price fixings':
        checker = InitialPriceChecker
        checkers.append(checker)
    elif params['mode'] == 'wrong nominal scalings':
        checker = PriceTRSChecker
        checkers.append(checker)
    elif params['mode'] == 'missing fixings':
        params = MissingResetChecker
        checkers.append(checker)
    elif params['mode'] == 'all error types':
        checker = DividendScalingChecker
        checkers.append(checker)
        checker = MissingDividendsChecker
        checkers.append(checker)
        checker = InitialPriceChecker
        checkers.append(checker)
        checker = PriceTRSChecker
        checkers.append(checker)
        checker = MissingResetChecker
        checkers.append(checker)
        
    return checkers

def _output_results(params, incidents):
    if params['output_mode'] == 'To Console':
        incidents.write_to_console()
    elif params['output_mode'] == 'email':
        incidents.send_as_email()
    elif params['output_mode'] == 'To File':
        incidents.write_to_file()
    else:
        LOGGER.DLOG('No such output mode %s' % params['output_mode'])

def ael_main(params):
    _init_logging(params)
    LOGGER.LOG('STARTING TRS ERROR REPORT GENERATION...')
    
    LOGGER.DLOG('Initializing incidents data structure...')
    incidents = _init_incidents(params)
    LOGGER.DLOG('Initialized incidents data structure.')
    
    considered_trs = set()
    LOGGER.DLOG('Processing instruments/trades...')
    for trade in params['trades']:
        trs = trade.Instrument()
        if trs.Name() in considered_trs:
            LOGGER.DLOG('Instrument %s (found via trade %s) already processed. Skipped.')
            continue
        elif not trs.Class().IsSubtype(acm.FTotalReturnSwap):
            LOGGER.WLOG('Instrument %s (found via trade %s) is not a TRS. Skipped.')
            continue
        
        LOGGER.DLOG('Processing instrument %s...' % trs.Name())
        considered_trs.add(trs.Name())
        
        try:
            checkers = _get_trs_checkers(params)
            for checker in checkers:
                try:
                    LOGGER.DLOG('Processing checker %s for instrument %s...' % (
                                    checker.__name__, trs.Name()))
                    checker_obj = checker(trs, params)
                    checker_obj.check()
                    checker_obj.stamp_incidents()
                    found_incidents = checker_obj.get_incidents()
                    incidents += found_incidents
                    
                    LOGGER.DLOG('Found %s incidents.' % len(found_incidents))
                    LOGGER.DLOG('Processed checker %s for instrument %s.' % (
                                    checker.__name__, trs.Name()))
                except NotInSearchScopeException:
                    LOGGER.DLOG('Instrument %s is not in search scope. Skipped.' % trs.Name())
                except InvalidInstrumentException:
                    LOGGER.WLOG('Instrument %s is considered invalid for the checking logic. Skipped.' % trs.Name())
                except Exception, e:
                    LOGGER.ELOG('Unknown error when checking instrument %s. Traceback: %s' % (
                                    trs.Name(), repr(traceback.extract_stack())))

        except Exception, e:
            LOGGER.ELOG('Unknown error when getting checkers for instrument %s, params %s. Traceback: %s' % (
                            trs.Name(), params, repr(traceback.extract_stack())))
            
        LOGGER.DLOG('Processed instrument %s...' % trs.Name())
    LOGGER.DLOG('Processed instruments/trades.')
    
    LOGGER.LOG('Creating report output...')
    _output_results(params, incidents)
    LOGGER.LOG('Created report output.')
    
    LOGGER.LOG('COMPLETED SUCCESSFULLY.')
