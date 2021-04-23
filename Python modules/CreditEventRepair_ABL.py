import acm
import CreditEventRepair
import uuid

datediff = acm.Time.DateDifference

INITIAL_DEFAULT_DATE = '2014-08-12'
DELAYED_DEFAULT_DATE = '2014-09-05'
SETTLEMENT_DATE = '2014-11-18'

trade_nbr_list = [66421268, 64189583, 40126338, 40114188, 40102580, 40092284, 40077918, 40072187, 39635812, 39597810, 39576652, 39219475, 39160106, 39133125, 39121662, 39115152,
                    38258231, 37274316, 37195747, 36969616, 36132372, 35363109, 35202608, 35114128, 34216939, 34039356, 31591467, 31308689, 30718928, 30426257, 30422732, 29707441,
                    21789058, 21789022, 17542031, 17541986, 40126339, 40114189, 40102581, 40092285, 40077919, 40072188, 39635813, 39597811, 39576653, 39219474, 39160107, 39121661,
                    39115153, 38258230, 37274317, 37195748, 36969615, 36132371, 31591468, 31308690, 30718927, 30426258, 30422731, 29707442, 21789057, 21789021, 17542030, 17541985,
                    39133126, 35363108, 35202607, 35114500, 34216850, 34039357]


def __parentOrSelf(party):
    assert(party.IsKindOf(acm.FParty))
    if party.Parent() is None:
        return party
    elif party == party.Parent():
        return party
    else:
        return __parentOrSelf(party.Parent())

cds_set = acm.FSet()
for trade_nbr in trade_nbr_list:
    trade = acm.FTrade[trade_nbr]
    if trade.Instrument().IsKindOf(acm.FCreditDefaultSwap):
        cds_set.Add(trade.Instrument())

abil_cds_list = []

for cds in cds_set:
    creditReferenceIssuer = cds.CreditReferenceIssuerOrIssuer()
    if creditReferenceIssuer is None:
        continue
    if __parentOrSelf(cds.CreditReferenceIssuerOrIssuer()).Name() == 'AFRICAN BANK LTD':
        cds_clone = cds.Clone()
        fixed_float_leg = cds_clone.FirstFloatLeg()
        if fixed_float_leg is None:
            fixed_float_leg = cds_clone.FirstFixedLeg()
        fixed_float_leg.AccruedIncluded(True)
        cds_clone.Apply(cds)
        cds.Commit()
        abil_cds_list.append(cds)

a = acm.StartApplication('Instrument Definition', acm.FCreditDefaultSwap())
for ins in abil_cds_list:
    dataDict = CreditEventRepair.CreditEventDialog.CreateDataDictionary(ins)
    dialog = CreditEventRepair.CreditEventDialog(dataDict)
    if datediff(ins.StartDate(), INITIAL_DEFAULT_DATE) > 0:
        dialog.m_defaultDate = DELAYED_DEFAULT_DATE
    else:
        dialog.m_defaultDate = INITIAL_DEFAULT_DATE
    dialog.m_auctioningDate = DELAYED_DEFAULT_DATE
    dialog.m_settlementDate = SETTLEMENT_DATE
    uuid_val = str(uuid.uuid4())
    dialog.m_creditEventId = ins.Name()[0:12] + uuid_val[0:8]

    dialog.PerformCreditEvent(a, ins)

a.Close()

