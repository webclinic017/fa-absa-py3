""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAUtility.py"
# Contains all references into BDP and AdaptivXVA modules.
import collections
import os
import re
import sys

import acm

import FBDPGui
import FBDPCommon
import FMarkToMarket
import FMtMPerform

import AAIntegrationUtility
import AAXVAProcess
import importlib

try:
    import AAParamsAndSettingsHelper
    import AADataCreator
except:
    raise Exception('Adaptiv XVA module not loaded')

def _getCalculationTypes():

    types = ['CVA', 'PFE']
    try:
        import AAFVAIntegration

        types.append('FVA')
    except:
        pass

    return types

# Public
CALCULATIONS_TYPES = tuple(sorted(_getCalculationTypes()))
DATES = FMarkToMarket.cvDate
INSTRUMENTS = FBDPGui.insertInstruments(instype=('Credit Balance',))

# Private
_Parameters = collections.namedtuple(
    'Parameters', (
        'market_data_path risk_factor_archive_path type date seed '
        'grid sampling antithetic num_scenarios cparty'
    )
)
_EXPLICIT_MD_LEFT_EXPR = '<ExplicitMarketData><![CDATA['
_EXPLICIT_MD_RIGHT_EXPR = ']]></ExplicitMarketData>'
_MD_VERSION_EXPR = 'AnalyticsVersion='
_MD_HEADER_REGEX = r'<(.*)>'

def reloadModules(ignore_gui=False):
    # partially order dependent
    importlib.reload(FBDPCommon)
    if not ignore_gui:
        importlib.reload(FBDPGui)

    importlib.reload(FMarkToMarket)
    importlib.reload(FMtMPerform)

    if ignore_gui:
        importlib.reload(AAIntegrationUtility)
    else:
        import AAIntegrationGuiCommon
        importlib.reload(AAIntegrationGuiCommon) # also reloads AAIntegrationUtility

    importlib.reload(AAXVAProcess)
    import AAXVAPerform
    importlib.reload(AAXVAPerform)
    if not ignore_gui:
        import AAXVAGuiCommon
        importlib.reload(AAXVAGuiCommon)

    # safe because the exporter is a class member of the export class
    # as long as exporters are created from the the export class after
    # this call
    import AAXVAAAJCreator
    importlib.reload(AAXVAAAJCreator)
    import AAXVARiskFactorArchiver
    importlib.reload(AAXVARiskFactorArchiver)
    return

def executeWithRedirectedLogger(func, logger):
    get_aa_logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger
    reload_exceptions = ['AAParamsAndSettingsHelper']
    try:
        AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger = lambda: logger
        _reloadAdaptivXVAModule(exceptions=reload_exceptions)
        return func()
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error('Failed: ' + str(e))
    finally:
        AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger = get_aa_logger
        _reloadAdaptivXVAModule(exceptions=reload_exceptions)

    return False

def getAdaptivXVAParamsHelper():
    return AAParamsAndSettingsHelper

def getAELDate(date):
    return FBDPCommon.toDateAEL(date)

def getACMDate(date):
    return FBDPCommon.toDate(date)

def validateCVAModule():
    FMtMPerform._validateCVAModule(exportCredBalAAJ=True)
    return

def validateAAJDirectory(path):
    FMtMPerform._validateExportCredBalAAJPath(
        exportCredBalAAJ=True, exportPath=path
    )
    return

def getMarketDataFilePath(path, calc_type, date):
    if not path:
        path = AADataCreator.getMarketDataFilePath(
            calculationType=calc_type, valuationDate=date,
            ignoreUseRealTimeMarketData=True
        )

    assert os.path.isfile(path), calc_type + ' base market data file not found'
    return AAIntegrationUtility.forwardSlashedPath(path=path)

def getCalculationQuery(instrs):
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    op = query.AddOpNode('OR')
    for ins in instrs:
        assert ins.IsKindOf(acm.FCreditBalance), \
            'Expected credit balance instrument but got ' + ins.InsType()
        op.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())

    return query

def getMarketDataInfo(distributed, calc_types, calc_query, output_dir):
    calc_infos = _getCalculationInfo(
        distributed=distributed, calc_types=calc_types,
        query=calc_query, output_dir=output_dir
    )
    return calc_infos

