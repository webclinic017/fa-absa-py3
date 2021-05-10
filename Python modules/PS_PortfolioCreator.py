'''-----------------------------------------------------------------------------
Facilitates the creation of portfolios for newly onboarded clients.

This module also exposes functions that assemble images of portfolio trees
based on client configuration that can be used for other purposes than just
creating them in the DB.

HISTORY
================================================================================
Date       Change no        Developer          Description
--------------------------------------------------------------------------------
2018-10-02                  Tibor Reiss        Use transactions
2020-02-06 FAPE-205         Tibor Reiss        Fix bug in FA regarding selection
                                               of portfolio based on name
-----------------------------------------------------------------------------'''
import acm

from at_logging import getLogger
from PS_AssetClasses import CFD
from PS_Names import (get_top_coll_portfolio_name,
                      get_top_cr_portfolio_name,
                      get_portfolio_name_by_id,
                      get_portfolio_name)
from PS_Onboarding_RTM import (PF_PREFIX_ACS,
                               PF_PREFIX_BANK)

LOGGER = getLogger()

PF_RISK = "PB_RISK"
PF_CR_LIVE = "PB_CR_LIVE"
PF_PRIME_BROKING = "ACS RTM Prime - Prime Broking"
PF_FINANCING = "PB_FINANCING"
PF_PSWAP_CR = "PB_PSWAP_CR"
PF_NONCASHCOLL = "PB_CR_NONCASHCOLL"


class Portfolio(object):
    """A simple object representing a portfolio outside of ACM."""

    _acm_cls = None

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

    __repr__ = __str__

    @staticmethod
    def _setup_new_prf(acm_prf):
        """Class-specific portfolio setup."""
        raise NotImplementedError()

    def check_portfolio(self):
        temp_pf = acm.FPhysicalPortfolio.Select01("name='{}'".format(self._name), None)
        if not temp_pf:
            temp_pf = acm.FPhysicalPortfolio.Select01("assignInfo='{}'".format(self._name), None)
        return temp_pf

    def to_acm(self, no_create=False):
        """
        Cast the object to the appropriate ACM entity.

        This method first looks into the database if an entity with the same name
        exists, and if not, a new one is created. If "no_create" is set to True,
        the eventual creation of a new DB entity is skipped.

        """
        temp_pf = self.check_portfolio()
        if temp_pf or no_create:
            return temp_pf

        acm_prf = self._acm_cls()
        acm_prf.Name(self._name)
        acm_prf.AssignInfo(self._name)
        acm_prf.Currency('ZAR')
        acm_prf.PortfolioOwner('PRIME SERVICES DESK')
        if self._acm_cls == acm.FPhysicalPortfolio:
            self._setup_new_prf(acm_prf)
        return acm_prf

    def move_to_db(self):
        """Move the portfolio to the DB."""
        acm_prf = self.to_acm()
        if not self.check_portfolio() and acm_prf is not None:
            # New portfolio - commit
            LOGGER.info("Comitting new portfolio {}".format(self._name))
            acm_prf.Commit()

    def join_to_db(self, parent_pf_name=""):
        # The top_pf is always on the tree already so skip it
        if not parent_pf_name:
            return
        # Check if the same link already exists -> do nothing
        # Check if a different link already exists -> onboarding tool has to fail
        # to avoid reinstating graveyarded portfolios.
        # (Validation rule fv137 would kick in but clicking "yes" would still allow this!)
        create_link = True
        parent_pf = acm.FCompoundPortfolio[parent_pf_name]
        child_pf = self.to_acm()
        if not parent_pf or not child_pf:
            raise ValueError("One of the portfolios (%s %s) does not exist!" % (parent_pf_name, self))
        member_links = child_pf.MemberLinks()
        if member_links.Size() == 1:
            if member_links[0].OwnerPortfolio().Name() == parent_pf_name:
                create_link = False
            else:
                raise ValueError("Portfolio %s is already on the tree!" % self)
        elif member_links.Size() > 1:
            raise ValueError("Too many links for portfolio %s!" % self)
        if create_link:
            LOGGER.info("Creating link: parent = {} child = {}".format(parent_pf_name, self._name))
            plink = acm.FPortfolioLink()
            plink.MemberPortfolio(self.to_acm())
            plink.OwnerPortfolio(parent_pf)
            plink.Commit()

    def print_tree(self, print_prefix=''):
        """Nicely print the whole subtree."""
        LOGGER.info(print_prefix + ' ' + self._name)

    def get_all_subprfs(self):
        """Return all portfolios rooted at self."""
        return [self._name]

    @classmethod
    def is_compound(cls):
        return cls._acm_cls == acm.FCompoundPortfolio


