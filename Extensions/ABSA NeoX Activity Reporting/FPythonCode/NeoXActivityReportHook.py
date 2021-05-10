"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportHook

DESCRIPTION
    This module is used to define the API of a hook used for event-driven Activity Reports to Neox
    (straight-through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959       Ncediso Nkambule        Cuen Edwards            Initial implementation.
2020-11-12      FAOPS-981       Ncediso Nkambule        Cuen Edwards            Update Production file Path.
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import os
import acm
import time
from glob import glob
from logging import getLogger
from datetime import datetime, date
from NeoXActivityReportsUtils import get_fparameter
from EnvironmentFunctions import is_production_environment


LOGGER = getLogger(__name__)


class ActivityReportsNeoxHook(object):
    """
    Definition of a hook used to perform Operations SBL NeoX.
    """
    last_generate_date_time = datetime.now()
    temp_directory = get_fparameter('NeoXParameters', 'neox_temp_directory').AsString()
    if is_production_environment():
        __destination_directory = get_fparameter('NeoXParameters', 'neox_production_directory').AsString()
    else:
        __destination_directory = get_fparameter('NeoXParameters', 'neox_test_directory').AsString()

    final_directory = os.path.join(__destination_directory, date.today().isoformat())
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        os.chmod(final_directory, 0o777)

    def Name(self):
        """
        Get the name of the Operations SBL NeoX Hook.
        """
        raise NotImplementedError()

    def IsTriggeredBy(self, event_object, event_message=None):
        """
        Determine whether or not to trigger the hooks SBL NeoX action/s
        for an event on the specified object.
        """
        raise NotImplementedError()

    def PerformEventProcessing(self, event_object, event_message=None):
        """
        Perform the hooks SBL NeoX action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        raise NotImplementedError()

    def PerformFileProcessing(self):
        raise NotImplementedError()

    def IsTimeForNewFile(self, file_identifier, minutes_limit=10, file_extension=".csv"):
        """
        Perform the hooks SBL NeoX action/s for an event on the specified object.

        Please note that the action does not necessarily occur to the event object itself but may occur to some
        related object/s.
        """
        temp_path = os.path.join(self.temp_directory, file_identifier + ".tmp")
        temp_path_exist_and_has_data = True
        if not os.path.exists(temp_path):
            temp_path_exist_and_has_data = False
        if os.path.exists(temp_path) and os.stat(temp_path).st_size == 0:
            temp_path_exist_and_has_data = False
        if temp_path_exist_and_has_data:
            list_of_files = glob(os.path.join(self.final_directory, r"*{}".format(file_extension)))
            list_of_files = [f for f in list_of_files if file_identifier in f]
            if not list_of_files:
                return True
            latest_file = max(list_of_files, key=os.path.getctime)
            this_time = os.path.getctime(latest_file)
            time_now = time.time()
            time_elapsed = (time_now - this_time) / 60
            LOGGER.debug("The last file was created {} minutes ago.".format(str(int(time_elapsed))))
            if minutes_limit < time_elapsed:
                return True
        return False

    @staticmethod
    def get_trade_from_event_object(event_object):
        trade = None
        if event_object.IsKindOf(acm.FTrade):
            trade = event_object
        if event_object.IsKindOf(acm.FSettlement):
            trade = event_object.Trade()
        if event_object.IsKindOf(acm.FInstrument):
            pass
        return trade
