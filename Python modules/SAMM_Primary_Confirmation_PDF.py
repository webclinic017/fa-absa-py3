# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    Aaeda Salejee    Ickin Vural            ABITFA-569
# Decommission platypus and move all existing reports using it to FOP

# OPS    Aaeda Salejee    Tshepo Mabena          796819
# Amended the code to include different rate types depending on the rolling period for Deposits.

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS    Bheki Mayisela   Jan Sinkora            ABITFA-1934
# Fixed account

# OPS Sipho Ndlalane    Sanele Macanda        CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions

# OPS Sipho Ndlalane    Andrei Conicov       CHNG0001799503 ABITFA - 2238 (18/03/2014)
# Added the possibility to merge files and made the 'date' an optional parameter
# Fixed the currency symbol

# OPS Sipho Ndlalane    Pavel Saparov       ABITFA-2237 (02/07/2014)
# Saving Confo Date Sent and Confo Text

# OPS Breytenbach Linda    Sanele Macanda   ABITFA-2747 (08/08/2014)

# OPS Elaine Visagie Sanele Macanda catering for negative interest rate ABITFA-3319- CHNG0002572133

# OPS    Ruiters Rehana         Lawrence Mucheka   CHNG0003005620
# Fix for Deposits which have a Float Leg only - Return 0.00 as the rate
# Fix for FRNs -  when rate is not available


from SAGEN_IT_Functions import startFile
from XMLReport import contact_from_pty, mkinfo, mkcaption, mkvalues
from at_ael_variables import AelVariableHandler
from zak_funcs import formcurr
import XMLReport
import acm
import ael
import at
import os
import at_time


ins_types = [at.INST_DEPOSIT, at.INST_CD, at.INST_FRN, at.INST_SECURITY_LOAN]

def get_date(txt):
    """Converts the provided text to a date"""
    return at.date_to_datetime(txt).date()


