""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorpActionsWorkbenchTableEventAdapter.py"
import acm
import ael
from FCorpActionsWorkbenchLogger import logger

LISTEN_EVENTS = ['insert', 'delete']

class TableListener(object):

    def __init__(self, tableName):
        self._started = False
        self._tableName = tableName

    def StartSubscription(self):
        if not self._started:
            aelTable = getattr(ael, self._tableName)
            if aelTable:
                aelTable.subscribe(self._EntityNotify, self)
            else:
                msg = "TableListener.StartSubscription() cannot recognise table {0}".format(self._tableName)
                logger.error(msg)
                return
            self._started = True
        else:
            msg = "TableListener.StartSubscription() Already subscribing table {0}".format(self._tableName)
            logger.debug(msg)

    def EndSubscription(self):
        if self._started:
            aelTable = getattr(ael, self._tableName)
            if aelTable:
                aelTable.unsubscribe(self._EntityNotify, self)
            else:
                msg = "TableListener.EndSubscription() cannot recognise table {0}".format(self._tableName)
                logger.error(msg)
                return
            self._started = False
        else:
            msg = "TableListener.EndSubscription() Already ended table {0}".format(self._tableName)
            logger.debug(msg)

    # ---- AEL Subscription ----

    @staticmethod
    def _EntityNotify(obj, ael_ent, _arg, event):
        try:
            #print '_EntityNotify:ael entity', ael_ent
            #print '_EntityNotify:arg', _arg
            #print '_EntityNotify:event', event
            #if not hasattr(ael_ent, 'insaddr'):
            #    return
            if not _arg:
                return
            acmEntity = acm.Ael.AelToFObject(ael_ent)
            _arg._OnEntity(acmEntity, event)
        except Exception as exc:
            logger.error("TableListener._EntityNotify Exception: %s", exc)

    # ---- Methods to be implemented in sub classes ----

    def _OnEntity(self, acmEntity, event):
        raise NotImplementedError
