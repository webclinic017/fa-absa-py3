'''
Purpose: [ISDA Matrix definitions used for commodity confirmations to Trident]
Department: [Operations]
Requester: [Moeketsi Makhalemele]
Developer: [Willie van der Bank]
CR Number: [183633 2012-05-19]
'''

import ael

ISDA_COMM_NAME = 0
ISDA_COMM_TYPE = 1
ISDA_COMM_UNIT = 2

ISDA_COMMODITY_MATRIX = {
'XAG': ['Silver', 'Precious Metal', 'Ounces'],
'XAU': ['Gold', 'Precious Metal', 'Ounces'],
'XPT': ['Platinum', 'Precious Metal', 'Ounces'],
'XPD': ['Palladium', 'Precious Metal', 'Ounces'],
'MCU': ['Copper', 'Base Metal', 'Tonne'],
'MAL': ['Aluminium', 'Base Metal', 'Tonne'],
'MPB': ['Lead', 'Base Metal', 'Tonne'],
'MNI': ['Nickel', 'Base Metal', 'Tonne'],
'MSN': ['Tin', 'Base Metal', 'Tonne'],
'MZN': ['Zinc', 'Base Metal', 'Tonne'],
'WTI': ['Oil-WTI', 'Energy', 'Barrel'],
'BRT': ['Oil-Brent', 'Energy', 'Barrel'],
'Bent': ['Oil-Brent', 'Energy', 'Barrel'],
'GAS_OIL': ['Gas-Oil', 'Energy', 'Barrel'],
'API': ['Coal', 'Energy', 'Barrel'],
}
