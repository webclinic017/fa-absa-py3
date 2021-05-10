import acm
import ael
import FRunScriptGUI
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
ael_variables.add('rate_index',
                  label='rate index',
                  mandatory=True,
                  default='"ZAR-PRIME","ZAR-REPO","ZAR-SAFEX-ON-DEP","ZAR-JIBAR-1M","ZAR-JIBAR-3M","ZAR-JIBAR-6M","ZAR-JIBAR-9M","ZAR-JIBAR-12M"',
                  multiple=True,
                  tab="Task Inputs")

ael_variables.add('Output file',
                  label='Output file',
                  mandatory=True,
                  default="/services/frontnt/Task/Rate_indicies.csv",
                  tab="Task Inputs")


def benchmark_data_extractor(data_input, fname):
    # pulling the prices rate indicies
    delimeter = ","
    with open(fname, "wb") as file:
        file.write(
            "Date" + delimeter + "Time Last Updated" + delimeter + "Instrument" + delimeter + "Market Name" + delimeter + "Bid" + delimeter + "Last" + delimeter + "Settle" + delimeter + "Low" + delimeter + "High" + "\n")
        for ins_name in data_input["Rate Index Name"]:
            ins = acm.FInstrument[str(ins_name)]
            for fp in ins.Prices():
                if fp.Market().Name() == "SPOT_MID" and ael.date(fp.Day()).to_string(
                        "%Y-%m-%d") == ael.date_today().to_string("%Y-%m-%d"):
                    file.write(ael.date(fp.Day()).to_string("%d-%m-%Y") + delimeter + str(
                        fp.UpdateTime()) + delimeter + ins_name + delimeter + fp.Market().Name() + delimeter + str(fp.Bid()) + delimeter + str(
                        fp.Last()) + delimeter
                            + str(fp.Settle()) + delimeter + str() + delimeter + str() + "\n")


def ael_main(ael_dict):
    data_input = {"Rate Index Name": ael_dict['rate_index']}
    fname = ael_dict['Output file']
    try:
        benchmark_data_extractor(data_input, fname)
        LOGGER.info("Completed successfully.")
    except Exception as e:
        LOGGER.error("Failed while trying to extract data for zar rate indicies.")
        LOGGER.info(e)
