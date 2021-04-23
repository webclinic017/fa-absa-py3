import acm

trade_list = [107090365,
107090740,
107090714,
107090353,
107090125,
107090756,
107090806,
107090620,
107090095,
107090833,
107090474,
107090536,
107090057,
107090668,
107090910,
107090568,
107090798,
107090323,
107090059,
107090748,
107090538,
107090708,
107090510,
107090229,
107090395,
107090808,
107090049,
107090482,
107090207,
107090598,
107090650,
107090118,
107090622,
107090391,
107090516,
107090532,
107090494,
107090766,
107090524,
107090041,
107090189,
107090273,
107090802,
107090411,
107090556,
107090259,
107090219,
107090684,
107090682,
107090187,
107090680,
107090265,
107090357,
107090768,
107090405,
107090847,
107090858,
107090106,
107090209,
107090389,
107090592,
107090752,
107090123,
107090335,
107090821,
107090227,
107090750,
107090458,
107090860,
107090424,
107090686,
107090874,
107090614,
107090397,
107090243,
107090888,
107090758,
107090466,
107090108,
107090442,
107090734,
107090580,
107090085,
107090853,
107090702,
107090716,
107090612,
107090201,
107090470,
107090574,
107090658,
107090468,
107090035,
107090024,
107090317,
107090325,
107090347,
107090092,
107090359,
107090438,
107090902,
107090648,
107090074,
107090542,
107090413,
107090624,
107090381,
107090165,
107090045,
107090153,
107090403,
107090782,
107090128,
107090345,
107090498,
107090664,
107090464,
107090215,
107090205,
107090292,
107090837,
107090608,
107090646,
107090409,
107090704,
107090843,
107090247,
107090866,
107090778,
107090788,
107090173,
107090055,
107090436,
107090383,
107090026,
107090213,
107090878,
107090432,
107090817,
107090600,
107090819,
107090534,
107090590,
107090355,
107090991,
107090576,
107090217,
107090900,
107090987,
107090151,
107090138,
107090558,
107090914,
107090185,
107090662,
107090912,
107090810,
107090578,
107090872,
107090638,
107090080,
107090097,
107090020,
107090377,
107090929,
107090300,
107090283,
107090496,
107090660,
107090249,
107090071,
107090738,
107090815,
107090876,
107090827,
107090341,
107091018,
107090203,
107090588,
107090308,
107090179,
107090953,
107090285,
107090981,
107091026,
107090387,
107090890,
107090610,
107090476,
107090728,
107090949,
107090917,
107090163,
107090257,
107090566,
107090375,
107090315,
107090199,
107091075,
107091028,
107090602,
107090634,
107090418,
107090694,
107090329,
107090225,
107090361,
107090626,
107090570,
107090379,
107090726,
107090407,
107090812,
107090762,
107090746,
107090053,
107090969,
107090923,
107090385,
107090430,
107090862,
107090642,
107090177,
107091021,
107090508,
107090971,
107090514,
107091037,
107090933,
107090764,
107091024,
107090945,
107090644,
107090450,
107090975,
107090076,
107090171,
107091033,
107090931,
107090157,
107090961,
107090155,
107090478,
107090941,
107090640,
107090167,
107090233,
107090722,
107090416,
107090456,
107090921,
107090676,
107090460,
107090506,
107090904,
107090143,
107090434,
107090927,
107090069,
107090028,
107090935,
107090037,
107090484,
107090983,
107090870,
107090849,
107090083,
107090656,
107090159,
107090792,
107090652,
107090967,
107090321,
107090490,
107090337,
107090146,
107090369,
107090548,
107090851,
107090149,
107090239,
107090373,
107090688,
107090141,
107090253,
107090452,
107090636,
107090898,
107090732,
107090736,
107090263,
107090530,
107090880,
107090223,
107090100,
107090584,
107090951,
107090864,
107090102,
107090043,
107090112,
107090132,
107090526,
107090550,
107090393,
107090175,
107090331,
107090191,
107090298,
107090351,
107090985,
107091083,
107090251,
107090522,
107090520,
107090401,
107090296,
107090039,
107090065,
107090371,
107090261,
107090754,
107090560,
107090502,
107090319,
107090882,
107090528,
107090063,
107090349,
107090594,
107090446,
107090562,
107090939,
107091109,
107090237,
107090780,
107090892,
107090033,
107090884,
107090604,
107090800,
107090582,
107090776,
107090500,
107090989,
107090544,
107091030,
107090546,
107090606,
107090121,
107091073,
107091077,
107090959,
107090977,
107090428,
107090271,
107090796,
107090016,
107090275,
107090919,
107090269,
107090963,
107090078,
107090183,
107090462,
107090287,
107090115,
107090472,
107090710,
107090690,
107090488,
107090947,
107091015,
107090937,
107090504,
107090666,
107090973,
107090955,
107090894,
107090586,
107090343,
107090130,
107090339,
107090306,
107090618,
107090067,
107090448,
107090031,
107090700,
107090856,
107090993,
107091035,
107090696,
107091081,
107090628,
107090552,
107090706,
107090906,
107090104,
107090692,
107090564,
107090161,
107090420,
107090718,
107090279,
107090486,
107090290,
107090540,
107090399,
107090630,
107090195,
107090444,
107090698,
107090277,
107090678,
107090957,
107090596,
107090022,
107090440,
107090744,
107090193,
107090670,
107090136,
107090868,
107090480,
107090724,
107090943,
107090979,
107090786,
107090211,
107090925,
107090090,
107090294,
107090616,
107090965,
107090197,
107090281,
107090654,
107090231,
107090087,
107090760,
107090363,
107090610,
107090181,
107090804,
107090241,
107090169,
107090572,
107090742,
107090841,
107090712,
107090267,
107090823,
107090327,
107090554,
107090134,
107090512,
107090235,
107090774,
107090051,
107090632,
107090426,
107090720,
107090886,
107090672,
107090770,
107090730,
107090255,
107090784,
107090311,
107090908,
107090302,
107090794,
107090772,
107090221,
107090061,
107090674,
107090304,
107090313,
107090245,
107090845,
107090518,
107090492,
107090896,
107090454,
107090422,
107090333,
107090790,
107090018,
107090047,
107090367]

for trade in trade_list:

    t = acm.FTrade[trade]
    t.AdditionalInfo().CCPmiddleware_id(None)
    t.AdditionalInfo().CCPmiddleware_ptynb(None)
    t.AdditionalInfo().CCPmiddleware_versi(None)
    t.AdditionalInfo().CCPmwire_booking_st(None)
    t.AdditionalInfo().CCPmwire_contract_s(None)
    t.AdditionalInfo().CCPmwire_message_st(None)
    t.AdditionalInfo().CCPmwire_new_status(None)
    t.AdditionalInfo().CCPmwire_process_st(None)
    t.AdditionalInfo().CCPmwire_user_msg(None)
    t.AdditionalInfo().MW_TradeUpdated(None)
    t.Contract(None)
    t.Commit()
    print('===============================================')
    print(t.Oid())
    print(t.AdditionalInfo().CCPmiddleware_id())
    print(t.Contract())
    print('===============================================')