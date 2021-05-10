"""
Date                    : 2017-03-28
Purpose                 : Saxo recon
Department and Desk     : Prime Service
Requester               : Eveshnee Naidoo
Developer               : Ondrej Bahounek

Date            CR              Developer               Change
==========      =========       ======================  ===================================================
2017-03-28      4443438         Ondrej Bahounek         ABITFA-4797, ABITFA-4777 - Initial implementation
2020-01-09      FAPE-XX         Iryna Shcherbina        Use default RTB email as the sender
"""

import acm
from at_feed_processing import SimpleCSVFeedProcessor
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_email import EmailHelper
from PB_Saxo_general import (DATE_LIST,
                             DATE_KEYS,
                             get_fund_portf,
                             get_account_alias,
                             get_saxo_instype_alias,
                             get_saxo_type_from_fa_type)


import os, string, datetime
from collections import defaultdict


LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()
TRADING_PORTF = get_fund_portf("")

# Dictionary of funds and their instypes currently currently beeing swept.
# Taken from 'PB_Saxo_sweeping_<alias>_<ins_short>_SERVER' tasks.
# Example of dictionary: [alias] = set('FUT', 'CFD')
FUND_INS_SCHEDULED = None


class MissingFileException(IOError):
    pass


class AbstractChecker(object):

    class CheckerError(Exception):

        def __init__(self, message, info_obj):
            super(AbstractChecker.CheckerError, self).__init__(message)
            self.info_obj = info_obj

    ERROR_MSG = "ERROR"

    def __init__(self, for_date, email_recipients=None):
        self.email_recipients = email_recipients
        self.email_subject = "Saxo recon %s (%s): %s" % (for_date,
            acm.FDhDatabase['ADM'].InstanceName(), self.ERROR_MSG)

    def send_email(self, body):
        email_helper = EmailHelper(
            body,
            self.email_subject,
            self.email_recipients,
        )
        if str(acm.Class()) == "FACMServer":
            email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email_helper.host = EmailHelper.get_acm_host()

        try:
            email_helper.send()
        except Exception as exc:
            LOGGER.error("Error while sending e-mail: %s", exc)

    def _perform_check(self):
        raise NotImplementedError()

    def _format_email_data(self, info_obj):
        raise NotImplementedError()

    def check(self):
        try:
            self._perform_check()
            return True
        except AbstractChecker.CheckerError as exc:
            LOGGER.error(str(exc))
            if self.email_recipients:
                email_data = self._format_email_data(exc.info_obj)
                self.send_email(email_data)


class Checker_NewTrading(AbstractChecker):

    class NewTradingProcessor(SimpleCSVFeedProcessor):

        _col_account_num = "AccountNumber"
        _col_ins_type = "InstrumentType"
        _required_columns = [_col_account_num, _col_ins_type]

        def __init__(self, file_path):
            super(Checker_NewTrading.NewTradingProcessor, self).__init__(file_path, do_logging=False)
            self.fund_trading_dict = defaultdict(set)

        def _process_record(self, record, dry_run):
            (row_nbr, record_data) = record

            alias = get_account_alias(record_data[self._col_account_num])
            if not alias:
                LOGGER.warning(
                    "Alias '%s' not recognised. Skipping row #%d...",
                    record_data[self._col_account_num], row_nbr)
                return

            ins_shortcut = get_saxo_instype_alias(record_data[self._col_ins_type])
            if not ins_shortcut:
                LOGGER.warning(
                    "Instrument type '%s' not recognised. Skipping row #%d...",
                    record_data[self._col_ins_type], row_nbr)
                return
            self.fund_trading_dict[alias].add(ins_shortcut)

        @staticmethod
        def get_fund_trading(file_path):
            proc = Checker_NewTrading.NewTradingProcessor(file_path)
            proc.process(False)
            return proc.fund_trading_dict

    ERROR_MSG = "New trading activity"

    def __init__(self, for_date, file_path, email_recipeints=None):
        super(Checker_NewTrading, self).__init__(for_date, email_recipeints)
        self.fund_ins_dict = Checker_NewTrading.NewTradingProcessor.get_fund_trading(file_path)
        self.fund_ins_scheduled = self._create_fund_ins_sch_dict()

    def _create_fund_ins_sch_dict(self):
        fund_ins_dict = defaultdict(set)
        tasks = acm.FAelTask.Select('name like "PB_Saxo_sweeping_*_SERVER"')
        for task in tasks:
            tsplit = task.Name().split("_")
            # if client's name contains more words (ACU_BLUINK), select both
            fund_name = "_".join(tsplit[3:-2])
            fund_ins_dict[fund_name].add(tsplit[-2])
        return fund_ins_dict

    def is_sweep_scheduled(self, alias, ins_shortcut):
        return ins_shortcut in self.fund_ins_scheduled[alias]

    def _perform_check(self):
        missing = defaultdict(set)
        for fund in self.fund_ins_dict:
            for ins_shortcut in self.fund_ins_dict[fund]:
                if not self.is_sweep_scheduled(fund, ins_shortcut):
                    LOGGER.warning("Fund '%s' started trading new instruments: '%s'", fund, ins_shortcut)
                    missing[fund].add(ins_shortcut)
        if missing:
            raise AbstractChecker.CheckerError(self.ERROR_MSG, missing)

    def _format_email_data(self, input_data_dict):
        msg = "Hello FO and IT, <br /><br />"
        msg += "Some funds have started trading new instrument types.<br /><br />"
        msg += ("Sweeping tasks for these funds and instrument types "
                "need to be scheduled on the backend:<br /><br />")
        for fund in input_data_dict:
            for ins_shortcut in input_data_dict[fund]:
                msg += "<b>{0}</b> : <b>{1} ({2})</b><br />".format(fund,
                    get_saxo_type_from_fa_type(ins_shortcut), ins_shortcut)
        msg += "<br /><br />"
        msg += ("<b>An onboarding process has to be performed for each combination, "
                "starting the day when its first trade occurred.</b><br /><br />")
        msg += "Best regards,<br />{0}".format(
            "CIB Africa TS Dev - Prime and Equities")
        msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
        return msg


