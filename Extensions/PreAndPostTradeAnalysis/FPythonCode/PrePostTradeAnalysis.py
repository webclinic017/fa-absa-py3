
import acm

def onStartExecutionTime(row, col, cell, val, operation):
    if row and (row.IsKindOf('FSalesOrder') or row.IsKindOf('FOrderProgram')):
        row.StartExecutionTime(val)
        if row.StartExecutionTime() < row.EndExecutionTime():
            row.Changed()
            
def onEndExecutionTime(row, col, cell, val, operation):
    if row and (row.IsKindOf('FSalesOrder') or row.IsKindOf('FOrderProgram')):
        row.EndExecutionTime(val)
        if row.StartExecutionTime() < row.EndExecutionTime():
            row.Changed()

def postChangeBenchmarkPriceType(row, col, cell, val, operation):
    if row and row.IsKindOf('FPrePostTradeAnalysis'):
        row.BenchmarkPriceType(val)
