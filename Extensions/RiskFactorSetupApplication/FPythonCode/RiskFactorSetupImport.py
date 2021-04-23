

try:
    import os
    import re
    import time
    
    import acm
    import FRunScriptGUI
    import FLogger

    import Transporter
    import RiskFactorSetupCustomAMBACommit
    
    logger = FLogger.FLogger(name = 'RiskFactorSetupImport')
    
    class RiskFactorSetupLoader( object ):
    
        pattern = re.compile("^\s*[\[<](/)?(MESSAGE|TRANSACTION)[\]>]")
        
        def __init__(self, configObject, batchSize):
            self.configObject = configObject
            self.batchSize = batchSize

        def __YieldMessage( self, filepointer ):
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
            
        def WriteToADS(self, messageFile, messageFilename):
            failedMessages   = []
            failedExceptions = {}

            # Reading messages, attempting to load and write to ADS.
            for messageId, message in enumerate(self.__YieldMessage(messageFile)):
                try:
                    self.__Commit(message)

                except Exception, exception:
                    logger.error(str(exception))
                    logger.debug("\n%s"%message)
                    failedMessages.append(message)
                    failedExceptions[messageId] = str(exception)

            # Processing failed messages, if required.
            failedNum = len(failedMessages)
            if failedNum:
                # Logging summary of failed message exceptions.
                logger.error("%s Messages Failed" % failedNum)
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

        def __Commit( self, message ):
            match = re.search('TYPE=INSERT_RISKFACTORSETUP', message)
            if not match:
                raise Exception("Only valid for inserts of risk factor setups.")
            
            # Checking if ADS connection present before attempting AMBA message load and commit.
            if not acm.IsConnected():
                raise Exception("Failed to load AMBA message: Not connected to ADS.")

            # Attempting create object from AMBA message.
            try:
                obj = acm.AMBAMessage.CreateCloneFromMessage(message, self.configObject)
            except Exception as exception:
                raise Exception("Create object from AMBA message failed: \"%s\"." % str(exception))

            if not obj:
                raise Exception("Create object from AMBA message failed.")

            # Attempting to commit object.
            attribute = 'Name' if hasattr(obj, 'Name') else 'Oid'
            objId = getattr(obj, attribute)()
            objId = "object %s['%s' = %s]." % (obj.Class().Name(), attribute, objId)

            try:
                RiskFactorSetupCustomAMBACommit.Commit( obj, self.batchSize )
                logger.debug("ADS object commit succeeded for %s" % objId)

            except Exception, exception:
                raise Exception("ADS object commit failed for %s: \"%s\"." % (objId, str(exception)))

    fileSelection = FRunScriptGUI.InputFileSelection(FileFilter = "AMBA message file (*.amb;*.mes;*.txt)|*.amb;*.mes;*.txt|All Files (*.*)|*.*||")
    dirSelection = FRunScriptGUI.DirectorySelection()

    ambaconfigs = ['Default',] + sorted(acm.GetDefaultContext().GetAllExtensions('FAMBADefinition', 'FObject', True, True, 'transporter', 'ambaloader', False)) 
    
    ael_variables = [
            ['basepath', 'Loader path', dirSelection, None, dirSelection, 0, 1, 'the file path'+'\nRunScriptCMD:basepath', None, True],
            ['inputfile', 'AMBA inputfile', fileSelection, None, fileSelection, 0, 1, 'The input file(s)'+'\nRunScriptCMD:inputfile', None, True],
            ['ambaconfig', 'AMBA config', 'string', ambaconfigs, "ISO", 1, 0, 'A FAMBADefinition setting'+'\nRunScriptCMD:ambaconfig', None, True],
            ['batchsize', 'Batch Size', 'int', None, 1000, 1, 0, 'Number if risk factor instances commited at a time'+'\nRunScriptCMD:batchsize', None, True]
        ]
    
    def ael_main(params):
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
        
        batchSize = params['batchsize']
        
        loader = RiskFactorSetupLoader(configObject=par, batchSize=batchSize)

        for messageFilename in str(params['inputfile'].SelectedFile()).split(','):
            if messageFilename:
                if basepath:
                    logger.info("Loading AMBA messages from file: '%s' from %s." % (messageFilename, basepath))
                    messageFilename = os.path.join(basepath, messageFilename)
                else:
                    logger.info("Loading AMBA messages from file: '%s'." % (messageFilename))

                with Transporter.OpenUnicode(messageFilename, 'r') as messageFile:
                    loader.WriteToADS(messageFile, messageFilename)
    
except Exception as ex:
    pass
    
