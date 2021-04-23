"""
Description: 
    Move all Prime Broking Stock porfolios under the new compound portfolio
    ACS RTM Prime - Prime Broking once we go live with RTM.

Project:     Risk Transfer Mechanism
Developer:   Jakub Tomaga
Date:        06/12/2017
"""


import time
import acm

portfolio_list = [
    "40675",
    "41293",
    "60012",
    "60046",
    "60103",
    "47316",
    "60137_Div_Arb",
    "60129",
    "60129_Div_Arb",
    "60129_Ca_Merger",
    "60129_EqPairs_ST",
    "60129_EquityDriven",
    "60129_L/SGen",
    "60129_LongOnly",
    "60129_ShortOnly",
    "60129_EqPairs_LT",
    "60137",
    "60137_CAMerger",
    "60137_EqPairs_ST",
    "60137_EquityDriven",
    "60137_L/SGen",
    "60137_LongOnly",
    "60137_ShortOnly",
    "60137_EqPairs_LT",
    "48389",
    "48405",
    "48413",
    "44297",
    "44313",
    "48694",
    "48447",
    "60616",
    "60392",
    "60798",
    "60491",
    "60673",
    "60681",
    "60632",
    "60822",
    "60400",
    "60434",
    "60509",
    "60517",
    "60533",
    "60541",
    "60566",
    "60590",
    "60608",
    "60657",
    "60715",
    "60723",
    "60731",
    "60749",
    "60772",
    "60780",
    "60806",
    "60814",
    "60830",
    "60848",
    "60863",
    "60889",
    "60905",
    "60913",
    "60947",
    "60954",
    "60962",
    "60970",
    "60996",
    "61010",
    "61028",
    "61036",
    "61044",
    "61077",
    "47308",
    "47324",
    "47340",
    "47357",
    "47365",
    "60939",
    "61051",
    "61069",
    "40923",
    "40931",
    "41350",
    "47332",
    "47464",
    "61093",
    "61101",
    "61127",
    "48645"
]

start = time.time()
owner_portfolio = acm.FPhysicalPortfolio["ACS RTM Prime - Prime Broking"]
for name in portfolio_list:
    portfolio = acm.FPhysicalPortfolio[name]
    print("Deleting links for: {0}".format(name))
    for link in portfolio.MemberLinks():
        link.Delete()
    print("Linking portfolio to new compound: {0}".format(owner_portfolio.Name()))
    port_link = acm.FPortfolioLink()
    port_link.MemberPortfolio(portfolio.Name())
    port_link.OwnerPortfolio(owner_portfolio)
    port_link.Commit()
end = time.time()
print("Completed successfully in {0} seconds.".format(end - start))