class PhysicalPortfolio(Portfolio):
    _acm_cls = acm.FPhysicalPortfolio

    @staticmethod
    def _setup_new_prf(acm_prf):
        query = "list='PortfolioType' AND name='Held For Trading'"
        held_for_trading = acm.FChoiceList.Select01(query, None)
        acm_prf.TypeChlItem(held_for_trading)


class CompoundPortfolio(Portfolio):
    _acm_cls = acm.FCompoundPortfolio

    def __init__(self, name):
        super(CompoundPortfolio, self).__init__(name)
        self._children = set([])

    def add_child(self, portfolio):
        self._children.add(portfolio)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def remove_child(self, portfolio):
        if portfolio not in self._children:
            raise ValueError("%s not in %s's children" % (portfolio, self))
        self._children -= {portfolio}

    def move_to_db(self):
        """Move the portfolio, as well as all the children, to the DB."""
        super(CompoundPortfolio, self).move_to_db()
        for child in self._children:
            child.move_to_db()

    def join_to_db(self, parent_pf_name=""):
        super(CompoundPortfolio, self).join_to_db(parent_pf_name)
        for child in self._children:
            child.join_to_db(self._name)

    def print_tree(self, print_prefix=''):
        """Nicely print the whole subtree."""
        super(CompoundPortfolio, self).print_tree(print_prefix)
        for child in self._children:
            child.print_tree(print_prefix + '----')

    def get_all_subprfs(self):
        return [self._name] + sum([c.get_all_subprfs() for c in self._children], [])


class PortfolioMissingException(Exception):
    pass


def pf_tree_risk_bank_top(config, _):
    top_pf = CompoundPortfolio(PF_RISK)
    client_compound = CompoundPortfolio(get_portfolio_name_by_id("RISK_FV", config["shortName"]))
    top_pf.add_child(client_compound)
    return top_pf


def pf_tree_risk_bank(config, product_type):
    top_pf = None
    if product_type.risk or product_type.key in ("corpBonds", "bonds"):
        top_pf = CompoundPortfolio(PF_RISK)
        client_compound = CompoundPortfolio(get_portfolio_name_by_id("RISK_FV", config["shortName"]))
        top_pf.add_child(client_compound)
        client_compound.add_child(PhysicalPortfolio(get_portfolio_name(product_type, config["shortName"])))
        if product_type.portfolio_infix == "CFD":
            client_compound.add_child(PhysicalPortfolio(PF_PREFIX_BANK + config["cfdAccount"]))
    return top_pf


def pf_tree_risk_client(config, product_type):
    top_pf = None
    if product_type.risk:
        top_pf = CompoundPortfolio(PF_CR_LIVE)
        client_compound1 = CompoundPortfolio(get_top_cr_portfolio_name(config["shortName"]))
        top_pf.add_child(client_compound1)
        client_compound2 = CompoundPortfolio(get_portfolio_name_by_id("RISK", config["shortName"], cr=True))
        client_compound1.add_child(client_compound2)
        client_compound2.add_child(PhysicalPortfolio(get_portfolio_name(product_type, config["shortName"], cr=True)))
    return top_pf


def pf_tree_financed(config, product_type):
    top_pf = None
    if product_type.financed:
        top_pf = CompoundPortfolio(PF_CR_LIVE)
        client_compound1 = CompoundPortfolio(get_top_cr_portfolio_name(config["shortName"]))
        top_pf.add_child(client_compound1)
        client_compound2 = CompoundPortfolio(get_portfolio_name_by_id("AGENCY", config["shortName"], cr=True))
        client_compound1.add_child(client_compound2)
        client_compound3 = CompoundPortfolio(get_portfolio_name_by_id("FINANCED", config["shortName"], cr=True))
        client_compound2.add_child(client_compound3)
        client_compound3.add_child(PhysicalPortfolio(get_portfolio_name(product_type, config["shortName"], cr=True)))
    return top_pf


