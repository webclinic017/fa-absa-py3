# coding=ascii
"""
Brendan Bosman      MINT-164.3       2015/09/01     1. Created as part of a refactoring process of TriResolve_EMIR.py
Brendan Bosman      MINT-366        2015/09/15      Implement Non EU files

Main Purpose:
1. Class declarations or EmirReportGenerator


To the developers working on this file:
1. This file was taken rom FA where tabsstop was equal to 8 spaces. In FA, most of the indention was 4 space, so
   reading the outside of FA was difficult if tabstop was not 8 spaces. Please be aware of this
2. Going forward, all indentions are 4 spaces, but tabstop is still 8
"""
 
import math
import re
import os

import xml.etree.ElementTree as ElementTree
import at, at_calculation_space as acs, FXRATE

from datetime import datetime

from TriResolve import *
from TriResolve_EMIR_Const import *


def get_midas_id(trd, ai_fallback=False):
    """Return Midas ID for the specified trade or None if it does not exist.
    :param ai_fallback:
    :param trd:
    """

    def from_string(s):
        """

        :param s:
        :return:
        """
        srch = re.search(MIDAS_ID_REGEX, s)
        if srch:
            return int(srch.group(1))

    if trd.Counterparty().Name() == MDK_CPTY_NAME:
        val = from_string(trd.OptionalKey())
        if val:
            return val

    if ai_fallback:  # additional info fallback is really slow
        source_system = trd.AdditionalInfo().Source_System()
        if source_system and source_system.upper() == 'MIDAS':
            full_id = trd.AdditionalInfo().Source_Trade_Id()
            if full_id:
                return from_string(full_id)


def mtm_val_curr(trd):
    """Return (MTM value, currency) of the trade.
    :param trd:
    """

    # Take the value from addinfo if present.
    if trd.Portfolio().AdditionalInfo().MTM_From_External() == 'Yes':
        tai = trd.AdditionalInfo()
        ext_curr = tai.ExternalCCY()
        ext_val = tai.ExternalVal()
        if ext_curr and ext_val:
            mtm_val = float(ext_val) * FXRATE.rate(ext_curr, 'USD')
            return (mtm_val, 'USD')

    simulated = {'Portfolio Currency': 'USD'}
    val_end = acs.calculate_value('FTradeSheet', trd, 'Portfolio Value End', simulated=simulated)

    mtm_curr = val_end.Unit()
    mtm_val = val_end.Number()
    if math.isnan(mtm_val) or math.isinf(mtm_val):
        raise ValueError('Unable to calculate PV using "Portfolio Value End" for trade {0}. \
Returned value is NaN or Inf.'.format(trd.Oid()))

    if trd.IsFxSwap() and trd.IsFxSwapFarLeg():
        mtm_val_near, mtm_curr_near = mtm_val_curr(trd.FxSwapNearLeg())
        if mtm_curr_near != mtm_curr:
            raise ValueError('Different MTM currencies for FX Swap legs, trade ' + str(trd.Oid()))
        mtm_val += mtm_val_near

    return (mtm_val, mtm_curr)


def norm_date(dt):
    """Normalize date, that is, replace magic values such as 3999-01-01 with None, otherwise return Y-m-d.
    :param dt:
    """
    if not dt:
        return None
    dt = at.date_to_datetime(dt)
    if 1900 < dt.year < 3000:
        return dt.strftime(at.DATE_YMD_FORMAT)


def serialize_bxa_config_to_xml(file_location):
    tree = ElementTree.parse(file_location)
    root = tree.getroot()
    return root
    

def barx_africa_filter(xml_config, broker_code, midas_cust_no, sds_id, start_date):
    broker_code_fields = (broker_code_field for broker_code_field in xml_config.findall('.//BrokerCode')
                            if broker_code_field.text == broker_code)
  
    for broker_code_field in broker_code_fields:
        counterparty_fields = (counterparty_field for counterparty_field in xml_config.findall('.//Counterparty')
                                if counterparty_field.attrib.get('sdsid') == str(sds_id)
                                    and counterparty_field.attrib.get('fxf_onboard_date') is not None
                                    and datetime.strptime(start_date, '%Y%m%d') > datetime.strptime(counterparty_field.attrib.get('fxf_onboard_date'), '%Y%m%d'))

        for counterparty_field in counterparty_fields:
            return False

    return True


def check_file_exists(file_path, file_description):
    file_exist = True
    file_exist &= os.path.exists(file_path)
    file_exist &= os.path.isfile(file_path)

    if not file_exist:
        raise ValueError(file_description + " is missing at " + file_path + ".")
            
            
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
