import acm, string
from xlrd import open_workbook
from PartyStaticSetup import AddConfirmationInstructions as addConfInstr

data_path = 'Y:/Jhb/Secondary Markets IT Deployments/FA/Change Pending/Party_VAT_FgnParty.xlsx'
set_cat_data_path = 'Y:/Jhb/Secondary Markets IT Deployments/FA/Change Pending/Trade_SettleCategory_21May.xlsx'
path = 'Y:/Jhb/Secondary Markets IT Deployments/FA/Change Pending/parties.xlsx'


def _get_confo_instr_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('parties')
        data = []
        error_list = []
        for row in sheet.get_rows():
            party_name = row[0].value
            if party_name =='Counterparty':
                continue
            data.append(party_name)
        return data
    except Exception as Ex:
        print Ex


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

        if 'Loan Ops Commitment Fee' not in rule_events:
            new_contact_rule = acm.FContactRule()
            new_contact_rule.Acquirer = acm.FParty['PRIMARY MARKETS']
            new_contact_rule.Contact = contact
            new_contact_rule.InsType('Curr')
            new_contact_rule.EventChlItem('Loan Ops Commitment Fee')
            new_contact_rule.Commit()
        if 'Loan Ops Commitment Fee Future Date' not in rule_events:
            new_contact_rule_future = acm.FContactRule()
            new_contact_rule_future.Acquirer = acm.FParty['PRIMARY MARKETS']
            new_contact_rule_future.Contact = contact
            new_contact_rule_future.InsType('Curr')
            new_contact_rule_future.EventChlItem('Loan Ops Commitment Fee Future Date')
            new_contact_rule_future.Commit()

    return None


def add_confo_instructions(party):
    names = [conf_instruction.Name() for conf_instruction in party.ConfInstructions()]
    if 'Curr Commitment Fee'not in names:
        transport ='Email'
        eventList = acm.FChoiceList.Select('list="Event" and name=Loan Ops Commitment Fee')[0]
        templateList = acm.FChoiceList.Select('list="Conf Template" and name=ABSA_Commitment_Fee_Invoice')[0]
        acquirer = acm.FParty['PRIMARY MARKETS']

        ci = acm.FConfInstruction()
        ci.Name('Commitment Fee') 
        ci.Counterparty(party)
        ci.InsType('Curr')
        ci.Active(True)
        ci.EventChlItem(eventList)
        ci.Transport(transport)

        try:
            ci.Commit()
        except Exception as e:
            print("Can't commit conf instruction: %s %s" % (party, e))
            

        new_ci = acm.FConfInstruction[ci.Oid()]
        new_ci.InternalDepartment(acquirer)
        
        rule = acm.FConfInstructionRule()
        rule.ChaserCutoffMethod('None')
        rule.ChaserCutoffPeriodCount(0)
        rule.ConfInstruction(ci)
        rule.Type('Default')
        rule.TemplateChoiceList(templateList)
        
        try:
            rule.Commit()
        except Exception:
            print("Can't commit conf instruction rule:%s %s" % (party, e))


def add_confo_instructions_future_date(party):
    names = [conf_instruction.Name() for conf_instruction in party.ConfInstructions()]
    if 'Commitment Fee Future Date'not in names:
        transport ='Email'
        eventList = acm.FChoiceList.Select('list="Event" and name=Loan Ops Commitment Fee Future Date')[0]
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
            print("Can't commit conf instruction: %s %s" % (party, e))
        
        new_ci = acm.FConfInstruction[ci.Oid()]
        new_ci.InternalDepartment(acquirer)
        new_ci.EventChlItem(eventList)
        new_ci.Name('Commitment Fee Future Date') 
        
        rule = acm.FConfInstructionRule()
        rule.ChaserCutoffMethod('None')
        rule.ChaserCutoffPeriodCount(0)
        rule.ConfInstruction(ci)
        rule.Type('Default')
        rule.TemplateChoiceList(templateList)
        
        try:
            rule.Commit()
        except Exception:
            print("Can't commit conf instruction rule:%s %s" % (party, e))

            