class Checker_Mirrors(AbstractChecker):

    BANK_CP = "SAXO BANK AS"
    ERROR_MSG = "MIRROR MISMATCH"

    def __init__(self, the_date, portf_bank, portf_clients, email_recipients=None):
        super(Checker_Mirrors, self).__init__(the_date, email_recipients)
        self.portf_bank = portf_bank
        self.portf_clients = portf_clients

    def _get_trades(self, portf_id, cp_id):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portf_id)
        qor = query.AddOpNode('OR')
        for trd_status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
            qor.AddAttrNode('Status', 'EQUAL', trd_status)
        query.AddAttrNode('Counterparty.Name', 'EQUAL', cp_id)
        return query.Select()

    def _get_cps(self, portf_id, cp_excld_list=None):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portf_id)
        qor = query.AddOpNode('OR')
        for trd_status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
            qor.AddAttrNode('Status', 'EQUAL', trd_status)

        # exclude given counterparties
        for cp_exclude in cp_excld_list:
            query.AddAttrNode('Counterparty.Name', 'NOT_EQUAL', cp_exclude)

        trds = query.Select()
        return set(t.CounterpartyId() for t in trds)

    def _perform_check(self):
        bank_trades = set(t.Oid() for t in self._get_trades(self.portf_bank, self.BANK_CP))
        clients = self._get_cps(self.portf_clients, [self.BANK_CP])

        bank_trds_amnt = len(bank_trades)
        client_trds_amnt = 0
        missing = defaultdict(set)
        for client_id in clients:
            client_trades = self._get_trades(self.portf_clients, client_id)
            client_trds_amnt += len(client_trades)
            for cl_trade in client_trades:
                if (not cl_trade.ContractTrdnbr()) or (cl_trade.ContractTrdnbr() not in bank_trades):
                    missing[client_id].add(cl_trade.Oid())
                    LOGGER.error(("%s: '%s' trade '%d' is not linked to "
                        "any bank trade in portfolio '%s'"),
                        self.ERROR_MSG, client_id, cl_trade.Oid(), self.portf_bank)
        if missing:
            raise AbstractChecker.CheckerError(self.ERROR_MSG, missing)

        LOGGER.info("Amount of bank trades: %d", bank_trds_amnt)
        LOGGER.info("Amount of clients trades: %d", client_trds_amnt)
        if bank_trds_amnt != client_trds_amnt:
            msg = ("%s: Amount of bank trades does not match amount of client trades."
                % self.ERROR_MSG)
            missing[self.BANK_CP].add(msg)
            raise AbstractChecker.CheckerError(msg, missing)

    def _format_email_data(self, input_data):
        msg = "Hello FO and IT, <br /><br />"
        msg += ("There is a mirror trade mismatch between bank portfolio '%s' "
                "and client portfolio '%s'.<br /><br />" % (self.portf_bank, self.portf_clients))
        msg += "These parties have incorrectly mirrored trades:<br /><br />"

        for fund in input_data:
            details = ",".join(str(detail) for detail in input_data[fund])
            msg += "<b>{0}</b>: {1}".format(fund, details)

        msg += "<br /><br />"
        msg += ("<b>Please, correct this immediately since it creates "
            "an operational risk.</b><br /><br />")
        msg += "Best regards,<br />{0}".format(
            "CIB Africa TS Dev - Prime and Equities")
        msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
        return msg


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


