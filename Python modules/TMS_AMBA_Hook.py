import ael, amb, string, sys, TMS_Functions
import TMS_Template_IRSwaption, TMS_Template_CurrSwap, TMS_Template_IRSwap, TMS_Template_FRA, TMS_Template_IRG


#---------------------------------------------------------------------------------------------
#Description:           AMBA Hook for BarCap TMS Feed
#Date Created:          2008-06-03
#Developer:             Neil Retief
#
#
#
#---------------------------------------------------------------------------------------------

'''
*********************************************************************************************************************************
*********************** Functions used to catch any updates on the additonal info's against a counterparty **********************
*********************************************************************************************************************************
'''

prefixes = {'UPDATE':'!','INSERT':'+','DELETE':'-'}
addInfos = ['+ADDITIONALINFO', '!ADDITIONALINFO', '-ADDITIONALINFO']

def parseEntitytoDict(mbfObj, entlist, entStr):
    '''Returns a dictionary with entities that have been added or changed.'''
    e_dict = {'+':[], '!':[]}
    delete_support = ['ADDITIONALINFO']
    if entStr in delete_support:
        e_dict = {'+':[], '!':[], '-':[]}
        
    if mbfObj:
   
        for ent in entlist:  
            obj = mbfObj.mbf_find_object(ent)

            while obj != None:
                id = None                
                pfx = get_prefix(obj)
                if e_dict.has_key(pfx) and obj.mbf_get_name() == ent:
                    if obj not in e_dict[pfx]:
                        e_dict[pfx].append(obj)
                obj = mbfObj.mbf_next_object()
    return e_dict
    
def get_prefix(entObj):
    'Returns !, +, - or empty string'
    prx2 = ''
    if entObj:
        prx = entObj.mbf_get_name()
    else:
        log(2, 'get_prefix: the intput is not an Object')

    if prx != '' and prx[0] in prefixes.values():
        prx2= prx[0]
        
    return prx2

'''
*********************************************************************************************************************************
*********************** Functions used to catch any updates on the additonal info's against a counterparty **********************
*********************************************************************************************************************************
'''

