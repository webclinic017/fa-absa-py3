""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/templates/FDocumentationParametersTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FDocumentationParametersTemplate

DESCRIPTION
    Changes to any of these settings require a restart of the
    documentation ATS for the changes to take affect.
----------------------------------------------------------------------------"""
from FOperationsHook import CustomHook

xmlDirectory = '/opt/front/arena/tmp/'
xmlEncoding = "UTF-8"
defaultCodePage = "ISO-8859-1"

xmlStoredInOperationsDocument = True

xslTemplateExtensionForConfirmationDocuments = ''
xsltDirectoryForConfirmationDocuments = ''
xsltFilenameExtensionForConfirmationDocuments = 'xml'

detailedLogging = False

saveCarbonCopySWIFT = False
saveCarbonCopyFreeform = False

ambAddress = ''

receiverMBName = 'documentation_RECEIVER'

# Equal to the value of -sender_source configured in the amba.ini file.
receiverSource = 'BO'

documentServiceRetriesOnTimeout = 3
documentServiceTimeoutInSeconds = 10

useAdaptivDocumentService  = True
AMBSenderForDocumentation  = "DOC_REQUEST_SENDER"
AMBSubjectForDocumentation = "DOC_REQUEST"

dateFormat = "%Y-%m-%d"
timeFormat = "%H:%M:%S"
dateTimeFormat = dateFormat + " " + timeFormat

adaptivWebUIAddress = ''

alwaysAcknowledgeSWIFTMessages = False

hooks = []