"""-----------------------------------------------------------------------------
PURPOSE              :  Setup script for price testing automation
DEPARTMENT           :  PCT Valuations
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2021-02-23  CHG0154733     Libor Svoboda       Initial Implementation
"""
import acm
import ael
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)
PT_CURVE_SUFFIX = '/PT'
CURVE_COLUMNS = (
    'attribute_type',
    'conflict_interval',
    'curr',
    'data',
    'estfunc_chlnbr',
    'estimation_type',
    'extrapol_type_long_end',
    'extrapol_type_short_end',
    'forward_period',
    'interpolation_type',
    'ipfunc_chlnbr',
    'ipol_rate_type',
    'ir_format',
    'is_bid_ask',
    'is_yield',
    'pay_day_method',
    'quotation_seqnbr',
    'real_time_updated',
    'rec_rate',
    'reference_day',
    'risk_type',
    'size',
    'spot_days',
    'storage_calc_type',
    'storage_daycount',
    'storage_rate_type',
    'underlying_yield_curve_seqnbr',
    'update_interval',
    'use_bm_dates',
    'yield_curve_type',
    'calculation_format',
    'conflict_interval2',
    'dependency_yield_curve_seqnbr',
    'period_days_offset',
    'composite_func_chlnbr',
    'period_convention',
    'free_text',
    'disc_type_chlnbr'
)
ATTRIBUTE_COLUMNS = (
    'issuer_ptynbr',
    'rating1_chlnbr',
    'rating2_chlnbr',
    'rating3_chlnbr',
    'category_chlnbr',
    'country_chlnbr',
    'bis_status',
    'seniority_chlnbr',
    'restructuring_type',
    'insaddr',
    'curr',
    'off_par',
    'underlying_yield_curve_seqnbr',
    'recovery_rate',
    'fixed_coupon',
    'assumed_recovery_rate',
)


ael_variables = AelVariableHandler()
ael_variables.add(
    'curves',
    label='PT Curves',
    cls=acm.FYieldCurve,
    multiple=True,
)


def sync_attr_spread_curve(original_curve_name):
    LOGGER.info('Syncing PT curve using "%s".' % original_curve_name)
    original_curve = ael.YieldCurve[original_curve_name]
    if not original_curve:
        LOGGER.info('Curve "%s" not found.' % original_curve_name)
        return
    pt_curve = None
    pt_curve_name = original_curve_name + PT_CURVE_SUFFIX
    if ael.YieldCurve[pt_curve_name]:
        pt_curve = ael.YieldCurve[pt_curve_name]
        LOGGER.info('Updating existing PT curve "%s".' 
                    % pt_curve_name)
    elif ael.YieldCurve[original_curve_name + '/PriceTesting']:
        pt_curve = ael.YieldCurve[original_curve_name + '/PriceTesting']
        LOGGER.info('Updating existing PT curve "%s".' 
                    % (original_curve_name + '/PriceTesting'))
    
    if not pt_curve:
        LOGGER.info('Creating new PT curve.')
        pt_curve = original_curve.new()
    else:
        pt_curve = pt_curve.clone()
        orig_periods = {point.date_period 
                            for point in original_curve.points()}
        pt_periods = {point.date_period for point in pt_curve.points()}
        extra_periods = pt_periods - orig_periods
        for extra_period in extra_periods:
            for point in list(pt_curve.points()):
                if point.date_period == extra_period:
                    point.delete()
        missing_periods = orig_periods - pt_periods
        for missing_period in missing_periods:
            point = ael.YieldCurvePoint.new(pt_curve)
            point.date_period = missing_period
        for column in CURVE_COLUMNS:
            try:
                setattr(pt_curve, column, getattr(original_curve, column))
            except AttributeError:
                LOGGER.warning('Curve object does not have a column "%s".' 
                               % column)
                continue
        for pt_attr, orig_attr in zip(pt_curve.attributes(), 
                                      original_curve.attributes()):
            for column in ATTRIBUTE_COLUMNS:
                try:
                    setattr(pt_attr, column, getattr(orig_attr, column))
                except AttributeError:
                    LOGGER.warning('Attribute object does not have a column "%s".'
                                   % column)
                    continue
            for spread in list(pt_attr.spreads()):
                if not spread.point_seqnbr:
                    spread.delete()
                    continue
                if not spread.point_seqnbr.date_period in orig_periods:
                    spread.delete()
            spread_periods = {spread.point_seqnbr.date_period 
                                  for spread in pt_attr.spreads()}
            missing_spread_periods = orig_periods - spread_periods
            for point in pt_curve.points():
                if not point.date_period in missing_spread_periods:
                    continue
                spread = ael.YCSpread.new(pt_attr)
                spread.point_seqnbr = point.seqnbr
    
    try:
        pt_curve.yield_curve_name = pt_curve_name
    except TypeError:
        LOGGER.exception('Failed to set "%s" as curve name.' % pt_curve_name)
        return
    
    try:
        pt_curve.commit()
    except:
        LOGGER.exception('Failed to commit curve "%s".' % pt_curve_name)
    else:
        LOGGER.info('Curve "%s" committed successfully.' % pt_curve_name)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    curves = ael_params['curves']
    for curve in curves:
        if curve.Type() != 'Attribute Spread':
            LOGGER.warning('Only applicable to Attribute Spread curves, skipping "%s".' 
                           % curve.Name())
            continue
        sync_attr_spread_curve(curve.Name())
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
