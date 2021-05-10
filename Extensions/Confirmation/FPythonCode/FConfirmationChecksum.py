""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationChecksum.py"
import acm
import traceback

# operations
import FOperationsUtils as Utils

# swift
from FSwiftServiceSelector import UseSwiftWriterForMessage

#-------------------------------------------------------------------------
def CreateChecksum(confirmation):
    checksum = ""
    try:
        if confirmation.IsApplicableForSWIFT() and UseSwiftWriterForMessage(confirmation):
            from FSwiftWriterAPIs import get_checksum_for
            checksum = get_checksum_for(confirmation)
        else:
            from FConfirmationXML import FConfirmationXML
            checksum = str(FConfirmationXML(confirmation).GenerateMD5FromTemplate())

    except Exception as error:
        Utils.LogAlways('Failed to generate checksum, checksum will not be set, error given:  {}. \n{}'.format(error, traceback.format_exc()))

    return checksum

#-------------------------------------------------------------------------
def UpdateConfirmationChecksums(confirmations):
    for confirmation in confirmations:
        UpdateConfirmationChecksum(confirmation)

#-------------------------------------------------------------------------
def UpdateConfirmationChecksum(confirmation):
    try:
        acm.Log("Updating checksum on confirmation %d" % confirmation.Oid())
        confirmation.Checksum(CreateChecksum(confirmation))
        confirmation.Commit()
    except Exception as e:
        acm.Log(e)