import acm
import xlrd

path = "Y:\Jhb\Secondary Markets IT Deployments\FA\Change Pending\List of clients for upload sheet.xlsx"
xl_workbook = xlrd.open_workbook(path)

sheet_names = xl_workbook.sheet_names()
xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

failed_to_update = []
counter = 0
for i in range(1, xl_sheet.nrows):
    counter_party_name = xl_sheet.cell(i, 0).value

    try:
        counter_party = acm.FParty[str(counter_party_name)]
        if counter_party:
            try:
                acm.BeginTransaction()  
                counter_party.AdditionalInfo().StriataAcceptReject  = 'AcceptReject' 
                counter_party.AdditionalInfo().StriataPassword = 'No'
                counter_party.Commit()
                print "updated counter party: %s - StriataAcceptReject: %s,  StriataPassword: %s" % (
                    counter_party.Name(),
                    counter_party.AdditionalInfo().StriataAcceptReject(),
                    counter_party.AdditionalInfo().StriataPassword()
                )
                for c in counter_party.ConfInstructions():
                    if c.Name() == 'Deposit Adjust Deposit Email':
                        old_trans_type = c.Transport()
                        c.Transport = 'File'
                        c.Commit()
                        print "Updated ConfInstructions 'Deposit Adjust Deposit Email' set Transport Type to %s from %s" % (
                        c.Transport(),
                        old_trans_type
                        )
                        break
                counter += 1
                acm.CommitTransaction()
                print "-----------------------"
            except Exception, error:
                print error
                failed_to_update.append(str(counter_party_name))
                acm.AbortTransaction()
        else:
            failed_to_update.append(counter_party_name)
    except Exception, error:
        print error
        failed_to_update.append(str(counter_party_name))

print "Completed %s Successfully, %s Failed" % (counter, len(failed_to_update))
print "Failed %s" % failed_to_update