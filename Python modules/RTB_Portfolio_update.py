import acm

tradeSet = [50303046,
34132733,
33208448,
32112483,
29254896,
28479633,
28479504,
27155798,
25228023,
25049645,
23672223,
23542195,
23494521,
23269646,
23214701,
23152138,
22765188,
22448243,
21217352,
20735984,
20735917,
18936849,
16023205,
15881629,
15861878,
11987095,
10156248,
8612754,
8074424,
6563657,
6086630,
5682025,
5307322,
5307290,
5307255,
5041177,
5028296,
4954966,
4836971,
4800598,
4684240,
4683058,
4681983,
4639573,
4553105,
4553054,
4102729,
4102697,
4102684,
4102597,
4102581,
4102385,
4099188,
4099187,
4099186,
4098570,
4098509,
4098425,
4096415,
4096325,
4096253,
4095767,
4095710,
4095549,
4094390,
4094248,
4093908,
4093836,
4093757,
4093630,
4093573,
4093462,
4091603,
4091555,
4088509,
4088430,
4088154,
4087908,
4086677,
4086052,
4086018,
4085829,
4084181,
4084054,
4024134,
3802311,
3524794,
3038536,
2889269,
2643871,
2631168,
2370182,
1757085,
1682839,
1601877,
1601061,
1600887,
1596091,
1582864,
1582761,
1582736,
1582723,
1582707,
1582698,
1582685,
1582505,
1582332,
1582160,
1582140,
1582074,
1582041,
1582037,
1582025,
1582024,
1582013,
1581966,
1581956,
1581955,
1581925,
1581923,
1581887,
1581882,
1581842,
1581802,
1581796,
1581778,
1581741,
1581739,
1581714,
1581581,
1581579,
1581545,
1581541,
1581528,
1581515,
1581484,
1581389,
1581380,
1581365,
1581348]


for t in tradeSet:
    trd = acm.FTrade[t]
    print(trd)
    trd.Portfolio('Call_3012')
    trd.Commit()

