"""
Description
===========
Date                          :  2011-04-
Purpose                       :  Module used to monitor updates to objects that don't have proper access rights defined around them
Department and Desk           :  PCG MO/FO
Requester                     :  Dirk Strauss
Developer                     :  Anil Parbhoo
CR Number                     :  651043

History
=======

Date            CR              Developer               Description
====            ======          ================        =============
2010-11-22      502802          Zaakirah Kajee          Initial Implementation
2015-06-05      ABITFA-3501     Vojtech Sidorin         Add pay_day_method to YC not important attributes.
"""

import ael, acm


# Module used to monitor yield curve and volatility settings access


all_yc_attr = set(ael.YieldCurve.columns())

all_vol_attr = set(ael.Volatility.columns())

not_important_yc_attr = set(['pay_day_method', 'creat_time', 'creat_usrnbr', 'updat_time', 'updat_usrnbr', 'protection', 'owner_usrnbr', 'four_eye_on', 'authorizer_usrnbr', 'version_id', 'size', 'data', 'forward_period.unit', 'forward_period.count', 'historical_day', 'next_seqnbr', 'original_yc_seqnbr', 'reference_day', 'seqnbr', 'underlying_yield_curve_seqnbr', 'calculation_format'])

not_important_vol_attr = set(['creat_time', 'creat_usrnbr', 'updat_time', 'updat_usrnbr', 'protection', 'owner_usrnbr', 'four_eye_on', 'authorizer_usrnbr', 'version_id', 'historical_day', 'original_vol_seqnbr', 'seqnbr'])

important_yc_attr = all_yc_attr - not_important_yc_attr

important_vol_attr = all_vol_attr - not_important_vol_attr



def check_attr(e1, e2):

    if e1.record_type == 'YieldCurve':
        important_attr = important_yc_attr
    else:
        important_attr = important_vol_attr



    # loop through the important_attr set to identify a change in the value of an attribute
    for a in important_attr:
        if eval("e1." + a) <> eval("e2." + a): #test if the attribute value has changed

            return 1

    return 0


fx_excl = ['insaddr', 'barrier_crossed_status', 'barrier_cross_date', 'seqnbr']

def check_attrfx(new, old):
    oldL= old.to_string().split('|')
    newL= new.to_string().split('|')
    col = new.columns()
    for a in range(0, len(oldL)):
        if oldL[a] != newL[a] and col[a] not in fx_excl:
            return 1
    return 0
