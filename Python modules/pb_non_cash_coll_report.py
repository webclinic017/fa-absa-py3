"""
-------------------------------------------------------------------------------
MODULE
    pb_non_cash_coll_report

DESCRIPTION
    Date                : 2018-02-27
    Purpose             : This module generates XML reports to check bookings
                          and their counter trades in the portfolios PB_CR_LIVE
                          and PB_CR_NONCASHCOLL
    Requester           : Eveshnee Naidoo
    Developer           : Tibor Reiss
    ABITFA              : 5282

HISTORY
===============================================================================
2018-02-27    Tibor Reiss    ABITFA-5282: initial implementation
-------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_report import DataToXMLReportCreator
from at_logging import getLogger
from datetime import datetime
from xml.etree import ElementTree
import re
from collections import defaultdict
from os import path

LOGGER = getLogger(__name__)

MATCHED = "YES"
NOT_MATCHED = "NO"
TRADE_QUERY = "pb_non_cash_coll_report"

class NonCashCollBookings(DataToXMLReportCreator):
    """
    Class for generating the XML report
    """
    def __init__(self, client, output_path, file_name, xsl_template, date_from=None):
        self.client = client
        self.match = defaultdict(lambda: defaultdict(list))
        self.date_from = date_from
        super(NonCashCollBookings, self).__init__(file_name, 'xls',
                                                  output_path, xsl_template)

    def _collect_data(self):
        """
        Check all trades and look for the matching trade
        Only checks one direction: from PB_CR_LIVE to PB_CR_NONCASHCOLL
        """
        LOGGER.info("Collecting data - {}...".format(__name__))
        
        #Can't be None
        if not self.date_from:
            raise ValueError("NonCashCollBookings.date_from is not initialized")
        
        #Get all client names
        client_names = NonCashCollBookings.get_clients("PB_*_FF_" + self.client + "_CR")
        
        #Loop through all clients
        for cln in client_names:
            LOGGER.info("Processing client {}...".format(cln))
            
            #The trades in PB_CR_LIVE
            query_trades = acm.FStoredASQLQuery[TRADE_QUERY].Query().Clone()
            pf_cr_live = NonCashCollBookings.get_portfolios("PB_*_FF_" + cln + "_CR")
            and_node = query_trades.AddOpNode("AND")
            and_node.AddAttrNodeString("Portfolio.Name", pf_cr_live, "EQUAL")
            and_node = query_trades.AddOpNode("AND")
            and_node.AddAttrNodeString("AcquireDay", self.date_from, "GREATER_EQUAL")
            bookings = query_trades.Select()
            LOGGER.info("Found {} primary trades".format(len(bookings)))
            
            #The non-cash collateral trades in PB_CR_NONCASHCOLL
            query_trades = acm.FStoredASQLQuery[TRADE_QUERY].Query().Clone()
            pf_non_cash_coll = NonCashCollBookings.get_portfolios("PB_CAT_*_" + cln + "_CR")
            and_node = query_trades.AddOpNode("AND")
            and_node.AddAttrNodeString("Portfolio.Name", pf_non_cash_coll, "RE_LIKE_NOCASE")
            and_node = query_trades.AddOpNode("AND")
            and_node.AddAttrNodeString("AcquireDay", self.date_from, "GREATER_EQUAL")
            non_cash_coll = query_trades.Select()
            LOGGER.info("Found {} non-cash-coll trades".format(len(non_cash_coll)))
            
            #Match on the following criteria:
            #  trdnbr: the primary trade must be before the non-cash coll trade
            #  ins_name: instrument names are similar
            #            check only first 7 characters
            #            TODO: more sophisticated matching, e.g. Levenshtein
            #  ins_type: same
            #  acquire_day: non-cash coll must be booked on the same day
            #  price: check only first two decimals
            for t1 in bookings:
                found_match = False
                ins_name1 = t1.Instrument().Name()
                for t2 in non_cash_coll:
                    ins_name2 = t2.Instrument().Name()
                    ins_name_len = len(ins_name2) if len(ins_name2) < 7 else 7
                    LOGGER.debug(ins_name_len, \
                                 ins_name1[0:ins_name_len], \
                                 ins_name2[0:ins_name_len])
                    if t1.Name() < t2.Name() \
                           and ins_name1[0:ins_name_len] ==  ins_name2[0:ins_name_len] \
                           and t1.Instrument().InsType() == t2.Instrument().InsType() \
                           and t1.AcquireDay() == t2.AcquireDay() \
                           and round(t1.Price(), 2) == round(t2.Price(), 2):
                        LOGGER.debug("Found a match: {} {}".format(t1.Name(), t2.Name()))
                        self.match[cln][MATCHED].append({
                               'InsName_str' : ins_name1,
                               'Number_int' : t1.Name(),
                               'Portfolio_str' : t1.Portfolio().Name(),
                               'TradeMatched_int' : t2.Name()})
                        found_match = True
                if not found_match:
                    self.match[cln][NOT_MATCHED].append({
                               'InsName_str' : ins_name1,
                               'Number_int' : t1.Name(),
                               'Portfolio_str' : t1.Portfolio().Name(),
                               'TradeMatched_int' : ''})
    
    def _generate_xml(self):
        LOGGER.info("Generating XML...")
        report_xml = ElementTree.Element('report')
        columns_xml = ElementTree.SubElement(report_xml, 'columns')
        columns_written = False
        #Create client element
        for cln in sorted(self.match):
            for m in self.match[cln]:
                if self.match[cln][m]:
                    client_xml = ElementTree.SubElement(report_xml, 'client')
                    client_xml.set('name', cln)
                    client_xml.set('matched',
                                   str(1) if m == MATCHED else str(0))
                    #Create trade elements
                    for t in self.match[cln][m]:
                        trade_xml = ElementTree.SubElement(client_xml, 'entity')
                        for k in t:
                            trade_xml.set(k, str(t[k]))
                            if not columns_written:
                                columns_xml.set(k.split('_')[0], '')
                        columns_written = True
        report_xml_str = ('<?xml version="1.0" encoding="utf-8"?>' +
                          ElementTree.tostring(report_xml))
        return report_xml_str

    @staticmethod
    def get_clients(pattern):
        """
        Return the client names which trades will be checked
        """
        LOGGER.info("Getting client names...")
        client_names = []
        query_clients  = acm.CreateFASQLQuery("FPhysicalPortfolio", "AND")
        query_clients.AddAttrNode("Name", "RE_LIKE_NOCASE", pattern)
        pfs = query_clients.Select()
        for pf in pfs:
            if not NonCashCollBookings.portf_is_graveyarded(pf.Name()):
                name = re.search('\w+_FF_([\w\ \.\_\/]+)_CR', pf.Name()).group(1)
                client_names.append(name)
        return set(client_names)
    
    @staticmethod
    def get_portfolios(pattern):
        """
        Return non-graveyarded portfolios 
        """
        portfolios = []
        query_pf = acm.CreateFASQLQuery("FPhysicalPortfolio", "AND")
        query_pf.AddAttrNode("Name", "RE_LIKE_NOCASE", pattern)
        res = query_pf.Select()
        for pf in res:
            if not NonCashCollBookings.portf_is_graveyarded(pf.Name()):            
                portfolios.append(pf.Name())
        return portfolios

    @staticmethod
    def portf_is_graveyarded(portf):
        """
        Check if portfolio or any of is parents is graveyarded
        """
        if not portf:
            return False

        acm_portf = portf
        if isinstance(portf, str):
            acm_portf = acm.FPhysicalPortfolio[portf]

        if acm_portf.Name() == "GRAVEYARD":
            return True
        for ml in acm_portf.MemberLinks():
            return NonCashCollBookings.portf_is_graveyarded(ml.OwnerPortfolio())
        return False

class NonCashCollPositions(NonCashCollBookings):
    def __init__(self, client, output_path, file_name, xsl_template):
        super(NonCashCollPositions, self).__init__(client, output_path, 
                                                   file_name, xsl_template)

    def _collect_data(self):
        LOGGER.info("Collecting data - {}...".format(__name__))
        
        #Get all portfolios under PB_CR_LIVE, and all client names
        client_names = NonCashCollBookings.get_clients(
                        "PB_*_FF_" + self.client + "_CR")
        
        calcSpace = acm.Calculations().CreateCalculationSpace(
                        "Standard", "FPortfolioSheet")
        #Iterate through every client
        for cln in client_names:
            LOGGER.info("Processing client {}...".format(cln))
            pf_cr_live = NonCashCollBookings.get_portfolios(
                        "PB_*_FF_" + cln + "_CR")
            pf_non_cash_coll = NonCashCollBookings.get_portfolios(
                        "PB_CAT_*_" + cln + "_CR")
            for pf in pf_cr_live:
                calcSpace.InsertItem(acm.FPhysicalPortfolio[pf])
            for pf in pf_non_cash_coll:
                calcSpace.InsertItem(acm.FPhysicalPortfolio[pf])
            calcSpace.Refresh()
            self.compare_portfolios(cln, calcSpace)
            calcSpace.Clear()

    def getValue(self, calcSpace, node, column_name):
        try:
            return_value = calcSpace.CalculateValue(node, column_name).Number()
        except:
            return_value = 0
        return return_value

    def compare_portfolios(self, cln, calcSpace):
        #Compare the positions in the given 2 portfolios
        pf_iter = calcSpace.RowTreeIterator().Clone().FirstChild()
        ins_pos = defaultdict(lambda: [ {'pos' : 0.0, 'pf' : []}, {'pos' : 0.0, 'pf' : []} ])
        while pf_iter:
            pf_name = pf_iter.Tree().StringKey()
            ins_iter = pf_iter.Clone().FirstChild()
            while ins_iter:
                ins_name = ins_iter.Tree().StringKey()
                pos_value = self.getValue(calcSpace, ins_iter.Tree(), "Portfolio Position")
                #XXX and XXX/MTM instruments belong to the same position
                #The XXX instrument is used to book the collateral
                #The XXX/MTM instrument is used to book the original trade
                regexp = re.compile('(.*)\/MTM')
                ins_name_short = regexp.match(ins_name)
                if ins_name_short:
                    ins_name_short = ins_name_short.group(1)
                else:
                    ins_name_short = ins_name
                if "PB_CAT" in pf_name:
                    ins_pos[ins_name_short][1]['pos'] += pos_value
                    if pf_name not in ins_pos[ins_name_short][1]['pf']:
                        ins_pos[ins_name_short][1]['pf'].append(pf_name)
                else:
                    ins_pos[ins_name_short][0]['pos'] += pos_value
                    if pf_name not in ins_pos[ins_name_short][0]['pf']:
                        ins_pos[ins_name_short][0]['pf'].append(pf_name)
                ins_iter = ins_iter.NextSibling()
            pf_iter = pf_iter.NextSibling()
        for i in ins_pos:
            ins_pos[i][0]['pos'] = round(ins_pos[i][0]['pos'], 2)
            ins_pos[i][1]['pos'] = round(ins_pos[i][1]['pos'], 2)
            if ins_pos[i][0]['pos'] == ins_pos[i][1]['pos']:
                if ins_pos[i][0]['pos'] != 0.0:
                    self.match[cln][MATCHED].append({
                        'InsName_str': i,
                        'Pos1Data_d': ins_pos[i][0]['pos'],
                        'Pos1Portfolio_str': ", ".join(ins_pos[i][0]['pf']),
                        'Pos2Data_d': ins_pos[i][1]['pos'],
                        'Pos2Portfolio_str': ", ".join(ins_pos[i][1]['pf']),})
            else:
                self.match[cln][NOT_MATCHED].append({
                        'InsName_str': i,
                        'Pos1Data_d': ins_pos[i][0]['pos'],
                        'Pos1Portfolio_str': ", ".join(ins_pos[i][0]['pf']),
                        'Pos2Data_d': ins_pos[i][1]['pos'],
                        'Pos2Portfolio_str': ", ".join(ins_pos[i][1]['pf']),})

ael_variables = AelVariableHandler()
ael_variables.add_bool("gen_position",
                       label="Position report",
                       alt="Check this to generate position report",
                       default=True)
ael_variables.add_bool("gen_trade",
                       label="Trade report",
                       alt="Check this to generate trade report",
                       default=True)
ael_variables.add("date_from",
                  label="Trades since this (relative) date",
                  cls="string",
                  default="-8d",
                  mandatory=True, 
                  alt="Trades with acquire day after the specified date")
ael_variables.add("dir",
                  label="Save to",
                  cls="string",
                  default=r"/services/frontnt/Task",
                  mandatory=True,
                  alt="Location for report")
ael_variables.add("client",
                  label="Client name",
                  cls="string",
                  default="*",
                  mandatory=True, 
                  alt="Specify a pattern according to which clients' \
                       names will be searched, e.g. to get all clients \
                       whose name starts with S write S*")

def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    
    xsl_template = acm.GetDefaultContext().GetExtension(
                  'FXSLTemplate', 'FObject', 'NonCashCollateralReport')
    output_path = ael_params['dir']
    
    #POSITIONS
    if ael_params['gen_position'] == True:
        try:
            file_name = "Positions_NonCashCollateral"
            report = NonCashCollPositions(ael_params['client'], output_path,
                                          file_name, xsl_template)
            report.create_report()
            LOGGER.output(path.join(ael_params['dir'], file_name + ".csv"))
            LOGGER.info("%s: Completed the position report.", acm.Time.TimeNow())
        except:
            LOGGER.exception("""Exception occurred while generating
                                position report""")
    
    #TRADES
    if ael_params['gen_trade'] == True:
        try:
            file_name = "Trades_NonCashCollateral"
            report = NonCashCollBookings(ael_params['client'], output_path, 
                                         file_name, xsl_template, 
                                         ael_params['date_from'])
            report.create_report()
            LOGGER.output(path.join(ael_params['dir'], file_name + ".csv"))
            LOGGER.info("%s: Completed the trade report.", acm.Time.TimeNow())
        except:
            LOGGER.exception("""Exception occurred while generating
                                trade report""")

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")    
    LOGGER.info("Task finished successfully")
