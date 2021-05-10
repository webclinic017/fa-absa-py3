""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/wi_processing/etc/FWIFormulas.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FWIFormulas - Formulas for the When Issue calculated values.

DESCRIPTION
    Calcuates the conversions between pre-WI and post-WI trade.

----------------------------------------------------------------------------"""


import acm


acmRound = acm.GetFunction('round', 3)


def JGB_BOND_PRICE_CONVERSION(r, C, A, N):
    """------------------------------------------------------------------------
    JGB BOND CONVERSION FORMULA
        P : Price
        C : Nominal Coupon Rate (in % on Annual Basis)
        r : Semi Annual Compound Yield (%)
        A : Days from the first Accrual Date to the Issue Date
        N : Number of Interest Payments to the Maturity Date
        F : 182.5 - A

        P = (C/2) / (1+(r/200))^(2*F/365) +
            (C*100)/r * ( 1/(1+r/200)^(2*F/365) -
                    1/( 1+r/200)^(2*F/365 + N - 1) +
            100/( 1+r/200)^(2*F/365 + N - 1)) -
            (C/2) * (2*A/365)

        In the calculation process, each calculation results are to be rounded
        to ten (10) decimal places.  P shall be rounded down to three (3)
        decimal places.
    ------------------------------------------------------------------------"""
    F = 182.5 - A

    value = (C / 2) / pow(1 + r / 200, 2 * F / 365)
    value = acmRound(value, 10, 'Normal')
    P = value

    value = ((C * 100) / r * (1 / pow(1 + r / 200, 2 * F / 365) -
            1 / pow(1 + r / 200, 2 * F / 365 + N - 1)))
    value = acmRound(value, 10, 'Normal')
    P = P + value

    value = 100 / pow(1 + r / 200, 2 * F / 365 + N - 1)
    value = acmRound(value, 10, 'Normal')
    P = P + value

    value = (C / 2) * (2 * A / 365)
    value = acmRound(value, 10, 'Normal')
    P = P - value

    P = acmRound(P, 3, 'Down')

    return P


def JGB_FRN_PRICE_CONVERSION(K, af, at, A, N):
    """------------------------------------------------------------------------
    JGB FRN CONVERSION FORMULA
        P    : Price
        K    : Reference Rate (%, Calculated from the Result of the latest
                10Year JGB Auction by the Issuer)
        af    : "a" fixed through the Auction (%)
        at  : "a" traded between counterparts in WI Transaction (%)
        A    : Days from the first Accrual Date to the Issue Date
        N    : Number of Interest Payments to the Maturity Date
        F    : 182.5 - A

        P = ((K - af) / 2) / pow(1 + (K - at) / 200, 2 * F / 365) +
            ((K - af) * 100 / (K - at)) * (1 / pow(1 + (K - at) / 200,
                    2 * F / 365 - 1 / pow(i + (K - at) / 200,
                            2 * F / 365 + N - 1)) +
            100 / pow(1 + (K - at) / 200, 2 * F / 365 + N - 1) -
            ((K - af) / 2) * ( 2 * A / 365)

        In the calculation process, each calculation results are to be rounded
        to ten (10) decimal places.  P shall be rounded down to three (3)
        decimal places.
    ------------------------------------------------------------------------"""
    F = 182.5 - A

    value = ((K - af) / 2) / pow(1 + (K - at) / 200, 2 * F / 365)
    value = acmRound(value, 10, 'Normal')
    P = value

    value = ((K - af) * 100 / (K - at)) * (1 / pow(1 + (K - at) / 200,
            2 * F / 365) - 1 / pow(1 + (K - at) / 200, 2 * F / 365 + N - 1))
    value = acmRound(value, 10, 'Normal')
    P = P + value

    value = 100 / pow(1 + (K - at) / 200, 2 * F / 365 + N - 1)
    value = acmRound(value, 10, 'Normal')
    P = P + value

    value = ((K - af) / 2) * (2 * A / 365)
    value = acmRound(value, 10, 'Normal')
    P = P - value

    P = acmRound(P, 3, 'Down')

    return P
