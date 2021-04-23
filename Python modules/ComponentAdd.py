'''
Description
This code is called by the ASQL function called ComponentAdd. It searches for all userprofiles that contains a specified component and then adds another specified component to that profile.

Date            Who                     What
14/10/2009      Willie van der Bank     Created
06/11/2009      Willie van der Bank     Added delete section
09/11/2009      Willie van der Bank     Added Main section to read from file
'''

import ael

def doComponentAdd(temp,prfnbr,compnbr,*rest):
    UP = ael.UserProfile[prfnbr]
    PC = UP.profile_components()[0]
    new_pc = PC.new()
    new_pc.compnbr = compnbr
    new_pc.commit()
    ael.poll()
    return 'Success'
    
def doComponentDelete(temp,prfnbr,compnbr,*rest):
    UP = ael.UserProfile[prfnbr]
    UPC = UP.clone()
    for PC in UPC.profile_components():
        if PC.compnbr.compnbr == compnbr:
            print ''
            PC.delete()
            UPC.commit()
            ael.poll()
    return 'Success'

def Main(path):
    infile = open(path, 'r')
    for line in infile:
            FS = line
            Profile = FS.split(',')[0]
            Component = FS.split(',')[1]
            Type = FS.split(',')[2]
            Action = FS.split(',')[3]
            try:
                prfnbr = ael.UserProfile[Profile].profnbr
            except:
                a = 1
            components = ael.Component
            for i in components:
                if i.compname == Component and i.type == Type:
                    compnbr = i.compnbr
            if Action == 'Add':
                try:
                    doComponentAdd(1, prfnbr, compnbr)
                    #print Profile, Component, Type, Action
                except Exception, e:
                    a = 1
                    print e
                    print Profile, Component, Type, Action
            elif Action == 'Delete':
                doComponentDelete(1, prfnbr, compnbr)
                #print Profile, Component, Type, Action
    infile.close()

Main('F:\\ComponentAdd.csv')
