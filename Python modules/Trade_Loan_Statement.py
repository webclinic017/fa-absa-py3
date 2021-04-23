'''
developer               date            change #        description
Evgeniya Baskaeva       08/11/2016      CHNG0003774716  Created.
Willie vd Bank          05/12/2017      CHNG0005202968  Redeploying change after it was rolled back
                                                        Added email functionality
Willie vd Bank          27/03/2018      CHG1000304907   Modified so that valid parties are identified through
                                                        the add_info called Trd_Loan_Statement on the contact
                                                        Modified the interest rate to use the rate on the instrument
Willie vd Bank          19/06/2018      CHG1000568752   Modified so that the recipient email address is retrieved from
                                                        the counterparty static
Willie vd Bank          27/09/2018      CHG1000912390   Fixed a formatting issue with the email addresses
                                                        Also modified the scheduled task so that all statements are sent to clients directly.
'''

import os
from datetime import datetime
import ael
import acm
from XMLReport import contact_from_pty, mkinfo, mktable
import XMLReport
from at_ael_variables import AelVariableHandler
from zak_funcs import formcurr
import at_logging
LOGGER = at_logging.getLogger()
from at_email import EmailHelper

TODAY = acm.Time().DateToday()
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
FIRSTDAYOFPREVMONTH = acm.Time().DateAddDelta(TODAY, 0, -1, 0)

SPACE_COL = acm.Calculations().CreateStandardCalculationsSpaceCollection()

CF_TYPE_LIST = [
    'Fixed Amount',
    'Interest Reinvestment',
    'Fixed Rate',
    'Float Rate',
    'Call Fixed Rate',
    'Call Float Rate',
    'Call Fixed Rate Adjustable',
    'Fixed Rate Adjustable',
    'Balance',
]

ZAR = 'ZAR'


class Report(XMLReport.StatementReportBase):
    def __init__(self, party, acquirers, zar_only,
                 start_day, end_day):
        self.party = party
        self.acquirers = acquirers
        self.zar_only = zar_only
        self.start_day = start_day
        self.end_day = end_day
        self.calc_space = acm.Calculations().CreateCalculationSpace(
            'Standard',
            'FPortfolioSheet'
        )
        self.calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss Start Date',
            'Custom Date'
        )
        self.calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss Start Date Custom',
            self.start_day
        )
        self.calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss End Date',
            'Custom Date'
        )
        self.calc_space.SimulateGlobalValue(
            'Portfolio Profit Loss End Date Custom',
            self.end_day
        )

    def client_address(self):
        return contact_from_pty(self.party)

    def statement_detail(self):
        eod = self.end_day.to_string("%d %B %Y")
        tod = datetime.strptime(TODAY, '%Y-%m-%d').strftime("%d %B %Y")
        col1 = 'Trade Loans Statement as at {0}'.format(eod)
        col2 = 'Issue date: {0}'.format(tod)
        cols = [
            {'name': col1,
             'width': '73%'},
            {'name': col2,
             'width': '27%'},
        ]

        yield mktable(cols, [], borderwidth='0')

        cols = [
            {'name': 'REFERENCE',
             'width': '2.0cm'},
            {'name': 'NOMINAL AMOUNT',
             'width': '3.0cm'},
            {'name': 'START DATE',
             'width': '2.0cm'},
            {'name': 'MATURITY DATE',
             'width': '2.0cm'},
            {'name': 'INTEREST RATE',
             'width': '2.0cm'},
            {'name': 'INTEREST',
             'width': '3.0cm'},
            {'name': 'MATURITY VALUE',
             'width': '3.0cm'}
        ]
        yield mktable(cols, self.get_table_rows())

        inf = '''We trust the above information corresponds with your records. 
                 Upon receipt hereof, kindly review this statement and 
                 notify us of any errors or discrepancies within 30 (thirty) 
                 days of this statement date.'''
        yield mkinfo(inf)

    def cur_ok(self, cur):
        return (cur.Name() == ZAR and self.zar_only) or \
               (cur.Name() != ZAR and not self.zar_only)

    def acq_ok(self, acq):
        return acq and acq in self.acquirers

    def get_table_rows(self):
        TALTrades = []
        trades = acm.FTrade.Select('counterparty = {0}'.format(self.party.Oid()))
        sum_nominal = 0
        sum_interest = 0
        sum_maturity = 0
        for tr in trades:
            cur = tr.Currency()
            acq = tr.Acquirer()
            if self.cur_ok(cur) and self.acq_ok(acq):
                ed = tr.Instrument().ExpiryDate()
                try:
                    exp_date = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    # skip trade: exp_date not set
                    continue
                start_day = datetime.strptime(str(self.start_day), '%Y-%m-%d')
                if exp_date > start_day and tr not in TALTrades:
                    legs = tr.Instrument().Legs()
                    cfs = legs[0].CashFlows()
                    cashflows = filter(
                        lambda cf: cf.CashFlowType() in CF_TYPE_LIST, cfs
                    )
                    if cashflows:
                        row = self.get_row(tr)
                        if row:
                            sum_nominal += row[1]
                            sum_interest += row[5]
                            sum_maturity += row[6]
                            yield self.get_formatted_row(row, cur.Name())

        yield ['', '', '', '', '', '']
        yield [
           'TOTAL',
           formcurr(sum_nominal),
           '',
           '',
           '',
           formcurr(sum_interest),
           formcurr(sum_maturity),
        ]

    def get_formatted_row(self, row, currency):
        trdnbr, nominal, value_day, exp_day, price, total_interest, mat_val = row
        f = '%d/%m/%Y'
        value_day = datetime.strptime(value_day, '%Y-%m-%d').strftime(f)
        exp_day = datetime.strptime(exp_day, '%Y-%m-%d %H:%M:%S').strftime(f)
        return [
            trdnbr,
            formcurr(nominal, currency=currency),
            value_day,
            exp_day,
            "{0:.3f}%".format(price),
            formcurr(total_interest, currency=currency),
            formcurr(mat_val, currency=currency),
        ]

    def get_row(self, tr):
        instr = tr.Instrument()
        calc_space = self.calc_space
        pai = calc_space.CalculateValue(tr, 'Portfolio Accrued Interest').Value().Number()
        psi = calc_space.CalculateValue(tr, 'Portfolio Settled Interest').Value().Number()
        total_interest = pai + psi
        if total_interest:
            if instr.InsType() in ('Deposit'):
                nominal_amount = abs(tr.Nominal())
                exp_date = instr.ExpiryDate()
                calc = tr.Calculation()
                set_int = calc.SettledInterest(SPACE_COL, self.start_day,
                                               exp_date, None, None, 3).Number()
                mat_val = nominal_amount + abs(set_int)
                return [
                    tr.Oid(),
                    nominal_amount,
                    tr.ValueDay(),
                    exp_date,
                    instr.Legs()[0].FixedRate(),
                    total_interest,
                    mat_val
                ]


