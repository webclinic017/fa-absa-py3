"""
MODULE
    PartyStaticSetup - Provides menu item to create
    party static relevant for the specific type of party

History
=======
2016-06-09                      Vojtech Sidorin DEMAT: Hide the MM Demat tick box in the GUI.
2016-06-10                      Vojtech Sidorin DEMAT: Clean-up the code.
2017-06-20      CHNG0004671894  Willie vd Bank  Initial deployment. Copied from existing module
                                                called ConfInstructionFactory.
"""

import acm
import AddConfirmationInstructions
reload(AddConfirmationInstructions)
import AddPartyStatic
#reload(AddPartyStatic)
from at_ael_variables import AelVariableHandler

ael_gui_parameters = {'runButtonLabel': '&&Create...',
                      'hideExtraControls': True,
                      'windowCaption': 'Perform Static Setup',
                      'closeWhenFinished': True}

staticType = ['Swift', 'Standard PDF', 'Encrypted PDF']
StriataAcceptRejectList = [cl.Name() for cl in acm.FChoiceList.Select('') if cl.List() == 'StriataAcceptReject']
#transportTypes = ['Network','Email']

settings = {'chaserCutoffMethod':'None',
            'chaserCutoffDaysClient':0,
            'chaserCutoffDaysIntern Dept':0,
            'chaserCutoffDaysCounterparty':0}

#read parameters
params = acm.FExtensionContext['Standard'].GetAllExtensions('FParameters')
for param in params:
    if param.Name().AsString() == 'PartyStaticSetup':
        param = param.Value()
        for attrib in param.Keys():
            strAttrib = attrib.AsString()
            if strAttrib in settings:
                settings[strAttrib] = param.GetString(strAttrib)

def item_find(list, item):
    try:
        if len(list) == 0:
            return False
        return (True if list.index(item) >= 0 else False)
    except Exception:
        return False

'''
def get_ael_variables():
    map = []

    map.append(['staticType','Choose Static Type','string',staticType,staticType[0],1,0,'', None])
    #map.append(['transportMechanism','Choose Transport Mechanism','string',transportTypes,transportTypes[0],1,0,'', None])
    map.append(['chaserCutoffMethod', 'Chaser Cutoff Method', 'string', ['Business Days', 'Calendar Days', 'None'],settings['chaserCutoffMethod'],1,0])
    map.append(['chaserCutoffDaysClient', 'Chaser Cutoff Days for Clients', 'int', range(1,15), settings['chaserCutoffDaysClient'], 1, 0])
    map.append(['chaserCutoffDaysCounterparty', 'Chaser Cutoff Days for Counterparties', 'int', range(1,15), settings['chaserCutoffDaysCounterparty'], 1, 0])
    map.append(['chaserCutoffDaysIntern Dept', 'Chaser Cutoff Days for Internal Departments', 'int', range(1,15), settings['chaserCutoffDaysIntern Dept'], 1, 0])
    return map

ael_variables = get_ael_variables()
'''

def encrypted_PDF(fieldValues):
    static_type = ael_variables.get('staticType').value
    if static_type != 'Encrypted PDF':
        ael_variables.get('StriataAcceptReject').enabled = 'No'
        ael_variables.get('StriataPassword').enabled = 'No'
    else:
        ael_variables.get('StriataAcceptReject').enabled = 'Yes'
        ael_variables.get('StriataPassword').enabled = 'Yes'

ael_variables = AelVariableHandler()
ael_variables.add(
    "staticType",
    label="Choose Static Type",
    default=staticType[0],
    collection=staticType,
    cls='string',
    hook=encrypted_PDF
)

ael_variables.add(
    "StriataAcceptReject",
    label="StriataAcceptReject",
    collection=StriataAcceptRejectList,
    mandatory = False,
    cls='string'
)

ael_variables.add_bool(
    "StriataPassword",
    label="StriataPassword",
    default=False
)

def ael_main_ex(dict, customData):
    '''
        This function is called after clicking on the menu item

        We add the customData values, so we have access to the party
    '''
    dict['_customData'] = customData
    ael_main(dict)

def ael_main(dict):
    '''
        Main function, containing the actual functionality.
    '''
    staticType = dict['staticType']
    StriataAcceptReject = dict['StriataAcceptReject']
    if dict['StriataPassword']:
        StriataPassword = 'Yes'
    else:
        StriataPassword = 'No'
    party = dict['_customData']['customData']['party']
    shell = dict['_customData']['customData']['shell']
    #transportMechanism = dict['transportMechanism']
    #chaserCutoffMethod = dict['chaserCutoffMethod']
    #chaserCutoffDays = int(dict['chaserCutoffDays%s' % party.Type()])
        
    if staticType == 'Swift':
        transportMechanism = 'Network'
    elif staticType == 'Standard PDF':
        transportMechanism = 'Email'
    if staticType == 'Encrypted PDF':
        transportMechanism = 'File'
        AddPartyStatic.addMain(party, StriataAcceptReject, StriataPassword)
    
    chaserCutoffMethod = 'None'
    chaserCutoffDays = 0
    AddConfirmationInstructions.addConfInstrToParty(party, chaserCutoffMethod, chaserCutoffDays, transportStr=transportMechanism)
    
def run(eii):
    partydef = eii.ExtensionObject()
    party = partydef.CurrentObject()
    if not party:
        print 'Open a party'
        return
    if party.Oid() < 0:
        print 'Save party first'
    shell = partydef.Shell()

    customData = {'party' : party,
                    'shell' : shell}
    acm.RunModuleWithParametersAndData('PartyStaticSetup', 'Standard', customData)
