def PayDateOpenEnd(moneyflow):
    """
    Method extending FMoneyFlow to be used in gropping for excluding
    rolling Open Ended instruments while keeping underlying cashflows intact.
    """
    repo_types = ('Repo/Reverse', 'SecurityLoan')

    if (moneyflow.Trade().Instrument().InsType() in repo_types
            and hasattr(moneyflow.SourceObject(), 'Instrument')
            and moneyflow.SourceObject().Instrument().InsType() in repo_types
            and moneyflow.Trade().Instrument().OpenEnd() == 'Open End'
            and moneyflow.PayDate() == moneyflow.Trade().Instrument().ExpiryDateOnly()):
                return '0000-00-00'
    else:
        return moneyflow.PayDate()
