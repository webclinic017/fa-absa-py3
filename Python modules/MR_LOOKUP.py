import ael
#Written by Abmw438
#LookupFunction
#example of ASQL
#select t.Issuer 'Issuer',
#MR_LOOKUP.VLookup(t.Issuer,0,2,'//v036syb004001/DART/ERM/DC/AEL_LOOKUP.csv') 'DG_RATING'
#Thus 1. The item to you want to find
#     2. The column where you want to find it
#     3. The column that you want to return
#     4. The csv file where these columns are stored


def VLookup(Args,*rest):
    ColLookup = (int)(Args[0][1]) #Args[0][1]
    ColReturn = (int)(Args[0][2]) #Args[0][2]
    ToLookup = Args[0][0] #Args[0][0]
    retDG = '9999'
    #FileToUse = '//v036syb004001/DART/ERM/DC/AEL_LOOKUP.csv' #Args[0][3]
    FileToUse = Args[0][3]
    try:
        myFile = open(FileToUse, 'r')
        line = myFile.readline()
        Test = []
        while line:
            Test = line.split(',')
            if ToLookup == Test[ColLookup]:
                #retDG = (int)(Test[ColReturn])
                #print Test[ColReturn]
                retDG = Test[ColReturn] 
                break
            line = myFile.readline()
    except:
        print 'Error in opening the file'
    myFile.close() 
    return retDG