def upload_data():
    data = _get_confo_instr_data(path)
    error_list = []
    success = []

    for d in data:
        try:
            contact = get_contact(str(d))
            if contact:
                new_contact_rule = create_contact_rule(contact)
                add_confo_instructions(acm.FParty[str(d)])
                add_confo_instructions_future_date(acm.FParty[str(d)])
                print "Added contact rule for %s" % str(d)
                success.append(d)
        except Exception as Ex:
            error_list.append(d)
            print Ex
    return error_list, success


def _get_trade_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('Sheet1')
        data = {}
        error_list = []
        for row in sheet.get_rows():
            if row[0].value == 'Trade Nbr':
                continue
            trade_no = str(row[0].value).split('.')[0]
            agent = row[1].value
            data.update({trade_no:'%s' % agent})
        return data
    except Exception as Ex:
        print Ex

def _get_party_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('Sheet2')
        data = {}
        error_list = []
        for row in sheet.get_rows():
            if row[0].value == 'Party ID':
                continue
            party_name = str(row[0].value)
            forgein = str(row[1].value)
            vat_no = row[2].value
            data.update({party_name:[forgein, vat_no]})
        return data
    except Exception as Ex:
        print Ex


def _get_agent_data(file):
    try:
        book = open_workbook(file, on_demand=True)
        sheet = book.sheet_by_name('Sheet1')
        data = {}
        error_list = []
        for row in sheet.get_rows():
            if row[0].value == 'Trade Nbr':
                continue
            trade_no = str(row[0].value).split('.')[0]
            agent = row[1].value
            data.update({trade_no:'%s' % agent})
        return data
    except Exception as Ex:
        print Ex

def add_vat_number(key, vat_number):
    try:
        party = acm.FParty[str(key)]
        party = party.StorageImage()
        party.AdditionalInfo().Vat_Number(str(str(vat_number).split('.')[0]))
        party.Commit()
        print "Added %s Val Number for :%s" % (str(vat_number).split('.')[0], key)
    except Exception as ex:
        print ex, key

def set_foreign_party(key, value):
    try:
        party = acm.FParty[key]
        party = party.StorageImage()
        party.Free2ChoiceList(value)
        party.Commit()
        print "Setting Foreign Party Value For %s" % party.Name()
    except Exception as ex:
        print ex, key
            
def upload_agent():
    data = _get_agent_data(data_path)
    error_list = []
    success = []
    
    
    for key, value in data.items():
        try:
           trade = acm.FTrade[key]
           value = str(value).strip()
           if value == 'ABSA':
               value = 'Absa Bank Limited'
           trade.AdditionalInfo().PM_FacilityAgent(value)
           trade.Commit()
           print trade.Oid(), trade.AdditionalInfo().PM_FacilityAgent()

        except Exception as Ex:
            error_list.append(key)
            print Ex
    return error_list, success
    

def upload_party():
    data = _get_party_data(data_path)
    error_list = []
    success = []

    for key, value in data.items():
        try:
            if value[1]:
                add_vat_number(key, value[1])
            if value[0] == 'Yes':
                set_foreign_party(key, value[0])
        except Exception as Ex:
            error_list.append(key)
            print Ex
    return error_list, success

def upload_set_cat():
    data = _get_trade_data(set_cat_data_path)
    error_list = []
    success = []

    for key, value in data.items():
        try:
            print key, value
            trade = acm.FTrade[key]
            trade.SettleCategoryChlItem(str(value))
            trade.Commit()
        except Exception as Ex:
            error_list.append(key)
            print Ex
    return error_list, success


print "-----------PARTY UPLOAD------------"
print upload_party()
print "-----------SETTLE CAT UPLOAD------------"
print upload_set_cat()
print "----CONFO INSTR UPLOAD---------"
print upload_data()