def createMarketData(
    distributed, calc_types, calc_query, market_data_paths,
    calc_infos, logger, indentation, indentation_level
):
    column_names, raw_md = _getCalcSpaceResults(
        distributed=distributed, attr_func=_getMarketDataExtensionAttr,
        calc_types=calc_types, query=calc_query
    )
    md_file_contents = _readInMarketDataFiles(paths=market_data_paths)
    prefix_indentation = indentation * indentation_level
    write_msg = 'Written %s market data file - %s.'
    raw_md = dict((column_names[c_name], md) for c_name, md in raw_md.items())
    mds = []
    for calc_type in sorted(raw_md):
        pre_filtered_md = raw_md[calc_type]
        calc_info = calc_infos[calc_type]
        if not calc_info:
            msg = 'Failed to extract %s calculation details.' % calc_type
            logger.error(prefix_indentation + msg)
            continue

        info = calc_info.values()[0]
        base_md = md_file_contents[calc_type]
        content = _getMarketDataContent(
            base_market_data=base_md, calc_type_market_data=pre_filtered_md
        )
        with open(info.market_data_path, 'w') as fout:
            fout.write('\n'.join(content))

        mds.append(info.market_data_path)
        msg = write_msg % (info.type, info.market_data_path)
        logger.info(prefix_indentation + msg)

    return mds

def createRiskFactorArchives(
    info, exe_dir, logger, indentation, indentation_level
):
    exe = os.path.join(exe_dir, 'FactorArchiveGenCmd.exe')
    gen_msg = 'Generating %s risk factor archive file.'
    write_msg = 'Written %s risk factor archive file - %s.'
    prefix_indentation = indentation * indentation_level
    new_prefix_indentation = prefix_indentation + indentation
    to_process = {}
    for calc_type in sorted(info):
        cparty_info = info[calc_type]
        if not cparty_info:
            msg = (
                'No calculation details from which to '
                'generate %s risk factor archives.'
            ) % calc_type
            logger.error(prefix_indentation + msg)
            continue

        for i in cparty_info.values():
            to_process.setdefault((i.type, i.risk_factor_archive_path), i)

    rfas = []
    for key in sorted(to_process.keys()):
        i = to_process[key]
        logger.debug(prefix_indentation + (gen_msg % i.type))
        rfa = _createRiskFactorArchive(
            info=i, exe=exe, logger=logger,
            prefix_indentation=new_prefix_indentation
        )
        if rfa and (rfa == i.risk_factor_archive_path):
            logger.info(prefix_indentation + (write_msg % (i.type, rfa)))
            rfas.append(rfa)
        elif rfa:
            msg = 'Invalid risk factor archive file, expected %s got %s.' % (
                i.risk_factor_archive_path, rfa
            )
            logger.error(new_prefix_indentation + msg)
        else:
            msg = 'Failed to create %s risk factor archive file.' % i.type
            logger.error(new_prefix_indentation + msg)

    return rfas

# To be fixed in subsequent SPRs
"""
def createAAJs(instrs, market_data_paths, distributed, column_names):
    calc = _getCalcSpaceManager(distributed=distributed)
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    op = query.AddOpNode('OR')
    for ins in instrs:
        assert ins.IsKindOf(acm.FCreditBalance), \
            'Expected credit balance instrument but got ' + ins.InsType()
        op.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())

    calc.init(asql_query=query, column_names=column_names.values())
    raw_aajs = calc.run()
    aajs = {}
    for column_name, pre_filtered_aajs in raw_aajs.items():
        calc_type = column_names[column_name]
        aajs[(column_name, calc_type)] = self._getAAJs(
            calc_type=calc_type, aajs=pre_filtered_aajs,
            market_data_paths=market_data_paths
        )

    aajs.clear()
    return aajs

def getAAJWriteDetails(aajs, iso_date, suffix, prefixes, getOutputFilepathCb):
    if not aajs:
        return None

    details = []
    file_name_template = _makeAAJFilename(iso_date=iso_date, suffix=suffix)
    for key in sorted(aajs):
        aaj = aajs[key]
        if not aaj:
            self._logger.debug(self._base_indentation + '    Nothing to write.')
            continue

        column_name, calc_type = key
        filepath = getOutputFilepathCb(
            filename=file_name_template, prefix=prefixes[calc_type]
        )
        details.append((column_name, filepath, aaj))

    return tuple(details)
"""

