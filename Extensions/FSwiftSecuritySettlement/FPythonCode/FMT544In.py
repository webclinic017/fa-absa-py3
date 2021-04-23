"""----------------------------------------------------------------------------
MODULE:
    FMT544In

DESCRIPTION:
    OPEN EXTENSION MODULE
    FMT544 class for user customization.
    User can override the mapping defined in the base class FMT54XInBase.
    This class can be populated using either swift data or an acm object.
    See FMT54XInBase for extracting the values from swift or acm

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import FMT54XInBase

class FMT544(FMT54XInBase.FMT54XBase):
    """ FMT544 class for user customization"""
    def __init__(self, source, direction):
        super(FMT544, self).__init__(source, direction, 'MT544')

    def CustomMappings(self):
        """ Override/add mappings"""
        ''''
        if self.source == 'SWIFT':
            self.set_color()
        elif self.source == 'ACM':
            self.set_color_from_settlement()
        '''
        pass

    def SetAttributes(self):
        super(FMT544, self).SetAttributes()
        self.CustomMappings()

    @staticmethod
    def GetColumnMetaData():
        """User can modify or extend the column metadata in this method and return it. This metadata will be used for creating columns for specific message type"""
        column_metadata = FMT54XInBase.FMT54XBase.GetColumnMetaData()
        return column_metadata

    '''
    # Following is the sample code to add a new attribute for mapping e.g. Color
    def set_color(self):
        try:
            self.__color = self.python_object.TRADDET.Color.value()
        except Exception, e:
            self.notifier.DEBUG("Exception occurred in set_color : %s"%str(e))

    def set_color_from_settlement(self):
        try:
            if self.acm_obj.Color():
                self.__color = self.acm_obj.Color()
        except Exception, e:
            self.notifier.DEBUG("Exception occurred in set_color_from_settlement : %s"%str(e))

    def Color(self):
        """ Get the color attribute"""
        return self.__color
    '''


