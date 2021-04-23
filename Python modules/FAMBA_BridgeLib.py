
#========================================================================
#
#File for shared resources
#
#
#
#
#
#
#
#========================================================================

import acm
import ael
import FAMBA_Bridge
import AMBA_Bridge_pref

def addInfoSpecRdOrNew(table,reverse=False):
    """ Returns the Amba bridge reference AdditionalInfoSpec of this table.
        Creates one if it cannot find it. """
    # Gets name of additional info field from FAMBA_Bridge
    if reverse:
        key = FAMBA_Bridge.reverse_addinfo_prefix + table
    else:
        key = FAMBA_Bridge.addinfo_prefix + table
    ais = ael.AdditionalInfoSpec[key]
    if not ais:
        ais = ael.AdditionalInfoSpec.new()
        ais.rec_type = table
        ais.field_name = key
        ais.mandatory = 0
        setattr(ais, 'data_type.grp', 'Standard')
        setattr(ais, 'data_type.type',
                ael.enum_from_string('B92StandardType', 'String'))
        ais.description = 'AMBA Bridge reference key.'
        ais.commit() 
        #fetch the real recaddress
        ais = ael.AdditionalInfoSpec[key]
    return ais


        
