""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPRollback.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
import acm
import ael


import datetime
from time import ctime
from math import ceil


import FBDPCommon
import FBDPInstrument


from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import importlib


NotFound = "NotFound"


def archive_recursive(clone, archive_status, testmode, rollback=None):
    if FBDPCommon.is_acm_object(clone):
        a_status = 'ArchiveStatus'
    else:
        a_status = 'archive_status'
    if (FBDPCommon.has_attr(clone, a_status) and
            FBDPCommon.record_type(clone) not in ['Trade', 'Settlement']):
        if FBDPCommon.get_attr(clone, a_status) != archive_status:
            FBDPCommon.set_attr(clone, a_status, archive_status)
            if rollback:
                rollback.add(clone, ['archive_status'])
            elif not testmode:
                FBDPCommon.commit(clone)
            Summary().ok(clone, (archive_status and Summary().ARCHIVE or
                    Summary().DEARCHIVE), FBDPCommon.display_id(clone))
            set_archive_status_on_children(clone, archive_status, testmode,
                    rollback)


def set_archive_status_on_children(clone, archive_status, testmode,
        rollback=None):
    if (FBDPCommon.record_type(clone) == "Trade" and archive_status == 1 and
            FBDPCommon.get_attr(clone,
            (FBDPCommon.is_acm_object(clone) and 'Aggregate' or 'aggregate'))):
        if testmode:
            return
        else:
            raise RuntimeError("Not able to deaggregate the position.")

    clone_ael = eval('ael.%s[%s]' % (FBDPCommon.record_type(clone),
            FBDPCommon.getPrimaryKey(clone))).clone()
    for child in clone_ael.children():
        c = child
        if FBDPCommon.is_acm_object(clone):
            c = FBDPCommon.ael_to_acm(child)
        archive_recursive(c, archive_status, testmode, rollback)


def dearchive_children(clone, testmode=1, rollback=None):
    set_archive_status_on_children(clone, 0, testmode, rollback)


def archive_children(clone, testmode=1, rollback=None):
    set_archive_status_on_children(clone, 1, testmode, rollback)

