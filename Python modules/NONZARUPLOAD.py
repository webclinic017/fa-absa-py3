#Upload Non ZAR Additional Infos and Choicelists

import ael, string

path = 'Y:\Jhb\Secondary Markets IT\DEPLOYMENTS\Current\381305 (Non ZAR Deal Ticket capture and PDF printing) -hoonherm\\'

def uploadAddInfo(file, clone):
    filename = path + 'Add Info upload\\' + file +  '.csv'

    try:
        f = open(filename)
    except:
        print 'Could not open file'
        return
    
    #read over first line
    line = f.readline()   
    for line in f:
        l = string.split(line, ',')
        new_ai = ael.AdditionalInfoSpec[clone].new()
        new_ai.field_name = l[0]
        new_ai.description = l[1]
        new_ai.default_value = l[2]
        new_ai.rec_type = l[3]
        new_ai.subrec_mask1 = int(l[4])
        new_ai.subrec_mask2 = 0
        #clone a previous one with a certain rec ref
        #new_ai.data_typegrp = l[5]
        #new_ai.data_typetype = l[6]
        #Subrec mask refers to only deposit screens
        try:
            new_ai.commit()
            print l[0], 'committed'
        except:
            print l[0], 'not commited'

uploadAddInfo('Choicelist', 'Commodity Type')
uploadAddInfo('Double', 'Spread Trigger')
uploadAddInfo('String', 'XtpJseRef')


def upload(name):
    filename = path + 'Choicelist upload\\' + name +  '.csv'

    #Add the choicelist under MASTER
    new_choice = ael.ChoiceList.new()
    new_choice.entry = name
    new_choice.list = 'MASTER'
    new_choice.description = name
    try:
        new_choice.commit()
        print name, 'committed'
    except:
        print name, 'not commited'

    try:
        f = open(filename)
    except:
        print 'Could not open file'
        return
    
    #read over first line
    line = f.readline()
    #Add the choiclist items
    for line in f:
        l = string.split(line, ',')
        entry = l[0]
        desc = l[1].rstrip('\n')

        new_choice = ael.ChoiceList.new()
        new_choice.entry = entry
        new_choice.list = name
        new_choice.description = desc
        try:
            new_choice.commit()
            print entry, 'committed'
        except:
            print entry, 'not commited'


upload('NonZAR_Deal Method')
upload('NonZAR_Deal Type')

def uploadChoice(name):
    filename = path + 'Choicelist upload\\' + name +  '.csv'

    try:
        f = open(filename)
    except:
        print 'Could not open file'
        return
    
    #read over first line
    line = f.readline()
    #Add the choiclist items
    for line in f:
        l = string.split(line, ',')
        entry = l[0]
        desc = l[1].rstrip('\n')

        new_choice = ael.ChoiceList.new()
        new_choice.entry = entry
        new_choice.list = name
        new_choice.description = desc
        try:
            new_choice.commit()
            print entry, 'committed'
        except:
            print entry, 'not commited'


uploadChoice('Funding Instype')
