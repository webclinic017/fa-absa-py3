'''----------------------------------------------------------------------------------------------------------------------------------
# Purpose                       :  Sets additional infos on trades from a csv upload file.

                                    ###############
                                    Column A should show the trade numbers and the rest of the columns should be the add_info values.
                                    The add_info column headings should be the actual names of the add_info fields on the trades.
                                    A                   B                       C
                                    Trade Number        add_info1 name          add_info2 name
                                    12345               add_info1 value         add_info2 value
                                    ###############
                                    
# Department and Desk           :  PCG
# Requester                     :  Lott Chidawaya
# Developer                     :  Willie van der Bank
# CR Number                     :  2012-06-26 278694
----------------------------------------------------------------------------------------------------------------------------------'''
import acm, string, ael

global tempTrades
global add_infos

tempTrades = {}
add_infos = []

def file_upload(filename):
    global tempTrades
    global add_infos
    add_infos = []
    tempLine = []
    
    try:
    	fhandle = open(filename)
    except:
    	print 'Could not open file'
	return
	
    #Load Headings (Which should be the Add_Info field names)
    fline = fhandle.readline()
    line = string.split(fline, ',')
    
    for tempVal in line[1:len(line)]:   #Exclude first column, which should be the heading "Trade"
        add_infos.append(tempVal.replace('\n', ''))
    #print add_infos    
    #Continue with objects and Add_Info values
    fline = fhandle.readline()
    while fline:
        line = string.split(fline, ',')
        for tempVal in line[1:len(line)]:       #Exclude first column, which should be the trade number
            tempLine.append(tempVal.replace('\n', ''))
        tempTrades[line[0]] = tempLine
        tempLine = []
        fline = fhandle.readline()

def UdateAddInfoMacro(temp,AddInfo,AddInfoName,trade,*rest):
    #try:
    trd = ael.Trade[trade]
    found = 0
    for ai in trd.additional_infos():
        if ai.addinf_specnbr.field_name == AddInfoName:
            found = 1
            ai_found = ai
    if found == 1:
        aicln = ai_found.clone()
        aicln.value = AddInfo
        aicln.commit()
    else:
        tcln = trd.clone()
        ai_new = ael.AdditionalInfo.new(tcln)
        ais = ael.AdditionalInfoSpec[AddInfoName]
        ai_new.addinf_specnbr = ais
        ai_new.value = AddInfo
        ai_new.commit()
    #print 'Add_Info(SL_Instruction_Note) on trade', trd.trdnbr, 'set to "' + AddInfo + '".'
    ael.poll()
    #return 'Updated'
        
    #except Exception, e:
    #    return 'Add_Info update failed', e
    #    print 'Add_Info update failed', e
        
ael_variables = [('file', 'Upload File', 'string', '', '', 1, 0, 'Must be full path and filename.')]

def ael_main(dict):
    file_upload(dict['file'])
    print 'Upload started...'
    for tT in tempTrades:
        count = 0
        for i in add_infos:
            #print tT, i, tempTrades[tT][count]
            try:
                UdateAddInfoMacro(1, tempTrades[tT][count], i, int(tT))
            except Exception, e:
                print 'Add_Info update failed on trade', tT, 'Error:', e
                print
                break
            count = count + 1
        print 'Trade', tT, 'updated sucessfully.'
    print 'Upload finished.'
