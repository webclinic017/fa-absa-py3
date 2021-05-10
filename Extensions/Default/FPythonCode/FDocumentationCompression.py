""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FDocumentationCompression.py"
from FOperationsUtils import LogVerbose

#-------------------------------------------------------------------------
def HexToZlib(data):
    ret = data
    try:
        ret = data.decode("hex")
    except ValueError as e:
        if len(data) == 0:
            pr = "%s HexToZlib has no data to decompress, might affect cancellations/chasers" % str(e)
            LogVerbose(pr)
        elif data.find("xml") != -1:
            pr = "%s HexToZlib: operationsdocument.data is xml should be stored compressed" % str(e)
            LogVerbose(pr)
        else:
            pr = "%s HexToZlib data is %s" % (str(e), data)
            LogVerbose(pr)
    return ret

#-------------------------------------------------------------------------
def ZlibAndHex(data):
    return data.encode("zlib").encode("hex")

#-------------------------------------------------------------------------
def ZlibToXml(data):
    ret = data
    try:
        ret = data.decode("zlib")
    except ValueError as e:
        if len(data) == 0:
            pr = "%s ZlibToXml has no data to decompress, might affect cancellations/chasers" % str(e)
            LogVerbose(pr)
        elif data.find("xml") != -1:
            pr = "%s ZlibToXml has no data to decompress, might affect cancellations/chasers" % str(e)
            LogVerbose(pr)
        else:
            pr = "%s ZlibToXml data is %s" % (str(e), data)
            LogVerbose(pr)
    return ret

