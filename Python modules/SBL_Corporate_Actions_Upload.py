"""-----------------------------------------------------------------------------------------
MODULE
    SBL_Corporate_Actions_Upload

DESCRIPTION
    Date                : 2019-10-21
    Purpose             : This will import corporate actions from a Standard Chartered diary
    Department and Desk : SBL Ops
    Requester           : James Stevens
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2019-10-21      PCGDEV-84       Qaqamba Ntshobane       Initial Implementation
2019-11-06      PCGDEV-181      Qaqamba Ntshobane       Made changes to allow files with 
                                                        empty cells to be uploaded with each
                                                        empty field index corresponding to 
                                                        its index in the file
2019-11-26      PCGDEV-211      Qaqamba Ntshobane       Changed the logic for cleaning up
                                                        rows of data from CA diary. Also
                                                        handled exception where date is 
                                                        'TBA' from diary.
2020-01-27      PCGDEV-235      Qaqamba Ntshobane       Updated duplicate check function.
                                                        Added dynamic CA event creation.

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import FBDPGui
import FBDPCommon
import FRunScriptGUI

import os
import sys
import xlrd
import string
import datetime

from at_logging import getLogger
from at_ael_variables import AelVariableHandler

import FOpenCorpAction
import FUploaderFunctions

ASCII = set(string.printable)
LOGGER = getLogger(__name__)
ROW_COUNT = 1

CONTEXT = acm.GetDefaultContext()
MODULE = CONTEXT.GetModule("Securities Lending ABSA")
EVENTS_LIST = FBDPGui.getCorpActTemplateNames()
ABSA_CA_EVENTS = MODULE.GetAllExtensions('FParameters')
EVENTS_LIST.extend(ABSA_CA_EVENTS)
EVENTS_LIST_UPPERCASE = map(lambda each: str(each).upper(), EVENTS_LIST)

DATE_CONTAINER = []
DATE_ROW_KEYWORDS = ['Last day to trade', 'Ex date', 'Record date']
CA_EVENTS_MAPPING = {'SCRIP':'SCRIPDIVIDEND','RIGHTSSUBSCIPTION':'RIGHTSSUBSCRIPTION', 'INTERESTING':'INTEREST'}
EXCLUDE_ROW_KEYWORDS = ["TAXABLE EVENTS", "RATIO ", "NON-TAXABLE EVENTS", "JSE", "CODE", "JSE CODE", "Last day to remat/demat", ""]

fileFilter = "XLSX Files (*.xlsx)|*.xlsx|XLS Files (*.xls)|*.xls|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
sys.setdefaultencoding('utf8')

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in XLS format.'
    )
ael_variables.add(
    "email_address",
    label="Email Address:",
    alt="Use a comma as a separator",
    multiple=True
    )


class CorporateActionsContainer():

    def __init__(self):
        self.record_mapping = {}

    def add_record_mapping(self, column_name, field_data):

        if type(field_data) == str:
            field_data = str(field_data)

        self.record_mapping.update({column_name: field_data})

    def get_record_mapping(self):
        return self.record_mapping


def remove_redundant_data():

    corpacts = [ca for ca in acm.FCorporateAction.Select("") if ca.Dividend() and (ca.AdditionalInfo().Gross_Taxable_Rate() or ca.Text())]

    for corpact in corpacts:
        gta = corpact.AdditionalInfo().Gross_Taxable_Rate()
        div_amount = round(corpact.Dividend().Amount(), 2)

        if (gta == "TBA" and div_amount) or (gta and round(float(gta[3:]), 2) == div_amount):
            corpact.AdditionalInfo().Gross_Taxable_Rate("")

        text_div = corpact.Text().split(" ")
        
        if len(text_div) > 1:
            continue
        
        if len(text_div) == 1:
            text_div = text_div[0][3:]

            if text_div.isdigit() and round(float(text_div), 2) == div_amount:
                corpact.Text("")
        corpact.Commit()


def set_addinfos(corp_act, row_data, security=None):

    divi = None

    if len(row_data) > 7:
        corp_act.AdditionalInfo().Tax_Rate(str(row_data[6]))
        corp_act.AdditionalInfo().WITF(str(row_data[7]))

        if is_foreign_currency(str(row_data[5])):
            row_data[5] = 'TBA'

        if str(row_data[9]) == 'Y':
            corp_act.AdditionalInfo().Tax_Indicator("Yes")
        else:
            corp_act.AdditionalInfo().Tax_Indicator("No")

        divi = str(row_data[5])

        if divi not in ['TBA', 'N/A'] and corp_act.Dividend() and\
           round(float(divi[3:]), 2) == round(corp_act.Dividend().Amount(), 2):
            return

        if corp_act.RecordDate() > acm.Time.DateToday() or not corp_act.Dividend():
            corp_act.AdditionalInfo().Gross_Taxable_Rate(divi)
            log_event(corp_act, str(divi), "success")

    if security:
        corp_act.AdditionalInfo().Security(security + ", " + str(row_data[3]))


def _create_new_ca_event(event_from_diary):

    MODULE.RegisterInStorage()

    ca_event_clone = MODULE.GetExtension('FParameters', 'FObject', ABSA_CA_EVENTS[-1]).Clone()
    ca_event_clone.Value().Name(event_from_diary)

    MODULE.AddExtension(ca_event_clone)
    MODULE.Apply(MODULE)
    MODULE.Commit()

    EVENTS_LIST.append(event_from_diary)
    EVENTS_LIST_UPPERCASE.append(event_from_diary.upper())


def _event_already_added(ca_event, corp_act):

    event_index = EVENTS_LIST_UPPERCASE.index(ca_event)
    return str(EVENTS_LIST[event_index]) == str(corp_act.Templates()[-1].Name())


def set_ca_events(corp_act, row_data):

    ca_event_from_diary = filter(lambda x: x in ASCII, str(row_data[1]))
    ca_event = ca_event_from_diary.replace(" ", "").strip("-")

    if ca_event in CA_EVENTS_MAPPING:
        ca_event = CA_EVENTS_MAPPING[ca_event]

    if len(corp_act.Templates()) > 0 and _event_already_added(ca_event, corp_act):
        return

    if ca_event not in EVENTS_LIST_UPPERCASE:
        ca_event_from_diary = ca_event_from_diary.title().replace(" ", "").strip("-")
        _create_new_ca_event(ca_event_from_diary)

    if ca_event in EVENTS_LIST_UPPERCASE:
        index = EVENTS_LIST_UPPERCASE.index(ca_event)
        cat = acm.FCorpactTemplate()
        cat.RegisterInStorage()
        cat.Name(EVENTS_LIST[index])
        cat.CorporateAction(corp_act)
        cat.Commit()


def log_events(email_addresses, file_name):

    global ROW_COUNT
    email_subject = 'Upload Logs: %s' % file_name[:-5]
    report_header = 'Corporate Actions Upload'
    email_sender = 'AbCapEQDMO@absa.africa'

    if FUploaderFunctions.REPORT_DATA:
        table_headings = 'Corporate Action', 'Rate', 'Log Info'
        FUploaderFunctions.add_header(table_headings)
        LOGGER.info("Corporate actions successfully imported onto FA")

    FUploaderFunctions.send_report(email_addresses, email_sender, email_subject, report_header)
    ROW_COUNT = 1


def is_foreign_currency(div_amount):

    return not div_amount[:3] == 'ZAR'


def to_date(date):

    if date in ['TBA', 'N/A']:
        return ''
    return FBDPCommon.toDate(date)


def set_dates(corp_act):

    for date in range(len(DATE_CONTAINER)):

        _date = to_date(DATE_CONTAINER[date][1])

        if DATE_CONTAINER[date][0] == "Last day to trade":
            corp_act.TradingEndDate(_date)
        elif DATE_CONTAINER[date][0] == "Ex date":
            corp_act.ExDate(_date)
        else:
            corp_act.RecordDate(_date)


def create_corpact_name(corp_act, row_data):

    if len(row_data) > 7:
        corp_id = str(row_data[10])
    else:
        corp_id = str(row_data[6])

    if corp_id:
        split_corp_id = corp_id[-4:].split("-")[-1]
    else:
        split_corp_id = ''

    split_date = corp_act.RecordDate().split('-')
    date_name = split_date[0][-2:] + split_date[1] + split_date[2]
    company_name = row_data[2].encode('utf-8').split(",")[0].rstrip()

    return str(str(row_data[0])+'_'+date_name+split_corp_id+'_'+company_name)[slice(39)].rstrip(), corp_id


def already_exists(corp_act, corpact_name, row_data):

    if acm.FCorporateAction[corpact_name]:
        corp_act = acm.FCorporateAction[corpact_name]

        if corp_act.AdditionalInfo().Gross_Taxable_Rate():
            div = corp_act.AdditionalInfo().Gross_Taxable_Rate()

            if not div == 'TBA':
                div = float(div[3:])

        elif corp_act.Dividend():
            div = corp_act.Dividend().Amount()
        else:
            div = None

        try:
            corpact_div = round(div, 5)
            diary_div = round(float(row_data[5][3:]), 5)
        except:
            corpact_div = div
            diary_div = str(row_data[5])

        if len(row_data) > 7:
            if is_foreign_currency(str(row_data[5])):
                row_data[5] = 'TBA'

            if not diary_div == 'TBA' and diary_div == corpact_div or (row_data[5] == 'TBA' and corpact_div):
                log_event(corp_act, str(diary_div), "duplicate")
                return None
        else:
            if row_data[4] and corp_act.Text() == str(row_data[4])[slice(38)].rstrip():
                log_event(corp_act, str(corp_act.Text()), "duplicate")
                return None
    return corp_act


def log_event(corp_act, rate, log_event):

    if log_event == "duplicate":
        row_info_list = [str(ROW_COUNT), str(corp_act.Name()), rate, 'Corporate Action already exists in FA']
        FUploaderFunctions.add_row(ROW_COUNT, row_info_list)
    elif log_event == "success":
        row_info_list = [str(ROW_COUNT), str(corp_act.Name()), rate, 'New Corporate Action Uploaded to FA']
        FUploaderFunctions.add_row(ROW_COUNT, row_info_list)


def create_corporate_action(corporate_actions_container):

    global ROW_COUNT
    corp_act = None

    for row_data in corporate_actions_container.get_record_mapping().values():

        if row_data:
            security = str(row_data[0])

            if len(DATE_CONTAINER) == 4 and DATE_CONTAINER[0][0] == DATE_CONTAINER[3][0]:
                del DATE_CONTAINER[:3]

            if len(row_data) == 2:
                if row_data[1] == "N/A":
                    row_data[1] = None

                DATE_CONTAINER.append(row_data)
                continue

            corp_act = acm.FCorporateAction()

            if DATE_CONTAINER:
                set_dates(corp_act)

            corpact_name, corp_id = create_corpact_name(corp_act, row_data)

            corp_act = already_exists(corp_act, corpact_name, row_data)

            if not corp_act:
                ROW_COUNT += 1
                continue

            corp_act.RegisterInStorage()

            corpact_text = str(row_data[4])[slice(38)].rstrip()
            corp_act.Name(corpact_name)
            corp_act.Text(corpact_text)
            corp_act.Market('SPOT')
            corp_act.CaChoiceType('Mandatory')

            if len(row_data) > 7:
                try:
                    corp_act.SettleDate(to_date(row_data[8]))
                except:
                    row_data.append(row_data[9])
                    row_data[9] = row_data[8]
                    corp_act.SettleDate(to_date(row_data[7]))

                if acm.FCorporateAction.Select("externalId='%s'" % corp_id):
                    corp_act.ExternalId(corp_id+"_"+security)
                else:
                    corp_act.ExternalId(corp_id)
            else:
                corp_act.SettleDate(to_date(row_data[5]))
                if acm.FCorporateAction.Select("externalId='%s'" % corp_id):
                    corp_act.ExternalId(corp_id+"_"+security)
                else:
                    corp_act.ExternalId(corp_id)

            instrument = "ZAR/"+security

            if acm.FInstrument[instrument]:
                corp_act.Instrument(acm.FInstrument[instrument])
                divi = acm.FDividend.Select("instrument='%s' and payDay='%s'" % (instrument, corp_act.SettleDate()))
                instrument = None

                if len(divi) == 1:
                    corp_act.Dividend(divi[0])
                else:
                    for ca_div in divi:
                        if ca_div.Description() in ['Foreign', '', 'Interim']:
                            corp_act.Dividend(ca_div)
            else:
                corp_act.Instrument = None

            set_addinfos(corp_act, row_data, instrument)

            if corp_act.SettleDate() == "":
                corp_act.WithdrawalDate(corp_act.RecordDate())

            corp_act.Commit()
            set_ca_events(corp_act, row_data)

            FOpenCorpAction.__setBusinessEvent(corp_act, None)

            if not len(row_data) > 7:
                log_event(corp_act, str(corp_act.Text()), "success")
            ROW_COUNT += 1


def clean_up_row_data(row_data):

    year = acm.Time().DateToday()[:4]
    prev_year = int(acm.Time().DateToday()[:4]) - 1

    if not row_data or (row_data and row_data in EXCLUDE_ROW_KEYWORDS):
        return
    if row_data[0] in DATE_ROW_KEYWORDS:
        return row_data[:2]
    if row_data[0] not in EXCLUDE_ROW_KEYWORDS:
        for row in row_data:
            if str(row).startswith(year) or str(row).startswith(str(prev_year)):
                index = row_data.index(row)
                return row_data[:(index+1)]


def read_corporate_actions(file_path, file_name):

    corporate_actions_container = CorporateActionsContainer()

    with xlrd.open_workbook(file_path) as wb:

        LOGGER.info("Reading Diary: %s." % file_name)

        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows

        for row in range(rows):
            row_data = []

            for col in range(sheet.ncols):
                if sheet.cell(row, 0).value == "":
                    continue
                value = sheet.cell(row, col).value
                row_data.append(value)

            row_data = clean_up_row_data(row_data)

            if row_data:
                corporate_actions_container.add_record_mapping(row, row_data)

        if len(corporate_actions_container.record_mapping) > 0:
            LOGGER.info("Diary read successfully")
        else:
            LOGGER.info("No corporate actions read from diary")
    create_corporate_action(corporate_actions_container)


def ael_main(dictionary):

    file_path = str(dictionary['input_file'])
    file_name = os.path.basename(file_path)
    email_addresses = dictionary['email_address']

    read_corporate_actions(file_path, file_name)
    log_events(email_addresses, file_name)
    remove_redundant_data()
    EVENTS_LIST[:]
    EVENTS_LIST_UPPERCASE[:]

    LOGGER.info("Completed successfully.")
