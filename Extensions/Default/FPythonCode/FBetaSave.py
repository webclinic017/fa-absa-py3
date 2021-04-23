"""
 FBetaSave

 This module saves a beta value from the Trading Manager into a mapped Correlation 
 Matrix (with the Correlation Type equal to 'Beta').
"""
import acm
import ael


def saveBeta(invokationInfo):
    cells = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    for cell in cells:
        tag = cell.Tag()
        column = cell.Column()
        columnId = column.ColumnId()
        context = column.Context().Name()
        if str(columnId) == "Beta":
            row = cell.RowObject()
            instrument = row.Instrument()
            if instrument.InsType() == "Stock":
                mappedCorrelationMatrix = acm.GetCalculatedValueFromString(instrument, 
                    context, 'correlationMatrix', tag).Value()
                if mappedCorrelationMatrix != None:
                    if mappedCorrelationMatrix.Type() == "Beta":
                        betaIndexChosen = acm.GetCalculatedValueFromString(instrument, 
                            context, 'betaIndexChosen', tag).Value()
                        betaValue = cell.Evaluator().Value()
                        correlationCell = mappedCorrelationMatrix.GetCorrelation(instrument, betaIndexChosen)
                        if correlationCell != None and correlationCell.CorrelationMatrix() != None:
                            correlationCell.Beta(betaValue)
                            correlationCell.Commit()
                        else:
                            acm.Log(instrument.Name() + ": The stock is not included in the mapped Correlation Matrix '" + mappedCorrelationMatrix.Name() + "'")    
                    else:
                        acm.Log(instrument.Name() + ': Can not save Beta value since Correlation Matrix type is not Beta.' )
            else:
                acm.Log(instrument.Name() + ': Only Beta values for Stocks can be saved.' )
            
