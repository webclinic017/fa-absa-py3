"""----------------------------------------------------------------------------
MODULE:
    FMT330In

DESCRIPTION:
    OPEN EXTENSION MODULE
    FMT330 class for user customization.
    User can override the mapping defined in the base class FMT330Base.
    This class can be populated using either swift data or an acm object.
    See FMT330Base for extracting the values from swift or an acm

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""
import FMT330InBase

class FMT330(FMT330InBase.FMT330Base):
    """ FMT330 class for user customization"""
    def __init__(self, source, direction):
        super(FMT330, self).__init__(source, direction)

    def CustomMappings(self):
        """ Override/add mappings"""
        ''''
        if self.source == 'SWIFT':
            self.set_color()
        elif self.source == 'ACM':
            self.set_color_from_trade()
        '''
        pass

    def SetAttributes(self):
        super(FMT330, self).SetAttributes()
        self.CustomMappings()

    @staticmethod
    def GetColumnMetaData():
        """User can modify or extend the column metadata in this method and return it. This metadata will be used for creating columns for specific message type"""
        column_metadata = FMT330InBase.FMT330Base.GetColumnMetaData()
        return column_metadata

    '''
    # Following is the sample code to add a new attribute for mapping e.g. Color
    def set_color(self):
        try:
            self.__color = self.python_object.TRADDET.Color.value()
        except Exception, e:
            self.notifier.DEBUG("Exception occurred in set_color : %s"%str(e))

    def set_color_from_trade(self):
        try:
            if self.acm_obj.Color():
                self.__color = self.acm_obj.Color()
        except Exception, e:
            self.notifier.DEBUG("Exception occurred in set_color_from_settlement : %s"%str(e))

    def Color(self):
        """ Get the color attribute"""
        return self.__color
    '''


