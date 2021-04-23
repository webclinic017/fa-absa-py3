"""----------------------------------------------------------------------------
MODULE
    FSwiftParameter - Module with variables needed by the SWIFT framework

HISTORY
============================================================================================================================
Date            Change no       Developer       Description
----------------------------------------------------------------------------------------------------------------------------
2017-08-26      2017 Upgrade    Willie vd Bank  Added DEFAULT_PARTIAL_SETTLEMENT_TYPE parameter as part of 2017 upgrade
2018-05-11      CHG1000406751   Willie vd Bank  Modified MT541 and MT543
2020-05-07      FAOPS-700       Cuen Edwards    Added rounding rule for KES.
----------------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------"""

OPTIONS = {}

OPTIONS[103] = {'ORDERING_CUSTOMER':'K',
                'INTERMEDIARY_INSTITUTION':'A',
                'BENEFICIARY_CUSTOMER':'A',
                'ACCOUNT_WITH_INSTITUTION':'A',
                'SENDERS_CORRESPONDENT': 'A',
                'ORDERING_INSTITUTION':'A'}

OPTIONS[192] = {}

OPTIONS[199] = {}

OPTIONS[200] = {'ACCOUNT_WITH_INSTITUTION':'A',
                'INTERMEDIARY':'A'}

OPTIONS[202] = {'ACCOUNT_WITH_INSTITUTION':'A',
                'BENEFICIARY_INSTITUTION':'A',
                'INTERMEDIARY':'A',
                'ORDERING_INSTITUTION':'A',
                'SENDERS_CORRESPONDENT': 'A'}
                
OPTIONS[210] = {'ORDERING_CUSTOMER':'C', 'ORDERING_INSTITUTION':'A',
                 'INTERMEDIARY':'A'}
OPTIONS[292] = {}

OPTIONS[299] = {}

OPTIONS[300] = {'PARTY_A':'A', 'PARTY_B':'A', 'SELL_RECEIVING_AGENT':'A',
                'BUY_RECEIVING_AGENT':'A', 'BUY_DELIVERY_AGENT':'A',
                'SELL_DELIVERY_AGENT':'A', 'SELL_BENEFICIARY_INSTITUTION':'A',
                'BUY_INTERMEDIARY':'A', 'SELL_INTERMEDIARY':'A'}
                
OPTIONS[305] = {'PARTY_A':'A', 'PARTY_B':'A', 'ACCOUNT_WITH_INSTITUTION':'A',
                'SENDER_CORRESPONDENT':'A', 'INTERMEDIARY':'A' }
                
OPTIONS[306] = {'PARTY_A':'A', 'PARTY_B':'A', 'SIP_PARTY_RECEIVING_AGENT':'A',
                'PAYOUT_RECEIVING_AGENT':'J','CALCULATION_AGENT':'A'}
                
OPTIONS[320] = {'PARTY_A':'A', 'PARTY_B':'A',
                'SIA_PARTY_A_INTERMEDIARY':'A',
                'SIA_PARTY_B_INTERMEDIARY':'A',
                'SIA_PARTY_A_RECEIVING_AGENT':'A',
                'SIA_PARTY_B_RECEIVING_AGENT':'A'}

OPTIONS[330] = {'PARTY_A':'A', 'PARTY_B':'A',
                'SIA_PARTY_A_RECEIVING_AGENT':'A',
                'SIA_PARTY_B_RECEIVING_AGENT':'A'}

OPTIONS[362] = {'PARTY_A':'A', 'PARTY_B':'A',
                'NAP_PARTY_A_RECEIVING_AGENT':'A',
                'NAP_PARTY_B_RECEIVING_AGENT':'A'}

OPTIONS[395] = {}


OPTIONS[402] = {'ACCOUNT_WITH_INSTITUTION':'A',
                'BENEFICIARY_CUSTOMER':'A',
                'BENEFICIARY_INSTITUTION':'A',
                'INTERMEDIARY_INSTITUTION':'A',
                'ORDERING_CUSTOMER':'A',
                'ORDERING_INSTITUTION':'A',
                'RECEIVERS_CORRESPONDENT':'A',
                'SENDERS_CORRESPONDENT': 'A'}
                
OPTIONS[540] = {'SETTLEMENT_DATETIME':'A', 'ACCOUNT':'A',
                'PARTY':'P', 'SAFEKEEPING_ACCOUNT':'A'}

OPTIONS[541] = {'SETTLEMENT_DATETIME':'A', 'ACCOUNT':'A',
                'PARTY':'P', 'SAFEKEEPING_ACCOUNT':'A'}
OPTIONS[542] = {'SETTLEMENT_DATETIME':'A', 'ACCOUNT':'A',
                'PARTY':'P', 'SAFEKEEPING_ACCOUNT':'A'}

OPTIONS[543] = {'SETTLEMENT_DATETIME':'A', 'ACCOUNT':'A',
                'PARTY':'P', 'SAFEKEEPING_ACCOUNT':'A'}

