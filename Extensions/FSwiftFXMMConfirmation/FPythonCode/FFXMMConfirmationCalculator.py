"""----------------------------------------------------------------------------
MODULE
    FFXMMConfirmationCalculator : FFXMMConfirmationCalculator contains the logic for calculating the MT type for FX MM confirmations.

FUNCTION
    get_applicable_mt_type()
        Returns the applicable mt types for a give mt type as input

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
MTMapping_Confirmation = \
{
    '395':  [
                {'Entitytype': 'Chaser'}
            ],
    '300': [
            {'Entitytype':'!Chaser',    'InstType':'Curr'},
            {'Entitytype':'!Chaser',    'InstType':'Future/Forward', 'UnderInst':'Curr', 'TradeType':"('Normal','Closing')", 'SettlementType':'Cash'}
        ],

    '305': [
            {'Entitytype':'!Chaser',     'InstType':'Option',   'UnderInst':'Curr', 'ExoticType':"(None,'','None')", 'Digital':'False',  'ExerciseType':'!Bermudan'}
        ],

    '330': [
            {'Entitytype':'!Chaser',     'InstType':'Deposit','OpenEndStrip':"('Open End','Terminated')"}
        ],

    '320': [
            {'Entitytype':'!Chaser',     'InstType':'Deposit','OpenEndStrip':"!('Open End','Terminated')"}
        ],

    '306': [
        {'Entitytype': '!Chaser', 'InstType': 'Option', 'UnderInst': 'Curr', 'ExoticType': 'Other'},
        {'Entitytype': '!Chaser', 'InstType': 'Option', 'UnderInst': 'Curr', 'Digital': 'True'},
        {'Entitytype': '!Chaser', 'InstType': 'Option', 'UnderInst': 'Curr', 'ExerciseType': 'Bermudan'}
    ]
}


def get_applicable_mt_type(acm_object, mt_type):
    """
    This function returns the possible multiple messages depending on the input type
    """
    import FFXMMConfirmationOutMain
    ret_list = []
    if "MT%s" % str(mt_type) in FFXMMConfirmationOutMain.SUPPORTED_MT_MESSAGE:
        ret_list = [mt_type]
        import FSwiftMTCalculatorHook
        # If the user has defined mt_type specific function in FSwiftMTCalculatorHook use that function
        applicable_mt_type_func = getattr(FSwiftMTCalculatorHook, 'get_applicable_mt_type_%s' % str(mt_type), None)
        if applicable_mt_type_func:
            ret_list = applicable_mt_type_func()
        else:
            if not ret_list:
                ret_list = [mt_type]

    return ret_list
