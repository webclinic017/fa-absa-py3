""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendRecordLookup.py"

import acm
import copy
import traceback
import pprint

pp = pprint.PrettyPrinter(indent=4)
from FParameterSettings import ParameterSettingsCreator
from FSecLendUtils import fn_timer
from FSecLendUtils import logger
import collections

# ----------------------------------------------------------------------------------------------
#  Lookup SearchCombo. This can be used by Party and Instruments.

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendRecordLookupSettings')


class SearchControl(object):
    """
    name: Diplay name of the control
    LookupObj: The class that is used for the lookup
    lookupIdsList: the list of ids one wants to use for the lookup
    """

    @fn_timer
    def __init__(self, name,
                 ObjLookup,
                 lookupIdsList,
                 tooltip=None,
                 width=30,
                 maxwidth=30,
                 displayAllIds=False):
        self.m_name = name
        self.m_label = None
        self.m_control = None
        self.search_items = acm.FDictionary()
        self.control_items = acm.FArray()
        self.m_width = width
        self.m_maxwidth = maxwidth
        self.m_populateEnabled = True
        self.m_displayAllIds = displayAllIds
        _lookupIdsList = list(lookupIdsList)
        self.m_objectlookup = ObjLookup(_lookupIdsList)
        self.m_tooltip = tooltip if tooltip else "object ids listed: {}".format(
            ", ".join(['Name'] + self.m_objectlookup.lookup_ids))
        self.m_objectlookup.AreAttributesValid(_lookupIdsList)

    def GetData(self):
        if self.m_displayAllIds:
            return self.m_control.GetData().split(':')[0].strip()
        else:
            return self.m_control.GetData()

    def DisplayAllIDs(self):
        return self.m_displayAllIds

    def SetData(self, data):
        return self.m_control.SetData(data)

    def Clear(self):
        self.m_control.SetData("")

    def IsValidData(self):
        """
        Validate data that is pasted into the control(not selected)
        When the user copy pastes an instrument ID without typing it. It should be validated
        """
        if self.GetData():
            user_selection = self.m_control.GetData().upper()
            return any(user_selection == obj.upper() or self.GetData() in self.search_items.At(obj)
                                                                for obj in self.search_items.Keys())
        return False

    def PopulateControl(self):
        if self.m_displayAllIds:
            for obj in self.m_objectlookup.DisplayItems():
                lookupIds = ' : '.join(str(e) for e in self.m_objectlookup.ObjectLookupIds(obj))
                item = obj + (" : " + lookupIds if lookupIds else "")
                self.control_items.Add(item)
                self.search_items.AtPut(item, frozenset(self.m_objectlookup.ObjectLookupIds(obj)))
        else:
            self.control_items.AddAll(self.m_objectlookup.DisplayItems())
            for obj in self.control_items:
                self.search_items.AtPut(obj, frozenset(self.m_objectlookup.ObjectLookupIds(obj)))
        self.m_control.Populate(self.control_items)

    def BuildLayoutPart(self, builder, label):
        builder.AddInput(self.m_name, label, self.m_width, self.m_maxwidth)

    def HandleCreate(self, layout):
        self.m_control = layout.GetControl(self.m_name)
        self.m_control.FilterAutoComplete(False)
        self.AddCallback('UserTyped')
        self.m_control.ToolTip(self.m_tooltip)

    def AddCallback(self, callbackType, callback=None, arg=None):
        if not callback and callbackType == 'UserTyped':
                callback = self.OnControlTyping
        self.m_control.AddCallback(callbackType, callback, None)

    def OnControlTyping(self, *args):
        user_entry = self.m_control.GetData()
        if user_entry:
            user_entry = user_entry.upper()
            temp = []
            for item in self.control_items:
                if user_entry in item.upper() or \
                        any(filter(lambda lookup_id: user_entry in lookup_id, self.search_items.At(item))):
                    temp.append(item)
            self.m_control.Populate(temp)
        else:
            self.m_control.Populate(self.control_items)


