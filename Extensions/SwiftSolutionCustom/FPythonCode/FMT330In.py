"""---------------------------------------------------------------------------------------------------------------------
MODULE
    FMT330In

VERSION: 3.0.1-0.5.3470

DESCRIPTION
    OPEN EXTENSION MODULE
    FMT330 class for user customization.
    User can override the mapping defined in the base class FMT330Base.
    This class can be populated using either swift data or an acm object.
    See FMT330Base for extracting the values from swift or an acm

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2021-04-15      FAOPS-978       Tawanda Mukhalela       Nqubeko Zondi           Initial Customizations for incoming
                                                                                MT330s
------------------------------------------------------------------------------------------------------------------------
"""
import FMT330InBase
import FSwiftReaderLogger


class FMT330(FMT330InBase.FMT330Base):
    """ FMT330 class for user customization"""

    notifier = FSwiftReaderLogger.FSwiftReaderLogger('FXMMConfIn', 'FFXMMConfirmationInNotify_Config')

    def __init__(self, source, direction):
        super(FMT330, self).__init__(source, direction)

    def CustomMappings(self):
        """ Override/add mappings"""
        pass
    
    def Type(self):
        return 'MT330'

    def SetAttributes(self):
        super(FMT330, self).SetAttributes()
        self.CustomMappings()

    @staticmethod
    def GetColumnMetaData():
        """
        User can modify or extend the column metadata in this method and return it.
        This metadata will be used for creating columns for specific message type
        """
        column_metadata = FMT330InBase.FMT330Base.GetColumnMetaData()
        return column_metadata

    def ProcessMTMessage(self, msg_id):
        """ process the incoming mt message"""
        import FSwiftMLUtils
        self.notifier.DEBUG("Processing incoming %s message." % (self.Type()))
        try:
            value_dict = {
                'swift_data': self.swift_data
            }
            external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(
                value_dict,
                message_typ=self.Type(),
                channel_id=msg_id,
                subject_typ='Confirmation',
                ext_ref=self.Identifier(),
                in_or_out="Incoming"
            )
            subject = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)
            state_chart = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type(), 'In')
            business_process = FSwiftMLUtils.get_or_create_business_process(external_obj, state_chart, self.Type())
            if business_process:
                info_message = 'Initialized : Business process id {bp_id} with state chart {state_chart} '
                info_message += 'on {subject} {subject_id}'
                self.notifier.DEBUG(info_message.format(
                    bp_id=business_process.Oid(),
                    state_chart=state_chart,
                    subject=subject.ClassName(),
                    subject_id=subject.Oid())
                )
        except Exception as e:
            self.notifier.DEBUG('Exception occurred in ProcessMTMessage : {}'.format(str(e)))

    def IsSupportedMessageFunction(self):
        return True
        
    # Following is the sample code to add a new attribute for mapping e.g. Color
    def set_color(self):
        try:
            self.__color = self.python_object.TRADDET.Color.value()
        except Exception as e:
            self.notifier.DEBUG("Exception occurred in set_color : %s" % str(e))

    def set_color_from_trade(self):
        try:
            if self.acm_obj.Color():
                self.__color = self.acm_obj.Color()
        except Exception as e:
            self.notifier.DEBUG("Exception occurred in set_color_from_settlement : %s" % str(e))

    def Color(self):
        """ Get the color attribute"""
        return self.__color



