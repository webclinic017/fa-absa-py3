'''
    Purpose                 : Exclude simulated trades.
    Department and Desk     : Complience
    Requester               : Steve Smit
    Developer               : Heinrich Cronje, Conicov Andrei
    CR Number               : 612353, ABITFA-2298
'''

import ael, acm, string, time

ael_variables = [('InputFile', 'InputFile', 'string', None, 'F:', 1),
                 ('OutputFile', 'OutputFile', 'string', None, 'F:', 1),
                 ('Date', 'Date (YYYY-MM-DD)', 'date', ael.date_today(), ael.date_today(), 1),
                 ('IgnoreRows', 'Ignore rows', 'int', None, '1', 1)
                ]
                
def ael_main(dict):
    try:
        date = dict['Date'].to_string()
    except:
        date = dict['Date']
        
    inFile = dict['InputFile'] + '//' + date + '/RestrictedList.csv'
    outFile = dict['OutputFile'] + '//' + date + '/BarcapRestrictedList_Result.csv'
    ignoreRows = dict['IgnoreRows']
    if ignoreRows < 0:
        acm.Log("The 'Ignore Rows' has to be a positive number, found {0}. Using zero.".format(ignoreRows))
        ignoreRows = 0
    restrictedFileCreation(inFile, outFile, date, ignoreRows)

def _create_row_item(t, ins):
    t_direction = "Sell" if t.quantity < 0 else "Buy"
    item = []
    sds_number = ins.issuer_ptynbr.add_info('BarCap_Eagle_SDSID')
    item.append(sds_number)
    item.append(str(t.trdnbr))
    item.append(ins.insid)
    item.append(ins.instype)
    item.append(ins.issuer_ptynbr.ptyid)
    item.append(t.counterparty_ptynbr.ptyid)
    item.append(t.creat_usrnbr.name)
    item.append(t.creat_usrnbr.userid)
    item.append(t.creat_usrnbr.name)
    item.append(t.creat_usrnbr.grpnbr.grpid)
    item.append(t.creat_usrnbr.grpnbr.orgnbr.orgid)
    item.append(str(t.quantity))
    item.append(t_direction)
    item.append(time.strftime("%H:%M:%S", time.gmtime(t.time)))
    item.append(time.strftime("%Y-%m-%d", time.gmtime(t.time)))
    
    return item

def restrictedFileCreation(inputFile, outputFile, date, ignoreRows, *rest):
    #********** Input- Output file names **********
    
    inputFilename = inputFile
    outputFilename = outputFile
    
    #**********************************************
    
    #********** Open input file **********
    
    try:
        file = open(inputFilename, 'r')
        inputFlag = 1
    except:
        inputFlag = 0
        subject = 'Barcap Restricted List File not found for ' + date
        body = 'The input file was missing. No results were produced'
        acm.Log('SUBJECT: ' + subject + ': MESSAGE: ' + body)
            
    #*************************************
    
    if inputFlag:

        #********** If Input File Opened, read SDS numbers **********
        
        SDSNumbers = []
        
        [file.readline() for x in range(ignoreRows)]
        lineFile = file.readline()
        
        while lineFile:
            lineFile = lineFile.rstrip()
            lineF = string.split(lineFile, ',')
            if lineF[0] != '':
                if not SDSNumbers.__contains__(lineF[0]):
                    SDSNumbers.append(lineF[0])
            lineFile = file.readline()
        
        file.close()
        acm.Log("Found {0} unique SDS numbers in the file".format(len(SDSNumbers)))
        #*************************************************************
        
        #********** Get all Additional infos with field name BarCap_Eagle_SDSID **********
        
        addInfoSpec = ael.AdditionalInfoSpec['BarCap_Eagle_SDSID']
        addInfo = ael.AdditionalInfo.select('addinf_specnbr=%i' % addInfoSpec.specnbr)
        
        #*********************************************************************************
        
        #********** All Issuer Parties with BarCap_Eagle_SDSID that matched the input SDSID **********
        
        Issuers = []
        for SDS in SDSNumbers:
            for ai in addInfo:
                if SDS == ai.value:
                    party = ael.Party[ai.recaddr]
                    if party.issuer == 1:
                        Issuers.append(party.ptynbr)
        acm.Log("Found {0} issuers".format(len(Issuers)))                
        #*********************************************************************************************
        
        #********** Headings and output list for output file **********
        
        outputResult = []
        outputResult.append('SDSID,Trdnbr,Insid,Instype,Issuer,Counterparty,Trader,TraderUserId,TraderName,TraderGrpid,TraderOrgnbr,TrdQuantity,TrdDirection,TrdTime,TrdDate')
        
        #**************************************************************
        
        #********** Get All trades created on the specified date with a specified Issuer into the output list **********
        
        date = ael.date(date)    
        for i in Issuers:
            instr = ael.Instrument.select('issuer_ptynbr=%i' % i)
            for ins in instr:
                if ins.trades().members() != []:
                    for t in ins.trades().members():
                        entry = ''
                        if ael.date_from_time(t.creat_time) == date:
                            if t.status != 'Simulated':
                                entry_list = _create_row_item(t, ins)
                                entry = ','.join(entry_list)
                                outputResult.append(entry)
        
        #***************************************************************************************************************
        
        #********** Output File Creation **********
        acm.Log("Outputed {0} rows".format(len(outputResult)))
        try:
            file = open(outputFilename, 'w')

            for o in outputResult:
                file.write(o + '\n')

            file.close()
        except:
            subject = 'Result File of Barcap Restricted List was not created for date ' + date
            body = 'The result file was missing. No output was produced'
            acm.Log('SUBJECT: ' + subject + ': MESSAGE: ' + body)

        #******************************************

        acm.Log("Wrote secondary output to {0}".format(outputFilename))
        acm.Log("Completed successfully")
