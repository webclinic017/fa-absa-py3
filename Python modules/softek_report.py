"""A post processor for CLM Reports for Softek.

Intended to decompose positions by underlying weights.
TODO: Remove the module once done with grouper.
"""

import csv
import os
import shutil
from collections import defaultdict

import acm

from at_logging import getLogger
from FReportAPIBaseUtils import getNewFilePath

LOGGER = getLogger(__name__)

# Column indexes
POS_END = 1
INSTRUMENT = 0
INS_TYPE = 5
UNDERLYING_TYPE = 6
UNDERLYING = 7
PORTFOLIO = 10
PRICE = 12
CURRENCY = 13
ISIN = 14
UNDERLYING_ISIN = 15
DUAL_LISTED = 16
ISSUER = 17
UNDERLYING_ISSUER = 18


def get_price(instrument):
    prices = instrument.Prices().Filter(
        lambda price: price.Market().Name() == 'SPOT')
    if prices:
        return prices[0].Last()


def decompose_position(row):
    ins_name = row[INSTRUMENT]
    LOGGER.info(
        'Decomposing instrument {},'
        'portfolio {}'.format(ins_name, row[PORTFOLIO]))
    instrument = acm.FInstrument[ins_name]
    if not instrument:
        LOGGER.error('Instrument {} not found'.format(ins_name))
        yield row
    underlying = instrument.Underlying()
    position = float(row[POS_END])

    new_row = [''] * len(row)
    comment = (
        'Future decomposition: {} Underlying: {} '
        'Qty: {}'.format(ins_name, row[UNDERLYING], position))
    new_row.append(comment)
    LOGGER.info(comment)
    instrument_maps = underlying.InstrumentMaps()
    for mapped_ins in instrument_maps:
        weighted_position = ((mapped_ins.Weight()/underlying.Factor()) *
                             position * instrument.ContractSize())
        LOGGER.info('Calculated weight for {}:'
                    ' {}'.format(mapped_ins.Instrument().Name(), weighted_position))
        new_row[POS_END] = weighted_position
        new_row[INSTRUMENT] = mapped_ins.Instrument().Name()
        new_row[INS_TYPE] = mapped_ins.Instrument().InsType()
        new_row[UNDERLYING_TYPE] = mapped_ins.Instrument().UnderlyingType()
        new_row[UNDERLYING] = mapped_ins.Instrument().Underlying()
        new_row[PORTFOLIO] = row[PORTFOLIO]
        new_row[DUAL_LISTED] = row[DUAL_LISTED]
        new_row[PRICE] = get_price(mapped_ins.Instrument())
        new_row[CURRENCY] = mapped_ins.Instrument().Currency().Name()
        yield new_row

    if not instrument_maps:
        yield row


def decompose_futures(rows):
    decomposed_by_prf = defaultdict(dict)
    for row in rows:
        for decomposed_row in decompose_position(row):
            portfolio = decomposed_row[PORTFOLIO]
            instrument = decomposed_row[INSTRUMENT]

            new = decomposed_row[:]
            prev = decomposed_by_prf[portfolio].get(instrument)
            if prev:
                new[POS_END] += prev[POS_END]
            decomposed_by_prf[portfolio][instrument] = new

    for instruments in decomposed_by_prf.values():
        for row in instruments.values():
            yield row


def process_rows(report_copy):
    ignore_first_n_rows = 6
    to_decompose = []

    with open(report_copy, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        for _ in range(ignore_first_n_rows):
            yield next(reader)
        for row in reader:
            ins_type = row[INS_TYPE]
            if not ins_type:
                continue
            ins_underlying_type = row[UNDERLYING_TYPE]
            if ins_type == 'Future' and ins_underlying_type == 'EquityIndex':
                to_decompose.append(row)
            else:
                yield row

    for row in decompose_futures(to_decompose):
        yield row


def write_to_csv(file_name, data):
    with open(file_name, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for entry in data:
            writer.writerow(entry)


def post_decompose_underlying_weights(report_object, param, xml):
    LOGGER.info('Decomposing Future/Forward positions')

    report_path = getNewFilePath(
        report_object,
        str(report_object.params.filePath),
        report_object.params.secondaryFileExtension)

    file_path, extension = os.path.splitext(report_path)
    report_copy = '{}_copy{}'.format(file_path, extension)
    shutil.move(report_path, report_copy)
    write_to_csv(report_path, process_rows(report_copy))
    os.remove(report_copy)
    LOGGER.info('Decomposition completed')