class TDMNResult(object):
    def __init__(self):
        self.output_pdf = ''
        self.filename = ''


def _get_contact_csv(party, filename):
    text = '''File_Path,Contact_Method,Contact_Person,Contact_Detail1,
              Contact_Detail2,Contact_Detail3\n'''
    contacts = party.contacts()
    contacttype = party.add_info('Interest Statement')
    # Counterparty Contacts:
    customer_contact = ''
    contact_detail = []

    for c in contacts:
        contact_rule = ael.ContactRule.select('contact_seqnbr = %d' % c.seqnbr)
        for cr in contact_rule:
            choice_list = cr.event_chlnbr
            if choice_list and choice_list.entry == 'Interest Statement':
                customer_contact += c.attention + '\\ '
                if contacttype == 'Email':
                    contact_detail.append(c.email)
                elif contacttype == 'Fax':
                    contact_detail.append(c.fax)
    if contacttype in ('None', ''):
        i = 'Party additional_info(Interest Statement) is blank or None!'
        LOGGER.info(i)
    else:
        t = [filename + ".pdf", contacttype, customer_contact]
        text += ','.join(t + contact_detail[:3])

    return text


def _gen_report(party, acquirers, zar_only,
                start_date, end_date, output_path, email, email_address):
    party_name = party.Name().replace('/', ' ')
    ed = end_date.to_string('%d %B %Y')
    filename = "FTDMIS{0}_{1}_{2}".format(party_name, '', ed)

    pdf_dir = os.path.join(output_path, 'PDF')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        LOGGER.info('Folder ' + pdf_dir + ' created.')
    
    report = Report(party, acquirers, zar_only, start_date, end_date)
    xml_file = report.create_report()
    gen = XMLReport.XMLReportGenerator(pdf_dir, 'XMLReport')
    result = gen.create(xml_file, filename)

    tdmn_result = TDMNResult()
    tdmn_result.output_pdf = result
    tdmn_result.filename = filename

    #LOGGER.info('Created: ' + result)
    print
    if email:
        _send_emails(tdmn_result, email_address)
    
    LOGGER.info('Done... {0}'.format(party_name))


