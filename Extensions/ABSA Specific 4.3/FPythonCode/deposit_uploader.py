"""
Description             : Booking tool for the GRP TREASURY and Money Markets desks based on different excel sheets
Department and Desk     : GRP TREASURY and Money Markets
Requester               : Karin Nieuwoudt
Developer               : Shalini Lala
JIRA                    : FAFO-42_Deposit_uploader_revised
JIRA                    : FAFO-49_Deposit uploader - fix + additional functionality
JIRA					: ARR-71 Added three more clients to the uploader
"""

import acm
import FRunScriptGUI
import FUxCore
import xlrd
from FUploaderUtils import CreateOutput
import os
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
from at_logging import getLogger
import FCallDepositFunctions
import hashlib
from collections import OrderedDict

DIALOG_FUNC = acm.GetFunction('msgBox', 3)
LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
DATE = acm.Time().DateToday()

BLUECOLOR = acm.UX().Colors().Create(222, 235, 255)
REDCOLOR = acm.UX().Colors().Create(195, 31, 0)
GREENCOLOR = acm.UX().Colors().Create(30, 170, 30)


def start_dialog(eii):
    # Callback from menu extension to start the main dialog
    shell = eii.ExtensionObject().Shell()
    builder = CreateLayout()
    sc_dialog = CreateUploaderLayout()

    return acm.UX().Dialogs().ShowCustomDialog(shell, builder, sc_dialog)


def amount_format(amount, separator=True):
    if separator:
        new_amount = '{:,}'.format(amount)
    else:
        new_amount = float(''.join(n for n in amount if n.isdigit() or n in ('-', '.')))
    return new_amount


def get_transaction(deposit, withdrawal, type, excel_amount):
    amount = "N/A"

    if excel_amount:
        number = excel_amount
    else:
        number = deposit if deposit else withdrawal
    try:
        # reformatting of data to remove special characters in amount column from spreadsheet whilst retaining characters '.', '-' and ','
        formatted_number = ''.join(n for n in number if n.isdigit() or n in ('-', '.', ','))
    except:
        formatted_number = number

    transaction_type = "N/A"
    if type:
        if type.upper() in ["CALL", "WITHDRAW", "TAKE OFF CALL", "WITHDRAWAL"]:
            withdrawal = float(formatted_number)
        elif type in ["PLACE", "PLACE ON CALL", "DEPOSIT"]:
            deposit = float(formatted_number)

    if deposit and deposit != '' and deposit != 0:
        amount = float(formatted_number)
        transaction_type = "DEPOSIT"
    elif withdrawal and withdrawal != '' and withdrawal != 0:
        amount = float(formatted_number)
        if amount > 0:
            amount = amount * -1
        transaction_type = "WITHDRAWAL"

    return amount, transaction_type


def set_reversal_grid_data(selected):
    record = selected.GetData()

    if record.At('status') == 'POSTED':
        reverse_amount = -1 * amount_format(record.At('amount'), False)
        reverse = 'TRUE'
        new_status = 'OK'

        try:
            cashflow = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
            cashflow.AddAttrNode('Leg.Instrument.Name', 'EQUAL', record.At('instrument'))
            cashflow.AddAttrNode('CreateTime', 'GREATER_EQUAL', acm.Time().DateToday())
            cashflow.AddAttrNode('AdditionalInfo.MM_Hash', 'EQUAL', record.At('hash'))
            id = cashflow.Select()[0].Oid()
        except:
            raise Exception('Original cash flow not found.')

        record.AtPut('status', new_status)
        record.AtPut('reverse', reverse)
        record.AtPut('reverse_amount', amount_format(reverse_amount))
        record.AtPut('id', id)

        selected.Label(record.At('status'), 5)
        selected.Label(record.At('reverse'), 6)
        selected.Label(record.At('reverse_amount'), 7)
        selected.Label(record.At('id'), 8)

        selected.SetData(record)


