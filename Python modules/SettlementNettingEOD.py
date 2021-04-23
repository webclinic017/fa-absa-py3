#  Developer           : Heinrich Cronje
#  Purpose             : SND implementation
#  Department and Desk : Operations
#  Requester           : Miguel
#  CR Number           : 662927

def __SND_SettlementNettingEOD():
    Utils.Log(True, '=====================================================================')
    Utils.Log(True, '>> Starting SettlementNettingEOD for SND Setting at %s' % time.asctime(time.localtime()))
    Utils.Log(True, '=====================================================================')
    
    STATUS = 'Authorised'
    CURRENCY = acm.FCurrency['ZAR']
    ACQUIRER_1 = 'STRUCT NOTES DESK'
    ACQUIRER_2 = 'CREDIT DERIVATIVES DESK'
    RELATION_TYPE = 'None'
    
    settlements_1 = acm.FSettlement.Select('status=%s  and currency=%i and acquirer=%s' \
                % (Utils.GetEnum('SettlementStatus', STATUS), CURRENCY.Oid(), ACQUIRER_1))

    settlements_2 = acm.FSettlement.Select('status=%s  and currency=%i and acquirer=%s' \
                % (Utils.GetEnum('SettlementStatus', STATUS), CURRENCY.Oid(), ACQUIRER_2))
                
    settlements = acm.FArray()
    
    for s in settlements_1:
        settlements.Add(s)
    for s in settlements_2:
        settlements.Add(s)

    Utils.Log(True, '>> ' + str(len(settlements)) + ' Settlement(s) to run through the Settlement Netting process...')
    CommitCount = 0
    
    for s in settlements:
        if s.RelationType() == RELATION_TYPE:
            isUpdateCollision = False
            Utils.Log(True, 'Running settlement ' + str(s.Oid()) + ' through Settlement Netting process...')
            isUpdateCollision = CreateSettlementNetting(s)
            
            if isUpdateCollision:
                Utils.Log(Ture, 'Error in creating the net for settlement ' + str(s.Oid()))
            
            CommitCount = CommitCount + 1
            
    Utils.Log(True, '>> ' + str(CommitCount) + ' Settlement(s) were netted via the Settlement Netting process')
    Utils.Log(True, '=====================================================================')
    Utils.Log(True, '>> Completed SettlementNettingEOD for SND Setting at %s' % time.asctime(time.localtime()))
    Utils.Log(True, '=====================================================================')

"""--------------------
    MAIN
--------------------"""
try:
    import acm, time
    import FOperationsUtils as Utils
    from SettlementNettingProcess import CreateSettlementNetting
    eod_Process_List = ['All', 'SND Netting']

    ael_variables = [('nettingProcess', 'Netting Process', 'string', eod_Process_List, 'All')]

    def ael_main(dict):
        if dict['nettingProcess'] in ('All', 'SND Netting'):
            __SND_SettlementNettingEOD()
        else:
            Utils.Log(True, 'No Settlement Netting EOD function for ' + dict['nettingProcess'])
            
        Utils.Log(True, '=====================================================================')
        Utils.Log(True, '>> Completed SettlementNettingEOD at %s' % time.asctime(time.localtime()))
        Utils.Log(True, '=====================================================================')
            
except Exception, e:
    Utils.Log(True, 'Could not run SettlementNettingEOD due to ')
    Utils.Log(True, e)
