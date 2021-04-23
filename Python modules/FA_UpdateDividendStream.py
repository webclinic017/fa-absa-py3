import acm
import sys

def UpdateDivStream(historicalDate):
    stocks=acm.FStock.Select('')

    for s in stocks:
        parName=s.MappedDividendStream().ParameterName()
        if parName:
            for d in s.MappedDividendStream().Parameter().Dividends():
                # historical date is date of the db dump
                if d.ExDivDay() < historicalDate:
                    print(parName, d.ExDivDay(), d.TaxFactor(), file=sys.stderr)
                    d.TaxFactor=0.0
                    d.Commit
