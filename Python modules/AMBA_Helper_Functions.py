'''----------------------------------------------------------------------------------------------------------
MODULE                  :       AMBA_Helper_Functions
PROJECT                 :       PACE MM
PURPOSE                 :       Class that contains methods to be used for AMBA message processing.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------
DESCRIPTION OF FUNCTIONS:

    objects_by_name             :       Input:  Type            Description
                                                AMB Object      Parent AMB object. Attributes within this AMB object
                                                                will be itterated.
                                                List            Prefixes of the AMB objects that should be returned ['','!','+']
                                                String          Name of the objects looking for inside the specified AMB object.
                                        Output: Returns all child AMB objects from a given AMB object based on specified prefixes.
    object_by_name              :       Input:  Type            Description
                                                AMB Object      Parent AMB object. Attributes within this AMB object
                                                                will be itterated.
                                                List            Prefixes of the first AMB object that should be returned ['','!','+']
                                                String          Name of the object looking for inside the specified AMB object.
                                        Output: Returns the first child specified AMB object from a given AMB object based on
                                                specified prefixes (insert, update...).
    get_object_type             :       Input:  Type            Description
                                                AMB Object      AMB object that the ADS table name is required.
                                        Output: Returns the table name of an AMB object. More tables can be added.
    get_AMBA_Object_Value       :       Input:  Type            Description
                                                AMB Object      AMB object on which a specified field value is required.
                                                String          The field name that is required on the specified AMB object.
                                        Output: Returns the string value of an AMB object field.
'''

class AMBA_Helper_Functions():
    @classmethod
    def objects_by_name(self, parent_obj, name_prefixes, name):
        obj = parent_obj.mbf_first_object()
        names = list()
        for name_prefix in name_prefixes:
            names.append(name_prefix + name)
        while obj:
            if obj.mbf_get_name() in names:
                yield obj
            obj = parent_obj.mbf_next_object()

    @classmethod
    def object_by_name(self, parent_obj, name_prefixes, name):
        for obj in self.objects_by_name(parent_obj, name_prefixes, name):
            return obj
        return None

    @classmethod
    def get_object_type(self, m):
        msgType_obj = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
        msgType = msgType_obj.mbf_get_value()
        if msgType in ('INSERT_TRADE', 'UPDATE_TRADE'):
            return 'TRADE'
        elif msgType in ('INSERT_INSTRUMENT', 'UPDATE_INSTRUMENT'):
            return 'INSTRUMENT'
        return None

    @classmethod
    def get_AMBA_Object_Value(self, parent_object, field):
        if parent_object:
            object = parent_object.mbf_find_object(field)
            if object:
                object_value = object.mbf_get_value()
                return object_value
        return None
