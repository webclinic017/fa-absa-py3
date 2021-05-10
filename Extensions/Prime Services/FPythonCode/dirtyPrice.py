import ps_gen_swift_mt515_client_trade


def dirtyPrice(object):
    try:
        dirtyprice = ps_gen_swift_mt515_client_trade._getDirtyPrice(object.Trade())
        return dirtyprice
    except ps_gen_swift_mt515_client_trade.IrrelevantInstrumentError:
        return None # Do not raise when queried for irrelevant instruments.