'''
*********************************************************************************************************************************
************************************************************* MAIN TMS HOOK *****************************************************
*********************************************************************************************************************************
'''
def TMS_Generate_Message (m, s):

    #Get the type of message being passed
    M_Type = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    
    
    #Get the trade inserts/updates   
    if (M_Type.mbf_get_value() in ('INSERT_TRADE', 'UPDATE_TRADE')):
        
        #Assign the Trade marker
        if M_Type.mbf_get_value() == 'INSERT_TRADE':
            T_Trade_Insert = m.mbf_find_object('+TRADE', 'MBFE_BEGINNING')
            
            #Get the Trade Number
            T_Nbr = T_Trade_Insert.mbf_find_object('TRDNBR', 'MBFE_BEGINNING')
            Opt_key = None
        else:
            T_Trade_Updates = m.mbf_find_object('!TRADE', 'MBFE_BEGINNING')
            T_AddInfo_Updates = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
            
            if T_Trade_Updates:
                T_Nbr = T_Trade_Updates.mbf_find_object('TRDNBR', 'MBFE_BEGINNING')
                Opt_key = T_Trade_Updates.mbf_find_object('!OPTIONAL_KEY', 'MBFE_BEGINNING')
            elif T_AddInfo_Updates:
                T_Nbr = T_AddInfo_Updates.mbf_find_object('TRDNBR', 'MBFE_BEGINNING')
                Opt_key = None
        
        #Get the operation being done
        ent_op = M_Type.mbf_get_value()
        
        #Get the trade object
        TObject = ael.Trade[(int)(T_Nbr.mbf_get_value())]
        
        #Get the instrument object
        IObject = ael.Instrument[TObject.insaddr.insaddr]
        
        #Get the underlying object if one exists
        if IObject.und_instype != 'None':
            Und_IObject = ael.Instrument[TObject.insaddr.und_insaddr.insaddr]
        else:
            Und_IObject = ''

        #Check for any new trades added
        if not Opt_key:
            if TMS_Functions.Send_Trade(ent_op, TObject.trdnbr) != 'NONE':
                
                #Get the correct operation to create the message
                ent_op = TMS_Functions.Send_Trade(ent_op, TObject.trdnbr)
                
                #Generate the correct template
                #IRSwaption
                if IObject.instype == 'Option' and Und_IObject.instype == 'Swap':
                    m = TMS_Template_IRSwaption.IRSwaption_Message(ent_op, TObject.trdnbr)
                    s = 'TMS MESSAGE'
                #FXSwap - The FXSwap Instrument has been deprecated for CRE Fixed Income.
                #elif IObject.instype == 'FxSwap':   
                #    m = TMS_Template_FXSwap.FXSwap_Message(ent_op,TObject.trdnbr)
                #    s = 'TMS MESSAGE'
                #CurrSwap
                elif IObject.instype == 'CurrSwap': 
                    m = TMS_Template_CurrSwap.CurrSwap_Message(ent_op, TObject.trdnbr)
                    s = 'TMS MESSAGE'
                #Swap
                elif IObject.instype == 'Swap': 
                    m = TMS_Template_IRSwap.IRSwap_Message(ent_op, TObject.trdnbr)
                    s = 'TMS MESSAGE'
                #FRA
                elif IObject.instype == 'FRA':   
                    m = TMS_Template_FRA.FRA_Message(ent_op, TObject.trdnbr)
                    s = 'TMS MESSAGE'
                #IRG
                elif ((IObject.instype == 'Option' and Und_IObject.instype == 'FRA') or \
                    IObject.instype in ('Cap', 'Floor')):
                    m = TMS_Template_IRG.IRG_Message(ent_op, TObject.trdnbr)
                    s = 'TMS MESSAGE'
                else:
                    return
            else:
                return
        else:
            return

    # Send trades through when an Instrument is updated
    elif M_Type.mbf_get_value() == 'UPDATE_INSTRUMENT':

        #Assign the M_Type value to an attribute
        ent_op = M_Type.mbf_get_value()
        
        #Get the instrument marker
        if m.mbf_find_object('!INSTRUMENT', 'MBFE_BEGINNING'):
            I = m.mbf_find_object('!INSTRUMENT', 'MBFE_BEGINNING')
        else:
            I = m.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
        
        #Get the insaddr marker
        I_Insaddr = I.mbf_find_object('INSADDR', 'MBFE_BEGINNING')
    
        #Get the instrument object
        IObject = ael.Instrument[(int)(I_Insaddr.mbf_get_value())]
    
        #Pass the instrument object to the Send_Trade function so that all relevant trades will be updated for TMS Message generation
        TMS_Functions.Send_Trade(ent_op, IObject.insaddr)
        
        return

    # Send trades through when a party is updated against a trade. An update will only be sent through 
    # if the SDS Counterparty additional info field is inserted/updated/deleted
    elif M_Type.mbf_get_value() == 'UPDATE_PARTY':

        Found = 0

        if m.mbf_find_object('!PARTY', 'MBFE_BEGINNING'):
            CPty = m.mbf_find_object('!PARTY', 'MBFE_BEGINNING')
        else:
            CPty = m.mbf_find_object('PARTY', 'MBFE_BEGINNING')

        #Assign the M_Type value to an attribute
        ent_op = M_Type.mbf_get_value()

        #Get the counterparty key
        CPty_ID = CPty.mbf_find_object('PTYID').mbf_get_value()
        CPty_Nbr = ael.Party[CPty_ID].ptynbr

        #Create the dictionary with a additional info fields
        add_dict = parseEntitytoDict(CPty, addInfos, 'ADDITIONALINFO')

        #Run through the dictionary and see whether the counterparty has been changed
        for a in add_dict.keys():
            for obj in add_dict[a]:
                newField = obj.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME')
                if newField:
                    if newField.mbf_get_value() == 'BarCap_SMS_CP_SDSID':
                        Found = 1
      
        #Pass the instrument object to the Send_Trade function so that all relevant trades will be updated for TMS Message generation
        if Found == 1:
            TMS_Functions.Send_Trade(ent_op, CPty_Nbr)                    
                    
        return
        
    else:
        return

    return (m, s)
