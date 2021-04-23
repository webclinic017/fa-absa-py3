import os
import acm, csv
from at_ael_variables import AelVariableHandler
import traceback

msgBox = acm.GetFunction('msgBox', 3)
FILETYPE = 'csv'
DELIMITER = ','
IMPORT_FILE = 'Create import file'
GET_FROM_FILE = 'Import from file'

attributes_to_exclude = [
    'CreateTime',
    'CreateUser',
    'Oid',
    'UpdateTime',
    'UpdateUser',
    'VersionId',
    'RecordType',
    'FourEyeOn',
    'ArchiveStatus',
    'Authorizer',
    'ExternalCutOff',
    'InternalCutOff',
    'C:Name'
]


class Simple_Object_Class():

    def __init__(self, main_attribute, object, prefix=''):
        self.main_attribute = main_attribute
        self.object = object
        self.prefix = prefix
        self.sorted_attributes = self._get_sorted_attributes()

    def _capitalize_first_letter(self, text):
        text = text[0].upper() + text[1:]
        return text

    def _sort_main_attribute_first(self, attribute_list):
        if self.main_attribute:
            attribute_list.remove(self.main_attribute)
            attribute_list = [self.main_attribute] + attribute_list
        return attribute_list

    def _add_prefix(self, attribute_list):
        if self.prefix:
            for i in range(len(attribute_list)):
                attribute_list[i] = self.prefix + ':' + attribute_list[i]
        return attribute_list

    def _get_sorted_attributes(self):
        str_obj = str(self.object)
        attribute_list = str_obj.split('\n')

        converted_attribute_list = []
        for i in attribute_list:
            if i.count('=') == 1:  # this will exclude references to other objects like add_infos
                equal_sign_location = i.find('=')
                attribute = i[:equal_sign_location].strip(' ')
                attribute = self._capitalize_first_letter(attribute)
                converted_attribute_list.append(attribute)

        converted_attribute_list = self._sort_main_attribute_first(converted_attribute_list)
        converted_attribute_list = self._add_prefix(converted_attribute_list)

        for attribute_excl in attributes_to_exclude:
            for attribute_in_list in converted_attribute_list:
                if attribute_excl == attribute_in_list:
                    converted_attribute_list.remove(attribute_in_list)

        return converted_attribute_list


def append_add_infos(object_class, object_type):
    attribute_list = object_class.sorted_attributes
    add_info_object_class = Simple_Object_Class('', object_class.object.AdditionalInfo(), 'AI')
    attribute_list += add_info_object_class.sorted_attributes
    return attribute_list


def set_attributes(obj, attribute, value):
    if 'AI:' in attribute:
        attribute = attribute.strip('AI:')
        obj = obj.AdditionalInfo()
    obj.SetProperty(attribute, value)


def _lower_first_letter(text):
    text = text[0].lower() + text[1:]
    return text


def filename(fieldValues):
    custom_name = ael_variables.get("object_type").value + "_DataFile." + FILETYPE
    directory = r"C:\Temp"
    ael_variables.get("filename").value = os.path.join(directory, custom_name)


ael_variables = AelVariableHandler()
ael_variables.add(
    "object_type",
    label="Object type:",
    collection=['Account', 'ConfirmationInstruction', 'Contact', 'ContactRule', 'Party', 'PartyAlias',
                'SettlementInstruction'],
    default='Party',
    hook=filename,
)
ael_variables.add(
    "action",
    label="Import/Export:",
    collection=[IMPORT_FILE, GET_FROM_FILE],
    default=IMPORT_FILE
)
ael_variables.add_input_file(
    "filename",
    cls="FFileSelection",
    label="Filename"
)


