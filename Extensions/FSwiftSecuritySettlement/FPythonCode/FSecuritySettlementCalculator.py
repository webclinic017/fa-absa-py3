"""----------------------------------------------------------------------------
MODULE
    FSecuritySettlementCalculator : FSecuritySettlementCalculator contains the logic for calculating the MT type for security settlements.

FUNCTION
    evaluate_mt_settlement()
        Evaluates the mt type of the settlement
    get_applicable_mt_type()
        Returns the applicable mt types for a give mt type as input

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
try:
    import FSwiftOperationsAPI
except Exception as e:
    pass
import FIntegrationUtils

try:
    acm_version = FIntegrationUtils.FIntegrationUtils.get_acm_version()
    if acm_version < 2018.2:
        from FSettlementEnums import SettlementDeliveryType, SettlementType
    else:
        SettlementDeliveryType = FSwiftOperationsAPI.GetSettlementDeliveryTypeEnum()
        SettlementType = FSwiftOperationsAPI.GetSettlementTypeEnum()
except Exception as e:
    pass

MTMapping_Settlement = \
{
    '540':  [
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery Free of Payment', 'Amount':'>0', 'InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'False'}
            ],
    '542':  [
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery Free of Payment', 'Amount':'<0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'False'}
            ],
    '541':  [
                {'Type': '!Redemptionget_swift_mt_type Security', 'DeliveryType':'Delivery versus Payment', 'Amount':'>0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'False'}
            ],
    '543':  [
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery versus Payment', 'Amount':'<0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'False'}
            ],

    'SESE023':  [
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery Free of Payment', 'Amount':'>0', 'InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'True'},
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery Free of Payment', 'Amount':'<0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'True'},
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery versus Payment', 'Amount':'>0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'True'},
                {'Type': '!Redemption Security', 'DeliveryType':'Delivery versus Payment', 'Amount':'<0','InstType': "!('Commodity Variant')", 'SecLoanUndType':"!('Commodity Variant','Commodity')", 'IsMX':'True'}
            ]
}

MTMapping_Confirmation = \
{
    '518': [
                {'Entitytype': '!Chaser', 'InstType' : "('Bond', 'Zero', 'FRN')"}
            ],
}

def evaluate_mt_settlement(boEntity, settlement_swift_type_calculator_obj):
    """
        This function returns the MT type of the settlement depending on the type and sign of the
        amount.
    """
    messageType = None
    if not boEntity.Type() == SettlementType.REDEMPTION_SECURITY:
        settlementDeliveryType = settlement_swift_type_calculator_obj.DeliveryType()
        amount = settlement_swift_type_calculator_obj.Amount()
        if settlementDeliveryType == SettlementDeliveryType.DELIVERY_FREE_OF_PAYMENT:
            if amount > 0:
                messageType = '540'
            else:
                messageType = '542'
        elif settlementDeliveryType == SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
            if amount > 0:
                messageType = '541'
            else:
                messageType = '543'
    return messageType

def get_applicable_mt_type(acm_object, mt_type):
    """
    This function returns the possible multiple messages depending on the input type
    """
    ret_list = []
    import FSecuritySettlementOutMain
    if "MT%s" % str(mt_type) in FSecuritySettlementOutMain.SUPPORTED_MT_MESSAGE or str(mt_type) in FSecuritySettlementOutMain.SUPPORTED_MX_MESSAGE:
        ret_list = [mt_type]
        # If the user has defined mt_type specific function in FSwiftMTCalculatorHook use that function
        import FSwiftMTCalculatorHook
        applicable_mt_type_func = getattr(FSwiftMTCalculatorHook, 'get_applicable_mt_type_%s' % str(mt_type), None)
        if applicable_mt_type_func:
            ret_list = applicable_mt_type_func()

    return ret_list


