'''
Created on 18 Nov 2013

@author: conicova
'''
from __future__ import print_function
import acm
import FRunScriptGUI
import os
from at_ael_variables import AelVariableHandler
import ael

acm_time = acm.Time()
TODAY = acm_time.DateToday()
TODAY_OFFSET_10_YEARS = acm_time.DateAddDelta(TODAY, 10, 0, 0)

class CashFlowLadderReport(object):
    
    _cf_header_titles = ['Pay Date', 'CF Proj', 'CF PV']
    _cf_proj_breaks_header_titles = ['Pay Date', 'TradeNbr', 'Trans ref', 'CFNbr'
                                        , 'CF Type', 'CF Proj', 'CF PV']
    @staticmethod
    def _get_number(item):
        '''
        Return the value of the attribute Number, if such attribute exists on the item.
        '''
        if hasattr(item, "Number"):
            item = item.Number()
       
        return item
    
    @classmethod
    def _proc_cash_flow(cls, cfl, trd, mf_calc_space):
        '''
        Returns a dictionary with the keys: Projected, PresentValue and Type
        and the corresponding values from the FCashFlow object.
        
        cfl: FCashFlow
        trd: FTrade
        mf_cal_space: FCalculationSpace  
        '''
        data = {}
        '''
        # !!! the calculation space returns a different value in some cases. 
        # cfl.projected_cf(trd.value_day)
        data['Projected'] = mf_calc_space.CalculateValue(cfl, 'Cash Analysis Projected', None, False)
        data['Projected'] = cls._get_number(data['Projected'])
        # cfl.present_value()
        data['PresentValue'] = mf_calc_space.CalculateValue(cfl, 'Portfolio Present Value', None, False)
        data['PresentValue'] = cls._get_number(data['PresentValue'])
        data['Type'] = mf_calc_space.CalculateValue(cfl, 'Money Flow Type', None, False)
        '''
        cfl_ael = ael.CashFlow[cfl.Oid()]
        data['Projected'] = cfl_ael.projected_cf(ael.date(trd.ValueDay()))
        data['PresentValue'] = cfl_ael.present_value()
        data['Type'] = cfl_ael.type
        return data

    def _proc_legs_cash_flows(self, trd, cf_strdate, cf_enddate
                              , legs, tq, cfdict, cftref, mf_calc_space):
        '''
        Processes all the cash flows from the passed list of legs.
        Populates the cfdict, cftref dictionaries.
        The cash flow pay date has to be in the specified time interval.
        
        trd: FTrade
        cf_strdate: date
        cf_enddate: date
        legs: list of FLeg
        tq: trade quantity
        cfdict: dictionary{date:(Projected,PresentValue)}
        cftref: dictionary{date:(trdnbr, cfwnbr)}
        mf_cal_space: FCalculationSpace 
        '''
        for l in legs:
            for c in l.CashFlows():
                # if c.PayDate() != '2013-07-31':
                    # continue
                if c.PayDate() >= cf_strdate and c.PayDate() <= cf_enddate:
                    cf_dts = c.PayDate()
                    if cf_dts not in cfdict.keys():
                        cfdict[cf_dts] = (0, 0)
                        cftref[cf_dts] = []
                    cfl_data = self._proc_cash_flow(c, trd, mf_calc_space)
                    mf_calc_space.Clear()
                    cfdict[cf_dts] = (cfdict[cf_dts][0] + cfl_data['Projected'] * tq
                                      , cfdict[cf_dts][1] + cfl_data['PresentValue'] * tq)
                    tlist = cftref[cf_dts]
                    entry = (trd.Oid(), c.Oid())
                    tlist.append(entry)
                    cftref[cf_dts] = tlist
                    # print (c.Oid(), '\t', trd.Oid(), '\t', cfl_data['Projected'] , '\t', cfl_data['PresentValue'], '\t', trd.ValueDay(), '\t', tq)
    @staticmethod
    def _get_weight(comblink, ins):
        '''
        Returns the weight of the specified instrument
        in the specified combination mapping.
        
        comblink: list of FComnInsMap
        ins: FInstrument 
        '''
        weight = 0
        for cl in comblink:        
            if cl.Instrument() == ins:
                weight = cl.Weight()
        return weight
    
    @staticmethod
    def _get_combination_obj(trd):
        '''
        Returns a tuple containing the:
            1. Instruments mapped to the Combination from the trade instrument
            2. The Combination mapping for the trade instrument
        The instrument has to be of type FCombination.
        
        trd: FTrade 
        '''
        comb_ins = trd.Instrument().Instruments()  # Has to be of type FCombination
        comblink = acm.FCombInstrMap.Select("combination = {0}".format(trd.Instrument().Oid()))
        
        return (comb_ins, comblink)
        
    def _proc_ins_type_not_combination(self, trd, cf_strdate
                                       , cf_enddate, cfdict, cftref, mf_calc_space):
        self._proc_legs_cash_flows(trd, cf_strdate, cf_enddate
                              , trd.Instrument().Legs(), trd.Quantity()
                              , cfdict, cftref, mf_calc_space)
    
    def _proc_ins_type_combination(self, trd, cf_strdate
                                   , cf_enddate, cfdict, cftref, mf_calc_space):
        comb_ins, comblink = self._get_combination_obj(trd)
        for ins in comb_ins:
            weight = self._get_weight(comblink, ins)
            tq = trd.Quantity() / 1000000.0 * weight
            self._proc_legs_cash_flows(trd, cf_strdate, cf_enddate
                                       , ins.Legs(), tq, cfdict, cftref, mf_calc_space)
    
    def _fill_dicts(self, tf, cf_strdate, cf_enddate, cfdict, cftref, mf_calc_space):
        processed = 0
        acm.Log("To process {0} trades".format(len(tf.Trades())))
        for trd in tf.Trades():
            if trd.Instrument().InsType() <> 'Combination':
                self._proc_ins_type_not_combination(trd, cf_strdate
                                                    , cf_enddate, cfdict, cftref, mf_calc_space)
            else:
                self._proc_ins_type_combination(trd, cf_strdate
                                                , cf_enddate, cfdict, cftref, mf_calc_space)
            processed += 1
            if processed % 100 == 0:
                acm.Log("Processed {0} trades".format(processed))
     
    @staticmethod
    def _output_list(vals, writer):
        writer("\t".join(vals))
   
    def create_report(self, tf, cf_strdate, cf_enddate, writer):
        '''
        Creates the CashFlowLadder report based on the 
        provided trade filter, start and end date.
        The report is outputed using the provided writer.
        
        tf: FTradeSelection
        cf_strdate: date
        cf_enddate: date
        writer: a method that gets a string parameter (one report line)
        '''
        self._output_list(self._cf_header_titles, writer)
        
        cfdict = {}  # Keys: Cash Flow Dates; Values: (Projected CF, Present Value)
        cftref = {}  # Keys: Cash Flow Dates; Values: [(t.trdnbr, c.cfwnbr)]
        
        context = acm.GetDefaultContext()
        mf_calc_space = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')
        
        self._fill_dicts(tf, cf_strdate, cf_enddate, cfdict, cftref, mf_calc_space)
        
        cfk = cfdict.keys()
        cfk.sort()
        
        cfbreaks = []  # Cash Flow dates
        for k in cfk:
            # Date, projected CF, Present Value
            cf_row_values = [str(k), str(cfdict[k][0]), str(cfdict[k][1])]
            self._output_list(cf_row_values, writer)
            if abs(cfdict[k][0]) > 1:
                cfbreaks.append(k)
        
        self._output_list([''], writer)
        self._output_list(['CF Proj Breaks'], writer)
        self._output_list(self._cf_proj_breaks_header_titles, writer)
        
        acm.Log("To process {0} cash flow breaks".format(len(cfbreaks)))
        for cfb in cfbreaks:
            tlist = cftref[cfb]
            for e in tlist:
                trd = acm.FTrade[e[0]]
                cfl = acm.FCashFlow[e[1]]
                tq = trd.Quantity()
                if trd.Instrument().InsType() == 'Combination':            
                    comb_ins, comblink = self._get_combination_obj(trd)
                    weight = 0
                    for ins in comb_ins:
                        weight = self._get_weight(comblink, cfl.Leg().Instrument())
                    tq = trd.Quantity() / 1000000.0 * weight
                    
                trx_trade = trd.TrxTrade().Oid() if trd.TrxTrade() else ''
                cfl_data = self._proc_cash_flow(cfl, trd, mf_calc_space)
                mf_calc_space.Clear()
                cf_proj_breaks_row_values = [cfb, str(trd.Oid()), str(trx_trade)
                                             , str(cfl.Oid())
                                             , cfl_data['Type']
                                             , str(cfl_data['Projected'] * tq)
                                             , str(cfl_data['PresentValue'] * tq)]
                self._output_list(cf_proj_breaks_row_values, writer)
    
