'''---------------------------------------------------------------------------------
 MODULE
     AMBALoader

     Copyright (c) 2011-2018 FIS FRONT ARENA. All rights reserved.

 DESCRIPTION
    This tool loads simple AMBA messages
    
 USAGE
    It can be used within Prime or from RunScriptCMD:

    <?xml version="1.0" encoding="ISO-8859-1" ?> 
    <RunScriptCMD>

    <!-- Load AMBA message from a file-->
     <Command callback="False" exitOnError="False" module="AMBALoader">
       <inputfile>AMBAMessage.txt</inputfile>
       <ambaconfig>ISO</ambaconfig>
     </Command>

    <!-- Load AMBA message directly in XML-->
     <Command callback="False" exitOnError="False" module="AMBALoader">
       <ambamessage>
[MESSAGE]
  [ACCOUNTINGPARAMETERS]
    NAME=TEST
    OPTION_ALLOC=PREMIUM_ALLOC_END
    IRA_ALLOC=PREMIUM_ALLOC_END
    BOND_ALLOC=PREMIUM_ALLOC_END
    ZERO_ALLOC=PREMIUM_ALLOC_END
    BILL_ALLOC=PREMIUM_ALLOC_END
    FRN_ALLOC=PREMIUM_ALLOC_END
    DEFAULT_ALLOC=PREMIUM_ALLOC_END
  [/ACCOUNTINGPARAMETERS]
[/MESSAGE]
    </ambamessage>
     </Command>

    </RunScriptCMD>


 REFERENCES

 ENDDESCRIPTION
---------------------------------------------------------------------------------'''
import acm
import re
import time
import os

import FLogger
logger = FLogger.FLogger(name = 'Transporter')

import Transporter
Transporter.checkProfileComponent("Start "+__name__)
from Transporter import IN_PRIME
from Transporter import ACM_SHORT_VERSION

import FRunScriptGUI

from cStringIO import StringIO 

class Loader(object):
    """
    Class that reads AMBA messages from file and attempts to commit them to the connected ADS.
    in the session.
    """
    pattern = re.compile("^\s*[\[<](/)?(MESSAGE|TRANSACTION)[\]>]")

    def __init__(self, registerInStorage=False, configObject=''):
        self.registerInStorage=registerInStorage
        self.configObject = configObject

    # TODO Report line number when failing to match open tag?
    def __yieldMessage(self, filepointer):
        level = []
        message = []
        for line in filepointer:
            if line.strip() == '':
                continue

            if line[0] in ('#', '-'):
                continue

            message.append(line)
            match = self.pattern.match(line)
            if match != None:
                (close, tag) = match.group(1, 2)
                if close:
                    if not level or tag != level.pop():
                        raise Exception('No matching open tag to /%s'%tag)
                    if not level:
                        yield "".join(message)
                        message = []
                else:
                    level.append(tag)


    def __getNumberOfMessages(self, messageFile):

        # Saving starting position in file.
        position = messageFile.tell()

        # Counting all messages until EOF. 
        #count = sum(1 for x in self.__yieldMessage(messageFile))
        count = 0
        for message in self.__yieldMessage(messageFile):
            count = count + 1

        # Restoring original position in file.
        messageFile.seek(position)

        return count


    def writeToADS(self, messageFile, messageFilename=None):
        failedMessages   = []
        failedExceptions = {}

        # Reading each message in turn from file and writing to ADS.

        # Reading number of messages in file.
        messageNum = self.__getNumberOfMessages(messageFile)
        logger.info("Found %s AMBA message%s." % (messageNum, '' if messageNum < 2 else 's' ))

        # Reading messages, attempting to load and write to ADS.
        for messageId, message in enumerate(self.__yieldMessage(messageFile), start=1):
            if messageNum < 100 or messageId % 100 == 1 or messageId == messageNum:
                logger.info("Processing AMBA message %s of %s." % (messageId, messageNum))
                
            try:
                self.__writeToADS(message)

            except Exception, exception:
                logger.error(str(exception))
                logger.debug("\n%s"%message)
                failedMessages.append(message)
                failedExceptions[messageId] = str(exception)

        # Processing failed messages, if required.
        failedNum = len(failedMessages)
        if failedNum:
            # Logging summary of failed message exceptions.
            logger.error("%s / %s Messages Failed" % (failedNum, messageNum))
            for messageId in failedExceptions:
                exception = failedExceptions[messageId]
                logger.info("Message %4s : %s" % (messageId, exception))

            # Writing out failed messages to file.
            if messageFilename:
                failedFilename = messageFilename + ".failed." + time.strftime("%Y%m%d_%H%M%S")
                logger.info("Writing out failed AMBA messages to file: %s" % failedFilename)
                with open(failedFilename, 'w') as failedFile:
                    for failedMessage in failedMessages:
                        failedFile.write(failedMessage)

            # TODO What about messages with warnings?


    def __writeToADS(self, message):
    
        # Checking if ADS connection present before attempting AMBA message load and commit.
        if not acm.IsConnected():
            raise Exception("Failed to load AMBA message: Not connected to ADS.")

        #Prior to ACM Version - 2016.2, upon importing Instrument AMBA message through AMBA loader 
        #the aliases on instrument are replaced, in-order to prevent that  SPR-380244
        if ACM_SHORT_VERSION < 2016.2:
            import amb
            buffer = amb.mbf_create_buffer_from_data(message)
            amba_message = buffer.mbf_read()
        
            ins_tag = amba_message.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
            if ins_tag :
                insid_tag = ins_tag.mbf_find_object('INSID', 'MBFE_BEGINNING')
                insid = insid_tag.mbf_get_value()
                ins = acm.FInstrument[insid]
                if ins and ins.Aliases():
                    for alias in ins.Aliases():
                        mb_msg = ins_tag.mbf_start_list("INSTRUMENTALIAS")
                        mb_msg.mbf_add_string("ALIAS", alias.Alias())
                        mb_msg.mbf_add_string("TYPE.ALIAS_TYPE_NAME", alias.Type().Name())
            message = amba_message.mbf_object_to_string() 

        #if one is trying to load DELETE_OBJECT type of AMBA message
        #we need to delete object identified by AMBA api CreateCloneMessage
        match = re.search('TYPE=DELETE_', message)
        if match :
            try :
                obj = acm.AMBAMessage.CreateCloneFromMessage(message)
                obj.Delete()
            except Exception, e:
                raise Exception("Delete failed with exception: \"%s\"." % str(e))
            return

        # Attempting create object from AMBA message.
        #logger.info("Loading AMBA message:\n%s" % message)
        try:
            if self.configObject:
                obj = acm.AMBAMessage.CreateCloneFromMessage(message, self.configObject)
            else:
                obj = acm.AMBAMessage.CreateCloneFromMessage(message)
        except Exception, exception:
            raise Exception("Create object from AMBA message failed: \"%s\"." % str(exception))

        if not obj:
            raise Exception("Create object from AMBA message failed.")

        # Attempting to commit object.
        attribute = 'Name' if hasattr(obj, 'Name') else 'Oid'
        objId = getattr(obj, attribute)()
        objId = "object %s['%s' = %s]." % (obj.Class().Name(), attribute, objId)

        #If the message object has an AutoUser attribute we assume we want it controlled using the message
        if hasattr(obj, 'AutoUser'):
            obj.AutoUser(False)

        try:
            obj.Commit()
            logger.debug("ADS object commit succeeded for %s" % objId)

        except Exception, exception:
            raise Exception("ADS object commit failed for %s: \"%s\"." % (objId, str(exception)))
        if self.registerInStorage:
            obj.RegisterInStorage()