TERMS_CONDITIONS = '/FIDU/'

FAS = 'FAS'
FAC = 'FAC'

USED_MT_MESSAGES_SETTLEMENT = [(103, 'Yes'), (192, 'Yes'), (199, 'Yes'),
                               (200, 'Yes'), (202, 'Yes'), (292, 'Yes'),
                               (299, 'Yes'), (210, 'Yes'), (402, 'Yes'),
                               (540, 'Yes'), (541, 'Yes'), (542, 'Yes'), 
                               (543, 'Yes'), (503, 'Yes')]

USED_MT_MESSAGES_CONFIRMATION = [(300, 'Yes'), (305, 'Yes'),
                                 (306, 'Yes'), (320, 'Yes'),
                                 (330, 'Yes'), (362, 'Yes'), (395, 'Yes'),
                                 (598, 'Yes'), (298, 'Yes'), (564, 'Yes')]

MT_MANDATORY_FIELDS = {
                   300 : ['15A', '20', '22A', '22C', '82A', '87A', '15B', '30T', '30V', '36', '32B', '57A', '33B'],
                   305 : ['20', '21', '22', '22C', '30', '82A', '31G', '26F', '32B', '36', '33B', '37K', '34A', '57A'],
                   306 : ['15A', '20', '22A', '22C', '21N', '12F', '12E', '17A', '17F', '22K', '82A', '87A', '77H', '15B', '17V', '30T', '30X', '29R', '30F'],
                   320 : ['15A', '20', '22A', '22B', '22C', '82A', '87A', '15B', '17R', '30T', '30V', '30P', '32B', '34E', '37G', '14D', '15C', '57A', '15D'],
                   330 : ['15A', '20', '22A', '22B', '22C', '82A', '87A', '15B', '17R', '30T', '30V', '38A', '32B', '37G', '14D', '15C', '57A'],
                   362 : ['15A', '20', '22A', '22C', '23A', '21N', '30V', '30P', '82A', '87A']
                    }

SWIFT_SUB_NETWORKS = ['EBA', 'TARGET2']

SWIFT_SERVICE_CODE = {'TARGET2':'TGT', 'EBA':'EBA'}

BANKING_PRIORITY = {'TARGET2':'NYNN', 'EBA':''}

NATIONAL_CLEARING_SYSTEM = {'Fedwire' : 'FW'}

ROUND_PER_CURR = {'EUR':2, 'USD':2, 'JPY':0, 'KRW':0, 'TRY':0, 'KWD':3, 'AED':2,
                  'ARS':2, 'AUD':2, 'BAM':2, 'BRL':2, 'BGN':2, 'CAD':2, 'CNY':2,
                  'CZK':2, 'DKK':2, 'GBP':2, 'HKD':2, 'HRK':2, 'HUF':2, 'ISK':2,
                  'INR':2, 'IDR':2, 'LVL':2, 'MYR':2, 'MXN':2, 'MXV':2, 'NZD':2,
                  'NOK':2, 'PHP':2, 'SAR':2, 'SGD':2, 'ZAR':2, 'SEK':2, 'CHF':2,
                  'TWD':2, 'THB':2, 'UGX':0, 'KES':0}

USE_PARTY_FULLNAME = 0

SEPARATOR = 'newline'

CODEWORD_NEWLINE = 'codeword'

SWIFT_LOOPBACK = 0

SENDER_BIC_LOOPBACK    = ""

RECEIVER_BIC_LOOPBACK  = ""

