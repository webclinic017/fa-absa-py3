""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitCorporateActions/./etc/FMarkitLayout.py"
D1 =\
{
    'from' : [1, 3, 19, 31, 43, 45, 173, 301, 307, 313, 318, 320, 321, 322, 325, 327, 337, 339, 349, 351, 361, 363, 366, 368, 378, 380, 390, 392, 402, 404, 414, 416, 426, 428, 438, 440, 450, 452, 462, 464, 474, 476, 486, 488, 498, 500, 510, 512, 522, 524, 536, 546, 548, 558, 560, 570, 572, 582, 584, 594, 596, 606, 608, 618, 620, 630, 632, 644, 654, 656, 666, 668, 678, 680, 690, 692, 702, 704, 714, 716, 726, 728, 738, 740, 750, 752, 762, 764, 776, 786, 788, 798, 800, 812, 814, 844, 846, 856, 858, 868, 870, 873, 875, 885, 887, 897, 899, 902, 904, 914, 918, 920, 921, 923, 933, 935, 945, 947, 957, 959, 969, 971, 981, 983, 987, 1003, 1005, 1021, 1023, 1033, 1035, 1045, 1047, 1057, 1059, 1069, 1079, 1089, 1099, 1144, 1145, 1147, 1148, 1150, 1154, 1156, 1157, 1159, 1175, 1177, 1193, 1195, 1211, 1212, 1214, 1215, 1217, 1221, 1281, 1283, 1298, 1300, 1315, 1317, 1333, 1335, 1347, 1349, 1361, 1363, 1373, 1375, 1387, 1389, 1410, 1420, 1430, 1440, 1442, 1502, 1512, 1514, 1517, 1519, 1525, 1535, 1537, 1547, 1549, 1550, 1552, 1555, 1565, 1567, 1570, 1571, 1573, 1621, 1631, 1633, 1634, 1636, 1648, 1658, 1660, 1661, 1663, 1783, 1793, 1795, 1805, 1807, 1817, 1819, 1835, 1837, 1853, 1855, 1871, 1873, 1889, 1891, 1907, 1909, 1910, 1912, 1922, 1924, 1963, 1973, 1975, 2005, 2007, 2017, 2019, 2029, 2031, 2041, 2043, 2053, 2055, 2072, 2088, 2090, 2100, 2102, 2105, 2107, 2123, 2125, 2135, 2137, 2140, 2142, 2152, 2154, 2164, 2166, 2176, 2178, 2188, 2190, 2200, 2202, 2212, 2214, 2224, 2226, 2229, 2231, 2241, 2243, 2255, 2271, 2273, 2274, 2276, 2279, 2281, 2291, 2293, 2303, 2305, 2306, 2308, 2309, 2311, 2327, 2329, 2345, 2347, 2363, 2365, 2368, 2370, 2380, 2382, 2392, 2394, 2395, 2397, 2400, 2402, 2403, 2405, 2406, 2408, 2424, 2426, 2427, 2429, 2489, 2491, 2501, 2503, 2513, 2515, 2525, 2527, 2539, 2541, 2544, 2547, 2548, 2549, 2551, 2561, 2563, 2566, 2568, 2578, 2580, 2590, 2592, 2593, 2595, 2596, 2598, 2599, 2601, 2602, 2604, 2605, 2607, 2622, 2632, 2634, 2644, 2646, 2647, 2649, 2650, 2652, 2653, 2655, 2665, 2667, 2677, 2679, 2689, 2691, 2701, 2703, 2706, 2708, 2709, 2711, 2712, 2714, 2724, 2726, 2729, 2731, 2741, 2743, 2744, 2745, 2746, 2747, 2748, 2760, 2762, 2765, 2825, 2838, 2840],
    'to' : [2, 18, 30, 42, 44, 172, 300, 306, 312, 317, 319, 320, 321, 324, 326, 336, 338, 348, 350, 360, 362, 365, 367, 377, 379, 389, 391, 401, 403, 413, 415, 425, 427, 437, 439, 449, 451, 461, 463, 473, 475, 485, 487, 497, 499, 509, 511, 521, 523, 535, 545, 547, 557, 559, 569, 571, 581, 583, 593, 595, 605, 607, 617, 619, 629, 631, 643, 653, 655, 665, 667, 677, 679, 689, 691, 701, 703, 713, 715, 725, 727, 737, 739, 749, 751, 761, 763, 775, 785, 787, 797, 799, 811, 813, 843, 845, 855, 857, 867, 869, 872, 874, 884, 886, 896, 898, 901, 903, 913, 917, 919, 920, 922, 932, 934, 944, 946, 956, 958, 968, 970, 980, 982, 986, 1002, 1004, 1020, 1022, 1032, 1034, 1044, 1046, 1056, 1058, 1068, 1078, 1088, 1098, 1143, 1144, 1146, 1147, 1149, 1153, 1155, 1156, 1158, 1174, 1176, 1192, 1194, 1210, 1211, 1213, 1214, 1216, 1220, 1280, 1282, 1297, 1299, 1314, 1316, 1332, 1334, 1346, 1348, 1360, 1362, 1372, 1374, 1386, 1388, 1409, 1419, 1429, 1439, 1441, 1501, 1511, 1513, 1516, 1518, 1524, 1534, 1536, 1546, 1548, 1549, 1551, 1554, 1564, 1566, 1569, 1570, 1572, 1620, 1630, 1632, 1633, 1635, 1647, 1657, 1659, 1660, 1662, 1782, 1792, 1794, 1804, 1806, 1816, 1818, 1834, 1836, 1852, 1854, 1870, 1872, 1888, 1890, 1906, 1908, 1909, 1911, 1921, 1923, 1962, 1972, 1974, 2004, 2006, 2016, 2018, 2028, 2030, 2040, 2042, 2052, 2054, 2071, 2087, 2089, 2099, 2101, 2104, 2106, 2122, 2124, 2134, 2136, 2139, 2141, 2151, 2153, 2163, 2165, 2175, 2177, 2187, 2189, 2199, 2201, 2211, 2213, 2223, 2225, 2228, 2230, 2240, 2242, 2254, 2270, 2272, 2273, 2275, 2278, 2280, 2290, 2292, 2302, 2304, 2305, 2307, 2308, 2310, 2326, 2328, 2344, 2346, 2362, 2364, 2367, 2369, 2379, 2381, 2391, 2393, 2394, 2396, 2399, 2401, 2402, 2404, 2405, 2407, 2423, 2425, 2426, 2428, 2488, 2490, 2500, 2502, 2512, 2514, 2524, 2526, 2538, 2540, 2543, 2546, 2547, 2548, 2550, 2560, 2562, 2565, 2567, 2577, 2579, 2589, 2591, 2592, 2594, 2595, 2597, 2598, 2600, 2601, 2603, 2604, 2606, 2621, 2631, 2633, 2643, 2645, 2646, 2648, 2649, 2651, 2652, 2654, 2664, 2666, 2676, 2678, 2688, 2690, 2700, 2702, 2705, 2707, 2708, 2710, 2711, 2713, 2723, 2725, 2728, 2730, 2740, 2742, 2743, 2744, 2745, 2746, 2747, 2759, 2761, 2764, 2824, 2837, 2839, 2900],
    'name' : ["Record Type", "CA ID", "Customer Internal Code", "Identifying Security ID", "Identifying Security ID Type", "Issuer Description", "Issue Description", "CFI Code", "Corporate Action Type", "Sub-Event Type", "Sub-Event Type Field Status", "Reserved", "Voluntary/Mandatory Code", "Workflow Status", "Corporate Action Status", "Effective Date", "Effective Date Field Status", "Expiration Date", "Expiration Date Field Status", "Expiration Time", "Expiration Time Field Status", "Expiration Time Zone", "Expiration Time Zone Field Status", "Ex Date", "Ex Date Field Status", "Record Date", "Record Date Field Status", "Payable Date", "Payable Date Field Status", "Financial Year End Date", "Financial Year End Date Field Status", "Ballot Due Date", "Ballot Due Date Field Status", "Trading Begin Date", "Trading Begin Date Field Status", "Trading End Date", "Trading End Date Field Status", "Subscription Begin Date", "Subscription Begin Date Field Status", "Subscription End Date", "Subscription End Date Field Status", "Exclusion Date", "Exclusion Date Field Status", "Publication Date", "Publication Date Field Status", "Redemption Date", "Redemption Date Field Status", "Withdrawal Date", "Withdrawal Date Field Status", "Reserved", "Meeting Date", "Meeting Date Field Status", "Meeting Time", "Meeting Time Field Status", "Consent Expiration Date", "Consent Expiration Date Field Status", "Default Date", "Default Date Field Status", "Put Date", "Put Date Field Status", "Proof of Claim Filing Date", "Proof of Claim Filing Date Field Status", "Class Action Begin Date", "Class Action Begin Date Field Status", "Class Action End Date", "Class Action End Date Field Status", "Originating Security Identification", "Judgment Date", "Judgment Date Field Status", "Hearing Date", "Hearing Date Field Status", "Put Period Begin Date", "Put Period Begin Date Field Status", "Put Period End Date", "Put Period End Date Field Status", "Refunded Maturity Date", "Refunded Maturity Date Field Status", "Retainment Period Begin Date", "Retainment Period Begin Date Field Status", "Retainment Period End Date", "Retainment Period End Date Field Status", "DTC Expiration Date", "DTC Expiration Date Field Status", "DTC Swing Date", "DTC Swing Date Field Status", "DTC Withdrawal Date", "DTC Withdrawal Date Field Status", "Reserved", "DTC Protect Expiration Date", "DTC Protect Expiration Date Field Status", "DTC Cover Protect Expiration Date", "DTC Cover Protect Expiration Date Field Status", "Offeror ID", "Offeror ID Field Status", "Offeror Name", "Offeror Name Field Status", "Early Expiration Date", "Early Expiration Date Field Status", "Early Expiration Time", "Early Expiration Time Field Status", "Early Expiration Time Zone", "Early Expiration Time Zone Field Status", "Early Withdrawal Date", "Early Withdrawal Date Field Status", "Early Withdrawal Time", "Early Withdrawal Time Field Status", "Early Withdrawal Time Zone", "Early Withdrawal Time Zone Field Status", "Reserved", "Odd Lot Holding Maximum", "Odd Lot Holding Maximum Field Status", "Conditional", "Conditional Field Status", "Cash Amount Low", "Cash Amount Low Field Status", "Cash Amount High", "Cash Amount High Field Status", "Price Per Share Increment", "Price Per Share Increment Field Status", "Proration Rate", "Proration Rate Field Status", "Consent Solicitation Indicator", "Consent Solicitation Indicator Field Status", "Reserved", "Subscription Old Shares Qty", "Subscription Old Shares Qty Field Status", "Subscription New Shares Qty", "Subscription New Shares Qty Field Status", "Due Bill Off Date", "Due Bill Off Date Field Status", "Due Bill On Date", "Due Bill On Date Field Status", "Non Refunded Maturity Date", "Non Refunded Maturity Date Field Status", "Added Date", "Modified Date", "Modified Time", "Active Until Date", "Reserved", "Dissenters Rights", "Dissenters Rights Field Status", "Oversubscription Indicator", "Oversubscription Indicator Field Status", "Protect Period Days", "Protect Period Days Field Status", "Partial Code", "Partial Code Field Status", "Entitled Dividend", "Entitled Dividend Status", "Total Price", "Total Price Status", "COAF", "Fully Underwritten Flag", "Fully Underwritten Flag Status", "Entitled to Dividend Flag", "Entitled to Dividend Flag Status", "Reserved", "Meeting Site", "Meeting Site Field Status", "Previous Pay Factor", "Previous Pay Factor Field Status", "Current Pay Factor", "Current Pay Factor Field Status", "Coupon Rate", "Coupon Rate Field Status", "Realized Loss Rate", "Realized Loss Rate Field Status", "Deferred Interest Rate", "Deferred Interest Rate Field Status", "Maturity Date", "Maturity Date Field Status", "Interest Shortfall Rate", "Interest Shortfall Rate Field Status", "Reserved", "Match Date", "Approved Date", "Review By Date", "Not Supported Reason Code", "Reserved", "Price", "Price Field Status", "Price Currency", "Price Currency Field Status", "Reserved", "New Par Value", "New Par Value Field Status", "Old Par Value", "Old Par Value Field Status", "Cancelled", "Cancelled Field Status", "Reserved", "Declaration Date (No Longer Used)", "Declaration Date Field Status (No Longer Used)", "Reserved", "Domicile Restrict Flag", "Domicile Restrict Flag Field Status", "Reserved", "Filing Date", "Filing Date Field Status", "Final Payment Flag", "Final Payment Flag Field Status", "Reserved", "New Security Dealing Date", "New Security Dealing Date Field Status", "Rights Trading Indicator", "Rights Trading Indicator Field Status", "Reserved", "Last Day for Split Full Paid Rights", "Last Day for Split Full Paid Rights Field Status", "Last Day for Split Nil Paid Rights", "Last Day for Split Nil Paid Rights Field Status", "Lottery Date", "Lottery Date Field Status", "Lottery Denomination Rate", "Lottery Denomination Rate Field Status", "Maximum Quantity Sought", "Maximum Quantity Sought Field Status", "Minimum Denomination", "Minimum Denomination Field", "Minimum Exercise Quantity", "Minimum Exercise Quantity Field Status", "Minimum Quantity Sought", "Minimum Quantity Sought Field Status", "Must all shares be submitted?", "Must all shares be submitted? Field Status", "Objection Date", "Objection Date Field Status", "Reserved", "SEC Registered", "SEC Registered Field Status", "Total # of Shares to Offer", "Total # of Shares to Offer Field Status", "Consent Protect Expiration Date (For Future Use)", "Consent Protect Expiration Date Field Status (For Future Use)", "Cover Protect Expiration Date", "Cover Protect Expiration Date Field Status", "DTC Consent Expiration Date", "DTC Consent Expiration Date Field Status", "Dividend Ranking Date", "Dividend Ranking Date Field Status", "Reserved", "Oversubscription Percentage", "Oversubscription Percentage Field Status", "Oversubscription Price", "Oversubscription Price Field Status", "Oversubscription Price Currency", "Oversubscription Price Currency Field Status", "Oversubscription Proration Rate", "Oversubscription Proration Rate Field Status", "Protect Expiration Date", "Protect Expiration Date Field Status", "Accrual Days Count", "Accrual Days Count Field Status", "Arrears Pay Begin Date", "Arrears Pay Begin Date Field Status", "Arrears Pay End Date", "Arrears Pay End Date Field Status", "Cover Consent Expiration Date (For Future Use)", "Cover Consent Expiration Date Field Status (For Future Use)", "DTC Consent Protect Expiration Date (For Future Use)", "DTC Consent Protect Expiration Date Field Status (For Future Use)", "DTC Cover Consent Expiration Date (For Future Use)", "DTC Cover Consent Expiration Date Field Status (For Future Use)", "Exercise Period Begin Date", "Exercise Period Begin Date Field Status", "Announcement Date", "Announcement Date Field Status", "Payment Frequency", "Payment Frequency Field Status", "Proration Date (For Future Use)", "Proration Date Field Status (For Future Use)", "Reserved", "Event Cash Value", "Event Cash Value Field Status", "Conditional Payment Code", "Conditional Payment Code Field Status", "Event Cash Value Currency", "Event Cash Value Currency Field Status", "Delisting Date", "Delisting Date Field Status", "Old Shares Dividend Ranking Date", "Old Shares Dividend Ranking Date Fields Status", "Due Bill Indicator", "Due Bill Indicator Field Status", "Foreign Source Indicator", "Foreign Source Indicator Field Status", "Minimum Oversubscripton Lot Quantity", "Minimum Oversubscripton Lot Quantity Field Status", "Minimum Quantity to Be Retained", "Minimum Quantity to Be Retained Field Status", "New Interest Rate", "New Interest Rate Field Status", "New Par Value Currency", "New Par Value Currency Field Status", "New Share Dispatched Date (For Future Use)", "New Share Dispatched Date Field Status (For Future Use)", "Next Put Date", "Next Put Date Field Status", "NRA Indicator", "NRA Indicator Field Status", "Old Par Value Currency", "Old Par Value Currency Field Status", "Proration Indicator", "Proration Indicator Field Status", "Tax Reportable Indicator", "Tax Reportable Indicator Field Status", "Number of Shares to be Issued", "Number of Shares to be Issued Field Status", "Step-Up Privilege", "Step-Up Privilege Field Status", "Surviving Company", "Surviving Company Field Status", "Trading Ends for Old Shares (For Future Use)", "Trading Ends for Old Shares Field Status (For Future Use)", "Type of Distribution", "Type of Distribution Field Status", "Unconditional Date", "Unconditional Date Field Status", "Security ID", "Security ID Type", "Country of Issue", "LSE Source Code", "Primary Exchange Flag", "Conditional Deposit Indicator (For Future Use)", "Conditional Deposit Indicator Field Status (For Future Use)", "Consent Expiration Time", "Consent Expiration Time Field Status", "Consent Expiration Time Zone", "Consent Expiration Time Zone Field Status", "Date To Purchase Shares (For Future Use)", "Date To Purchase Shares Field Status (For Future Use)", "Date To Sell Shares (For Future Use)", "Date To Sell Shares Field Status (For Future Use)", "Fall Into Odd Lot Indicator (For Future Use)", "Fall Into Odd Lot Indicator Field Status (For Future Use)", "Final Exercise Indicator", "Final Exercise Indicator Field Status", "Increase On Shares Indicator", "Increase On Shares Indicator Field Status", "Odd Lot Proration Indicator (For Future Use)", "Odd Lot Proration Indicator Field Status (For Future Use)", "Preliminary Rate Flag", "Preliminary Rate Flag Field Status", "Reserved", "Stock Merged Date W/I (SD)", "Stock Merged Date W/I (SD) Field Status", "Stock Merged Date W/I (TD)", "Stock Merged Date W/I (TD) Field Status", "Subscription Basis Indicator (For Future Use)", "Subscription Basis Indicator Field Status (For Future Use)", "Surrender Shares Indicator", "Surrender Shares Indicator Field Status", "W/I Applicable Trade Indicator", "W/I Applicable Trade Indicator Field Status", "W/I Settlement Date", "W/I Settlement Date Field Status", "W/I Trade End Date", "W/I Trade End Date Field Status", "W/I Trade Start Date", "W/I Trade Start Date Field Status", "Withdrawal Time", "Withdrawal Time Field Status", "Withdrawal Time Zone", "Withdrawal Time Zone Field Status", "Payout Option Available", "Payout Option Available Field Status", "Currency Option Available", "Currency Option Available Field Status", "DTC Expiration Time", "DTC Expiration Time Field Status", "DTC Expiration Time Zone (For Future Use)", "DTC Expiration Time Zone Field Status (For Future Use)", "Final Date To Dissent", "Final Date To Dissent Field Status", "Text Changed Indicator", "Critical Field Changed Indicator", "Required Field Changed Indicator", "Optional Field Changed Indicator", "Payout Changed Indicator", "SOI Matching Security Id", "SOI Matching Security Id Type", "Country Of Issuer", "Offeror Full Name", "Rate Calculation Method Type", "Rate Calculation Method Type Field Status", "Reserved"]
}