class ObjectlookupProxy(object):

    @fn_timer
    def __init__(self, settings_lookup_ids):
        self.lookup_ids = []
        self.validated_lookup_ids = []
        self.m_addinfos = {}
        self.m_aliases = {}
        self.m_attributes = collections.OrderedDict()
        self.SetValidLookUpIds(settings_lookup_ids)
        self.LookupIds(copy.deepcopy(self.validated_lookup_ids))

    def SetValidLookUpIds(self, settings_lookup_ids):
        pass

    def LookupIds(self, lookup_ids=None):
        if lookup_ids:
            self.lookup_ids = lookup_ids
        return self.lookup_ids

    def AreAttributesValid(self, settings_lookup_ids):
        res = len(settings_lookup_ids) == len(self.LookupIds())
        if not res:
            logger.info('Not All attributes are valid. Only the following list is {}'.format(self.lookup_ids))
        return res

    @staticmethod
    def isAddInfo(attr):
        return "AdditionalInfo:" in attr

    @staticmethod
    def isAlias(attr):
        return "Aliases.Type.AliasTypeName:" in attr

    def isAttribute(self, acmObj, attributes):
        if ":" not in attributes:  # not alias and not addinfo
            attr = attributes.split(".", 1)
            if len(attr) == 2:
                try:
                    return self.isAttribute(acmObj.GetMethod(attr[0], 0).ValueDomain(), attr[1])
                except Exception as e:
                    logger.info('isAttribute: error {} {}'.format(e, attr))
                    return False
            else:
                return acmObj.GetMethod(attr[0], 0) is not None

    def GetAttributeValue(self, acmObj, attributes):
        attr = attributes.split(".", 1)
        if len(attr) == 2:
            try:
                return self.GetAttributeValue(getattr(acmObj, attr[0])(), attr[1])
            except Exception as e:
                logger.info('isAttribute: error {} {}'.format(e, attr))
                return False
        else:
            return getattr(acmObj, attr[0])()

    def DisplayItems(self):
        """items to be set in the box and diplayed in the user control"""
        return self.m_attributes.keys()

    def ObjectLookupIds(self, ins_name):
        """ the lookup ids list for each instrument
        this is a dicionnary of instrument names and
        their correspondant list of ids that can be used
        """
        a = set(self.m_attributes.get(ins_name, []))
        b = set(self.m_addinfos.get(ins_name, []))
        c = set(self.m_aliases.get(ins_name, []))
        return a | b | c


