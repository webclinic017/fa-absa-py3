'''
Purpose                 :SalesCredit Feed,, Updated to use ACM Date,Updated To Correct String Conversion, Updated To Handle exceptions 
Department and Desk     :IT
Requester:              :Daniel Simoes
Developer               :Henk Nel,Ickin Vural
CR Number               :C000000469235,C000000470674,C000000476513
'''

import ael, acm

def GetSalesData(temp,FileName,Directory,Date, *rest):

    

    filename            =  Directory + FileName
    outfile             =  open(filename, 'w')
    outfile.close()
    
    
    
    outfile = open(filename, 'a')

    TrdNbr                              =       'TrdNbr'
    Sales_Person1                       =       'Sales_Person1'
    Sales_Person2                       =       'Sales_Person2'
    Sales_Person3                       =       'Sales_Person3'
    Sales_Person4                       =       'Sales_Person4'
    Sales_Person5                       =       'Sales_Person5'
    Sales_Credit1                       =       'Sales_Credit1'       
    Sales_Credit2                       =       'Sales_Credit2' 
    Sales_Credit3                       =       'Sales_Credit3' 
    Sales_Credit4                       =       'Sales_Credit4' 
    Sales_Credit5                       =       'Sales_Credit5' 
    ValueAddCredits                     =       'ValueAddCredits'          
    ValueAddCredits2                    =       'ValueAddCredits2'                
    ValueAddCredits3                    =       'ValueAddCredits3'                
    ValueAddCredits4                    =       'ValueAddCredits4'                
    ValueAddCredits5                    =       'ValueAddCredits5'                
    Shadow_Revenue_Type                 =       'Shadow_Revenue_Type'
    Repday                              =       'Repday'

    outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(TrdNbr, Sales_Person1, Sales_Credit1, Sales_Person2, Sales_Credit2, Sales_Person3, Sales_Credit3, Sales_Person4, Sales_Credit4, Sales_Person5, Sales_Credit5, ValueAddCredits, ValueAddCredits2, ValueAddCredits3, ValueAddCredits4, ValueAddCredits5, Shadow_Revenue_Type, Repday))


    outfile.close()



    if Date:
        Date = ael.date(Date)
        LastBankingDay = acm.Time().AsDate(Date)
    else:
        Date = ael.date_today()
        LastBankingDay = acm.Time().AsDate(Date)
        
        
    
    trades = acm.FTrade.Select("updateTime >= '%s'" %(LastBankingDay))


    



    for value in trades:
        outfile = open(filename, 'a')
        t = ael.Trade[value.Oid()]
        writerecord = 0
        if t.sales_person_usrnbr != None:
            writerecord = 1
        for i in range(2, 7):
            field = 'Sales_Person' + str(i)
            if t.add_info(field) != '':
                writerecord = 1
        if writerecord == 1:

            TrdNbr                      =      str(t.trdnbr)
            
            Sales_Person1               =      ''
            
            try:
                Sales_Person1           =      t.sales_person_usrnbr.userid
            except:
                Sales_Person1           =      ''
                
            Sales_Person1               =     str(Sales_Person1)
                
            Sales_Person2               =     str(t.add_info('Sales_Person2'))
            Sales_Person3               =     str(t.add_info('Sales_Person3'))
            Sales_Person4               =     str(t.add_info('Sales_Person4'))
            Sales_Person5               =     str(t.add_info('Sales_Person5'))
            
            
            Sales_Credit1               =     ''
            
            try:
                Sales_Credit1           =     t.sales_credit
            except:
                Sales_Credit1           =     ''
                
            Sales_Credit1               =     str(Sales_Credit1)
                
            Sales_Credit2               =     str(t.add_info('Sales_Credit2'))
            Sales_Credit3               =     str(t.add_info('Sales_Credit3'))
            Sales_Credit4               =     str(t.add_info('Sales_Credit4'))
            Sales_Credit5               =     str(t.add_info('Sales_Credit5'))

            ValueAddCredits             =     str(t.add_info('ValueAddCredits'))
            ValueAddCredits2            =     str(t.add_info('ValueAddCredits2'))
            ValueAddCredits3            =     str(t.add_info('ValueAddCredits3'))
            ValueAddCredits4            =     str(t.add_info('ValueAddCredits4'))
            ValueAddCredits5            =     str(t.add_info('ValueAddCredits5'))

            if str(t.add_info('Shadow_Revenue_Type')) == '':
                Shadow_Revenue_Type     =     'Auto'
            else:
                Shadow_Revenue_Type     =     str(t.add_info('Shadow_Revenue_Type'))



            Repday                      =     LastBankingDay

            outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(TrdNbr, Sales_Person1, Sales_Credit1, Sales_Person2, Sales_Credit2, Sales_Person3, Sales_Credit3, Sales_Person4, Sales_Credit4, Sales_Person5, Sales_Credit5, ValueAddCredits, ValueAddCredits2, ValueAddCredits3, ValueAddCredits4, ValueAddCredits5, Shadow_Revenue_Type, Repday))

        outfile.close()
    return filename


