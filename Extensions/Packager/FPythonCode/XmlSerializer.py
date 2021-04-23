"""-------------------------------------------------------------------------------------------------------
MODULE
    XmlSerializer

    (c) Copyright 2009-2018 by FIS Front Arena. All rights reserved.

VERSION
    1.0.1(0.1.55)
DESCRIPTION
    A wrapper around acm.XmlSerializer. Create temp files and deletes them afterwards
    
MAJOR REVISIONS

    2009-02-09  RL  Initial implementation
    2009-03-13  RL  Revert to Archive in versions without FXmlSerializer TEST...
    2011-05-12  RL  Allow compressed contents
    2011-06-14  RL  Replace nonexistent context
-------------------------------------------------------------------------------------------------------"""

import acm
import os
import tempfile
import zlib
import base64
import xml.etree.cElementTree as ET
import FLogger

logger = FLogger.FLogger(name = 'Transporter')

class XmlSerializer():
    """ XmlSerializer wraps the acm.XmlSerializer """
    def __init__(self):
        self.xmlser = acm.FXmlSerializer()
    def Export(self, filename, item):
        self.xmlser.Export(filename, item)

    def Import(self, filename):
        return self.xmlser.Import(filename)

    def ReplaceContexts(self, archiveData):
        """ Find all columns using non existent Contexts and replace with the default context """

        """<FStandardColumnCreatorTemplate type ="AcmDomain">
              <columnId type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Portfolio Position</string>
                  </Text>
                </FSymbol>
              </columnId>
              <contextSym type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">NonStandard</string>
                  </Text>
                </FSymbol>
              </contextSym>
          </FStandardColumnCreatorTemplate>
        """

        logger.DLOG("XmlSerializer Replace Contexts")
        xmlObj = ET.fromstring(archiveData)
        contexts = [str(context.Name()) for context in acm.FExtensionContext.Select('')]
        
        for obj in xmlObj.findall('.//FStandardColumnCreatorTemplate'):
            contextTag=obj.find('contextSym/FSymbol/Text/string')
            if (contextTag != None) and (contextTag.text not in contexts):
                columnTag = obj.find('columnId/FSymbol/Text/string')
                if columnTag != None:
                    logger.WLOG("Column '%s' Replace Context '%s' with '%s'"%(columnTag.text, contextTag.text, str(acm.GetDefaultContext().Name()) ))
                else:
                    logger.WLOG("Replace Context '%s' with 's'"%(contextTag.text, str(acm.GetDefaultContext().Name()) ))
                contextTag.text = str(acm.GetDefaultContext().Name())

        return ET.tostring(xmlObj, 'ISO-8859-1')

    def ExportStream(self, item, compress=False):
        tmp_fd, tmp_name = tempfile.mkstemp(suffix = '.shx')
        logger.DLOG("XmlSerializer ExportStream create tempfile %s"%tmp_name)
        fil = None
        try:
            self.Export(tmp_name, item)
            fil = os.fdopen(tmp_fd, 'r')
            stream = fil.read()
            if compress and len(stream) != 0:
                stream = base64.b64encode(zlib.compress(stream))
                logger.DLOG("XmlSerializer compressed stream")
        finally:
            if fil and not fil.closed: fil.close()
            os.remove(tmp_name)
            logger.DLOG("XmlSerializer ExportStream remove tempfile")

        return stream

    def ImportStream(self, stream):
        tmp_fd, tmp_name = tempfile.mkstemp(suffix = '.shx')
        logger.DLOG("XmlSerializer ImportStream create tempfile %s"%tmp_name)
        fil = item = None
        try:
            fil = os.fdopen(tmp_fd, 'w')
            try:
                stream = zlib.decompress(base64.b64decode(stream))
                logger.DLOG("XmlSerializer decompressed stream")
            except:
                pass
            if stream == '':
                raise Exception("File is broken")
            stream = self.ReplaceContexts(stream)
            fil.write(stream)
            fil.close()
            item = self.Import(tmp_name)
        finally:
            if fil and not fil.closed: fil.close()
            os.remove(tmp_name)
            logger.DLOG("XmlSerializer ImportStream remove tempfile")
            
        assert item, "xmlserializer could not import the object, maybe wrong format?"
        return item