class ReturnConfirmationReport(XMLReport.StatementReportBase):
    def __init__(self, trade, date, filter_by_date):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.date = date
        self.filter_by_date = filter_by_date
        self.t = ael.Trade[trade.Oid()]
        self.mm_instype = self._mmInstype()

    def _accNum(self):
        used_account = self.trade.used_account(self.trade.Currency().Name(),
                                               1, 0, 0, 0, None)
        account = acm.FAccount[used_account]
        return account.Account() if account else ' '

    def _mmInstype(self):
        try:
            return (self.t.add_info(at.addInfoSpecEnum.FUNDING_INSTYPE)
                or self.t.add_info(at.addInfoSpecEnum.MM_INSTYPE)
                or self.t.add_info(at.addInfoSpecEnum.INSTYPE))
        except:
            return ' '

    def _nominal(self):
        if self.t.insaddr.instype in ins_types:
            # return 0 if the trade date is not equal to the specified date
            # and the BO Confirm date is not equal to the specified date
            if self.filter_by_date:
                if not self.date == get_date(self.t.creat_time):
                    ts_val = at.addInfo.get_value(self.trade,
                                                  at.addInfoSpecEnum.BOCONFIRM_TIMESTAMP)
                    if (not ts_val or self.date != get_date(ts_val)):
                        return 0.0

            # Ael nominal_amount behaves inconsistently.
            return abs(self.trade.Nominal())
        return 0.0

    def _rate(self):
        Rate = '0.00'
        ResetDates = []

        if self.t.insaddr.instype == at.INST_FRN:
            for l in self.t.insaddr.legs():
                for cf in l.cash_flows():
                    if cf.type == 'Float Rate':
                        for r in cf.resets():
                            ResetDates.append(r.start_day)

            for l in self.t.insaddr.legs():
                for cf in l.cash_flows():
                    if cf.type == 'Float Rate':
                        for r in cf.resets():
                            if min(ResetDates) == r.start_day:
                                Rate = "{0} PLUS SPREAD {1} ( {2} %)".format(l.float_rate.insid,
                                                                    l.spread,
                                                                    l.spread + r.value)

        elif self.t.insaddr.instype in (at.INST_CD, at.INST_DEPOSIT):            
            for l in self.t.insaddr.legs():
                if l.type == 'Fixed':
                    Rate = l.fixed_rate                

        else:
            Rate = str(self.t.price)
        return Rate

    def _rollPeriod(self):
        legs = self.trade.Instrument().Legs()
        is_deposit = self.trade.Instrument().InsType() == at.INST_DEPOSIT
        return legs[-1].RollingPeriod() if legs and is_deposit else ''

    def _rollUnit(self):
        Rollunit = ''
        for l in self.t.insaddr.legs():
            roll_period_count = getattr(l, 'rolling_period.count')
            roll_period_unit = getattr(l, 'rolling_period.unit')

            if roll_period_count == 0:
                Rollunit = ' '
            elif (roll_period_count == 1 and roll_period_unit == 'Month'):
                Rollunit = 'Month'
            else:
                Rollunit = roll_period_unit
        return Rollunit

    def _type(self):
        nominal_amount = self.trade.Nominal()
        return 'your Deposit' if nominal_amount < 0 else 'our Loan to you'

    def client_address(self):
        return contact_from_pty(self.trade.Counterparty())

    def statement_detail(self):

        detailList = [("CONFIRMATION DATE", self.date.strftime('%Y-%m-%d')),
            ("ACCOUNT NR:", self._accNum()),
            ("OUR REF:", "{0} {1}".format(self.t.trdnbr, self.mm_instype))]

        yield mkvalues(*detailList)

        yield mkcaption("We confirm {0} to you as follows:".format(self._type()))

        if self.mm_instype == 'FDI':
            rates = {"1m": "(NACM)",
                     "3m": "(NACQ)",
                     "6m": "(NACH)",
                     "12m": "(NACA)",
                     "1y": "(NACA)"}
            rate_name = rates[self._rollPeriod()]
        elif self.mm_instype in ('FDE', 'FDC'):
            rate_name = "(Yield)"
        else:
            rate_name = "% per Annum"

        trd_curr = self.trade.Currency().Name()
        irp = str(self._rollPeriod()) + " " + self._rollUnit()
        intr = self.t.interest_settled(self.t.value_day,
                                           self.t.insaddr.exp_day,
                                           trd_curr)
        returnRate = self._rate()
        if returnRate and float(returnRate) < 0.0:
            intr *=-1
        else:
            intr = abs(intr)
            
        value_day = self.t.value_day.to_string("%d %B %Y")
        exp_day = self.t.insaddr.exp_day.to_string("%d %B %Y")

        detailList = [
            ("Amount of " + self._type(), formcurr(self._nominal(), currency=trd_curr)),
            ("Period of " + self._type(), "{0} - {1}".format(value_day, exp_day)),
            ("Rate " + rate_name, "{0}%".format(self._rate())),
            ("Interest", formcurr(intr, currency=trd_curr)),
            ("Interest Rolling Period", 'End of Term' if irp == "0d  " else irp)]

        if self._mmInstype() == 'FDE':
            day_count = acm.Time().DateDifference(self.t.insaddr.exp_day,
                                                  self.t.value_day)
            detailList.insert(2, ("Day Count ", day_count))

        yield mkvalues(*detailList)

        yield mkinfo("THIS IS A COMPUTER-GENERATED DOCUMENT"
                     " AND DOES NOT REQUIRE ANY SIGNATURES.")

    def update_addinfo(self):
        # Update two additional info fields 'Confo Date Sent' and 'Confo Text'
        try:
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_DATE_SENT,
                            at_time.time_now())
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_TEXT,
                            acm.User().Name())
        except:
            acm.Log('Error: Unable to save Confo Date Sent add info timestamp.')

directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory("Y:/Jhb/Operations Secondary Markets/Money Market Ops/MM Confirmations")

ael_gui_parameters = {'windowCaption': 'Money Market Confirmation'}


def ASQL(*_rest):
    acm.RunModuleWithParameters('SAMM_Primary_Confirmation_PDF', 'Standard')  # @UndefinedVariable
    return 'SUCCESS'

ael_variables = AelVariableHandler()


def filter_by_date(fieldValues):
    """Input hook for ael_variables"""
    use_custom_dates = ael_variables[3].value == '1'
    ael_variables[4].enabled = use_custom_dates
    return fieldValues

ael_variables.add(
    'OutputDirectory',
    label='Output Directory',
    cls=directorySelection,
    default=directorySelection,
    alt='The directory where the report(s) will be generated.',
    mandatory=0,
    multiple=1
    )
ael_variables.add(
    'TradeNumber',
    label='Trade Number',
    alt='To run for a specific trade, enter the trade number here.',
    cls='string'
    )
ael_variables.add(
    'TradeFilter',
    label='Trade Filter',
    collection=sorted(f.fltid for f in ael.TradeFilter),
    default='ALL',
    alt='The trade filter title that will be used to create trade rows'
    )