class CreateUploaderLayout(FUxCore.LayoutDialog):
    COLUMNS = ['Code', 'Trade', 'Instrument', 'Balance', 'Amount', 'Status', 'Reverse', 'Reverse Amount',
               'Cash Flow ID']
    COLUMNS_1 = ['Code', 'Trade', 'Instrument', 'New Balance', 'Amount Booked']

    def HandleCreate(self, dlg, layout):
        # Runs when the GUI is being created
        self._fux_dlg = dlg
        self._fux_dlg.Caption('Cash Flow Bookings')
        self._fux_dlg.SetBackgroundColor(BLUECOLOR)
        self._shell = dlg.Shell()

        self.input_file = layout.GetControl("input_file")

        self.select_file_button = layout.GetControl("select_file")
        self.select_file_button.AddCallback("Activate", self.on_select_file_button_pressed, None)

        self.reverse_check_button = layout.GetControl("reverse_check")

        self.reverse_check_button_1 = layout.GetControl("reverse_check_1")
        self.reverse_check_button_1.AddCallback("Activate", self.on_select_all_to_reverse, None)

        self.client_name_dropdown = layout.GetControl("client_name")
        self.client_name_dropdown.Populate(filenames_map.keys())

        self.upload_cashflows_button = layout.GetControl("upload_cashflows")
        self.upload_cashflows_button.AddCallback("Activate", self.on_upload_cashflows_button_pressed, None)

        self.action = layout.GetControl('action')
        self.action.SetColor("Text", REDCOLOR)
        self.action.SetStandardFont("Bold")

        self.unprocessed = layout.GetControl("cashflows_to_upload")
        self.unprocessed.ShowGridLines()
        self.unprocessed.ShowColumnHeaders()
        self.unprocessed.EnableMultiSelect(True)
        self.unprocessed.AddColumn(self.COLUMNS)
        self.unprocessed.Editable(True)
        self.unprocessed.AddCallback('DefaultAction', self.on_double_click, None)

        self.processed = layout.GetControl("cashflows_uploaded")
        self.processed.ShowGridLines()
        self.processed.ShowColumnHeaders()
        self.processed.EnableMultiSelect(True)
        self.processed.AddColumn(self.COLUMNS_1)
        self.processed.Editable(True)

        self.process_cashflows_button = layout.GetControl("process_cashflows")
        self.process_cashflows_button.AddCallback("Activate", self.on_process_cashflows_button_pressed, None)

        self.total_deposits = layout.GetControl('total_deposits')
        self.total_deposits.SetColor("Text", GREENCOLOR)

        self.total_withdrawals = layout.GetControl('total_withdrawals')
        self.total_withdrawals.SetColor("Text", REDCOLOR)

        self.total = layout.GetControl('total')

    def HandleApply(self):
        return True

    def on_select_file_button_pressed(self, *args):
        # Runs for select file
        path, filename = os.path.split(self.input_file.GetData())
        selection = acm.FFileSelection()
        selection.SelectedDirectory(r"{0}".format(path))
        selection.PickDirectory(False)
        selection.PickExistingFile(True)
        if acm.UX().Dialogs().BrowseForFile(self._fux_dlg.Shell(), selection):
            self.input_file.SetData(selection.SelectedFile().Text())

    def on_upload_cashflows_button_pressed(self, *args):
        # Runs for upload cashflows
        self.unprocessed.RemoveAllItems()
        self.processed.RemoveAllItems()
        self.reverse_check_button.SetCheck(0)
        self.reverse_check_button_1.SetCheck(0)
        self.total_deposits.SetData('')
        self.total_withdrawals.SetData('')
        self.total.SetData('')
        file_path = self.input_file.GetData()
        reverse = self.reverse_check_button.Checked()
        client = self.client_name_dropdown.GetData()
        proc = ProcessXLSFileData(file_path, client)
        proc.add_error_notifier(notify_log)
        self.action.SetData('LOADING...')
        try:
            proc.process(False)
        except Exception as e:
            message = 'Incorrect file format.'
            DIALOG_FUNC('Error', message, 0)
            self.client_name_dropdown.SetData('')
            self.action.SetData('')
            raise Exception("Unable to read data for: %s" % dict, e)

        records = proc.records

        for r in records:
            r['instrument'] = acm.FInstrument[r['instrument']].Name() if acm.FInstrument[r['instrument']] else "N/A"
            if r['status'] not in ["MISSING", "MULTIPLE TRADES"]:
                new_balance = r['amount'] + r['balance']
                r['amount'] = amount_format(r['amount'])
                r['balance'] = amount_format(r['balance'])
            else:
                new_balance = r['balance']

            cashflow_data = []
            cashflow_data.extend(
                [r['code'], r['trade'], r['instrument'], r['balance'], r['amount'], r['status'], r['reverse'],
                 r['reverse_amount'], r['id'], new_balance])

            root = self.unprocessed.GetRootItem()
            child = root.AddChild()
            for i, item in enumerate(cashflow_data):
                child.Label(item, i)
            child.SetData(r)

        self.client_name_dropdown.SetData('')
        self.action.SetData('')

    def on_select_all_to_reverse(self, *args):
        self.action.SetData('LOADING...')
        self.unprocessed.SelectAllItems(True)
        all = self.unprocessed.GetSelectedItems()

        for selected in all:
            set_reversal_grid_data(selected)

        self.unprocessed.SelectAllItems(False)
        self.action.SetData('')

    def on_double_click(self, *args):
        self.action.SetData('LOADING...')
        selected = self.unprocessed.GetSelectedItem()

        set_reversal_grid_data(selected)

        self.action.SetData('')

    def on_process_cashflows_button_pressed(self, *args):
        # Runs for process cashflows
        LOGGER.info("------------------------- Cash Flows for pay date: %s -------------------------" % DATE)
        deposits = 0
        withdrawals = 0

        self.processed.RemoveAllItems()

        root_item = self.unprocessed.GetRootItem()
        root = self.processed.GetRootItem()

        self.action.SetData('PROCESSING...')

        for i, child in enumerate(root_item.Children()):
            record = {}
            cashflow = child.GetData()
            if cashflow.At('status') == "OK":
                if cashflow.At('reverse') == "TRUE" and (
                        self.reverse_check_button.Checked() == True or self.reverse_check_button_1.Checked() == True):
                    amount = amount_format(cashflow.At('reverse_amount'), False)
                    status = 'REVERSED'
                    balance = cashflow.At('new_balance') + amount
                else:
                    amount = amount_format(cashflow.At('amount'), False)
                    status = 'POSTED'
                    balance = cashflow.At('new_balance')

                LOGGER.info("Client Code: %s" % cashflow.At('code'))
                LOGGER.info("Call account: %s" % cashflow.At('instrument'))
                LOGGER.info("Amount: %s" % amount)
                LOGGER.info("Balance: %s" % str(balance))

                try:
                    cashFlow = FCallDepositFunctions.adjust(acm.FInstrument[cashflow.At('instrument')], float(amount),
                                                            acm.Time().DateToday(), None, None, None, 1, None)
                    cashFlow.AddInfoValue('MM_Hash', cashflow.At('hash'))
                    cashFlow.AddInfoValue('Settle_Type', 'Reverse' if (
                            self.reverse_check_button.Checked() == True or self.reverse_check_button_1.Checked() == True) else 'Settle')
                    cashFlow.AddInfoValue('Reversed_CF_Ref', cashflow.At('id') if (
                            self.reverse_check_button.Checked() == True or self.reverse_check_button_1.Checked() == True) else '')
                    cashFlow.Commit()

                    if float(amount) > 0:
                        deposits += float(amount)
                    else:
                        withdrawals += float(amount)

                    cashflow.AtPut('status', status)
                    child.Label(cashflow.At('status'), 5)

                    record['code'] = cashflow.At('code')
                    record['trade'] = cashflow.At('trade')
                    record['instrument'] = cashflow.At('instrument')
                    record['balance'] = amount_format(record['balance'])
                    record['amount'] = amount_format(amount)
                    booked_cashflow = [record['code'], record['trade'], record['instrument'], record['balance'],
                                       record['amount']]

                    child = root.AddChild()
                    for i, item in enumerate(booked_cashflow):
                        child.Label(item, i)
                    child.SetData(record)


                except Exception as e:
                    LOGGER.exception('ERROR on %s ' % cashflow.At('instrument'), e)

        self.total_deposits.SetData(amount_format(deposits))
        self.total_withdrawals.SetData(amount_format(withdrawals))
        total = deposits + withdrawals
        self.total.SetData(amount_format(total))
        if self.total >= 0:
            self.total.SetColor("Text", GREENCOLOR)
        else:
            self.total.SetColor("Text", REDCOLOR)

        self.action.SetData('')


