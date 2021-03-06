import acm

'''
coded by Anil Parbhoo
10 Oct 2017
CHNG0005021776
PLD defnbrs are obtained from the asql below

select
pld.defnbr,
i.insid,
i.instype,
pld.errmsg,
pld.not_active,
c.insid'curr',
 pld.updat_time,
 pd.disid'distributor',
 pld.idp_code,
 cl2.entry'semantic',
 cl.entry'Service',
 pa.ptyid'Party'

from PriceLinkDefinition pld, 
pricedistributor pd,
 choicelist cl,
 choicelist cl2,
 party pa,
 instrument i,
 instrument c


where 
 pld.disnbr = pd.disnbr

and pld.service = cl.seqnbr
and cl.list = 'PriceServices'
and pld.semantic = cl2.seqnbr
and cl2.list = 'PriceSemantics'
and pld.source_ptynbr = pa.ptynbr
and pld.curr = c.insaddr
and pld.insaddr = i.insaddr
and pld.errmsg ~= ''
and i.instype not in ('Curr', 'RateIndex')

order by i.instype

'''


ml = [23,
24,
114,
115,
160,
161,
183,
184,
185,
186,
326,
327,
345,
346,
353,
354,
360,
361,
409,
410,
486,
487,
488,
489,
490,
491,
492,
493,
504,
505,
518,
519,
544,
545,
580,
581,
590,
591,
598,
599,
602,
603,
619,
620,
631,
632,
635,
636,
693,
694,
697,
698,
707,
708,
720,
721,
725,
726,
727,
728,
731,
732,
741,
742,
758,
759,
760,
761,
796,
797,
822,
823,
834,
835,
838,
839,
901,
902,
903,
904,
923,
924,
980,
981,
987,
988,
989,
990,
991,
992,
997,
998,
999,
1000,
1031,
1032,
1033,
1034,
1046,
1047,
1051,
1052,
1083,
1084,
1120,
1121,
1142,
1143,
1145,
1146,
1153,
1154,
1179,
1180,
1186,
1210,
1211,
1224,
1225,
1252,
1350,
1351,
1540,
1541,
1660,
1661,
1664,
1665,
1666,
1667,
2040,
2041,
2060,
2061,
2079,
2080,
2085,
2086,
2180,
2181,
2208,
2209,
2265,
2266,
2271,
2272,
2274,
2275,
2330,
2331,
2342,
2343,
2344,
2345,
2346,
2347,
2348,
2349,
2350,
2351,
2354,
2355,
2603,
2604,
2608,
2609,
2621,
2622,
2690,
2691,
2734,
2735,
2786,
2787,
2815,
2848,
2849,
2865,
2866,
2879,
2880,
2904,
2905,
2936,
2937,
3040,
3041,
3082,
3083,
3101,
3102,
3109,
3110,
3150,
3151,
3199,
3200,
3233,
3234,
3392,
3393,
3394,
3395,
3409,
3410,
3447,
3448,
3449,
3450,
3464,
3472,
3497,
3505,
3506,
3526,
3527,
3574,
3575,
3619,
3620,
3624,
3746,
3747,
3748,
3749,
3760,
3761,
4100,
4101,
4109,
4110,
4166,
4167,
4170,
4171,
4172,
4173,
4177,
4178,
4179,
4180,
4183,
4184,
4205,
4207,
4208,
4210,
4216,
4217,
4218,
4219,
4242,
4243,
4269,
4270,
4433,
4545,
4546,
4547,
4548,
4553,
4554,
4559,
4560,
4569,
4570,
4571,
4587,
4590,
4591,
4600,
4601,
4613,
4614,
4637,
4642,
4681,
4691,
4704,
4705,
4727,
4728,
4747,
4748,
4761,
4762,
4770,
4771,
4772,
4773,
4283,
4294,
4496,
4506,
4509,
4557,
4558,
4568,
4602,
4605,
4606,
4633,
4634,
4680,
4756,
4758,
1689,
55,
274,
942,
943,
944,
945,
946,
947,
948,
746,
747,
888,
889,
890,
891,
958,
1401,
1402,
2844,
2845,
2188,
2189,
2190,
2191,
2192,
2193,
2194,
2195,
2196,
2197,
2200,
2201,
2202,
2203,
2240,
2241,
2242,
2243,
2244,
2245,
2246,
2247,
2248,
2249,
2250,
2251,
2252,
2253,
2254,
2255,
2256,
2257,
2258,
2259,
2264,
2316,
2317,
2318,
2358,
2359,
2360,
2361,
2369,
2370,
2371,
2372,
2380,
2381,
2382,
2383,
2384,
2385,
2386,
2387,
2388,
2389,
2390,
2391,
2416,
2417,
2431,
2432,
2444,
2595,
2639,
2640,
2643,
2644,
2645,
2646,
2647,
2648,
2650,
2651,
2652,
2653,
2654,
2655,
2664,
2665,
2672,
2673,
2675,
972,
973,
974,
975,
976,
977,
978,
1557,
1558,
3968,
3970,
3971,
1659,
3136,
2119,
2121,
2523,
2524,
4277,
4278,
4669,
4670
]

for i in ml:
    pld = acm.FPriceLinkDefinition[i]
    if pld.ErrorMessage():
        if pld.Instrument().InsType() not in ['Curr', 'RateIndex']:
            try:
                pld.NotActive('True')
                pld.Commit()
                print pld.NotActive(), pld.Instrument().InsType(), pld.Oid(), pld.ErrorMessage() 
            except:
                print pld.Oid(), 'was NOT updated'
            

