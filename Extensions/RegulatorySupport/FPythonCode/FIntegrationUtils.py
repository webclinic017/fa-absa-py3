import sys
import string
import os
import re, base64
try:
    import acm
except:
    pass

try:
    import ael
except :
    pass

class FIntegrationUtils(object):
    def get_contacts(self, party):
        """get the contacts that are available on the party"""
        contacts = set()
        for contact in party.Contacts():
            contacts.add(contact.Fullname())
        return list(contacts)

    def get_party_handle(self, party_val):
        """get the actual party object from the given input - either string or party obj"""
        party_handle = None
        try:
            if isinstance(party_val, str):
                party_handle = acm.FParty[party_val]
            elif party_val.IsKindOf(acm.FParty):
                party_handle = party_val
        except Exception as e:
            # this exception is hit when the IsKindOf is called on a None party object that is being sent
            pass
        return party_handle

    def get_instrument_handle(self, ins_val):
        """get the actual instrument object from the given input - either string or instrument obj"""
        instrument_handle = None
        try:
            if isinstance(ins_val, str):
                instrument_handle = acm.FInstrument[ins_val]
            elif ins_val.IsKindOf(acm.FInstrument):
                instrument_handle = ins_val
        except Exception as e:
            # this exception is hit when the IsKindOf is called on a None instrument object that is being sent
            pass
        return instrument_handle

    def is_valid_choice_list_val(self, choice_list, choice_list_val):
        """validate that the given value is an entry for the given choicelist"""
        is_valid_choice_list = False
        choicelists = acm.FChoiceList.Select("list = '%s' and name = '%s'" % (choice_list, choice_list_val))
        if choicelists:
            is_valid_choice_list = True
        return is_valid_choice_list

    def get_choice_list(self, choice_list, choice_list_val):
        """get the choicelist object from the given query"""
        choicelist_val = None
        choicelists = acm.FChoiceList.Select("list = '%s' and name = '%s'" % (choice_list, choice_list_val))
        if choicelists:
            choicelist_val = choicelists[0]
        return choicelist_val

    def get_valid_contact(self, party, contact):
        """validate if the given contact exists on the give party"""
        valid_contact = None
        contact_name = None
        try:
            if contact.IsKindOf(acm.FContact):
                contact_name = contact.Fullname()
        except:
            contact_name = contact
        for contactVal in party.Contacts():
            if contactVal.Fullname() == contact_name:
                valid_contact = contactVal
                break
        return valid_contact

    def create_additional_info_spec(self, add_info_spec_attr):
        """ Create additional info's"""
        ais = acm.FAdditionalInfoSpec[add_info_spec_attr['FieldName']]
        if ais:
            raise AddInfoSpecAlreadyExits("Additional info <%s> exists on table <%s>" % (
            add_info_spec_attr['FieldName'], add_info_spec_attr['Table']))
        ais = acm.FAdditionalInfoSpec()
        self.set_additional_info_spec_attr(ais, add_info_spec_attr)

    def set_additional_info_spec(self, add_info_spec_attr, filter=None):
        """set the additionalInfoSpec attributes"""
        ais = acm.FAdditionalInfoSpec[add_info_spec_attr['FieldName']]
        if not ais:
            ais = acm.FAdditionalInfoSpec()
        self.set_additional_info_spec_attr(ais, add_info_spec_attr, filter)

    def get_additional_info_spec(self, add_info, rec_addr):
        """get the additionalinfo instance on the given acm object for a given addInfoSpec"""
        add_info_obj = None
        add_info_spec = acm.FAdditionalInfoSpec[add_info]
        if add_info_spec:
            try:
                add_info_objs = acm.FAdditionalInfo.Select(
                    'addInf=%d and recaddr =%d' % (add_info_spec.Oid(), rec_addr.Oid()))
                if add_info_objs:
                    add_info_obj = add_info_objs[0]
            except Exception as e:
                raise Exception('Error while accessing additional info %s' % (add_info))

        else:
            raise AddInfoSpecNotExist('%s is not a valid AdditionalInfoSpec' % (add_info))
        return add_info_obj

    def get_alias_type(self, alias_typ):
        """get the alias type instance on the given acm object for a given alias type name"""
        alias_typ_spec = None
        alias_typ_spec = acm.FInstrAliasType[alias_typ]
        if not alias_typ_spec:
            raise AliasTypeSpecNotExist('%s is not a valid AliasType'%(alias_typ))
        return alias_typ_spec

    def get_alias_val(self, alias_typ, rec_addr):
        """get the alias value instance on the given acm object for a given alias type name"""
        alias_val = None
        alias_typ_obj = self.get_alias_type(alias_typ)
        if alias_typ_obj:
            try:
                alias_obj = acm.FInstrumentAlias.Select01('type=%d and instrument =%d'%(alias_typ_obj.Oid(), rec_addr.Oid()), 'Not found')
                if alias_obj:
                    alias_val = alias_obj.Alias()

            except Exception as e:
                raise Exception('Error while accessing %s Alias for %s : %s'%(alias_typ, str(rec_addr.Name()), str(e)))

        return alias_val

    def get_isda_index_tenor_alias_val(self, rec_addr):
        """get the ISDAIndexTenor alias value for the acm FInstrument object"""
        alias_typ_name = 'ISDAIndexTenor'
        alias_typ_obj = None
        alias_val = None
        reg = '\d{1,2}[M|Y|D]{1}'
        alias_typ_spec = acm.FInstrAliasType[alias_typ_name]
        if alias_typ_spec:
            try:
                alias_typ_obj = acm.FInstrumentAlias.Select01('type=%d and instrument =%d'%(alias_typ_spec.Oid(), rec_addr.Oid()), 'Not found')
                if alias_typ_obj:
                    alias = alias_typ_obj.Alias()
                    alias_val = alias
                    if alias.find('-') != -1:
                        split_text = alias.split('-')
                        data_to_strip = split_text[-1]
                        pattern = re.compile(reg)
                        if pattern.match(data_to_strip):
                            alias_val = '-'.join(split_text[:-1])
            except Exception as e:
                raise Exception('Error while accessing Alias %s : %s'%(alias_typ_name, str(e)))

        else:
            raise AliasTypeSpecNotExist('%s is not a valid AliasType'%(alias_typ_name))
        return alias_val

    def get_isda_index_tenor_addinfo_val(self, rec_addr):
        """get the ISDAIndexTenor AddInfo value for the acm FInstrument object"""
        addinfo_spec_name = 'ISDAIndexTenor'
        addinfo_spec_obj = None
        addinfo_val = None
        reg = '\d{1,2}[M|Y|D]{1}'
        addinfo_spec = acm.FAdditionalInfoSpec[addinfo_spec_name]
        if addinfo_spec:
            try:
                addinfo_spec_obj = acm.FAdditionalInfo.Select01('addInf=%d and recaddr =%d'%(addinfo_spec.Oid(), rec_addr.Oid()), 'Not found')
                if addinfo_spec_obj:
                    addinfo = addinfo_spec_obj.FieldValue()
                    addinfo_val = addinfo
                    if addinfo.find('-') != -1:
                        split_text = addinfo.split('-')
                        data_to_strip = '-' + split_text[-1]
                        pattern = re.compile(reg)
                        if pattern.match(data_to_strip):
                            alias_val = '-'.join(split_text[:-1])
            except Exception as e:
                raise Exception('Error while accessing AdditionalInfo %s : %s'%(addinfo_spec_name, str(e)))

        else:
            raise AdditionalInfoSpecNotExist('%s is not a valid AdditionalInfoSpec'%(addinfo_spec_name))
        return addinfo_val

    def get_isda_index_tenor(self, rec_addr):
        index_tenor_val = ''
        exception_str = ''
        try:
            index_tenor_val = self.get_isda_index_tenor_alias_val(rec_addr)
        except Exception as e:
            exception_str += str(e)

        if not index_tenor_val:
            try:
                index_tenor_val = self.get_isda_index_tenor_addinfo_val(rec_addr)
            except Exception as e:
                exception_str += '\n' + str(e)
        if exception_str:
            raise Exception(exception_str)
        return index_tenor_val

    def get_data_type_type(self, type_val):
        """get the DataTypeType to be set on the AddInfoSpec while creating it"""
        date_type_type = None
        try:
            if type_val in acm.FEnumeration['enum(B92StandardType)'].Choices():
                date_type_type = acm.FEnumeration['enum(B92StandardType)'].Enumeration(type_val)
            elif type_val in acm.FEnumeration['enum(B92RecordType)'].Choices():
                date_type_type = acm.FEnumeration['enum(B92RecordType)'].Enumeration(type_val)
        except:
            if type_val in acm.FEnumeration['enum(B92StandardType)'].Elements():
                date_type_type = acm.FEnumeration['enum(B92StandardType)'].Enumeration(type_val)
            elif type_val in acm.FEnumeration['enum(B92RecordType)'].Elements():
                date_type_type = acm.FEnumeration['enum(B92RecordType)'].Enumeration(type_val)
        return date_type_type

    def set_additional_info_spec_attr(self, ais, add_info_spec_attr, filter = None):
        """ Set additional info spec attributes"""
        try:
            ais.FieldName(add_info_spec_attr['FieldName'])
            ais.Description(add_info_spec_attr['Description'])

            ais.DefaultValue(add_info_spec_attr['Default'])

            ais.DataTypeGroup = acm.FEnumeration['enum(B92DataGroup)'].Enumeration(add_info_spec_attr['TypeGroup'])
            ais.DataTypeType(self.get_data_type_type(add_info_spec_attr['Type']))


            ais.RecType = add_info_spec_attr['Table']

            if add_info_spec_attr['Type'] == 'ChoiceList':
                choiceListValues = []
                if 'Values' in add_info_spec_attr.keys():
                    choiceListValues = add_info_spec_attr['Values']
                try:
                    self.create_choice_list(add_info_spec_attr['Description'], choiceListValues,
                                            add_info_spec_attr['Description'])
                except ChoiceListAlreadyExist as e:
                    pass
            if filter:
                for each_sub_table in filter:
                    try:
                        ais.AddSubType(each_sub_table)
                    except:
                        # it means this subType does not exist for this PRIME version. No point in raising exception here as this insType is not available on this acm Version.
                        pass
            ais.Commit()

        except Exception as e:
            raise Exception("Error occured while committing AddInfoSpec <%s>. Error: <%s>" % (
            add_info_spec_attr['FieldName'], str(e)))

    def update_element_in_choice_list(self, cl_name, cl_val, cl_val_description = None, cl_sort_order = None):
        """update the given element in the given choicelist with its description and sort order"""
        query = "list = '%s' and name ='%s'" %(cl_name, cl_val[0:39])
        cl_object = acm.FChoiceList.Select01(query, None)
        if cl_object:
            try:
                cl_object.List = cl_name
                cl_object.Name = cl_val
                if cl_val_description:
                    cl_object.Description(cl_val_description)
                if cl_sort_order:
                    cl_object.SortOrder(cl_sort_order)
                cl_object.Commit()
            except Exception as e:
                raise Exception("Error in update_element_in_choice_list", str(e))
        else:
            raise Exception("Either Choice list <%s> does not exist or it does not contain element <%s>"%(cl_name, cl_val))

    def insert_element_in_choice_list(self, cl_name, cl_val, cl_val_description = None, cl_sort_order = None):
        """insert the given element into the given choicelist with its description and sort order"""
        query = "list = '%s' and name ='%s'" %(cl_name, cl_val[0:39])
        cl_object = acm.FChoiceList.Select01(query, None)
        if not cl_object:
            cl_object = acm.FChoiceList()
        else:
            raise ChoiceListAlreadyExist("Choice list <%s> already contains element <%s>"%(cl_name, cl_val))
        try:
            cl_object.List = cl_name
            cl_object.Name = cl_val
            if cl_val_description:
                cl_object.Description(cl_val_description)
            if cl_sort_order:
                cl_object.SortOrder(cl_sort_order)
            cl_object.Commit()
        except Exception as e:
            raise Exception("Error in insert_element_in_choice_list", str(e))

    def remove_element_from_choice_list(self, cl_name, cl_val):
        """remove the given element from the given choicelist"""
        query = "list = '%s' and name ='%s'" % (cl_name, cl_val[0:39])
        cl_object = acm.FChoiceList.Select01(query, None)
        if cl_object:
            try:
                cl_object.Delete()
            except Exception as e:
                raise Exception("Error in remove_element_from_choice_list", str(e))
        else:
            raise ChoiceListNotFound("<%s> does not exist in <%s> ChoiceList" % (cl_val, cl_name))

    def delete_choice_list(self, cl_name):
        """delete the given choicelist"""
        cl_object = acm.FChoiceList[cl_name]
        if cl_object:
            cl_values = None
            try:
                cl_values = cl_object.Choices().AsList()
            except:
                cl_values = cl_object.Elements().AsList()
            for cl_val in cl_values:
                self.remove_element_from_choice_list(cl_name, cl_val.Name())
            self.remove_element_from_choice_list('MASTER', cl_name)

    def create_choice_list(self, cl_name, cl_values = [], description = None, bMaster = True, bUpdate = False):
        """create the choicelist with the given values"""
        cl_object = None
        choicelist_name = cl_name
        if bMaster:
            try:
                self.insert_element_in_choice_list('MASTER', cl_name, description)
            except ChoiceListAlreadyExist as e:
                if bUpdate:
                    self.update_element_in_choice_list('MASTER', cl_name, description)
        for cl_val in cl_values:
            cl_val_description = None
            cl_val_sort_order = None
            if 'description' in cl_val.keys():
                cl_val_description = cl_val['description']
            if 'sort_order' in cl_val.keys():
                cl_val_sort_order = cl_val['sort_order']
            if 'name' in cl_val.keys():
                choicelist_name = cl_val['name']
            try:
                self.insert_element_in_choice_list(cl_name, choicelist_name, cl_val_description, cl_val_sort_order)
            except ChoiceListAlreadyExist as e:
                if bUpdate:
                    self.update_element_in_choice_list(cl_name, choicelist_name, cl_val_description, cl_val_sort_order)
                else:
                    raise ChoiceListAlreadyExist(str(e))
        return cl_object

    def update_additional_info_spec(self, spec_name, add_info_spec_attr):
        """ Update additional info spec"""
        ais = acm.FAdditionalInfoSpec[spec_name]
        if ais:
            self.set_additional_info_spec(ais, add_info_spec_attr)

    def set_additional_info(self, add_info_spec, pObject, value):
        """set additional Info"""
        if getattr(pObject.AdditionalInfo(), add_info_spec, None) is None:
            raise AddInfoSpecNotExist("Additional info %s does not exist on %s" % (add_info_spec, pObject.ClassName()))
            return
        if self.get_acm_version() >= 2016.1:
            try:
                setattr(pObject.AdditionalInfo(), add_info_spec, value)
                pObject.Commit()
            except Exception as e:
                raise Exception(
                    "Error occurred during setting AddInfo %s with value %s. Error %s" % (add_info_spec, value, str(e)))
        else:
            ais = acm.FAdditionalInfoSpec[add_info_spec]
            if not ais:
                add_info_spec = add_info_spec[0].lower() + add_info_spec[1:]
                ais = acm.FAdditionalInfoSpec[add_info_spec]
            if ais:
                ai = None
                query = 'addInf=%d and recaddr=%d' % (ais.Oid(), pObject.Oid())
                ai_vals = acm.FAdditionalInfo.Select(query)
                for ai_val in ai_vals:
                    if ai_val.Oid() > 0:
                        ai = ai_val
                        break
                if ai:
                    self.update_addtional_info(ai, value)
                else:
                    self.create_additional_info(ais, pObject, value)

    def create_additional_info(self, ais, pObject, value):
        """create new additional Info"""
        try:
            if str(value) not in ['None',
                                  '']:  # added as this are considered valid values for 15.1 and it tries to apply these values and throws error
                ai = acm.FAdditionalInfo()
                ai.Recaddr = pObject.Oid()
                ai.AddInf = ais.Oid()
                ai.FieldValue(value)
                ai.Commit()
        except Exception as e:
            raise Exception(
                "Error occurred during adding AddInfo %s with value %s. Error %s" % (ais.Name(), value, str(e)))

    def delete_add_info_spec(self, add_info_spec):
        ais = acm.FAdditionalInfoSpec[add_info_spec]
        if ais:
            try:
                if ais.DataTypeGroup() =='RecordRef' and \
                    acm.EnumToString('B92RecordType', ais.DataTypeType()).AsString() == 'ChoiceList':
                    self.delete_choice_list(ais.Description())
                ais.Delete()

            except Exception as e:
                raise Exception("Error occured while deleting AddInfoSpec <%s>. Error: <%s>" % (add_info_spec, str(e)))
        else:
            raise AddInfoSpecNotExist("AddInfoSpec <%s> does not exist in database" % add_info_spec)

    def update_addtional_info(self, ai, value=None):
        """update the additional info"""
        try:
            if str(value) not in ['None',
                                  '']:  # added as this are considered valid values for 15.1 and it tries to apply these values and throws error
                aiC = ai.Clone()
                aiC.FieldValue(value)
                ai.Apply(aiC)
                ai.Commit()
            else:
                ai.Delete()
        except Exception as e:
            raise Exception(
                "Error occurred while updating AddInfo %s with value %s. Error %s" % (ai.AddInf().Name(), value, str(e)))

    def get_extension_contents(self, ext_type, ext_name):
        """ Get Extension contents for given type and name"""

        contents = ''
        ext_obj = acm.GetDefaultContext().GetExtension(ext_type, 'FObject', ext_name)
        if ext_obj:
            contents = ext_obj.Value()
        return contents

    '''def import_modules_from_string(self, modules):
        """ Import the modules from string"""
        imported_modules = []
        for module in modules:
            imp_module = None
            try:
                try:
                    import importlib
                    imp_module = importlib.import_module(module)
                except:
                    imp_module = __import__(module)
                imported_modules.append(imp_module)
            except Exception, error:
                self.notifier.ERROR(str(error))
        return imported_modules'''

    def import_modules_from_string(self, modules):
        """ Import the modules from string"""
        try:
            imported_modules = []
            for module in modules:
                imp_module = None
                imp_module = self.import_module_from_string(module)
                if imp_module:
                    imported_modules.append(imp_module)
            return imported_modules
        except Exception as e:
            raise Exception("Exception in import_modules_from_string : %s" % str(e))

    def import_module_from_string(self, module):
        """ Import the module from string"""
        imp_module = None
        try:
            import importlib
            imp_module = importlib.import_module(module)
        except:
            imp_module = __import__(module)
        return imp_module

    def get_doc_string_for_modules(self, ext_module):
        """ Get the doc string foe extension modules"""
        module_doc_strings = []
        try:
            ext_mod = acm.FExtensionModule[ext_module]
            if ext_mod:
                python_exts = ext_mod.GetAllExtensions('FPythonCode')
                module_names = python_exts.Transform('Name', acm.FArray, None)
                module_names = module_names.Transform('Text', acm.FArray, None)
                modules = self.import_modules_from_string(module_names)
                for module in modules:
                    module_doc_strings.append((module.__file__, module.__doc__))
        except Exception as error:
            raise Exception("Exception in get_doc_string_for_modules : %s" % str(error))
        return module_doc_strings

    def python_version(self):
        """ Return python version"""
        python_version = sys.version.split()[0]
        major, minor, micro = python_version.split('.')
        return str(major) + str(minor)

    def create_alias_type(self, alias_on, alias_description, alias_type_name, name):
        acmAlias = None
        if alias_on == 'Party':
            acmAlias = acm.FPartyAliasType.Select("name='%s'" % name)
            alias_on_val = 'Party'
        if alias_on == 'Instrument':
            acmAlias = acm.FInstrAliasType.Select("name='%s'" % name)
            alias_on_val = 'Instr'
        if not acmAlias:
            alias = eval("acm.F" + alias_on_val + "AliasType()")
            alias.AliasTypeDescription(alias_description)
            alias.AliasTypeName(alias_type_name)
            alias.Name(name)
            alias.Type(alias_on)
            alias.Commit()
        else:
            raise AliasTypeAlreadyExist("AliasType <%s> exists on table <%s>" % (alias_type_name, alias_on))

    def isBool(self, input_val):
        """check if the provided input is really a boolean value or not"""
        if isinstance(input_val, str):
            if input_val.upper() in ['FALSE', '0', 'NO']:
                input_val = False
            elif input_val.upper() in ['TRUE', '1', 'YES']:
                input_val = True
            else:
                input_val = None
        elif isinstance(input_val, int):
            if input_val == 0:
                input_val = False
            if input_val == 1:
                input_val = True
        return input_val

    def remove_choicelist_entry(self, choices,
                                choicelists):  # multiple choices can be removed from multiple choicelists.
        """delete the given choicelist entry"""
        for choicelist in choicelists:
            for choice in choices:
                self.remove_element_from_choice_list(choicelist, choice)

    @staticmethod
    def get_acm_version():
        """ Get the acm version"""
        version = None
        try:
            version = (float(".".join(acm.ShortVersion().strip(string.ascii_letters) .split(".")[0:2])))
        except:
            val = ".".join(acm.ShortVersion().strip(string.ascii_letters) .split(".")[0:2])
            version = (float(val.split('.')[0]))
        return version

    @staticmethod
    def get_acm_version_override():
        """ Override the acm version"""
        context = acm.GetDefaultContext()
        extn = "FIntegrationUtilsOverride"
        config_extension = context.GetExtension("FParameters", "FObject", extn)
        if config_extension:
            ver = config_extension.Value()['ACM_VERSION_OVERRIDE']
            ver = float(ver.Text())
        else:
            ver = FIntegrationUtils.get_acm_version()
        return ver

    def get_dates(self, date_string, instrument=None):
        # Convert yesterday to business day
        valid_date = None
        try:
            date_string_input = date_string.upper()
            if date_string_input == 'Y' or date_string_input == 'YESTERDAY':
                date_string = '-1d'
            try:
                valid_date = ael.date_from_string(date_string)
            except:
                try:
                    valid_date = self.ParseDateField(date_string, instrument)
                except:
                    date_parameter = date_string.upper()
                    if date_parameter.upper() == 'T' or date_parameter.upper() == 'TODAY' or \
                                    date_parameter == '':
                        valid_date = ael.date_today()
                    elif date_parameter.upper() == 'Y' or date_parameter.upper() == 'YESTERDAY':
                        valid_date = ael.date_today().add_days(-1)
                    else:
                        print("Please enter dates in formats supported" \
                              + " as mentioned in documentation")
        except Exception as error:
            print("Could not load module ael or incorrect date format.", str(error))

        return valid_date

    def ParseDateField(self, date_parameter, instrument=None):
        valid_date = ''
        try:
            if date_parameter:
                date_string = date_parameter.lstrip('-0123456789')
                days = date_parameter[:len(date_string) * -1]
                calendar = None

                if len(date_string) == 4:  # Business center
                    date_string = date_string.upper()
                    try:
                        calendar = acm.FCalendar.Select01('businessCenter=%s' % date_string, 'Not found')
                        if not calendar:
                            print("Please enter valid date, Calendar with business center %s not in database" % date_string)
                    except Exception as ex:
                        # For older version of prime where business calendar field not in calendar
                        print("Please enter valid date, Cannot find calendar with business center %s, %s" % (
                        date_string, str(ex)))

                elif len(date_string) == 3:  # Currency
                    date_string = date_string.upper()
                    curr_from_db = acm.FInstrument[date_string]
                    if curr_from_db:
                        calendar = curr_from_db.Calendar()
                    else:
                        print("Please enter valid date, Cannot find currency %s in database" % date_string)

                elif len(date_string) == 1 and date_string == 'd':
                    if instrument:
                        instrument = instrument[0]
                        print("Get instrument <%s> calendar" % instrument.Name())
                        calendar = instrument.SettlementCalendar()
                        if not calendar:
                            if instrument.Currency() and instrument.Currency().Calendar():
                                calendar = instrument.Currency().Calendar()
                    else:
                        valid_date = ael.date_today().add_period(date_parameter)

                else:
                    valid_date = ael.date_today().add_period(date_parameter)

                if calendar and days.lstrip('-').isdigit():
                    valid_date = calendar.AdjustBankingDays(ael.date_today(), int(days))

                if valid_date:
                    valid_date = ael.date_from_string(str(valid_date))
        except Exception as error:
            print("Could not load module ael or incorrect date format.", str(error))

        return valid_date

    def unlink_external_object(self, ael_object):
        if ael_object:
            if ael_object.record_type == 'Instrument':
                ext_obj = acm.FExternalObject.Select("instrument=%d"%ael_object.insaddr)
                if ext_obj:
                    for i in ext_obj[:]:
                        try:
                            i.Instrument = None
                            i.Commit()
                        except Exception as e:
                             raise Exception("Exception in unlink ExternalObject from Instrument : %s" % str(i.insid))
            elif ael_object.record_type == 'Settlement':
                ext_obj = acm.FExternalObject.Select("settlement=%d"%ael_object.seqnbr)
                if ext_obj:
                    for i in ext_obj[:]:
                        try:
                            i.Settlement = None
                            i.Commit()
                        except Exception as e:
                            raise Exception("Exception in unlink ExternalObject from Settlement : %s" % str(i.seqnbr))
            elif ael_object.record_type == 'Confirmation':
                ext_obj = acm.FExternalObject.Select("confirmation=%d"%ael_object.seqnbr)
                if ext_obj:
                    for i in ext_obj[:]:
                        try:
                            i.Confirmation = None
                            i.Commit()
                        except Exception as e:
                            raise Exception("Exception in unlink ExternalObject from Confirmation : %s" % str(i.seqnbr))
            elif ael_object.record_type == 'Party':
                ext_obj = acm.FExternalObject.Select("party=%d"%ael_object.ptynbr)
                if ext_obj:
                    for i in ext_obj[:]:
                        try:
                            i.Party = None
                            i.Commit()
                        except Exception as e:
                            raise Exception("Exception in unlink ExternalObject from Party : %s" % str(i.ptyid))
            elif ael_object.record_type == 'CorpAction':
                ext_obj = acm.FExternalObject.Select("corpAction=%d"%ael_object.seqnbr)
                if ext_obj:
                    for i in ext_obj[:]:
                        try:
                            i.CorpAction = None
                            i.Commit()
                        except Exception as e:
                            raise Exception("Exception in unlink ExternalObject from CorpAction : %s" % str(i.name))

    def create_price_semantic(self, semantic_name, provider_type):
        """Creating price semantic"""
        is_created = False
        semantic_obj = acm.FPriceSemantic[semantic_name]
        if not semantic_obj:
            try:
                priceSemantic = acm.FPriceSemantic()
                priceSemantic.Name(semantic_name)
                priceSemantic.ProviderType(provider_type)
                priceSemantic.Commit()
                is_created = True
            except Exception as e:
                raise Exception('Error creating semantic {} : {}'.format(semantic_name, str(e)))
        else:
            raise AlreadyExist("Semantic {} already exists in db".format(semantic_name))
        return is_created

    def create_marketplace(self, market_place_name):
        """Creating price Market Place"""
        is_created = False
        market_obj = acm.FMarketPlace[market_place_name]
        if not market_obj:

            try:
                party = acm.FMarketPlace()
                party.Name(market_place_name)
                party.Commit()
                is_created = True
            except Exception as e:
                raise Exception('Error creating market place {} : {}'.format(market_place_name, str(e)))
        else:
            raise AlreadyExist("Market Place {} already exists in db".format(market_place_name))
        return is_created

    def create_distributor(self, dist_name, dist_type):
        """Creating price distributor"""
        is_created = False
        dist_obj = acm.FPriceDistributor[dist_name]
        if not dist_obj:
            try:
                price_dist = acm.FPriceDistributor()
                price_dist.Name(dist_name)
                price_dist.DistributorType(dist_type)
                price_dist.Commit()
                is_created = True
            except Exception as e:
                raise Exception('Error creating distributor {} : {}'.format(dist_name, str(e)))
        else:
            raise AlreadyExist("Distributor {} already exists in db".format(dist_name))
        return is_created

    def copy_folder_with_options(self, src_path, dest_path, include_extension='*', ignore_folders=None, flat_hierarchy=False):
        """
        params:
        source_path = C:\\Users\\E1077313\\Work\\Veracode\\SwiftIntegration
        destination_path = C:\\Users\\E1077313\\Work\\Veracode\\ScanReady
        extension_to_copy = ['.py']
        flat_hierarchy=False, Controls whether to imitate the tree structure or copy all files in the single folder
        folders_to_skip = ['XSD', 'Parameters', 'BindingModules', 'FSwiftCustomMessage', 'LongForm','MiFIDII',
        'RegulatoryInfo','STRATE','__pycache__','TemplateFiles','FSwiftXSDGenerator','ClassDiagram','SampleMessages',
        'lib','AsgardTests','build','Deprecated','Design & Analysis','SwiftWriterExample']

        Usage:
        copy_folder_with_options(source_path, destination_path, extension_to_copy, folders_to_skip, flat_hierarchy)
        """
        import shutil
        def copy_folder(src_path, dest_path):
            file_copy_counter = 0
            scan_iter = os.scandir(src_path)
            for entry in scan_iter:
                dest_dir_or_file = dest_path + '\\' + entry.name
                src_dir_or_file = src_path + '\\' + entry.name
                file_or_folder_name = entry.name

                if flat_hierarchy:
                    dest_dir_or_file = dest_path

                if entry.is_dir():
                    if ignore_folders is None or (
                            ignore_folders is not None and file_or_folder_name not in ignore_folders):
                        if not flat_hierarchy:
                            os.makedirs(dest_dir_or_file)
                        file_copy_counter += copy_folder(src_dir_or_file, dest_dir_or_file)
                else:
                    file_ext = os.path.splitext(file_or_folder_name)[1]
                    copy_file = include_extension == '*' or file_ext in include_extension
                    if copy_file:
                        name = os.path.basename(src_dir_or_file)
                        if os.path.exists(os.path.join(dest_dir_or_file, name)):
                            print('The file is duplicate and has been overwritten', src_dir_or_file)
                        shutil.copy2(src_dir_or_file, dest_dir_or_file)
                        file_copy_counter += 1
            scan_iter.close()
            return file_copy_counter

        def clean_folder(dest_path):
            try:
                scan_iter = os.scandir(dest_path)
            except FileNotFoundError:
                if flat_hierarchy: #Create the distination path only once
                    os.mkdir(dest_path)
                return

            for entry in scan_iter:
                dest_dir_or_file = dest_path + '\\' + entry.name
                if entry.is_dir():
                    shutil.rmtree(dest_dir_or_file)
                else:
                    os.remove(dest_dir_or_file)
            scan_iter.close()

        clean_folder(dest_path)
        return copy_folder(src_path, dest_path)


