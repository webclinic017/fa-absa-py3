import acm
 
"""
Script that assists with the set up of PACE/APS configuration in Prime.
It performs various tasks - they should be clear from the tick boxes on the run script screen.
 
The basic assumption for this setup is that we will have an APS/CE/DC/calc user for each user group in FA
that will be using server side pace.
We place the calc user in the same user group with the users.
We assume user rights are given on group level, not individual user level.
The reason for this is to ensure the calc user has exactly the same user rights as the group.
We assume kerberos is used - if not remove the principal setting part and add password setting.
 
If a CE is not selected but distribution is switched on in a sheet, it will use local PACE - see 
prime .ini parameters that need to be set.
 
You need to set the DC (DCMain_name) as Distribution.Configuration on the Organisation level.
You need to setup an APS on the server for each user group - service name must match the APS in Prime.
You need to create TM worksheets that have Distribution switched on and has the CE selected corresponding
to the user group that will be using the sheet.
 
This setup is not ideal in terms of re-use of calculations, i.e. if 2 user groups have access to the same portfolios 
and use the same calculation settings, and want to see the same columns - the sheets will be calculated twice
on the server.  This is because each CE will have its own APS and therefore there will be no re-use between 
calculations for different user groups.
 
This setup is however good in terms of protecting the data from users that are not supposed to see the values.
We protect the CE to ensure only users in that user group can see/use it.  If you have World=Read CEs then it
is possible that users will have access to values that they should not have - note if the sheet contains portfolios
then there should not be an issue since Prime will know that the user cannot see/use the portfolio and therefore
the item will not be in the TM sheet, however if the sheet uses a Trade Filter or Query Folder, then all users have access
to the filter and via PACE calculations will get access to the full calculated values 
 
 
 
"""
 
ael_variables = [
    ['param_userGroups', 'User Groups', acm.FUserGroup, None, 'FO Africa Trader', 1, 1, 'User group to do setup for', None, 1],
    ['param_create_UserProfile', 'Create User Profile', 'bool', [True, False], True, 0, 0, 'Create UP', None, 1],
    ['param_create_CalcUser', 'Create Calculation User', 'bool', [True, False], True, 0, 0, 'Create CU', None, 1],
    
    ['param_create_CE', 'Create Calculation Environment', 'bool', [True, False], True, 0, 0, 'Create CE', None, 1],
    ['param_create_DC', 'Create Distribution Configuration', 'bool', [True, False], True, 0, 0, 'Create DC', None, 1],
    ['param_create_APS', 'Create APS', 'bool', [True, False], True, 0, 0, 'Create APS', None, 1],
    ['param_create_DCMain', 'Create/Update Main Distribution Configuration', 'bool', [True, False], True, 0, 0, 'Create/Update DC Main', None, 1]
 
 
]
 
UserGroup_strip = ' Trader' #string to strip from user group name before using in all other names (due to length restrictions)
APS_prefix      = 'APS_'
CE_prefix       = 'CE_'
CalcUser_prefix = 'APS_'
#CalcUser_kerb_principals = ['sysfauat@INTRANET.BARCAPINT.COM','sysfaprd@INTRANET.BARCAPINT.COM','sysfadev@INTRANET.BARCAPINT.COM']
CalcUser_kerb_principals = ['sysfaprd@INTRANET.BARCAPINT.COM']
CalcUser_profile= 'PACE_SERVER'                         #user profile given to PACE calc users
comps_to_add    = ['PaceConfiguration', 'PaceEngine']    #components to add to CalcUser_profile
DC_prefix       = 'DC_'
DCMain_name     = 'DC_USER_MAIN'
 
 
 
def ael_main(dict):
    userGroups = dict['param_userGroups']
    param_create_UserProfile    = dict['param_create_UserProfile']
    param_create_CalcUser       = dict['param_create_CalcUser']
    
    param_create_CE       = dict['param_create_CE']
    param_create_DC       = dict['param_create_DC']
    param_create_APS      = dict['param_create_APS']
    param_create_DCMain   = dict['param_create_DCMain']
    
    
    
    
    for userGroup in userGroups:
        userGroupName = userGroup.Name()
        print '\n...%s...' %userGroupName
        userGroupNameShort = userGroupName.replace(UserGroup_strip, '')
    
        if param_create_UserProfile:    create_UserProfile()
        if param_create_CalcUser:       create_CalcUser(userGroupNameShort, userGroupName)
        if param_create_CE:             create_CE(userGroupNameShort)
        if param_create_DC:             create_DC(userGroupNameShort)
        if param_create_APS:            create_APS(userGroupNameShort)
        if param_create_DCMain:         create_update_DCMain(userGroupNameShort)
        print 'Done'
        
 
 
