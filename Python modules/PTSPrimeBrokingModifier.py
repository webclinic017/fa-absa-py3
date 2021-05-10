"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PTSPrimeBrokingModifier

DESCRIPTION
    This module is used to get prime broking clients from their corresponding portfolio

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-11-21     FAOPS-586       Stuart Wilson           Capital Markets         Initial implementation
2019-12-10     FAOPS-697       Stuart Wilson           Markets IT              Performance improvement
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from logging import getLogger

LOGGER = getLogger('Prime Broking PTS modification')


class PTSPrimeBrokingModifier:
    def __init__(self):
        self.pb_portfolio_linked_parties = dict()
        self.pb_reporting_prf = acm.FAdditionalInfoSpec['PB_Reporting_Prf']

    def get_parent_portfolio(self, portfolio):
        links = portfolio.MemberLinks()
        if links.IsEmpty():
            LOGGER.debug('returning none in get parent')
            return None
        else:
            if links[0].OwnerPortfolio() is None:
                return None
            else:
                LOGGER.debug('returning parent portfolio {name}'.format(name=links[0].OwnerPortfolio().Name()))
                return links[0].OwnerPortfolio()

    def get_cp_from_pb_trade_portfolio(self, trade_portfolio):
        """
        Gets the corresponding Prime Broking counterparty associated with the portfolio
        on the trade
        """
        top_node = acm.FPhysicalPortfolio['PB_CR_LIVE']
        prev_parent = trade_portfolio
        parent = self.get_parent_portfolio(trade_portfolio)

        while parent != top_node:
            prev_parent = parent
            parent = self.get_parent_portfolio(prev_parent)
            if parent is None:
                LOGGER.exception("No party linked to trade portfolio for Prime Broking")
                return None
        if prev_parent:
            prev_parent_name = prev_parent.Name()
            if prev_parent_name in self.pb_portfolio_linked_parties:
                return self.pb_portfolio_linked_parties[prev_parent_name]
            else:
                return self.get_pb_portfolio_linked_party(prev_parent)

    def get_pb_portfolio_linked_party(self, trade_portfolio):
        """
        Returns a party that have the addinfo 'PB_Reporting_Prf' populated relating to a prime broking portfolio
        """
        for addinf in self.pb_reporting_prf.AddInf().AsArray():
            parent_addinfo = addinf.Parent()
            addinf_fieldvalue = addinf.FieldValue()
            if addinf_fieldvalue == trade_portfolio.Name():
                self.pb_portfolio_linked_parties[addinf_fieldvalue] = parent_addinfo
                return addinf.Parent()

