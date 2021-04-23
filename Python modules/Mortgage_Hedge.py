'''
Purpose               :  Create swap trades with equal and opposite PV for swap trades created for mortgages.
                         Add additional filtering criteria - exlude trades with counterparty GT INTERNAL TRADES or FMAINTENANCE
                         and exclude trades done before 01/12/2011
Department and Desk   :  PCG, PCG
Requester             :  Gregory Davis, Gregory Davis
Developer             :  Jaysen Naicker, Jaysen Naicker
CR Number             :  852399, 883073
'''
import acm

class SheetCalcSpace(object):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet')
    @classmethod
    def get_column_calc(cls, obj, column_id):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation(obj, column_id)
        return calc

def GetTrades(portfolio, status, rindex):
    query = acm.CreateFASQLQuery('FTrade', 'AND')

    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Swap'))
    op.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', acm.Time().DateToday())
    op.AddAttrNode('ValueDay', 'GREATER_EQUAL', acm.Time().DateFromYMD(2011, 12, 01))
    op.AddAttrNode('Counterparty.Name', 'NOT_EQUAL', 'GT INTERNAL TRADES')
    op.AddAttrNode('Counterparty.Name', 'NOT_EQUAL', 'FMAINTENANCE')

    op.AddAttrNode('AdditionalInfo.Hedge_Ref_2', 'EQUAL', '')

    op = query.AddOpNode('OR')
    for port in portfolio:
        op.AddAttrNode('Portfolio.Name', 'EQUAL', port)

    op = query.AddOpNode('OR')
    for stat in status:
        op.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', stat))

    op = query.AddOpNode('OR')
    for ind in rindex:
        op.AddAttrNode('Instrument.Legs.FloatRateReference.Name', 'EQUAL', ind)

    return query.Select()


def ValEnd(trd, *rest):
    Value = 0
    try:
        calc = SheetCalcSpace.get_column_calc(trd, 'Portfolio Value End')
        Value = calc.Value().Number()
    except:
        print('error', trd.Oid())
    return Value

context = acm.GetDefaultContext()
sheet_type = 'FPortfolioSheet'
calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)

def myFunc(shift, **rest):
    Trade = rest['trade'].Clone()
    for leg in Trade.Instrument().Legs():
        if leg.LegType() == 'Fixed':
            leg.FixedRate(shift)
            leg.GenerateCashFlows(shift)
    return ValEnd(Trade) - rest['nominal']


def secant(func, oldx, x, TOL=1e-8, **rest):  # f(x)=func(x)
    """
    Similar to Newton's method, but the derivative is estimated by line through 2 starting points.
    http://en.wikipedia.org/wiki/Secant_method
    """

    oldf, f = func(oldx, **rest), func(x, **rest)
    if (abs(f) > abs(oldf)):  # swap so that f(x) is closer to 0
        oldx, x = x, oldx
        oldf, f = f, oldf
    count = 0
    while 1:
        dx = f * (x - oldx) / float(f - oldf)
        if abs(dx) < TOL * (1 + abs(x)):
            return (x - dx)
        else:
            if count >= 500:
                return 0
        oldx, x = x, x - dx
        oldf, f = f, func(x, **rest)
        count = count + 1
    return 0


