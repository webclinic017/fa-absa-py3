""" Compiled: NONE NONE """

from ABSAFOperationsXML import ABSAFOperationsXML
from ABSAFOperationsXML import InvalidTagException
from ABSAFOperationsXML import InvalidEventException

import FOperationsUtils as Utils
import ABSA_XML_Main_Template
import acm


class ABSAFConfirmationXML(object):
    def __init__(self, confirmation):
        self.__confirmation = confirmation
        self.__template = ABSA_XML_Main_Template.IRSOpen


    def GenerateMD5FromTemplate(self):
        try:
            return ABSAFOperationsXML.GenerateMD5FromTemplate(self.__template, self.__confirmation)
        except InvalidTagException, re:
            print(True, "Error in template: " +str(self.__confirmation.ConfTemplateChlItem().Name()) + str(re) +str(" for trade: ") +str(self.__confirmation.Trade().Oid()))
            return ""

    def ZlibAndHex(self, data):
        import zlib
        return zlib.compress(data, 9).encode("hex")

    def CheckISDAEarlyTermination(self, XML):
        try:
            ISDA_CURRENCIES = ['CAD', 'MXN', 'USD', 'CHF', 'CZK', 'DKK', 'EUR', 'GBP', 'HUF', 'ILS', 'NOK', 'PLN', 'SEK', 'TRY', 'ZAR', 'AUD', 'CNY', 'HKD', 'IDR', 'INR', 'JPY', 'KRW', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'TWD']
            #remove the early termination nodes for currencies not in the isda matrix.
            if (self.__confirmation.Trade().Instrument().Currency().Name() not in ISDA_CURRENCIES):
                tagsToRemove = ["earlyTerminationProvision"]
                
                for j in tagsToRemove:
                    for i in XML.getElementsByTagName(j):
                        i.parentNode.removeChild(i)
                
                for i in XML.getElementsByTagName('customisedProduct'):
                    i.removeChild(i.firstChild)
                    i.appendChild(XML.createTextNode(str('true')))
        except Exception, e:
            acm.Log ("Error method CheckISDAEarlyTermination - " + str(e))

        return XML

    def GenerateXmlFromTemplate(self):
        try:
            XML = ABSAFOperationsXML.GenerateXmlFromTemplate(self.__template, self.__confirmation)
            XML = self.CheckISDAEarlyTermination(XML)            
            xmlAsString = ABSAFOperationsXML.ToXml(XML)            
                        
            if (len(self.ZlibAndHex(xmlAsString)) < (64*1024 - 1 )):
                return xmlAsString
            tagsToRemove = ["cashflows"]
            
            for j in tagsToRemove:
                for i in XML.getElementsByTagName(j):
                    i.parentNode.removeChild(i)
            
            for i in XML.getElementsByTagName('customisedProduct'):
                i.removeChild(i.firstChild)
                i.appendChild(XML.createTextNode(str('true')))
            
            return ABSAFOperationsXML.ToXml(XML)
            
        except InvalidTagException, re:
            acm.Log ("Error in template: " +str(self.__confirmation.ConfTemplateChlItem().Name()) + str(re) + str(" for trade: ") +str(self.__confirmation.Trade().Oid()))
            return ""
        except InvalidEventException, re:
            acm.Log(str(re))
            return "InvalidEventException"