# Private
def _getCalcExtensionAttr(calc_type):
    return calc_type.lower() + 'CalculationXML'

def _getDealsExtensionAttr(calc_type):
    return calc_type.lower() + 'DealsXML'

def _getMarketDataExtensionAttr(calc_type):
    return calc_type.lower() + 'DealsMarketDataXML'

def _getCalcSpaceManager(distributed):
    space = FBDPCommon.CalculationSpaceManager(
        use_distributed_calc=distributed
    )
    return space

def _getCalcSpaceResults(distributed, attr_func, calc_types, query):
    # Todo: May be possible to reuse calc space manager (investigate!)
    val = AAParamsAndSettingsHelper.FParameters['RealTimeMarketData']
    column_names = result = None
    try:
        AAParamsAndSettingsHelper.FParameters['RealTimeMarketData'] = True
        calc = _getCalcSpaceManager(distributed=distributed)
        column_names = dict((attr_func(calc_type=ct), ct) for ct in calc_types)
        calc.init(asql_query=query, column_names=column_names.keys())
        result = calc.run()
    finally:
        AAParamsAndSettingsHelper.FParameters['RealTimeMarketData'] = val

    return column_names, result

def _readInMarketDataFiles(paths):
    contents = {}
    for calc_type, path in paths.items():
        with open(path, 'r') as fin:
            contents[calc_type] = tuple(fin.readlines())

    return contents

def _getMarketDataContent(base_market_data, calc_type_market_data):
    md = collections.OrderedDict()
    _updateMarketDataDict(
        market_data_dict=md, market_data=base_market_data, from_instrs=False
    )
    for ins_md in calc_type_market_data:
        if ins_md.value:
            ins_md = _getExplicitMarketData(market_data=ins_md.value)
            _updateMarketDataDict(
                market_data_dict=md, market_data=ins_md, from_instrs=True
            )

    md_file_contents = []
    for section, data in md.items():
        if section == _MD_VERSION_EXPR:
            md_file_contents.append(section + data)
        else:
            data = sorted('%s%s' % (k, v) for k, v in data.items())
            md_file_contents.append('<' + section + '>')
            md_file_contents.extend(data)

        md_file_contents.append('')

    return tuple(md_file_contents)

def _getCalculationInfo(distributed, calc_types, query, output_dir):
    column_names, raw_info = _getCalcSpaceResults(
        distributed=distributed, attr_func=_getCalcExtensionAttr,
        calc_types=calc_types, query=query
    )
    infos = {} # keys on type then counterparty
    for column_name, pre_filtered_info in raw_info.items():
        calc_type = column_names[column_name]
        path_template = AAIntegrationUtility.forwardSlashedPath(
            path=os.path.join(output_dir, calc_type)
        )
        md_path = path_template + '_MarketData.dat'
        rfa_path = path_template + '_RiskFactorArchive.dat'
        info = infos.setdefault(calc_type, {})
        for ins_info in pre_filtered_info:
            data = ins_info.value
            if not data:
                continue

            extract = lambda attr: _extractAttribute(data=data, attr=attr)
            cparty = extract(attr='Counterparty')
            if cparty not in info:
                content = info[cparty] = {}
                content['market_data_path'] = md_path
                content['risk_factor_archive_path'] = rfa_path
                content['type'] = calc_type
                content['date'] = extract(attr='Base_Date')
                content['seed'] = extract(attr='Random_Seed')
                content['grid'] = extract(attr='Scenario_Time_Grid')
                content['sampling'] = extract(attr='Sampling')
                content['antithetic'] = str(extract(attr='Antithetic') == 'Yes')
                content['num_scenarios'] = extract(attr='Scenarios')
                content['cparty'] = cparty
                info[cparty] = _Parameters(**content)

    return infos

