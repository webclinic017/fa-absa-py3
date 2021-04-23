'''----------------------------------------------------------------------
Requester : Dirk Strauss, Matthew Berry
Developer : Dirk Strauss, Paul Jacot-Guillarmod
Purpose   : Calculate the spread for a basis curve
            as the difference between the fx curve and swap curve.
CR Number : 878654 (Initial Deployment)
CR Number : 765440 - 31/01/2013 - Peter Basista - Added more detailed logging
----------------------------------------------------------------------'''

import acm, ael, re

class TimePeriodError(Exception): pass

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['swapCurve', 'Swap Curve', 'FYieldCurve', None, None, 1, 0,
        'Swap Curve', None, 1],
    ['basisCurve', 'Basis Curve', 'FYieldCurve', None, None, 1, 0,
        'Basis Curve', None, 1],
    ['fxCurve', 'FX Curve', 'FYieldCurve', None, None, 1, 0,
        'FX Curve', None, 1],
    ['maxDateOffset', 'Cut Off Period', 'string', None, '2y', 1, 0,
        'Date period to be used in calculating a cutoff date, '
        'only points below this date will be updated.', None, 1],
    ['decimalPlaces', 'Rounding Specifications', 'int', None, 8, 1, 0,
        'Specify the number of decimal places to round rates', None, 1]]

def ael_main(ael_dict):
    acm_swap_curve = ael_dict['swapCurve']
    swap_curve = ael.YieldCurve[acm_swap_curve.Name()]

    acm_basis_curve = ael_dict['basisCurve']
    basis_curve = ael.YieldCurve[acm_basis_curve.Name()]

    acm_fx_curve = ael_dict['fxCurve']
    fx_curve = ael.YieldCurve[acm_fx_curve.Name()]

    max_date_offset = ael_dict['maxDateOffset']
    if not re.compile('^[0-9]+[dDwWmMyY]$').match(max_date_offset):
        raise TimePeriodError('A time period must be specified '\
                'as a number followed by d, w, m or y eg. 2y, 3d')

    decimal_places = ael_dict['decimalPlaces']

    update_basis_curve(swap_curve, basis_curve, fx_curve,
            max_date_offset, decimal_places)

    acm.Log("Completed Successfully")

def update_basis_curve(swap_curve, basis_curve, fx_curve,
        max_date_offset, decimal_places):
    """Update the spreads on the basis curve
    with the difference between the fx rate and swap rate."""

    day_count = basis_curve.storage_daycount
    rate_type = basis_curve.storage_rate_type
    calc_type = 'Par Rate'

    pay_day_method = basis_curve.pay_day_method
    calendar_currency = basis_curve.curr

    today = ael.date_today()
    max_date = today.add_period(max_date_offset)
    max_date = max_date.adjust_to_banking_day(calendar_currency,
            pay_day_method)

    points = basis_curve.points()
    basis_point = {}
    acm.Log("Basis curve update started")

    # Calculate the basis spread which is the difference
    # between the fx curve and swap curve
    for point in points:
        tenor = point.date_period
        date = today.add_period(tenor)
        date = date.adjust_to_banking_day(calendar_currency, pay_day_method)

        if date <= max_date:
            swap_rate = swap_curve.yc_rate(today, date,
                    rate_type, day_count, calc_type)
            fx_rate = fx_curve.yc_rate(today, date,
                    rate_type, day_count, calc_type)
            basis = round(fx_rate - swap_rate, decimal_places)
            acm.Log("Updating tenor %s using swap_rate == %.*f "
                    "and fx_rate == %.*f. New basis == %.*f" %
                    (tenor, decimal_places, swap_rate,
                        decimal_places, fx_rate, decimal_places, basis))
            basis_point[tenor] = basis

    attr = basis_curve.attributes()[0]
    spreads = attr.spreads()

    epsilon = (0.5 / 10 ** decimal_places)

    # If the spread has changed then update it with the new basis spread
    for spread in spreads:
        point = spread.point_seqnbr
        tenor = point.date_period
        if tenor in basis_point:
            basis = basis_point[tenor]
            if abs(spread.spread - basis) > epsilon:
                acm.Log("Tenor %s: Updating old spread (%.*f) "
                        "to a new value of %.*f" %
                        (tenor, decimal_places, spread.spread,
                            decimal_places, basis))
                sc = spread.clone()
                sc.spread = basis
                sc.commit()
            else:
                acm.Log("Tenor %s: Keeping original spread value of %.*f" %
                        (tenor, decimal_places, spread.spread))

    # Touch basis curve so that its timestamp is updated
    # in the event of none of the spreads being updated
    touch_curve(basis_curve)
    acm.Log("Basis curve update completed")

def touch_curve(ael_curve):
    """Updates the update timestamp on the yield curve"""

    acm_curve = acm.FYieldCurve[ael_curve.yield_curve_name]
    acm_curve.Touch()
    acm_curve.Commit()

def test(fx_curve):
    bm_pv = []

    for bm in fx_curve.benchmarks():
        ins = bm.instrument
        tpl = (ins.maturity_date(), ins.insid, ins.present_value())
        bm_pv.append(tpl)

    bm_pv.sort()

    for tpl in bm_pv:
        print tpl[0], tpl[1], tpl[2]
