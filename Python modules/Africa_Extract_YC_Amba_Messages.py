#Script used to sync Yield Curves from Abcap FA to Africa FA
#Should run in Absa and dump a file that will be amba loaded in Africa.
#Done in acm to allow for mapping and duplication of curves (1 in Absa -> 3 in Africa)
#due to time zones
#Previous solution was purely driven from amba ext and load by RTB based on flat files
#outside of FA containing RecAddrs - but this assumes the names are equal in both 
#installations and cannot easily handle mapping.
#Note - underlying curves still need to have the same name in Abcap/Africa.
#This simply does a text replace on the "YIELD_CURVE_NAME=" tag.

import acm
import amb

amba_tag_for_yc_replace = "YIELD_CURVE_NAME="

ael_variables=[
['yc_list_as_is', 'Dump YCs as-is_YC', acm.FYieldCurve, acm.FYieldCurve.Select(''), None, 0, 1,
    'Select the YCs to send across to FA Africa with the same name'],
['yc_names_rename_absa', 'Dump additional YCs.Absa Names.To be renamed_YC', 'string', None, None, 0, 0,
    'Type exact YC names(Abcap) to send across to FA Africa with replaced names. Comma separated list.'],
['yc_names_rename_africa', 'Dump additional YCs.Africa Names_YC', 'string', None, None, 0, 0,
    'Type YC names(Africa). Comma separated list.'],
['yc_file_name', 'Amba file name_YC',  'string', None, None, 0, 0,
    'Type full file path/name where the amba file should be dropped. \
    Will be picked up by separate amba.exe command to be loaded into FA Africa']]

def create_amba_message_from_obj(acmObj):
    if not acmObj:
        return ""
    generator = acm.FAMBAMessageGenerator()
    generator.SourceName("AbcapPyScript")
    msg = generator.Generate(acmObj).AsString()
    amb_obj = amb.mbf_create_buffer_from_data(msg).mbf_read()
    yc = amb_obj.mbf_find_object('YIELDCURVE', 'MBFE_BEGINNING')
    while yc.mbf_find_object("ADDITIONALINFO"):
        yc.mbf_remove_object()     

    return amb_obj.mbf_object_to_string()
    
def ael_main(dict):
    yc_list_as_is          = dict['yc_list_as_is']
    yc_names_rename_absa   = dict['yc_names_rename_absa'].split(',')
    yc_names_rename_africa = dict['yc_names_rename_africa'].split(',')
    yc_file_name           = dict['yc_file_name']
    
    #Remove blanks from lists, FA automatically adds a "" as item to list if user left it empty.
    while '' in yc_names_rename_absa   :yc_names_rename_absa.remove('')
    while '' in yc_names_rename_africa :yc_names_rename_africa.remove('')
    
    amba_message= ''
    
    #Build msgs for as-is list
    for yc in yc_list_as_is:
        amba_message += create_amba_message_from_obj(yc)
        print 'Added as-is message for %s' % yc.Name()
        break

    #Since we need to be able to send the same YC multiple times, cannot use item-picker in variables,
    #using just comma-separated strings.  YC might not exist or length of lists might not match.
    if len(yc_names_rename_absa) != len(yc_names_rename_africa):
        raise Exception('Error: Rename lists with Absa names and Africa names are not equal. Aborting...')
    
    #Build msgs for replace list
    for yc_name_absa, yc_name_africa in zip(yc_names_rename_absa, yc_names_rename_africa):
        yc = acm.FYieldCurve[yc_name_absa]
        if not yc:
            raise Exception('Error: YC name specified (%s)not found in Abcap FA. Aborting...' % (yc_name_absa))
        original_message = create_amba_message_from_obj(yc)
        replaced_message = original_message.replace(amba_tag_for_yc_replace+yc_name_absa,
                                                    amba_tag_for_yc_replace+yc_name_africa)
        amba_message += replaced_message
        print 'Added name replaced message for %s. New name is %s' % (yc_name_absa, yc_name_africa)

    print '\nFull amba message that will be written to file (%s):\n%s' %(yc_file_name, amba_message)
    
    try:
        output_file = open(yc_file_name, 'w')
        output_file.write(amba_message)
        output_file.close()
        print 'Wrote secondary output to:%s'%yc_file_name
        #print amba_message
    except IOError as e:
        print 'ERROR : Secondary output not created: I/O error({0}): {1}'.format(e.errno, e.strerror)
    except Exception as e:
        print 'ERROR : Secondary output not created: Unexpected error:', e
    
