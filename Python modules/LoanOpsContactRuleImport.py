import acm, string
from xlrd import open_workbook
from PartyStaticSetup import AddConfirmationInstructions as addConfInstr

path = 'Y:/Jhb/Secondary Markets IT Deployments/FA/Change Pending/parties.xlsx'


def _get_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('Counterparty List')
        data = []
        error_list = []
        for row in sheet.get_rows():
            party_name = row[0].value
            data.append(party_name)
        return data
    except Exception as Ex:
        print(Ex)


def get_contact(party_id):
    party = acm.FParty[party_id]
    for contact in party.Contacts():
        if 'LOAN_OPS_NOTICE' in contact.Fullname():
            return contact

    return None


def create_contact_rule(contact):
    if contact:
        rule_events = []
        for rule in contact.ContactRules():
            rule_events.append(rule.EventChlItem().Name())

        if 'Loan Ops Commitment Fee Amendment' not in rule_events:
            new_contact_rule = acm.FContactRule()
            new_contact_rule.Acquirer = acm.FParty['PRIMARY MARKETS']
            new_contact_rule.Contact = contact
            new_contact_rule.InsType('Curr')
            new_contact_rule.EventChlItem('Loan Ops Commitment Fee Amendment')
            new_contact_rule.Commit()

    return None


def add_confo_instructions(party):
    names = [conf_instruction.Name() for conf_instruction in party.ConfInstructions()]
    if 'Loan Ops Commitment Fee Amendment' not in names:
        transport = 'Email'
        eventList = acm.FChoiceList.Select('list="Event" and name=Loan Ops Commitment Fee Amendment')[0]
        templateList = acm.FChoiceList.Select('list="Conf Template" and name=ABSA_Commitment_Fee_Invoice')[0]
        acquirer = acm.FParty['PRIMARY MARKETS']

        ci = acm.FConfInstruction()
        ci.Counterparty(party)
        ci.InsType('Curr')
        ci.Active(True)
        ci.Transport(transport)
        try:
            ci.Commit()
        except Exception as e:
            print(("Can't commit conf instruction: %s %s" % (party, e)))

        new_ci = acm.FConfInstruction[ci.Oid()]
        new_ci.InternalDepartment(acquirer)
        new_ci.EventChlItem(eventList)
        new_ci.Name('Commitment Fee Amendment')

        rule = acm.FConfInstructionRule()
        rule.ChaserCutoffMethod('None')
        rule.ChaserCutoffPeriodCount(0)
        rule.ConfInstruction(ci)
        rule.Type('Default')
        rule.TemplateChoiceList(templateList)

        try:
            rule.Commit()
        except Exception as e:
            print(("Can't commit conf instruction rule:%s %s" % (party, e)))


def upload_data():
    data = _get_data(path)
    error_list = []
    success = []

    for key in data:
        try:
            if key == 'C:Party':
                continue
            contact = get_contact(str(key))
            if contact:
                new_contact_rule = create_contact_rule(contact)
                add_confo_instructions(acm.FParty[str(key)])
                print("Added contact rule for %s" % str(key))
                success.append(key)
        except Exception as Ex:
            error_list.append(key)
            print(Ex)
    return error_list, success


def upload_acc_contact():
    key = 'PRIMARY MARKETS'
    contact = get_contact(str(key))
    if contact:
        new_contact_rule = create_contact_rule(contact)


data = upload_data()
print("fail list", data[0])
print("succesfully list", data[1])
