'''
MODULE
    AddConfirmationInstructions - Add Conf instructions to parties that havent yet.

DESCRIPTION
    creates confirmation instructions and conf instruction rules

HISTORY

2015-09-17                      Sanele Macanda          Adaptiv go-live
2016-03-08      Abitfa 4042     Evgeniya Baskaeva       Modified to enable MT300s
2016-03-22      Abitfa 4054     Willie van der Bank     Modified for STP
2016-06-10      DEMAT           Vojtech Sidorin         Clean-up the code
2016-08-30      ABITFA 4424     Gabriel Marko           Demat Confirmation Instructions
2017-06-20      CHNG0004671894  Willie van der Bank     Added File option
'''

import acm
import at_logging

LOGGER = at_logging.getLogger()

MAPPINGS = {
    # InsCategory
    'Demat':
        {
            # InsType
            'None':
                {
                    # (Event, Transport): Template
                    ('', 'Network') : 'SWIFT',
                    ('New Trade', 'Email'): 'ABSA_FI_Generic_Main'
                },
        },
    '':
        {
            'Deposit':
                {
                    ('Account Ceded', None): 'ABSA_Deposit_Cede_Main',
                    ('Close', None): 'ABSA_Deposit_Close',
                    ('New Trade Call', None): 'ABSA_Call_Deposit_Opening_Main',
                    ('Novation', None): 'ABSA_Deposit_Main',
                    ('Partial Close', None): 'ABSA_Deposit_Close',
                    ('Prolong Deposit', None): 'ABSA_Deposit_Main',
                    ('Rate Fixing Call', None): 'ABSA_Rate_Fixing_Main',
                    ('Rate Fixing', None): 'ABSA_Rate_Fixing_Main',
                },
            'Option':
                {
                    ('New Trade', None): 'SWIFT'
                },
        }
}


def get_event_template_mapping(transType):

    if transType == 'Email':
        MAPPINGS['']['Deposit'][('New Trade', 'Email')] = 'ABSA_Deposit_Main'
        MAPPINGS['']['Deposit'][('Adjust Deposit', 'Email')] = 'ABSA_Deposit_Adjust_Main'
        MAPPINGS['']['Deposit'][('Maturity Notice', 'Email')] = 'ABSA_Maturity_Notice'
    elif transType == 'File':
        MAPPINGS['']['Deposit'][('New Trade', 'File')] = 'ABSA_Deposit_Main'
        MAPPINGS['']['Deposit'][('Adjust Deposit', 'File')] = 'ABSA_Deposit_Adjust_Main'
        MAPPINGS['']['Deposit'][('Maturity Notice', 'File')] = 'ABSA_Maturity_Notice'
    else:
        MAPPINGS['']['Deposit'][('New Trade', 'Network')] = 'SWIFT'
        MAPPINGS['']['Deposit'][('Adjust Deposit', 'Email')] = 'ABSA_Deposit_Adjust_Main'
        MAPPINGS['']['Deposit'][('Maturity Notice', 'Network')] = 'ABSA_Maturity_Notice'
        MAPPINGS['']['None'] = {('', 'Network'): 'SWIFT'}

    flattened_list = [
        [
            ins_cat,
            ins,
            et,
            MAPPINGS[ins_cat][ins][et]
        ]
        for ins_cat in MAPPINGS
        for ins in MAPPINGS[ins_cat]
        for et in MAPPINGS[ins_cat][ins]
    ]

    return flattened_list


def functional_name(name):
    for ins_cat in MAPPINGS:
        if name.startswith(ins_cat):
            name = name.lstrip(ins_cat).lstrip()
    return name.replace('Email', '').replace('Network', '')


def addConfInstrToParty(party,
                        chaserCutoffMethod,
                        chaserCutoffDays,
                        transportStr=None,
                        instypes=None,
                        activateExisting=False):

    if instypes is None:
        instypes = get_event_template_mapping(transportStr)


    existing_conf_instructions = []
    inactive_conf_instructions = {}


    for conf_instruction in party.ConfInstructions():
        func_name = functional_name(conf_instruction.Name())
        existing_conf_instructions.append(func_name)
        if not conf_instruction.Active():
            inactive_conf_instructions[func_name] = conf_instruction


    for ins_cat, ins_type, event_transport, template in instypes:

        event, transport = event_transport
        if not transport:
            transport = transportStr
            transport = 'Network' if ins_type in ('None') else 'Email'
            if event == 'New Trade' and ins_type in ('Deposit', 'Option') and transportStr == 'Network':
                transport = 'Network'

        try:
            eventList = False
            if event:
                eventList = acm.FChoiceList.Select('list="Event" and name=%s' % event)[0]
            templateList = acm.FChoiceList.Select('list="Conf Template" and name=%s' % template)[0]
        except Exception:
            LOGGER.exception('Incomplete choice lists. Cant add Conf Instruction:')
            continue

        # dont override existing conf instructions
        ci_name = ('%s %s %s %s' % (ins_cat, ins_type, event, transport)).lstrip()
        func_name = functional_name(ci_name)

        if func_name in existing_conf_instructions:
            # activate if requested
            if activateExisting:
                if func_name in inactive_conf_instructions:
                    ci = inactive_conf_instructions[func_name]
                    ciC = ci.Clone()
                    ciC.Active(True)
                    ci.Apply(ciC)
                    try:
                        ci.Commit()
                    except Exception:
                        LOGGER.exception("Can't activate conf instruction:")
            continue

        acm.BeginTransaction()

        # Create Conf Instruction
        ci = acm.FConfInstruction()
        ci.Counterparty(party)
        ci.InternalDepartment()
        ci.Active(True)
        ci.InsType(ins_type)

        if ins_cat:
            ci.SettleCategoryChlItem(ins_cat)

        if ins_type == 'Option':
            ci.UndInsType('Curr')

        ci.Name(ci_name)

        if eventList:
            ci.EventChlItem(eventList)

        ci.Transport(transport)

        try:
            ci.Commit()
        except Exception:
            LOGGER.exception("Can't commit conf instruction:")

        # Create Conf Instruction rule
        rule = acm.FConfInstructionRule()

        rule.Stp(str(ci_name.replace(' ', '') != 'NoneNetwork'))
        rule.ChaserCutoffMethod(chaserCutoffMethod)
        rule.ChaserCutoffPeriodCount(chaserCutoffDays)
        rule.ConfInstruction(ci)
        rule.Type('Default')
        rule.TemplateChoiceList(templateList)

        try:
            rule.Commit()
        except Exception:
            LOGGER.exception("Can't commit conf instruction rule:")

        try:
            acm.CommitTransaction()
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception("Can't commit conf instruction and rule:")
            LOGGER.info('Counterparty_Name: %s', party.Name())
