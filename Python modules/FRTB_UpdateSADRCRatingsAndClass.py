"""--------------------------------------------------------------------
MODULE:         FRTB_UpdatePartyRating
    
DESCRIPTION:    This module contains a ael task that updates party FRTB ratings and classes on the Party table with a mapping file created from Spear and Client Static. 

                The file format is as follows:
                
                OID	FA Name	        Source System	Rating Type	Type
                9229	UNICREDIT SPA	1	        AA	        Corporates


History:        Created - Nicolaas Duvenage 2020-02-21
                Updated - Nicolaas Duvenage 2020-05-06
--------------------------------------------------------------------"""
import acm
import FRunScriptGUI

def createRatingsDict(input_file, source_system):
    ratings_dict = {}
    with open(str(input_file), 'r') as input:
        for line in input:
            split               = line.split(',')
            number              = split[0].rstrip()
            fa_oid              = split[1].rstrip()
            fa_name             = split[2].rstrip()
            file_source_sys     = split[3].rstrip()
            rating              = split[4].rstrip()
            issuer_type         = split[5].rstrip()
            
            if source_system == file_source_sys:
                ratings_dict[number] = [fa_oid, rating]
    return ratings_dict


def createClassDict(input_file, source_system):
    class_dict = {}
    with open(str(input_file), 'r') as input:
        for line in input:
            split               = line.split(',')
            number              = split[0].rstrip()
            fa_oid              = split[1].rstrip()
            fa_name             = split[2].rstrip()
            file_source_sys     = split[3].rstrip()
            rating              = split[4].rstrip()
            issuer_type         = split[5].rstrip()
            
            if source_system == file_source_sys:
                class_dict[number] = [fa_oid, issuer_type]
    return class_dict


def updateFRTBPartyRatings(ratings_dict):
    print("Updating Ratings...")
    print("---"*100)
    for key in ratings_dict:
        oid    = ratings_dict[key][0]
        rating = ratings_dict[key][1]
        party = acm.FParty.Select("oid = %s"%(oid))
        if len(party) == 0:
            print("Error - Party does not exist for Oid: %s"%(oid))
        elif len(party) != 0:
            party_obj = party[0]
            try:
                clone = party_obj.Clone()
                clone.Rating3(rating)
                party_obj.Apply(clone)
                party_obj.Commit()
                print("Info - Successfully updated party: %s with rating: %s"%(oid, rating))
            except Exception as e:
                print(str(e))
    print("Finished Rating update...")
    print("---"*100)

    
def updateDRCClass(class_dict, source_system):
    print("Updating DRC Classes...")
    print("---"*100)
    for key in class_dict:
        oid = class_dict[key][0]
        type = class_dict[key][1]
        party = acm.FParty.Select("oid = %s"%(oid))
        if len(party) == 0:
            print("Error - Party does not exist for Oid: %s"%(oid))
        elif len(party) != 0:
            party_obj = party[0]
            try:
                clone = party_obj.Clone()
                if source_system == '1': #1 = Capital
                    clone.Free4ChoiceList(type)
                elif source_system == '2': #2 = ARO
                    clone.Free5ChoiceList(type)
                party_obj.Apply(clone)
                party_obj.Commit()
                print("Info - Successfully updated party: %s with class: %s"%(oid, type))
            except Exception as e:
                print(str(e))
    print("Finished DRC Class update...")
    print ("---"*100)
    
input_file = FRunScriptGUI.InputFileSelection(('CSV Files (*.csv)|*.csv'))
tt_level   = 'Select the source system indicator, Capital = 1 or ARO = 2.'
tt_file    = 'Select the .csv Spear ratings file containg: SSID,FRTB Rating'

ael_variables = [ 
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            ['source_system',
            'Source System Indicator_Update Party Ratings',
            'string',  ['1', '2'], None,
            1, 0, tt_level, None, None],
            ['spear_ratings_file',
            'Spear Ratings File_Update Party Ratings',
            input_file, None, input_file,
            1, 1, tt_file, None, None]
            ]

def ael_main(ael_output):
    spear_ratings_file = ael_output['spear_ratings_file']
    source_system      = ael_output['source_system']
    ratings_dict       = createRatingsDict(spear_ratings_file, source_system)
    #updateFRTBPartyRatings(ratings_dict)
    class_dict         = createClassDict(spear_ratings_file, source_system)
    updateDRCClass(class_dict, source_system)
