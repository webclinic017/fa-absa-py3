import ael

#ins_report_by()
#---------------
#
#Called when opening an instrument containing the field
#"Report By" (e.g. Buy-Sellback). The return value
#(i.e. the default GUI value) can be 'Price' or 'Consideration'

def ins_report_by():
    default_value = 'Price'
    return default_value
