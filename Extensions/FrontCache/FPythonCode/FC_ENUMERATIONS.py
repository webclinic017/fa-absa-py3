
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_ENUMERATIONS
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module holds all the enumerations needed for Frotn Cache
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing Front Arena and Python modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
from enum import Enum

'''----------------------------------------------------------------------------------------------------------
Enumerators for the Request Type of the Request Message.
----------------------------------------------------------------------------------------------------------'''
class RequestType():
    INSTRUMENT_TRADES = 1
    PORTFOLIO_TRADES = 2
    SINGLE_TRADE = 3
    SINGLE_SETTLEMENT = 4
    INSTRUMENT_SENSITIVITIES = 5
    PORTFOLIO_SENSITIVITIES = 6
    TRANSACTIONS = 7
    TRANSACTIONS_EOD = 8
    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)
'''----------------------------------------------------------------------------------------------------------
Enumerators for the Request Event Type of the Request Message.
----------------------------------------------------------------------------------------------------------'''
class RequestEventType():
    UNKNOWN = 0
    REAL_TIME_INSERT_TRADE = 1
    REAL_TIME_UPDATE_TRADE = 2
    REAL_TIME_INSERT_INSTRUMENT = 3
    REAL_TIME_UPDATE_INSTRUMENT = 4
    INTRADAY_TRADE = 5
    INTRADAY_INSTRUMENT_TRADES = 6
    INTRADAY_PORTFOLIO_TRADES = 7
    INTRADAY_INSTRUMENT = 8
    INTRADAY_PORTFOLIO = 9
    EOD_PORTFOLIO_TRADES = 10
    EOD_PORTFOLIO_TRADES_ON_TREE = 11
    EOD_PORTFOLIO_TRADES_OFF_TREE = 12
    REAL_TIME_INSERT_SETTLEMENT = 13
    REAL_TIME_UPDATE_SETTLEMENT = 14

    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)

'''----------------------------------------------------------------------------------------------------------
Enumerators for the Response Type of the Request Message.
----------------------------------------------------------------------------------------------------------'''
class ResponseType():
    UNKNOWN = 0
    SINGLE_TRADE_START = 1
    SINGLE_TRADE_END = 2
    INSTRUMENT_TRADES_START = 3
    INSTRUMENT_TRADES_END = 4
    PORTFOLIO_TRADES_START = 5
    PORTFOLIO_TRADES_END = 6
    SINGLE_INSTRUMENT_START = 7
    SINGLE_INSTRUMENT_END = 8
    SINGLE_PORTFOLIO_START = 9
    SINGLE_PORTFOLIO_END = 10
    SINGLE_SETTLEMENT_START = 11
    SINGLE_SETTLEMENT_END = 12

    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)

'''----------------------------------------------------------------------------------------------------------
Enumerators for the Data Serialization Type
----------------------------------------------------------------------------------------------------------'''
class SerializationType(Enum):
    XML = 0
    JSON = 1
    XML_COMPRESSED = 2
    JSON_COMPRESSED = 3
    PROTOBUF = 4

class RequestTopic():
    OFFICIAL_EOD_CLIENT_REPORTING = 1
    EOD_PORTFOLIO_TRADES_REQUEST = 2
    EOD_PORTFOLIO_TRADES_REQUEST2 = 3
    EOD_PORTFOLIO_TRADES_REQUEST3 = 4
    SINGLE_TRADE_REAL_TIME_INSERT_TRADE = 5
    SINGLE_TRADE_REAL_TIME_UPDATE_TRADE = 6
    SINGLE_TRADE_REAL_TIME_DELETE_TRADE = 7
    INSTRUMENT_TRADES_REAL_TIME_INSERT_INSTRUMENT = 8
    INSTRUMENT_TRADES_REAL_TIME_UPDATE_INSTRUMENT = 9
    INSTRUMENT_TRADES_REAL_TIME_DELETE_INSTRUMENT = 10
    SINGLE_SETTLEMENT_REAL_TIME_INSERT_SETTLEMENT = 11
    SINGLE_SETTLEMENT_REAL_TIME_UPDATE_SETTLEMENT = 12
    SINGLE_SETTLEMENT_REAL_TIME_DELETE_SETTLEMENT = 13
    INTRADAY_TRADE_REQUEST = 14
    INTRADAY_INSTRUMENT_TRADES_REQUEST = 15
    INTRADAY_SETTLEMENT_REQUEST = 16
    INTRADAY_INSTRUMENT_SENSITIVITY_REQUEST = 17
    INTRADAY_PORTFOLIO_SENSITIVITY_REQUEST = 18
    EOD_INSTRUMENT_SENSITIVITIES_REQUEST = 19
    EOD_PORTFOLIO_SENSITIVITIES_REQUEST = 20
    EOD_INSTRUMENT_SENSITIVITIES_PSWAP_REQUEST = 40

    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)

