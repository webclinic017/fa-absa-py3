"""Decommission platypus and move all existing reports using it to FOP"""
# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    Aaeda Salejee    Ickin Vural            C000000697493, ABITFA-569
# Decommission platypus and move all existing reports using it to FOP

# OPS    Miguel da Silva  Jaysen Naicker         768545
# Change outfile name to start with Call instead of FRN

# OPS    Molemo Masuku    Willie van der Bank    469612 2012-09-21
# Added counterparty settlement account details

# OPS    ?                Anwar Banoo            736861
# Corrected list index issue with error thrown when splitting account into branch and account number

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS     Sipho Ndlalane   Sinethemba Saul         CHNG0001027597
# Added code to update two additional info fields

# OPS Sipho Ndlalane    Sanele Macanda        CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions

# OPS Sipho Ndlalane    Andrei Conicov       CHNG0001849553 ABITFA - 2365 (18/03/2014)
# Fixed the currency symbol and the default output path

# OPS Sipho Ndlalane    Bhavnisha Sarawan    CHNG0001849553 - ABITFA - 1815 (18/03/2014)
# Changed the account selection from the cashflow to the settlement to cater for manual account adjustments


from SAGEN_IT_Functions import startFile
from XMLReport import mkinfo, mkcaption, mkvalues
from zak_funcs import formcurr
import STATIC_TEMPLATE
import XMLReport
import acm
import ael
import at
import copy
import os
import time


class Report(XMLReport.StatementReportBase):

    def __init__(self, trade, cashflow):
        self.trade = trade
        self.cashflow = cashflow
        self.amount = trade.Quantity() * cashflow.FixedAmount()

    def _intRate(self):
        check_date = self.cashflow.StartDate() or self.cashflow.PayDate()

        leg = self.trade.Instrument().Legs()[0]
        if check_date == acm.Time.DateNow():
            return '%.4f' % leg.FixedRate()
        else:
            for c in leg.CashFlows():
                if c.CashFlowType() == 'Call Fixed Rate Adjustable':
                    for r in c.Resets():
                        if r.StartDate() <= check_date and r.EndDate() > check_date:  # should be YYYY-MM-DD therefore fine
                            return '%.4f' % r.FixingValue()

        return 0.0

    def bank_address(self):
        addr = copy.copy(STATIC_TEMPLATE.ADDRESS_ALICELANE)
        addr['name'] = 'PCG Client Services'
        addr['tel'] = '+27 (0)11 895 7425 / 7597 / 6750'
        addr['fax'] = '+27 (0)11 895 6922'
        addr['email'] = 'mmconfirmations@absacapital.com'

        return addr

    def client_address(self):
        return XMLReport.contact_from_pty(self.trade.Counterparty())

    def statement_detail(self):

        yield mkcaption('THE FOLLOWING TRANSACTION WAS APPLIED TO YOUR ACCOUNT:')

        if self.amount < 0:
            ttype = 'COUNTERPARTY RECEIVES'
        elif self.amount > 0:
            ttype = 'COUNTERPARTY PAYS'
        else:
            ttype = 'NO TRANSFER'

        trd_curr = self.trade.Currency().Name()
        yield mkvalues(["ACCOUNT TYPE", self.trade.AdditionalInfo().Funding_Instype()],
                       ["CALL ACCOUNT NUMBER", self.trade.Instrument().Name()],
                       ["TRANSACTION TYPE", ttype],
                       ["TRADE NUMBER:", self.trade.Name()],
                       ["TRANSACTION VALUE DATE:", self.cashflow.StartDate() or self.cashflow.PayDate() or ''],
                       ["TRANSACTION AMOUNT:", formcurr(abs(self.amount), currency=trd_curr)],
                       ["ACCOUNT INTEREST RATE:", str(self._intRate()) + " %"])

        if self.amount < 0:
            settlement = acm.FSettlement.Select('cashFlow = %i' % (self.cashflow.Oid()))
            for s in settlement:
                if s.Parent() == None:
                    accnbr = s.CounterpartyAccount().split(' ')
                    yield mkvalues(["CORRESPONDENT BANK:", s.TheirCorrBank()],
                                   ["ACCOUNT NAME:", s.CounterpartyAccName()],
                                   ["ACCOUNT NUMBER:", accnbr[1] if len(accnbr) > 1 else accnbr[0]],
                                   ["BRANCH CODE:", accnbr[0]])

        yield mkinfo("ABSA BANK TREASURY DETAILS ARE AS FOLLOWS:",
               "Branch: Eloff Street Johannesburg",
               "Account Number: 660 000 135",
               "Branch Code: 632 505",
               "THIS IS A COMPUTER-GENERATED DOCUMENT AND DOES NOT REQUIRE ANY SIGNATURES.")

    def update_addinfo(self):
        # Update two additional info fields 'Confo Date Sent' and 'Confo Text'
        try:
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_DATE_SENT,
                            str(acm.Time.TimeNow()))
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_TEXT,
                            ael.user().name)
        except:
            acm.Log('Error: Additional Info fields could not be updated')