class Rollback:
    """
    Class for maintaining rollback information.
    All subclasses must implement the template method perform(self).
    """

    Testmode = None
    MAX_TR_SIZE = 50
    TIME_FMT = '%y%m%d %H%M%S.%f'
    DB_NAME_MAX_LEN = FBDPCommon.getMaxNameLength(acm.FRollbackSpec)
    NAME_MAX_LEN = DB_NAME_MAX_LEN - len(
        datetime.datetime(day=1, month=1, year=1970).strftime(TIME_FMT)[:-3]
    ) - 1

    def __init__(self, rollbackName=None, *args, **keyargs):
        if rollbackName:
            Rollback.Testmode = keyargs['Testmode']
            self.initSpec(rollbackName=rollbackName)
            self.perform(*args)
            Summary().log(self.ael_variables_dict)
            Logme()(None, 'FINISH')

    def initSpec(self, rollbackName):
        dTime = datetime.datetime.today().strftime(Rollback.TIME_FMT)[:-3]
        # truncate name by NAME_MAX_LEN
        rollbackName = rollbackName[:Rollback.NAME_MAX_LEN] + ' ' + dTime
        assert len(rollbackName) <= Rollback.DB_NAME_MAX_LEN, \
            'FRollbackSpec name (%s) is too long (%d vs %d)' % (
                rollbackName, len(rollbackName), Rollback.DB_NAME_MAX_LEN
            )
        self.initializeSpecification(rollbackName)
        return

    def perform(self):
        raise NotImplementedError

    def encapsulateAttribute(self, o, oid=None):
        try:
            if type(o) == type(''):
                return """\'\'\'%s\'\'\'""" % o
            if not oid:
                try:
                    oid = FBDPCommon.getPrimaryKey(o)
                except:
                    pass
            if FBDPCommon.is_acm_object(o):
                return 'acm.F%s[%s]' % (o.Category(), oid)
            elif type(o) == ael.ael_entity:
                return 'ael.%s[%d]' % (o.record_type, oid)
            elif type(o) == ael.ael_date:
                return 'ael.date(\'%s\')' % o
            else:
                return str(o)
        except RuntimeError:
            return 'unknown'

    def logCreatedMirrorTrade(self, trade):
        if trade:
            if FBDPCommon.is_acm_object(trade):
                mirrorTrade = trade.MirrorTrade()
                if (not mirrorTrade and self.Testmode and
                        trade.MirrorPortfolio()):
                    mirrorTrade = trade.Clone()
                    mirrorTrade.Portfolio(trade.MirrorPortfolio())
                    mirrorTrade.Acquirer(trade.Counterparty())
                    mirrorTrade.Counterparty(trade.Acquirer())
                    mirrorTrade.Quantity(-trade.Quantity())
                    mirrorTrade.Premium(-trade.Premium())
            else:
                mirrorTrade = trade.mirror_trdnbr
            if mirrorTrade:
                Logme()('*** Creating trade ***')
                self.logSaveTrade(mirrorTrade)
                Summary().ok(mirrorTrade, Summary().CREATE)

    def logSaveTrade(self, t):
        isAcm = FBDPCommon.is_acm_object(t)
        Logme()('Trade Number: %s' % (t.Oid() if isAcm else t.trdnbr))
        Logme()('Insid: %s' % (t.Instrument().Name() if isAcm else
                t.insaddr.insid))
        Logme()('Portfolio:%s' % ((t.Portfolio() and t.Portfolio().Name()) if
                isAcm else (t.prfnbr and t.prfnbr.prfid)))
        Logme()('Trade Time: %s' % (t.TradeTime() if isAcm else ctime(t.time)),
                'DEBUG')
        Logme()('Quantity: %f' % (t.Quantity() if isAcm else t.quantity))
        Logme()('Price: %f' % (t.Price() if isAcm else t.price))
        Logme()('Curr: %s' % (t.Currency().Name() if isAcm else t.curr.insid))
        Logme()('Premium: %f' % (t.Premium() if isAcm else t.premium), 'DEBUG')
        typ = (t.Type() if isAcm else t.type)
        Logme()('Type: %s' % typ)
        if typ == 'Cash Posting':
            Logme()('Cashposted instrument: %s' %
                    (t.Text1() if isAcm else t.text1))
        if typ in ('Clear PL', 'Cash Posting'):
            Logme()('AggregatePl: %f' %
                    (t.AggregatePl() if isAcm else t.aggregate_pl))
        Logme()(30 * '_')

    def initializeSpecification(self, specificationName):
        #self.spec = acm.FRollbackSpec()
        #self.spec.Name = specificationName
        self.spec = ael.RollbackSpec.new()
        self.spec.name = specificationName

    def __str__(self):
        return self.encapsulateAttribute(self.rollbackSpec)

    def validateCounterparty(self, counterparty, t, oid):
        if not counterparty:
            if FBDPCommon.is_acm_object(t):
                tStatus = t.Status()
            else:
                tStatus = t.status
            Logme()('No counterparty. Will skip this %s trade' % tStatus,
                    'WARNING')
            Summary().fail(t, Summary().CREATE, 'No counterparty', oid)
            return False
        if not acm.FParty[counterparty]:
            Summary().fail(t, Summary().CREATE, "User: %s does not exist." %
                    counterparty, oid)
            raise RuntimeError("Counterparty: %s does not exist." %
                    counterparty)
        return True

    def validateAcquirer(self, acquirer, t, oid):
        if not acquirer:
            if FBDPCommon.is_acm_object(t):
                tStatus = t.Status()
            else:
                tStatus = t.status
            Logme()('No acquirer. Will skip this %s trade' % tStatus,
                    'WARNING')
            Summary().fail(t, Summary().CREATE, 'No acquirer', oid)
            return False
        if not acm.FParty[acquirer]:
            Summary().fail(t, Summary().CREATE, "Acquirer: %s does not "
                    "exist." % acquirer, oid)
            raise RuntimeError("Acquirer: %s does not exist." % acquirer)
        return True

    def validateTrader(self, trader, t, oid):
        # If a trader has been specified at all, it must be a valid user.
        if trader and not acm.FUser[trader]:
            Summary().fail(t, Summary().CREATE, "User: %s does not exist." %
                    trader, oid)
            raise RuntimeError("User: %s does not exist." % trader)

    def commitOrRollback(self, t, oid, attribs, op):
        if not 'trades_to_log' in dir(self):
            self.trades_to_log = []
        self.trades_to_log.append(t)
        if self.add(t, attribs, op):
            Summary().ok(t, (Summary().UPDATE if (op == 'Update') else
                    Summary().CREATE))
        else:
            Summary().fail(t, Summary().CREATE, "Not possible to commit trade "
                    "or rollback data", oid)
            raise RuntimeError("Not possible to commit trade or rollback "
                    "data", oid)

    def add_trade(self, t=None, attribs=[], op=None,
            modified_child_entities=None):
        oid = FBDPCommon.getPrimaryKey(t)
        op = (op or (attribs or modified_child_entities) and 'Update' or
              'Create')
        error = 'Error'

        isAcm = FBDPCommon.is_acm_object(t)
        if isAcm:
            ins = t.Instrument()
            name = ins.Name()
            tradeable = FBDPInstrument.isTradable(t.Instrument())
            counterparty = t.Counterparty() and t.Counterparty().Name()
            acquirer = t.Acquirer() and t.Acquirer().Name()
            trader = t.Trader() and t.Trader().Name()
            status = t.Status()
        else:
            ins = t.insaddr
            name = ins.insid
            tradeable = FBDPInstrument.isTradable(t.insaddr)
            counterparty = (t.counterparty_ptynbr and
                    t.counterparty_ptynbr.ptynbr)
            acquirer = t.acquirer_ptynbr and t.acquirer_ptynbr.ptyid
            trader = t.trader_usrnbr and t.trader_usrnbr.userid
            status = t.status

        if not tradeable:
            Summary().fail(t, Summary().CREATE,
                    ('Instrument %s is not tradable' % name), oid)
            return error
        if status != "Simulated":
            if (not self.validateAcquirer(acquirer, t, oid) or
                    not self.validateCounterparty(counterparty, t, oid)):
                return error
        self.validateTrader(trader, t, oid)
        self.commitOrRollback(t, oid, attribs, op)

    def transit_business_process_state(self, bp, event,
                             toState=None, reason=''):
        """
        Handle business process event in roll back
        """
        if event == None and toState == None or bp == None \
                or not FBDPCommon.is_acm_object(bp):
            return False

        if 'transaction_list' in dir(self):
            if event:
                bp.HandleEvent(event)
            else:
                bp.ForceToState(toState, reason)
            op = 'Update'
            attribs = []
            orig = eval(self.encapsulateAttribute(bp))
            bp_id = FBDPCommon.getPrimaryKey(bp)
            orig_copy = bp
            rd = self.createRollbackData(bp_id, orig_copy, attribs, op)
            tpl = (bp, bp_id, orig_copy, attribs, op, rd)
            self.addToTransactionList(tpl)
            return True

        # Commit and add rollback data to the rollback spec directly.
        self.beginTransaction()
        self.transit_business_process_state(bp, event, toState, reason)
        try:
            self.commitTransaction()
        except:
            self.abortTransaction()
            return False
        return True

    def add(self, e, attribs=[], op=None, modified_child_entities=None):
        """
        Only add to transaction list
        """
        if 'transaction_list' in dir(self):
            op = (op or (attribs or modified_child_entities) and 'Update' or
                  'Create')
            if modified_child_entities and op == 'Update':
                for ca in modified_child_entities:
                    (c, c_attribs) = ca
                    c_op = c_attribs and 'Update' or 'Create'
                    c_orig = eval(self.encapsulateAttribute(c))
                    c_id = FBDPCommon.getPrimaryKey(c)
                    c = ((c_op == 'Update') and
                             FBDPCommon.clone(c_orig) or c)
                    rd1 = self.createRollbackData(c_id, c, c_attribs, c_op)
                    tpl = (None, c_id, c, c_attribs, c_op, rd1)
                    self.addToTransactionList(tpl)

            orig = eval(self.encapsulateAttribute(e))
            e_id = FBDPCommon.getPrimaryKey(e)
            orig_copy = (op == 'Update') and FBDPCommon.clone(orig) or e
            rd = self.createRollbackData(e_id, orig_copy, attribs, op)
            tpl = (e, e_id, orig_copy, attribs, op, rd)
            self.addToTransactionList(tpl)
            return True
        # Commit and add rollback data to the rollback spec directly.
        self.beginTransaction()
        self.add(e, attribs, op, modified_child_entities)
        try:
            self.commitTransaction()
        except:
            self.abortTransaction()
            return False
        return True

    def commitTransaction(self, splitInCaseOfFailure=False):
        """
        To big transactions will be impossible to handle, so in the case that
        the commit of the transaction failes, the transaction will be split
        into smaller transactions. If the reason for the failure is NOT a to
        big SQL query, all changes will be rolled back before returning.
        """
        if not 'transaction_list' in dir(self):
            raise Exception("You are trying to commit a non existing "
                    "transaction.  Make sure to call begin_transaction() "
                    "first.")
        if 'trades_to_log' not in dir(self):
            self.trades_to_log = []
        self.commitAll(splitInCaseOfFailure)
        acm.PollDbEvents()
        self.clearTransactionData()

    def beginTransaction(self):
        if 'transaction_list' in dir(self):
            raise Exception("You are trying to start a second transaction.  "
                    "Only one transaction can be handled at a time.")
        self.transaction_list = []
        self.commited_list = []

    def abortTransaction(self):
        self.rollbackTransactions()
        self.clearTransactionData()

    def clearTransactionData(self):
        if 'transaction_list' in dir(self):
            del self.transaction_list
        if 'trades_to_log' in dir(self):
            del self.trades_to_log
        if 'commited_list' in dir(self):
            del self.commited_list

    def commitAddedEntities(self):
        if 'transaction_list' not in dir(self):
            raise Exception("You are trying to commit a non existing "
                    "transaction.  Make sure to call begin_transaction() "
                    "first. ")
        if not 'trades_to_log' in dir(self):
            self.trades_to_log = []
        self.commitList(self.transaction_list)
        self.commited_list.append(self.transaction_list)
        self.transaction_list = []
        acm.PollDbEvents()
        if 'trades_to_log' in dir(self):
            del self.trades_to_log

    def addToTransactionList(self, tuple_or_list):
        if type(tuple_or_list) == type(()):  # tuple
            self.transaction_list.append(tuple_or_list)
        else:
            self.transaction_list.extend(tuple_or_list)
        return True

    def commitFunction(self, op):
        return (op == 'Delete') and FBDPCommon.delete or FBDPCommon.commit

    def commitAll(self, splitInCaseOfFailure):
        """ Commit all objects in transaction list """
        try:
            self.commitList(self.transaction_list)
        except Exception as error:
            if (splitInCaseOfFailure and
                    len(self.transaction_list) > self.MAX_TR_SIZE):
                failmsg = self.commitSmallerTransactions()
                if failmsg:
                    raise RuntimeError(failmsg)
            else:
                raise RuntimeError(error)
        return 0

    def commitList(self, tr_list):
        try:
            acm.BeginTransaction()
        except Exception as error:
            Logme()('Rollback failed to begin transaction. \n%s.' %
                    (str(error)), 'ERROR')
            raise error
        try:
            for tpl in tr_list:
                e = tpl[0]
                op = tpl[4]
                rd = tpl[5]
                if e:
                    commit_function = self.commitFunction(op)
                    arg = [e]
                    orig = eval(self.encapsulateAttribute(e))
                    if orig and op == 'Update':
                        arg.append(orig)
                    if not Rollback.Testmode:
                        try:
                            commit_function(*arg)
                        except Exception as error:
                            Logme()('Failed to %s object. %s.' % (op,
                                    str(error)), 'ERROR')
                            raise Exception("Rollback unable to commit "
                                    "object. " + str(error))
                        if op != 'Delete':
                            try:
                                rd.commit()
                            except Exception as e:
                                Logme()('Failed to commit rollback data. %s.' %
                                        (op, str(error)), 'ERROR')
                                raise Exception("Rollback unable to commit "
                                        "rollback data. " + str(error))
        except Exception as e:
            acm.AbortTransaction()
            raise e

        try:
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise e
        acm.PollDbEvents()
        try:
            self.logAndUpdateRollbackData(tr_list)
        except Exception as e:
            raise Exception("Failed to log and update Rollback Data. %s." %
                    str(e))

    def commitSmallerTransactions(self):
        size = len(self.transaction_list)
        commitSize = min(int(ceil(size / 10.0)), self.MAX_TR_SIZE)
        cmList = self.splitTransactionList(commitSize, self.transaction_list)
        for trList in cmList:
            try:
                self.commitList(trList)
            except Exception:
                break
            else:
                self.commited_list.append(trList)

    def rollbackTransactions(self):
        # Rollback all previous changes
        acm.PollDbEvents()
        if 'commited_list' not in dir(self):
            return
        self.commited_list.reverse()
        for rollbackList in self.commited_list:
            for tpl in rollbackList:
                e = tpl[0]
                oid = tpl[1]
                orig_copy = tpl[2]
                attribs = tpl[3]
                op = tpl[4]
                if op == 'Create':
                    #delete e with ael
                    e_ael = eval('ael.%s[%d]' % (FBDPCommon.record_type(e),
                            oid))
                    e_str = self.encapsulateAttribute(e)
                    if e_ael:
                        e_ael.delete()
                        Logme()('Deleted (newly created): %s' % e_str, 'DEBUG')

                else:
                    if op == 'Delete':
                        #recreate orig_copy if possible
                        if orig_copy:
                            if FBDPCommon.is_acm_object(orig_copy):
                                obj = orig_copy.Clone()
                                try:
                                    FBDPCommon.commit(obj, e)
                                    acm.PollDbEvents()
                                except Exception as ex:
                                    print(ex)
                    elif op == 'Update':
                        if FBDPCommon.is_acm_object(e) and \
                                    e.IsKindOf(acm.FBusinessProcess):
                            previousState = e.CurrentStep(
                                ).PreviousStep().State().Name()
                            e.ForceToState(
                                previousState, 'Abort Transaction')
                            obj = e
                        else:
                            obj = FBDPCommon.clone(e)
                            for attr in attribs:
                                if attr not in ['UpdateUser', 'UpdateTime']:
                                    FBDPCommon.set_attr(obj, attr,
                                            FBDPCommon.get_attr(
                                                orig_copy, attr))
                    try:
                        FBDPCommon.commit(obj, e)
                        acm.PollDbEvents()
                    except Exception as ex:
                        print(ex)

    def splitTransactionList(self, size, transactionList):
        counter = 0
        mainList = []
        subList = []
        for tpl in transactionList:
            subList.append(tpl)
            counter += 1
            if counter == size:
                mainList.append(subList)
                subList = []
                counter = 0
        if subList:
            mainList.append(subList)
        return mainList

    def logAndUpdateRollbackData(self, tr_list):
        """ If commit went well, save rollback data """
        for tpl in tr_list:
            e = tpl[0]
            oid = tpl[1]
            op = tpl[4]
            rd = tpl[5]
            if self.trades_to_log.count(e):
                self.trades_to_log.remove(e)
                Logme()('')
                if op == 'Update':
                    if 'LogMode' in dir(Logme()) and Logme().LogMode > 0:
                        Logme()('*** Updating trade ***')
                    else:
                        pass
                else:
                    Logme()('*** Creating trade ***')
                self.logSaveTrade(e)
            if op == 'Create' and not Rollback.Testmode:
                oid = FBDPCommon.getPrimaryKey(e)
                self.updateRollbackDataId(rd, e, oid)

    def updateRollbackDataId(self, rd, entity, oid):
        if FBDPCommon.is_acm_object(entity):
            if entity.IsKindOf('FTrade'):
                entity = ael.Trade[oid]
                if entity:
                    oid = entity.trdnbr
        rd.entity = self.encapsulateAttribute(entity, oid)
        rd.commit()

    # ######  When SPR 291568 is done, this should be replaced with acm #######
    def createRollbackData(self, oid, entity, attribs, op):
        rd = ael.RollbackData.new(self.spec)
        attributes = {}
        for i in attribs:
            attributes[i] = self.encapsulateAttribute(
                    FBDPCommon.get_attr(entity, i))
        rd.set_attributes(str(attributes))
        rd.entity = self.encapsulateAttribute(entity, oid)
        rd.operation = op
        return rd

    # ######  When SPR 291568 is done, this should be replaced with acm #######
    def rollback(self, spec, instruments):
        """Rollback (undo) a corporate action from the rollback data in the
        database."""
        r = ael.RollbackSpec[spec]
        self.instruments = instruments
        if r:
            self.spec = r.clone()
            rb_list = [(-i.seqnbr, i) for i in self.spec.rollback_data()]
            rb_list.sort()
            rb_list = [i[1] for i in rb_list]
            counter = 0
            keep_spec = False
            for i in rb_list:
                self.keep_rd = False
                self.entityIsArchived = False
                self.referred_ins = None
                if i.entity:
                    entity = eval(i.entity)
                    if entity:
                        self.rollback_data(entity, i)
                    else:
                        Logme()("Entity '{0}' was not found.".format(
                                str(i.entity)), 'WARNING')
                if self.keep_rd:
                    keep_spec = True
                else:
                    try:
                        dummy = FBDPCommon.record_type(entity)
                    except (AttributeError, RuntimeError) as error:
                        if str(error) in (("'NoneType' object has no "
                                "attribute 'record_type'"),
                                "entity is deleted"):
                            continue
                        else:
                            raise Exception(str(error))
                    else:
                        try:
                            i.delete()
                        except RuntimeError as error:
                            if str(error) == "entity is deleted":
                                pass
                            else:
                                raise
                        counter += 1
                        if counter > 100:
                            self.spec.commit()
                            counter = 0
            self.spec.commit()
            if not keep_spec:
                r.delete()
            else:
                Logme()("Some data wasn't rolled back. Keeping Rollback "
                        "Specification.", 'INFO')

    # ######  When SPR 291568 is done, this should be replaced with acm #######
    def rollback_data(self, entity, i):
        try:
            is_instr = FBDPCommon.record_type(entity) == 'Instrument'
            if FBDPCommon.is_acm_object(entity):
                if is_instr or entity.Instrument():
                    self.referred_ins = (is_instr and entity.Oid() or
                        entity.Instrument().Oid())
            elif entity.insaddr:
                self.referred_ins = (is_instr and entity.insaddr or
                        entity.insaddr.insaddr)
        except:
            pass
        if not self.instruments or (self.referred_ins in self.instruments):
            if i.operation == 'Create':
                if self.void == 'Void':
                    if FBDPCommon.record_type(entity) == 'Trade':
                        e = FBDPCommon.clone(entity)
                        if FBDPCommon.is_acm_object(e):
                            e.Status = 'Void'
                        else:
                            e.status = 'Void'
                        try:
                            FBDPCommon.commit(e)
                        except:
                            Logme()('Failed to void %s' %
                                    (self.encapsulateAttribute(entity)),
                                    'WARNING')
                            self.keep_rd = True
                        else:
                            Logme()('Voided: %s' %
                                    (self.encapsulateAttribute(entity)))
                else:
                    #deletes with ael
                    if FBDPCommon.record_type(entity) != 'Trade':
                        try:
                            FBDPCommon.delete(entity)
                            Summary().ok(entity, Summary().DELETE)
                        except Exception as e:
                            e_str = self.encapsulateAttribute(entity)
                            Logme()('failed to delete %s. Got exception %s'
                                    % (e_str, str(e)), 'WARNING')
                            Summary().fail(entity, Summary().DELETE)
                    else:
                        # use the old ael deletion for trades.
                        e_ael = eval('ael.%s[%d]' %
                            (FBDPCommon.record_type(entity),
                            FBDPCommon.getPrimaryKey(entity)))
                        e_str = self.encapsulateAttribute(entity)
                        mirrorTrdnbr = self.getMirrorTrdnbr(e_ael)
                        if FBDPCommon.delete_object(e_ael, 0):
                            Logme()('Deleted: %s' % e_str)
                            self.logMirrorDelete(mirrorTrdnbr)
                        else:
                            Logme()('Not possible to delete %s.' % e_str,
                                'WARNING')
                            self.keep_rd = True
            elif i.operation == 'Update':
                Logme()('Entity: %s' % self.encapsulateAttribute(entity))
                if FBDPCommon.is_acm_object(entity) and \
                            entity.IsKindOf(acm.FBusinessProcess):
                    previousState = entity.CurrentStep(
                                ).PreviousStep().State().Name()
                    entity.ForceToState(
                                previousState, 'Roll back')
                    e = entity
                else:
                    e = FBDPCommon.clone(entity)
                    attribs = eval(i.get_attributes()[:i.size])
                    if 'archive_status' in attribs or 'ArchiveStatus' in attribs:
                        a_status = (('archive_status' in attribs) and
                                'archive_status' or 'ArchiveStatus')
                        self.entityIsArchived = eval(attribs[a_status])
                        if self.entityIsArchived:
                            archive_children(e)
                        else:
                            dearchive_children(e)
                    for k in attribs.keys():
                        if k in ['UpdateUser', 'UpdateTime']:
                            continue
                        if k == 'UpdateSource' and FBDPCommon.record_type(
                                                    e) == 'CorpAction':
                            continue
                        FBDPCommon.set_attr(e, k, eval(attribs[k]))
                        if k in ['archive_status', 'ArchiveStatus']:
                            Summary().ok(e, (eval(attribs[k]) and Summary().ARCHIVE
                                    or Summary().DEARCHIVE), None)
                        Logme()(' Attribute: %s' % k)
                # This try statement was entered because rollback tried to
                # update a price with a deleted instrument.  Maybe this needs
                # to be handled in a better way.
                try:
                    FBDPCommon.commit(e, entity)
                    if i.operation == 'Update':
                        acm.PollDbEvents()
                except RuntimeError as error:
                    Logme()('Failed to update %s, %s.' %
                            (self.encapsulateAttribute(entity), error),
                            'WARNING')
                    self.keep_rd = True
                else:
                    if self.entityIsArchived:
                        entity = None
        else:  # filtered out by instruments
            self.keep_rd = True

    def getMirrorTrdnbr(self, aelObj):
        if aelObj and aelObj.record_type == 'Trade':
            if aelObj.mirror_trdnbr:
                return aelObj.mirror_trdnbr.trdnbr
        return 0

    def logMirrorDelete(self, mirrorTrdnbr):
        if mirrorTrdnbr and not ael.Trade[mirrorTrdnbr]:
            Logme()('Deleted mirror Trade %s' % mirrorTrdnbr)


