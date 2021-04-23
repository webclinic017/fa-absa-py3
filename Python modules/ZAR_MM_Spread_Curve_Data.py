import acm
import csv
import FRunScriptGUI
import FUxCore

from at_logging import getLogger
from Spread_Curve_Sorter import sort_spreadpoints
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

ael_variables.add('curve_name',
                  label='curve name',
                  mandatory=True,
                  default="ZAR-MM-FundingSpr",
                  tab="Task Inputs")

ael_variables.add('Output file',
                  label='Output file',
                  mandatory=True,
                  default="/services/frontnt/Task/ZAR_MM_Funding_spreads.csv",
                  tab="Task Inputs")


def ael_main(ael_dict):
    gname = ael_dict['Output file']
    curve_name = ael_dict["curve_name"]
    try:
        with open(gname, "wb") as f:
            writer = csv.writer(f)
            writer.writerow(["RepDate", "Action", "yc", "date_period", "date_period.unit"])
            spread_curve_data = sort_spreadpoints(curve_name)
            for counter in range(len(spread_curve_data[spread_curve_data.keys()[-1]])):
                row1 = [spread_curve_data[key][counter] for key in spread_curve_data.keys()]
                row2 = [acm.Time.DateToday(), curve_name]
                writer.writerow(row2+row1)
        LOGGER.info("Completed successfully.")
    except Exception as e:
        LOGGER.error("Failed to write to file {}".format(gname))
        LOGGER.info(e)

    