# Loader end


class AMBALoader(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        fileSelection = FRunScriptGUI.InputFileSelection(FileFilter = "AMBA message file (*.amb;*.mes;*.txt)|*.amb;*.mes;*.txt|All Files (*.*)|*.*||")
        dirSelection = FRunScriptGUI.DirectorySelection()
        
        ambaconfigs = ['Default',] + sorted(acm.GetDefaultContext().GetAllExtensions('FAMBADefinition', 'FObject', True, True, 'transporter', 'ambaloader', False)) 
        hasAmbaconfigSupport = acm.AMBAMessage.GetMethod("CreateCloneFromMessage", 2) != None
        
        vars = [['basepath', 'Loader path', dirSelection, None, dirSelection, 0, 1, 'the file path'+'\nRunScriptCMD:basepath'[:None if IN_PRIME else 0], None, True],
                ['inputfile', 'AMBA inputfile', fileSelection, None, fileSelection, 0, 1, 'The input file(s)'+'\nRunScriptCMD:inputfile'[:None if IN_PRIME else 0], None, True],
                ['ambamessage', 'AMBA message', 'string', None, "", 0, 0, 'An AMBA message'+'\nRunScriptCMD:ambamessage'[:None if IN_PRIME else 0], None, True],
                ['ambaconfig', 'AMBA config', 'string', ambaconfigs, "ISO" if hasAmbaconfigSupport else "Default", 2, 0, 'A FAMBADefinition setting'+'\nRunScriptCMD:ambaconfig'[:None if IN_PRIME else 0], None, hasAmbaconfigSupport],
            ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)

ael_gui_parameters = {'runButtonLabel':   'Load',
                    'hideExtraControls': Transporter.transporterSetup.get('hideExtraControls', 'True') =='True',
                    'scriptDescription':'Beware: AMBALoader is configured to use the same FAMBADefinition as AMBAPackager.\nDifferent settings might be needed depending on where your AMBA files are exported.',
                    'windowCaption' : 'Transporter:%s '%__name__ + chr(0xA9) + '2018 FIS Front Arena',
                    'version' : '1.0.1(0.1.55)'}


ael_variables=AMBALoader()

def ael_main(params):
    """ Extract all amba messages"""
    logger.LOG("%s %s"%(__name__, '1.0.1(0.1.55)') )

    basepath = Transporter.parseEnv(params['basepath'].AsString())

    configObject = params['ambaconfig'].strip()

    if configObject:
        par = acm.GetDefaultContext().GetExtension('FAMBADefinition', 'FObject', configObject)
        if par:
            par = par.Value()
    else:
        par=None

    if basepath and not os.path.exists(basepath):
        raise IOError("Invalid Path '%s'"%basepath)
    params['basepath'] = acm.FSymbol(basepath)
    
    loader = Loader(configObject=par)

    for messageFilename in str(params['inputfile'].SelectedFile()).split(','):
        if messageFilename:
            if basepath:
                logger.info("Loading AMBA messages from file: '%s' from %s." % (messageFilename, basepath))
                messageFilename = os.path.join(basepath, messageFilename)
            else:
                logger.info("Loading AMBA messages from file: '%s'." % (messageFilename))

            with Transporter.OpenUnicode(messageFilename, 'r') as messageFile:
                loader.writeToADS(messageFile, messageFilename)

    ambamessage = str(params['ambamessage']).strip()
    if ambamessage:
        ambamessage=ambamessage.replace('\\n', '\n')
        loader.writeToADS(StringIO(ambamessage))
    return 0