ael_variables.add(
    'filter_by_date',
    label='Custom date',
    collection=[0, 1],
    alt='Check this in order to filter trades by date',
    cls='int',
    hook=filter_by_date
    )
ael_variables.add(
    'Date',
    label='Date',
    default=acm.Time().DateNow(),
    mandatory=0,
    cls='string'
    )
ael_variables.add(
    'merge_files',
    label='Merge files',
    collection=[0, 1],
    alt='Check this in order to merge the generated files',
    cls='int',
    default=1
    )


def _get_dir(outputDirectory, date, instype, txt_date):
    """Returns the directory path, to which the report has to be copied"""
    if instype == at.INST_DEPOSIT:
        directory = os.path.join(outputDirectory, 'Fixed Deposits',
                                 date.strftime('%d %b %y'))
    elif instype == at.INST_CD:
        directory = os.path.join(outputDirectory, 'NCD', txt_date)
    elif instype == at.INST_FRN:
        directory = os.path.join(outputDirectory, 'FRN', txt_date)
    elif instype == at.INST_SECURITY_LOAN:
        directory = os.path.join(outputDirectory, 'SECURITYLOAN', txt_date)

    return directory


def _get_file_name(is_merged, txt_date, cpty_names, trade_nrs):
    """"Generates a file name for the new report"""
    cpty_names = "~".join(cpty_names)
    trade_nrs = "~".join(trade_nrs)

    if is_merged:
        cpty_names = cpty_names[0:min(20, len(cpty_names))]
        trade_nrs = trade_nrs[0:min(20, len(trade_nrs))]

    filename = '{0}_ ({1}) _{2}'.format(cpty_names, trade_nrs, txt_date)

    return filename


def _generate_report(items, date, outputDirectory, instype):
    """Generates a report and copies it to the specified output directory

    items - [(counterparty, xml report, trade number)]
    """

    merge_files = len(items) > 1
    xmls = [item[1] for item in items]
    cpty_names = set(item[0].replace('/', '') for item in items)
    trade_nrs = set(str(item[2]) for item in items)

    txt_date = date.strftime('%Y.%m.%d')
    directory = _get_dir(outputDirectory, date, instype, txt_date)
    filename = _get_file_name(merge_files, txt_date, cpty_names, trade_nrs)

    acm.Log('Generating Report')
    repgen = XMLReport.XMLReportGenerator(directory, 'XMLReport')
    output = repgen.create_merged(xmls, filename)
    startFile(output)
    acm.Log('Generated Report')



def ael_main(parameters):
    outputDir = str(parameters['OutputDirectory'])
    tradeNumber = parameters['TradeNumber']
    tf_name = parameters['TradeFilter']
    date = get_date(parameters['Date'])
    filter_by_date = parameters['filter_by_date']
    merge_files = parameters['merge_files']

    trades = []
    if tradeNumber and tf_name == 'ALL':
        for trd in str(tradeNumber).split(','):
            try:
                trade = acm.FTrade[int(trd)]

                if (trade.Instrument().InsType() in ins_types
                        and trade.Status() in [at.TS_BO_CONFIRMED,
                                               at.TS_BOBO_CONFIRMED]):
                    trades.append(trade)
                else:
                    msg = "Trd:{0}, InsType:{1}, Staus:{2}".format(trd,
                                                                   trade.Instrument().InsType(),
                                                                   trade.Status())
                    acm.Log('Please check trade is valid!')
                    acm.Log(msg)
            except:
                acm.Log('No trades to process')

    if tf_name and not tradeNumber:
        try:
            tf = ael.TradeFilter[tf_name]

            for t in tf.trades():
                if t.insaddr.instype in ins_types:
                    if not filter_by_date or get_date(t.time) == date:
                        trades.append(acm.FTrade[t.trdnbr])
                    else:
                        acm.Log('Please check trade is valid!')
        except:
            acm.Log('Invalid Filter!')

    reports = {}

    for ins_type in ins_types:
        reports[ins_type] = []

    for trade in trades:
        report = ReturnConfirmationReport(trade, date, filter_by_date)
        xml = report.create_report()
        report.update_addinfo()

        instype = trade.Instrument().InsType()
        cpty_name = trade.Counterparty().Fullname()

        item = (cpty_name, xml, trade.Oid())

        if instype in reports:
            reports[instype].append(item)

    for instype, items in list(reports.items()):
        if len(items) == 0:
            continue

        if merge_files:
            _generate_report(items, date, outputDir, instype)
        else:
            for item in items:
                _generate_report([item], date, outputDir, instype)

    acm.Log('Finished')
