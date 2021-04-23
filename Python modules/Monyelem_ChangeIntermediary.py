import acm
import csv

with open(r"C:\Users\monyelem\Documents\NewData.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    #Skip header
    next(csvreader)
    row_counter = 1
    for row in csvreader:
        row_counter += 1
        try:
            #Get parameters - only need to update corr3 (intermediary 2)
            party = acm.FParty[row[0]]
            currency = row[1]
            account_number = row[2]
            acc = acm.FAccount.Select01("party = %i and account = '%s' and currency = '%s'" % (party.Oid(), account_number, currency), None)
            print("PROCESSING row ", row_counter, ": ", party.Name(), currency, account_number)
            if row[7]:
                corr_bank_3 = acm.FParty[row[7]]
                cp_code_3 = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT' and alias = '%s'" % (corr_bank_3.Oid(), row[8]), None)
                #Make the change
                acc2 = acc.Clone()
                acc2.CorrespondentBank3(corr_bank_3)
                acc2.Bic3(cp_code_3)
                acc.Apply(acc2)
                acc.Commit()
                print("CHANGE successful for ", party.Name(), currency, account_number)
            else:
                print("NO CHANGE for ", party.Name(), currency, account_number)
        except Exception as e:
            print("ERROR while processing row ", row_counter)
            print(str(e))
            if "The chain of accounts contains gaps." in str(e):
                try:
                    corr_bank_1 = acm.FParty[row[3]]
                    cp_code_1 = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT' and alias = '%s'" % (corr_bank_1.Oid(), row[4]), None)
                    corr_bank_2 = acm.FParty[row[5]]
                    cp_code_2 = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT' and alias = '%s'" % (corr_bank_2.Oid(), row[6]), None)
                    corr_bank_3 = acm.FParty[row[7]]
                    cp_code_3 = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT' and alias = '%s'" % (corr_bank_3.Oid(), row[8]), None)
                    #Make the change
                    acc2 = acc.Clone()
                    acc2.CorrespondentBank(corr_bank_1)
                    acc2.Bic(cp_code_1)
                    acc2.CorrespondentBank2(corr_bank_2)
                    acc2.Bic2(cp_code_2)
                    acc2.CorrespondentBank3(corr_bank_3)
                    acc2.Bic3(cp_code_3)
                    acc.Apply(acc2)
                    acc.Commit()
                    print("CHANGE2 successful for ", party.Name(), currency, account_number)
                except Exception as e:
                    print("ERROR2 while processing row ", row_counter)
                    print(str(e))
            else:
                print("UNKNOWN ERROR!!!")