class RollbackInfo(Rollback):

    def __str__(self):
        return repr(self)


class RollbackWrapper(RollbackInfo):
    """
    This wrapper can be used more efficiently than the traditional way using
    inheritance.  With this wrapper, you are able to add rollback information
    from multiple scripts, and its implementation is also more intuitive.

    To use this wrapper, create an instance of it, ie
        rollback = RollbackWrapper()

    To add information to the rollback instance, use the functions:
        rollback.add(entity, attribs, op)
        rollback.add(trade, attribs, op)
    where
        entity - the entity considered
        attribs - an array of attributes that are changed
        op - operation, any of the values "Update", "Create" and "Delete"

    To get the traditional summary in the end of the log, you should also
    end using the function
        rollback.end()

    for example:
        rollback.add_trade(t)   (op default to "Create")
        rollback.add(ca, ['status', 'name'])  (op default to "Adjust")

    Observe: When operation is "Create" or "Update", the entity is committed
    to the database automatically. There is therefore no need to commit it
    after sending it in to the rollback.
    """

    def __init__(self, rollbackName=None, Testmode=0, param={}):
        importlib.reload(FBDPCommon)
        Rollback.Testmode = Testmode
        self.ael_variables_dict = param
        if rollbackName:
            self.initSpec(rollbackName)

    def end(self):
        Summary().log(self.ael_variables_dict)
        Logme()(None, 'FINISH')


class RollbackAutoTransaction:

    def __init__(self, rollback):
        self.rollback = rollback

    def __enter__(self):
        self.rollback.beginTransaction()

    def __exit__(self, typ, value, traceback):
        self.rollback.abortTransaction()
        return False
