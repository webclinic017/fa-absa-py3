"""
-------------------------------------------------------------------------------------------------------------
HISTORY
=============================================================================================================
Date            Change no       Developer           Description
-------------------------------------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Manan Ghosh         Initial deployment
2016-09-06      CHNG0003914707  Willie vd Bank      Updated MATCH_DEMAT_TRADE to exclude trades where acqr BPID
                                                    and cpty PBID are the same
2017-12-11      CHNG0005220511  Manan Ghosh         Changes for DIS to allow Pre Settle Confirmation
2020-07-27      FAOPS-780       Ntokozo Skosana     Allow CDS cashflows to satisfy PreSettlement event
-------------------------------------------------------------------------------------------------------------
"""

from demat_functions import is_demat

cashflow_type_instrument_mapping = {
    'Float Rate': ('FRN', 'CLN', 'Bill', 'CD', 'CDS', 'Deposit'),
    'Fixed Rate': ('IndexLinkedBond', 'Bond', 'Zero', 'CD', 'CDS'),
    'Fixed Amount': ('IndexLinkedBond', 'Bond', 'Zero', 'CD', 'FRN', 'CDS', 'Deposit')
    }


def MATCH_DEMAT_TRADE(trade):

    if not is_demat(trade):
        return False
    if trade.AdditionalInfo().Demat_Acq_BPID() == trade.AdditionalInfo().MM_DEMAT_CP_BPID():
        return False
    instrument = trade.Instrument()
    if instrument.InsType() not in ('CD', 'FRN', 'Bill'):
        return False
    if trade.Status() != 'FO Confirmed':
        return False

    return True


def IsPreSettlementEvent(cashflow):

    instrument = cashflow.Leg().Instrument()
    if cashflow.AdditionalInfo().Demat_CE_Reference() is None:
        return False
    cash_flow_type = cashflow.CashFlowType()
    instrument_type = instrument.InsType()
    if instrument_type not in cashflow_type_instrument_mapping[cash_flow_type]:
        return False

    return True
