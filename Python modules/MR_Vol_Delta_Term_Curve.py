"""
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
"""
import math
import os

import acm
import MR_MainFunctions

from at_logging import getLogger
from at_time import acm_date, ael_date, date_from_string


LOGGER = getLogger(__name__)
InsL = []
EXTENSION_ATTRIBUTE = 'volatilityStructureInformation'


def is_nan(value):
    try:
        return math.isnan(float(value))
    except ValueError:
        return False


def OpenFile(temp, FileDir, Filename, *rest):
    filename = os.path.join(FileDir, Filename)
    outfile = open(filename, 'w')
    outfile.close()

    del InsL[:]

    return filename


def Write(v, FileDir, Filename, *rest):
    filename = os.path.join(FileDir, Filename)
    if v.seqnbr not in InsL:
        InsL.append(v.seqnbr)
        outfile = open(filename, 'a')

        # Base record
        BAS = 'BAS'
        Exchange_RateSPEC = 'Volatility - Delta/TermSPEC'
        OBJECT = 'Volatility - Delta/TermSPEC'
        TYPE = 'Volatility - Delta/Term'
        IDENTIFIER = v.vol_name

        NAME = v.vol_name

        ActiveFLAG = 'TRUE'
        CurveUnitCAL = ''
        CurveUnitDAYC = MR_MainFunctions.DayCountFix('Act/365')
        CurveUnitPERD = 'annual'
        CurveUnitUNIT = '%'

        DatumDATE = MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB = '0'

        RelativeCurveFLAG = 'TRUE'
        StateProcFUNC = ''
        TimeEvolutionFUNC = '@Constant'
        FunctionIdFLAG = 'TRUE'

        GenIndxSfExt0FLAG = 'FALSE'
        GenIndxSfExt1FLAG = 'FALSE'
        GenIndxSuf0SIN = '@Linear'
        GenIndxSuf1SIN = '@Linear'

        outfile.write(
            '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME,
                ActiveFLAG, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD,
                CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG,
                StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenIndxSfExt0FLAG,
                GenIndxSfExt1FLAG, GenIndxSuf0SIN, GenIndxSuf1SIN))

        # Roll Over Generic Zero Surface
        BASFLAG = 'rm_ro'
        Volatility = 'Volatility - Delta/TermSPEC : Generic Volatility Delta Term Surface'
        ATTRIBUTE = 'Generic Volatility Delta Term Surface'
        OBJECT = 'Volatility - Delta/TermSPEC'

        context = acm.GetDefaultContext()
        vol_structure = acm.FVolatilityStructure[v.seqnbr]
        vol_info = acm.GetCalculatedValueFromString(
            vol_structure, context, EXTENSION_ATTRIBUTE, None).Value()
        vol_structure_type = vol_structure.StructureType()

        for StrikeCount in range(0, 11):
            for VolPeriod in ('1d', '1w', '1m', '2m', '3m', '6m', '9m',
                              '1y', '2y', '3y', '4y', '5y'):
                period = acm_date(date_from_string(VolPeriod))

                GnVolMnyTrmSf0AXS = StrikeCount / 10.0
                GnVolMnyTrmSf1AXS = MR_MainFunctions.CurveDays(VolPeriod)

                # The interface of the `Value` method of the volatility structure
                # information object depends on the type of the volatility surface.

                # For FMalzParametricVolatilityInformation the interface is:
                # Value(expiryDate, delta, foreignRate, domesticRate)
                if vol_structure_type == 'Malz':
                    GnVolMnyTrmSfNODE = vol_info.Value(period, GnVolMnyTrmSf0AXS, None, None)

                # For FSinglePointVolatilityInformation (which applies to benchmark
                # volatility structures) the interface is:
                # Value(expiryDate, strike)
                elif vol_structure_type.startswith('Benchmark'):
                    GnVolMnyTrmSfNODE = vol_info.Value(period, GnVolMnyTrmSf0AXS)

                # Otherwise try getting volatility the old way using ael.
                # (ael does not work for certain volatility structure types
                # as of upgrade to Prime 2018).
                else:
                    period = ael_date(date_from_string(VolPeriod))
                    LOGGER.info('Using ael to get volatility for `%s` structure type',
                                vol_structure_type)
                    GnVolMnyTrmSfNODE = v.vol_get(GnVolMnyTrmSf0AXS, period, period, 1)
                    if is_nan(GnVolMnyTrmSfNODE):
                        LOGGER.error(
                            'Could not retrieve volatility for `%s` structure type. '
                            'ael was used, please use acm', vol_structure_type)

                outfile.write('%s,%s,%s,%s,%s,%s,%s\n' % (
                    BASFLAG, Volatility, ATTRIBUTE, OBJECT, GnVolMnyTrmSf0AXS,
                    GnVolMnyTrmSf1AXS, GnVolMnyTrmSfNODE))

        outfile.close()

    return str(v.seqnbr)
