"""----------------------------------------------------------------------------
MODULE:
    FMT548In

DESCRIPTION:
    OPEN EXTENSION MODULE
    FMT548 class for user customization.
    User can override the mapping defined in the base class FMT548InBase.
    This class can be populated using either swift data or an acm object.
    See FMT548InBase for extracting the values from swift #or an acm

VERSION: 2.2.0-0.5.3102
----------------------------------------------------------------------------"""
import FMT548InBase
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSwiftMLUtils
import acm

class FMT548(FMT548InBase.FMT548Base):
    """ FMT547 class for user customization"""

    def __init__(self, source, direction):
        super(FMT548, self).__init__(source, direction, 'MT548')

    def CustomMappings(self):
        """ Override/add mappings"""
        pass

    def SetAttributes(self):
        super(FMT548, self).SetAttributes()
        self.CustomMappings()

    @staticmethod
    def GetColumnMetaData():
        """User can modify or extend the column metadata in this method and return it. This metadata will be used for creating columns for specific message type"""
        column_metadata = FMT548InBase.FMT548Base.GetColumnMetaData()
        return column_metadata

    #Overridden for STRATE MT548
    def set_status_code(self):
        try:
            for each in self.python_object.SequenceA_GeneralInformation.SubSequenceA2_Status:
                value = each.StatusCode.value()[-4:]

            self._status_code = value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_status_code : %s" % str(e))


    # Methods to fetch data from the swift message
    def set_identifier(self):
        try:
            #This override caters to STRATE MT548.
            #Fetch related reference (identifier), deal reference(deal_identifier) from message
            self._identifier = 'NoIdentifier'
            for link in self.python_object.SequenceA_GeneralInformation.SubSequenceA1_Linkages:
                if link.Reference_C and link.Reference_C.value()[1:5] == 'TRRF':
                    related_ref_val = link.Reference_C.value()[7:]
                    sett_object = acm.FSettlement[ str(related_ref_val)]
                    #If the settlement is in status Void that means it is cancelled and hence look for cancelaltion settlement
                    if sett_object.Status() == 'Void':
                        sett_to_pair = sett_object.Parent()
                    else:
                        sett_to_pair = sett_object
                    self._identifier = sett_to_pair.Oid()
                    self._internal_identifier = sett_to_pair.Oid()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identifier : %s"%str(e))

    def UniquePair(self):
        """Lookup the unique identifier in the MT54X message and search for the specific 
            settlement in case of STRATE 548"""

        if self.is_STRATE_reply():
            settlement_no = self.InternalIdentifier()
            if settlement_no:
                sett_object = acm.FSettlement[str(settlement_no)]
                #If the settlement is in status Void that means it is cancelled and hence look for cancelaltion settlement
                pair_object = sett_object
            if not pair_object:
                notifier.INFO('FSettlement ' + str(settlement_no) + ' not found' + '\n' + self.SwiftData())
            return pair_object
        else:
            super(FMT548, self).UniquePair()

    def is_STRATE_reply(self):
        is_STRATE = 0
        for link in self.python_object.SequenceA_GeneralInformation.SubSequenceA1_Linkages:
            if link.Reference_C and link.Reference_C.value()[1:5] == 'TRRF':
                is_STRATE += 1
                break
        if is_STRATE == 1:
            for link in self.python_object.SequenceA_GeneralInformation.SubSequenceA2_Status:
                if link.StatusCode and 'STRA' in link.StatusCode.value():
                    is_STRATE += 1
                    break
        if is_STRATE == 2:
            return True
        return False
