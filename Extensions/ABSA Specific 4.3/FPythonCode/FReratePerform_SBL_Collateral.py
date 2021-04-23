""" PRIME 2009.2.1 build 4.4.253.0 modified for ABSA"""

"""----------------------------------------------------------------------------
MODULE
    FReratePerform - Module which reates selected instruments.

    (c) Copyright 2006 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the rerate procedure based on the
    parameters passed from the script FRerate.


----------------------------------------------------------------------------"""
#Import builtin modules

import time
import FBDPString
import FBDPCurrentContext
#Import Front modules

import ael
import FSQL_functions
import acm

from FBDPCommon import Summary

hook = False
w = None

try:
    from FSpreadHook import rerate_spread
    from FSpreadHook import Wrapper
except ImportError:
    pass
else:
    hook = rerate_spread
    w = Wrapper(None)


def supportedLegType(legType):
    return legType in (
        'Call Float',
        'Call Fixed Adjustable',
        'Fixed Adjustable'
    )


def rerate(args):
    if hook:
        FBDPCurrentContext.Logme()('rerate_spread hook enabled!')
        hook_fn = hook

    FBDPCurrentContext.Logme()('rate_from_task_gui(always ignored): %f' % (args['rate']))
    rate_from_task_gui = args['rate']
    no_date_input = False

    if len(args['date']) == 0:
        no_date_input = True
    else:
        date = ael.date(args['date'])

    exceptions = False

    for acm_ins in args['instruments']:

        ins = ael.Instrument[acm_ins.Oid()]
        rerate_type = ''

        try:
            if ins.open_end != 'Open End':
                Summary().ignore(
                    ins,
                    'ReRate',
                    'Non open end instrument',
                    ins.insid
                )
                continue

            for leg in ins.legs():
                if not supportedLegType(leg.type):
                    continue
                if leg.cash_flows():
                    # acm_ins = acm.FInstrument[ins.insid]
                    if acm_ins.AdditionalInfo().CallFloatRef():
                        rerate_type = 'Ref'
                        float_ref_name = acm_ins.AdditionalInfo().CallFloatRef()
                        float_ref = acm.FInstrument[float_ref_name]

                        if not float_ref or float_ref.InsType() != 'RateIndex':

                            Summary().fail(
                                ins,
                                'ReRate(%s)' % rerate_type,
                                'CallFloatRef add info(%s) is not a RateIndex' % float_ref_name,
                                ins.insid
                            )

                            FBDPCurrentContext.Logme()(
                                '%s : CallFloatRef add info(%s) is not a RateIndex' % (ins.insid, float_ref_name)
                            )

                            continue

                        rate_from_float_ref = float_ref.used_price()

                        if rate_from_float_ref != float(rate_from_float_ref):
                            Summary().fail(
                                ins,
                                'ReRate(%s)' % rerate_type,
                                'CallFloatRef(%s) has no valid price/rate' % float_ref_name,
                                ins.insid
                            )

                            FBDPCurrentContext.Logme()(
                                '%s : CallFloatRef(%s) has no valid price/rate' % (ins.insid, float_ref_name)
                            )

                            continue

                        spread_from_insdef = acm_ins.AdditionalInfo().CallFloatSpread()
                        new_rate = float(rate_from_float_ref) + float(spread_from_insdef)

                        FBDPCurrentContext.Logme()(
                            '%s :new rate: %f (based on rate from Float ref %f plus spread on insdef %f)' % (
                                ins.insid,
                                new_rate,
                                rate_from_float_ref,
                                spread_from_insdef
                            )
                        )

                    else:
                        rerate_type = 'Fixed'
                        rate_from_reset = 0.0;
                        if hook:
                            rate_from_reset = hook_fn(ins, w)

                        new_rate = leg.fixed_rate

                        FBDPCurrentContext.Logme()(
                            '%s :new rate: %f (based on rate in reset table)' % (ins.insid, new_rate)
                        )

                    if no_date_input:
                        # ABSA special handling
                        date = leg.end_day

                    if leg.end_day == ael.date_today():
                        ins.re_rate(date, new_rate)
                        Summary().ok(ins, 'ReRate(%s)' % rerate_type)
                    else:
                        Summary().ignore(
                            ins,
                            'ReRate(%s)' % rerate_type,
                            'End day <> Today',
                            ins.insid
                        )

                        FBDPCurrentContext.Logme()(
                            '%s :ignored/not rerated, End day <> Today ' % (ins.insid)
                        )
                
                else:
                    Summary().ignore(
                        ins,
                        'NoCashFlows',
                        'Instrument does not have Cash Flows',
                        ins.insid
                    )
                    
                    FBDPCurrentContext.Logme()(
                        '%s: ignored, does not have cashflows.' % ins.insid
                    )           
                                        
        except Exception as e:
            exceptions = True
            Summary().fail(
                ins,
                'ReRate(%s)' % rerate_type,
                'Exception occured-see log above for details',
                ins.insid
            )

            FBDPCurrentContext.Logme()(
                'Exception occured when rerating %s, \n  Exception:%s .\n' % (ins.insid, str(e))
            )

    Summary().log(args)

    FBDPString.logme('FINISH')

    if exceptions:
        print("Exception(s) occured. See the log for details: %s" % FBDPString.logme.Logfile)
    else:
        print("Completed Successfully ::")
