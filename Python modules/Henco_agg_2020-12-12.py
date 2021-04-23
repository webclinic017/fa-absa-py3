import acm

from FBDPCommon import delete_object
from AGGREGATION_CASH_POSTING_ARCHIV import AGGREGATION_ARCHIVE
from AGGREGATION_CASH_POSTING_ARCHIV import AGGREGATION_DEAGGREGATE


def delete_trades(trades):
    for trade in trades:
        trdnbr = trade.Oid()
        try:
            addinfo = trade.AdditionalInfo()
            if addinfo:
                addinfo.Delete()

            for payment in trade.Payments():
                delete_object(payment, False)

            settlements = [settle for settle in trade.Settlements()]
            for settle in settlements:
                delete_object(settle, False)

            delete_object(trade, False)
            print((
                "Payments, settlements and Additional Infos deleted successfully from trade {}".format(
                    trdnbr
                )
            ))

        except Exception as err:
            print(("Error: Cannot delete trade {}: {}".format(trdnbr, err)))


def deaggregate_trades():
    trades = []
    for trdnbr in trdnbrs:
        trade = acm.FTrade[trdnbr]
        if trade:
            trades.append(trade)

    acm.BeginTransaction()

    archive_class = AGGREGATION_ARCHIVE("Trade", trades, 0)
    archive_class.deArchiveObjects()

    aggregate_class = AGGREGATION_DEAGGREGATE(trades)
    aggregate_class.deaggregateTrades()

    try:
        acm.CommitTransaction()
        print(("Trades {} deaggregated.".format(trdnbrs)))
    except Exception as err:
        acm.AbortTransaction
        print(("ERROR: Trades {} failed to deaggregate: {}".format(trdnbrs, err)))
    else:

        delete_trades(trades)


trdnbrs = [acm.FTrade[132319389]]
delete_trades(trdnbrs)
