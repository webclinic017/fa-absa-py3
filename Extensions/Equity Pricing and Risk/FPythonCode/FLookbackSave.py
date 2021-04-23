import acm
import ael

def saveLookbackExtremeValue(invokationInfo):
    cells = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    for cell in cells:
        column = cell.Column()
        columnId = column.ColumnId()
        if str(columnId) == "Lookback Extreme Value":
            row = cell.RowObject()
            if row.IsKindOf(acm.FSingleInstrumentAndTrades) or row.IsKindOf(acm.FPriceLevelRow):
                instrument = row.Instrument()
                instype=instrument.InsType()            
                if instype=='Option' or instype=='Warrant':
                    if instrument.IsExotic():
                        if instrument.IsLookback():
                            extVal = cell.Evaluator().Value()
                            instrument.Exotic().LookbackExtremeValue=extVal
                            instrument.Exotic().Commit()
                            ael.log(instrument.Name() + ": Saved %.2f %s as Extreme Value."%(extVal.Number(), extVal.Unit().Text()))
                        else:
                            ael.log(instrument.Name() + ": Can only save lookback extreme value for Lookback Options.")
                    else:
                        ael.log(instrument.Name() + ": Can only save lookback extreme value for Lookback Options.")
                else:
                    ael.log(instrument.Name() + ": Can only save lookback extreme value for Lookback Options.")
