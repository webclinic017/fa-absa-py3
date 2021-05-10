""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftExceptions.py"
import exceptions

#-------------------------------------------------------------------------
class DocServiceSwiftMessageException(exceptions.Exception):
    def __init__(self, args = None):
        super(DocServiceSwiftMessageException, self).__init__(args)

#-------------------------------------------------------------------------
class SwiftWriterAPIException(exceptions.Exception):
    def __init__(self, args = None):
        super(SwiftWriterAPIException, self).__init__(args)