today = acm.Time().DateNow()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory(r'Y:\Jhb\Operations Secondary Markets\Money Market Ops\MM Confirmations\Call Accounts Confirmations')
ael_gui_parameters = {'windowCaption': 'Money Market Confirmation'}


def ASQL(*rest):
    acm.RunModuleWithParameters('SAMM_Call_Dep_Loan_Confo_PDF', 'Standard')  # @UndefinedVariable
    return 'SUCCESS'

ael_variables = [
                    ['OutputDirectory', 'Output Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
                    ['TradeNumber', 'Trade Number', 'string', None, None, 0, 0, 'To run for a specific trade, enter the trade number here.', None, 1],
                    ['CashFlowNbr', 'Cash Flow Number', 'string', None, 'ALL', 0, 0, 'To run for a specific cash flow, enter the cash flow number here.', None, 1],
                    ['Date', 'Date', 'string', today, today, 1]]


def ael_main(parameters):
    
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
    
    outputDirectory = parameters['OutputDirectory']
    date = parameters['Date']
    trades_cashflows = _filter_trd_cashflows(parameters['TradeNumber'],
                                                parameters['CashFlowNbr'],
                                                date)
    
    directory = os.path.join(str(outputDirectory), ael.date_today().to_string('%d.%b.%Y'))
    
    if not os.path.exists(str(directory)):
        try:
            os.mkdir(directory)
        except:
            msg = ("The provided output directory '{0}'" 
            "does not exist and could not be created.".format(str(directory)))
            warning_function("Error", msg, 0)
            return
    
    if not os.access(str(directory), os.W_OK):
        msg = ("The provided output directory '{0}'" 
            "is not writeable.".format(str(directory)))
        warning_function("Error", msg, 0)
        return
    
    # Transform all trades and cashflows from trades_cashflows to xmls
    xmls = []
    for trade, cashflow in trades_cashflows:
        report = Report(trade, cashflow)
        xmls.append(report.create_report())
        report.update_addinfo()

    # Merge all pdfs into one report
    
    gen = XMLReport.XMLReportGenerator(directory, 'XMLReport')
    output = gen.create_merged(xmls, 'Call Confirmation {0}'.format(time.ctime().replace(':', '')))

    acm.Log("Report written to {0}".format(output))
    startFile(output)


def _filter_trd_cashflows(trd_nrs, cashflow_nrs, date):
    """Filter input values from GUI and return [trade, cashflow] pairs."""

    trades = [acm.FTrade[int(tn)] for tn in trd_nrs.split(',') if tn]
    trades_cashflows = []

    # Cashflows are 'ALL' and there are trade numbers
    if trades and cashflow_nrs == 'ALL':
        for trade in trades:
            if (trade.Instrument().InsType() == 'Deposit'
                and trade.Status() in ['BO Confirmed', 'BO-BO Confirmed']):

                for cf in trade.Instrument().Legs()[0].CashFlows():
                    if cf.CashFlowType() == 'Fixed Amount':
                        if date in [cf.StartDate(), cf.PayDate()]:
                            trades_cashflows.append([trade, cf])
            else:
                acm.Log('Warning! Please check trade is valid!')

    # There are cashflow numbers but not trade numbers
    if not trd_nrs and cashflow_nrs and cashflow_nrs != 'ALL':
        cashflows = []
        
        for cashflow in cashflow_nrs.split(','):
            if acm.FCashFlow[int(cashflow)]:
                cashflows.append(acm.FCashFlow[int(cashflow)])
            else:
                acm.Log('Warning! Please check cash flow {0} is valid!'.format(cashflow))
        
        for cashflow in cashflows:
            trade = cashflow.Leg().Instrument().Trades()[0]

            if cashflow.CashFlowType() == 'Fixed Amount':
                trades_cashflows.append([trade, cashflow])
            else:
                acm.Log('Warning! Please check cash flow {0} is of a Fixed Amount type!'.format(cashflow.Oid()))

    if not trades_cashflows:
        acm.Log("Warning! Please set either trade numbers (and set cashflows to ALL) "
                "or cashflows (and leave trade numbers empty).")

    return trades_cashflows
