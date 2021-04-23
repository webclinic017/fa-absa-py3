"""
This ATS handles all outgoing SWIFT messages from python scripts to be placed onto MQ
This is kept as a seperate ATS script to cater for future outgoing SWIFT placements

HISTORY
=========================================================================================
Date        Change no       Developer       Description
-----------------------------------------------------------------------------------------
XXXXXXXXXX  XXXXXXX         Rohan vd Walt   Initial Implementation
2016-11-28  CHNG0004147753  Gabriel Marko   Changed from *task mode* to *module mode* ATS
"""

import FOperationsUtils as Utils
import acm
import ael
import sys
import time

from demat_isin_mgmt import send_isin_request
from Queue import Queue


ISIN_MNGMT_BPS = 'MM ISIN Management TBS'
processing_queue = Queue()

def _listener(obj, entity, arg, operation):
    """Adds the entity and the original entity to the processing queue queue."""
    entity = acm.FBusinessProcess[entity.seqnbr]
    processing_queue.put(entity)


def start():
    Utils.Log(True, "Python version: %s" % (sys.version))

    # Recovery procedure: Put all not processed BusinessProcesses to the
    # processing_que

    Utils.Log(True, "Putting not processed BusinessProcesses to the processing queue")
    not_processed_bps = acm.FStoredASQLQuery[ISIN_MNGMT_BPS].Query().Select()
    for bp in not_processed_bps:
        processing_queue.put(bp)

    Utils.Log(True, "Subscribing to BusinessProcess table")
    ael.BusinessProcess.subscribe(_listener)

    Utils.Log(True, "MQ Custum Swift Out ATS started at %s" % (time.ctime()))
    return True


def stop():
    ael.BusinessProcess.unsubscribe(_listener)
    Utils.Log(True, "Unsubscribed from BusinessProcess table")
    Utils.Log(True, "Stopping ATS")


def work():
    while not processing_queue.empty():
        entity = processing_queue.get()
        try:
            if acm.FStoredASQLQuery[ISIN_MNGMT_BPS].Query().IsSatisfiedBy(entity):
                send_isin_request(entity)
        except Exception as ex:
            print('Exception:', ex)
