"""------------------------------------------------------------------------
MODULE
    FIntegrationTestComponentUtils -
DESCRIPTION:
    The module that contains APIs to be used for testing sanity of the component
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within
     the core is not supported.
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this
     module at user end
--------------------------------------------------------------------------"""
import ast
import acm
import FLogger
logger = FLogger.FLogger(name=__name__, level=1)
def checkTradeTypeExists(trade_type):
    """returns True if the trade type in the input argument exists in ADS, else returns False"""
    trade_type_enum = None
    trade_type_enum_exists = False
    try:
        trade_type_enum = acm.EnumFromString('TradeType', trade_type)
        if trade_type_enum:
            trade_type_enum_exists = True
    except:
        pass
    if not trade_type_enum:
        logger.error("TradeType <%s> is not supported in ADS" % trade_type)
    return trade_type_enum_exists

def checkPartyExists(party_name):#this function needs to be moved into FIntegrationUtils
    """returns the party object if the party name in the input argument exists in ADS"""
    valid_party = acm.FParty[party_name]
    if not valid_party:
        logger.error("Party <%s> does not exist in ADS."%party_name)
    return valid_party

def checkPartyExistsWithType(party_name, party_type=None):
    """returns True if the party of a given type exists in ADS, else it returns False"""
    valid_party = False
    if party_type:
        try:
            valid_party = eval("acm." + party_type + "['" + party_name + "']")
            if not valid_party:
                valid_party = checkPartyExists(party_name)
                if valid_party:
                    logger.warn("Party <%s> is expected to be of type <%s>.\
                     However, it exists in ADS of type <%s>"%(party_name,\
                                                              party_type, valid_party.Type()))
            else:
                valid_party = True
        except:
            pass
    else:
        valid_party = checkPartyExists(party_name)
        if valid_party:
            logger.debug("Party <%s> exists in ADS of type <%s>"%(party_name, valid_party.Type()))
            valid_party = True
    return valid_party

def checkAliasTypeExists(acm_object_type, alias_type):
    """returns True is the alias Type on the mentioned class in the\
    input argument exists in ADS, else it returns False"""
    alias_type_exists = False
    alias_type_lookup = {'Party' : 'FPartyAliasType', 'Instrument' : 'FInstrAliasType'}
    if acm_object_type in list(alias_type_lookup.keys()):
        val = "acm." + alias_type_lookup[acm_object_type] + "['" + alias_type + "']"
        try:
            alias_type_obj = eval("acm." + alias_type_lookup[\
                                acm_object_type] + "['" + alias_type + "']")
            logger.debug("AliasType <%s> exists on <%s>"%(alias_type, acm_object_type))
            if not alias_type_obj:
                logger.error("AliasType <%s> does not exist on <%s>"%(alias_type, acm_object_type))
            else:
                alias_type_exists = True
        except:
            pass
    return alias_type_exists

def checkAliasValuesExists(parent_object_type, alias_type, alias_name):
    """returns True is an alias of a specific type on the class exists in ADS, else returns False"""
    alias_exists = True
    alias_type_count = len(eval("acm." + alias_type + '.Select("type = ' + "'" + \
                alias_name + "'" + '")'))
    if alias_type_count == 0:
        logger.warn("<%s> is not set on %s(s) in ADS. Please check the data preparation"%(\
        alias_name, parent_object_type))
        alias_exists = False
    return alias_exists

def checkAddInfoSpecExists(acm_class, addinfo_spec_name):
    """returns True if the AdditionalInfoSpec exists on the given class. else returns False """
    addinfo_spec_exists = False
    addinfo_spec = acm.FAdditionalInfoSpec[addinfo_spec_name]
    if addinfo_spec:
        if addinfo_spec.RecType() == acm_class:
            logger.debug("<%s> on <%s> exists in ADS."%(acm_class, addinfo_spec_name))
            addinfo_spec_exists = True
        else:
            logger.error("<%s> exists on <%s> instead of on <%s> in ADS."%(\
                addinfo_spec_name, acm_class, addinfo_spec.RecType()))
    else:
        logger.error("<%s> on <%s> does not exist in ADS"%(addinfo_spec_name, acm_class))
    return addinfo_spec_exists

