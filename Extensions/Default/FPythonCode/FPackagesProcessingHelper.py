""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/etc/FPackagesProcessingHelper.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import FPackagesProcessingUtility as util
import importlib
importlib.reload(util)
import FNewExpirationPerform
importlib.reload(FNewExpirationPerform)
import FBDPWorld

def make_generic_performer(
    owner, objs, indentation, performer_cls, check_success_func, perform_func
):
    # returns an instance of a generic perform, completely managed by
    # local code
    if not issubclass(performer_cls, _AelSameObjectsPerformer):
        raise Exception('Invalid generic performer type')

    if not len(objs):
        return None

    return performer_cls(
        owner, objs, indentation, perform_func, check_success_func
    )

def make_FNewExpirationPerform_performer(
    owner, params, objs, performer_cls, check_success_func, action
):
    # returns an wrapper for FNewExpirationPerform, which can only be
    # managed by local code and FNewExpirationPerform
    if not len(objs):
        return None

    ref_obj = objs[0]
    ref_obj_type = util.getType(ref_obj, False)
    for obj in objs:
        if not util.isType(obj, ref_obj_type):
            raise Exception('Invalid ael entity(s): %s' % obj)

    return performer_cls(owner, params, action, objs, check_success_func)

def assertCompatibleWithPerformer(objs):
    assert len(objs), 'No objects passed to performer'
    if not util.areAllKnownTypes(objs, True):
        msg = 'Unhandled object(s) passed to performer: %s' % ', '.join(
            str(obj) for obj in objs
        )
        raise Exception(msg)

    ref_obj = objs[0]
    ref_type = type(ref_obj)
    if not all(ref_type == type(obj) for obj in objs):
        raise Exception('Cannot specify object of mixed entities')

    record_type = getattr(ref_obj, 'record_type', None)
    is_same_type = False
    if record_type:
        is_same_type = all(obj.record_type == record_type for obj in objs)
    else:
        is_same_type = all(
            isinstance(obj, util.PackageWrapper) for obj in objs
        )

    if not is_same_type:
        raise Exception('Invalid object(s): %s' % objs)

    for obj in objs:
        obj = util.getAelObject(obj)
        obj_as = obj.archive_status
        if (obj_as != 0) and (obj_as != 1):
            name = util.getAelName(obj)
            msg = '%s has unhandled archive status %i' % (name, obj_as)
            raise Exception(msg)

    return

class _WorldProxy(FBDPWorld.World):
    """
    Helper class to ensure FNewExpirationPerform has the correct
    parameters and to also enable passing of various bits of
    information to FNewExpirationPerform
    """
    ARCHIVE_ACTION = 'archive'
    DEARCHIVE_ACTION = 'dearchive'
    LIVE_DELETE_ACTION = 'live delete'
    ARCHIVE_DELETE_ACTION = 'archive delete'

    def __init__(self, params, action):
        assert action in (
            _WorldProxy.ARCHIVE_ACTION, _WorldProxy.DEARCHIVE_ACTION,
            _WorldProxy.LIVE_DELETE_ACTION, _WorldProxy.ARCHIVE_DELETE_ACTION
        )
        params = params.copy()
        params['preservePL'] = params.get('PreservePL')
        params['suppress_exceptions'] = False
        super(_WorldProxy, self).__init__(params)
        self._params = params
        self._action = action

class _Performer(object):
    """
    Wrapper class for an entity on which to perform the action
    (i.e. to archive/de-archive or delete)
    """
    def __init__(self, owner, name, obj, indentation, check_success_func):
        self._owner = owner
        self._name = name
        self._obj = obj
        self._indentation = indentation
        self._check_success_func = check_success_func

        self._owner.other_params['perform_called'] = True
        self._oid = util.getOid(self._obj)
        self._type = util.getType(self._obj)

    def isInTestMode(self):
        return self._owner.testmode

    def logActionStarted(self):
        util.Log.logActionStarted(
            self._owner._task, self._name, self._indentation
        )
        if (self._type != util.Type.pkg_wrapper) and \
           isinstance(self, _SinglePerformer):
            util.Log.logOk(self._obj, self._owner._action, self._name)

    def logActionFinished(self):
        util.Log.logActionFinished(
            self._owner._task, self._name, self._indentation
        )
        self.checkPerformSucceeded()

    def getRollback(self):
        return self._owner

    def perform(self):
        raise NotImplementedError('Must be overridden in the subclass.')

    def checkPerformSucceeded(self):
        if not self.isInTestMode():
            try:
                return self._check_success_func(self._type, self._oid)
            except:
                util.Log.logOk(self._obj, self._owner._action, self._name, -1)
                util.Log.logError(self._obj, None, False, self._owner._action)
                raise

