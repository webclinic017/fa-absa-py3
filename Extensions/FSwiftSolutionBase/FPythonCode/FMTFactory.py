"""----------------------------------------------------------------------------
MODULE:
    FMTFactory

DESCRIPTION:
    OPEN EXTENSION MODULE
    This module creates the FMTnnn object. The object can be created using
    either swift data or an acm object. It is derived from the FMTFactoryBase

FUNCTIONS:
    CreateMTObject(swift_data, acm_object=None):
        Returns Created FMTnnn object

    # Sample code if user intend to develop MT123, he needs to import the FMT123
    try:
        import FMT123
    except Exception, e:
        pass
    class FMTFactory(FMTFactoryBase.FMTFactoryBase):
        @staticmethod
        def CreateMTObject(swift_data, acm_object=None, direction='IN'):
            mt_type = FSwiftMLUtils.get_mt_type_from_swift(swift_data)
            source = acm_object if acm_object else swift_data
            # ADD FOLLOWING CODE BLOCK
            if mt_type == 'MT123':
                # Create object of the FMT123
                return FMT123.FMT123(source, direction)
            else:
                return FMTFactoryBase.FMTFactoryBase.CreateMTObject(
                swift_data, acm_object, direction)

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import acm
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SwiftReader', 'FSwiftReaderNotifyConfig')
import FSwiftMLUtils
import FMTFactoryBase

'''
# If user intend to develop MT123, he need to import the FMT123
try:
    import FMT123
except Exception, e:
    pass
'''
class FMTFactory(FMTFactoryBase.FMTFactoryBase):
    """ FMTFactory class to create MT object as per message type"""
    @staticmethod
    def CreateMTObject(swift_data, acm_object=None, direction='IN'):
        if swift_data.startswith('{1:'):
            mt_type = FSwiftMLUtils.get_mt_type_from_swift(swift_data)
        else:
            mt_type = FSwiftMLUtils.get_mt_type_from_xml(swift_data)
            mt_type = mt_type[0:7]
        source = acm_object if acm_object else swift_data
        if mt_type == 'MT123':
            '''
            # Create object of the FMT123
            mtObj = FMT123.FMT123(source, direction)
            mtObj.SetAttributes()
            return mtObj
            '''
            pass
        else:
            mtObj = FMTFactoryBase.FMTFactoryBase.CreateMTObject(swift_data, acm_object, direction)
            '''To make mappings configurable depending on incoming swift msg, set the swift data in case of creating the object from ACM object.'''
            if not isinstance(source, str) and source.IsKindOf(acm.FObject):
                mtObj.SetAdditionalSwiftData(swift_data)

            mtObj.SetAttributes()
            return mtObj


    @staticmethod
    def CreateMTObjectFromACM(mt_type, acm_object, direction='IN'):
        if mt_type == 'MT123':
            '''
            # Create object of the FMT123
            mtObj = FMT123.FMT123(source, direction)
            mtObj.SetAttributes()
            return mtObj
            '''
            pass
        else:
            mtObj = FMTFactoryBase.FMTFactoryBase.CreateMTObjectFromACM(mt_type, acm_object, direction)
            mtObj.SetAttributes()
            return mtObj

    @staticmethod
    def CreateDerivedMTObject(swift_data,acm_object, mt_type, direction='IN'):
        source = acm_object if acm_object else swift_data
        if mt_type == 'MT123':
            '''
            # Create object of the FMT123
            return FMT123.FMT123(source, direction)
            '''
            pass
        else:
            mtObj = FMTFactoryBase.FMTFactoryBase.CreateDerivedMTObject(swift_data, acm_object, mt_type, direction)
            if not isinstance(source, str) and source.IsKindOf(acm.FObject):
                mtObj.SetAdditionalSwiftData(swift_data)

            mtObj.SetAttributes()
            return mtObj