def checkChoiceLists(choice_list, choice_list_vals):
    """check if the ChoiceList exists along with all the values that are required in it"""
    all_choice_lists_exist = True
    updated_choice_list_vals = []
    for choice_list_val in choice_list_vals:
        update_choice_list = choice_list_val
        if len(choice_list_val) > 39:
            update_choice_list = choice_list_val[0:39]
        updated_choice_list_vals.append(update_choice_list)
    choice_lists_adm = acm.FChoiceList.Select("list = '%s'"%choice_list)
    choice_list_adm_names = []
    for choice_list_adm in choice_lists_adm:
        choice_list_adm_names.append(choice_list_adm.Name())
    if choice_lists_adm:
        if len(choice_lists_adm) < len(choice_list_vals):
            logger.warn("All ChoiceList values for <%s> does not exist within ADS."%(choice_list))
            all_choice_lists_exist = False
        else:
            for choice_list_val in updated_choice_list_vals:               
                if choice_list_val.strip() not in choice_list_adm_names:
                    logger.error("<%s> is not in ChoiceList <%s> in ADS."%(\
                            choice_list_val.strip(), choice_list))
                    all_choice_lists_exist = False
    else:
        logger.error("ChoiceList <%s> does not exist in ADS"%choice_list)
        all_choice_lists_exist = False
    return all_choice_lists_exist

def checkStateChartExists(state_chart_name):
    """check if the statechart exists"""
    state_chart_exists = False
    state_chart = acm.FStateChart[state_chart_name]
    if state_chart:
        state_chart_exists = True
    else:
        logger.error("StateChart <%s> does not exist in ADS"%state_chart_name)
    return state_chart_exists

def checkStateChartAddInfoExists(state_chart_name, addinfo_val, addinfo_spec_name):
    """check if the AddInfo for a given AddInfoSpec exists on the given statechart"""
    state_chart_addinfo_exists = False
    state_chart = acm.FStateChart[state_chart_name]
    if state_chart:
        add_info = eval("state_chart.AdditionalInfo()." + addinfo_spec_name + "()")
        if add_info:
            if add_info == addinfo_val:
                state_chart_addinfo_exists = True
            else:
                logger.error("AdditionalInfo <%s> on StateChart <%s> has value <%s>\
                 instead of <%s> in ADS"%(addinfo_spec_name,\
                                           state_chart_name, add_info, addinfo_val))
        else:
            logger.error("AdditionalInfo <%s> does not exist in StateChart\
             <%s> in ADS"%(addinfo_spec_name, state_chart_name))
    else:
        logger.error("StateChart <%s> does not exist in ADS"%state_chart_name)
    return state_chart_addinfo_exists

def get_fparameter_value(fparameter, module_name):
    """get the value of the given FParameter in the given module"""
    ext_obj = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', module_name)
    fparameter_val = None
    for key in ext_obj.Value().Keys():
        if key.AsString() == fparameter:
            fparameter_val = ext_obj.Value()[key]
            fparameter_val = str(fparameter_val).split('#')[0]
            if fparameter_val.count('{'):
                fparameter_val = fparameter_val.replace("'", "")
            
            if fparameter_val.find("'") == 0:
                fparameter_val = fparameter_val[1:]
                fparameter_val = fparameter_val[:-1]
            if fparameter_val.find('"') == 0:
                fparameter_val = fparameter_val[1:]
                fparameter_val = fparameter_val[:-1]
                
    return fparameter_val

def get_all_mandatory_fparameters(fparameter, module_name, fparameters_dict):
    """get all the mandatory FParameters"""
    ext_obj = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', module_name)
    key_list = []
    val_list = []
    for key in ext_obj.Value().Keys():
        key_list.append(str(key))
    for vals in ext_obj.Value().Values():
        vals = str(vals).split('#')[0]
        if vals.count('{') == 0:
            vals = vals.replace("'", "")
        val_list.append(str(vals))
    params_dict = dict(list(zip(key_list, val_list)))
    for each_val in params_dict:
        if params_dict[each_val] or params_dict[each_val].upper() != 'NONE':
            fparameters_dict[each_val] = params_dict[each_val]
        else:
            logger.error("FParameter <%s> is a mandatory FParameter\
             and its value is missing"%each_val)
    return fparameters_dict

