"""=================================================================================
MODULE
    FPriceLinkDefinitionValidation

DESCRIPTION
    This script is a validation script which validates all the columns in the
    new PriceLinkDefinition table, either:
    - from the new PriceLinkSpecification GUI
    - from the PriceLinkDefinitionUpgrade script
    - or manually when adding or updating any column in the new PriceLinkDefinition
      table via another script

If the validation fails, the changes made to the columns in the PriceLinkDefinition
table will not be saved.
================================================================================="""
import ael
import acm
import FPriceDistributorValidation
import FPriceDefinitionValidation
import FPriceXMLValidation

# token types
typeString = 'string'
typeInt = 'int'
typeFloat = 'float'
typeChoice = 'choice'
typeTime = 'time'
typeBool = 'bool'
allTypes = [typeString, typeInt, typeFloat, typeChoice, typeTime, typeBool]

# dirty_interval default
dirty_interval = None

# tokens
tokenService                 ='service'
tokenIdp_Code                ='idp_code'
tokenIdp_Code_APH            ='idp_code'
tokenSemantic                ='semantic'
tokenStart_Time              ='start_time'
tokenStop_Time               ='stop_time'
tokenIs_Fraction             ='is_fraction'
tokenUpdate_Interval         ='update_interval'
tokenLast_Follow_Interval    ='last_follow_interval'
tokenDirty_Interval          ='dirty_interval'
tokenNot_Active              ='not_active'
tokenDiscard_Zero_Price      ='discard_zero_price'
tokenDiscard_Zero_Quantity   ='discard_zero_quantity'
tokenDiscard_Negative_Price  ='discard_negative_price'
tokenForce_Update            ='force_update'
tokenKeep_Intraday_Prices    ='keep_intraday_prices'
tokenMultiplication_Factor   ='multiplication_factor'
tokenAddition_Addend         ='addition_addend'
tokenErrmsg                  ='errmsg'
tokenLog_Price               ='log_price'
tokenDoNot_Reset_Fields      ='donot_reset_fields'
tokenXml_Data                ='xml_data'
distributor_type             ='distributor_type'

allTokens = [tokenService,
            tokenIdp_Code,
            tokenSemantic,
            tokenNot_Active,
            tokenIs_Fraction,
            tokenStart_Time,
            tokenStop_Time,
            tokenDirty_Interval,
            tokenUpdate_Interval,
            tokenLast_Follow_Interval,
            tokenDiscard_Zero_Price,
            tokenDiscard_Zero_Quantity,
            tokenDiscard_Negative_Price,
            tokenForce_Update,
            tokenKeep_Intraday_Prices,
            tokenAddition_Addend,
            tokenMultiplication_Factor,
            tokenErrmsg,
            tokenLog_Price,
            tokenDoNot_Reset_Fields,
            tokenXml_Data]

# tokenValidations
# format: token: (prettyName, type, type argument list, exclude list
# type argument list format:
#       typeString: ignored
#       typeInt:    None or [minval, maxval]
#       typeBool:   None or [minval, maxval]
#       typeFloat:  None or [minval, maxval]
#       typeChoice: list of valid values, like ['0', '1', '2']
#       typeTime:   ignored
# exclude argument list format: [[type, type argument list], ...]
#  if a value matches a given type but also an exclude type, it will be considered invalid
tokenValidations = {tokenIdp_Code: ('IDP Code', typeString, [0, 63], None),
                    tokenService: ('Service', typeString, None, None),
                    tokenSemantic: ('Semantic', typeString, None, None),
                    tokenNot_Active: ('Not Active', typeBool, [0, 1], None),
                    tokenIs_Fraction: ('Digital/Fraction',  typeBool, [0, 1], None),
                    tokenStart_Time: ('Start Time', typeTime, [0, 1439], None),
                    tokenStop_Time: ('Stop Time', typeTime, [0, 1439], None),
                    tokenDirty_Interval: ('Dirty Interval', typeInt, [0, 1000000000], None),
                    tokenUpdate_Interval: ('Update Interval', typeInt, [-1, 1000000000], None),
                    tokenLast_Follow_Interval: ('Last Follow Interval', typeBool, [0, 1], None),
                    tokenDiscard_Zero_Price: ('Discard Zero Price', typeChoice, ['None', 'True', 'False'], None),
                    tokenDiscard_Zero_Quantity: ('Discard Zero Quantity', typeChoice, ['None', 'True', 'False'], None),
                    tokenDiscard_Negative_Price: ('Discard Negative Price', typeChoice, ['None', 'True', 'False'], None),
                    tokenForce_Update: ('Force Update', typeChoice, ['None', 'True', 'False'], None),
                    tokenKeep_Intraday_Prices: ('Keep Intraday Prices', typeChoice, ['None', 'True', 'False'], None),
                    tokenAddition_Addend: ('Addition Addend', typeFloat, [-1000000000, 1000000000], None),
                    tokenMultiplication_Factor: ('Multiplication Factor', typeFloat, [-1000000000, 1000000000], None),
                    tokenErrmsg: ('Error Message', typeString, [0, 63], None),
                    tokenLog_Price: ('Log Prices', typeBool, [0, 1], None),
                    tokenDoNot_Reset_Fields: ('Do Not Reset Fields', typeInt, [-1, 32767], None),
                    tokenXml_Data: ('XML Data', typeString, None, None)}