def CreateLayout():
    # Creates the layout of the GUI dialog

    b = acm.FUxLayoutBuilder()

    b.BeginVertBox('None')
    b.BeginHorzBox('EtchedIn', label='Cash Flow Bookings')
    b.AddInput('input_file', 'Input file')
    b.AddButton('select_file', '...', False, True)
    b.EndBox()
    b.AddSpace(10)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddOption('client_name', 'Client')
    b.AddButton('upload_cashflows', 'Load')
    b.AddButton('cancel', 'Cancel')
    b.EndBox()
    b.BeginVertBox('EtchedIn', 'Unprocessed Cash Flows')
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddLabel('action', "", False, True)
    b.EndBox()
    b.AddList('cashflows_to_upload', 15, -1, 150, -1)
    b.EndBox()
    b.AddSpace(10)
    b.BeginVertBox('EtchedIn', 'Processed Cash Flows')
    b.AddList('cashflows_uploaded', 15, -1, 150, -1)
    b.EndBox()
    b.AddSpace(10)
    b.BeginHorzBox('None')
    b.AddCheckbox('reverse_check', 'Reverse Selected')
    b.AddCheckbox('reverse_check_1', 'Reverse All')
    b.AddButton('process_cashflows', 'Process')
    b.AddFill()
    b.BeginVertBox('EtchedIn', 'Total Deposits')
    b.AddLabel('total_deposits', "", False, True)
    b.EndBox()
    b.BeginVertBox('EtchedIn', 'Total Withdrawals')
    b.AddLabel('total_withdrawals', "", False, True)
    b.EndBox()
    b.BeginVertBox('EtchedIn', 'Total Uploaded')
    b.AddLabel('total', "", False, True)
    b.EndBox()
    b.EndBox()
    b.EndBox()
    return b


