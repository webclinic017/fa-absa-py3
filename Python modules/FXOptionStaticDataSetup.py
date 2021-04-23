"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FXOptionConfirmationStaticDataSetup.

DESCRIPTION
    This module contains a temporary AEL main script used for the setup
    of trade confirmation party data.

    PLEASE NOTE: This script is intended to be manually deleted after
    execution.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer                  Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-12-04      FAOPS-439       Tawanda Mukhalela          Letitia Carboni         FX Option Confirmation Static Upload
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import collections
import datetime
import DocumentGeneral
import os
import re
import xlrd


LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Input File Path.
    ael_variable_handler.add_input_file(
        name='input_file_path',
        label='Input File Path',
        file_filter='*.xlsx',
        mandatory=True,
        multiple=False,
        alt='The file path of the input party data excel file.'
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        input_file_path = ael_parameters['input_file_path'].AsString()
        _validate_input_file_path(input_file_path)
        _setup_trade_affirmation_parties(input_file_path)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _validate_input_file_path(input_file_path):
    """
    Validate the input file path.
    """
    if not os.path.exists(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not exist."
        raise ValueError(exception_message.format(
            input_file_path=input_file_path
        ))
    if not os.path.isfile(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not point to a file."
        raise ValueError(exception_message.format(
            input_file_path=input_file_path
        ))


def _setup_trade_affirmation_parties(input_file_path):
    """
    Setup trade affirmation parties.
    """
    for acquirer, acquirer_party_data in _get_party_data_by_acquirer(input_file_path).items():
        for party_data in acquirer_party_data:
            _setup_party(acquirer, party_data)
        
        
def _setup_party(acquirer, party_data):
    """
    Setup a trade affirmation party for a particular acquirer.
    """
    party = _find_party_by_name(party_data.name)
    if party is None:
        LOGGER.warning("A party with the name '{name}' does not exist - skipping...".format(
            name=party_data.name
        ))
        return
    message = "Setting up party '{party_name}'..."
    LOGGER.info(message.format(
        party_name=party_data.name
    ))
    try:
        _setup_contact(party, party_data, acquirer)
        if party.Type() != 'Intern Dept':
            _setup_confirmation_instruction(party, party_data, acquirer)
    except Exception as exception:
        LOGGER.exception(exception)


def _find_party_by_name(name):
    """
    Find a party by name.

    If a party with the specified name is not found then
    None is returned.
    """
    return acm.FParty[name]


def _setup_contact(party, party_data, acquirer):
    """
    Setup trade affirmation contact for a particular acquirer.
    """
    email_addresses = _format_email_addresses(party_data.email)
    contact = None
    if party.Type() == 'Intern Dept':
        contact = _find_contact_by_full_name(party, party_data.contact_name)
    else:
        contact = _find_contact_by_email_addresses(party, email_addresses)
    if contact is None:
        LOGGER.info("- 'An existing contact was not found, creating.")
        contact = acm.FContact()
        contact.Fullname(party_data.contact_name)
        contact.Party(party)
    else:
        LOGGER.info("- 'An existing contact was found, updating.")
    contact.Address(party_data.address_line_1)
    contact.Address2(party_data.address_line_2)
    contact.City(party_data.address_city)
    contact.Country(party_data.address_country)
    zip_code = _format_zip_code(party_data.address_zipcode)
    contact.Zipcode(zip_code)
    contact.Attention(party_data.attention)
    telephone = _format_phone_number(party_data.telephone)
    contact.Telephone(telephone)
    fax = _format_phone_number(party_data.fax)
    contact.Fax(fax)
    if len(email_addresses) > 100:
        LOGGER.warning("The email addresses for party '{name}' are longer than 100 characters.".format(
            name=party_data.name
        ))
    for email_address in email_addresses.split(','):
        if not _email_address_appears_valid(email_address):
            LOGGER.warning("The email address '{email_address}' for party '{name}' appears invalid.".format(
                email_address=email_address,
                name=party_data.name
            ))
    contact.Email(email_addresses)
    _setup_contact_rule(contact, party_data.event, acquirer)
    contact.Commit()


def _email_address_appears_valid(email_address):
    return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email_address)


def _find_contact_by_full_name(party, contact_name):
    """
    Find any existing contact with the specified full name.
    """
    for contact in party.Contacts():
        if contact.Fullname() == contact_name:
            return contact
    return None


def _find_contact_by_email_addresses(party, email_addresses):
    """
    Find any existing contact with the same email addresses.
    """
    for contact in party.Contacts():
        if email_addresses_match(contact.Email().split(','), email_addresses.split(',')):
            return contact
    return None


def email_addresses_match(email_addresses1, email_addresses2):
    """
    Determine whether or not two list contain the same set of email
    addresses, irrespective of order.
    """
    if len(email_addresses1) != len(email_addresses2):
        return False
    for email_address in email_addresses1:
        if email_address not in email_addresses2:
            return False
    return True

    
def _format_zip_code(zip_code):
    """
    Perform cleanup formatting on a zip code.
    """
    if zip_code is None or zip_code.strip() == '':
        return None
    return zip_code.replace('.0', '')

    
def _format_phone_number(phone_number):
    """
    Perform cleanup formatting on a phone number.
    """
    if phone_number is None:
        return None
    formatted_phone_number = phone_number.strip()
    # Remove any characters other than letters and numbers.
    formatted_phone_number = re.sub(r'(?u)[^a-zA-Z0-9]', '', formatted_phone_number)
    if len(formatted_phone_number) != 11:
        # Only catering for expected international format found in
        # current upload sheet, e.g. +27118957492, 27118957492, etc.
        return phone_number
    formatted_phone_number = ('+' + formatted_phone_number[:2] + ' ' + formatted_phone_number[2:4] +
        ' ' + formatted_phone_number[4:7] + ' ' + formatted_phone_number[7:])
    return formatted_phone_number
    
    
def _format_email_addresses(email_addresses):
    """
    Perform cleanup formatting on an email address.
    """
    if email_addresses is None:
        return None
    email_addresses = email_addresses.strip()
    return email_addresses.replace(';', ',').replace(' ', '')

    
def _setup_contact_rule(contact, event_name, acquirer):
    """
    Setup contact rule for for specified event and acquirer.
    """
    instype = 'Option'
    underlying_instype = 'Curr'
    contact_rule = _find_contact_rule_by_event_name_and_acquirer(contact, event_name, acquirer)
    if contact_rule is None:
        message = "- '{event_name}' contact rule for acquirer '{acquirer_name}' "
        message += "not found, creating."
        LOGGER.info(message.format(
            event_name=event_name,
            acquirer_name=acquirer.Name()
        ))
        contact_rule = acm.FContactRule()
        contact_rule.EventChlItem(event_name)
        contact.ContactRules().Add(contact_rule)
    else:
        message = "- '{event_name}' contact rule for acquirer '{acquirer_name}' "
        message += "found, updating."
        LOGGER.info(message.format(
            event_name=event_name,
            acquirer_name=acquirer.Name()
        ))
    contact_rule.Acquirer(acquirer)
    contact_rule.Currency(None)
    contact_rule.InsType(instype)
    contact_rule.UndInsType(underlying_instype)
    contact_rule.IssuanceType('None')
    contact_rule.ProductTypeChlItem(None)

    
def _find_contact_rule_by_event_name_and_acquirer(contact, event_name, acquirer):
    """
    Find an existing contact rule for a specified event name and
    acquirer.
    """
    for contact_rule in contact.ContactRules():
        if contact_rule.EventChlItem() is None:
            continue
        if contact_rule.EventChlItem().Name() != event_name:
            continue
        if contact_rule.Acquirer() == acquirer:
            return contact_rule
    return None


def _setup_confirmation_instruction(party, party_data, acquirer):
    """
    Setup trade affirmation confirmation instruction.
    """
    event_name = party_data.event
    template_name = None
    if event_name == 'Trade Confirmation':
        template_name = 'ABSA_Trade_Confirmation'
    else:
        ValueError("Unsupported event '{event_name}' specified.".format(
            event_name=event_name
        ))
    confirmation_instruction = _find_confirmation_instruction_by_event_name_and_acquirer(
        party, event_name, acquirer)
    if confirmation_instruction is None:
        message = "- '{event_name}' confirmation_instruction for acquirer '{acquirer_name}' not found, creating."
        LOGGER.info(message.format(
            event_name=event_name,
            acquirer_name=acquirer.Name()
        ))
        confirmation_instruction = acm.FConfInstruction()
        confirmation_instruction.RegisterInStorage()
        confirmation_instruction.Counterparty(party)
        confirmation_instruction.InternalDepartment(acquirer)
        confirmation_instruction.InsType('Option')
        confirmation_instruction.UndInsType('Curr')
        confirmation_instruction.EventChlItem(event_name)
    else:
        message = "- '{event_name}' confirmation_instruction found, updating."
        LOGGER.info(message.format(
            event_name=event_name
        ))
        confirmation_instruction = confirmation_instruction.StorageImage()
    confirmation_instruction_name = '{acquirer_id2} {event_name} Email'.format(
        acquirer_id2=acquirer.Id2(),
        event_name=event_name
    )
    confirmation_instruction.Name(confirmation_instruction_name)
    confirmation_instruction.Transport('Email')
    confirmation_instruction.Active(True)
    _setup_confirmation_instruction_rule(confirmation_instruction, template_name)
    confirmation_instruction.Commit()
        
    
def _find_confirmation_instruction_by_event_name_and_acquirer(party, event_name, acquirer):
    """
    Find an existing confirmation instruction for a specified event
    name and acquirer.
    """
    for confirmation_instruction in party.ConfInstructions():
        if confirmation_instruction.EventChlItem() is None:
            continue
        if confirmation_instruction.EventChlItem().Name() != event_name:
            continue
        if confirmation_instruction.InternalDepartment() is None:
            continue
        if confirmation_instruction.InternalDepartment() == acquirer:
            return confirmation_instruction
    return None    


def _setup_confirmation_instruction_rule(confirmation_instruction, template_name):
    """
    Setup confirmation instruction rule.
    """
    confirmation_instruction_rule = _find_confirmation_instruction_rule_by_template_name(
        confirmation_instruction, template_name)
    if confirmation_instruction_rule is None:
        message = "- '{template_name}' confirmation instruction rule not found, creating."
        LOGGER.info(message.format(
            template_name=template_name
        ))
        confirmation_instruction_rule = acm.FConfInstructionRule()
        confirmation_instruction_rule.TemplateChoiceList(template_name)
        confirmation_instruction.ConfInstructionRules().Add(confirmation_instruction_rule)
    else:
        message = "- '{template_name}' confirmation instruction rule found, updating."
        LOGGER.info(message.format(
            template_name=template_name
        ))
    confirmation_instruction_rule.Type('Default')
    confirmation_instruction_rule.Stp(False)
        
        
def _find_confirmation_instruction_rule_by_template_name(confirmation_instruction, template_name):
    """
    Find an existing confirmation instruction rule by template name.
    """
    for confirmation_instruction_rule in confirmation_instruction.ConfInstructionRules():
        if confirmation_instruction_rule.TemplateChoiceList() is None:
            continue
        if confirmation_instruction_rule.TemplateChoiceList().Name() == template_name:
            return confirmation_instruction_rule
    return None
    
    
def _get_party_data_by_acquirer(input_file_path):
    """
    Get a list of party data objects by acquirer for the data
    contained in the workbook represented by a specified path.

    The name of each sheet is expected to match a party within
    Front Arena.
    """
    column_list = _get_workbook_column_list()
    party_data_class = collections.namedtuple('PartyData', column_list)
    party_data_by_acquirer = {}
    with xlrd.open_workbook(input_file_path) as workbook:
        for sheet in workbook.sheets():
            sheet_name = str(sheet.name)
            acquirer = _find_party_by_name(sheet_name)
            if acquirer is None:
                raise ValueError("A party with the name of sheet '{sheet_name}' does not exist.".format(
                    sheet_name=sheet_name
                ))
            if acquirer.Type() != 'Intern Dept':
                raise ValueError("The party represented by sheet '{sheet_name}' is not an internal department.".format(
                    sheet_name=sheet_name
                ))
            sheet_party_data = _get_party_data_from_sheet(party_data_class, 
                sheet, column_list)
            party_data_by_acquirer[acquirer] = sheet_party_data
    return party_data_by_acquirer


def _get_workbook_column_list():
    """
    Get the list of expected workbook columns.
    """
    return [
        'name',
        'full_name',
        'contact_name',
        'address_line_1',
        'address_line_2',
        'address_city',
        'address_country',
        'address_zipcode',
        'attention',
        'telephone',
        'fax',
        'email',
        'event'
    ]


def _get_party_data_from_sheet(party_data_class, sheet, column_list):
    """
    Get a list of party data objects for the data contained in a 
    specified sheet.
    """
    _validate_sheet_columns(sheet, column_list)
    party_data = list()
    for row_index in range(sheet.nrows):
        if row_index == 0:
            # Skip headers.
            continue
        row_party_data = _get_party_data_from_row(party_data_class, sheet,
            row_index, column_list)
        party_data.append(row_party_data)
    return party_data


def _validate_sheet_columns(sheet, column_list):
    """
    Validate the columns of a specified sheet.
    """
    expected_number_of_columns = len(column_list)
    if sheet.ncols != expected_number_of_columns:
        exception_message = "Expecting {expected} workbook columns, encountered "
        exception_message += "{encountered} on sheet '{sheet_name}'."
        raise ValueError(exception_message.format(
            expected=expected_number_of_columns,
            encountered=sheet.ncols,
            sheet_name=sheet.name
        ))


def _get_party_data_from_row(party_data_class, sheet, row_index, column_list):
    """
    Get a party data object for the data on a specified sheet row.
    """
    try:
        cell_values_by_column_name = {}
        for column_index in range(sheet.ncols):
            column_name = column_list[column_index]
            column_value = str(sheet.cell(row_index, column_index).value).encode('utf8')
            cell_values_by_column_name[column_name] = column_value
        return party_data_class(**cell_values_by_column_name)
    except Exception as exception:
        raise ValueError('Error reading party data from sheet {sheet_name}, row {row_index}: {exception}'.format(
            sheet_name=str(sheet.name),
            row_index=row_index + 1,
            exception=exception
        ))
