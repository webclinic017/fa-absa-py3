""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftServiceSelector.py"
import acm, traceback

from FSwiftExceptions import SwiftWriterAPIException

#-------------------------------------------------------------------------
def UseSwiftWriterForMessage(fObject):
    useSwiftWriter = False

    try:
        import FSwiftWriterAPIs

        mtType = FSwiftWriterAPIs.get_swift_mt_type(fObject)

        mtTypeString = 'MT{}'.format(mtType)

        useSwiftWriter = not mtType

        if not useSwiftWriter and FSwiftWriterAPIs.is_outgoing_message_supported(mtTypeString):
            
            useSwiftWriter = not FSwiftWriterAPIs.should_message_be_generated_by_adaptivdocs(mtTypeString)

    except ImportError as exception:

        if not str(exception) == 'No module named FSwiftWriterAPIs':

            raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for message generation: {}. \n{}'.format(exception, traceback.format_exc()))

    except Exception as exception:
        
        raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for message generation: {}. \n{}'.format(exception, traceback.format_exc()))
            
    return useSwiftWriter

#-------------------------------------------------------------------------
def UseSwiftWriterForMT(fObject):
    useSwiftWriter = False

    try:
        import FSwiftWriterAPIs

        mtType = FSwiftWriterAPIs.get_swift_mt_type(fObject)

        mtTypeString = 'MT{}'.format(mtType)
            
        useSwiftWriter = not mtType or FSwiftWriterAPIs.is_outgoing_message_supported(mtTypeString)

    except ImportError as exception:

        if not str(exception) == 'No module named FSwiftWriterAPIs':

            raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for MT calculation: {}. \n{}'.format(exception, traceback.format_exc()))

    except Exception as exception:

        raise SwiftWriterAPIException("Exception when deciding which Swift solution to use for MT calculation: {}. \n{}".format(exception, traceback.format_exc()))
            
    return useSwiftWriter