class CashflowCheck(object):
    def __init__(self, amount, deposit, hash):
        self.amount = amount
        self.deposit = acm.FInstrument[deposit]
        self.hash = hash

    def get_trade(self):
        trades = self.deposit.Trades()
        length = len(trades)

        if length == 1:
            trade = trades[0].Oid()
        elif len(trades) > 1:
            trade = "MULTIPLE TRADES"
        else:
            trade = None
        return trade

    def get_balance(self):
        # Return balance of the deposit
        column = "Deposit balance"
        try:
            balance = CALC_SPACE.CalculateValue(self.deposit, column).Number()
        except Exception as e:
            name = self.deposit.Name()
            LOGGER.exception("Unable to get balance for: %s" % name, e)
        return balance

    def get_cashflow(self):
        # Return cashflow with a given hash
        type = None
        leg = self.deposit.Legs()[0]
        for cf in leg.CashFlows():
            if cf.PayDate() == DATE:
                add_info_hash = cf.AddInfoValue('MM_Hash')
                add_info_settle_type = cf.AddInfoValue('Settle_Type')
                if (cf.CashFlowType() == "Fixed Amount") and (add_info_hash == self.hash) and (
                        add_info_settle_type == "Settle"):
                    type = "Settle"
                elif (cf.CashFlowType() == "Fixed Amount") and (add_info_hash == self.hash) and (
                        add_info_settle_type == "Reverse"):
                    type = "Reverse"
        return type

    def breach_check(self):
        # Check if uploading the amount won't breach the min balance
        balance = self.get_balance()
        if balance + self.amount < self.deposit.MinimumPiece():
            return False
        return True

    def get_upload_status(self):
        # Return status of the future upload operation
        '''
        OK - Cashflow can be posted
        MISSING - Cashflow can't be posted - no deposit
        POSTED - Cashflow already posted
        BREACH - Cashflow would breach the min balance
        '''
        status = "OK"
        if not self.deposit:
            status = "MISSING"
        else:
            if not self.get_trade():
                status = "MISSING"
            elif self.get_trade() == "MULTIPLE TRADES":
                status = "MULTIPLE TRADES"
            elif self.get_cashflow() == "Settle":
                status = "POSTED"
            elif self.get_cashflow() == "Reverse":
                status = "REVERSED"
            elif not self.breach_check():
                status = "BREACH"
        return status


