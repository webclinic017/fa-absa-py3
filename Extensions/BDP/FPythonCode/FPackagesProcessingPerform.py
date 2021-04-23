""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/etc/FPackagesProcessingPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPackagesProcessingPerform - Instrument/deal packages perform impl base

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import ael

import FPackagesProcessingUtility as util
import importlib
importlib.reload(util)
import FBDPCommon
import FBDPInstrument
import FBDPRollback
from FBDPCurrentContext import Summary, Logme

def perform(params, performer):
    try:
        _perform(params, performer)
    finally:
        _cleanParams(params)
        Summary().log(params)
        util.Log.log(None, 'FINISH')

def _perform(params, performer):
    if not any(x in params for x in ('ins_pkg_oids', 'deal_pkg_oids')):
        raise Exception('No instrument or deal packages selected')

    name = params['ScriptName']
    acm_expiry_date = FBDPCommon.toDate(params['Date'].strip())
    if (not acm_expiry_date) or (acm_expiry_date == ''):
        raise Exception('Invalid date: %s' % (acm_expiry_date or None))

    if acm_expiry_date > acm.Time.DateToday():
        raise Exception('Date cannot be in the future: %s' % acm_expiry_date)

    Logme()('%s expiry date: %s' % (name, str(acm_expiry_date)))
    acm_trade_date = acm.Time.DateAddDelta(
        acm_expiry_date, 0, 0, -1.0 * params['OpenTradeDays']
    )
    Logme()('%s trade date: %s' % (name, str(acm_trade_date)))
    acm_expiry_date_inclusive = acm.Time.DateAddDelta(
        acm_expiry_date, 0, 0, -1
    )
    ael_trade_time = ael.date(acm_trade_date).to_time()
    other_params = params['other_params']
    gui_params = {}
    for key, value in params.items():
        if key != 'other_params':
            gui_params[key] = value

    other_params['gui_params'] = gui_params

    # baseParams are the parameters required by PackagesProcessingPerform
    archive_status = other_params['archive_status']
    ins_pkgs = params.get('ins_pkg_oids', [])
    deal_pkgs = params.get('deal_pkg_oids', [])
    action = other_params['action']
    baseParams = {
        'expiry_date_inclusive': acm_expiry_date_inclusive,
        'trade_time': ael_trade_time,
        'name': name,
        'ins_pkgs': ins_pkgs,
        'deal_pkgs': deal_pkgs,
        'archive_status': archive_status,
        'task': other_params['task'].capitalize(),
        'action': action,
    }
    # remove the other params no longer needed so that other_params
    # only consists of the parameters required by the sub-class
    for param in ('archive_status', 'task', 'action'):
        del other_params[param]

    # execute perform
    p = performer(bool(params['Testmode']), baseParams, other_params)
    try:
        p.perform()
    except:
        if ael.RollbackSpec[p.spec.name]:
            msg = (
                '%s failed to complete, rollback back modified '
                'entities' % action[0:-1].capitalize()
            )
            util.Log.log(msg, 'INFO', False)
            try:
                rollback = FBDPRollback.RollbackInfo()
                rollback.rollback(p.spec.name, None)
                util.Log.log('Rollback finished', 'INFO', False)
            except Exception as e:
                msg = 'Rollback failed to complete: %s' % e
                util.Log.log(msg, 'INFO', False)

            Summary().abortEntries()

        raise

    return

def _cleanParams(params):
    # cleanup params entries and remove those unnecessary for logging
    del params['other_params']
    for x in ('ins_pkg_oids', 'deal_pkg_oids'):
        if x in params:
            del params[x]

    return

