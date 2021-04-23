"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementInCallbacksBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module. User can override the default logic in derived
    class FSecuritySettlementInCallbacks
    Business process conditional_entry/exit and on_entry/exit callbacks.

FUNCTIONS:
    For sample state xxx there are always the four standard extension points:
        condition_entry_state_xxx():
            To control if all the pre-requisites to performing the action and
            entering the state are defined.
        on_entry_state_xxx():
            Is the place to perform the action.
            For example, the on_ entry_state_matched is the place to set the
            confirmation status to Matched
        condition_exit_state_xxx():
            To control that all pre-requisites for performing the next action
            are fulfilled.
        on_exit_state_xxx():
             Is the place to reset values that you set in the state entry, if
             you are leaving the state to go backwards in the workflow.
             For example if you exit from the "Matched" state to go and re-pair,
             or to manually cancel, then you would want to remove the
             confirmation Matched status

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSwiftMLUtils
import FMT54XProcessFunctions

class FSecuritySettlementInCallbacksBase(object):
    def __init__(self):
        pass

    def getStateBeforePairing(self, bpr):
        prevStatus = None
        for step in bpr.Steps():
            if step.State().Name() == 'Paired':
                diaryEntry = step.DiaryEntry()
                if diaryEntry:
                    param = diaryEntry.Parameters()
                    if param:
                        prevStatus = param.At('AcmObjectStatusBeforePairing', None)
                        break
        return prevStatus

    def isUnpairAllowed(self, sett):
        '''
            Check if either all the children at a level are in Cancelled or if one child is in Replaced,
            recursively check further its children.

            1. S2 should be allowed to be unpaired
                                     S1
                         --------------------------
                        |                         |
                       S2(Settled)               S3(Replaced)
                                         ------------------------
                                        |                       |
                                       S4(Cancelled)           S5(Cancelled)


            2. S2 should NOT be allowed to be unpaired
                                     S1
                         --------------------------
                        |                         |
                       S2(Settled)               S3(Replaced)
                                         ------------------------------
                                        |                             |
                                       S4(Acknowledged)              S5(Replaced)
                                                             -----------------------
                                                            |                       |
                                                           S4(Cancelled)           S5(Cancelled)
        '''

        if sett.Status() == 'Replaced':
            for child in sett.PartialChildren():
                if not self.isUnpairAllowed(child):
                    return False
            return True
        elif sett.Status() == 'Cancelled':
            return True
        else:
            return False

    # The context parameter is an instance of FBusinessProcessCallbackContext
    # Conditions return True or False
    # Name convention is
    # 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def condition_entry_state_ready(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_paired(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_settled(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_unpaired(self, context):
        '''Adding a check to not enable unpair menu for level 1 partial if there is a level 2 partial'''
        bp = context.CurrentStep().BusinessProcess()
        acm_object = FSwiftMLUtils.get_acm_object_from_bpr(bp)
        if acm_object and acm_object.PartialParent() is not None:
            parent = acm_object.PartialParent()
            sibling = [each for each in parent.PartialChildren() if each != acm_object][0]

            if sibling.Status() == 'Replaced' and not self.isUnpairAllowed(sibling):
                return False
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_ignored(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_difference(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_tradegenerated(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_partialmatch(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_manuallycancelled(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

    def condition_entry_state_manuallycorrected(self, context):
        return FSwiftMLUtils.HasUserRights(FSwiftMLUtils.get_operation_name_from_bpr_context(context))

# ------------------------------------------------------------------------------
    def condition_exit_state_ready(self, context):
        return True

    def condition_exit_state_paired(self, context):
        return True

    def condition_exit_state_settled(self, context):
        return True

    def condition_exit_state_unpaired(self, context):
        return True

    def condition_exit_state_ignored(self, context):
        return True

    def condition_exit_state_difference(self, context):
        return True

    def condition_exit_state_tradegenerated(self, context):
        return True

    def condition_exit_state_partialmatch(self, context):
        return True

    def condition_exit_state_manuallycancelled(self, context):
        return True

    def condition_exit_state_manuallycorrected(self, context):
        return True
# ------------------------------------------------------------------------------
    # Entry/Exit callbacks do not return anything
    # Name convention is
    # 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
    def on_entry_state_ready(self, context):
        pass

    def on_entry_state_paired(self, context):
        try:
            # In case user want to pair the settlement explicitly, he needs to pass
            # the parameter SettlementNumber during HandleEvent
            # e.g. Unpair settlement and then Pair with new settlement
            set_num = context.Parameters().AtString('SettlementNumber')
            if set_num:
                set_obj = acm.FSettlement[set_num.AsString()]
                notifier.INFO('Linking businessprocess %d to acm object %s:%d'%(context.CurrentStep().BusinessProcess().Oid(), set_obj.ClassName(), set_obj.Oid()))
                FSwiftMLUtils.FSwiftExternalObject.link_acm_object(context.CurrentStep().BusinessProcess(), set_obj)
                #FSwiftMLUtils.link_acm_object(context.CurrentStep().BusinessProcess(), set_obj)
        except Exception as e:
                notifier.ERROR("Exception in on_entry_state_paired %s"%e)
                notifier.DEBUG(str(e), exc_info=1)

    def on_entry_state_settled(self, context):
        try:
            self.set_settlement_attributes(context)
        except Exception as error:
            notifier.ERROR("Exception in on_entry_state_settled %s" % str(error))
            notifier.DEBUG(str(error), exc_info=1)


    def CommitObject(self, acm_object):
        acm.BeginTransaction()
        try:
            FSwiftMLUtils.commit_and_retry(acm_object)
            for child in acm_object.Children():
                FSwiftMLUtils.commit_and_retry(child)
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise Exception("Error occured when committing %s" % str(e))


    def on_entry_state_unpaired(self, context):
        try:
            bp = context.CurrentStep().BusinessProcess()
            acm_object = FSwiftMLUtils.get_acm_object_from_bpr(bp)
            if acm_object:
                mt_object = FSwiftMLUtils.create_their_object_from_bpr(bp)
                try:
                    import FSwiftOperationsAPI
                    FSwiftOperationsAPI.ClearSettledDataOnHierarchy(acm_object)
                    self.CommitObject(acm_object)
                except ImportError as e:
                    notifier.ERROR("Can not import extension FSwiftOperationsAPI")
                except Exception as e:
                    notifier.ERROR("Error occurred while using FSwiftOperationsAPI: %s"%str(e))

                if acm_object.Status() not in ['Replaced']:
                    try:
                        prevStatus = self.getStateBeforePairing(bp)
                        acm_object.Status(prevStatus)
                        FSwiftMLUtils.commit_and_retry(acm_object)
                    except Exception as e:
                        notifier.ERROR("Can not move Settlement %s from status %s to %s status" % (acm_object.Oid(), acm_object.Status(), prevStatus))
                        notifier.DEBUG(str(e), exc_info=1)

                FSwiftMLUtils.unlink_references(bp)

                #Undo partial settlement applicable only if acm object is child of partial, acm_object is in Authorised state, siblings are also in authorised state.
                if acm_object.PartialParent() is not None:
                    parent = acm_object.PartialParent()
                    sibling = [each for each in parent.PartialChildren() if each != acm_object][0]
                    acm_version = FSwiftMLUtils.get_acm_version()

                    if  ( acm_version > 2017.1 and acm_object.Status() == 'Authorised' and sibling.Status() == 'Authorised' and acm_object.PartialSettlementType() == 'NPAR') or \
                        ( acm_version > 2017.2 and acm_object.Status() == 'Acknowledged' and sibling.Status() == 'Acknowledged' and acm_object.PartialSettlementType() == 'PART'):
                        undoPartialSettlement = acm.FUndoPartialSettlement(acm_object)
                        undoPartialSettlement.Execute()
                        undoPartialSettlement.CommitResult()


        except Exception as error:
            notifier.ERROR("Error occurred in on_entry_state_unpaired: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)

    def on_entry_state_ignored(self, context):
        pass

    def on_entry_state_difference(self, context):
        try:
            self.set_settlement_attributes(context)
        except Exception as e:
            notifier.ERROR("Error occurred while setting add info on_entry_state_difference: %s" % str(e))



    def on_entry_state_tradegenerated(self, context):
        pass


    def on_entry_state_partialmatch(self, context):
        pass


    def on_entry_state_manuallycancelled(self, context):
        pass


    def on_entry_state_manuallycorrected(self, context):
        pass

# ------------------------------------------------------------------------------
    def on_exit_state_ready(self, context):
        pass

    def on_exit_state_paired(self, context):
        pass

    def on_exit_state_settled(self, context):
        pass

    def on_exit_state_unpaired(self, context):
        pass

    def on_exit_state_ignored(self, context):
        pass

    def on_exit_state_difference(self, context):
        pass

    def on_exit_state_tradegenerated(self, context):
        pass

    def on_exit_state_partialmatch(self, context):
        pass

    def on_exit_state_manuallycancelled(self, context):
        pass

    def on_exit_state_manuallycorrected(self, context):
        pass
# ------------------------------------------------------------------------------
    def supress_payment_message(self, sett_obj):
        try:
            import FSwiftOperationsAPI
            FSwiftOperationsAPI.SuppressPaymentMessageAck(sett_obj)
        except (ImportError, AttributeError):
            try:
                suppressPaymentMessageAck = acm.FSuppressPaymentMessageAck(sett_obj)
                suppressPaymentMessageAck.Execute()
                suppressPaymentMessageAck.CommitResult()
            except Exception as e:
                raise Exception(e)
        except Exception as e:
            notifier.ERROR("Error occurred in supress_payment_message: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def set_settlement_attributes(self, context):
        """ Set the settlement attributes like status, settled amount, settled date"""
        try:
            mt_object = FSwiftMLUtils.create_their_object_from_bpr(context.CurrentStep().BusinessProcess())
            bpr = context.CurrentStep().BusinessProcess()
            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(bpr)
            sett_obj = FSwiftMLUtils.FSwiftExternalObject.get_acm_object_from_ext_object(ext_obj)


            '''
            """ Sample code Customisation for: In case user wants forced trigger into 'Processed' State
                for corresponding MT548, when corresponding
                settlement is in settled state
            """

            ext_object = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = sett_obj, msg_typ='MT548', integration_type='Incoming')
            if ext_object:
                sc_name = FSwiftMLUtils.get_state_chart_name_for_mt_type('MT548', 'In')
                mt_548_bpr = FSwiftMLUtils.get_bpr_from_subject_statechart(ext_object,sc_name)
                import FSecuritySettlementInProcessing
                processing_obj = FSecuritySettlementInProcessing.FSecuritySettlementStatusProcessingAdviceInProcessing(mt_548_bpr)
                processing_obj.trigger_next_event('Done')

            '''

            if FMT54XProcessFunctions.is_partial(mt_object) and sett_obj.PartialParent() is None:
                return

            if sett_obj.Status() == 'Authorised' and FSwiftMLUtils.get_acm_version() < 2017.2:
                self.supress_payment_message(sett_obj)
            try:
                import FSwiftOperationsAPI
                FSwiftOperationsAPI.SetSettledDataOnHierarchy(sett_obj, mt_object.SettledDate(), mt_object.Premium(), mt_object.SettledAmount())
            except (ImportError, AttributeError):
                acm.Operations.SetSettledDataOnHierarchy(sett_obj, mt_object.SettledDate(), mt_object.Premium(), mt_object.SettledAmount())
                self.CommitObject(sett_obj)
        except Exception as error:
            notifier.ERROR("Error occurred in set_settlement_attributes: %s"%str(error))
            notifier.DEBUG(str(error), exc_info=1)

