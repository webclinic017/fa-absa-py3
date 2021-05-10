"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FDocumentationParameters.

DESCRIPTION
    This module contains parameters used to configure documentation functionality
    within Front Arena.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2015-10-20      CHNG0003433716  Lawrence Mucheka        OPS                     Allow for multiple DOC ATSes - Settlements
2016-04-11      CHNG0003588948  Lawrence Mucheka        OPS                     Allow for multiple DOC ATSes - Confirmations
2017                            Willie van der Bank                             Added hooks parameter and removed LogTrace as part of
                                                                                2017 upgrade.
2018-10-16      FAOPS-167       Cuen Edwards            Elaine Visagie          Increased documentServiceTimeoutInSeconds from 10 seconds
                                                                                to 60 seconds to allow for the generation of larger
                                                                                documents.
2018-11-23                      Cuen Edwards                                    Refactored out environment parameter lookup to
                                                                                EnvironmentFunctions and reformatted.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import EnvironmentFunctions


CONF_DOC_ATS_USER_BASE = 'ATS_DOC_CONFO'
STLM_DOC_ATS_USER_BASE = 'ATS_DOC_STLM'

ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_documentation_parameter('Host'),
    amb_port=EnvironmentFunctions.get_documentation_parameter('Port'),
    amb_login=EnvironmentFunctions.get_documentation_parameter('Login')
)

receiverSourceConfBase = EnvironmentFunctions.get_documentation_parameter('ReceiverSourceCONFBase')
receiverSourceStlmBase = EnvironmentFunctions.get_documentation_parameter('ReceiverSourceSTLMBase')

if acm.UserName().startswith(CONF_DOC_ATS_USER_BASE):
    atsNumber = acm.UserName()[len(CONF_DOC_ATS_USER_BASE):]
    receiverMBName = EnvironmentFunctions.get_documentation_parameter('ReceiverNameCONF{atsNumber}'.format(
        atsNumber=atsNumber
    ))
    receiverSource = EnvironmentFunctions.get_documentation_parameter('ReceiverSourceCONF{atsNumber}'.format(
        atsNumber=atsNumber
    ))
elif acm.UserName().startswith(STLM_DOC_ATS_USER_BASE):
    atsNumber = acm.UserName()[len(STLM_DOC_ATS_USER_BASE):]
    receiverMBName = EnvironmentFunctions.get_documentation_parameter('ReceiverNameSTLM{atsNumber}'.format(
        atsNumber=atsNumber
    ))
    receiverSource = EnvironmentFunctions.get_documentation_parameter('ReceiverSourceSTLM{atsNumber}'.format(
        atsNumber=atsNumber
    ))
elif acm.UserName() == 'ATS_DOC_ACKNACK':
    receiverMBName = EnvironmentFunctions.get_documentation_parameter('ReceiverNameACKNACK')
    receiverSource = EnvironmentFunctions.get_documentation_parameter('ReceiverSourceACKNACK')
else:
    receiverMBName = EnvironmentFunctions.get_documentation_parameter('ReceiverName')
    receiverSource = EnvironmentFunctions.get_documentation_parameter('ReceiverSource')

AMBSenderForDocumentation = EnvironmentFunctions.get_documentation_parameter('AMBSenderForDoc')

AMBSubjectForDocumentation = EnvironmentFunctions.get_documentation_parameter('AMBSubjectForDoc')

xmlDirectory = ''
    
###############################################################################
# ATS
###############################################################################
xmlEncoding = "UTF-8"

defaultCodePage = "ISO-8859-1"

xmlStoredInOperationsDocument = True

xslTemplateExtensionForConfirmationDocuments = ''

xsltDirectoryForConfirmationDocuments = ''

xsltFilenameExtensionForConfirmationDocuments = 'xml'

detailedLogging = True

saveCarbonCopySWIFT = False

saveCarbonCopyFreeform = False

alwaysAcknowledgeSWIFTMessages = False

traceLevel = 5

###############################################################################
# AMBA and AMB
###############################################################################
documentServiceRetriesOnTimeout = 3

documentServiceTimeoutInSeconds = 60

useAdaptivDocumentService = True

dateFormat = "%Y-%m-%d"

timeFormat = "%H:%M:%S"

dateTimeFormat = dateFormat + " " + timeFormat

###############################################################################
# Adaptiv Web UI
###############################################################################
adaptivWebUIAddress = ''

hooks = []