class FParamsEncode(object):
    def __init__(self):
        self.__key = 'FrontArenaOTC'
        self.__key = self.__key

    def get_key(self):
        return self.__key

    def set_encrypted_password(self, content):
        """set the encoded value for the given content"""
        enc = []
        for i in range(len(content)):
            key_c = self.__key[i % len(self.__key)]
            enc_c = chr((ord(content[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        if sys.version_info[0] < 3:
            encoded_value = '0x4' + base64.urlsafe_b64encode("".join(enc))
        else:
            enc_string = "".join(enc)
            enc_encoded = enc_string.encode('UTF-8')
            encoded_value = base64.urlsafe_b64encode(enc_encoded)
            encoded_value = b'0x4' + encoded_value
        return encoded_value

    def get_decrypted_password(self, content):
        """get the encoded value for the given content"""
        dec = []
        content = content[3:]
        if sys.version_info[0] < 3:
            enc = base64.urlsafe_b64decode(content)
        else:
            enc = base64.urlsafe_b64decode(content).decode('UTF-8')
        for i in range(len(enc)):
            key_c = self.__key[i % len(self.__key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def get_string(self, content):
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8')
        except:
            pass
        try:
            if isinstance(content, unicode):
                content = content.encode('ascii', 'replace')
        except:
            pass
        return content

# -----------------exception classes---------------------------------------------------

class AddInfoSpecAlreadyExits(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)


class AddInfoSpecNotExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

class ChoiceListAlreadyExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

class ChoiceListNotFound(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

class AliasTypeSpecNotExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

class AdditionalInfoSpecNotExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

class AliasTypeAlreadyExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)


class AlreadyExist(Exception):
    def _set_message(self, message):
        self.message = message

    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)




