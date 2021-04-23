""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/archive/FArchivePackagesPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FArchivePackagesPerform - Module to archive instrument/deal packages

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FPackagesProcessingPerform
import importlib
importlib.reload(FPackagesProcessingPerform)
import FPackagesProcessingUtility as util
importlib.reload(util)
import FArchivePackagesHelper as archive_helper
importlib.reload(archive_helper)
from FBDPCurrentContext import Summary

def perform(params):
    dearchive = bool(params['Dearchive'])
    # archive_status here corresponds to current value for the target object
    params['other_params'] = {
        'task': 'de-archiving' if dearchive else 'archiving',
        'archive_status': int(bool(dearchive)),
        'dearchive': dearchive,
        'action': Summary().DEARCHIVE if dearchive else Summary().ARCHIVE,
    }
    FPackagesProcessingPerform.perform(params, ArchivePackages)

class ArchivePackages(FPackagesProcessingPerform.PackagesProcessingPerform):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        super(ArchivePackages, self).__init__(
            testmode, baseParams, otherParams
        )
        self.viable_ins_pkgs = []

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

        # collect entities for which it's ok to (de-)archive
        ins_pkgs = self._getViablePkgs(ins_pkgs)
        deal_pkgs = self._getViablePkgs(deal_pkgs)
        trades = pkg.trades
        instrs = pkg.instrs
        ins_pkg_links = pkg.ins_pkg_links
        deal_pkg_links = pkg.deal_pkg_links
        trade_links = pkg.trade_links
        ins_links = pkg.ins_links

        # references to objects (type and oid) are used instead
        # of ael or acm objects representations as archiving caused
        # them to be removed from the cache and prevents subsequent
        # referencing with reading them back in
        filtered_pkg = util.PackageWrapper(
            root=pkg.root,
            ins_pkgs=self._getValidObjects(ins_pkgs),
            deal_pkgs=self._getValidObjects(deal_pkgs),
            trades=self._getValidObjects(trades),
            instrs=self._getValidObjects(instrs),
            ins_pkg_links=self._getValidObjects(ins_pkg_links),
            deal_pkg_links=self._getValidObjects(deal_pkg_links),
            trade_links=self._getValidObjects(trade_links),
            ins_links=self._getValidObjects(ins_links)
        )
        return filtered_pkg

    def _getPerformer(self, pkgs, perform_func):
        return archive_helper.get_archiver(
            owner=self, indentation='', objs=pkgs,
            archive=not bool(self.source_archive_status),
            perform_func=perform_func
        )

    def _processPackage(self, pkg):
        trades = util.makeAelObjectFromListOfParams(pkg.trades)
        lead_trades, non_lead_trades = self.splitOnLead(trades)

        self._archiveAelObjs(pkg.trade_links)
        self._archiveAelObjs(
            util.getMakeAelObjectParamsFromList(non_lead_trades)
        )
        self._archiveAelObjs(pkg.ins_links)
        self._archiveAelObjs(pkg.instrs)
        if self.source_archive_status == 0:
            # when archiving, always archive deal packages
            # before instrument packages, due to dependencies
            self._archiveAelObjs(pkg.deal_pkg_links)
            self._archiveAelObjs(pkg.deal_pkgs)
            self._archiveAelObjs(
                util.getMakeAelObjectParamsFromList(lead_trades)
            )
            self._archiveAelObjs(pkg.ins_links)
            self._archiveAelObjs(pkg.ins_pkg_links)
            self._archiveAelObjs(pkg.ins_pkgs)
        else:
            # when de-archiving, always archive instrument packages
            # before deal packages, due to dependencies
            self._archiveAelObjs(pkg.ins_pkg_links)
            self._archiveAelObjs(pkg.ins_pkgs)
            self._archiveAelObjs(
                util.getMakeAelObjectParamsFromList(lead_trades)
            )
            self._archiveAelObjs(pkg.deal_pkg_links)
            self._archiveAelObjs(pkg.deal_pkgs)

    # private
    def _getViablePkgs(self, pkgs):
        viable_pkgs = []
        for pkg in pkgs:
            if self._canOperateOnPkg(pkg):
                viable_pkgs.append(pkg)
                if util.isType(pkg, util.Type.ins_pkg):
                    self.viable_ins_pkgs.append(pkg.seqnbr)

        return viable_pkgs

    def _canOperateOnPkg(self, pkg):
        if self.source_archive_status == 1 and \
            util.isType(pkg, util.Type.deal_pkg):
            ins_pkg = pkg.ins_package_seqnbr
            if ins_pkg.archive_status == 1 and \
                ins_pkg.seqnbr not in self.viable_ins_pkgs:
                msg = '%s is required to be de-archived before operation' % (
                    util.getAelName(ins_pkg)
                )
                util.Log.logWarning(pkg, msg, True)
                return False

        return True

    def _getValidObjects(self, objs):
        # return only the objects that are not currently in the correct
        # archive status
        valid_objs = []
        for obj in objs:
            if obj.archive_status == self.source_archive_status:
                valid_objs.append(obj)
            else:
                msg = '%s archive_status = %i' % (
                    util.getAelName(obj), obj.archive_status
                )
                util.Log.logIgnore(obj, msg, True)

        return util.getMakeAelObjectParamsFromList(valid_objs)

    def _archiveAelObjs(self, objs_params):
        performer = archive_helper.get_archiver(
            owner=self, indentation=util.INDENTATION * 2,
            objs=util.makeAelObjectFromListOfParams(objs_params),
            archive=not bool(self.source_archive_status)
        )
        if performer:
            performer.perform()