def ael_main(argv):
    filename = argv['filename'].AsString()
    action = argv['action']
    object_type = argv['object_type']

    if object_type == 'Party':
        object_class = Simple_Object_Class('Name', acm.FParty())
        object_class.sorted_attributes = append_add_infos(object_class, object_type)
    elif object_type == 'Contact':
        object_class = Simple_Object_Class('Party', acm.FContact())
        object_class.sorted_attributes = append_add_infos(object_class, object_type)
    elif object_type == 'PartyAlias':
        object_class = Simple_Object_Class('Party', acm.FPartyAlias())
    elif object_type == 'Account':
        object_class = Simple_Object_Class('Party', acm.FAccount())
    elif object_type == 'ContactRule':
        object_class = Simple_Object_Class('', acm.FContactRule())
        contact_class = Simple_Object_Class('Party', acm.FContact(), 'C')
        object_class.sorted_attributes = contact_class.sorted_attributes + object_class.sorted_attributes
    elif object_type == 'ConfirmationInstruction':
        object_class = Simple_Object_Class('', '')
        object_class.sorted_attributes = ['Party', 'Choose Static Type', 'StriataAcceptReject', 'StriataPassword']
    elif object_type == 'SettlementInstruction':
        object_class = Simple_Object_Class('', '')
        object_class.sorted_attributes = ['Party', 'Name', 'AccountType', 'Acquirer', 'Instype', 'Currency',
                                          'TradeSettleCategory', 'InsSettleCategory', 'OptKey1', 'CashFlowType',
                                          'AccountName', 'EffectiveFrom']

    if action == IMPORT_FILE:
        directory, file_name = os.path.split(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w") as file:
            for i in object_class.sorted_attributes:
                file.write(i)
                file.write(DELIMITER)
        output_string = ("Import file created: %s" % filename)

    elif action == GET_FROM_FILE:

        try:
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)

                output_string = ("Import file %s is empty" % filename)

                for row in reader:
                    # obj = object_class.object  # possible improvement

                    if object_type in ('Contact', 'Party', 'PartyAlias'):

                        if object_type == 'Contact':
                            obj = acm.FContact()
                        elif object_type == 'PartyAlias':
                            obj = acm.FPartyAlias()
                        elif object_type == 'Party':
                            obj = acm.FParty[row['Name']]
                            if not obj:
                                if row['Type'] == 'Issuer':
                                    obj = acm.FIssuer()
                                elif row['Type'] == 'Broker':
                                    obj = acm.FBroker()
                                elif row['Type'] == 'Client':
                                    print("I am creating a client")
                                    obj = acm.FClient()
                                elif row['Type'] == 'Counterparty':
                                    obj = acm.FCounterParty()
                                else:
                                    obj = acm.FParty()

                        for attribute_name in row:
                            if row[attribute_name]:
                                set_attributes(obj, attribute_name, row[attribute_name])

                        obj.Commit()

                    elif object_type == 'Account':
                        obj = acm.FAccount()

                        for attribute_name in row:
                            if row[attribute_name]:
                                if attribute_name == 'Currency' and row[attribute_name] == 'ALL':
                                    set_attributes(obj, attribute_name, None)
                                    continue
                                if attribute_name in ['DataSourceScheme', 'DataSourceScheme2', 'DataSourceScheme3']:
                                    if attribute_name[-1] == 'e':
                                        counter = ''
                                    else:
                                        counter = attribute_name[-1]
                                    Alias = row[attribute_name]
                                    PartyName = row['CorrespondentBank' + counter]
                                    alias_object = acm.FPartyAlias.Select(
                                        "party = '%s' and alias = '%s' and type = 'DataSourceScheme'" % (
                                        PartyName, Alias))
                                    if alias_object:
                                        alias_object = alias_object[0]
                                    else:
                                        output_string = (
                                                    "Import of file %s failed!. Alias could not be found! See log for further detail." % filename)
                                        print(('Swift alias %s does not exist on party %s! ' % (Alias, PartyName)))
                                    set_attributes(obj, attribute_name, alias_object)
                                    continue

                                if ('Bic' in attribute_name) or (attribute_name == 'NetworkAlias'):
                                    if 'Bic' in attribute_name:
                                        counter = ''
                                        if len(attribute_name) > 3:
                                            counter = attribute_name[3]
                                        PartyName = row['CorrespondentBank' + counter]
                                    else:
                                        PartyName = row['Party']
                                    Alias = row[attribute_name]
                                    alias_object = acm.FPartyAlias.Select(
                                        "party = '%s' and alias = '%s' and type = 'SWIFT'" % (PartyName, Alias))
                                    if alias_object:
                                        alias_object = alias_object[0]
                                    else:
                                        output_string = (
                                                    "Import of file %s failed!. Alias could not be found! See log for further detail." % filename)
                                        print(('Swift alias %s does not exist on party %s! ' % (Alias, PartyName)))
                                    set_attributes(obj, attribute_name, alias_object)
                                    continue
                                else:
                                    set_attributes(obj, attribute_name, row[attribute_name])

                        obj.Commit()

                    elif object_type == 'ContactRule':
                        obj = acm.FContactRule()
                        parent_object_variables = ''

                        for attribute_name in row:
                            if row[attribute_name]:
                                if ':' in attribute_name:
                                    pos = attribute_name.find(':')
                                    parent_object_variables += _lower_first_letter(attribute_name[pos + 1:]) + ' = "' + \
                                                               row[attribute_name] + '" and '
                                else:
                                    set_attributes(obj, attribute_name, row[attribute_name])

                        contact_object = acm.FContact.Select(parent_object_variables)
                        if not contact_object:
                            output_string = (
                                        "Import of file %s failed!. Contact could not be found! See log for further detail." % filename)
                            print('Contact not found: ', parent_object_variables)
                            break
                        contact_object = acm.FContact.Select(parent_object_variables)[0]

                        obj.Contact(contact_object)

                        obj.Commit()

                    elif object_type == 'ConfirmationInstruction':
                        from PartyStaticSetup import AddPartyStatic, AddConfirmationInstructions

                        party = acm.FParty[row['Party']]
                        if not party:
                            output_string = ("Import of file %s failed!. Party %s does not exist!" % (
                            filename, row['Party']))
                            break
                        static_type = row['Choose Static Type']
                        striata_accept_reject = row['StriataAcceptReject']
                        striata_password = row['StriataPassword']

                        if row['Choose Static Type']:
                            static_type
                        if static_type == 'Swift':
                            transport_mechanism = 'Network'
                        elif static_type == 'Standard PDF':
                            transport_mechanism = 'Email'
                        if static_type == 'Encrypted PDF':
                            transport_mechanism = 'File'
                            AddPartyStatic.addMain(party, striata_accept_reject, striata_password)

                        chaser_cutoff_method = 'None'
                        chaser_cutoff_days = 0

                        AddConfirmationInstructions.addConfInstrToParty(party, chaser_cutoff_method, chaser_cutoff_days,
                                                                        transportStr=transport_mechanism)

                    elif object_type == 'SettlementInstruction':
                        from SAGEN_Add_SSI_ASQLQuery import main

                        convert_to_list = lambda x: '' if x.split(',') == [''] else x.split(',')

                        main(row['Party'], row['Name'], row['AccountType'], True,
                             convert_to_list(row['Acquirer']), convert_to_list(row['Instype']),
                             convert_to_list(row['Currency']),
                             convert_to_list(row['TradeSettleCategory']), convert_to_list(row['InsSettleCategory']),
                             convert_to_list(row['OptKey1']),
                             convert_to_list(row['CashFlowType']), row['AccountName'], row['EffectiveFrom'])

                    print('Processed:', row)

                    output_string = ("Import of file %s completed." % filename)

        except Exception as e:
            print('Import issue on this line:')
            print(row)
            print(e)
            traceback.print_exc()
            raise e

    print(output_string)
    msgBox(__name__, output_string, 0)


def ASQL(*rest):
    acm.RunModuleWithParameters(__name__, 'Standard')
    return 'Done'
