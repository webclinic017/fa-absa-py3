import acm
import csv
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger()

def delete_wrong_resets(cash_flow_number):
    cf = acm.FCashFlow[cash_flow_number]
    old_resets = cf.Resets()
    if len(old_resets) > 0:
        resets_to_delete = []
        for r in old_resets:
            resets_to_delete.append(r.Oid())
        acm.BeginTransaction()
        try:
            for r in resets_to_delete:
                #LOGGER.info("Deleting reset...")
                single_reset = acm.FReset[r]
                single_reset.Delete()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception("FAILED deleting single reset")
            raise
        LOGGER.info("FINISHED deleting!")

def write_new_resets(cash_flow, resets):
    #Write the new resets for the "Funding" cash flows
    LOGGER.info("STARTING write_new_resets() for {}...".format(cash_flow.Leg().IndexRef().Name()))
    acm.BeginTransaction()
    try:
        for r in resets:
            #LOGGER.info("Writing reset...")
            reset = acm.FReset()
            reset.CashFlow(cash_flow)
            reset.ResetType(r[0])
            reset.Day(r[1])
            reset.StartDate(r[2])
            reset.EndDate(r[3])
            reset.FixingValue(r[4])
            reset.ReadTime(r[5])
            reset.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Something went wrong when writing resets for {}...".format(cash_flow.Leg().IndexRef().Name()))

ael_variables = AelVariableHandler()
ael_variables.add("file_name", label="File Name", cls="string")

def ael_main(ael_dict):
    new_resets = []
    cf_number = 0
    file_name = ael_dict["file_name"]
    with open(file_name, "r") as output:
        csv_reader = csv.reader(output, delimiter=',')
        for row in csv_reader:
            if row[0] == "Instrument":
                new_resets = []
                ins_name = row[1]
                cf_number = row[2]
            elif row[0] == "END RESET" and len(new_resets) > 0:
                cf = acm.FCashFlow[cf_number]
                delete_wrong_resets(cf_number)
                write_new_resets(cf, new_resets)
                LOGGER.info("FINISHED writing resets!")
            else:
                new_resets.append(row)
    LOGGER.info("FINISHED")
