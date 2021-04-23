#once off script to define the disc type for OIS curve related benchmarks

import acm
ael_variables = []

def ael_main(dict):

    bms = [
    ('EUR-USD/CCS/LI-EU/10Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/12Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/15Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/20Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/25Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/3Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/4Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/5Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/6Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/7Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/8Y-CSA', 'CSA-USD'),
    ('EUR-USD/CCS/LI-EU/9Y-CSA', 'CSA-USD'),
    ('EUR/IRS/GEN/10Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/12Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/15Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/1Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/20Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/25Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/2Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/30Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/3Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/4Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/5Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/6Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/7Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/8Y-CSA', 'CSA-EUR'),
    ('EUR/IRS/GEN/9Y-CSA', 'CSA-EUR'),
    ('GBP-USD/CCS/LI-LI/10Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/12Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/15Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/18M-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/20Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/25Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/30Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/3Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/4Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/5Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/6Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/7Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/8Y-CSA', 'CSA-GBP'),
    ('GBP-USD/CCS/LI-LI/9Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/10Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/12Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/15Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/18M-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/1Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/20Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/25Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/2Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/30Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/3Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/4Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/5Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/6Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/7Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/8Y-CSA', 'CSA-GBP'),
    ('GBP/IRS/GEN/9Y-CSA', 'CSA-GBP'),
    ('JPY-FRA-LI-12M-15M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-15M-18M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-18M-21M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-21M-24M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-3M-6M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-6M-9M-CSA', 'CSA-JPY'),
    ('JPY-FRA-LI-9M-12M-CSA', 'CSA-JPY'),
    ('ZAR-USD/CCS/LI-JI/0Y-10Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-12Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-15Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-1Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-2Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-30Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-3Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-4Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-5Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-6Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-7Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-8Y-CSA', 'CSA-USD'),
    ('ZAR-USD/CCS/LI-JI/0Y-9Y-CSA', 'CSA-USD'),
    ('ZAR/FRA/JI/12X15-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/15X18-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/18X21-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/21X24-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/3X6-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/6X9-CSA', 'CSA-ZAR'),
    ('ZAR/FRA/JI/9X12-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/10Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/12Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/15Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/20Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/25Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/30Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/3Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/4Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/5Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/6Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/7Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/8Y-CSA', 'CSA-ZAR'),
    ('ZAR/IRS/GEN/9Y-CSA', 'CSA-ZAR'),
    ('EUR/BasisSwap/EONIA-3M/10Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/12Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/15Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/20Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/25Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/2Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/30Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/3Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/4Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/5Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/6Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/7Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/8Y', 'CSA-EUR'),
    ('EUR/BasisSwap/EONIA-3M/9Y', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/12M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/15M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/18M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/1M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/21M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/2M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/3M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/6M', 'CSA-EUR'),
    ('EUR/IRS/EONIA/GEN/9M', 'CSA-EUR'),
    ('CurrencyBasisSwapDefault', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/10Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/12Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/15Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/20Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/25Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/3Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/4Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/5Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/6Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/7Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/8Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3M/6M/9Y', 'CSA-EUR'),
    ('EUR/BasisSwap/3m/6M/30Y', 'CSA-EUR'),
    ('GBP/BasisSwap/3M/6M/10Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/12Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/15Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/20Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/25Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/30Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/3Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/4Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/5Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/6Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/7Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/8Y', 'CSA-GBP'),
    ('GBP/BasisSwap/3M/6M/9Y', 'CSA-GBP'),
    ('JPY/BasisSwap/3M/6M/10Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/12Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/15Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/20Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/25Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/30Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/3Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/4Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/5Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/6Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/7Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/8Y', 'CSA-JPY'),
    ('JPY/BasisSwap/3M/6M/9Y', 'CSA-JPY'),
    ('ZAR/BasisSwap/OIS-JI/10Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/12M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/12Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/15M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/15Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/18M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/20Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/21M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/25Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/2Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/30Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/3M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/3Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/4Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/5Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/6M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/6Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/7Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/8Y', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/9M', 'CSA-ZAR'),
    ('ZAR/BasisSwap/OIS-JI/9Y', 'CSA-ZAR'),
    ('GBP/BasisSwap/SONIA-3M/10Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/12Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/15Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/20Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/25Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/2Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/30Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/3Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/4Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/5Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/6Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/7Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/8Y', 'CSA-GBP'),
    ('GBP/BasisSwap/SONIA-3M/9Y', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/12M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/15M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/18M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/1M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/21M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/2M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/3M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/6M', 'CSA-GBP'),
    ('GBP/IRS/SONIA/GEN/9M', 'CSA-GBP'),
    ('EUR/3MFUTURE/JUN15', 'CSA-EUR'),
    ('EUR/3MFUTURE/MAR15', 'CSA-EUR'),
    ('EUR/3MFUTURE/DEC14', 'CSA-EUR'),
    ('EUR/3MFUTURE/SEP14', 'CSA-EUR'),
    ('EUR/3MFUTURE/JUN14', 'CSA-EUR'),
    ('EUR/3MFUTURE/MAR14', 'CSA-EUR'),
    ('EUR/3MFUTURE/DEC13', 'CSA-EUR'),
    ('EUR/3MFUTURE/SEP13', 'CSA-EUR'),
    ('GBP/3MFUTURE/JUN15', 'CSA-GBP'),
    ('GBP/3MFUTURE/MAR15', 'CSA-GBP'),
    ('GBP/3MFUTURE/SEP14', 'CSA-GBP'),
    ('GBP/3MFUTURE/JUN14', 'CSA-GBP'),
    ('GBP/3MFUTURE/MAR14', 'CSA-GBP'),
    ('GBP/3MFUTURE/DEC13', 'CSA-GBP'),
    ('GBP/3MFUTURE/SEP13', 'CSA-GBP')]



    for bm in bms:

        if acm.FInstrument[bm[0]]:
            ins = acm.FInstrument[bm[0]]
            ins.DiscountingType(bm[1]) 
            try:
                ins.Commit()
            except:
                acm.Log('could not commit the disc type for the instrument %s' %ins.Name())
                
        else:
            print bm[0], 'no such instrument'



