"""------------------------------------------------------------------------
MODULE
    AddBusinessCenters -
DESCRIPTION:
    This file is to be customised at user end to add more calendars and their business centers as per the business need.
VERSION: %R%
--------------------------------------------------------------------------"""
import acm
name = "BusinessCenter"

def getACMVersion():
    version = acm.Version()    
    indexPos = version.find(',')
    if indexPos != -1:
        versionNumber = version[0:indexPos]
        indexPos = versionNumber.find('.')
        indexPos1 = versionNumber.find('.', indexPos + 1)
        if indexPos1 > -1:
            versionNumber = versionNumber[0: indexPos1]
        return float(versionNumber)
    else:
        return float(version)
        
def setAddInfo(name, object, value):
    """set the additional infos on the calendar"""
    ai=getattr(object.AdditionalInfo(), name)
    if not ai():
        ais = acm.FAdditionalInfoSpec[name]
        if getACMVersion() >= 2015.4:
            object.AddInfoValue(ais, value)
            object.Commit()
        else:
            ai = acm.FAdditionalInfo()
            ai.Recaddr(object.Oid())
            ai.AddInf(ais)
            ai.FieldValue(value)
            ai.Commit()
        print "'%s' -- (BusinessCenter) -->'%s' added" %(object.Name(), value)        
    else:
        print "'%s'-- BusinessCenter --> '%s' already present" %(object.Name(), value)        
        object.Commit()
    

def setBusinessCenters():
    """Assign BusinessCenter value (AddInfo) to the calendars"""
    bsDict = {
        'Bangkok': 'THBA', 'Beijing': 'CHBE', 'Brasilia': 'BRBR', 'Budapest': 'HUBU',
        'Copenhagen': 'DKCO', 'Dubai': 'AEDU', 'Hong Kong': 'CHHK', 'Istanbul': 'TUIS',
        'Johannesburg': 'ZAJO', 'Kuala Lumpur': 'MAKL', 'London': 'GBLO', 'Manila': 'PHMA',
        'Moscow': 'RUMO', 'New York': 'USNY', 'Oslo': 'NOOS', 'Riyadh': 'SARI',
        'Seoul': 'KRSE', 'Singapore': 'SISI', 'Stockholm': 'SEST', 'Sydney': 'AUSY',
        'Taipei': 'TWTA', 'Target' : 'EUTA', 'Tel-Aviv': 'ILTA', 'Tokyo': 'JPTO',
        'Toronto': 'CATO', 'Warsaw': 'PLWA', 'Wellington': 'NZWE', 'Zurich': 'CHZU'
        }
    for cal in acm.FCalendar.Select(''):
        calN = cal.Name()
        if not calN in bsDict.keys():
            print "No BusinessCenter information provided for '%s'."%calN
        else:
            if not IsBusinessCenterOnCal():
                try:
                    setAddInfo(name, cal, bsDict[calN])
                except:
                    print "Restart PRIME after adding the AddintionalInfoSpec and rerun this script to add AdditionalInfos."
                    break
            else:
                if cal.BusinessCenter() == bsDict[calN]:
                    print "'%s'-- BusinessCenter --> '%s' already present" %(cal.Name(), bsDict[calN])
                else:
                    cal.BusinessCenter(bsDict[calN])
                    cal.Commit()
                    print "'%s' -- (BusinessCenter) -->'%s' added" %(cal.Name(), bsDict[calN])

def addInfoSpecs():
    """add the BusinessCenter AdditionalInfoSpec"""
    oldais = acm.FAdditionalInfoSpec["BusinessCentre"]    
    if oldais:
        cloned_ais = oldais.Clone()        
        cloned_ais.FieldName(name)       
        oldais.Apply(cloned_ais)      
        oldais.Commit()
        print 'Renamed BusinessCentre to BusinessCenter'    
    else:        
        ais = acm.FAdditionalInfoSpec[name]            
        if ais:
            print "Already have AdditionalInfoSpec '%s'; hence not adding it." %name        
        else:
            ais = acm.FAdditionalInfoSpec()            
            ais.FieldName = name 
            ais.DataTypeGroup(acm.FEnumeration['enum(B92DataGroup)'].Enumeration('Standard'))      

          
            typ = acm.FEnumeration['enum(B92StandardType)'].Enumeration('String')
            ais.DataTypeType(typ)
            ais.Description = "Business Day Calendar"                
            ais.RecType('Calendar')
            ais.Commit()
            print "AdditionalInfoSpec '%s' added on Calendar to database ." %name            

def IsBusinessCenterOnCal():
    isBusinessCenter = True
    try:
        cal = acm.FCalendar.Select('')[0]
        cal.BusinessCenter()
    except:
        isBusinessCenter = False
    return isBusinessCenter
    
if not IsBusinessCenterOnCal():
    addInfoSpecs()
setBusinessCenters()





