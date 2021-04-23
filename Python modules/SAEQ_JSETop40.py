import ael
ins = ael.Instrument["ZAR/ALSI"]

sFileName = '/services/front/scripts/temp/SAEQ_JSETop40_' + ael.date_today().to_string("%y%m%d") + '.txt'
print(sFileName)
fReport = open(sFileName, "w")

try:
    link = ins.combination_links()    
    for lnk in link.members():
        con = lnk.member_insaddr
        fReport.write(con.insid + "\n")
finally:
    fReport.close()

print("Top40 generated and saved sucessfully.")
