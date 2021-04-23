"""-----------------------------------------------------------------------
MODULE
    FADMRiskFactorDescription - Assembles ADM bound risk factor
    information for an external_id.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    TODO: Fill in a nice description

EXTERNAL DEPENDENCIES
    PRIME 2010.1 or later.
-----------------------------------------------------------------------"""

import acm
import exceptions
import itertools
from collections import namedtuple
from FVaRPerformanceLogging import acm_perf_log
from FVaRPerformanceLogging import log_trace, log_debug, log_error
import FVaRStaticData

class FAtlasMappingError(exceptions.Exception):
    pass

def create_descriptions_from_external_id(external_id, 
    risk_factor_scenario_builder):
    rfds_per_extern_id = risk_factor_scenario_builder.\
        RiskFactors(external_id)
    rf_type = None
    rf_groups = []
    attr_types = []
    for rfd in rfds_per_extern_id:
        rf_type = rfd.Target().RiskFactorType()
        rf_groups.append(rfd.Target().RiskFactorGroup())
        attr_types.append(rfd.RiskFactorDescription().TargetCoordinates())
    return rfds_per_extern_id, rf_type, (tuple(rf_groups), 
                                         tuple(attr_types))

def packed_rfds_as_array(packing_dict):
    packed_rfds = []
    #sorted_external_ids = acm.FArray()
    sorted_external_ids = []
    for rfd_container, ext_ids in packing_dict.values():
        sorted_external_ids.extend(ext_ids)
        packed_rfds.append(rfd_container)
    return sorted_external_ids, packed_rfds

ADMRiskFactorDescriptionData = namedtuple("ADMRiskFactorDescriptionData",
    ["adm_risk_factor_descriptions", "risk_factor_types",
     "ordered_external_ids"])
PackingStruct = namedtuple("PackingStruct", ["containers", "ext_ids"])
def packed_risk_factor_descriptions_from_external_ids(external_ids,
    risk_factor_scenario_builder):
    """
    Builds a packed structure of risk factor descriptions used to represent
    the Delta vectors for parametric value at risk. The packing is done
    to provide vectorization in the bucket dimension to improve performance.
    
    CASE 1, single shift (typically equity/FX):
        [[eq_description]]
            will result in a single shift:
                [eq_shift]
        
    CASE 2, single stacked shift
            (FX with multiple currencies in a rf group):
        [[fx_description = {GBP, EUR}]]
            will result in a stacked shift:
                [GBP shift]
                     |
                [EUR shift]
            
    CASE 3, vectorized non-stacked shift
            (IR/Credit with 1<-->1 mapping between ext id and spec)
        [[ir_descr_bucket1], [ir_descr_bucket2], [ir_descr_bucket3]]
            will result in a vectorized single shift:
                [ir_shift_bucket1, ir_shift_bucket2, ir_shift_bucket3]
            
    CASE 4, vectorized stacked shift
            (IR/Credit with 1<-->m mapping between ext id and spec)
        [[ir1_shift_bucket1], [ir1_shift_bucket2], [ir1_shift_bucket3]]
        [[ir2_shift_bucket1], [ir2_shift_bucket2], [ir2_shift_bucket3]]
            will result in a vectorized stacked shift:
                [ir1_shift_bucket1, ir1_shift_bucket2, ir1_shift_bucket3]
                                            |
                [ir2_shift_bucket1, ir2_shift_bucket2, ir2_shift_bucket3]
    """
    packing_dict = {}
    type_dict = {}
    for ext_id in external_ids:
        rfds_per_ext_id, rf_type, pack_key = create_descriptions_from_external_id(
                ext_id, risk_factor_scenario_builder)
        if not (rfds_per_ext_id and \
            FVaRStaticData.risk_type_supported(rf_type)):
            continue            
        type_dict[ext_id] = rf_type
        if not pack_key in packing_dict:
            containers = [acm.FRiskFactorContainer() \
                          for i in range(len(rfds_per_ext_id))]
            packing_dict[pack_key] = PackingStruct(containers, [])
        packed_struct = packing_dict[pack_key]
        for rfd_container, rfd in itertools.izip(packed_struct.containers, 
                                                 rfds_per_ext_id):
            rfd_container.AddRiskFactor(rfd)
        packed_struct.ext_ids.append(ext_id)
    sorted_external_ids, packed_rfds = packed_rfds_as_array(packing_dict)
    sorted_rf_types = [type_dict[ext_id] for ext_id in sorted_external_ids]
    return ADMRiskFactorDescriptionData(packed_rfds, sorted_rf_types,
        sorted_external_ids)
