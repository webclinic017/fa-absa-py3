import ael

def set_AdditionalInfoSpec(toClone, fieldName, rec_type, description, default):
    ais = ael.AdditionalInfoSpec[toClone].new()
    ais.field_name = fieldName
    ais.rec_type = rec_type
    ais.description = description
    ais.default_value = default
    try:
        ais.commit()
        return 'Additional info Spec: ' + fieldName + ' was created successfuly.'
    except:
        return 'Additional info Spec: ' + fieldName + ' encountered an error.'
        
print set_AdditionalInfoSpec(798, 'Clearing Status', 'Trade', 'Clearing Status of MW trades', '')
print set_AdditionalInfoSpec(798, 'Clearing Trade ID', 'Trade', 'SWML Trade ID', '') 
print set_AdditionalInfoSpec(798, 'Clearing Member', 'Trade', 'Clearing Member', '')
print set_AdditionalInfoSpec(798, 'ClearingMemberCode', 'Trade', 'Clearing Member Code', '')