def _createRiskFactorArchive(info, exe, logger, prefix_indentation):
    def success(output_files, stdout):
        success = (len(output_files) == 1) and \
            ('Generate completed successfully.' in stdout)
        return success

    comment = 'Created by Front Arena for %s calculation on %s' % (
        info.type, info.date
    )
    grid, end = info.grid.rsplit('(', 1)
    end = end.strip(')')
    cwd = os.path.dirname(info.risk_factor_archive_path)
    kwargs = {
        'Action': 'Generate',
        'Storage': 'File',
        'Comments': comment,
        'ArchiveFile': info.risk_factor_archive_path,
        'MarketDataFile': info.market_data_path,
        'Seed': info.seed,
        'NumScenarios': info.num_scenarios,
        'StartDate': info.date,
        'End': end,
        'TimeGrid': grid,
        'Sampling': info.sampling,
        'Antithetic': info.antithetic,
        'ModelCorrelations': False,
        'NumThreads': 0
    }
    args = ['--%s=%s' % (k, v) for k, v in kwargs.items()]
    stdout = lambda msg: logger.debug(prefix_indentation + msg)
    stderr = lambda msg: logger.error(prefix_indentation + msg)
    proc = AAXVAProcess.SynchronousProcess(
        name='Risk factor archive generator',
        cwd=cwd, exe=exe, args=args, stdout=stdout, stderr=stderr,
        output_files=[info.risk_factor_archive_path],
        success_check_func=success
    )
    return info.risk_factor_archive_path if proc.run() else None

def _updateMarketDataDict(market_data_dict, market_data, from_instrs):
    # Contains aggregated and de-duplicated market data, containing
    # market data file as base data overridden with the first
    # read data from instruments.
    contents = None
    for line in market_data:
        line = line.strip()
        if (not line):
            continue

        matches = re.findall(_MD_HEADER_REGEX, line)
        if matches or line.startswith(_MD_VERSION_EXPR):
            assert (not matches) or len(matches) == 1, \
                'Unable to process market data line'
            if matches:
                contents = market_data_dict.setdefault(matches[0], {})
            else:
                contents = None
                market_data_dict[_MD_VERSION_EXPR] = line.split('=', 1)[1]

            continue

        if contents is not None:
            key = line
            value = ''
            split = line.split('=', 1)
            if len(split) == 2:
                key, value = split
                if ',' in key:
                    key, value = line.split(',', 1)
                    key = key + ','
                else:
                    key = key + '='

            if from_instrs:
                contents.setdefault(key, value)
            else:
                contents[key] = value

    return

def _getExplicitMarketData(market_data):
    data = market_data.split(_EXPLICIT_MD_LEFT_EXPR, 1)[1]
    data = data.rsplit(_EXPLICIT_MD_RIGHT_EXPR, 1)[0]
    data = re.sub(r'[\n]+', r'\n', data)
    return tuple(d + '\n' for d in data.split('\n'))

def _extractAttribute(data, attr):
    return data.rsplit(',' + attr + '=', 1)[1].split(',', 1)[0].strip(']')