trade_filter_names = sorted([f.Name() for f in acm.FTradeSelection.Select("")])

def custom_dates(fieldValues):
        """Input hook for ael_variables"""
        use_custom_dates = ael_variables[1].value == '1'
        ael_variables[2].enabled = use_custom_dates
        ael_variables[3].enabled = use_custom_dates
        return fieldValues

ael_variables = AelVariableHandler()

ael_variables.add(
    'tf_title',
    label='TradeFilter',
    collection=trade_filter_names,
    default='SND_All_Trades_GNB',
    alt='The trade filter title that will be used to create trade rows',
    mandatory=1 
    )
ael_variables.add(
    'custom_dates',
    label='Custom dates',
    collection=[0, 1],
    alt='Check this in order to use custom end and start dates',
    cls='int',
    hook=custom_dates  
    )
ael_variables.add(
    'cf_strdate',
    label='CF Start Date',
    default=TODAY,
    alt='Cash Flow start date'
    )
ael_variables.add(
    'cf_enddate',
    label='CF End Date',
    default=TODAY_OFFSET_10_YEARS,
    alt='Cash Flow end date' 
    )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp\ABITFA-2134',
    alt='The directory where to which the file will be dropped.',
    mandatory=1 
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='CashFlowLadder.csv',
    alt='The directory where to which the file will be dropped.',
    mandatory=1 
    )

def ael_main(dict_arg):
    """Main entry point for FA"""
    acm.Log("Starting {0}".format(__name__))
    
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
    
    tf_title = dict_arg['tf_title']
    path = dict_arg['path']
    custom_dates = dict_arg['custom_dates']
    cf_strdate = TODAY
    cf_enddate = TODAY_OFFSET_10_YEARS
    if custom_dates:
        cf_strdate = dict_arg['cf_strdate']
        cf_enddate = dict_arg['cf_enddate']
        
    file_name = dict_arg['file_name']
    
    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return
    
    tf = acm.FTradeSelection[tf_title]
    if not tf:
        warning_function("Warning",
            "Could not find the specified trade filter!", 0)
        return
    
    file_path = os.path.join(path, file_name)
    
    with open(file_path, 'w') as file_w:
        writer_f = lambda line: file_w.write(line + '\n')
        writer_f("Start date:{0}".format(cf_strdate))
        writer_f("End date:{0}".format(cf_enddate))
        CashFlowLadderReport().create_report(tf, cf_strdate, cf_enddate, writer_f)
    
    acm.Log("Wrote secondary output to {0}".format(file_path))
    acm.Log("Completed successfully")
                