class PackagesProcessingPerform(FBDPRollback.RollbackWrapper, object):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        # public
        self.testmode = testmode
        self.other_params = otherParams
        self.source_archive_status = baseParams['archive_status']

        # private
        self._expiry_date_inclusive = baseParams['expiry_date_inclusive']
        self._trade_time = baseParams['trade_time']
        self._task = baseParams['task']
        self._action = baseParams['action']
        self._input_pkgs = util.Packages(
            ins_pkgs=baseParams['ins_pkgs'], deal_pkgs=baseParams['deal_pkgs']
        )
        # unordered collections of pkg related objects used in expiry check
        self._examined_pkgs = util.PackageWrapper(
            root=None,
            ins_pkgs={}, deal_pkgs={}, trades={}, instrs={},
            ins_pkg_links={}, deal_pkg_links={}, trade_links={}, ins_links={}
        )
        # collection of known lead trade instruments
        self._lead_objs = {}
        # collections of pkg related objects grouped by source package
        self._pkgs = []
        FBDPRollback.RollbackWrapper.__init__(
            self, rollbackName=baseParams['name'],
            Testmode=self.testmode, param={}
        )

    # public
    def perform(self):
        acm.PollDbEvents()
        self._loadPkgs()
        self.other_params['perform_called'] = False
        self._perform()
        return

    def splitOnLead(self, objs):
        lead_objs = []
        non_lead_objs = []
        if len(objs):
            for obj in objs:
                name = util.getAelName(obj)
                if self._lead_objs.get(name):
                    lead_objs.append(obj)
                else:
                    non_lead_objs.append(obj)

        return lead_objs, non_lead_objs

    # for overriding
    def _getFilteredPackage(self, pkg):
        """
        The method used to collect valid pkgs and pkg related entities
        valid for performer
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def _getPerformer(self, pkgs, perform_func):
        """
        The method used to construct the perform executor
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def _processPackage(self, pkg):
        """
        The method used to actually perform the task on a given package
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    # private
    def _loadPkgs(self):
        act_on_live_objs = not bool(self.source_archive_status)
        # for all packages inspections, any already archived sub-components
        # are assumed to have already expired.
        if len(self._input_pkgs.ins_pkgs):
            ignores = self._loadAelInsPkgs(act_on_live_objs)
            if len(ignores):
                ins_pkgs = self._input_pkgs.ins_pkgs
                ins_pkgs = [pkg for pkg in ins_pkgs if pkg not in ignores]
                del self._input_pkgs.ins_pkgs[:]
                self._input_pkgs.ins_pkgs.extend(ins_pkgs)

        self._loadAelDealPkgs(act_on_live_objs)
        self._removeDuplicateRoots()
        for pkg in self._pkgs:
            util.applyToPackageWrapper(pkg, util.Log.logProcessed, True)

        # filter out non-viable and empty packages and components
        pkgs = []
        pkg_wrappers = (self._getFilteredPackage(pkg) for pkg in self._pkgs)
        for pkg_wrapper in pkg_wrappers:
            objs = []
            for component in pkg_wrapper:
                if component != pkg_wrapper.root:
                    objs.extend(component)

            if objs:
                pkgs.append(pkg_wrapper)

        # packages with root = deal package should be processed before
        # instrument packages
        ordered_pkgs = [
            pkg for pkg in pkgs if util.isType(pkg.root, util.Type.deal_pkg)
        ]
        ordered_pkgs.extend(
            pkg for pkg in pkgs if util.isType(pkg.root, util.Type.ins_pkg)
        )
        self._pkgs = ordered_pkgs
        return

    def _perform(self):
        perform_func = lambda performer: self._processPackage(
            performer.getObject()
        )
        performer = self._getPerformer(self._pkgs, perform_func)
        if performer:
            try:
                util.prepareFNewExpiration(self._pkgs)
                performer.perform()
            finally:
                util.undoPrepareFNewExpiration()

        return

    def _getExaminedObjs(self, obj):
        return util.getPackageWrapperAttribute(
            util.getAelObject(obj), self._examined_pkgs
        )

    def _appendToPkgs(self, pkg):
        if not util.isKnownType(pkg, False):
            name = util.getAelName(pkg)
            raise Exception('Expected %s to be ael entity' % name)

        pkg = util.PackageWrapper(
            root=pkg,
            ins_pkgs=list(), deal_pkgs=list(),
            trades=list(), instrs=list(),
            ins_pkg_links=list(), deal_pkg_links=list(),
            trade_links=list(), ins_links=list()
        )
        self._pkgs.append(pkg)

    def _updatePkg(self, obj, pkg, add_to_pkg):
        if not util.isKnownType(obj, False):
            name = util.getAelName(obj)
            raise Exception('Expected %s to be ael entity' % name)

        if obj == pkg.root:
            return True

        if util.getOid(obj) <= 0:
            return False

        obj_type = util.getType(obj, False)
        if (obj_type == util.Type.trade) and (obj.time >= self._trade_time):
            return False

        pkg_components = util.getPackageWrapperAttribute(obj, pkg)
        if add_to_pkg and (obj not in pkg_components):
            pkg_components.append(obj)
            return True

        return False

    def _addObjectToPkg(self, obj, pkg, add_to_pkg):
        if obj:
            obj = util.getAelObject(obj)
            name = util.getAelName(obj)
            examined_objs = self._getExaminedObjs(obj)
            examined_obj = examined_objs.get(name)
            added = False
            if (not examined_obj) or (not examined_obj.added):
                # Only act on instruments if the root is an instrument package
                if util.isType(obj, util.Type.ins):
                    add_to_pkg = add_to_pkg and (
                        not util.isType(pkg.root, util.Type.deal_pkg)
                    ) and not self._lead_objs.get(name)

                added = self._updatePkg(obj, pkg, add_to_pkg)
                examined_objs[name] = util.ExaminedObject(
                    expired=True, added=added,
                    can_add=(not added) or add_to_pkg, in_progress=False
                )

        return

    def _removeDuplicateRoots(self):
        # remove duplicates to avoid duplicate operations on the same entities
        entities = []

        def assertNoDuplicates(pkg):
            flattened_pkg = []

            def append(obj):
                if isinstance(obj, list):
                    flattened_pkg.extend(obj)
                else:
                    flattened_pkg.append(obj)

            append(pkg)
            util.applyToPackageWrapper(pkg, append, True)
            for entity in flattened_pkg:
                if entity in entities:
                    msg = 'Duplicate object found: %s' % (
                        util.getAelName(entity)
                    )
                    raise Exception(msg)
                else:
                    entities.append(entity)

        for pkg in reversed(self._pkgs):
            root = pkg.root
            for _pkg in self._pkgs:
                if _pkg.root != root:
                    if (root in _pkg.ins_pkgs) or (root in _pkg.deal_pkgs):
                        self._pkgs.remove(pkg)
                        continue

        for pkg in self._pkgs:
            assertNoDuplicates(pkg)

        return

    def _loadAelInsPkgs(self, act_on_live_objs):
        ignores = []
        for pkg_oid in self._input_pkgs.ins_pkgs:
            if pkg_oid in ignores:
                continue

            ael_pkg = ael.InstrumentPackage[pkg_oid]
            util.Log.logProcessing(ael_pkg, None, indent=False)
            if ael_pkg.archive_status != self.source_archive_status:
                msg = '%s archive_status = %i' % (
                    util.getAelName(ael_pkg), ael_pkg.archive_status
                )
                util.Log.logIgnore(ael_pkg, msg, True)
                ignores.append(pkg_oid)
                util.Log.logFinishedProcessing(ael_pkg, None, indent=False)
                continue

            self._appendToPkgs(ael_pkg)
            if act_on_live_objs and ael_pkg.archive_status == 0:
                # perform various checks on live ins pkg to only add expired
                acm_pkg = FBDPCommon.ael_to_acm(ael_pkg)
                if not self._allExpired([acm_pkg], True):
                    util.Log.logUnexpired(ael_pkg)
                    # undo appendToPkgs
                    del self._pkgs[len(self._pkgs) - 1]
                    ignores.append(pkg_oid)
                    continue

            self._loadAelSubComponents(ael_pkg, True)
            util.Log.logFinishedProcessing(ael_pkg, None, indent=False)

        return ignores

    def _loadAelDealPkgs(self, act_on_live_objs):
        def copyObjsToPkgWrapper(objs, pkg_w):
            if len(objs):
                ref_obj = objs[0]
                pkg_w_comp = util.getPackageWrapperAttribute(ref_obj, pkg_w)
                pkg_w_comp.extend(objs)

            return

        def retrieveDealPkgsByInsPkg(ins_pkg_oid):
            query = (
                'SELECT DISTINCT dp.seqnbr'
                ' FROM deal_package as dp'
                ' WHERE'
                ' (dp.ins_package_seqnbr = %i)'
            ) % ins_pkg_oid
            pkgs = FBDPCommon.FBDPQuerySelection(
                name='Deal Packages',
                query_expr=query,
                result_types=[ael.DealPackage]
            ).Run()
            return pkgs

        def loadDealPkg(
            ael_pkg, ignores, ignore_archive_status, indent, parent_ins_pkg
        ):
            pkg_oid = util.getOid(ael_pkg)
            if (pkg_oid in ignores):
                return

            util.Log.logProcessing(ael_pkg, None, indent=indent)
            if (not ignore_archive_status) and \
               (ael_pkg.archive_status != self.source_archive_status):
                msg = '%s archive_status = %i' % (
                    util.getAelName(ael_pkg), ael_pkg.archive_status
                )
                util.Log.logIgnore(ael_pkg, msg, True)
                ignores.append(pkg_oid)
                util.Log.logFinishedProcessing(ael_pkg, None, indent=False)
                return

            self._appendToPkgs(ael_pkg)
            if act_on_live_objs and ael_pkg.archive_status == 0:
                # perform various checks on live deal pkg to only add expired
                acm_pkg = FBDPCommon.ael_to_acm(ael_pkg)
                if not self._allExpired([acm_pkg], True):
                    util.Log.logUnexpired(ael_pkg)
                    del self._pkgs[len(self._pkgs) - 1]
                    ignores.append(pkg_oid)
                    return

            self._loadAelSubComponents(ael_pkg, True)
            if parent_ins_pkg:
                done = False
                deal_pkg_w = self._pkgs[-1]
                for pkg_w in self._pkgs:
                    if pkg_w.root == parent_ins_pkg:
                        if deal_pkg_w.root not in pkg_w.deal_pkgs:
                            pkg_w.deal_pkgs.append(deal_pkg_w.root)

                        clone = lambda objs: copyObjsToPkgWrapper(objs, pkg_w)
                        util.applyToPackageWrapper(deal_pkg_w, clone, False)
                        del self._pkgs[len(self._pkgs) - 1]
                        done = True
                        break

                if not done:
                    msg = (
                        'Failed to copy deal package contents to previously '
                        'added instrument package wrapper.'
                    )
                    raise Exception(msg)

            util.Log.logFinishedProcessing(ael_pkg, None, indent=indent)
            return

        ignores = []
        already_added = []
        # first collect all unique deal packages belonging
        # to specified instrument packages
        target_type = 'deal packages'
        for ins_pkg_oid in self._input_pkgs.ins_pkgs:
            ael_ins_pkg = ael.InstrumentPackage[ins_pkg_oid]
            util.Log.logProcessing(target_type, ael_ins_pkg, indent=False)
            for ael_deal_pkg in retrieveDealPkgsByInsPkg(ins_pkg_oid):
                loadDealPkg(ael_deal_pkg, ignores, True, True, ael_ins_pkg)
                already_added.append(util.getOid(ael_deal_pkg))

            util.Log.logFinishedProcessing(
                target_type, ael_ins_pkg, indent=False
            )

        # then collect all remaining deal packages specified in input
        for pkg_oid in self._input_pkgs.deal_pkgs:
            if pkg_oid not in already_added:
                ael_pkg = ael.DealPackage[pkg_oid]
                loadDealPkg(ael_pkg, ignores, False, False, None)

        return

    def _loadInsPkgLinks(self, ins_pkg_oid, add_to_pkg):
        query = (
            'SELECT DISTINCT ipl.seqnbr'
            ' FROM instrument_package_link as ipl'
            ' WHERE'
            ' ('
            '(ipl.parent_seqnbr = %i)'
            ' OR'
            ' (ipl.child_seqnbr = %i)'
            ')'
        ) % (ins_pkg_oid, ins_pkg_oid)
        links = FBDPCommon.FBDPQuerySelection(
            name='Instrument Package Links',
            query_expr=query,
            result_types=[ael.InstrumentPackageLink]
        ).Run()
        pkg_w = self._pkgs[-1]
        for l in links:
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            self._loadAelSubComponents(l.child_seqnbr, add_to_pkg)
            self._loadAelSubComponents(l.parent_seqnbr, False)

        return

    def _loadDealPkgInsLinks(self, ins_pkg_oid, add_to_pkg):
        query = (
            'SELECT DISTINCT dpil.seqnbr'
            ' FROM deal_package_ins_link as dpil'
            ' WHERE'
            ' (dpil.ins_package_seqnbr = %i)'
        ) % ins_pkg_oid
        links = FBDPCommon.FBDPQuerySelection(
            name='Instrument Package Links',
            query_expr=query,
            result_types=[ael.DealPackageInsLink]
        ).Run()
        pkg_w = self._pkgs[-1]
        for l in links:
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            self._loadAelSubComponents(l.ins_package_seqnbr, add_to_pkg)
            self._loadAelSubComponents(l.insaddr, add_to_pkg)

        return

    def _loadDealPkgLinks(self, deal_pkg_oid, add_to_pkg):
        query = (
            'SELECT DISTINCT dpl.seqnbr'
            ' FROM deal_package_link as dpl'
            ' WHERE'
            ' (dpl.deal_package_seqnbr = %i)'
            ' OR'
            ' (dpl.child_deal_package_seqnbr = %i)'
        ) % (deal_pkg_oid, deal_pkg_oid)
        links = FBDPCommon.FBDPQuerySelection(
            name='Deal Package Links',
            query_expr=query,
            result_types=[ael.DealPackageLink]
        ).Run()
        pkg_w = self._pkgs[-1]
        for l in links:
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            self._loadAelSubComponents(
                l.child_deal_package_seqnbr, add_to_pkg
            )
            self._loadAelSubComponents(l.deal_package_seqnbr, False)

        return

    def _loadDealPkgTradeLinks(self, deal_pkg_oid, add_to_pkg):
        query = (
            'SELECT DISTINCT dptl.seqnbr'
            ' FROM deal_package_trd_link as dptl'
            ' WHERE'
            ' (dptl.deal_package_seqnbr = %i)'
        ) % deal_pkg_oid
        links = FBDPCommon.FBDPQuerySelection(
            name='Deal Package Trade Links',
            query_expr=query,
            result_types=[ael.DealPackageTrdLink]
        ).Run()
        pkg_w = self._pkgs[-1]
        for l in links:
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            self._loadAelSubComponents(l.deal_package_seqnbr, add_to_pkg)
            self._loadAelSubComponents(l.trdnbr, add_to_pkg)

        return

    def _isLeadTrade(self, trade):
        name = util.getAelName(trade)
        is_lead = self._lead_objs.get(name)
        if is_lead is None:
            query = (
                'SELECT DISTINCT dptl.seqnbr'
                ' FROM deal_package_trd_link as dptl'
                ' WHERE'
                ' (dptl.trdnbr = %i)'
            ) % util.getOid(trade)
            link = FBDPCommon.FBDPQuerySelection(
                name='Deal Package Trade Links',
                query_expr=query,
                result_types=[ael.DealPackageTrdLink]
            ).Run()[0]
            is_lead = link.is_lead
            self._lead_objs[name] = is_lead

        return is_lead

    def _isLeadTradeInstrument(self, instrument):
        name = util.getAelName(instrument)
        is_lead = self._lead_objs.get(name)
        if is_lead is None:
            query = (
                'SELECT DISTINCT dptl.seqnbr'
                ' FROM trade, deal_package_trd_link as dptl'
                ' WHERE'
                ' (trade.insaddr = %i)'
                ' AND '
                ' (dptl.trdnbr = trade.trdnbr)'
            ) % util.getOid(instrument)
            links = FBDPCommon.FBDPQuerySelection(
                name='Instrument Package Instrument Trade Links',
                query_expr=query,
                result_types=[ael.DealPackageTrdLink]
            ).Run()
            is_lead = any(link.is_lead for link in links)
            self._lead_objs[name] = is_lead

        return is_lead

    def _loadAelSubComponents(self, obj, add_to_pkg):
        if not obj:
            return

        name = util.getAelName(obj)
        if not util.isKnownType(obj, False):
            raise Exception('Expected %s to be ael entity' % name)

        # logic prevents self._pkgs from containing duplicates
        examined_objs = self._getExaminedObjs(obj)
        examined_obj = examined_objs.get(name)
        examine = (not examined_obj) or (
            (not examined_obj.added) and (not examined_obj.in_progress) and (
                examined_obj.can_add
            )
        )
        examined_objs[name] = util.ExaminedObject(
            expired=True, added=False, can_add=add_to_pkg, in_progress=True
        )
        if (not add_to_pkg) or (not examine):
            return

        loaders = None
        obj_type = util.getType(obj)
        if obj_type == util.Type.ins_pkg:
            loaders = [self._loadInsPkgLinks, self._loadDealPkgInsLinks]
        elif obj_type == util.Type.deal_pkg:
            loaders = [self._loadDealPkgLinks, self._loadDealPkgTradeLinks]
        elif obj_type == util.Type.trade:
            loaders = []
        elif obj_type == util.Type.ins:
            loaders = []
        else:
            raise Exception('Unknown package sub-type specified')

        pkg_w = self._pkgs[-1]
        self._addObjectToPkg(obj, pkg_w, add_to_pkg)
        if len(loaders):
            oid = util.getOid(obj)
            for load in loaders:
                load(oid, add_to_pkg)

        return

    # Code for inspecting live entities
    def _insPkgExpired(self, pkg, add_to_pkg):
        if self._insPkgInstrsExpired(pkg, add_to_pkg):
            if self._insPkgDealPkgsExpired(pkg, add_to_pkg):
                if self._insPkgChildrenExpired(pkg, add_to_pkg):
                    # restricts operations to only those instrument packages
                    # whose dependents & dependencies are expired
                    return self._insPkgParentsExpired(pkg, False)

        return False

    def _dealPkgExpired(self, pkg, add_to_pkg):
        if self._dealPkgInstrsExpired(pkg, add_to_pkg):
            if self._dealPkgTradesExpired(pkg, add_to_pkg):
                if self._dealPkgInsPkgExpired(pkg, False):
                    if self._dealPkgChildrenExpired(pkg, add_to_pkg):
                        # restricts operations to only those deal packages
                        # whose dependents & dependencies are expired
                        return self._dealPkgParentsExpired(pkg, False)

        return False

    def _tradeExpired(self, trade, add_to_pkg):
        if self._isLeadTrade(trade):
            return trade.TradeTime() <= self._expiry_date_inclusive

        if trade.TradeTime() > self._expiry_date_inclusive:
            return False

        instrs = [util.returnOrNone(trade.Instrument)]
        return self._allExpired(instrs, add_to_pkg)

    def _insExpired(self, ins, add_to_pkg):
        if self._isLeadTradeInstrument(ins):
            return True

        return FBDPInstrument.isExpired(ins, self._expiry_date_inclusive)

    def _insPkgInstrsExpired(self, pkg, add_to_pkg):
        instrs = []
        pkg_w = self._pkgs[-1]
        for l in pkg.InstrumentLinks():
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            ins = util.returnOrNone(l.Instrument)
            instrs.append(ins)

        return self._allExpired(instrs, add_to_pkg)

    def _insPkgDealPkgsExpired(self, pkg, add_to_pkg):
        dps = util.returnOrNone(pkg.DealPackages)
        return self._allExpired(dps, add_to_pkg)

    def _insPkgChildrenExpired(self, pkg, add_to_pkg):
        pkgs = []
        pkg_w = self._pkgs[-1]
        for l in pkg.ChildLinks():
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            ip = util.returnOrNone(l.ChildPackage)
            pkgs.append(ip)

        return self._allExpired(pkgs, add_to_pkg)

    def _insPkgParentsExpired(self, pkg, add_to_pkg):
        pkgs = []
        pkg_w = self._pkgs[-1]
        for l in pkg.ParentLinks():
            self._addObjectToPkg(l, pkg_w, True)
            ip = util.returnOrNone(l.ParentPackage)
            pkgs.append(ip)

        return self._allExpired(pkgs, add_to_pkg)

    def _dealPkgInstrsExpired(self, pkg, add_to_pkg):
        instrs = util.returnOrNone(pkg.Instruments)
        return self._allExpired(instrs, add_to_pkg)

    def _dealPkgTradesExpired(self, pkg, add_to_pkg):
        trades = []
        pkg_w = self._pkgs[-1]
        for l in pkg.TradeLinks():
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            trade = util.returnOrNone(l.Trade)
            trades.append(trade)

        return self._allExpired(trades, add_to_pkg)

    def _dealPkgInsPkgExpired(self, pkg, add_to_pkg):
        pkgs = [util.returnOrNone(pkg.InstrumentPackage)]
        return self._allExpired(pkgs, add_to_pkg)

    def _dealPkgChildrenExpired(self, pkg, add_to_pkg):
        pkgs = []
        pkg_w = self._pkgs[-1]
        for l in pkg.ChildDealPackageLinks():
            self._addObjectToPkg(l, pkg_w, add_to_pkg)
            dp = util.returnOrNone(l.ChildDealPackage)
            pkgs.append(dp)

        return self._allExpired(pkgs, add_to_pkg)

    def _dealPkgParentsExpired(self, pkg, add_to_pkg):
        pkgs = []
        pkg_w = self._pkgs[-1]
        for l in pkg.ParentDealPackageLinks():
            self._addObjectToPkg(l, pkg_w, True)
            dp = util.returnOrNone(l.DealPackage)
            pkgs.append(dp)

        return self._allExpired(pkgs, add_to_pkg)

    def _allExpired(self, objs, add_to_pkg):
        # fails fast and prevent duplicate checks
        objs = [obj for obj in objs if obj]
        if not len(objs):
            return True

        if not all(FBDPCommon.is_acm_object(obj) for obj in objs):
            raise Exception('Expected list of ACM entities')

        ref_obj = objs[0]
        obj_type = util.getType(ref_obj)
        expiry_check_func = None
        if obj_type == util.Type.ins_pkg:
            expiry_check_func = self._insPkgExpired
        elif obj_type == util.Type.deal_pkg:
            expiry_check_func = self._dealPkgExpired
        elif obj_type == util.Type.trade:
            expiry_check_func = self._tradeExpired
        elif obj_type == util.Type.ins:
            expiry_check_func = self._insExpired
        else:
            raise Exception('Unknown package sub-type specified')

        # if object has previously been examined and
        # yet _allExpired is still called on it, then
        # it must have previously been found to be expired.
        # logic also prevents self._pkgs from containing
        # duplicates
        examined_objs = self._getExaminedObjs(ref_obj)
        pkg_w = self._pkgs[-1]
        for obj in objs:
            name = util.getAelName(obj)
            examined_obj = examined_objs.get(name)
            examine = (not examined_obj) or (
                (not examined_obj.added) and (not examined_obj.in_progress)
            )
            if examine:
                examined_objs[name] = util.ExaminedObject(
                    expired=True, added=False,
                    can_add=add_to_pkg, in_progress=True
                )
                is_expired = expiry_check_func(obj, add_to_pkg)
                if is_expired:
                    self._addObjectToPkg(obj, pkg_w, add_to_pkg)
                else:
                    examined_objs[name] = util.ExaminedObject(
                        expired=False, added=False,
                        can_add=False, in_progress=False
                    )
                    return False
            elif not examined_obj.expired:
                return False

        return True