"""
def _makeAAJFilename(iso_date, suffix):
    name = FMtMPerform._makeAAJFilename(
        mtmIsoDate=iso_date, insName=suffix
    )
    return name

def _getAAJs(calc_type, aajs, market_data_files):
    market_data_file = _getMarketDataFilePath(prefix=calc_type)
    header = footer = market_data_header = None
    combined_dd = []
    combined_md = {}
    for i, aaj in enumerate(aajs):
        ins = aaj.object_name
        if i == 0:
            header = self._extractHeader(text=aaj.value, calc_type=calc_type)
            footer = self._extractFooter(text=aaj.value)
            market_data_header = self._extractMarketDataHeader(
                text=aaj.value, calc_type=calc_type
            )

        self._combineDealsData(source=aaj.value, combined_data=combined_dd)
        self._combinemartketData(
            source=aaj.value, combined_data=combined_md
        )

    combined_dd = '<Deals>' + ''.join(combined_dd) + '</Deals>'
    combined_md = '\n' + '\n'.join(sorted(combined_md.values())) + '\n'
    combined_aaj = header + combined_dd + market_data_header + \
            combined_md + footer
    return combined_aaj

    def _extractHeader(self, text, calc_type):
        text = self._extract(
            text=text, left='<Calc>', right='</ResultsViewer>', inclusive=True
        )
        scenario_spec = self._getScenarioSpec(calc_type=calc_type)
        text = text.replace(
            'Deterministic_Scenarios=Off',
            'Deterministic_Scenarios=%s' % scenario_spec[0],
        ).replace(
            'Scenario_Path=,',
            'Scenario_Path=%s,' % scenario_spec[1],
        )
        return text

    def _extractFooter(self, text):
        text = self._extract(
            text=text, left=']]></ExplicitMarketData>', right='</Calc>', inclusive=True
        )
        return text

    def _extractMarketDataHeader(self, text, calc_type):
        market_data_file = self._getMarketDataFilePath(prefix=calc_type)
        left = '<MergeMarketData>'
        right = '<Price Factors>'
        text = self._extract(text=text, left=left, right=right, inclusive=True)
        text = re.sub(
            '<MarketDataFile>(.*)</MarketDataFile>',
            '<MarketDataFile>' + market_data_file + '</MarketDataFile>',
            text
        )
        return text

    def _extract(self, text, left, right, inclusive):
        sub_text = text.split(left, 1)[1].rsplit(right, 1)[0]
        if inclusive:
            sub_text = left + sub_text + right

        return sub_text.strip()

    def _nonGreedyFindAll(self, data, left, right, inclusive):
        objs = []
        obj = None
        d = data
        while d:
            try:
                obj, d = d.split(left, 1)[1].split(right, 1)
            except:
                break

            if inclusive:
                objs.append(left + obj + right)
            else:
                objs.append(obj)

        return tuple(objs)

    def _combineDealsData(self, source, combined_data):
        data = self._extract(
            text=source, left='</ResultsViewer><Deals>',
            right='</Deals><MergeMarketData>', inclusive=False
        )
        netting_sets = self._nonGreedyFindAll(
            data=data, left='<Deal>Object=NettingCollateralSet,',
            right='</Deal></Deals></Deal>', inclusive=True
        )
        combined_data.extend(netting_sets)
        return

    def _combinemartketData(self, source, combined_data):
        data = self._extract(
            text=source, left='<Price Factors>',
            right=']]></ExplicitMarketData>', inclusive=False
        )
        for pf in data.split('\n'):
            pf = pf.strip()
            if pf:
                pf_id = pf.split(',', 1)[0]
                combined_data[pf_id] = pf

        return

    def _getScenarioSpec(self, calc_type):
        get_name = lambda suffix: '%s_%s' % (calc_type, suffix)
        enabled = lambda suffix: \
            bool(int(self._ael_params[get_name(suffix=suffix)]))
        if enabled(suffix='DeterministicScenarios'):
            if enabled(suffix='ScenariosFromFile'):
                archived_scenario_file = self._getPathParam(
                    key=get_name(suffix='ScenarioFile'), check_path=True
                )
                return ('FromFile', archived_scenario_file)
            else:
                output_scenario_file = self._getOutputFilepath(
                    filename='scenarios_%s.dat' % self.OUTPUT_SUFFIX,
                    prefix=calc_type
                )
                return ('Generate', output_scenario_file)


        return ('Off', '')
"""

def _reloadAdaptivXVAModule(exceptions=None):
    target_mods = ('CVA', 'Adaptiv XVA', 'FVA', 'Adaptiv 16.2 FVA')
    exceptions = exceptions or []
    _reloadPythonModules(modules=target_mods, exceptions=exceptions)
    return

def _reloadPythonModules(modules, exceptions):
    modules = list(modules)
    exceptions = list(exceptions)
    ext_mods = []
    for c in acm.FExtensionContext.Select(''):
        ext_mods.extend(m for m in c.Modules() if str(m.Name()) in modules)

    for ext_mod in ext_mods:
        for p_mod in ext_mod.GetAllExtensions(type=acm.FPythonCode):
            name = str(p_mod.Name()).strip()
            if name not in exceptions:
                importlib.reload(__import__(name))
                exceptions.append(name)

    return
