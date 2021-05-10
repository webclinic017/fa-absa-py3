
import acm

mapping={"Bond":"FI",
  "NCD":"FI",
  "NCC":"FI",
  "FRN":"FI",
  "IndexLinkedBond":"FI",
  "Stock":"EQ",
  "ETF":"EQ",
  "CD":"FI",
  "Deposit":"Cash"}

def PSCollateralType(instrument):
    if instrument.InsType() in mapping:
        return mapping[instrument.InsType()]
    return "Cash"
