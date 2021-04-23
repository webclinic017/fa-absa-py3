"""
Description: 
    Bulk update of assign info to new portfolios so that XTP trades feed
    correctly once we go live with RTM.

Project:     Risk Transfer Mechanism
Developer:   Bhavik Mistry / Jakub Tomaga
Date:        06/12/2017
"""


import acm


ports = [['40659', '40659_Syndicate trades', 'ACS RTM - 40659_Syndicate trades'],
['40147', '40147', 'ACS RTM - 40147'],
['40188', '40188', 'ACS RTM - 40188'],
['40196', '40196', 'ACS RTM - 40196'],
['40238', '40238', 'ACS RTM - 40238'],
['40246', '40246', 'ACS RTM - 40246'],
['40428', '40428', 'ACS RTM - 40428'],
['40436', '40436', 'ACS RTM - 40436'],
['41012', '41012', 'ACS RTM - 41012'],
['41038', '41038', 'ACS RTM - 41038'],
['60574', '60574', 'ACS RTM - 60574'],
['40238_CFD_ZERO', '40238_CFD_ZERO', 'ACS RTM - 40238_CFD_ZERO'],
['45005', '45005', 'ACS RTM - 45005'],
['45039', '45039', 'ACS RTM - 45039'],
['45088', '45088 MSCI', 'ACS RTM - 45088 MSCI'],
['45112', '45112 USD Breakable SS', 'ACS RTM - 45112'],
['45146', '45146 ZAR Breakable SS', 'ACS RTM - 45146'],
['45153', '45153 SSF1', 'ACS RTM - 45153 SSF1'],
['45161', '45161 SSF2', 'ACS RTM - 45161 SSF2'],
['45195', '45195 Bespoke Structures', 'ACS RTM - 45195'],
['45070', 'Delta One 2 45070', 'ACS RTM - 45070'],
['40592', '40592', 'ACS RTM - 40592'],
['41020', '41020', 'ACS RTM - 41020'],
['41046', '41046', 'ACS RTM - 41046'],
['41053', '41053', 'ACS RTM - 41053'],
['41079', '41079_RAFRES', 'ACS RTM - RES'],
['41087', '41087_RAFIND', 'ACS RTM - IND'],
['41095', '41095_RAFFIN', 'ACS RTM - FIN'],
['41129', 'Mapps Growth 41129', 'ACS RTM - Growth'],
['41137', 'Mapps Protector 41137', 'ACS RTM - Protect'],
['41269', 'NewFunds Equity Momentum ETF', 'ACS RTM - Mom'],
['41244', 'NewFunds GOVI ETF', 'ACS RTM - GOVI'],
['41251', 'NewFunds ILBI ETF', 'ACS RTM - ILBI'],
['41236', 'NewFunds SWIX 40 ETF', 'ACS RTM - SWIX'],
['41277', 'NewFunds Tradable Money Market Index ET', 'ACS RTM - Mmark'],
['43083', '43083', 'ACS RTM - 43083'],
['43067', '43067 EQ_SA_Pairs', 'ACS RTM - 43067'],
['46094', '46094 Delta Hedge Exotics', 'ACS RTM - 46094'],
['42002', '42002', 'ACS RTM - 42002'],
['42010', '42010 Straddles', 'ACS RTM - 42010'],
['42036', '42036 Single Stock Hedge', 'ACS RTM - 42036'],
['48363', '48363 Index Flow', 'ACS RTM - 48363'],
['44040', '44040 - Oasis', 'ACS RTM ST - Islamic Structures'],
['44032', '44032 - LEIPs', 'ACS RTM ST - LEIPs Structures'],
['43117', '43117 EQ_SA_PairsOption', 'ACS RTM - 43117'],
['44081', '44081', 'ACS RTM ST - NVL Risk'],
['41111', '41111', 'ACS RTM - 41111'],
['40584', '40584', 'ACS RTM - 40584'],
['40865', '40865', 'ACS RTM - 40865'],
['41210', '41210', 'ACS RTM - 41210'],
['46003', '46003', 'ACS RTM - 46003'],
['46029', '46029', 'ACS RTM - 46029'],
['46078', '46078', 'ACS RTM - 46078'],
['46128', '46128', 'ACS RTM - 46128'],
['47373', '47373', 'ACS RTM - 47373'],
['46037', '46037 EQ_SS_Directional', 'ACS RTM - 46037'],
['46052', '46052 Book Build', 'ACS RTM - 46052'],
['46136', '46136', 'ACS RTM - 46136'],
['47258', '47258', 'ACS RTM - 47258'],
['40121', '40121 CFD Misdeals', 'ACS RTM - 40121 CFD Misdeals'],
['42945', '42945 CFD Misdeals', 'ACS RTM - 42945 CFD Misdeals'],
['47274_CFD_Funding', '47274_CFD_Funding', 'ACS RTM - 47274_CFD_Funding'],
['47423', 'Exotics', 'ACS RTM - Exotics'],
['47449', 'Corporate/Hedge', 'ACS RTM - Corporate/Hedge'],
['47431', 'Vanilla', 'ACS RTM - Vanilla']]


for p in ports:
    old_port = acm.FPhysicalPortfolio[p[1]]
    new_port = acm.FPhysicalPortfolio[p[2]]
    if old_port is not None and new_port is not None:
        try:
            print "Current AssingInfo on {0} is {1}".format(p[1], old_port.AssignInfo())
            old_port.AssignInfo(old_port.AssignInfo() + '_OLD')
            old_port.Commit()
            print "New AssingInfo on {0} is {1}".format(p[1], old_port.AssignInfo())

            new_port.AssignInfo(p[0])
            new_port.Commit()
            print "AssignInfo for {0} set to {1}".format(p[2], p[0])
        except Exception as e:
            print 'Failed to Update Portfolio %s due to error %s!'%(p[2], e)
    else:
        print 'Both portfolios do not exist skipping' + str(p)

print 'Update complete'
