import acm
import csv
import os
import FAFOUtils

import ColleteralReportCreator
from DelegatedReportBase import (DelegatedReportBase, AssetClass)
from ValuationReportCreator import ValuationCreatorFromStoredQuery
from TradeEventsCreator import TradeEventsCreatorFromStoredQuery
from random import randint
from datetime import datetime, date, timedelta
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
FOOTER = ['*0RCM-END00000001']
VAL_FOOTER = ['*6RCM-END00000001']

ael_variables = AelVariableHandler()

ael_variables.add('query_folder',
                  label='Query folder',
                  cls=acm.FStoredASQLQuery,
                  mandatory=False,
                  collection=sorted(acm.FStoredASQLQuery.Select("subType='FTrade'")),
                  default=acm.FStoredASQLQuery['DelegateReporting_All'],
                  tab="General")

ael_variables.add('data_submitter_value',
                  label='Data Submitter Value',
                  mandatory=True,
                  default='SLI1CVYMJ21DST0Q8K25',
                  tab="General")

ael_variables.add('report_type',
                  label='Report Type',
                  mandatory=True,
                  collection=DelegatedReportBase.REPORT_TYPES,
                  tab="General")

ael_variables.add('asset_class',
                  label='Asset Class',
                  mandatory=True,
                  collection=DelegatedReportBase.ASSET_CLASSES.keys(),
                  tab="General")

ael_variables.add('columns',
                  label='Columns',
                  mandatory=True,
                  multiple=True,
                  tab="General")

ael_variables.add('action',
                  label='Report  Action',
                  mandatory=True,
                  collection=DelegatedReportBase.ACTION,
                  tab="General")

ael_variables.add('region',
                  label='Region or Jurisdiction',
                  mandatory=False,
                  default='EU',
                  tab="General")

ael_variables.add('output_folder',
                  label='Output Folder',
                  mandatory=True,
                  default='/services/frontnt/Task',
                  tab="General")

ael_variables.add('input_folder',
                  label='Market Risk File',
                  mandatory=False,
                  default='/apps/services/front/QUERIES/GEN/TASK/temp',
                  tab="Colleteral")

ael_variables.add('collateral_position_file',
                  label='Collateral Position File',
                  mandatory=False,
                  default='CollateralBalancePositions.csv',
                  tab="Colleteral")

ael_variables.add('collateral_portfolios',
                  label='Counterparty Collateral Choice List',
                  cls=acm.FChoiceList,
                  mandatory=False,
                  collection=sorted(acm.FChoiceList.Choices()),
                  default=acm.FChoiceList['EMIR Collateral Portfolio List'],
                  tab="Colleteral")

ael_variables.add('level',
                  label='Colleteral level',
                  mandatory=False,
                  collection=ColleteralReportCreator.ColleteralReportCreator.LEVELS,
                  tab="Colleteral")


def validate(date_text):
    try:
        if datetime.strptime(date_text, '%Y-%m-%d'):
            return True
    except ValueError:
        return False


def return_latest_date_folder(path):
    return sorted([name for name in os.listdir(path) if validate(name) and os.path.isdir('{}/{}'.format(path, name))],
                  reverse=True)[0]


def create_output_location(output_file):
    try:
        if not os.path.exists(output_file):
            os.makedirs(output_file)
            return True
    except ValueError:
        return False


def create_file_name(region, asset_class):
    o_code = asset_class.uat_ocode
    environment = DelegatedReportBase.UAT
    sys_id = asset_class.sysid
    if "Production" == acm.FInstallationData.Select('').At(0).Name():
        o_code = asset_class.production_ocode
        environment = DelegatedReportBase.PROD
    file_name = "{environment}.UP.C{o_code}.S{sys_id}".format(environment=environment,
                                                              o_code=o_code,
                                                              sys_id=sys_id)

    return file_name


