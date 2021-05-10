"""----------------------------------------------------------------------------------------------
MODULE
    JSE_ins_version_updater

DESCRIPTION
    Date                : 2020-03-31
    Purpose             : Updates JSE instrument version in FA as an Instrument Alias.
    Department and Desk : BDA
    Requester           : BDA
    Developer           : Qaqamba Ntshobane

HISTORY
==================================================================================================
Date            Change no       Developer               Description
--------------------------------------------------------------------------------------------------
2020-03-31      PCGDEV-339      Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
-----------------------------------------------------------------------------------------------"""

import acm
import csv

from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
INS_ALIAS_TYPE = acm.FInstrAliasType['JSE_Instrument_Version']

DIRECTORY_SELECTOR = acm.FFileSelection()
DIRECTORY_SELECTOR.PickExistingFile(True)
DIRECTORY_SELECTOR.SelectedFile(r'Y:\Jhb\FALanding\Prod\BDA\BDAL92_Instruments.csv')

ael_variables = AelVariableHandler()
ael_variables.add(
    'file_directory',
    label='File Location',
    default=DIRECTORY_SELECTOR,
    cls='string'
    )


def process_instruments(file):

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            instrument = acm.FInstrument.Select("isin='%s'" % row[0])

            if instrument and instrument[0].Name().split("/")[1] == row[1].replace(" ", ""):

                jse_version = str(instrument[0].Oid())+"_"+row[2]
                ins_aliases = [alias.Alias() for alias in instrument[0].Aliases()]
                alias_object = None

                if ins_aliases:
                    if jse_version in ins_aliases:
                        continue
                    
                    ins_aliases_ = [ia[:-2] for ia in ins_aliases]

                    if jse_version[:-2] in ins_aliases_:
                        alias_object = ins_aliases[ins_aliases_.index(jse_version[:-2])]
                        alias_object = acm.FInstrumentAlias[alias_object]

                        if not alias_object:
                            continue

                        alias_object = alias_object.StorageImage()
                else:
                    alias_object = acm.FInstrumentAlias()
                    alias_object.RegisterInStorage()

                alias_object.Alias(jse_version)
                alias_object.Type(INS_ALIAS_TYPE)
                alias_object.Instrument(acm.FInstrument[instrument[0].Name()])

                LOGGER.info("Updating %s with version number %s" %(instrument[0].Name(), alias_object.Alias()))

                try:
                    alias_object.Commit()
                except Exception as e:
                    LOGGER.exception("Failed to update: %s", e)
        LOGGER.info('Done')


def ael_main(dictionary):

    file_name = dictionary['file_directory']
    process_instruments(file_name)