class _SinglePerformer(_Performer):
    """
    Base wrapper class for performing action on single object
    """
    def __init__(self, owner, obj, indentation, check_success_func):
        name = util.getAelName(obj)
        if isinstance(obj, util.PackageWrapper):
            ael_obj = util.getAelObject(obj)
            obj_type = util.getType(ael_obj)
            if (obj_type == util.Type.deal_pkg) and (len(obj.deal_pkgs) == 0):
                name = name + ' components'
            elif (obj_type == util.Type.ins_pkg) and (len(obj.ins_pkgs) == 0):
                name = name + ' components'

        super(_SinglePerformer, self).__init__(
            owner, name, obj, indentation, check_success_func
        )

class _BatchPerformer(_Performer):
    """
    Base wrapper class for performing action on multiple objects in a batch
    """
    pass

class _AelObjectPerformer(_SinglePerformer):
    def __init__(
        self, owner, obj, perform_func, indentation, check_success_func
    ):
        super(_AelObjectPerformer, self).__init__(
            owner, obj, indentation, check_success_func
        )
        self._perform_func = perform_func

    def getObject(self):
        return self._obj

    def perform(self):
        self.logActionStarted()
        self._perform_func(self)
        self.logActionFinished()

class _AelObjectsPerformer(_BatchPerformer):
    def __init__(
        self, owner, name, ref_obj, indentation,
        performers, objs, check_success_func
    ):
        assert len(performers), 'Found no performers'
        super(_AelObjectsPerformer, self).__init__(
            owner, name, ref_obj, indentation, check_success_func
        )
        self._performers = performers
        self._obj_params = util.getMakeAelObjectParamsFromList(objs)

    def perform(self):
        self.logActionStarted()

        fexp_base_cls = FNewExpirationPerform._NewExpirationPerformBase
        for performer in self._performers:
            if isinstance(performer, fexp_base_cls):
                performer.perform(performer._getWorldRef()._params)
            else:
                performer.perform()

        self.logActionFinished()

    def checkPerformSucceeded(self):
        if not self.isInTestMode():
            obj_type = None
            oid = None
            errors = []
            for obj_type, oid in self._obj_params:
                try:
                    self._check_success_func(obj_type, oid)
                except Exception as e:
                    obj = util.makeAelObject(obj_type, oid)
                    util.Log.logOk(obj, self._owner._action, self._name, -1)
                    util.Log.logError(obj, None, False, self._owner._action)
                    errors.append(str(e))

            if len(errors):
                raise Exception(', '.join(errors))

        return

class _AelSameObjectsPerformer(_AelObjectsPerformer):
    def __init__(
        self, owner, objs, indentation, perform_func, check_success_func
    ):
        ref_obj = objs[0]
        name = util.getAelName(ref_obj).split('[')[0] + 's'
        performers = []
        new_indentation = indentation + util.INDENTATION
        for obj in objs:
            performers.append(_AelObjectPerformer(
                owner, obj, perform_func, new_indentation, check_success_func
            ))

        success_func = lambda obj_type, oid: None
        super(_AelSameObjectsPerformer, self).__init__(
            owner, name, ref_obj, indentation, performers, objs, success_func
        )