def get_dtk_header(asset_class):
    date = datetime.now().strftime('%d%m%Y')
    sys_id = asset_class.sysid
    o_code = asset_class.uat_ocode
    if "Production" == acm.FInstallationData.Select('').At(0).Name():
        o_code = asset_class.production_ocode

    header = "HDR.S{sys_id}.E00.C{o_code}.S0000{date}GRTUpload                N    *               ".format(
        sys_id=sys_id, o_code=o_code, date=date)
    return header


def get_app_header(asset_class):
    date = datetime.now().strftime('%Y-%m-%d')
    o_code = asset_class.uat_ocode
    asset_id = asset_class.asset_id
    if "Production" == acm.FInstallationData.Select('').At(0).Name():
        o_code = asset_class.production_ocode
    header = "*{o_code}{date}OSFTPCONNECTION@ABSA.AFRICA              -{asset_id}".format(
        o_code=o_code, date=date, asset_id=asset_id)
    trailer = " " * (78 - len(header))
    return header + trailer


def get_app_trailer(asset_class, record_count):
    o_code = asset_class.uat_ocode
    if "Production" == acm.FInstallationData.Select('').At(0).Name():
        o_code = asset_class.production_ocode

    if o_code[0] in ('2', '3', '4', '5', '6'):
        return "*{o_code}-END".format(o_code=o_code)
    else:
        digits = len(str(record_count))
        zeros = "0" * (8 - digits)
        trailer = zeros + str(record_count)
        return "*{o_code}-END{record_count_trailer}".format(o_code=o_code, record_count_trailer=trailer)


def get_dtk_trailer(asset_class, record_count):
    o_code = asset_class.uat_ocode
    sys_id = asset_class.sysid

    if "Production" == acm.FInstallationData.Select('').At(0).Name():
        o_code = asset_class.production_ocode
    trailer_header = "END.S{sys_id}.E00.C{o_code}.S0000{record_count}".format(o_code=o_code, sys_id=sys_id,
                                                                              record_count=record_count)
    trailer = " " * (80 - len(trailer_header))
    return trailer_header + trailer


def write_output_file(folder, file_name, results, header, asset_class):
    if os.path.exists(folder):
        LOGGER.info("File path exists")
        file = folder + "/" + file_name
        with open(file, 'wb') as output_file:
            writer = csv.writer(output_file, quoting=csv.QUOTE_NONE)
            writer.writerow([get_dtk_header(asset_class)])
            writer.writerow([get_app_header(asset_class)])
            writer.writerow(header)
            for item in results:
                writer.writerow(item)
            writer.writerow([get_app_trailer(asset_class, len(results))])
            writer.writerow([get_dtk_trailer(asset_class, len(results))])
        LOGGER.info("Wrote secondary output to:{}/{}".format(folder, file_name))
    else:
        LOGGER.error("File path: {} does not exist.".format(folder))


def ael_main(ael_dict):
    report_type = str(ael_dict['report_type'])
    portfolio = ael_dict['collateral_portfolios']
    region = ael_dict['region']
    asset_class = DelegatedReportBase.ASSET_CLASSES[ael_dict['asset_class']]
    action = ael_dict['action']
    columns = ael_dict['columns']
    data_submitter = ael_dict['data_submitter_value']
    dataset = ael_dict['query_folder']

    if "Collateral" == report_type:
        collateral_input_file = r'{0}/{1}/{2}'.format(ael_dict['input_folder'],
                                                      return_latest_date_folder(ael_dict['input_folder']),
                                                      ael_dict['collateral_position_file'])
        creator = ColleteralReportCreator.ColleteralCreatorFromCSV(collateral_input_file, action, asset_class, columns,
                                                                   portfolio, data_submitter)
    elif "Valuation" == report_type:
        creator = ValuationCreatorFromStoredQuery(dataset, action, asset_class,
                                                  data_submitter, columns)
    else:
        creator = TradeEventsCreatorFromStoredQuery(dataset, action, asset_class,
                                                    data_submitter, columns)
    if creator:
        creator.process(False)
        results = creator.results
        if len(results) > 0:
            write_output_file(ael_dict['output_folder'],
                              "{file}.csv".format(file=create_file_name(region, asset_class)),
                              results, columns, asset_class)