class ProcessXLSFileData(SimpleXLSFeedProcessor):
    def __init__(self, file_path, client):
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.file_path = file_path
        self.records = []
        self.dict = None
        self.file_name = self.file_path[(self.file_path.rfind('\\') + 1):]
        self.upper_file_name = (self.file_name.upper()).strip()
        self.client_name = client

        try:
            value = filenames_map[self.client_name]
            self.dict = value[1]
            self.start_index = value[2]
            self.end_index = value[3]
        except KeyError:
            message = 'Please select client name.'
            DIALOG_FUNC('Complete', message, 0)
            raise Exception('File name not included in list.')

    def _generate_records(self):
        # Generates tuples (index, record)
        '''
        index is the XLS line number (counting only data lines
        and starting from 1).
        record is a dict with the current record
        '''
        # Get source data
        worksheet = self._get_data()
        transaction_type = None
        client_code = None
        amount = None
        if "ARGON" == self.client_name:
            for row in range(0, worksheet.nrows):
                index = row
                self._log("XLS line {0}".format(index))
                if not worksheet.cell_type(row, 0) == xlrd.XL_CELL_EMPTY:
                    if "WITHDRAWALS" in str(worksheet.cell_value(row, 0)):
                        transaction_type = 'WITHDRAWAL'
                        continue
                    if "DEPOSITS" in str(worksheet.cell_value(row, 0)):
                        transaction_type = 'DEPOSIT'
                        continue
                    if transaction_type:
                        client_code = worksheet.cell_value(row, 0)
                        amount = worksheet.cell_value(row, 1)
                        record = {"TRADE TYPE": transaction_type,
                                  "CLIENT CODE": client_code,
                                  "AMOUNT": amount}
                        yield (index, record)

        else:
            columns = []
            if "ABSA AM" == self.client_name:
                columns = ["ACCOUNT", "ACCOUNT NAME"," DEPOSIT", "WITHDRAWAL"] 
            else:
                for col in range(worksheet.ncols):
                    columns.append(worksheet.cell_value(self.start_index - 1, col).encode("utf-8"))
                columns = filter(None, columns)
            for row in range(self.start_index, worksheet.nrows - self.end_index):
                index = row
                self._log("XLS line {0}".format(index))
                values = []
                for col in range(worksheet.ncols):
                    values.append(worksheet.cell_value(row, col))

                if self.client_name in ('OMWTC', 'ABSA AM','CORONATION','ABSA-PROWESS'):
                    record = {columns[i]: values[i] for i in range(len(columns))}
                    yield (index, record)
                else:
                    filtered_values = filter(None, values)
                    if len(filtered_values) == len(columns):
                        record = {columns[i]: filter(None, values)[i] for i in range(len(columns))}
                        yield (index, record)

    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record
        result = {}
        for key, value in record_data.items():
            upper_key = (key.upper()).strip()
            if "CITADEL" == self.client_name and "CALL ACCOUNT NUMBER" == upper_key:
                result[upper_key] = value.replace('-', '-ZAR-', 1)
            else:
                result[upper_key] = value

        record_data = result

        processor = CLIENT_Processor(record_data, self.dict, self.client_name)
        cashflow_keys = processor.variables
        if cashflow_keys:
            self.counterparty_code = "N/A"
            self.call_account = "N/A"
            self.balance = "N/A"
            self.trade = "N/A"

            self.hash = hashlib.md5()
            self.counterparty_code = str(record_data[cashflow_keys["counterparty_code_key"]])
            self.call_account = str(record_data[cashflow_keys["call_account_key"]])
            self.hash.update(
                self.call_account + str(DATE) + str(cashflow_keys["amount"]) + str(cashflow_keys["transaction_type"]))
            self.creator = CashflowCheck(cashflow_keys["amount"], self.call_account, self.hash.hexdigest())
            self.status = self.creator.get_upload_status()

            if self.status not in ["MISSING", "MULTIPLE TRADES"]:
                self.balance = self.creator.get_balance()
                self.trade = self.creator.get_trade()

            cashflow_data = {'code': self.counterparty_code, 'instrument': self.call_account,
                             'trade': self.trade, 'amount': cashflow_keys["amount"], 'balance': self.balance,
                             'status': self.status, 'hash': self.hash.hexdigest(), 'reverse': 'FALSE',
                             'reverse_amount': 'N/A', 'id': 'N/A'}

            self.records.append(cashflow_data)


class CLIENT_Processor():
    def __init__(self, record_data, dict, client):
        self.variables = {}
        self.client = client
        if record_data[dict["code_key"]] != '':
            type = None
            excel_amount = None
            deposit = None
            withdrawal = None

            if 'ALLAN GRAY' == self.client:
                self.variables["counterparty_code_key"] = dict["code_key"]
                self.variables["call_account_key"] = dict["account_key"]
                amount = float(record_data[dict["amount_key"]])
                self.variables["amount"] = amount
                if amount < 0:
                    self.variables["transaction_type"] = "WITHDRAWAL"
                else:
                    self.variables["transaction_type"] = "DEPOSIT"

            if dict["type_key"]:
                if record_data[dict["type_key"]] != '':
                    type = record_data[dict["type_key"]].upper().strip()
                    excel_amount = record_data[dict["amount_key"]]
            else:
                deposit = record_data[dict["deposit_key"]] if dict["deposit_key"] else None
                withdrawal = record_data[dict["withdrawal_key"]] if dict["withdrawal_key"] else None

            if deposit or withdrawal or type or excel_amount:
                self.variables["counterparty_code_key"] = dict["code_key"]
                self.variables["call_account_key"] = dict["account_key"]
                [amount, transaction_type] = get_transaction(deposit, withdrawal, type, excel_amount)
                self.variables["amount"] = amount
                self.variables["transaction_type"] = transaction_type
        else:
            self.variables = None


