'''--------------------------------------------------------------------------------------
MODULE
    sbl_iress_cpty_report

DESCRIPTION
    Date                : 2020-04-20
    Purpose             : Script generates IRESS Counterparty recon downstream report
    Department and Desk : SBL and Collateral
    Requester           : Gasant Thulsie, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-61

HISTORY
=========================================================================================
Date            JIRA no        Developer               Description
-----------------------------------------------------------------------------------------
2020-04-20      PCGDEV-61      Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import os
import acm
import csv

import datetime
from at_logging import getLogger
import FUploaderFunctions as gen_uploader
import sbl_reporting_utils as reporting_utils
            
LOGGER = getLogger(__name__)
FILE_HEADERS = ["CODE", "STD_TAXABLE", "UDF22"]
    

def write_file_data(directory, run_date):
    try:
        row_data = {}
        LOGGER.info("Processing security loan counterparties")
        sl_counterparties = [party for party in acm.FParty.Select("")
                            if party.add_info("SL_G1PartyCode") != "" and 
                            (party.Name().startswith("SLB") or party.Name().startswith("SLL"))]
        with open(directory, "wb") as csv_file:
            writer = csv.DictWriter(csv_file, FILE_HEADERS)
            writer.writeheader()
            for party in sl_counterparties:
                LOGGER.info("Processing {cpty}".format(cpty=party.Name()))
                party_code = party.add_info("SL_G1PartyCode")
                party_perfix = party.add_info("PERFIX_CLIENT")
                if party_perfix == "Yes":
                    party_perfix = "Y"
                else:
                    party_perfix = "N"
                party_taxable = party.add_info("TAXABLE_STATUS")
                if party_taxable == "Yes":
                    party_taxable = "Y"
                else:
                    party_taxable = "N"
                if party_code:
                    row_data["CODE"] = party_code
                    row_data["STD_TAXABLE"] = party_taxable
                    row_data["UDF22"] = party_perfix
                    writer.writerow(row_data)
    except Exception as e:
        LOGGER.info("Could not add file data because {err}".format(err=str(e)))
        raise Exception("Could not add file data because {error}".format(error=str(e)))

ael_variables = gen_uploader.get_ael_variables()
email_variable = ael_variables[4]
ael_variables.remove(email_variable)


def ael_main(dictionary):
    try:
        file_name = dictionary["file_name"]
        run_date = gen_uploader.get_input_date(dictionary)
        date_string = datetime.datetime.strptime(str(run_date), '%Y-%m-%d').strftime('%m%d')
        filename = "{file_name}_{file_date}01.txt".format(file_name=file_name, file_date=date_string)
        output_file, run_date = reporting_utils.get_directory(dictionary, filename, True)
        write_file_data(output_file, run_date)
        LOGGER.info("Completed successfully")
        LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))
    except Exception as e:
        LOGGER.info("Failed to write file because {err}".format(err=str(e)))
        raise Exception("Failed to write file because {error}".format(error=str(e)))