dict_trans = {0: ' ', 1: ' ', 2: ' ', 3: ' ', 4: ' ',
5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' ', 10: '\n',
11: ' ', 12: ' ', 13: '\r', 14: ' ', 15: ' ', 16: ' ',
17: ' ', 18: ' ', 19: ' ', 20: ' ', 21: ' ', 22: ' ',
23: ' ', 24: ' ', 25: ' ', 26: ' ', 27: ' ', 28: ' ',
29: ' ', 30: ' ', 31: ' ', 32: ' ', 33: ' ', 34: ' ', 35: ' ',
36: ' ', 37: ' ', 38: ' ',39: "'", 40: '(', 41: ')', 42: ' ', 43: '+',
44: ',', 45: '-', 46: '.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3',
52: '4', 53: '5', 54: '6',55: '7', 56: '8', 57: '9', 58: ':', 59: ';',
60: ' ', 61: '=', 62: ' ', 63: ' ', 64: '@', 65: 'A', 66: 'B', 67: 'C',
68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J', 75: 'K',
76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S',
84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z', 91: ' ',
92: '/', 93: ' ', 94: ' ', 95: ' ', 96: ' ', 97: 'a', 98: 'b', 99: 'c',
100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j',
107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q',
114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x',
121: 'y', 122: 'z', 123: ' ', 124: ' ', 125: ' ', 126: ' ',
127: ' ', 128: ' ', 129: ' ', 130: ' ', 131: ' ', 132: ' ',
133: ' ', 134: ' ', 135: ' ', 136: ' ', 137: ' ', 138: ' ',
139: ' ', 140: ' ', 141: ' ', 142: ' ', 143: ' ', 144: ' ',
145: ' ', 146: ' ', 147: ' ', 148: ' ', 149: ' ', 150: ' ',
151: ' ', 152: ' ', 153: ' ', 154: ' ', 155: ' ', 156: ' ',
157: ' ', 158: ' ', 159: ' ', 160: ' ', 161: ' ', 162: ' ',
163: ' ', 164: ' ', 165: ' ', 166: ' ', 167: ' ', 168: ' ',
169: ' ', 170: ' ', 171: ' ', 172: ' ', 173: ' ', 174: ' ',
175: ' ', 176: ' ', 177: ' ', 178: ' ', 179: ' ', 180: ' ',
181: ' ', 182: ' ', 183: ' ', 184: ' ', 185: ' ', 186: ' ',
187: ' ', 188: ' ', 189: ' ', 190: ' ', 191: ' ', 192: ' ',
193: ' ', 194: ' ', 195: ' ', 196: ' ', 197: ' ', 198: ' ',
199: ' ', 200: ' ', 201: ' ', 202: ' ', 203: ' ', 204: ' ',
205: ' ', 206: ' ', 207: ' ', 208: ' ', 209: ' ', 210: 'O',
211: 'O', 212: 'O', 213: 'O', 214: 'O', 215: ' ', 216: ' ',
217: 'U', 218: 'U', 219: 'U', 220: 'U', 221: 'Y', 222: ' ',
223: ' ', 224: 'a', 225: 'a', 226: 'a', 227: 'a', 228: 'a',
229: 'a', 230: ' ', 231: 'c', 232: 'e', 233: 'e', 234: 'e',
235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i', 240: ' ',
241: 'n', 242: 'o', 243: 'o', 244: 'o', 245: 'o', 246: 'o',
247: ' ', 248: ' ', 249: 'u', 250: 'u', 251: 'u', 252: 'u',
253: 'y', 254: ' ', 255: 'y'}

POPULATE_RELEASE_DAY = 0

city_dict = {'BUENOS AIRES' : 'ARBA',
             'VIENNA'      : 'ATVI',
             'MELBOURNE'   : 'AUME',
             'SYDNEY'      : 'AUSY',
             'BRUSSELS'    : 'BEBR',
             'SAO PAULO':'BRSP',
             'MONTREAL':'CAMO',
             'TORONTO':'CATO',
             'GENEVA':'CHGE',
             'ZURICH':'CHZU',
             'SANTIAGO':'CLSA',
             'BEIJING':'CNBE',
             'PRAGUE':'CZPR',
             'EUROPEAN CENTRAL BANK':'DECB',
             'FRANKFURT':'DEFR',
             'COPENHAGEN':'DKCO',
             'TALLINN':'EETA',
             'MADRID':'ESMA',
             'TARGET':'EUTA',
             'HELSINKI':'FIHE',
             'PARIS':'FRPA',
             'LONDON':'GBLO',
             'ATHENS':'GRAT',
             'HONG KONG':'HKHK',
             'BUDAPEST':'HUBU',
             'JAKARTA':'IDJA',
             'DUBLIN':'IEDU',
             'TEL AVIV':'ILTA',
             'MUMBAI':'INMU',
             'MILAN':'ITMI',
             'ROME':'ITRO',
             'TOKYO':'JPTO',
             'SEOUL':'KRSE',
             'BEIRUT':'LBBE',
             'COLOMBO':'LKCO',
             'LUXEMBOURG':'LULU',
             'MEXICO CITY':'MXMC',
             'KUALA LUMPUR':'MYKL',
             'AMSTERDAM':'NLAM',
             'OSLO':'NOOS',
             'NEW YORK FED':'NYFD',
             'NEW YORK STOCK EXCHANGE':'NYSE',
             'AUCKLAND':'NZAU',
             'WELLINGTON':'NZWE',
             'PANAMA CITY':'PAPC',
             'MANILA':'PHMA',
             'WARSAW':'PLWA',
             'LISBON':'PTLI',
             'BUCHAREST':'ROBU',
             'MOSCOW':'RUMO',
             'RIYADH':'SARI',
             'STOCKHOLM':'SEST',
             'SINGAPORE':'SGSI',
             'BRATISLAVA':'SKBR',
             'BANGKOK':'THBA',
             'ANKARA':'TRAN',
             'ISTANBUL':'TRIS',
             'TAIPEI':'TWTA',
             'CHICAGO':'USCH',
             'U.S. GOVERNMENT SECURITIES':'USGS',
             'LOS ANGELES':'USLA',
             'NEWYORK':'USNY',
             'HANOI':'VNHA',
             'JOHANNESBURG':'ZAJO',
             'EDINBURGH':'GBED'}

DEFAULT_PARTIAL_SETTLEMENT_TYPE = 'NPAR'