def checkDataPrepOnParty(component_name, party):
    """check if all the data preparation on the party is\
     in place on the basis of the component that it is being used in"""
    data_prep_ready = True
    if component_name == 'AMWI-DealTaker':
        alias_name = None
        for alias in party.Aliases():
            if alias.Type().Name() == 'MarkitWireID':
                alias_name = alias.Name()
                break
        if party.LEI() or party.Swift() or alias_name:
            logger.debug("Party <%s> has the required data prep in place"%party.Name())
        else:
            data_prep_ready = False
            logger.error("Party<%s> does not have MarkitWireID/LEI/BIC setup."%party.Name())
    return data_prep_ready

def testChannel(channel, event, arg):
    """event callback for testing"""
    pass

def checkAMBChannelExists(message_broker, channel_name):
    """check if the provided channel is present in the AMB"""
    import amb
    channel_exists = False
    if message_broker:
        try:
            amb.mb_init(message_broker)
            if channel_name:
                reader = amb.mb_queue_init_reader(channel_name, testChannel, None)
                if reader:
                    channel_exists = True
                else:
                    logger.error(\
                        "The AMB channel <%s> is not present in ADS. Kindly check up your setup."%\
                            channel_name)
            else:
                logger.error(\
                    "The AMB channel details are not mentioned. Kindly check up your setup.")
            amb.mb_close()
        except Exception as error:
            logger.error("Exception while connecting to AMB. Error: <%s>"%str(error))
    else:
        logger.error("The AMB details are not mentioned. Kindly check up your setup.")
    return channel_exists

def checkAMBConnection(message_broker):
    """check if the given AMB details can be connected"""
    import amb
    is_amb_connected = False
    if message_broker:
        try:
            amb.mb_init(message_broker)
            amb.mb_close()
            is_amb_connected = True
        except Exception as error:
            logger.error("Exception while connecting to AMB. Error: <%s>"%str(error))
    else:
        logger.error("The AMB details are not mentioned. Kindly check up your setup.")
    return is_amb_connected

def checkMandatoryFParamaters(mandatory_fparameters):
    """checks of the given dictionary of FParameters are present in ADS with value"""
    fparameter_list = []
    fparameters_dict = {}
    fparameters_present = True
    for each_list in list(mandatory_fparameters.values()):
        fparameter_list.extend(each_list)
    for module in mandatory_fparameters:
        for fparameter in mandatory_fparameters[module]:
            fparameters_dict = get_all_mandatory_fparameters(fparameter, module, fparameters_dict)
    for each_fparameter in fparameter_list:
        if each_fparameter in list(fparameters_dict.keys()):
            fparameter_value = fparameters_dict[each_fparameter]
            if (not fparameter_value) or str(fparameter_value).upper() == 'NONE':
                logger.error("FParameter <%s>'s value is mandatory and it is not set in ADS."%\
                                each_fparameter)
                fparameters_present = False
            else:
                logger.debug("FParameter------", each_fparameter)
        else:
            logger.error("FParameter <%s> is mandatory and is not present in ADS."%\
                            each_fparameter)
    return fparameters_present

def checkRegulatoryAPIExists(acm_object, attr_list):
    """check for the presense of the pre-requistes in the ADS required for\
     the functioning for the RegulatorySupport"""
    acm_object_type = None
    reg_info = None
    regulatory_apis_exist = True
    try:
        if acm_object.IsKindOf(acm.FTrade):
            acm_object_type = 'Trade'
        elif acm_object.IsKindOf(acm.FInstrument):
            acm_object_type = 'Instrument'
        elif acm_object.IsKindOf(acm.FContact):
            acm_object_type = 'Contact'
        elif acm_object.IsKindOf(acm.FParty):
            acm_object_type = 'Party'
        elif acm_object.IsKindOf(acm.FPerson):
            acm_object_type = 'Person'
    except:
        pass
    try:
        reg_info = acm_object.RegulatoryInfo()
    except:
        logger.error("RegulatoryInfo instance on the %s is not accessible. Import\
        the RegulatorySupport package for expected functionality."%acm_object_type)
        regulatory_apis_exist = False
    if reg_info:
        for each_api in attr_list:
            try:
                eval('reg_info.' + each_api + '()')
            except:
                logger.error("API <%s> is not found on %s.RegulatoryInfo"%(\
                                each_api, acm_object_type))
                regulatory_apis_exist = False
    return regulatory_apis_exist