class _FNewExpirationObjectLogger(_AelObjectPerformer):
    def __init__(self, owner, obj, indentation):
        perform_func = lambda obj: None
        check_success_func = lambda obj_type, oid: None
        super(_FNewExpirationObjectLogger, self).__init__(
            owner, obj, perform_func, indentation, check_success_func
        )

class _FNewExpirationPerformWrapper(_AelObjectsPerformer):
    def __init__(
        self, owner, name, ref_obj, indentation,
        performers, check_success_func, objs
    ):
        """
        Wrapper class for perform action via FNewExpiration
        """
        super(_FNewExpirationPerformWrapper, self).__init__(
            owner, name, ref_obj, indentation,
            performers, objs, check_success_func
        )
        self._objs = objs

    def perform(self):
        # Some wrapper code to provide logging in line with the rest
        # of this script for FNewExpirationPerform.perform (c.f. loggers)
        indentation = self._indentation + util.INDENTATION
        loggers = [
            _FNewExpirationObjectLogger(
                self._owner, obj, indentation
            ) for obj in self._objs
        ]
        logActionStarted = self.logActionStarted
        logActionFinished = self.logActionFinished
        self.logActionStarted = self.logActionFinished = lambda: None

        logActionStarted()
        for logger in loggers:
            logger.logActionStarted()

        # Execute perform function with the inherent _AelObjectsPerformer
        # logging suppressed as FNewExpiration performs it own logging
        super(_FNewExpirationPerformWrapper, self).perform()
        for logger in loggers:
            logger.logActionFinished()

        logActionFinished()

class _AelTradesPerformer(_FNewExpirationPerformWrapper):
    def __init__(self, owner, params, action, objs, check_success_func):
        if not util.areAllKnownTypes(objs, False):
            raise Exception('Invalid trade object(s): %s' % type(objs))

        # As FNewExpiration cannot handle archiving trades whose
        # underlying intruments are already archived, so they must first be
        # de-archived, then re-archived when finished
        self._ins_to_dearchive = []
        trades_by_ins = {}
        for obj in objs:
            obj = util.getAelObject(obj)
            ins = obj.insaddr
            if (not owner.testmode) and (obj.archive_status == 0):
                if (ins.archive_status == 1):
                    if ins not in self._ins_to_dearchive:
                        self._ins_to_dearchive.append(ins)

            trades_by_ins.setdefault(util.getOid(ins), []).append(obj)

        # Performers are constructed on a per instrument basis as
        # FNewExpiration works by retreiving the trades from the instrument
        # object
        performers = []
        for ins_oid, trades in trades_by_ins.items():
            name = util.getAelName(trades[0]).split('[')[0] + 's'
            world = _WorldProxy(params, action)
            world._params['allowed_trades'] = [t.trdnbr for t in trades]
            performers.append(FNewExpirationPerform._createPerformer(
                log=world, action=world._action,
                object_type='trade', inst=ins_oid
            ))

        super(_AelTradesPerformer, self).__init__(
            owner, name, objs[0], util.INDENTATION * 2,
            performers, check_success_func, objs
        )

    def perform(self):
        # dearchive the necessary instruments
        for ins in self._ins_to_dearchive:
            util.archive(ins, 0, False, self.getRollback())

        super(_AelTradesPerformer, self).perform()
        # rearchive the necessary instruments
        for ins in self._ins_to_dearchive:
            util.archive(ins, 1, False, self.getRollback())

        return

class _AelInstrumentsPerformer(_FNewExpirationPerformWrapper):
    def __init__(self, owner, params, action, objs, check_success_func):
        if not util.areAllKnownTypes(objs, False):
            raise Exception('Invalid instrument object(s): %s' % type(objs))

        ref_obj = objs[0]
        name = util.getAelName(ref_obj).split('[')[0] + 's'
        world = _WorldProxy(params, action)
        performers = []
        for ins in objs:
            performers.append(FNewExpirationPerform._createPerformer(
                log=world, action=world._action,
                object_type='instrument', inst=ins.insaddr
            ))

        super(_AelInstrumentsPerformer, self).__init__(
            owner, name, ref_obj, util.INDENTATION * 2,
            performers, check_success_func, objs
        )
