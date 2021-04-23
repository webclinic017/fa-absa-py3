import ael, acm

class optionType:
    MANDATORY = 1
    OPTIONAL  = 2

class validationStatus:
    FAILURE    = 0
    SUCCESS    = 1
    INCOMPLETE = 2

# attributes
attrAsk = "ask"
attrBid = "bid"
attrSettle = "settle"
attrLast = "last"

# tags
tagFilter            ='filter'
tagFilters           ='filters'
tagCondition         ='condition'
tagOperands          ='operands'
tagMovingBox         ='movingbox'
tagSpikeAvoidance    ='spikeavoidance'
tagAttributes        ='attributes'
tagLogging           ='logging'
tagTodayOnly         ='todayonly'
tagTimeMax           ='timemax'
tagPriceWidth        ='pricewidth'
tagPriceOffset       ='priceoffset'
tagPriceSpikePercent ='pricespikepercent'


opEQ  = "EQ"
opNE  = "NE"
opAND = "AND"
opOR  = "OR"
opGT = "GT"
opGTE = "GTE"
opLT = "LT"
opLTE = "LTE"

Attributes = [ attrAsk,
              attrBid,
              attrLast,
              attrSettle]

Operators = [ opEQ,
              opNE,
              opAND,
              opOR,
              opGT,
              opGTE,
              opLT,
              opLTE]

tagsCondition =  [tagFilter,
            tagFilters,
            tagCondition,
            tagOperands,
            tagAttributes,
            tagLogging]


tagsMovingBox =  [tagFilter,
            tagFilters,
            tagMovingBox,
            tagPriceWidth,
            tagPriceOffset,
            tagAttributes,
            tagTimeMax,
            tagTodayOnly,
            tagLogging]


tagsSpikeAvoidance = [tagFilter,
            tagFilters,
            tagSpikeAvoidance,
            tagPriceSpikePercent,
            tagAttributes,
            tagTodayOnly,
            tagLogging]


occMandatory = 'mandatory'
occOptional = 'optional'
allOccurences = [occMandatory, occOptional]

# Condition
syntaxCondition = \
    [(tagFilter,              occMandatory),
    (tagFilters,                occMandatory),
    (tagCondition,               occMandatory),
    (tagOperands, 		  occMandatory),
    (tagAttributes,            occOptional),
    (tagLogging,             occOptional)]


# MovingBox
syntaxMovingBox = \
    [(tagFilter,              occMandatory),
    (tagFilters,                occMandatory),
    (tagMovingBox,               occMandatory),
    (tagPriceWidth, 		  occMandatory),
    (tagPriceOffset,            occOptional),
    (tagAttributes,            occOptional),
    (tagTimeMax,               occOptional),
    (tagTodayOnly,             occOptional),
    (tagLogging,             occOptional)]


# SpikeAvoidance
syntaxSpikeAvoidance = \
    [(tagFilter,              occMandatory),
    (tagFilters,                occMandatory),
    (tagSpikeAvoidance,               occMandatory),
    (tagPriceSpikePercent, 		  occOptional),
    (tagAttributes,            occOptional),
    (tagTodayOnly,             occOptional),
    (tagLogging,             occOptional)]


def ValidateXMLData(xml_data):
    try:

        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET

        validStatus = validationStatus.SUCCESS

        tree = ET.fromstring(xml_data)

        if(tree.tag.lower() != tagFilters):
            raise Exception("Mandatory parameter filters missing in syntax")
            validStatus = validationStatus.FAILURE
        if(tree[0].tag.lower() != tagFilter):
            raise Exception("Mandatory parameter filter missing in syntax")
            validStatus = validationStatus.FAILURE


        if(tree[0][0].tag.lower() == tagCondition):
            syntax = syntaxCondition
            allTag = tagsCondition
        elif(tree[0][0].tag.lower() == tagMovingBox):
            syntax = syntaxMovingBox
            allTag = tagsMovingBox
        elif(tree[0][0].tag.lower() == tagSpikeAvoidance):
            syntax = syntaxSpikeAvoidance
            allTag = tagsSpikeAvoidance
        else:
            raise Exception("Mandatory strategy parameter missing in syntax")
            validStatus = validationStatus.FAILURE


        for (tag, occ) in syntax:
            iFound = 0
            for elem in tree.getiterator():
                if(elem.tag.lower() == "operand"):
                     if(elem.child.tag.lower() != tagAttributes and elem.child.tag.lower() != tagLogging):
                        if(elem.child.tag not in Operators):
                            raise Exception("Invalid operator %s in syntax" % elem.tag)
                            validStatus = validationStatus.FAILURE

                if(elem.tag.lower() == "attributes"):
                    allAttributes = elem.text.split()
                    for attr in allAttributes:
                        if(attr.lower() not in Attributes):
                            raise Exception("Invalid attribute %s in syntax" % attr)
                            validStatus = validationStatus.FAILURE

                if(elem.tag.lower() not in allTag):
                    if elem.tag in Operators:
                        continue
                    elif(tree[0][0].tag.lower() == tagCondition):
                        continue
                    else:
                        raise Exception("Invalid tag %s in syntax" % elem.tag)
                        validStatus = validationStatus.FAILURE


                if(tag.lower() == elem.tag.lower()):
                    iFound = 1
                    break

            if(iFound == 0 and occ == occMandatory):
                raise Exception("Mandatory parameter %s missing in syntax" % tag)
                validStatus = validationStatus.FAILURE

        return validStatus

    except Exception, e:
        errmsg = "XML data parsing error %s"  % str(e)
        print(errmsg)
        ael.log(errmsg)
        validStatus = validationStatus.FAILURE
        return validStatus