def pf_tree_fullyfunded(config, product_type):
    top_pf = None
    if product_type.fullyfunded:
        top_pf = CompoundPortfolio(PF_CR_LIVE)
        client_compound1 = CompoundPortfolio(get_top_cr_portfolio_name(config["shortName"]))
        top_pf.add_child(client_compound1)
        client_compound2 = CompoundPortfolio(get_portfolio_name_by_id("AGENCY", config["shortName"], cr=True))
        client_compound1.add_child(client_compound2)
        client_compound3 = CompoundPortfolio(get_portfolio_name_by_id("FULLYFUNDED", config["shortName"], cr=True))
        client_compound2.add_child(client_compound3)
        client_compound3.add_child(
            PhysicalPortfolio(get_portfolio_name(product_type, config["shortName"], cr=True, fullyfunded=True)))
    return top_pf


def pf_tree_cfd(config, product_type):
    top_pf = None
    if config[CFD.key] and product_type.portfolio_infix == "CFD":
        top_pf = CompoundPortfolio(PF_PRIME_BROKING)
        top_pf.add_child(PhysicalPortfolio(config["cfdAccount"]))
        top_pf.add_child(PhysicalPortfolio(PF_PREFIX_ACS + config["cfdAccount"]))
    return top_pf


def pf_tree_pbfinancing(config, _):
    top_pf = CompoundPortfolio(PF_FINANCING)
    client_compound = CompoundPortfolio("PB_" + config["shortName"] + "_FINANCING")
    top_pf.add_child(client_compound)
    children = [get_portfolio_name_by_id("CALLACCNT", config["shortName"]),
                get_portfolio_name_by_id("FINANCING", config["shortName"])]
    if config["sblAgreement"]:
        children.append(get_portfolio_name_by_id("SBL_FEE", config["shortName"]))
    for child in children:
        client_compound.add_child(PhysicalPortfolio(child))
    return top_pf


def pf_tree_calc(config, _):
    top_pf = CompoundPortfolio(PF_PSWAP_CR)
    top_pf.add_child(PhysicalPortfolio(get_portfolio_name_by_id("PSWAP", config["shortName"], cr=True)))
    return top_pf


def pf_tree_noncashcoll(config, _):
    top_pf = CompoundPortfolio(PF_NONCASHCOLL)
    client_compound = CompoundPortfolio(get_top_coll_portfolio_name(config["shortName"]))
    top_pf.add_child(client_compound)
    for i in ["A", "B", "C", "D", "E"]:
        infix = "CAT_" + i
        client_compound.add_child(PhysicalPortfolio(get_portfolio_name_by_id(infix, config["shortName"], cr=True)))
    return top_pf


func_product_specific = [pf_tree_risk_bank, pf_tree_risk_client,
                         pf_tree_financed, pf_tree_fullyfunded, pf_tree_cfd]
func_general = [pf_tree_pbfinancing, pf_tree_calc,
                pf_tree_noncashcoll, pf_tree_risk_bank_top]


def setup_portfolios(config, product_type):
    """
    Creating new portfolios and their corresponding
    portfolio links does not work in one transaction.
    """
    if product_type is None:
        func_list = func_general
    else:
        func_list = func_product_specific
    for f in func_list:
        top_pf = f(config, product_type)
        if top_pf:
            top_pf.print_tree()
            if not config["dryRun"]:
                # Unfortunately, can't commit addinfos here because some of the
                # functions in PS_AddInfos2 need a parent (or other dependencies)
                acm.BeginTransaction()
                try:
                    top_pf.move_to_db()
                    acm.CommitTransaction()
                except Exception as e:
                    acm.AbortTransaction()
                    LOGGER.exception("Could not commit portfolios")
                    raise e
                acm.PollDbEvents()
                acm.BeginTransaction()
                try:
                    top_pf.join_to_db("")
                    acm.CommitTransaction()
                except Exception as e:
                    acm.AbortTransaction()
                    LOGGER.exception("Could not create portfolio links")
                    raise e
