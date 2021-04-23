import ael
#Written by Abmw438
#Required for the SNI report

def Find_DG(Name,*rest):
    Name = Name[0][0]
    retDG = 9999 
    try:
        myFile = open('//v036syb004001/DART/ERM/DC/AEL_LOOKUP.csv', 'r')
        line = myFile.readline()
        while line:
            FRONT_NAME, SDS_NAME, DG_RATING = line.split(',')
            #print '*',Name,'*',FRONT_NAME,'*'
            if Name == FRONT_NAME:
                retDG = (int)(DG_RATING) 
                break
                #print FRONT_NAME,' ',SDS_NAME,' ',DG_RATING
            line = myFile.readline()
    except:
        print 'Error in opening the file'
    myFile.close()    
    return retDG