occMandatory = 'mandatory'
occOptional = 'optional'
allOccurences = [occMandatory, occOptional]

# syntax definition
# format: [(token, occurrence), (token, occurrence), ...]

# Valid syntaxes
# For APH
# If len is 1, it is the IDP Code
# If len is 2, it is APH(Service + IDP Code) (NOTE : APH and AMPH are Differentiated from its Distributor name)
# If len is 3 or greater, it is APH(Service+IDP+Semantics+additional parameters)
# For AMPH
# If len is 1, it is the IDP Code
# If len is greater then 1, it is AMPH(IDP+PRIO+START+additional parameters)

# APH
aphSyntax = \
    [(tokenIdp_Code,              occMandatory),
    (tokenService,                occOptional),
    (tokenSemantic,               occOptional),
    (tokenNot_Active, 		  occOptional),
    (tokenIs_Fraction,            occOptional),
    (tokenStart_Time,             occOptional),
    (tokenStop_Time,              occOptional),
    (tokenDirty_Interval,         occOptional),
    (tokenUpdate_Interval,        occOptional),
    (tokenLast_Follow_Interval,   occOptional),
    (tokenDiscard_Zero_Price,     occOptional),
    (tokenDiscard_Zero_Quantity,  occOptional),
    (tokenDiscard_Negative_Price, occOptional),
    (tokenForce_Update,           occOptional),
    (tokenKeep_Intraday_Prices,   occOptional),
    (tokenAddition_Addend,        occOptional),
    (tokenMultiplication_Factor,  occOptional),
    (tokenErrmsg,                 occOptional),
    (tokenLog_Price,              occOptional),
    (tokenDoNot_Reset_Fields,     occOptional),
    (tokenXml_Data,               occOptional)]

# AMPH
amphSyntax = \
    [(tokenIdp_Code,              occMandatory),
    (tokenNot_Active, 		  occOptional),
    (tokenIs_Fraction,            occOptional),
    (tokenStart_Time,             occOptional),
    (tokenStop_Time,              occOptional),
    (tokenDirty_Interval,         occOptional),
    (tokenUpdate_Interval,        occOptional),
    (tokenLast_Follow_Interval,   occOptional),
    (tokenDiscard_Zero_Price,     occOptional),
    (tokenDiscard_Zero_Quantity,  occOptional),
    (tokenDiscard_Negative_Price, occOptional),
    (tokenForce_Update,           occOptional),
    (tokenKeep_Intraday_Prices,   occOptional),
    (tokenAddition_Addend,        occOptional),
    (tokenMultiplication_Factor,  occOptional),
    (tokenErrmsg,                 occOptional),
    (tokenLog_Price,              occOptional),
    (tokenDoNot_Reset_Fields,     occOptional),
    (tokenXml_Data,               occOptional)]