class TradeDomain():
    SOUTH_AFRICA = 1
    BOTSWANA = 2
    EGYPT = 3
    GHANA = 4
    KENYA = 5
    MAURITIUS_OFFSHORE = 6
    MAURITIUS_ONSHORE = 7
    MOZAMBIQUE = 8
    SEYCHELLES = 9
    TANZANIA = 10
    TANZANIA_NBC = 11
    UGANDA = 12
    ZAMBIA = 13
    ZIMBABWE = 14

    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)

class ServiceComponent():
    FC_REQ_COORD_01_ATS = 1
    FC_REQT_IT_01_ATS = 2
    FC_REQT_PS_01_ATS = 3
    FC_REQT_PT_01_ATS = 4
    FC_REQT_SS_01_ATS = 5
    FC_REQT_ST_01_ATS = 6
    FC_RES_COORD_01_ATS = 7
    FC_RT_01_ATS = 8
    FC_ISCOLL_01_ATS_01 = 9
    FC_ISCOLL_01_ATS_02 = 10
    FC_ISCOLL_01_ATS_03 = 11
    FC_ISCOLL_01_ATS_04 = 12
    FC_ISCOLL_01_ATS_05 = 13
    FC_ISCOLL_01_ATS_06 = 14
    FC_ISCOLL_01_ATS_07 = 15
    FC_ISCOLL_01_ATS_08 = 16
    FC_ISCOLL_01_ATS_09 = 17
    FC_ISCOLL_01_ATS_10 = 18
    FC_ISCOLL_01_ATS_11 = 19
    FC_ISCOLL_01_ATS_12 = 20
    FC_ISCOLL_01_ATS_13 = 21
    FC_ISCOLL_01_ATS_14 = 22
    FC_ISCOLL_01_ATS_15 = 23
    FC_ISCOLL_01_ATS_16 = 24
    FC_ISCOLL_01_ATS_17 = 25
    FC_ISCOLL_01_ATS_18 = 26
    FC_ISCOLL_01_ATS_19 = 27
    FC_ISCOLL_01_ATS_20 = 28
    FC_PSCOLL_01_ATS_01 = 29
    FC_PSCOLL_01_ATS_02 = 30
    FC_PSCOLL_01_ATS_03 = 31
    FC_PSCOLL_01_ATS_04 = 32
    FC_PSCOLL_01_ATS_05 = 33
    FC_PSCOLL_01_ATS_06 = 34
    FC_PSCOLL_01_ATS_07 = 35
    FC_PSCOLL_01_ATS_08 = 36
    FC_PSCOLL_01_ATS_09 = 37
    FC_PSCOLL_01_ATS_10 = 38
    FC_SCOLL_01_ATS_01 = 39
    FC_SCOLL_01_ATS_02 = 40
    FC_SCOLL_01_ATS_03 = 41
    FC_SCOLL_01_ATS_04 = 42
    FC_SCOLL_01_ATS_05 = 43
    FC_TCOLL_01_ATS_01 = 44
    FC_TCOLL_01_ATS_02 = 45
    FC_TCOLL_01_ATS_03 = 46
    FC_TCOLL_01_ATS_04 = 47
    FC_TCOLL_01_ATS_05 = 48
    FC_TCOLL_01_ATS_06 = 49
    FC_TCOLL_01_ATS_07 = 50
    FC_TCOLL_01_ATS_08 = 51
    FC_TCOLL_01_ATS_09 = 52
    FC_TCOLL_01_ATS_10 = 53
    FC_TCOLL_01_ATS_11 = 54
    FC_TCOLL_01_ATS_12 = 55
    FC_TCOLL_01_ATS_13 = 56
    FC_TCOLL_01_ATS_14 = 57
    FC_TCOLL_01_ATS_15 = 58
    FC_TCOLL_01_ATS_16 = 59
    FC_TCOLL_01_ATS_17 = 60
    FC_TCOLL_01_ATS_18 = 61
    FC_TCOLL_01_ATS_19 = 62
    FC_TCOLL_01_ATS_20 = 63
    FC_TCOLL_01_ATS_21 = 64
    FC_TCOLL_01_ATS_22 = 65
    FC_TCOLL_01_ATS_23 = 66
    FC_TCOLL_01_ATS_24 = 67
    FC_TCOLL_01_ATS_25 = 68
    FC_TCOLL_01_ATS_26 = 69
    FC_TCOLL_01_ATS_27 = 70
    FC_TCOLL_01_ATS_28 = 71
    FC_TCOLL_01_ATS_29 = 72
    FC_TCOLL_01_ATS_30 = 73
    FC_TCOLL_01_ATS_31 = 74
    FC_TCOLL_01_ATS_32 = 75
    FC_TCOLL_01_ATS_33 = 76
    FC_TCOLL_01_ATS_34 = 77
    FC_TCOLL_01_ATS_35 = 78
    FC_TCOLL_01_ATS_36 = 79
    FC_TCOLL_01_ATS_37 = 80
    FC_TCOLL_01_ATS_38 = 81
    FC_TCOLL_01_ATS_39 = 82
    FC_TCOLL_01_ATS_40 = 83
    FC_TCOLL_01_ATS_41 = 84
    FC_TCOLL_01_ATS_42 = 85
    FC_TCOLL_01_ATS_43 = 86
    FC_TCOLL_01_ATS_44 = 87
    FC_TCOLL_01_ATS_45 = 88
    FC_TCOLL_01_ATS_46 = 89
    FC_TCOLL_01_ATS_47 = 90
    FC_TCOLL_01_ATS_48 = 91
    FC_TCOLL_01_ATS_49 = 92
    FC_TCOLL_01_ATS_50 = 93
    FC_TCOLL_01_ATS_51 = 94
    FC_TCOLL_01_ATS_52 = 95
    FC_TCOLL_01_ATS_53 = 96
    FC_TCOLL_01_ATS_54 = 97
    FC_TCOLL_01_ATS_55 = 98
    FC_TCOLL_01_ATS_56 = 99
    FC_TCOLL_01_ATS_57 = 100
    FC_TCOLL_01_ATS_58 = 101
    FC_TCOLL_01_ATS_59 = 102
    FC_TCOLL_01_ATS_60 = 103
    FC_TCOLL_01_ATS_61 = 104
    FC_TCOLL_01_ATS_62 = 105
    FC_TCOLL_01_ATS_63 = 106
    FC_TCOLL_01_ATS_64 = 107
    FC_TCOLL_01_ATS_65 = 108
    FC_TCOLL_01_ATS_66 = 109
    FC_TCOLL_01_ATS_67 = 110
    FC_TCOLL_01_ATS_68 = 111
    FC_TCOLL_01_ATS_69 = 112
    FC_TCOLL_01_ATS_70 = 113
    FC_TCOLL_01_ATS_71 = 114
    FC_TCOLL_01_ATS_72 = 115
    FC_TCOLL_01_ATS_73 = 116
    FC_TCOLL_01_ATS_74 = 117
    FC_TCOLL_01_ATS_75 = 118
    FC_TCOLL_01_ATS_76 = 119
    FC_TCOLL_01_ATS_77 = 120
    FC_TCOLL_01_ATS_78 = 121
    FC_TCOLL_01_ATS_79 = 122
    FC_TCOLL_01_ATS_80 = 123
    FC_TCOLL_01_ATS_81 = 124
    FC_TCOLL_01_ATS_82 = 125
    FC_TCOLL_01_ATS_83 = 126
    FC_TCOLL_01_ATS_84 = 127
    FC_TCOLL_01_ATS_85 = 128
    PortfolioTradeSvc = 129
    DistributionWorker = 130
    FC_PSCOLL_01_ATS_11 = 131
    FC_PSCOLL_01_ATS_12 = 132
    FC_PSCOLL_01_ATS_13 = 133
    FC_PSCOLL_01_ATS_14 = 134
    FC_PSCOLL_01_ATS_15 = 135
    FC_PSCOLL_01_ATS_16 = 136
    FC_PSCOLL_01_ATS_17 = 137
    FC_PSCOLL_01_ATS_18 = 138
    FC_PSCOLL_01_ATS_19 = 139
    FC_PSCOLL_01_ATS_20 = 140
    Worker01 = 141
    Worker02 = 142
    Worker03 = 143
    Worker04 = 144
    Worker05 = 145
    Worker06 = 146
    Worker07 = 147
    Worker08 = 148
    Worker09 = 149
    Worker10 = 150
    Worker11 = 151
    Worker12 = 152
    Worker13 = 153
    Worker14 = 154
    Worker15 = 155
    Worker16 = 156
    Worker17 = 157
    Worker18 = 158
    Worker19 = 159
    Worker20 = 160
    Worker21 = 161
    Worker22 = 162
    Worker23 = 163
    Worker24 = 164
    Worker25 = 165
    Worker26 = 166
    Worker27 = 167
    Worker28 = 168
    Worker29 = 169
    Worker30 = 170
    Worker31 = 171
    Worker32 = 172
    Worker33 = 173
    Worker34 = 174
    Worker35 = 175
    Worker36 = 176
    Worker37 = 177
    Worker38 = 178
    Worker39 = 179
    Worker40 = 180
    Worker41 = 181
    Worker42 = 182
    Worker43 = 183
    Worker44 = 184
    Worker45 = 185
    Worker46 = 186
    Worker47 = 187
    Worker48 = 188
    Worker49 = 189
    Worker50 = 190
    WorkCoordinatorSvc = 191
    RealTimeTradeSvc = 192
    InstrumentTradeSvc = 193
    FC_TCOLL_01_ATS_86 = 194
    FC_TCOLL_01_ATS_87 = 195
    FC_TCOLL_01_ATS_88 = 196
    FC_TCOLL_01_ATS_89 = 197
    FC_TCOLL_01_ATS_90 = 198
    FC_TCOLL_01_ATS_91 = 199
    FC_TCOLL_01_ATS_92 = 200
    FC_TCOLL_01_ATS_93 = 201
    FC_TCOLL_01_ATS_94 = 202
    FC_TCOLL_01_ATS_95 = 203
    FC_TCOLL_01_ATS_96 = 204
    FC_TCOLL_01_ATS_97 = 205
    FC_TCOLL_01_ATS_98 = 206
    FC_TCOLL_01_ATS_99 = 207
    FC_TCOLL_01_ATS_100 = 208
    FC_TCOLL_01_ATS_101 = 209
    FC_TCOLL_01_ATS_102 = 210
    FC_TCOLL_01_ATS_103 = 211
    FC_TCOLL_01_ATS_104 = 212
    FC_TCOLL_01_ATS_105 = 213
    FC_TCOLL_01_ATS_106 = 214
    FC_TCOLL_01_ATS_107 = 215
    FC_TCOLL_01_ATS_108 = 216
    FC_TCOLL_01_ATS_109 = 217
    FC_TCOLL_01_ATS_110 = 218
    FC_TCOLL_01_ATS_111 = 219
    FC_TCOLL_01_ATS_112 = 220
    FC_TCOLL_01_ATS_113 = 221
    FC_TCOLL_01_ATS_114 = 222
    FC_TCOLL_01_ATS_115 = 223
    FC_TCOLL_01_ATS_116 = 224
    FC_TCOLL_01_ATS_117 = 225
    FC_TCOLL_01_ATS_118 = 226
    FC_TCOLL_01_ATS_119 = 227
    FC_TCOLL_01_ATS_120 = 228
    FC_TCOLL_01_ATS_121 = 229
    FC_TCOLL_01_ATS_122 = 230
    FC_TCOLL_01_ATS_123 = 231
    FC_TCOLL_01_ATS_124 = 232
    FC_TCOLL_01_ATS_125 = 233
    FC_TCOLL_01_ATS_126 = 234
    FC_TCOLL_01_ATS_127 = 235
    FC_TCOLL_01_ATS_128 = 236
    FC_TCOLL_01_ATS_129 = 237
    FC_TCOLL_01_ATS_130 = 238
    FC_TCOLL_01_ATS_131 = 239
    FC_TCOLL_01_ATS_132 = 240
    FC_TCOLL_01_ATS_133 = 241
    FC_TCOLL_01_ATS_134 = 242
    FC_TCOLL_01_ATS_135 = 243
    FC_REQT_IS_01_ATS = 279
    FC_REQT_IS_02_ATS = 280
    FC_REQT_IS_03_ATS = 281
    FC_REQT_IS_04_ATS = 282
    FC_REQT_IS_05_ATS = 283
    FC_ISCOLL_01_ATS_21 = 284
    FC_ISCOLL_01_ATS_22 = 285
    FC_ISCOLL_01_ATS_23 = 286
    FC_ISCOLL_01_ATS_24 = 287
    FC_ISCOLL_01_ATS_25 = 288
    FC_ISCOLL_01_ATS_26 = 289
    FC_ISCOLL_01_ATS_27 = 290
    FC_ISCOLL_01_ATS_28 = 291
    FC_ISCOLL_01_ATS_29 = 292
    FC_ISCOLL_01_ATS_30 = 293
    FC_ISCOLL_01_ATS_31 = 294
    FC_ISCOLL_01_ATS_32 = 295
    FC_ISCOLL_01_ATS_33 = 296
    FC_ISCOLL_01_ATS_34 = 297
    FC_ISCOLL_01_ATS_35 = 298
    FC_ISCOLL_01_ATS_36 = 299
    FC_ISCOLL_01_ATS_37 = 300
    FC_ISCOLL_01_ATS_38 = 301
    FC_ISCOLL_01_ATS_39 = 302
    FC_ISCOLL_01_ATS_40 = 303
    FC_ISCOLL_01_ATS_41 = 304
    FC_ISCOLL_01_ATS_42 = 305
    FC_ISCOLL_01_ATS_43 = 306
    FC_ISCOLL_01_ATS_44 = 307
    FC_ISCOLL_01_ATS_45 = 308
    FC_ISCOLL_01_ATS_46 = 309
    FC_ISCOLL_01_ATS_47 = 310
    FC_ISCOLL_01_ATS_48 = 311
    FC_ISCOLL_01_ATS_49 = 312
    FC_ISCOLL_01_ATS_50 = 313
    FC_ISCOLL_01_ATS_51 = 314
    FC_ISCOLL_01_ATS_52 = 315
    FC_ISCOLL_01_ATS_53 = 316
    FC_ISCOLL_01_ATS_54 = 317
    FC_ISCOLL_01_ATS_55 = 318
    FC_ISCOLL_01_ATS_56 = 319
    FC_ISCOLL_01_ATS_57 = 320
    FC_ISCOLL_01_ATS_58 = 321
    FC_ISCOLL_01_ATS_59 = 322
    FC_ISCOLL_01_ATS_60 = 323
    FC_ISCOLL_01_ATS_61 = 324
    FC_ISCOLL_01_ATS_62 = 325
    FC_ISCOLL_01_ATS_63 = 326
    FC_ISCOLL_01_ATS_64 = 327
    FC_ISCOLL_01_ATS_65 = 328
    FC_ISCOLL_01_ATS_66 = 329
    FC_ISCOLL_01_ATS_67 = 330
    FC_ISCOLL_01_ATS_68 = 331
    FC_ISCOLL_01_ATS_69 = 332
    FC_ISCOLL_01_ATS_70 = 333
    FC_PSCOLL_01_ATS_21 = 335
    FC_PSCOLL_01_ATS_22 = 336
    FC_PSCOLL_01_ATS_23 = 337
    FC_PSCOLL_01_ATS_24 = 338
    FC_PSCOLL_01_ATS_25 = 339
    FC_PSCOLL_01_ATS_26 = 340
    FC_PSCOLL_01_ATS_27 = 341
    FC_PSCOLL_01_ATS_28 = 342
    FC_PSCOLL_01_ATS_29 = 343
    FC_PSCOLL_01_ATS_30 = 344
    FC_PSCOLL_01_ATS_31 = 345
    FC_PSCOLL_01_ATS_32 = 346
    FC_PSCOLL_01_ATS_33 = 347
    FC_PSCOLL_01_ATS_34 = 348
    FC_PSCOLL_01_ATS_35 = 349
    FC_PSCOLL_01_ATS_36 = 350
    FC_PSCOLL_01_ATS_37 = 351
    FC_PSCOLL_01_ATS_38 = 352
    FC_PSCOLL_01_ATS_39 = 353
    FC_PSCOLL_01_ATS_40 = 354
    FC_TXCOLL_01_ATS_01 = 355
    FC_TXCOLL_01_ATS_02 = 356
    FC_TXCOLL_01_ATS_03 = 357
    FC_TXCOLL_01_ATS_04 = 358
    FC_TXCOLL_01_ATS_05 = 359
    FC_REQT_TX_01_ATS = 360
    FC_REQ_COORD_RT_01_ATS = 361
    FC_RTTCOLL_01_ATS_01 = 362
    FC_RTTCOLL_01_ATS_02 = 363
    FC_RTTCOLL_01_ATS_03 = 364
    FC_RTTCOLL_01_ATS_04 = 365
    FC_RTTCOLL_01_ATS_05 = 366
    FC_RTTCOLL_01_ATS_06 = 367
    FC_RTTCOLL_01_ATS_07 = 368
    FC_RTTCOLL_01_ATS_08 = 369
    FC_RTTCOLL_01_ATS_09 = 370
    FC_RTTCOLL_01_ATS_10 = 371
    FC_RTTCOLL_01_ATS_11 = 372
    FC_RTTCOLL_01_ATS_12 = 373
    FC_RTTCOLL_01_ATS_13 = 374
    FC_RTTCOLL_01_ATS_14 = 375
    FC_RTTCOLL_01_ATS_15 = 376
    FC_RTTCOLL_01_ATS_16 = 377
    FC_RTTCOLL_01_ATS_17 = 378
    FC_RTTCOLL_01_ATS_18 = 379
    FC_RTTCOLL_01_ATS_19 = 380
    FC_RTTCOLL_01_ATS_20 = 381
    FC_RTTCOLL_01_ATS_21 = 382
    FC_RTTCOLL_01_ATS_22 = 383
    FC_RTTCOLL_01_ATS_23 = 384
    FC_RTTCOLL_01_ATS_24 = 385
    FC_RTTCOLL_01_ATS_25 = 386
    FC_RTTCOLL_01_ATS_26 = 387
    FC_RTTCOLL_01_ATS_27 = 388
    FC_RTTCOLL_01_ATS_28 = 389
    FC_RTTCOLL_01_ATS_29 = 390
    FC_RTTCOLL_01_ATS_30 = 391


    @classmethod
    def fromstring(cls, str):
      return getattr(cls, str.upper(), None)

    @classmethod
    def tostring(cls, val):
        for k, v in vars(cls).iteritems():
            if v==val:
                return k