class InstrumentLookup(ObjectlookupProxy):
    """This class is used to implement the lookup for FUXControls like combobox."""

    _records = None

    def __init__(self, settings_lookup_ids):
        super(InstrumentLookup, self).__init__(settings_lookup_ids)
        self.SetAttributes()
        self.SetAddInfos()
        self.SetAliases()

    def SetValidLookUpIds(self, settings_lookup_ids):
        """Filter unvalid lookup ids set by the user"""
        aliases_types = [alias.Name() for alias in acm.FInstrAliasType.Select('')]
        addinfos_types = [addinfo.Name() for addinfo in acm.FAdditionalInfoSpec.Select("recType='Instrument'")]

        for id in settings_lookup_ids:
            if id in aliases_types:
                self.validated_lookup_ids.append("Aliases.Type.AliasTypeName:" + id)
            elif id in addinfos_types:
                self.validated_lookup_ids.append("AdditionalInfo:" + id)
            elif self.isAttribute(acm.FInstrument, id):
                self.validated_lookup_ids.append(id)
            else:
                logger.error('Instrument Lookup Id "{}" not valid'.format(id))

    def SetAddInfos(self):
        # caches securities AddInfos values. Expl:{"BMW":["BmwAddInfoID_ISINValue"..]}
        query = acm.CreateFASQLQuery(acm.FAdditionalInfo, 'AND')
        query.AddAttrNode('AddInf.RecType', 'EQUAL', 'Instrument')
        op = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAddInfo(attr):
                op.AddAttrNode('AddInf.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True
        if at_least_one:
            for addinfo in query.Select():
                ins_name = addinfo.Parent().Name()
                if ins_name not in self.m_addinfos:
                    self.m_addinfos.setdefault(ins_name, [addinfo.FieldValue().upper()])
                else:
                    self.m_addinfos[ins_name].append(addinfo.FieldValue().upper())

    def SetAliases(self):
        # caches securities aliases values. Expl:{"BMW":["BmwAliasSedolValue"..]}
        query = acm.CreateFASQLQuery(acm.FInstrumentAlias, 'AND')
        ins = query.AddOpNode('OR')
        for it in self.m_attributes:
            ins.AddAttrNode('Instrument.Name', 'EQUAL', it)  # Strip
        type = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAlias(attr):
                type.AddAttrNode('Type.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True
        if at_least_one:  # at least one alias in the list should have been found in the ADS
            l = query.Select()
            for alias in l:
                ins_name = alias.Instrument().Name()
                if ins_name not in self.m_aliases:
                    self.m_aliases.setdefault(ins_name, [alias.Alias().upper()])
                else:
                    self.m_aliases[ins_name].append(alias.Alias().upper())

    def SetAttributes(self):
        # store instrument attributes values. Expl:{"BMW":["BmwIsinValue","BMWNameValue"..]}
        for attr in self.validated_lookup_ids[:]:
            if self.isAttribute(acm.FInstrument, attr):
                for instrument in self.getRecords():
                    id = self.GetAttributeValue(instrument, attr)
                    if id:
                        id = id.upper()
                        if instrument.Name() not in self.m_attributes:
                            self.m_attributes.setdefault(instrument.Name(), [id])
                        else:
                            self.m_attributes[instrument.Name()].append(id)
                    else:
                        if instrument.Name() not in self.m_attributes:
                            self.m_attributes.setdefault(instrument.Name(), [])

                self.validated_lookup_ids.remove(attr)

        if not self.m_attributes:  # if no attributes in the lookup list, fill in the instrument names at least
            for instrument in self.getRecords():
                self.m_attributes.setdefault(instrument.Name(), [])

    @classmethod
    def getRecords(cls):
        if not cls._records or bool(_SETTINGS.Reload()):
            query = acm.CreateFASQLQuery(acm.FSecurityLoan, 'AND')
            query.AddAttrNode('ProductTypeChlItem.Name', 'EQUAL', 'Master Security Loan')
            acm.FStock.Select('').First()  # It's quicker to first select all stocks and then ask for them as Underlying
            cls._records = sorted([ins.Underlying() for ins in query.Select()])
        return cls._records


class FInstrumentLookup(InstrumentLookup):
    """
    This class is used for the clipboard lookup
    or file upload lookup or any script that wants to lookup for instruments
    """

    def __init__(self, settings_lookup_ids):
        self.all_ids = {}  # faster
        super(FInstrumentLookup, self).__init__(settings_lookup_ids)

    def SetValidLookUpIds(self, settings_lookup_ids):
        super(FInstrumentLookup, self).SetValidLookUpIds(settings_lookup_ids)
        if 'Name' not in self.validated_lookup_ids:
            self.validated_lookup_ids.append('Name')

    def SetAddInfos(self):
        # caches security AddInfos {"addinfotype":{"addinfoValue":"Security"}}
        query = acm.CreateFASQLQuery(acm.FAdditionalInfo, 'AND')
        query.AddAttrNode('AddInf.RecType', 'EQUAL', 'Instrument')
        op = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAddInfo(attr):
                op.AddAttrNode('AddInf.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True

        if at_least_one:
            for addinfo in query.Select():
                addinfotype = "AdditionalInfo:" + addinfo.AddInf().Name()
                if addinfotype not in self.all_ids:
                    self.all_ids.setdefault(addinfotype, {addinfo.FieldValue(): [addinfo.Parent()]})
                else:
                    if addinfo.FieldValue() not in self.all_ids[addinfotype]:
                        self.all_ids[addinfotype].setdefault(addinfo.FieldValue(), [addinfo.Parent()])
                    else:
                        self.all_ids[addinfotype][addinfo.FieldValue()].append(addinfo.Parent())

    def SetAliases(self):
        # caches security aliases {"AliasType":{"AliasValue":"Security"}}
        query = acm.CreateFASQLQuery(acm.FInstrumentAlias, 'AND')
        ins = query.AddOpNode('OR')
        for it in self.getRecords():
            ins.AddAttrNode('Instrument.Name', 'EQUAL', it.Name())
        type = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAlias(attr):
                type.AddAttrNode('Type.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True

        if at_least_one:
            for alias in query.Select():
                alias_type = "Aliases.Type.AliasTypeName:" + alias.Type().Name()
                if alias_type not in self.all_ids:
                    self.all_ids.setdefault(alias_type, {alias.Alias(): [alias.Instrument()]})
                else:
                    if alias.Alias() not in self.all_ids[alias_type]:
                        self.all_ids[alias_type].setdefault(alias.Alias(), [alias.Instrument()])
                    else:
                        self.all_ids[alias_type][alias.Alias()].append(alias.Instrument())

    def SetAttributes(self):
        # caches security attributes {"AttributeName":{"AttributeValue":"Security"}}
        for attr in self.validated_lookup_ids[:]:
            if self.isAttribute(acm.FInstrument, attr):
                for instrument in self.getRecords():
                    id = self.GetAttributeValue(instrument, attr)
                    if id:
                        if attr not in self.all_ids:
                            self.all_ids.setdefault(attr, {id: [instrument]})
                        else:
                            if id not in self.all_ids[attr]:
                                self.all_ids[attr].setdefault(id, [instrument])
                            else:
                                self.all_ids[attr][id].append(instrument)
                    else:
                        if attr not in self.all_ids:
                            self.all_ids.setdefault(attr, {})
                self.validated_lookup_ids.remove(attr)

    def __call__(self, lookup_list):
        """
            looks for an object using an incremental list of items from the lookup_list
            if item N doesnt give a hit, remove it and proceed with N+1
            if item N gives more then one hit, narrow down the result using N+1
            if item N gives one hit, return the result and break.
            pp.pprint(self.all_ids)

            Can be used this way:
            FInstrument = FInstrumentLookup(['ID_ISIN','SEDOL','Currency.Name'])
            print FInstrument(['SE0000108656', '0010865XX','SEK'])
            -> should give Ericsson A as two ID_ISIN exists in the
            database SE0000108656, no sedol=0010865XX and one SEK matching Ericsson A
        """

        def getRecord(lookup_ids, lookup_list):
            records = self.all_ids.get(lookup_ids[0], []).get(lookup_list[0], [])
            if len(records) == 1:
                logger.debug("Look-up found element:{}".format(records[0].Name()))
                return records
            elif len(records) > 1:
                logger.debug("{} elements found with id {}={}.\nLook up list left:{}\nList ids left:{}\n".format(
                    len(records), lookup_ids[0], lookup_list[0], lookup_list, lookup_ids))
                if len(lookup_ids) > 1:
                    inter = records
                    sublist = getRecord(lookup_ids[1:], lookup_list[1:])
                    if len(sublist) > 0:
                        inter = list(set(records) & set(sublist))
                    return inter
                else:
                    return records
            else:
                logger.debug(
                    "FInstrumentLookup: No element found with id {}={}.\nLook up list left:{}\nList ids left:{}\n".format(
                        lookup_ids[0], lookup_list[0], lookup_ids, lookup_list))
                if len(lookup_ids) > 1:
                    return getRecord(lookup_ids[1:], lookup_list[1:])
                else:
                    return []

        try:
            result = getRecord(self.LookupIds(), lookup_list)
            return result
        except Exception:
            logger.debug("IncrementalLookup error:{}".format(traceback.format_exc()))
            return None


class PartyLookup(ObjectlookupProxy):
    """
    This class is used to implement the lookup for FUXControls like combobox.
    It is used to control the typing of the user letter by letter and return back the potential matches
    The next class, FPartyLookup is used to match an exact ID coming from a file for example, if it's different then
    the exact match of that ID then it wont return it.
    """

    _records = None

    def __init__(self, settings_lookup_ids):
        super(PartyLookup, self).__init__(settings_lookup_ids)
        self.SetAttributes()
        self.SetAddInfos()
        self.SetAliases()

    def SetValidLookUpIds(self, settings_lookup_ids):
        """Filter unvalid lookup ids set by the user"""
        aliases_types = [alias.Name() for alias in acm.FPartyAliasType.Select('')]
        addinfos_types = [addinfo.Name() for addinfo in acm.FAdditionalInfoSpec.Select("recType='Party'")]

        for id in settings_lookup_ids:
            if id in aliases_types:
                self.validated_lookup_ids.append("Aliases.Type.AliasTypeName:" + id)
            elif id in addinfos_types:
                self.validated_lookup_ids.append("AdditionalInfo:" + id)
            elif self.isAttribute(acm.FParty, id):
                self.validated_lookup_ids.append(id)
            else:
                logger.error('Party Lookup Id "{}" not valid'.format(id))

    def SetAddInfos(self):
        # caches securities AddInfos values. Expl:{"BMW":["BmwAddInfoID_ISINValue"..]}
        query = acm.CreateFASQLQuery(acm.FAdditionalInfo, 'AND')
        query.AddAttrNode('AddInf.RecType', 'EQUAL', 'Party')
        op = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAddInfo(attr):
                op.AddAttrNode('AddInf.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True
        if at_least_one:
            for addinfo in query.Select():
                name = addinfo.Parent().Name()
                if name not in self.m_addinfos:
                    self.m_addinfos.setdefault(name, [addinfo.FieldValue().upper()])
                else:
                    self.m_addinfos[name].append(addinfo.FieldValue().upper())

    def SetAliases(self):
        # caches securities aliases values. Expl:{"BMW":["BmwAliasSedolValue"..]}
        query = acm.CreateFASQLQuery(acm.FPartyAlias, 'AND')
        party = query.AddOpNode('OR')
        for it in self.m_attributes:
            party.AddAttrNode('Party.Name', 'EQUAL', it)  # Strip
        type = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAlias(attr):
                type.AddAttrNode('Type.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True
        if at_least_one:  # at least one alias in the list should have been found in the ADS
            l = query.Select()
            for alias in l:
                name = alias.Party().Name()
                if name not in self.m_aliases:
                    self.m_aliases.setdefault(name, [alias.Alias().upper()])
                else:
                    self.m_aliases[name].append(alias.Alias().upper())

    def SetAttributes(self):
        # store party attributes values.
        for attr in self.validated_lookup_ids[:]:
            if self.isAttribute(acm.FParty, attr):
                for party in self.getRecords():
                    id = self.GetAttributeValue(party, attr)
                    if id:
                        id = id.upper()
                        if party.Name() not in self.m_attributes:
                            self.m_attributes.setdefault(party.Name(), [id])
                        else:
                            self.m_attributes[party.Name()].append(id)
                    else:
                        if party.Name() not in self.m_attributes:
                            self.m_attributes.setdefault(party.Name(), [])
                self.validated_lookup_ids.remove(attr)

        if not self.m_attributes:  # if no attributes in the lookup list, fill in the instrument names at least
            for party in self.getRecords():
                self.m_attributes.setdefault(party.Name(), [])

    @classmethod
    def getRecords(cls):
        if not cls._records or bool(_SETTINGS.Reload()):
            query = acm.CreateFASQLQuery(acm.FParty, 'OR')
            query.AddAttrNode('Type', 'EQUAL', "CounterParty")
            query.AddAttrNode('Type', 'EQUAL', "Client")
            acm.FParty.Select('').First()  # It's quicker to first select all stocks and then ask for them as Underlying
            cls._records = sorted(query.Select())
        return cls._records


class FPartyLookup(PartyLookup):

    def __init__(self, settings_lookup_ids):
        self.all_ids = {}
        super(FPartyLookup, self).__init__(settings_lookup_ids)

    def SetValidLookUpIds(self, settings_lookup_ids):
        super(FPartyLookup, self).SetValidLookUpIds(settings_lookup_ids)
        if 'Name' not in self.validated_lookup_ids:
            self.validated_lookup_ids.append('Name')

    def SetAliases(self):
        query = acm.CreateFASQLQuery(acm.FPartyAlias, 'AND')
        type = query.AddOpNode('OR')
        type.AddAttrNode('Party.Type', 'EQUAL', "CounterParty")
        type = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAlias(attr):
                type.AddAttrNode('Type.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True

        if at_least_one:
            for alias in query.Select():
                alias_type = "Aliases.Type.AliasTypeName:" + alias.Type().Name()
                if alias_type not in self.all_ids:
                    self.all_ids.setdefault(alias_type, {alias.Alias(): [alias.Party()]})
                else:
                    if alias.Alias() not in self.all_ids[alias_type]:
                        self.all_ids[alias_type].setdefault(alias.Alias(), [alias.Party()])
                    else:
                        self.all_ids[alias_type][alias.Alias()].append(alias.Party())

    def SetAddInfos(self):
        # caches security AddInfos {"addinfotype":{"addinfoValue":"Security"}}
        query = acm.CreateFASQLQuery(acm.FAdditionalInfo, 'AND')
        query.AddAttrNode('AddInf.RecType', 'EQUAL', 'Party')
        op = query.AddOpNode('OR')
        at_least_one = False
        for attr in self.validated_lookup_ids[:]:
            if self.isAddInfo(attr):
                op.AddAttrNode('AddInf.Name', 'EQUAL', attr.split(":")[1])
                self.validated_lookup_ids.remove(attr)
                at_least_one = True

        if at_least_one:
            for addinfo in query.Select():
                addinfotype = "AdditionalInfo:" + addinfo.AddInf().Name()
                if addinfotype not in self.all_ids:
                    self.all_ids.setdefault(addinfotype, {addinfo.FieldValue(): [addinfo.Parent()]})
                else:
                    if addinfo.FieldValue() not in self.all_ids[addinfotype]:
                        self.all_ids[addinfotype].setdefault(addinfo.FieldValue(), [addinfo.Parent()])
                    else:
                        self.all_ids[addinfotype][addinfo.FieldValue()].append(addinfo.Parent())

    def SetAttributes(self):
        for attr in self.validated_lookup_ids[:]:
            if self.isAttribute(acm.FParty, attr):
                for party in self.getRecords():
                    id = self.GetAttributeValue(party, attr)
                    if id:
                        if attr not in self.all_ids:
                            self.all_ids.setdefault(attr, {id: [party]})
                        else:
                            if id not in self.all_ids[attr]:
                                self.all_ids[attr].setdefault(id, [party])
                            else:
                                self.all_ids[attr][id].append(party)
                    else:
                        if attr not in self.all_ids:
                            self.all_ids.setdefault(attr, {})
                self.validated_lookup_ids.remove(attr)

    def __call__(self, lookup_list):
        """
            looks for an object using an incremental list of items from the lookup_list
            if item N doesnt give a hit, remove it and proceed with N+1
            if item N gives more then one hit, narrow down the result using N+1
            if item N gives one hit, return the result and break.
            pp.pprint(self.all_ids)

            Can be used this way:
            FParty = FPartyLookup(["Telephone", "BIC", "Id"])
            print FParty(["0768692360", "UBS", "11111111110004"])
        """

        def getRecord(lookup_ids, lookup_list):
            records = self.all_ids.get(lookup_ids[0], []).get(lookup_list[0], [])
            if len(records) == 1:
                logger.debug("Look-up found element:{}".format(records[0]))
                return records
            elif len(records) > 1:
                logger.debug("{} elements found with id {}={}.\nLook up list left:{}\nList ids left:{}\n".format(
                    len(records), lookup_ids[0], lookup_list[0], lookup_list, lookup_ids))
                if len(lookup_ids) > 1:
                    inter = records
                    sublist = getRecord(lookup_ids[1:], lookup_list[1:])
                    if len(sublist) > 0:
                        inter = list(set(records) & set(sublist))
                    return inter
                else:
                    return records
            else:
                logger.debug(
                    "FPartyLookup:No element found with id {}={}.\nLook up list left:{}\nList ids left:{}\n".format(
                        lookup_ids[0], lookup_list[0], lookup_ids, lookup_list))
                if len(lookup_ids) > 1:
                    return getRecord(lookup_ids[1:], lookup_list[1:])
                else:
                    return []

        try:
            result = getRecord(self.LookupIds(), lookup_list)
            return result
        except Exception:
            logger.debug("IncrementalLookup error:{}".format(traceback.format_exc()))
            return None