def create_UserProfile():
    UP = acm.FUserProfile[CalcUser_profile]
    if UP:
        print 'UserProfile exists'
    else:
        print 'Will create UserProfile %s ' %CalcUser_profile
        UP = acm.FUserProfile()
        UP.Name(CalcUser_profile)
        UP.Commit()
        
        for comp in comps_to_add:
            pc1 = acm.FProfileComponent()
            pc1.UserProfile(UP)
            pc1.Component(acm.FComponent.Select01('name = %s' %comp, 'Component %s not found' % comp))
            pc1.AllowCreate(True)
            pc1.AllowDelete(True)
            pc1.AllowWrite(True)
            pc1.Commit()
        
        
def create_APS(userGroupNameShort):
    APS_name = '%s%s' % (APS_prefix, userGroupNameShort)
    DC_name = '%s%s' % (DC_prefix, userGroupNameShort)
    APS = acm.FPaceEngine.Select('name = %s' % APS_name)
    if APS:
        print 'APS %s already exists, will not create/update' % APS_name
    else:
        print 'Creating APS %s' % APS_name
        APS = acm.FPaceEngine()
        APS.Name(APS_name)
        APS.Configuration(DC_name)
        APS.Commit()
    
 
def create_CalcUser(userGroupNameShort, userGroupName):
    userNameShort = '%s%s' % (CalcUser_prefix, userGroupNameShort)
    userNameShort = userNameShort.upper()
    User = acm.FUser.Select('name = %s' % userNameShort)
    if User:
        print 'CalcUser %s already exists, will not create/update' % userNameShort
    else:
        print 'Creating CalcUser %s, will add principals (%s) and user profile %s' % (userNameShort, CalcUser_kerb_principals, CalcUser_profile)
        CU = acm.FUser()
        CU.Name(userNameShort)
        CU.UserGroup(userGroupName)
        CU.FullName('Calc user for this user group')
        CU.Commit()
        
        for p_text in CalcUser_kerb_principals:
            principal = acm.FPrincipalUser()
            principal.User(CU)
            principal.Type('Kerberos')
            principal.Principal(p_text)
            principal.Commit()
            #print 'Added principal %s' % p_text
 
        
        UPL = acm.FUserProfileLink()
        UPL.User(CU)
        UPL.UserProfile = CalcUser_profile
        UPL.Commit()
 
        
def create_CE(userGroupNameShort):
    CE_name = '%s%s' % (CE_prefix, userGroupNameShort)
    CalcUser_name = '%s%s' % (CalcUser_prefix, userGroupNameShort)
    CalcUser_name = CalcUser_name.upper()
    CE = acm.FStoredCalculationEnvironment.Select('name = %s' % CE_name)
    if CE:
        print 'CalcEnv %s already exists, will not create/update' % CE_name
    else:
        print 'Creating CalcEnv %s, user %s' % (CE_name, CalcUser_name)
        CE = acm.FStoredCalculationEnvironment()
        CU = acm.FUser[CalcUser_name]
        if not CU: print '...Error finding CU %s' %CalcUser_name
        CE.Name(CE_name)
        CE.CalcUser(CU)
        CE.Owner(CU)
        CE.Protection(4080)
        CE.AutoUser(False)
        CE.User(None)
        CE.Commit()       
        
    
 
def create_update_DCMain(userGroupNameShort):
    DCMain = acm.FPaceConfiguration.Select01('name = %s' % DCMain_name, '')
    APS_name = '%s%s' % (APS_prefix, userGroupNameShort)
    CE_name = '%s%s' % (CE_prefix, userGroupNameShort)
    if DCMain:
        print 'Main DistrConf already exists ', DCMain_name
    else:
        print 'Creating Main DistrConf %s' % DCMain_name
        DCMain = acm.FPaceConfiguration()
        DCMain.Name(DCMain_name)
        DCMain.DefaultEngine(None)
        DCMain.Commit()
        
    print 'Updating Main DistrConf %s with partition for %s' % (DCMain_name, APS_name)
    found=False
    for configPart in DCMain.ConfigParts():
        if configPart.Engine().Name() == APS_name:
            print 'Partition for %s already set, skipping' %APS_name
            found=True
            break
    if not found:
        print 'Create partition for %s' % APS_name
        configPart = acm.FPaceConfigPart()
        APS = acm.FPaceEngine.Select01('name = %s' % APS_name, 'APS not found')
        configPart.Engine(APS)
        configPart.Configuration(DCMain)
        configPart.Commit()
        
        configElement = acm.FPaceConfigElement()
        configElement.TaskType = 'environment'
        configElement.TaskKey = CE_name
        
        configElement.Part = configPart
        configElement.Commit()
        
    
def create_DC(userGroupNameShort):
    DC_name = '%s%s' % (DC_prefix, userGroupNameShort)
    DCs = acm.FPaceConfiguration.Select('name = %s' % DC_name)
    if DCs:
        print 'DistrConf %s already exists, will not create/update' % DC_name
    else:
        print 'Creating DistrConf %s' % DC_name
        DC = acm.FPaceConfiguration()
        DC.Name(DC_name)
        DC.DefaultEngine(None)
        DC.Commit()
