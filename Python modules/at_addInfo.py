# SUBMODULE      at_addInfo, part of 'at' module
# For history see 'at' module.

import acm                      #@UnresolvedImport
import at_addInfoSpec as addInfoSpec
import at_dataTypes as dataTypes
import at_choiceList as choiceList

def delete(entity, add_info_name):
    """Delete the specified additional info from the entity.

    :param entity: ACM persistent object, e.g. ``FInstrument``
    :type entity: ``FPersistent``
    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string

    """
    add_info = get(entity, add_info_name)
    if add_info: add_info.Delete()

def find(add_info_name, value):
    """Return a list of FAdditionalInfo.

    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string
    :param value: Value of the additional info
    :type value: string
    :returns: ``list`` of ``FAdditionalInfo``

    """
    return [ai for ai in addInfoSpec.get(add_info_name).AddInf() if ai.FieldValue() == value]

def get(entity, add_info_name):
    """Return additional info object for the specified entity.

    :param entity: ACM object.
    :type entity: ``FPersistent``
    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string
    :returns: ``FAdditionalInfo`` -- or ``None``.

    """
    return acm.FAdditionalInfo.Select01('recaddr = {0} and addInf="{1}"'.format(entity.Oid(), add_info_name), None)

def get_value(entity, add_info_name):
    """Return additional info VALUE for the specified entity.

    :param entity: ACM object.
    :type entity: ``FPersistent``
    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string
    :returns: string

    """
    
    property_name = acm.FAdditionalInfoSpec[add_info_name].AttributeName().AsString()
    property_name = property_name[0].upper() + property_name[1:]
    return entity.AdditionalInfo().GetProperty(property_name)

def save(entity, add_info_name, value):
    """Set additional info to the entity, creating new when necessary.

    :param entity: ACM object.
    :type entity: ``FPersistent``
    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string
    :param value: Additional info value.
    :type value: string
    :raises: ``ValueError`` when ``value`` is invalid for the additional info specification.

    """
    _validate_addInfo_value(entity, add_info_name, value)

    add_info = get(entity, add_info_name)
    if add_info == None: # AddInfo does not exist
        add_info = acm.FAdditionalInfo()
        add_info.Recaddr(entity.Oid())
        add_info.AddInf(acm.FAdditionalInfoSpec[add_info_name])
        add_info.FieldValue(value)
    else: # AddInfo exists
        add_info.FieldValue(value)
    add_info.Commit()
    return add_info

def _validate_addInfo_value(entity, add_info_name, value):
    if value in ('', None): raise ValueError('Value cannot be empty or None.')
    
    ais = addInfoSpec.get(add_info_name)
    
    if ais.RecType() != entity.RecordType():
        raise ValueError("Addinfo '%s' not defined on '%s'" %(add_info_name, entity.RecordType()))

    # verify the value matches a choice list value
    if ais.DataTypeType() == dataTypes.DT_CHOICE_LIST and ais.DataTypeGroup() == dataTypes.DTG_RECORD_REF:
        cl = choiceList.get(ais.Description())
        if not (value in (c.Name() for c in cl.Choices())):
            raise ValueError('Value {0} is not in choice list {1}.'.format(value, cl.Name()))

def save_or_delete(entity, add_info_name, value):
    """Save or delete addInfo for specified entity.

    When ``value`` is ``None`` or an empty string the function deletes the additional info.

    :param entity: ACM object.
    :type entity: ``FPersistent``
    :param add_info_name: Name of the additional info specification.
    :type add_info_name: string
    :param value: Additional info value.
    :type value: string
    :raises: ``ValueError`` when ``value`` is invalid for the additional info specification.

    """
    if value is None or value == '':
        delete(entity, add_info_name)
    else:
        save(entity, add_info_name, value)
