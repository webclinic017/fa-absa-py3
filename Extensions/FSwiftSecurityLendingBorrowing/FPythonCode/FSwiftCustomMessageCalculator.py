"""----------------------------------------------------------------------------
MODULE
    FSecuritySettlementCalculator : FSecuritySettlementCalculator contains the logic for calculating the MT type for security settlements.

FUNCTION
    evaluate_mt_settlement()
        Evaluates the mt type of the settlement
    get_applicable_mt_type()
        Returns the applicable mt types for a give mt type as input

VERSION: 2.2.0-0.5.3102

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

def get_applicable_mt_type(acm_object, mt_type):
    """
    This function returns the possible multiple messages depending on the input type
    """
    ret_list = []
    import FSwiftSecurityLendingBorrowingOutMain
    if "MT%s" % str(mt_type) in FSwiftSecurityLendingBorrowingOutMain.SUPPORTED_MT_MESSAGE:
        ret_list = [mt_type]
        # If the user has defined mt_type specific function in FSwiftMTCalculatorHook use that function
        import FSwiftMTCalculatorHook
        applicable_mt_type_func = getattr(FSwiftMTCalculatorHook, 'get_applicable_mt_type_%s' % str(mt_type), None)
        if applicable_mt_type_func:
            ret_list = applicable_mt_type_func(acm_object)

    return ret_list
