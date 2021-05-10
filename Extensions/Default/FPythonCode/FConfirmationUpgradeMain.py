""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationUpgradeMain.py"
import acm
import FConfirmationUpgradeDeleteEvent
import FConfirmationUpgradeDeprecatedEvents

from FOperationsUtils import Log
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
from FConfirmationChecksum import CreateChecksum

ael_variables = []

def upgrade_start(parameterDictionary):
    UpgradeChecksum()
    SetExpiryDay()
    FConfirmationUpgradeDeprecatedEvents.UpgradeDeprecatedConfirmations()
    FConfirmationUpgradeDeleteEvent.DeleteDeprecatedEvents()

def ael_main(parameterDictionary):
    Log(True, 'Confirmation upgrade commenced ...')
    upgrade_start(parameterDictionary)
    Log(True, 'Confirmation upgrade completed ...')

def UpgradeChecksum():
    confirmations = acm.FConfirmation.Select('')
    counter = 0

    Log(True, 'Setting check sum on confirmations ...')
    for confirmation in confirmations:
        if confirmation.IsPostRelease():
            confirmation.Checksum(CreateChecksum(confirmation))
            try:
                confirmation.Commit()
                counter += 1
                if (counter % 1000 == 0):
                    Log(True, '%d confirmations updated, please wait ...' % counter)
            except Exception as error:
                Log(True, 'Error when upgrading confirmation %d: %s' % (confirmation.Oid(), error))

    Log(True, 'Check sum update completed. %d confirmations updated' % counter)

def SetExpiryDay():
    confirmations = acm.FConfirmation.Select('')
    counter = 0
    calendar = HelperFunctions.GetDefaultCalendar()
    Log(True, 'Setting expiry day on confirmations ...')

    for confirmation in confirmations:
        createTime = acm.Time.DateFromTime(confirmation.CreateTime())
        expiryDay = calendar.AdjustBankingDays(createTime, 10)
        confirmation.ExpiryDay(expiryDay)
        try:
            confirmation.Commit()
            counter += 1
            if (counter % 1000 == 0):
                Log(True, '%d confirmations updated, please wait ...' % counter)
        except Exception as error:
            Log(True, 'Error when upgrading confirmation %d: %s' % (confirmation.Oid(), error))

    Log(True, 'Expiry day update completed. %d confirmations updated' % counter)