# aphAllSyntaxes and amphAllSyntaxes
# format: [(syntax, prettyName), (syntax, prettyName), ...]
aphAllSyntaxes = [(aphSyntax, 'APH')]

amphAllSyntaxes = [(amphSyntax, 'AMPH')]

# Validation of the syntaxes and tokens
def validateDataType(dataType, optArgs):
    if dataType == typeChoice:
        if not optArgs:
            raise Exception("WARN : Type %s must have an argument list with at least "\
                                                   "one valid value" % dataType)
        try:
            optArgs[0]
        except:
            raise Exception("WARN : Type %s must have an argument list with at least "\
                                                   "one valid value" % dataType)
    elif dataType == typeInt:
        pass  # todo
    elif dataType == typeFloat:
        pass  # todo
    elif dataType == typeString:
        pass  # todo
    elif dataType == typeBool:
        if not optArgs:
            raise Exception("WARN : Type %s must have an argument list with at least "\
                                                   "one valid value" % dataType)
        try:
            optArgs[0]
        except:
            raise Exception("WARN : Type %s must have an argument list with at least "\
                                                   "one valid value" % dataType)


def validateTokenValidation(token, prettyName, dataType, optArgs, notTypeEntries):
    global allTokens, allTypes, typeChoice, typeInt, typeFloat, typeBool

    if not token in allTokens:
        raise Exception("WARN : Invalid token, missing in allTokens")
    if not prettyName:
        raise Exception("WARN : Nice name missing")
    if not dataType in allTypes:
        raise Exception("WARN : Invalid type '%s', missing in allTypes" % dataType)

    validateDataType(dataType, optArgs)

    if notTypeEntries:
        for notEntry in notTypeEntries:
            notEntryLen = len(notEntry)
            notType = None
            notTypeOptArgs = None

            if notEntryLen < 1 or notEntryLen > 2:
                raise Exception("WARN : Invalid exclude definition, definition '%s'"\
                                                                          % notEntry)
            if notEntryLen > 0:
                notType = notEntry[0]
            if notEntryLen > 1:
                notTypeOptArgs = notEntry[1]

            try:
                validateDataType(notType, notTypeOptArgs)
            except Exception, extraInfo:
                errMsg = "%s. <Invalid exclude definition, definition '%s'"\
                                                  %(str(extraInfo), notEntry)
                if notTypeOptArgs:
                    errMsg += ", arguments '%s'>" % notTypeOptArgs
                print errMsg
                raise Exception(errMsg)

def validateSyntax(syntax, name):
    global allTokens, allOccurences, occOptional, occMandatory

    count = 0
    foundOptional = False
    for (token, occ) in syntax:
        if not token:
            raise Exception("Invalid entry in syntax '%s', token missing" % name)
        if not token in allTokens:
            raise Exception("Invalid token '%s' in syntax '%s'" % (token, name))
        if not occ:
            raise Exception("Invalid entry in syntax '%s', occurence missing" % name)
        if not occ in allOccurences:
            raise Exception("Invalid occurence '%s' for token '%s' in syntax '%s'" % (occ, token, name))
        if occ == occOptional and count == 0:
            raise Exception("Invalid occurence '%s' for the first token '%s' in syntax '%s'" % (occ, token, name))
        if occ == occMandatory and foundOptional:
            raise Exception("Invalid occurence '%s' after '%s' for the token '%s' in syntax '%s'" % (occ, occOptional, token, name))
        if occ == occOptional:
            foundOptional = True
        count += 1


def validateSyntaxes(aph):
    global aphAllSyntaxes, amphAllSyntaxes

    aph_amph={"APH":aphAllSyntaxes, "AMPH":amphAllSyntaxes}

    try:
        for key in tokenValidations.keys():
            (prettyName, dataType, optArgs, notEntries) = tokenValidations[key]
            try:
                validateTokenValidation(key, prettyName, dataType, optArgs, notEntries)
            except Exception, extraInfo:
                print str(extraInfo)
                ael.log(str(extraInfo))

    except Exception, e:
        print "Error when accessing token validations list: %s" % str(e)
        ael.log(str(e))

    try:
        for (syntax, name) in aph_amph[aph]:
            try:
                validateSyntax(syntax, name)
            except Exception, e:
                print "Error in syntax '%s': %s" % (name, e)
    except Exception, e:
        print "Error when accessing syntax list: %s" % e

