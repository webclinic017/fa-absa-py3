import acm
import at_addInfo as adf

def LinkNewMatchTrade(n, frontTradeId, markitWireId, markedForClearing, *rest):
    try:
        if not markitWireId:
            return 'No MWRereference supplied'

        if frontTradeId:
            existingTrade = acm.FTrade[frontTradeId]

            if existingTrade:
                if existingTrade.AdditionalInfo().CCPmiddleware_id() != markitWireId:

                    print 'FA trade found with trade number', frontTradeId

                    newVersion = '<%s\\%s>' %(1, 1)
                    adf.save(existingTrade, 'CCPmiddleware_id', markitWireId)

                    if markedForClearing:
                        if markedForClearing == 'true':
                            adf.save(existingTrade, 'CCPclearing_process', 'T2_EB')
                        else:
                            adf.save(existingTrade, 'CCPclearing_process', 'DirectDeal')
                    else:
                        adf.save(existingTrade, 'CCPclearing_process', 'DirectDeal')

                    adf.save(existingTrade, 'CCPclearing_status', 'Released')
                    adf.save(existingTrade, 'CCPmiddleware_versi', newVersion)

                    return 'Success'
            else:
                return 'Trade doesn''t exist in Front Arena'
        else:
            return 'No FrontReference supplied'
    except Exception as inst:
        return 'Failed: %s' %(inst.message)
