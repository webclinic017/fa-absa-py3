
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       AMBA_GENERATE_MESSAGE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module generates an AMBA message bsaed on a specific imput data set.
                                The input set should look as follow:
                                List of a tuple containing the following:
                                    Path in a List of Strings.
                                    String for the enw List name to be inserted at the specified path.
                                    Dictionary containing the key value for the new tag in the AMBA messgae
                                    and the value .
                                    i.e. [([],'',{})]
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Front Arena and Python modules needed for Real Time ATS Worker.
----------------------------------------------------------------------------------------------------------'''
import amb

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules modules needed for AMBA_GENERATE_MESSAGE.
----------------------------------------------------------------------------------------------------------'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

'''----------------------------------------------------------------------------------------------------------
AMB Base class containing the header fields needed on an AMBA message.
----------------------------------------------------------------------------------------------------------'''
class AMBA_GENERATE_MESSAGE_BASE():
    def __init__(self, reserved, msgType, version, creationTime, source):
        self._reserved = reserved
        self._msgType = msgType
        self._version = version
        self._creationTime = creationTime
        self._source = source
        self.AMBA_Message = None
    
    '''----------------------------------------------------------------------------------------------------------
    Method to start the creation of the AMBA message.
    ----------------------------------------------------------------------------------------------------------'''
    def start_AMBA_Message(self):
        self.AMBA_Message = amb.mbf_start_message(self._reserved, self._msgType, self._version, self._creationTime, self._source)

'''----------------------------------------------------------------------------------------------------------
Class that generates an AMBA message from a specific input set.
----------------------------------------------------------------------------------------------------------'''
class AMBA_GENERATE_MESSAGE(AMBA_GENERATE_MESSAGE_BASE):
    def __init__(self, reserved = None, msgType = 'DEFAULT', version = '1.0', creationTime = None, source = 'DEFAULT', AMBADataInputLists = None):
        AMBA_GENERATE_MESSAGE_BASE.__init__(self, reserved, msgType, version, creationTime, source)
        self._AMBADataInputLists = AMBADataInputLists
    
    '''----------------------------------------------------------------------------------------------------------
    Function that added a Tag and a Value to an AMB object
    ----------------------------------------------------------------------------------------------------------'''
    def _add_TagAndValue(self, mbf_object, tagName, value):
        try:
            return mbf_object.mbf_add_string(tagName, value)
        except:
            return mbf_object.mbf_add_string(tagName, '')
    
    '''----------------------------------------------------------------------------------------------------------
    Function that adds a dictionary containing Tag names and values to a AMB object
    ----------------------------------------------------------------------------------------------------------'''
    def _add_DataDictionary(self, object, dataDictionary):
        for item in dataDictionary:
            self._add_TagAndValue(object, item, dataDictionary[item])

    '''----------------------------------------------------------------------------------------------------------
    Function that added an empty List to an AMB object
    ----------------------------------------------------------------------------------------------------------'''
    def _add_List_to_AMBA_Object(self, object, listName):
        object.mbf_start_list(listName)
        object.mbf_end_list()
        return object

    '''----------------------------------------------------------------------------------------------------------
    Function that adds a dictionary containing Tag ames ad values between a newly inserted List.
    ----------------------------------------------------------------------------------------------------------'''
    def _add_List_and_Data_to_AMBA_Object(self, object, listName, dataDictionary):
        newList = object
        if listName:
            newList = object.mbf_start_list(listName)
            
        if dataDictionary:
            self._add_DataDictionary(newList, dataDictionary)
        
        if listName:
            newList.mbf_end_list()

    '''----------------------------------------------------------------------------------------------------------
    Function that builds the Path structure of the AMBA message.
    ----------------------------------------------------------------------------------------------------------'''
    def _build_AMBA_Path_Structure(self, path, positionObject):
        if path and len(path) > 0:
            item = path[0]
            for obj in ambaUtils.objects_by_name(positionObject, ['', '!', '+'], item):
                path = path[1:]
                self._build_AMBA_Path_Structure(path, obj)
                break
            else:
                positionObject = self._add_List_to_AMBA_Object(positionObject, item)
                if len(path) > 1:
                    self._build_AMBA_Path_Structure(path, positionObject)
        else:
            return positionObject

    def add_element_to_amb_msg(self, string, value):
        self.AMBA_Message.mbf_add_string(string, value)

    '''----------------------------------------------------------------------------------------------------------
    Function that adds a list with a dictionary of data to a specific path on the AMBA object
    ----------------------------------------------------------------------------------------------------------'''
    def _get_Nodes_to_add_New_List(self, object, pathList, listName, dataDictionary):
        if not pathList:
            self._add_List_and_Data_to_AMBA_Object(object, listName, dataDictionary)
        if pathList:
            for obj in ambaUtils.objects_by_name(object, ['', '!', '+'], pathList[0]):
                if len(pathList) > 0:
                    pathList = pathList[1:]
                    self._get_Nodes_to_add_New_List(obj, pathList, listName, dataDictionary)
                else:
                    self._add_List_and_Data_to_AMBA_Object(obj, listName, dataDictionary)
    
    '''----------------------------------------------------------------------------------------------------------
    Function that builds a AMBA message based on a specifc input set.
    ----------------------------------------------------------------------------------------------------------'''
    def generate_AMBA_Message(self):
        self.start_AMBA_Message()
        for AMBADataInputList in self._AMBADataInputLists:
            self._build_AMBA_Path_Structure(AMBADataInputList[0], self.AMBA_Message)            
            self._get_Nodes_to_add_New_List(self.AMBA_Message, AMBADataInputList[0], AMBADataInputList[1], AMBADataInputList[2])
