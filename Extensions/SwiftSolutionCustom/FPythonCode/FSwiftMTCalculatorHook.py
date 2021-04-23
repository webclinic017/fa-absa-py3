"""---------------------------------------------------------------------------------------------------------------------
MODULE:
      FSwiftMTCalculatorHook

DESCRIPTION:
      This module is used to override the message type returned by FSwiftMTCalculator

FUNCTIONS:
    calculate_swift_message_type():
       Override this function to return customized mt type

VERSION: 2.1.1-0.5.2995

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-03-09      FAOPS-1027      Willie vd Bank          Martin Wortmann         Added a fix to the core function
                                                                                IsThirdPartyFX. This function has a bug
                                                                                in SMS VERSION 3.0.3-0.5.3744 which was
                                                                                resolved with a hotfix in
                                                                                VERSION 3.0.0-0.5.3383. This override
                                                                                should be removed with the next upgrade.
------------------------------------------------------------------------------------------------------------------------
"""
import FSwiftMTCalculatorBase


class ConfirmationSwiftTypeCalculator(FSwiftMTCalculatorBase.ConfirmationSwiftTypeCalculatorBase):
    """ This class implements the attributes used in the message type calculator
        Override the following functions to provide your implementation optionally.
    """
    def __init__(self, acm_object):
        self._acm_object = acm_object
        super(ConfirmationSwiftTypeCalculator, self).__init__(acm_object)

    '''
    def Entitytype(self):
        return customized value

    def InstType(self):
        return customized value

    def UnderInst(self):
        return customized value

    def ExoticType(self):
        return customized value

    def Digital(self):
        return customized value

    def ExerciseType(self):
        return customized value

    def OpenEndStrip(self):
        return customized value

    def Reset(self):
        return customized value

    def ProdEntry(self):
        return customized value

    def IsCOV(self):
        return customized value

    def IsMX(self):
        return customized value
    '''


class SettlementSwiftTypeCalculator(FSwiftMTCalculatorBase.SettlementSwiftTypeCalculatorBase):
    """
        This class implements the attributes used in the message type calculator
        Override the following functions to provide your implementation optionally.
    """
    def __init__(self, acm_object):
        self._acm_object = acm_object
        super(SettlementSwiftTypeCalculator, self).__init__(acm_object)

    '''
    def Amount(self):
        return customized value

    def CPType(self):
        return customized value

    def HasBIC(self):
        return customized value

    def Relation(self):
        return customized value

    def Status(self):
        return customized value

    def TARGET2(self):
        return customized value

    def EBA(self):
        return customized value

    def NotifyReceipt(self):
        return customized value

    def DeliveryType(self):
        return customized value

    def TradeType(self):
        return customized value

    def IsMX(self):
        """ Valid return values : True or False """
        return customized value
    '''

    def IsThirdPartyFX(self):
        """
        Boolean method to denote whether the trade is third party foreign exchange deal
        i.e ThirdPartyFX
        """
        trade = self._acm_object.Trade()
        if trade and trade.SettleCategoryChlItem() and trade.SettleCategoryChlItem().Name() == 'ThirdPartyFX':
            return True
        return False

    def IsCOV(self):
        """
        Gets the IsCov Value from Custom Method
        """
        return self._acm_object.IsCov()


def calculate_swift_message_type(acm_obj, message_type_from_mt_calculator):
    """This hook is called after FSwiftMTCalculator calculates the swift message type corresponding
    to the acm object. User can customize the swift message to be generated for an acm object from this
    hook."""
    try:
        import acm
        import FSBLCalculator
        import FSettlementHooks
        from FSwiftServiceSelector import is_unsupported_settlement

        if acm_obj.IsKindOf(acm.FSettlement):
            if is_unsupported_settlement(acm_obj):
                message_type_from_mt_calculator = FSettlementHooks.GetMTMessage(acm_obj,
                                                                                message_type_from_mt_calculator)
    except ImportError as e:
        print str(e)
        print 'Could not excecute code for Custom message calculation, proceeding with default calculator logic'
        return message_type_from_mt_calculator
    return FSBLCalculator.get_custom_message_type(acm_obj, message_type_from_mt_calculator)

    
def print_calculator_map():
    """
    This function prints the calculator mappings
    :return:
    """
    import FSwiftMTCalculator
    for entries in FSwiftMTCalculator.get_calculator_mappings():
        for mt_type, mapping_list in entries.iteritems():
            for mapping in mapping_list:
                print mt_type, '-->', mapping

# Override the following dictionary to alter the existing attributes.
# e.g. overrride_calculator_mapping = {'103':{'CPType':'Counterparty'}}
overrride_calculator_mapping = {}
