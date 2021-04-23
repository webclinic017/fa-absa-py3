import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import collections
import datetime
import DocumentGeneral
import os
import xlrd
import at

LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Input File Path.
    ael_variable_handler._add_file_selection(
        name='input_file_path',
        label='Input File Path',
        input_output='input',
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
        _setup_reset_advice_parties(input_file_path)
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
        ))
    if not os.path.isfile(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not point to a file."
        raise ValueError(exception_message.format(
        ))


def _setup_reset_advice_parties(input_file_path):
    """
    Setup IRS reset advice parties.
    """
    for party_data in _get_party_data_from_workbook(input_file_path):
        _setup_party(party_data)


def _setup_party(party_data):
    """
    Setup a reset advice party.
    """
    party = _find_party_by_name(party_data.Name)
    if party is None:
        LOGGER.warning("A party with the name '{name}' does not exist - skipping...".format(
            name=party_data.Name
        ))
        return
    party = _get_party_by_name(party_data.Name)
    message = "Setting up party '{party_name}'..."
    LOGGER.info(message.format(
        party_name=party_data.Name
    ))
    _setup_contact(party, party_data)
    if party.Type() != 'Intern Dept':
        _setup_confirmation_instruction(party, party_data)


def _find_party_by_name(name):
    """
    Find a party by name.

    If a party with the specified name is not found then
    None is returned.
    """
    return acm.FParty[name]


def _get_party_by_name(name):
    """
    Get an existing party by name.

    If a party with the specified name is not found then
    an error is raised.
    """
    party = acm.FParty[name]
    if party is None:
        raise ValueError("A party with the name '{name}' does not exist.".format(
            name=name
        ))
    return party


def _setup_contact(party, party_data):
    """
    Setup reset advice contact.
    """
    contact = _find_contact_by_full_name(party, party_data.Contact_Name)
    if contact is None:
        message = "- '{contact_name}' contact not found, creating."
        LOGGER.info(message.format(
            contact_name=party_data.Contact_Name
        ))
        contact = acm.FContact()
        contact.RegisterInStorage()
        contact.Fullname(party_data.Contact_Name)
        contact.Party(party)
    else:
        message = "- '{contact_name}' contact found, updating."
        LOGGER.info(message.format(
            contact_name=party_data.Contact_Name
        ))
        contact = contact.StorageImage()
    contact.Address(party_data.Address)
    contact.Address2(party_data.Address2)
    contact.City(party_data.City)
    contact.Country(party_data.Country)
    zip_code = _format_zip_code(party_data.Zipcode)
    contact.Zipcode(zip_code)
    contact.Attention(party_data.Attention)
    telephone = _format_phone_number(party_data.Telephone)
    contact.Telephone(telephone)
    fax = _format_phone_number(party_data.Fax)
    contact.Fax(fax)
    email = _format_email_addresses(party_data.Email)
    contact.Email(email)
    _setup_contact_rule(contact)
    contact.Commit()


def _find_contact_by_full_name(party, contact_name):
    """
    Find any existing contact with the specified full name.
    """
    for contact in party.Contacts():
        if contact.Fullname() == contact_name:
            return contact
    return None


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
    # Only catering for expected format found current
    # upload sheet, e.g. +27118957492
    if len(phone_number) == 12:
        phone_number = (phone_number[:3] + ' ' + phone_number[3:5] +
                        ' ' + phone_number[5:8] + ' ' + phone_number[8:])
    return phone_number


def _format_email_addresses(email_addresses):
    """
    Perform cleanup formatting on an email address.
    """
    if email_addresses is None:
        return None
    email_addresses = email_addresses.strip()
    return email_addresses.replace(';', ',').replace(' ', '')


def _setup_contact_rule(contact):
    """
    Setup term statement contact rule for statements for a specified
    acquirer.
    """
    events = _instrument_type_restriction()
    instrments = ['CurrSwap']
    for instr in instrments:
        for event_name in events:
            contact_rule = _find_contact_rule_by_event_name(contact, event_name, instr)
            if contact_rule is None:
                message = "- '{event_name}' contact rule"
                message += "not found, creating."
                LOGGER.info(message.format(
                    event_name=event_name
                ))
                contact_rule = acm.FContactRule()
                contact_rule.EventChlItem(event_name)
                contact.ContactRules().Add(contact_rule)
            else:
                message = "- '{event_name}' contact rule"
                message += "found, updating."
                LOGGER.info(message.format(
                    event_name=event_name
                ))
            contact_rule.Currency(None)
            contact_rule.InsType(instr)
            contact_rule.UndInsType('None')
            contact_rule.IssuanceType('None')
            contact_rule.ProductTypeChlItem(None)


def _find_contact_rule_by_event_name(contact, event_name, instr):
    """
    Find an existing contact rule for a specified event name and
    acquirer.
    """
    for contact_rule in contact.ContactRules():
        if contact_rule.EventChlItem() is None:
            continue
        if contact_rule.EventChlItem().Name() != event_name:
            continue
        if contact_rule.EventChlItem().Name() == event_name and contact_rule.InsType() == instr:
            return contact_rule
    return None


def _instrument_type_restriction():
    return ['Reset Confirmation']


def _setup_confirmation_instruction(party, party_data):
    """
    Setup term statement confirmation instruction.
    """
    events = _instrument_type_restriction()
    instrments = ['CurrSwap']
    for instr in instrments:
        for event_name in events:
            confirmation_instruction = _find_confirmation_instruction_by_event_name(party, event_name, instr)
            if confirmation_instruction is None:
                message = "- '{event_name}' confirmation_instruction not found, creating."
                LOGGER.info(message.format(
                    event_name=event_name
                ))
                confirmation_instruction = acm.FConfInstruction()
                confirmation_instruction.RegisterInStorage()
                confirmation_instruction.Counterparty(party)
                confirmation_instruction.EventChlItem(event_name)
            else:
                message = "- '{event_name}' confirmation_instruction found, updating."
                LOGGER.info(message.format(
                    event_name=event_name
                ))
                confirmation_instruction = confirmation_instruction.StorageImage()
            confirmation_instruction_name = '{instr} {event_name} Email'.format(instr=instr,
                                                                                event_name=event_name)
            confirmation_instruction.Name(confirmation_instruction_name)
            confirmation_instruction.Transport('Email')
            confirmation_instruction.Active(True)
            confirmation_instruction.InsType(instr)
            _setup_confirmation_instruction_rule(confirmation_instruction)
            confirmation_instruction.Commit()


def _find_confirmation_instruction_by_event_name(party, event_name, instr):
    """
    Find an existing confirmation instruction for a specified event
    name.
    """
    for confirmation_instruction in party.ConfInstructions():
        if confirmation_instruction.EventChlItem() is None:
            continue
        if confirmation_instruction.EventChlItem().Name() != event_name:
            continue
        if confirmation_instruction.InsType() == instr:
            return confirmation_instruction
    return None


def _setup_confirmation_instruction_rule(confirmation_instruction):
    """
    Setup term statement confirmation instruction rule.
    """
    template_name = 'ABSA_IRS_Presettlement'
    rule_types = ['Default', 'Amendment', 'Cancellation']
    rules = _find_confirmation_instruction_rule_by_template_name(confirmation_instruction, template_name)

    # for type in rule_types:
    for type in rule_types:

        message = "- '{template_name}' confirmation instruction rule not found, creating."
        LOGGER.info(message.format(
            template_name=template_name
        ))
        confirmation_instruction_rule = acm.FConfInstructionRule()
        confirmation_instruction_rule.TemplateChoiceList(template_name)

        if type == 'Amendment' or type == 'Cancellation':
            confirmation_instruction_rule.Stp(False)
        elif type == 'Default':
            confirmation_instruction_rule.Stp(True)

        confirmation_instruction_rule.Type(type)
        if rules:
            for rule in rules:
                if rule.Type() not in rule_types:
                    confirmation_instruction.ConfInstructionRules().Add(confirmation_instruction_rule)
        else:
            confirmation_instruction.ConfInstructionRules().Add(confirmation_instruction_rule)

        print('STP : ', confirmation_instruction_rule.Type())


def _find_confirmation_instruction_rule_by_template_name(confirmation_instruction, template_name):
    """
    Find an existing confirmation instruction rule by template name.
    """
    rules = []
    for confirmation_instruction_rule in confirmation_instruction.ConfInstructionRules():
        if confirmation_instruction_rule.TemplateChoiceList() is None:
            continue
        if confirmation_instruction_rule.TemplateChoiceList().Name() == template_name:
            rules.append(confirmation_instruction_rule)

    return rules


def _get_party_data_from_workbook(input_file_path):
    """
    Get a list of party data objects for the data contained in the
    workbook represented by a specified path.
    """
    column_list = _get_workbook_column_list()
    party_data_class = collections.namedtuple('PartyData', column_list)
    party_data = list()
    with xlrd.open_workbook(input_file_path) as workbook:
        for sheet in workbook.sheets():
            if sheet.name == 'Clean' or sheet.name == 'Sheet1':
                sheet_party_data = _get_party_data_from_sheet(party_data_class,
                                                              sheet, column_list)
                party_data.extend(sheet_party_data)
    return party_data


def _get_workbook_column_list():
    """
    Get the list of expected workbook columns.
    """
    return [
        'Name',
        'Full_Name',
        'Contact_Name',
        'Address',
        'Address2',
        'City',
        'Country',
        'Zipcode',
        'Attention',
        'Telephone',
        'Fax',
        'Email'
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
    print(expected_number_of_columns)
    print(sheet.ncols)
    if sheet.ncols != expected_number_of_columns:
        exception_message = "Expecting {expected} workbook columns, {encountered} "
        exception_message += "encountered on sheet '{}'."
        raise ValueError(exception_message.format(
            expected=expected_number_of_columns,
            encountered=sheet.ncols
        ))


def _get_party_data_from_row(party_data_class, sheet, row_index, column_list):
    """
    Get a party data object for the data on a specified sheet row.
    """
    cell_values_by_column_name = {}
    for column_index in range(sheet.ncols):
        column_name = column_list[column_index]
        cell_values_by_column_name[column_name] = str(sheet.cell(row_index, column_index).value)
    return party_data_class(**cell_values_by_column_name)
