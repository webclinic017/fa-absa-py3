""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/delete/FDeletePackagesPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDeletePackagesPerform - Module to delete instrument/deal packages

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import ael

import FPackagesProcessingPerform
import importlib
importlib.reload(FPackagesProcessingPerform)
import FPackagesProcessingUtility as util
importlib.reload(util)
import FDeletePackagesHelper as delete_helper
importlib.reload(delete_helper)
import FBDPCommon
from FBDPCurrentContext import Summary

def perform(params):
    params['other_params'] = {
        'task': 'deleting',
        'archive_status': int(not params['NonArchived']),
        'action': Summary().DELETE,
    }
    FPackagesProcessingPerform.perform(params, DeletePackages)

class DeletePackages(FPackagesProcessingPerform.PackagesProcessingPerform):
    # override
    def _getFilteredPackage(self, pkg):
        ins_pkgs = pkg.ins_pkgs
        deal_pkgs = pkg.deal_pkgs
        pkg_type = util.getType(pkg.root)
        if pkg_type == util.Type.ins_pkg:
            ins_pkgs = [pkg.root] + ins_pkgs
        elif pkg_type == util.Type.deal_pkg:
            deal_pkgs = [pkg.root] + deal_pkgs
        else:
            raise Exception('Unknown package type specified')

        # collect entities for which it's ok to delete
        trades = pkg.trades
        instrs = self._getViableInstrs(pkg.instrs, ins_pkgs)
        ins_pkg_links = self._getViableInsPkgLinks(
            pkg.ins_pkg_links, ins_pkgs
        )
        deal_pkg_links = self._getViableDealPkgLinks(
            pkg.deal_pkg_links, deal_pkgs
        )
        trade_links = self._getViableDealPkgTradeLinks(
            pkg.trade_links, trades, deal_pkgs
        )
        ins_links = self._getViableDealPkgInsLinks(
            pkg.ins_links, instrs, ins_pkgs
        )

        # references to objects (type and oid) are used instead
        # of ael or acm objects representations to later permit
        # checking they've been deleted
        filtered_pkg = util.PackageWrapper(
            root=pkg.root,
            ins_pkgs=util.getMakeAelObjectParamsFromList(ins_pkgs),
            deal_pkgs=util.getMakeAelObjectParamsFromList(deal_pkgs),
            trades=util.getMakeAelObjectParamsFromList(trades),
            instrs=util.getMakeAelObjectParamsFromList(instrs),
            ins_pkg_links=util.getMakeAelObjectParamsFromList(ins_pkg_links),
            deal_pkg_links=util.getMakeAelObjectParamsFromList(
                deal_pkg_links
            ),
            trade_links=util.getMakeAelObjectParamsFromList(trade_links),
            ins_links=util.getMakeAelObjectParamsFromList(ins_links)
        )
        return filtered_pkg

    def _getPerformer(self, pkgs, perform_func):
        return delete_helper.get_deleter(
            owner=self, indentation='', objs=pkgs,
            objs_are_archived=int(self.source_archive_status),
            perform_func=perform_func
        )

    def _processPackage(self, pkg):
        # deal package need to be deleted before instrument package
        # due to dependencies
        trades = util.makeAelObjectFromListOfParams(pkg.trades)
        lead_trades, non_lead_trades = self.splitOnLead(trades)

        self._deleteAelObjs(pkg.trade_links)
        self._deleteAelObjs(
            util.getMakeAelObjectParamsFromList(non_lead_trades)
        )
        self._deleteAelObjs(pkg.ins_links)
        self._deleteAelObjs(pkg.instrs)
        self._deleteAelObjs(pkg.deal_pkg_links)
        self._deleteAelObjs(pkg.deal_pkgs)
        self._deleteAelObjs(
            util.getMakeAelObjectParamsFromList(lead_trades)
        )
        self._deleteAelObjs(pkg.ins_pkg_links)
        self._deleteAelObjs(pkg.ins_pkgs)

    # private
    def _getViableInstrs(self, instrs, ins_pkgs):
        # filter out instruments referenced by other instrument
        # packages not included in the current selection list
        ins_pkg_oids = ', '.join(str(util.getOid(pkg)) for pkg in ins_pkgs)

        def getOtherLinks(ins):
            query = (
                'SELECT DISTINCT dpil.seqnbr'
                ' FROM deal_package_ins_link as dpil'
                ' WHERE'
                ' (dpil.insaddr = %i)'
                ' AND'
                ' (dpil.ins_package_seqnbr NOT IN (%s))'
            ) % (util.getOid(ins), ins_pkg_oids)
            links = FBDPCommon.FBDPQuerySelection(
                name='Other deal package instrument links',
                query_expr=query,
                result_types=[ael.DealPackageInsLink]
            ).Run()
            return links

        viable_instrs = []
        for ins in instrs:
            links = getOtherLinks(ins)
            if len(links) == 0:
                viable_instrs.append(ins)

        return viable_instrs

    def _getViableInsPkgLinks(self, links, ins_pkgs):
        msg_prefix = 'parent and/or child instrument package'
        viable_links = []
        for link in links:
            self._appendViableLink(
                viable_links, link, msg_prefix, link.child_seqnbr,
                link.parent_seqnbr, ins_pkgs, ins_pkgs
            )

        return viable_links

    def _getViableDealPkgLinks(self, links, deal_pkgs):
        msg_prefix = 'parent and/or deal instrument package'
        viable_links = []
        for link in links:
            self._appendViableLink(
                viable_links, link, msg_prefix, link.child_deal_package_seqnbr,
                link.deal_package_seqnbr, deal_pkgs, deal_pkgs
            )

        return viable_links

    def _getViableDealPkgTradeLinks(self, links, trades, deal_pkgs):
        msg_prefix = 'trade and/or deal package'
        viable_links = []
        for link in links:
            self._appendViableLink(
                viable_links, link, msg_prefix, link.trdnbr,
                link.deal_package_seqnbr, trades, deal_pkgs
            )

        return viable_links

    def _getViableDealPkgInsLinks(self, links, instrs, ins_pkgs):
        msg_prefix = 'instrument and/or instrument package'
        viable_links = []
        for link in links:
            self._appendViableLink(
                viable_links, link, msg_prefix, link.insaddr,
                link.ins_package_seqnbr, instrs, ins_pkgs
            )

        return viable_links

    def _appendViableLink(
            self, list_to_append, link, msg_prefix,
            left, right, left_ref, right_ref
    ):
        # append only those links that have a null linked entity or has
        # a linked entity present in current selection list
        if (not (left or right)) or (left in left_ref) or (right in right_ref):
            list_to_append.append(link)
            return

        msg = '%s link reference exists but not selected for deletion' % \
            msg_prefix
        util.Log.logIgnore(link, msg, True)
        return

    def _deleteAelObjs(self, objs_params):
        objs = util.makeAelObjectFromListOfParams(objs_params)
        live_objs = [obj for obj in objs if obj.archive_status == 0]
        archived_objs = [obj for obj in objs if obj.archive_status == 1]
        for objs in (archived_objs, live_objs):
            if len(objs):
                archive_status = objs[0].archive_status
                msg = 'Acting on %sarchived %ss' % (
                    '' if archive_status else 'non-', util.getType(objs[0])
                )
                util.Log.log(msg, 'INFO', True)
                performer = delete_helper.get_deleter(
                    owner=self, indentation=util.INDENTATION * 2,
                    objs=objs, objs_are_archived=bool(archive_status)
                )
                performer.perform()

        return
