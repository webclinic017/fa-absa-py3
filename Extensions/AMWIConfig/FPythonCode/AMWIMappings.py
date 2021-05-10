'''----------------------------------------------------------------------------------------------------------
MODULE                  :       AMWIMappings
PROJECT                 :       Markit Wire OTC Project
PURPOSE                 :       This module will be used to map entries in AMWI_Mappings integration config
DEPARTMENT AND DESK     :       Markit Wire Front-End Users
REQUESTER               :       AMWI OTC Project
DEVELOPER               :       Arthur Grace
CR NUMBER               :       CHNG0002337584

IMPORTANT -- This module should only be called if important information needs to be sent from the Markit Wire Interface
----------------------------------------------------------------------------------------------------------'''
import acm
import xml.dom.minidom as xml

configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, "AMWI_Mappings")
config = xml.parseString(configuration)
mappings = config.getElementsByTagName("Mappings")


def return_mapping(entry, typeofentry):
    for mapping in mappings:
        if mapping.getAttribute("MappingName") == typeofentry:
            map = mapping.getElementsByTagName("Mapping")
            for mappedentries in map:
                if mappedentries.getAttribute("key") == entry:
                    return mappedentries.childNodes[0].nodeValue


def return_mapping_tenor(entry, period, typeofentry):
    for mapping in mappings:
        if mapping.getAttribute("MappingName") == typeofentry:
            map = mapping.getElementsByTagName("Mapping")
            for mappedentries in map:
                if mappedentries.getAttribute("key") == entry:
                    if mappedentries.getAttribute("Period") == period:
                        return mappedentries.childNodes[0].nodeValue
