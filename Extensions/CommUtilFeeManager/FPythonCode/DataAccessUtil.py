'''
MODULE
    DataAccess - A class that allows you to read, write and delete you the TextObject table. 
   
HISTORY
    Date        Developer               Notes
    2017-10-09  Ntuthuko Matthews       created
'''


import ael
from HelperFunctions import HelperFunctions


class DataAccess(object):

    def __init__(self):
        self.name = ''
        self.text_object = None

    def Select(self, name, convertToJson=True):
        self.name = name
        self.text_object = ael.TextObject.read('type = "Customizable" and name = "{0}"'.format(self.name))
        #convert to json if the textobject exists
        if self.text_object and convertToJson:
            text = self.text_object.get_text()[1:-1]
            return HelperFunctions().load_json(text)
        elif self.text_object:
            return self.text_object
        return None

    def Save(self, data, name, serialze=True):
        self.name = name
        #get a textobject based on the name
        self.text_object = self.Select(self.name, False)
        if serialze:
            parsed_json = HelperFunctions().add_json(data)
        if not self.text_object:
            to = ael.TextObject.new()
            to.type = 'Customizable'
            to.name = self.name
            to.data = str(parsed_json)
            to.commit()
            self.text_object = to  
        else:
            self.text_object = self.text_object.clone()
            self.text_object.data = str(parsed_json)
            self.text_object.commit()
        ael.poll()

    def Delete(self, name):
        self.name = name
        self.text_object = self.Select(self.name, False)
        if self.text_object:
            self.text_object = self.text_object.clone()
            self.text_object.delete()
            self.text_object.commit()
            self.text_object = None
            ael.poll()
