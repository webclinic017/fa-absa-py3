
""" Compiled: 2017-03-16 11:22:19 """

#__src_file__ = "extensions/BrokerageRisk/etc/ECBCentConversion.py"
import acm

def CreateCentConversion(eii):
    #To add a currency - cent conversion, add the currency ISO name, three letters for minor unit and potential size (100 is default)
    currencies =   [("USD", "USC"),
                    ("EUR", "EUC"),
                    ("GBP", "GBX"),
                    ("INR", "INP"),
                    ("AUD", "AUC"),
                    ("CAD", "CAC"),
                    ("SGD", "SGC"),
                    ("CHF", "CHR"),
                    ("MYR", "MYS"),
                    ("JPY", "JPS"),
                    ("CNY", "CNJ", 10),
                    ("NZD", "NZC"),
                    ("THB", "THS"),
                    ("HUF", "HUX"),
                    ("AED", "AEF"),
                    ("HKD", "HKC"),
                    ("MXN", "MXC"),
                    ("ZAR", "ZAC"),
                    ("PHP", "PHS"),
                    ("SEK", "SEO"),
                    ("IDR", "IDS"),
                    ("SAR", "SAH"),
                    ("BRL", "BRC"),
                    ("TRY", "TRK"),
                    ("KES", "KEC"),
                    ("KRW", "KRJ"),
                    ("EGP", "EGX"),
                    ("IQD", "IQF", 1000),
                    ("NOK", "NOO"),
                    ("KWD", "KWF", 1000),
                    ("RUB", "RUK"),
                    ("DKK", "DKO"),
                    ("PKR", "PKP"),
                    ("ILS", "ILA"),
                    ("PLN", "PLG"),
                    ("QAR", "QAD"),
                    ("OMR", "OMB", 1000),
                    ("COP", "COC"),
                    ("CLP", "CLC"),
                    ("TWD", "TWJ", 10),
                    ("ARS", "ARC"),
                    ("CZK", "CZH"),
                    ("VND", "VNH"),
                    ("MAD", "MAS"),
                    ("JOD", "JOQ"),
                    ("BHD", "BHF", 1000),
                    ("XOF", "XOC"),
                    ("LKR", "LKC"),
                    ("UAH", "UAK"),
                    ("NGN", "NGK"),
                    ("RON", "ROB"),
                    ("BDT", "BDP"),
                    ("PEN", "PEC"),
                    ("GEL", "GET"),
                    ("XAF", "XAC"),
                    ("FJD", "FJC"),
                    ("VEF", "VEC"),
                    ("BYR", "BYK"),
                    ("HRK", "HRL"),
                    ("UZS", "UZT"),
                    ("BGN", "BGS"),
                    ("DZD", "DZS"),
                    ("IRR", "IRD"),
                    ("DOP", "DOC"),
                    ("CRC", "CRX"),
                    ("SYP", "SYX"),
                    ("LYD", "LYX", 1000),
                    ("JMD", "JMC"),
                    ("MUR", "MUC"),
                    ("GHS", "GHG"),
                    ("AOA", "AOC"),
                    ("UYU", "UYC"),
                    ("AFN", "AFP"),
                    ("LBP", "LBX"),
                    ("XPF", "XPC"),
                    ("TTD", "TTC"),
                    ("TZS", "TZC"),
                    ("ALL", "ALQ"),
                    ("XCD", "XCC"),
                    ("GTQ", "GTC"),
                    ("NPR", "NPP"),
                    ("BOB", "BOC"),
                    ("ZWD", "ZWC"),
                    ("BBD", "BBC"),
                    ("CUC", "CUX"),
                    ("LAK", "LAA"),
                    ("BND", "BNC"),
                    ("BWP", "BWT"),
                    ("HNL", "HNC"),
                    ("PYG", "PYC"),
                    ("ETB", "ETS"),
                    ("NAD", "NAC"),
                    ("PGK", "PGT"),
                    ("SDG", "SDP"),
                    ("MOP", "MOH", 10),
                    ("NIO", "NIC"),
                    ("KZT", "KZX"),
                    ("BAM", "BAF"),
                    ("GYD", "GYC"),
                    ("YER", "YEF"),
                    ("MGA", "MGI", 5),
                    ("KYD", "KYC"),
                    ("MZN", "MZC"),
                    ("RSD", "RSP"),
                    ("SCR", "SCC"),
                    ("AMD", "AML"),
                    ("AZN", "AZQ"),
                    ("SLL", "SLC"),
                    ("TOP", "TOS"),
                    ("BZD", "BZC"),
                    ("MWK", "MWT"),
                    ("GMD", "GMB"),
                    ("BIF", "BIC"),
                    ("SOS", "SOX"),
                    ("HTG", "HTC"),
                    ("GNF", "GNC"),
                    ("MVR", "MVL"),
                    ("MNT", "MNM"),
                    ("TJS", "TJT"),
                    ("KPW", "KPC"),
                    ("MMK", "MMP"),
                    ("LRD", "LRC"),
                    ("GIP", "GIX"),
                    ("MDL", "MDB"),
                    ("CUP", "CUC"),
                    ("KHR", "KHK", 10),
                    ("MKD", "MKX"),
                    ("MRO", "MRK"),
                    ("SZL", "SZC"),
                    ("CVE", "CVC"),
                    ("SVC", "SVX"),
                    ("BSD", "BSC"),
                    ("RWF", "RWC"),
                    ("BTN", "BTC"),
                    ("KMF", "KMC"),
                    ("WST", "WSS"),
                    ("SPL", "SPC"),
                    ("FKP", "FKX"),
                    ("SHP", "SHS"),
                    ("JEP", "JEX"),
                    ("TVD", "TVC"),
                    ("IMP", "IMX"),
                    ("GGP", "GGX"),
                    ("ZMW", "ZMN")]

    market = acm.FMarketPlace['ECBFIX'] or CreateMarket('ECBFIX')

    # Helper function to unpack tuples of varying length, defaulting the ratio result to 100 if not provided
    def UnpackCurrencyTuple(major, minor, *ratio):
        return major, minor, ratio[0] if ratio else 100

    for currencyInfo in currencies:
        currName, centName, ratio = UnpackCurrencyTuple( *currencyInfo ) # returns 100 as ratio if no ratio is provided
        currency = acm.FCurrency[currName]
        if not currency:
            # Silently skip any currency in the list above which is NOT found in the ADS (assuming it is not set up for a reason, and because we don't have enough information about the instrument here)
            continue

        # Check if there already is a conversion ratio in place - if so, don't create any new entries
        prices = [ price for price in currency.Prices() if price.Currency().Name() == centName and price.Market() == market ]
        if not prices:
            # Conversion ratio (stored as a price) not found - create entries
            acm.BeginTransaction()
            try:
                centCurrency = acm.FCurrency[centName] or CommitCurrencyClone(currency.Clone(), centName)
                price = acm.FPrice()
                price.Instrument(currency)
                price.Currency(centCurrency)
                price.Market(market)

                price.Bid(ratio)
                price.Ask(ratio)
                price.Day(acm.Time.DateNow())

                price.Commit()
                acm.CommitTransaction()
            except:
                acm.AbortTransaction()
                print ('*** Could NOT create information for %s/%s' % ( currName, centName ))
                #raise


def CommitCurrencyClone(centCurrency, centName):
    print ('Creating new currency %s' % centName)
    if acm.FInstrument[centName]:
        error = 'Name specified for cent currency (%s) already in use for instrument of type %s' % ( centCurrency.Name(), acm.FInstrument[centName].InsType() )
        print (error)
        raise RuntimeError(error)

    centCurrency.Name(centName)
    centCurrency.Commit()

    # Must remove any InstrumentAlias for the cloned currency, since it will create a duplicate conflict in SQL (and we don't know the proper way to create an alternative alias here since this will be specific to the installation)

    for alias in list( centCurrency.Aliases() ):
        alias.Delete()

    return centCurrency


def CreateMarket(name):
    mkt = acm.FMarketPlace()
    mkt.Name(name)
    mkt.NotTrading(True)
    mkt.Commit()
