"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Upload rate and held information from csv file to Front Arena
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Natasha Williams
DEVELOPER               :  Peter Fabian
CR NUMBER               :  620455
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
"""

import acm
import sl_auto_return_run
import sl_rates
import FRunScriptGUI
import PS_TimeSeriesFunctions

class SBLRatesUploader(object):

    def __init__(self, rateFilePath):
        firstRateColumn = 3
        self.timeSeriesNames = (sl_rates.SblRates._SBL_RATE_KEY, sl_rates.SblRates._SBL_HELD_KEY)
        self.SBLRatesFile = sl_rates.SblFileRates(rateFilePath, firstRateColumn)
        self.errors = []

    def removeOldRates(self, instrumentsToDelete):
        deletedValue = sl_rates.SblTimeSeriesRates.RateDeleted()
        date = acm.Time().DateNow()
        for insName in instrumentsToDelete:
            for timeSeriesName in self.timeSeriesNames:
                try:
                    instrument = acm.FInstrument[insName]
                    PS_TimeSeriesFunctions.UpdateTimeSeriesValue(timeSeriesName, instrument, deletedValue, date)
                except Exception as e:
                    self.errors.append("Couldn't update rate for instrument %s and date %s with value %g: %s"
                                       % (insName, str(date), deletedValue, str(e)))


    def _instrumentsInTimeSeries(self, timeSeriesName):
        instruments = set()
        timeSeriesSpec = acm.FTimeSeriesSpec[timeSeriesName]
        timeSeriesItems = acm.FTimeSeries.Select('timeSeriesSpec=%i' % (timeSeriesSpec.Oid()))
        for timeSeriesEntry in timeSeriesItems:
            try:
                insName = acm.FInstrument[timeSeriesEntry.Recaddr()].Name()
                instruments.add(insName)
            except AttributeError as e:
                self.errors.append("Instrument with insaddr %s not found"
                                   % (timeSeriesEntry.Recaddr()))
        return instruments


    def uploadRates(self):
        # some forced action here, sorry for that, it's in the name of code reuse
        self.SBLRatesFile._readRates()
        self._rates = self.SBLRatesFile._rates

        newInstruments = set(self._rates.keys())
        oldInstruments = set()
        for timeSeriesName in self.timeSeriesNames:
            oldInstruments |= self._instrumentsInTimeSeries(timeSeriesName)
        # here <<Internal>> and <<Spread>> are not included, since they're only in newInstruments
        instrumentsToDelete = oldInstruments - newInstruments


        print("'Removing' old timeseries data")
        self.removeOldRates(instrumentsToDelete)
        print("Done")

        # upload the internal rate & spread
        internalRate = self._rates[sl_rates.SblRates._INTERNAL_KEY].rate
        spread = self._rates[sl_rates.SblRates._SPREAD_KEY].rate
        self.updateInternalRates(internalRate, spread)
        # upload external rate
        self.updateExternalRates(self._rates)
        print("Rates updated successfully")


    def updateInternalRates(self, internalRate=None, spread=None):
        autoReturnTasks = acm.FAelTask.Select("moduleName='sl_auto_return_run'")
        sweepingTasks = acm.FAelTask.Select("moduleName='sl_run_sweeping_query_folder'")
        tasks = autoReturnTasks.Union(sweepingTasks)
        for task in tasks.AsList():
            try:
                params = task.Parameters()
                if internalRate:
                    # change internal rate
                    params.RemoveKeyString(sl_auto_return_run.internalRateKey)
                    params.AtPutStrings(sl_auto_return_run.internalRateKey, str(internalRate))
                    print(("Updating task '%s' with Internal Rate %f" % (task.Name(), internalRate)))

                if spread:
                    # change the spread
                    params.RemoveKeyString(sl_auto_return_run.internalSpreadKey)
                    params.AtPutStrings(sl_auto_return_run.internalSpreadKey, str(spread))
                    print(("Updating task '%s' with Spread %f" % (task.Name(), spread)))

                if internalRate or spread:
                    # commit changes
                    params.Commit()
                    task.Parameters(params)
                    task.Commit()
                    print("Update successful")

            except Exception as e:
                self.errors.append("Could not update task %s, the internal rate and/or spread were not updated! %s" % (task.Name(), str(e)))
                raise

    def updateExternalRates(self, SBLRates):
        # SBLRates: insid -> SblRateTuple
        date = acm.Time().DateNow()
        for (insName, rateTuple) in SBLRates.iteritems():
            if insName and insName not in (sl_rates.SblRates._INTERNAL_KEY, sl_rates.SblRates._SPREAD_KEY):
                try:
                    instrument = acm.FInstrument[insName]
                    # update rate
                    PS_TimeSeriesFunctions.UpdateTimeSeriesValueForce(sl_rates.SblRates._SBL_RATE_KEY, instrument, float(rateTuple.rate), date)
                    # update held
                    SBL_Held = 1 if not rateTuple.autoReturn else 0
                    PS_TimeSeriesFunctions.UpdateTimeSeriesValueForce(sl_rates.SblRates._SBL_HELD_KEY, instrument, SBL_Held, date)

                    print(("Instrument '%s' updated. Rate: %f, Held: %s" % (insName, rateTuple.rate, str(not rateTuple.autoReturn))))
                except Exception as e:
                    self.errors.append("Couldn't update rate for instrument %s and date %s: %s"
                          % (insName, str(date), str(e)))


SBLRatesFilePathKey = "SBLRatesFile"
ratesFileSelection = FRunScriptGUI.InputFileSelection("*.csv")
ratesFileSelection.SelectedFile(r'Y:\Jhb\Arena\Data\SecurityLending\Rates\SBL_Rates.csv')

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [SBLRatesFilePathKey, 'SBL Rates file location', ratesFileSelection, None, ratesFileSelection, 1, 1, 'Location of SBL_Rates.csv file.', None, 1],
]

def ael_main(parameters):
    SBLRatesFilePath = str(parameters[SBLRatesFilePathKey].SelectedFile())

    try:
        uploader = SBLRatesUploader(SBLRatesFilePath)
        uploader.uploadRates()
        if not uploader.errors:
            print("Completed successfully")
        else:
            print("="*50)
            print("Errors:")
            print("\n" + "\n".join(uploader.errors))
            print("="*50)
    except Exception, ex:
        print(str(ex))