ABSA_PROWESS = {"code_key": "COUNTERPARTY CODE", "account_key": "CALL ACCOUNT NUMBER", "deposit_key": "DEPOSITS",
                "withdrawal_key": "WITHDRAWALS", "type_key": None, "amount_key": None}
CORONATION = {"code_key": "PORTFOLIO CODE", "account_key": "PORTFOLIO CODE", "deposit_key": "DEPOSIT",
              "withdrawal_key": "WITHDRAWAL", "type_key": None, "amount_key": None}
OMWTC = {"code_key": "PORTF CODE", "account_key": "ABSA CALL NO.", "deposit_key": "DEPOSIT",
         "withdrawal_key": "WITHDRAWAL", "type_key": None, "amount_key": None}
TAQUANTA = {"code_key": "FUND", "account_key": "CALL ACCOUNT NUMBER", "deposit_key": None, "withdrawal_key": None,
            "type_key": "TRANSACTION TYPE", "amount_key": "AMOUNT"}
VUNANI_FM = {"code_key": "PORTFOLIO", "account_key": "PORTFOLIO", "deposit_key": None, "withdrawal_key": None,
             "type_key": "INSTRUCTION", "amount_key": "RAND AMOUNT"}
ABSA_AM = {"code_key": "ACCOUNT", "account_key": "ACCOUNT", "deposit_key": "DEPOSIT", "withdrawal_key": "WITHDRAWAL",
           "type_key": None, "amount_key": None}
OMIG_IM = {"code_key": "CLIENT CODE", "account_key": "CLIENT CODE", "deposit_key": None, "withdrawal_key": None,
           "type_key": "TYPE", "amount_key": "SETTLE GROSS AMOUNT"}
INVESTEC_WITHDRAWALS = {"code_key": "PORTFOLIO CODE", "account_key": "PORTFOLIO CODE", "deposit_key": None,
                        "withdrawal_key": "AMOUNT", "type_key": None, "amount_key": None}
INVESTEC_DEPOSITS = {"code_key": "PORTFOLIO CODE", "account_key": "PORTFOLIO CODE", "deposit_key": "AMOUNT",
                     "withdrawal_key": None, "type_key": None, "amount_key": None}
ALLAN_GRAY = {"code_key": "PORTFOLIO", "account_key": "PORTFOLIO", "deposit_key": None, "withdrawal_key": None,
              "type_key": None,
              "amount_key": "VALUE"}
CITADEL = {"code_key": "CLIENT FULL NAME", "account_key": "CALL ACCOUNT NUMBER", "deposit_key": None,
           "withdrawal_key": None, "type_key": "TRADE TYPE", "amount_key": "AMOUNT"}
ARGON = {"code_key": "CLIENT CODE", "account_key": "CLIENT CODE", "deposit_key": None, "withdrawal_key": None,
         "type_key": "TRADE TYPE", "amount_key": "AMOUNT"}

filenames_map = OrderedDict()
filenames_map['ABSA-PROWESS'] = ['ABSA-PROWESS', ABSA_PROWESS, 5, 0]
filenames_map['CORONATION'] = ['CORONATION', CORONATION, 1, 0]
filenames_map['OMWTC'] = ['OMWTC', OMWTC, 1, 0]
filenames_map['TAQUANTA'] = ['TAQUANTA', TAQUANTA, 1, 0]
filenames_map['VUNANI FM'] = ['VUNANI FM', VUNANI_FM, 3, 0]
filenames_map['OMIG IM'] = ['OMIG IM', OMIG_IM, 1, 0]
filenames_map['ABSA AM'] = ['ABSA AM', ABSA_AM, 9, 0]
filenames_map['NINETY ONE WITHDRAWALS'] = ['NINETY ONE WITHDRAWALS', INVESTEC_WITHDRAWALS, 7, 0]
filenames_map['NINETY ONE DEPOSITS'] = ['NINETY ONE DEPOSITS', INVESTEC_DEPOSITS, 7, 0]
filenames_map['ALLAN GRAY'] = ['ALLAN GRAY', ALLAN_GRAY, 13, 0]
filenames_map['CITADEL'] = ['CITADEL', CITADEL, 5, 0]
filenames_map['ARGON'] = ['ARGON', ARGON, 0, 0]


