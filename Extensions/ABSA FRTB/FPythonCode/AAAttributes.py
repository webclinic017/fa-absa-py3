""" Compiled: 2020-01-21 09:44:05 """

#__src_file__ = "extensions/aa_integration/./etc/AAAttributes.py"
"""----------------------------------------------------------------------------
MODULE
    AAAttributes - Module containing AA installation attributes.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import os
import acm

ATTRIBUTES = {
    'LIB_PATH': r'C:\Program Files\FIS\Adaptiv Analytics',
    'START_MEMORY_CUBE_SERVICE': False,
    'ARTIQ_DESTINATION_DIR': None,
    'ARTIQ_DESTINATION_INCREMENT': 'Main',
    'ARTIQ_DESTINATION_SNAPSHOT': 1,
}

FRTB_SNAPSHOT=1
SACCR_SNAPSHOT=1
CSV_FILEIMPORT_SNAPSHOT=1

FRTBATTRIBUTES = ATTRIBUTES.copy()
FRTBATTRIBUTES['START_MEMORY_CUBE_SERVICE'] = False
FRTBATTRIBUTES['DEFAULT_STATIC_DATA_DIR'] = os.path.join(
    FRTBATTRIBUTES['LIB_PATH'], 'Configuration', 'StaticData'
)
FRTBATTRIBUTES['COMBINED_STATIC_DATA_PATH'] = os.path.join(
    FRTBATTRIBUTES['DEFAULT_STATIC_DATA_DIR'], 'CombinedFRTBStaticData.xml'
)
FRTBATTRIBUTES['ARTIQ_DESTINATION_SNAPSHOT'] = FRTB_SNAPSHOT

SACCRATTRIBUTES = ATTRIBUTES.copy()
SACCRATTRIBUTES['START_MEMORY_CUBE_SERVICE'] = False
SACCRATTRIBUTES['ARTIQ_DESTINATION_SNAPSHOT'] = SACCR_SNAPSHOT

CSVFILEIMPORTATTRIBUTES = ATTRIBUTES.copy()
CSVFILEIMPORTATTRIBUTES['START_MEMORY_CUBE_SERVICE'] = False
CSVFILEIMPORTATTRIBUTES['ARTIQ_DESTINATION_SNAPSHOT'] = CSV_FILEIMPORT_SNAPSHOT

SIMMATTRIBUTES = ATTRIBUTES.copy()

DEFAULTATTRIBUTES = ATTRIBUTES.copy()

FRTB_GROUPER_DIMENSION_MAP = {acm.FSymbol('Trade.Portfolio'): 'Portfolio',
                        #acm.FSymbol('Trade.Instrument'): 'Instrument Name'}
                        acm.FSymbol('Trade.Instrument'): 'Reference'}

KVAATTRIBUTES = ATTRIBUTES.copy()
KVAATTRIBUTES['START_MEMORY_CUBE_SERVICE'] = False

CALC_SNAPSHOT_MAP = {
    'FRTB All': 1,
    'SA DRC': 1,
    'SA RRAO': 1,
    'SA SBA': 1,
    'IMA DRC': 1,
    'IMA ES': 1,
    'IMA Hypothetical_PL': 1,
    'IMA PL_Attribution': 1,
    'IMA Risk_Theoretical_PL': 1,
    'IMA SES': 1,
    'CSV Import': 1,
    'SA-CCR': 1,
    'KVA':1,
    'SIMM':1,
    'Sensitivities':1,
    'SensitivitiesPL':1,
    'PLRates':1
    
}

GROUPER_COLUMNNAME_MAP = {
    'Trade: Currency' : 'Currency',
    'Trade Currency' : 'Currency',
    'Currency' : 'Currency',
    'Trade: Acquirer' : 'Acquirer'
}