def ProcessTrade(t, ind_lookup, portfolio_to, cparty):
    ins_clone = t.Instrument().Clone()
    fixed_rate = 0
    float_rate = 0
    isSameFloatInstrument = False

    for leg in ins_clone.Legs():
        leg.PayLeg(not leg.PayLeg())
        if leg.LegType() == 'Float':
            if leg.FloatRateReference().Name() == ind_lookup[leg.FloatRateReference().Name()]:
                isSameFloatInstrument = True
            else:
            	leg.FloatRateReference(acm.FRateIndex[ind_lookup[leg.FloatRateReference().Name()]])

        else:
            fixed_rate = leg.FixedRate()

    new_ins = ins_clone.SuggestName()
    ins_clone.Name(new_ins)
    ins_clone.Commit()

    t.Oid()
    t_clone = t.Clone()
    t_clone.Instrument(ins_clone)
    t_clone.Counterparty(acm.FParty[cparty])
    t_clone.MirrorTrade(None)
    t_clone.Status(acm.EnumFromString('TradeStatus', 'FO Confirmed'))
    t_clone.Portfolio(acm.FPhysicalPortfolio[portfolio_to])

    if not isSameFloatInstrument:

        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')

        new_float_rate = 0
        for leg in ins_clone.Legs():
            if leg.LegType() == 'Float':
                for cashFlow in leg.CashFlows():
                    for reset in cashFlow.Resets():
                        reset.Delete()

                cashFlow.Delete()
                leg.ResetType(acm.EnumFromString('ResetType', 'Weighted'))
                leg.ResetPeriod('1d')
                new_float_rate = leg.FloatRateReference().UsedPrice(t.ValueDay(), ins_clone.Currency().Name(), 'SPOT')
                leg.GenerateCashFlows(new_float_rate)

        target = -1 * ValEnd(t)
        x0 = fixed_rate
        x1 = fixed_rate + new_float_rate
        new_fixed_rate = secant(myFunc, x0, x1, trade=t_clone, nominal=target)

        for leg in ins_clone.Legs():
            if leg.LegType() == 'Fixed':
                leg.FixedRate(new_fixed_rate)
                leg.GenerateCashFlows(new_fixed_rate)

        new_ins = ins_clone.SuggestName()
        ins_clone.Name(new_ins)
        ins_clone.Commit()

    try:
        acm.BeginTransaction()
        t.Commit()
        t_clone.Commit()
        acm.CommitTransaction()
    except Exception, e:
        print("Exception: " + e)
        acm.AbortTransaction()

    if t_clone.add_info('Hedge_Ref_2') == '':
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(t_clone.Oid())
        addInfo.AddInf(acm.FAdditionalInfoSpec['Hedge_Ref_2'])
        addInfo.Value(str(t.Oid()))
        addInfo.Commit()

    if t.add_info('Hedge_Ref_2') == '':
        taddInfo = acm.FAdditionalInfo()
        taddInfo.Recaddr(t.Oid())
        taddInfo.AddInf(acm.FAdditionalInfoSpec['Hedge_Ref_2'])
        taddInfo.Value(str(t.Oid()))
        taddInfo.Commit()

    return 0


ael_variables = [
    ['plist', 'Portfolios to select from:', 'string', ['ERM CFH', 'ERM CFH Equity', 'ERM CFH Funding Desk', 'ERM CFH NSBB WHOLESALE', 'ERM CFH NSBB COMMERCIAL'], 'ERM CFH,ERM CFH Equity,ERM CFH Funding Desk,ERM CFH NSBB WHOLESALE,ERM CFH NSBB COMMERCIAL', 1, 1, 'Portfolios to filter on.', None, 1],
    ['oport', 'Portfolio to write to:', 'string', ['GT R&C VAR Loans_Test'], 'GT R&C VAR Loans_Test', 1, 0, 'Portfolios to output new trades to.', None, 1],
    ['slist', 'Status:', 'string', ['BO Confirmed', 'BO-BO Confirmed'], 'BO Confirmed,BO-BO Confirmed', 1, 1, 'Status to filter on.', None, 1],
    ['ilist', 'Float index to process:', 'string', ['ZAR-JIBAR-3M', 'ZAR-PRIME-3M'], 'ZAR-JIBAR-3M,ZAR-PRIME-3M', 1, 1, 'Float index rate to filter on.', None, 1],
    ['mlist', 'Float index to map to:', 'string', ['ZAR-PRIME-3M', 'ZAR-PRIME-3M'], 'ZAR-PRIME-3M,ZAR-PRIME-3M', 1, 1, 'Float index rate to change to.', None, 1],
    ['cparty', 'Counterparty for new trade:', 'string', ['GT SIMULATED TRADES'], 'GT SIMULATED TRADES', 1, 0, 'Counterparty for new trade.', None, 1],
]

def ael_main(parameters):
    portfolios = parameters['plist']
    statuses = parameters['slist']
    indices = parameters['ilist']
    mindices = parameters['mlist']
    cparty = parameters['cparty']

    portfolio_to = parameters['oport']
    if len(indices) <> len (mindices):
        func = acm.GetFunction('msgBox', 3)
        func("Fail", "Number of entries not equal for indices in the process and mapping entry fields.", 0)

    ind_lookup = {}
    cnt = 0
    for indx in indices:
        ind_lookup[indices[cnt]] = mindices[cnt]
        cnt = cnt + 1

    trades = GetTrades(portfolios, statuses, indices)
    if trades:
        for t in trades:
            ProcessTrade(t, ind_lookup, portfolio_to, cparty)

        print('Processing complete..')
    print('Task completed successfully')