def _send_emails(tdmn_result, email_address):
    mail_to = email_address     #must be a list of string items
    attachments = [tdmn_result.output_pdf]
    #print("Email will be send to: {0}, with attachments: {1}".format(mail_to, attachments))
    mail_cc = []                #must be a list of string items
    body = ''
    subject = 'Front Arena Trade Loan Statement'
    mail_from = 'dbntrade@absa.co.za' #will be set to the outlook owner
    email = EmailHelper(body, subject, mail_to, mail_from, attachments, mail_cc=mail_cc)
    # Use outlook to send email from front end
    # Use SMTP to send email from back end
    if str(acm.Class()) == "FACMServer":
        email.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email.host = EmailHelper.get_acm_host()
    email.send()


def custom_dates(fieldValues):
    """Input hook for ael_variables"""
    use_custom_dates = ael_variables[1].value
    ael_variables[2].enabled = use_custom_dates
    ael_variables[3].enabled = use_custom_dates
    return fieldValues
    
def send_email(fieldValues):
    """Input hook for ael_variables"""
    send_emails = ael_variables[5].value
    ael_variables[6].enabled = send_emails
    ael_variables[7].enabled = ael_variables[6].value
    ael_variables[8].enabled = ael_variables[6].value
    return fieldValues

def adhoc_email_address(fieldValues):
    """Input hook for ael_variables"""
    send_emails = ael_variables[6].value
    ael_variables[7].enabled = send_emails
    ael_variables[8].enabled = send_emails
    return fieldValues
    
def get_parties():
    parties = {}
    contacts = acm.FContact.Select('')
    for c in contacts:
        if c.AdditionalInfo().Trd_Loan_Statement():
            key = c.Party()
            if parties.has_key(key):
                parties[key] += ',' + c.Email()
            else:
                parties[key] = c.Email()
    return parties
        
ael_variables = AelVariableHandler()
ael_variables.add(
    "acquirers",
    label="Acquirer",
    multiple=True,
    cls=acm.FParty,
)
ael_variables.add_bool(
    'custom_dates',
    label='Custom dates',
    alt='Check this in order to use custom from and to dates',
    hook=custom_dates,
    default=False,
)
ael_variables.add(
    'start_date',
    label='Start date',
    default=FIRSTDAYOFPREVMONTH,
)
ael_variables.add(
    'end_date',
    label='End date',
    default=TODAY,
)
ael_variables.add(
    'path',
    label='Output folder',
    default=r'c:\tmp',
    alt='The directory to which the file will be dropped.',
)
ael_variables.add_bool(
    'send_email',
    label='Send email',
    alt='Check this in order to email the statements',
    hook=send_email,
)
ael_variables.add_bool(
    'adhoc_email_address',
    label='Ad hoc email address',
    alt='Check this in order to email the statements to an ad hoc address',
    hook=adhoc_email_address,
)
ael_variables.add(
    'email_address',
    label='Email adress',
    alt='The directory to which the file will be dropped.',
)
#The following parameter should be removed once business is happy with the functionality in prod
ael_variables.add(
    'custom_parties',
    label='Ignore ad hoc email address override',
    alt='List the counterpaties for which the ad hoc email address override should be ignored or leave blank.',
    multiple=True,
    cls=acm.FParty,
    mandatory=False,
)

def ael_main(argv):
    acm.Log("Starting {0}".format(__name__))

    path = argv['path']
    start_date = ael.date(FIRSTDAYOFPREVMONTH)
    end_date = ael.date(TODAY)
    zar_only = True
    custom_dates = argv['custom_dates']
    if custom_dates:
        start_date = ael.date(argv['start_date'])
        end_date = ael.date(argv['end_date'])

    if not os.access(path, os.W_OK):
        i = 'Output path is not writable! Client valuation not generated!'
        LOGGER.warning(i)
        return

    parties = get_parties()
    acquirers = argv['acquirers']
    email = argv['send_email']
    adhoc_email_address = argv['adhoc_email_address']
    
    custom_parties = argv['custom_parties']
    
    for party in parties:
        email_address = argv['email_address'].split(',')
        if not adhoc_email_address or party in custom_parties:
            email_address = parties[party].split(',')
        _gen_report(party, acquirers, zar_only,
                    start_date, end_date, path, email, email_address)
