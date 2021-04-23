import acm
import sys

#Link to be added to the ACMB Context:
#Instrument,Curr,Mapping Type,Parameter Name,Parameter Type
linkList =[['USD', 'AUD', 'Instrument', 'AUD-USD/FX/OPT', 'Yield Curve'],
['USD', 'BRT_CRD_OIL', 'Instrument', 'USD/BRT_CRD_OIL', 'Yield Curve'],
['USD', 'BWP', 'Instrument', 'BWP-USD/FX', 'Yield Curve'],
['USD', 'CAD', 'Instrument', 'USD-CAD/FX', 'Yield Curve'],
['USD', 'CHF', 'Instrument', 'CHF-BASIS', 'Yield Curve'],
['USD', 'COAL', 'Instrument', 'USD/COAL DEPO', 'Yield Curve'],
['USD', 'EUR', 'Instrument', 'EUR-BASIS', 'Yield Curve'],
['USD', 'FO_NWE_1perc_FUEL', 'Instrument', 'FO_NWE_1%_CIF', 'Yield Curve'],
['USD', 'GAS_OIL', 'Instrument', 'ICE_GO', 'Yield Curve'],
['USD', 'GBP', 'Instrument', 'GBP-BASIS', 'Yield Curve'],
['GHS', 'GHS', 'Instrument', 'GHS_CURVE', 'Yield Curve'],
['USD', 'GHS', 'Instrument', 'GHS-FX', 'Yield Curve'],
['USD', 'GO_Med_02_FOB', 'Instrument', 'GO_Med_0.2_FOB', 'Yield Curve'],
['USD', 'JET_AG_FOB_FUEL', 'Instrument', 'JET_AG_FOB', 'Yield Curve'],
['USD', 'JET_FUEL', 'Instrument', 'JET_NWE_FOB', 'Yield Curve'],
['USD', 'JET_Med_FobFUEL', 'Instrument', 'JET_Med_FOB', 'Yield Curve'],
['USD', 'JPY', 'Instrument', 'JPY-BASIS', 'Yield Curve'],
['USD', 'KES', 'Instrument', 'KES-FX_CURVE', 'Yield Curve'],
['USD', 'MAL', 'Instrument', 'USD/MAL DEPO', 'Yield Curve'],
['USD', 'MCU', 'Instrument', 'USD/MCU DEPO', 'Yield Curve'],
['USD', 'MNI', 'Instrument', 'USD/MNI DEPO', 'Yield Curve'],
['USD', 'MPB', 'Instrument', 'USD/MPB DEPO', 'Yield Curve'],
['USD', 'MSN', 'Instrument', 'USD/MSN DEPO', 'Yield Curve'],
['USD', 'MUR', 'Instrument', 'MUR-FX', 'Yield Curve'],
['USD', 'MXN', 'Instrument', 'MXN-BASIS-Old', 'Yield Curve'],
['MZN', 'MZN', 'Instrument', 'MZN-GOV', 'Yield Curve'],
['USD', 'MZN', 'Instrument', 'USD/MZN DEPO', 'Yield Curve'],
['NAD', 'NAD', 'Instrument', 'NAD_Govi', 'Yield Curve'],
['USD', 'NAD', 'Instrument', 'NAD-Basis', 'Yield Curve'],
['NGN', 'NGN', 'Instrument', 'nigeria_govi', 'Yield Curve'],
['USD', 'NGN', 'Instrument', 'NGN-BASIS', 'Yield Curve'],
['USD', 'NZD', 'Instrument', 'NZD-USD/FX', 'Yield Curve'],
['USD', 'Sin_Fuel_Oil', 'Instrument', 'ICE_GO', 'Yield Curve'],
['USD', 'Sing180FO', 'Instrument', 'FO_Sing_180_FOB', 'Yield Curve'],
['USD', 'TRY', 'Instrument', 'USD-TRY/FX', 'Yield Curve'],
['TZS', 'TZS', 'Instrument', 'TZS-BOND-CURVE', 'Yield Curve'],
['USD', 'TZS', 'Instrument', 'TZS-FX_CURVE', 'Yield Curve'],
['UGX', 'UGX', 'Instrument', 'UGX-Govi', 'Yield Curve'],
['USD', 'UGX', 'Instrument', 'UGX-FX', 'Yield Curve'],
['ULSD_DIESEL', 'ULSD_DIESEL', 'Instrument', 'Med_ULSD_FOB', 'Yield Curve'],
['USD', 'ULSD_DIESEL', 'Instrument', 'Med_ULSD_FOB', 'Yield Curve'],
['USD', 'XAG', 'Instrument', 'XAG-DEPO', 'Yield Curve'],
['USD', 'XAU', 'Instrument', 'XAU-DEPO', 'Yield Curve'],
['USD', 'XPD', 'Instrument', 'XPD-DEPO', 'Yield Curve'],
['USD', 'XPT', 'Instrument', 'XPT-DEPO', 'Yield Curve'],
['USD', 'XRH', 'Instrument', 'USD/XRH DEPO', 'Yield Curve'],
['USD', 'ZAR', 'Instrument', 'ZAR-BASIS', 'Yield Curve'],
['USD', 'ZMK', 'Instrument', 'ZMK-FX', 'Yield Curve'],
['HUF', 'HUF', 'Instrument', 'HUF-SWAP', 'Yield Curve'],
['ILS', 'ILS', 'Instrument', 'ILS-SWAP', 'Yield Curve'],
['MXN', 'MXN', 'Instrument', 'MXN-SWAP', 'Yield Curve'],
['PLN', 'PLN', 'Instrument', 'PLN-SWAP', 'Yield Curve'],
['MUR', 'MUR', 'Instrument', 'MUR-GOVI', 'Yield Curve'],
['MXN', 'MXN', 'Instrument', 'MXN-SWAP', 'Yield Curve']]


context=acm.FContext["ACMB Global"]
count=0
for link in linkList:
    try:
        cl = acm.FContextLink()
        cl.Context = 'ACMB Global'
        cl.Instrument = acm.FInstrument[link[0]]
        if link[1] != 'None':
            cl.Currency = acm.FInstrument[link[1]]
        cl.MappingType = link[2]
        cl.Name = acm.FYieldCurve[link[3]]
        cl.Type = link[4]
        cl.Commit()
        count=count + 1
    except Exception, e:
        print >> sys.stderr, "Fail to create context link for ", link, e
        
print >> sys.stderr, count, " Context Links for FX Base Curves out of ", len(linkList), " were added successfully"