D2 =\
{
    'from' : [1, 3, 19, 21, 24, 36, 291, 292, 296, 297, 298, 308, 310, 320, 322],
    'to' : [2, 18, 20, 23, 35, 290, 291, 295, 296, 297, 307, 309, 319, 321, 2900],
    'name' : ["Record Type", "CA ID", "Option Status", "Option Number", "Contra-CUSIP Code", "Option Text", "Default Option Indicator", "Option Action", "Option Action Change Indicator", "Option Text Changed Indicator", "Conversion Suspension Start Date", "Conversion Suspension Start Date Status", "Conversion Suspension End Date", "Conversion Suspension End Date Status", "Reserved"]
}

D3 =\
{
    'from' : [1, 3, 19, 21, 24, 26, 28, 30, 42, 48, 70, 92, 114, 136, 139, 141, 163, 166, 188, 191, 213, 235, 257, 260, 272, 274, 296, 297, 298, 300, 312, 313, 316, 444, 572, 573, 576, 876, 877, 893, 903, 904, 926, 1226, 1248, 1249, 1271, 1283, 1285, 1307, 1329, 1351],
    'to' : [2, 18, 20, 23, 25, 27, 29, 41, 47, 69, 91, 113, 135, 138, 140, 162, 165, 187, 190, 212, 234, 256, 259, 271, 273, 295, 296, 297, 299, 311, 312, 315, 443, 571, 572, 575, 875, 876, 892, 902, 903, 925, 1225, 1247, 1248, 1270, 1282, 1284, 1306, 1328, 1350, 2900],
    'name' : ["Record Type", "CA ID", "Payout Status", "Option Number", "Payout Number", "Payout Type", "Payout Security ID Type", "Payout Security ID", "CFI Code", "Payout Rate", "Payout Amount", "Payout Net Amount", "Payout Gross Amount", "Currency Code", "Fractional Share Rule", "Price", "Price Currency", "Cash-in-lieu", "Cash-in-lieu Currency", "Old Shares", "New Shares", "Fee", "Fee Currency", "Payout Security Id", "Payout Security Id Type", "Withholding Tax Rate", "Payout Changed Indicator", "Payout Type Changed Indicator", "Payout SOI Match Security Id Type", "Payout SOI Match Security ID", "Estimated Rate Flag", "Country of Issue", "Issuer Description", "Issue Description", "SOI Indicator", "Country of Issuer", "Reserved", "New Payout Security Flag", "Conversion Rate", "Conversion Rate Date", "Refunded/non-refunded flag", "Withholding of Foreign Tax", "Reserved", "DTC Currency Conversion Rate", "DTC Contra CUSIP Flag", "DTC Cash in Lieu Price", "DTC Disbursed Security ID", "DTC Disbursed Security ID Type", "DTC Fee Rate", "DTC Security Rate", "DTC Cash Rate", "Reserved"]
}