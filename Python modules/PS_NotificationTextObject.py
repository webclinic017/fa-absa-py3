'''-----------------------------------------------------------------------------
Stores issues encountered during the day in the text object.
Based on the comparison between the issues which were currently found 
and issues stored in the text object, status (resolved/unresolved) 
of issue can be returned.

HISTORY
================================================================================
Date            Change no      Developer            Description
--------------------------------------------------------------------------------
2021-02-26        ---          Katerina Frickova    Initial implementation

--------------------------------------------------------------------------------
'''

import acm
import json
from at_logging import getLogger
LOGGER = getLogger(__name__)


def load_json(text):
    try:
        return json.loads(text)
    except TypeError:
        LOGGER.error("[ERROR] Converting JSON string to Python dictionary. Detail: %s" % TypeError.message)
        return None
        
        
def to_json(text):
    try:
        return json.dumps(text, default=lambda x: None)
    except TypeError:
        LOGGER.error("[ERROR] Could not export data to JSON format. Detail: %s" % TypeError.message)
        
            
class NotificationTextObject(object):
    """
        A class for the manipulation with text object. 
        Here the text object serves as a storage of issues found by notification tasks.
    """
    
    def __init__(self, text_object_name, input_dict):
        self.text_object_name = text_object_name
        self.input_dict = input_dict
        
    def get_text_object(self):
        text_object = acm.FCustomTextObject.Select01('name={}'.format(self.text_object_name), None)
        if not text_object:
            LOGGER.info('Could not find Text Object. Name: {}'.format(self.text_object_name))
        return text_object
            
    def delete_text_object(self):
        text_object = self.get_text_object()
        if text_object:
            try:
                text_object.Delete()
            except Exception as e:
                LOGGER.error("[ERROR] Unable to delete text object. Detail: %s" % e)
                
    def update_text_object(self):
        """ Update issues stored in the text object."""
        
        text_object = self.get_text_object()
        resolved_issues = None
        
        if text_object and text_object.UpdateDay() == acm.Time.DateToday():
            LOGGER.info("Text object was already created today. Reading the data...")
            
            text_object_clone = text_object.Clone()
            text_in_object = load_json(text_object_clone.Text())
            
            if text_in_object:
                resolved_issues = {oid: issue_info for oid, issue_info in list(text_in_object.items()) if oid not in self.input_dict}

            text_in_object.update(self.input_dict)
            text_object_clone.Text(to_json(text_in_object))
            text_object.Apply(text_object_clone)
            text_object.Commit()
            
        else:
            LOGGER.info("Text Object does not exist or it was not updated since yesterday - Creating")
            if text_object:
                self.delete_text_object()
            new_text_object = acm.FCustomTextObject()  
            new_text_object.Name(self.text_object_name)
            new_text_object.Text(to_json(self.input_dict))
            new_text_object.Commit()
            
        return resolved_issues
            

