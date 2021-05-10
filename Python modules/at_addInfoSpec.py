"""Manages Additional Info Specification (FAdditionalInfoSpec)."""

#SUBMODULE      at_addInfoSpec, part of 'at' module
#For history see 'at' module.

import acm                          #@UnresolvedImport
import logging
import at_dataTypes as dataTypes


def create_cl(add_info_name, choice_list_name, rec_type, default_value = None):
    """Create a new choice-list-based additional info specification."""
    ais = acm.FAdditionalInfoSpec()
    ais.DataTypeGroup(dataTypes.DTG_RECORD_REF)
    
    choice_list = acm.FChoiceList.Select01('name="{0}"'.format(choice_list_name), None)
    if not choice_list: raise Exception('Choice list "{0}" was not found!'.format(choice_list_name))
    
    ais.DataTypeType(dataTypes.DT_CHOICE_LIST)
    ais.DefaultValue(default_value)
    ais.Description(choice_list_name) # binding to choice list
    ais.FieldName(add_info_name)
    ais.Name(add_info_name)
    ais.RecType(rec_type)
    ais.Commit()
    return ais

def delete(add_info_name):
    """Delete an addInfoSpec specified by its name and all its values."""
    logging.info('Deleting add info spec "{0}"'.format(add_info_name))
    ais = acm.FAdditionalInfoSpec[add_info_name]
    if not ais: return False
    delete_all_values(add_info_name)
    ais.Delete()
    return True

def delete_all_values(add_info_name):
    """Delete all addInfo values specified by their addInfoSpec name."""
    ais = acm.FAdditionalInfoSpec[add_info_name]
    if not ais: raise ValueError('Additional Info named "' + add_info_name + '" was not found.')
    add_infos = list(ais.AddInf())
    for ai in add_infos:
        logging.info('Deleting add info "{0}" from entity "{1}"'.format(add_info_name, ai.Recaddr()))
        ai.Delete()

def find(name):
    """Return an additional info specification by its name."""
    if not name: raise ValueError('name must be defined.')
    return acm.FAdditionalInfoSpec.Select01('name="{0}"'.format(name), None)

def get(name):
    """Return an additional info specification by its name. Throws an exception when no entry is found."""
    result = find(name)
    if not result: raise LookupError('addInfoSpec was not found')
    return result