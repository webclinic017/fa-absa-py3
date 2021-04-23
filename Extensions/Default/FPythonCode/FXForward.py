
import acm


def UpdateDefaultInstrument(ins):
    try:
        ins.SettlementType = 'Physical Delivery'
        ins.UnderlyingType = 'Curr'
        ins.Underlying = None
        ins.PayType = 'Forward'
        ins.ContractSize = 1
        ins.PayOffsetMethod = 'Calendar Days'
    except Exception as e:
        print ('UpdateDefaultInstrument failed', e)