ael_variables = AelVariableHandler()
ael_variables.add("date",
                  label="Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("A date for which files will be taken. "
                       "Used for {DATE} template."))
ael_variables.add("custom_date",
                  label="Custom Date",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("A date for which files will be taken. "
                       "Used for {DATE} template. "
                       "Format: '2016-09-30'."))

ael_variables.add("check_new_trading",
                  label="Check New Trading?_New Trading",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add("file_dir",
                  label="Directory_New Trading",
                  default=r"y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\SAXO\${DATE}",
                  alt=("Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add("trading_activity_file",
                  label="Trading Activity filename_New Trading",
                  default="TradesExecuted_${DATE}.csv",
                  alt=("Path template to the trades executed input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format DD-MM-YYYY). "
                       "It can also be absolute path."))
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default="Eveshnee.Naidoo@absacapital.com,CIBAfricaTSDevPrime@internal.barclayscapital.com",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma separated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))

ael_variables.add("check_mirrors",
                  label="Check Correct Mirrors?_Mirroring",
                  cls="bool",
                  collection=(True, False),
                  default=False)
ael_variables.add("portf_bank",
                  label="Bank Portfolio_Mirroring",
                  cls="FPhysicalPortfolio",
                  default=TRADING_PORTF,
                  mandatory=True,
                  alt=("Bank trrading portfolio (mirror to Client Portfolio)."))
ael_variables.add("portf_clients",
                  label="Client Portfolio_Mirroring",
                  cls="FPhysicalPortfolio",
                  default=TRADING_PORTF,
                  mandatory=True,
                  alt=("Client trrading portfolio (mirror to the Bank Portfolio)"))


def get_input_date(ael_dict):
    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = DATE_LIST[ael_dict['date']]
    return the_date


def get_file_path(ael_dict, var_file_name):

    the_date = get_input_date(ael_dict)

    # file date will be converted to "dd-mm-YYYY"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    file_date_string = _dt.strftime("%d-%m-%Y")
    dir_date_string = the_date

    # filename in string
    file_name = ael_dict[var_file_name]
    fname_template = string.Template(file_name)
    file_name = fname_template.substitute(DATE=file_date_string)
    if os.path.exists(file_name):
        return file_name

    # directory in string
    file_dir = ael_dict["file_dir"]
    fdir_template = string.Template(file_dir)
    file_dir = fdir_template.substitute(DATE=dir_date_string)

    file_path = os.path.join(file_dir, file_name)

    if not os.path.exists(file_path):
        raise MissingFileException(file_path)
    return file_path


def ael_main(ael_dict):
    the_date = get_input_date(ael_dict)
    email_recipients = list(ael_dict["email_recipients"])

    LOGGER.info("Running recons...")
    LOGGER.info("Recon date: %s", the_date)

    result_ok = True
    if ael_dict["check_new_trading"]:
        LOGGER.info("*" * 64)
        LOGGER.info("Running %s check...", Checker_NewTrading.ERROR_MSG)
        file_path = get_file_path(ael_dict, "trading_activity_file")
        checker = Checker_NewTrading(the_date, file_path, email_recipients)
        result_ok = result_ok and checker.check()

    if ael_dict["check_mirrors"]:
        LOGGER.info("*" * 64)
        LOGGER.info("Running %s check...", Checker_Mirrors.ERROR_MSG)
        checker = Checker_Mirrors(the_date, ael_dict["portf_bank"].Name(),
            ael_dict["portf_clients"].Name(), email_recipients)
        result_ok = result_ok and checker.check()

    if result_ok:
        LOGGER.info("Completed successfully.")
    else:
        raise RuntimeError("Errors occurred.")
