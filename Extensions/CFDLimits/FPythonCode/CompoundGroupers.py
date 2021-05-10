"""-----------------------------------------------------------------------
MODULE
    CompoundGroupers

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Selects the subportfolio one level down from the Compound Portfolio.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Sungard
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm

def subPrfLevel1(trade):
    portfolio = trade.Portfolio()
    member_links = portfolio.MemberLinks()
    if member_links.Size() >= 1:
        for pl in portfolio.MemberLinks():
                owner_portfolio = pl.OwnerPortfolio()
        return owner_portfolio