def matchInt(val, prettyName, optArgs):
    converted = 0
    try:
        converted = int(val)
    except:
        raise Exception("Value '%s' for token '%s' is not an integer" % (val, prettyName))
    if optArgs:
        try:
            if len(optArgs) > 0 and converted < int(optArgs[0]):
                raise Exception("Too small value, %d < %d, for token '%s'" % (converted, int(optArgs[0]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in minimum range '%s'" % (prettyName, converted, optArgs[0]))
        try:
            if len(optArgs) > 1 and converted > int(optArgs[1]):
                raise Exception("Too large value, %d > %d, for token '%s'" % (converted, int(optArgs[1]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in maximum range '%s'" % (prettyName, converted, optArgs[1]))

def matchBool(val, prettyName, optArgs):
    if optArgs:
        try:
            if not val in optArgs:
                raise Exception("Invalid value '%s' for token '%s', valid values %s" % (val, prettyName, optArgs))
        except:
            raise Exception("In-valid boolean value for token '%s'" % prettyName)
    else:
        raise Exception("In-valid boolean value for token'%s'" % prettyName)


def matchFloat(val, prettyName, optArgs):
    converted = 0
    try:
        converted = float(val)
    except:
        raise Exception("Value '%s' for token '%s' is not a float" % (val, prettyName))
    if optArgs:
        try:
            if len(optArgs) > 0 and converted < float(optArgs[0]):
                raise Exception("Too small value, %d < %d, for token '%s'" % (converted, float(optArgs[0]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in minimum range '%s'" % (prettyName, converted, optArgs[0]))
        try:
            if len(optArgs) > 1 and converted > float(optArgs[1]):
                raise Exception("Too large value, %d > %d, for token '%s'" % (converted, float(optArgs[1]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in maximum range '%s'" % (prettyName, converted, optArgs[1]))

def matchChoice(val, prettyName, optArgs):
    if optArgs:
        try:
            if not val in optArgs:
                raise Exception("Invalid value '%s' for token '%s', valid values %s" % (val, prettyName, optArgs))
        except:
            raise Exception("List of valid choices missing for token '%s'" % prettyName)
    else:
        raise Exception("List of valid choices missing for token '%s'" % prettyName)


def format_time(time_val):
    hours = minutes = time_hm = ""
    hours = str(int(time_val)/60)
    hours = hours.zfill(2)
    minutes = str(int(time_val)%60)
    minutes = minutes.zfill(2)
    time_hm = hours + minutes
    return time_hm

def matchTime(val, prettyName, optArgs):
    if val != -1:
        val = format_time(val)
    valLen = len(str(val))
    if valLen < 0 or valLen > 5:
        if val != -1:
            raise Exception("Invalid time '%s' for token '%s', valid formats "\
                   "are H:MM and HH:MM, where HH:MM should be less then 23:59"\
                                                            % (val, prettyName))
    try:
        #matchInt(val, prettyName, None)
        if valLen == 4:
            matchInt(str(val)[0:2], prettyName, [0, 23])
            matchInt(str(val)[2:4], prettyName, [0, 59])
        elif valLen == 3:
            matchInt(str(val)[0:1], prettyName, [0, 9])
            matchInt(str(val)[1:3], prettyName, [0, 59])
    except:
        raise Exception("Invalid time '%s' for token '%s', valid formats are "\
        "H:MM and HH:MM, where HH:MM should be less then 23:59" %(val, prettyName))

def matchString(val, prettyName, optArgs):
    converted = 0
    try:
        converted = len(val)
    except:
        raise Exception("Value '%s' for token '%s' is not a String" % (val, prettyName))
    if optArgs:
        try:
            if len(optArgs) > 0 and converted < int(optArgs[0]):
                raise Exception("Too small length for string, %d < %d, for token '%s'"\
                                          % (converted, float(optArgs[0]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in minimum range '%s'"\
                                          % (prettyName, converted, optArgs[0]))
        try:
            if len(optArgs) > 1 and converted > int(optArgs[1]):
                raise Exception("Length of String Exceeds max limit, %d > %d, "\
                      "for token '%s'" % (converted, int(optArgs[1]), prettyName))
        except:
            raise Exception("Token '%s':%d is not in maximum range '%s'"\
                                          % (prettyName, converted, optArgs[1]))

def matchToken(val, prettyName, dataType, optArgs, notDataTypes):
    global typeString, typeInt, typeFloat, typeChoice, typeTime

    if dataType == typeString:
        matchString(val, prettyName, optArgs)
    elif dataType == typeInt:
        matchInt(val, prettyName, optArgs)
    elif dataType == typeFloat:
        matchFloat(val, prettyName, optArgs)
    elif dataType == typeChoice:
        matchChoice(val, prettyName, optArgs)
    elif dataType == typeTime:
        matchTime(val, prettyName, optArgs)
    elif dataType == typeBool:
        matchBool(val, prettyName, optArgs)

    if notDataTypes:
        for notEntry in notDataTypes:
            notEntryLen = len(notEntry)
            notTypeOptArgs = None

            if notEntryLen < 1 or notEntryLen > 2:
                raise Exception("Invalid exclude definition for token '%s', definition '%s'" % (prettyName, notEntry))
            if notEntryLen > 0:
                notType = notEntry[0]
            if notEntryLen > 1:
                notTypeOptArgs = notEntry[1]

            err = ""
            try:
                matchToken(val, "dummy", notType, notTypeOptArgs, None)
                err = "Invalid string '%s' for token '%s', matches exclude type '%s'" % (val, prettyName, notType)
                if notTypeOptArgs:
                    err += " with arguments %s" % notTypeOptArgs
            except:
                pass

            if err:
                raise Exception(err)

def matchSyntax(syntax, parts, resultList = None):
    global tokenValidations, occMandatory, occOptional

    partIndex = 0
    for (token, occ) in syntax:
        (prettyName, dataType, optArgs, notDataTypes) = tokenValidations[token]

        part = None
        if partIndex < len(parts):
            part = parts[partIndex]
        partIndex += 1

        if occ == occMandatory:
            if not part:
                raise Exception("Mandatory token '%s' missing" % prettyName)
        elif occ == occOptional:
            if not part:
                continue
        matchToken(part, prettyName, dataType, optArgs, notDataTypes)

        if resultList is not None:
            resultList.append((prettyName, part));

    if partIndex < len(parts):
        raise Exception("Superfluous data %s" % parts[partIndex:])


def resultString(pld, lines, resultList):
    defnbr = pld.defnbr
    ins = pld.insaddr.display_id()
    curr = pld.curr.display_id()
    market = pld.source_ptynbr.display_id()

    str = "PriceLinkDefinition"
    if defnbr:
        str += " (%d)" % defnbr
    str += "\n"

    str += "  instrument '%s'\n" % ins
    str += "  currency '%s'\n" % curr
    str += "  market '%s'\n" % market

    if resultList:
        for (name, status, tokens) in resultList:
            str += "    Syntax: '%s', Result: '%s', Matches: %s\n" % (name, status, tokens)

    return str

def raiseResultException(pld, lines, msg, resultList):

    err = "Error in PriceLinkDefinition"
    if pld:
        defnbr = pld.defnbr
        ins = pld.insaddr.display_id()
        curr = pld.curr.display_id()
        market = pld.source_ptynbr.display_id()

        if defnbr:
            err += " (defnbr: %d)" % defnbr
        err += "\n"

        err += "  Instrument: '%s'\n" % ins
        err += "  Currency  : '%s'\n" % curr
        err += "  Market    : '%s'\n" % market

        err += "WARN : '%s'\n" % msg

    if resultList:
        for (name, status, tokens) in resultList:
            err += "    Syntax: '%s', Result: '%s', Matches: %s\n" % \
                                                        (name, status, tokens)

    print "Validation Error: %s" %err
    raise Exception(err)

def exc(w, e):
    errorMsg = "%s. <Exception: %s> "%(w, e)
    print errorMsg
    ael.log(errorMsg)

def getAttributeFromPLD(pld_pd, attribute):
    retattribute = ''
    try:
        retattribute = getattr(pld_pd, attribute)
    except Exception, e:
        exc("WARN : Unknown attribute %s for PLD object."%attribute, e)
    return retattribute

def validateColumns(columnList, aph, resultList):
    global aphAllSyntaxes, amphAllSyntaxes

    dLen = len(columnList)
    if not dLen:
        raise Exception("ERROR : Price Link Definition grid is empty.\n")

    aph_amph={"APH":aphAllSyntaxes, "AMPH":amphAllSyntaxes}

    matching = []

    for (s, name) in aph_amph[aph]:
        syntaxResult = []
        try:
            matchSyntax(s, columnList, syntaxResult)
            matching.append(name)
            resultList.append((name, "OK", syntaxResult))
        except Exception, e:
            resultList.append((name, str(e), syntaxResult))

    if len(matching) > 0:
        return matching
    raise Exception("ERROR : Invalid Entry in Price link definition grid.\n")

def readPriceLinkDefinitionColumns(pld, listOfColumnsinPLD, aph):
    try:
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'idp_code'))
        if aph == 'APH':
            if getAttributeFromPLD(pld, 'service') != None:
                if getAttributeFromPLD(pld, 'service') != '':
                    listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'service').display_id())
                else:
                    listOfColumnsinPLD.append('NULL')
            else:
                listOfColumnsinPLD.append('NULL')
        if aph == 'APH':
            if getAttributeFromPLD(pld, 'semantic') != None:
                if getAttributeFromPLD(pld, 'semantic') != '':
                    listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'semantic').display_id())
                else:
                    listOfColumnsinPLD.append('NULL')
            else:
                listOfColumnsinPLD.append('NULL')
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'not_active'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'is_fraction'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'start_time'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'stop_time'))
        listOfColumnsinPLD.append(dirty_interval)
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'update_interval'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'last_follow_interval'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'discard_zero_price'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'discard_zero_quantity'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'discard_negative_price'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'force_update'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'keep_intraday_prices'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'addition_addend'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'multiplication_factor'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'errmsg'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'log_price'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'donot_reset_fields'))
        listOfColumnsinPLD.append(getAttributeFromPLD(pld, 'xml_data'))

    except Exception, e:
        print "INFO : Validation FAIL!!\n"
        ael.log("INFO : Validation FAIL!!\n")
        raiseResultException(pld, '', listOfColumnsinPLD, e)

def getUpdateInterval(priceLinkDefinitionObj):
    '''Retrieve update interval from PLD object. If at PLD level it is -1
        return update interval of price distributor'''
    updateInterval = -1
    if priceLinkDefinitionObj:
        updateInterval = getAttributeFromPLD(priceLinkDefinitionObj, 'update_interval')
        if -1 == updateInterval:
            #If update_interval = -1 then fetch the update_interval from price distributor
            disnbr = getAttributeFromPLD(priceLinkDefinitionObj, 'disnbr')
            if disnbr:
                priceDistributor = ael.PriceDistributor[disnbr.display_id()]
                try:
                     updateInterval =  getattr(priceDistributor, 'update_interval')

                except Exception, e:
                    print "WARN : Unable to retrieve 'update_interval' from Price "\
                                                               "Distributor object."

    return updateInterval

def getXMLData(priceLinkDefinitionObj):
    '''Retrieve update interval from PLD object. If at PLD level it is -1
        return update interval of price distributor'''
    xmlData = ""
    if priceLinkDefinitionObj:
        xmlData = getAttributeFromPLD(priceLinkDefinitionObj, 'xml_data')
        if "" == xmlData:
            #If xml_data is blank then fetch the it from price distributor
            disnbr = getAttributeFromPLD(priceLinkDefinitionObj, 'disnbr')
            if disnbr:
                priceDistributor = ael.PriceDistributor[disnbr.display_id()]
                try:
                     xmlData =  getattr(priceDistributor, 'xml_data')

                except Exception, e:
                    print "WARN : Unable to retrieve 'xml_data' from Price "\
                                                               "Distributor object."

    return xmlData

def validatePriceLinkDefinition(pld, printResult = False):
    if not pld:
        return

    nbOfColumnsPLD = []
    APH_AMPH = ''
    distributor_type = ''
    pd_service = None
    pd_semantic = None
    pld_service = None
    pld_semantic = None
    matching = None
    resultList = []

    #Determine if Distributor is APH ro AMPH
    if getAttributeFromPLD(pld, 'disnbr') != None:
        AMPH_disnbr = getAttributeFromPLD(pld, 'disnbr').disnbr
        DistributorNumbers = ael.PriceDistributor.select()
        for disnbr in DistributorNumbers:
            disnumber = getAttributeFromPLD(disnbr, 'disnbr')
            if disnumber == AMPH_disnbr:
                disName = getAttributeFromPLD(disnbr, 'disid')
                dirty_interval = getAttributeFromPLD(disnbr, 'dirty_interval')
                distributor_type = getAttributeFromPLD(disnbr, 'distributor_type')
                pd_service = getAttributeFromPLD(disnbr, 'service')
                pd_semantic = getAttributeFromPLD(disnbr, 'semantic')
                if 'AMPH' == disName.upper().split('_')[0]:
                    APH_AMPH = 'AMPH'
                else:
                    APH_AMPH = 'APH'
    else:
        print "WARN: Invalid Price link defintion. Price link defintion is "\
                                                  "not mapped to any distributor."
        return

    #Read service and semantic
    pld_service = getAttributeFromPLD(pld, 'service')
    pld_semantic = getAttributeFromPLD(pld, 'semantic')

    if distributor_type == 'Bloomberg':
        if pld_service != None:
            if pld_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for"\
                " distributor of type Bloomberg in price_link_definition table"\
                                        %(pld_service.display_id()), resultList)

        if pd_service != None:
            if pd_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for"\
                    " distributor of type Bloomberg in price_distributor table"\
                                         %(pd_service.display_id()), resultList)

        if pld_semantic == None:
            if pd_semantic == None:
                raiseResultException(pld, '', "Semantic is required for distributor"\
                           " of type Bloomberg in either price_distributor or "\
                                      "price_link_definition table", resultList)

        if pld_semantic != None:
            if pld_semantic.display_id() == '':
                if pd_semantic != None:
                    if pd_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for "\
                        "distributor of type Bloomberg in either  price_link_definition"\
                                  " or price_distributor table", resultList)

        if pd_semantic == None:
            if pld_semantic == None:
                raiseResultException(pld, '', "Semantic required for distributor"\
                           " of type Bloomberg in either price_link_definition or "\
                                      "price_distributor table", resultList)

        if pd_semantic != None:
            if pd_semantic.display_id() == '':
                if pld_semantic != None:
                    if pld_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for "\
                        "distributor of type Bloomberg in either price_distributor"\
                                  " or price_link_definition table", resultList)

    elif distributor_type == 'MarketMap':
        if pld_service != None:
            if pld_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for distributor of type MarketMap in price_link_definition table"\
                %(pld_service.display_id()), resultList)

        if pd_service != None:
            if pd_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for distributor of type MarketMap in price_distributor table"\
                %(pd_service.display_id()), resultList)

        if pld_semantic == None:
            if pd_semantic == None:
                raiseResultException(pld, '', "Semantic required for distributor of type MarketMap in either price_link_definition or price_distributor table", resultList)

        if pld_semantic != None:
            if pld_semantic.display_id() == '':
                if pd_semantic != None:
                    if pd_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for distributor of type MarketMap in either price_link_definition or price_distributor table", resultList)

        if pd_semantic == None:
            if pld_semantic == None:
                raiseResultException(pld, '', "Semantic required for distributor of type MarketMap in either price_link_definition or price_distributor table", resultList)

        if pd_semantic != None:
            if pd_semantic.display_id() == '':
                if pld_semantic != None:
                    if pld_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for distributor of type MarketMap in either price_link_definition or price_distributor table", resultList)

    elif distributor_type == 'Reuters':
        if pld_service == None:
            if pd_service == None:
                raiseResultException(pld, '', "Service required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pld_service != None:
            if pld_service.display_id() == '':
                if pd_service != None:
                    if pd_service.display_id() == '':
                        raiseResultException(pld, '', "Service required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pd_service == None:
            if pld_service == None:
                raiseResultException(pld, '', "Service required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pd_service != None:
            if pd_service.display_id() == '':
                if pld_service != None:
                    if pld_service.display_id() == '':
                        raiseResultException(pld, '', "Service required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pld_semantic == None:
            if pd_semantic == None:
                raiseResultException(pld, '', "Semantic required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pld_semantic != None:
            if pld_semantic.display_id() == '':
                if pd_semantic != None:
                    if pd_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pd_semantic == None:
            if pld_semantic == None:
                raiseResultException(pld, '', "Semantic required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

        if pd_semantic != None:
            if pd_semantic.display_id() == '':
                if pld_semantic != None:
                    if pld_semantic.display_id() == '':
                        raiseResultException(pld, '', "Semantic required for distributor of type Reuters in either price_link_definition or price_distributor table", resultList)

    elif distributor_type == 'AMS':
        if pld_service != None:
            if pld_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for AMPH distributor in price_link_definition table"\
                %(pld_service.display_id()), resultList)
        if pld_semantic != None:
            if pld_semantic.display_id() != '':
                raiseResultException(pld, '', "Semantic: '%s' is not required for AMPH distributor in price_link_definition table"\
                %(pld_semantic.display_id()), resultList)
        if pd_service != None:
            if pd_service.display_id() != '':
                raiseResultException(pld, '', "Service: '%s' is not required for AMPH distributor in price_distributor table"\
                %(pd_service.display_id()), resultList)
        if pd_semantic != None:
            if pd_semantic.display_id() != '':
                raiseResultException(pld, '', "Semantic: '%s' is not required for AMPH distributor in price_distributor table"\
                %(pd_semantic.display_id()), resultList)

    #Read Column Values
    readPriceLinkDefinitionColumns(pld, nbOfColumnsPLD, APH_AMPH)

    #Validate Conditions...
    update_interval = getUpdateInterval(pld)
    if ((update_interval > -1) and dirty_interval):
        if  dirty_interval <= update_interval:
            raiseResultException(pld, '', "Update Interval: %d, should be less than Dirty Interval: %d, Dirty Interval is set at distributor level."\
            %(update_interval, dirty_interval), resultList)

    if getAttributeFromPLD(pld, 'multiplication_factor') == 0:
        print "WARNING: Prices will be multiplied by ZERO as multiplication factor is %d for '%s'"%(getAttributeFromPLD(pld, 'multiplication_factor'), getAttributeFromPLD(pld, 'idp_code'))


    #Validate XML data
    xml_data = getXMLData(pld)
    if xml_data:
        FPriceXMLValidation.ValidateXMLData(xml_data)

    #Validate Columns...
    try:
        matching = validateColumns(nbOfColumnsPLD, APH_AMPH, resultList)
    except Exception, e:
        raiseResultException(pld, nbOfColumnsPLD, str(e), resultList)

    if len(matching) > 1:
        raiseResultException(pld, nbOfColumnsPLD, "Ambigous match, Column : %s"%matching, resultList)

    if printResult:
        print resultString(pld, nbOfColumnsPLD, resultList)

    #Validate Syntaxes...
    validateSyntaxes(APH_AMPH)


def validate_transaction(transaction_list,*rest):
    out_list = []
    for (o, op) in transaction_list:
        if o.record_type == 'PriceLinkDefinition' and op <> 'Delete':
            validatePriceLinkDefinition(o)
            out_list.append((o, op))
        elif o.record_type == 'PriceDefinition' and op <> 'Delete':
	    FPriceDefinitionValidation.validatePriceLinkDefinition(o)
            out_list.append((o, op))
        elif o.record_type == 'PriceDistributor' and op <> 'Delete':
            if FPriceDistributorValidation.validate_transaction(o):
                out_list.append((o, op))
    return out_list

