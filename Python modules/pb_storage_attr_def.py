"""
A module which contains the class and functions
for persistently storing the instances
of AttributeDefinition class into Front Arena.
"""

from json import dumps, JSONDecoder

from pb_attr_def import (AttributeDefinition,
                         AttributeDefinitionEncoder)
from pb_storage_core import (create_text_object,
                             get_text_object,
                             NoSuchTextObject,
                             TEXT_OBJECT_SUBTYPE)


class AttributeDefinitionStorage(object):

    """
    A class providing access to all the instances
    of the AttributeDefinition class
    which are persistently stored in Front Arena.
    """

    cls_text_object_id = "pb_attr_defs"

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the AttributeDefinitionStorage class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        attr_defs_s = json_representation["attr_defs"]
        attr_defs = {}
        for attr_id, attr_def in attr_defs_s.items():
            attr_defs[attr_id] = AttributeDefinition.from_json(attr_def)
        attr_def_storage = cls(attr_defs=attr_defs)
        return attr_def_storage


    def __init__(self, text_object_id=cls_text_object_id, attr_defs=None):
        self.text_object_id = text_object_id
        if attr_defs is None:
            self.attr_defs = {}
        else:
            assert isinstance(attr_defs, dict)
            self.attr_defs = attr_defs


    def __repr__(self):
        representation = ("{0}(text_object_id={1}, "
                          "attr_defs={2})").format(type(self).__name__,
                                                   repr(self.text_object_id),
                                                   repr(self.attr_defs))
        return representation


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.text_object_id == other.text_object_id
                    and self.attr_defs == other.attr_defs)
        else:
            return False


    def load(self, text_object_id=None):
        """
        Load the data for the current instance
        from the underlying text object.

        If the text_object_id parameter is provided,
        it will be used to replace the stored text object ID
        before getting the underlying text object.
        """
        if text_object_id:
            self.text_object_id = text_object_id
        text_object = get_text_object(self.text_object_id)
        json_string = text_object.Text()
        decoder = JSONDecoder()
        json_representation = decoder.decode(json_string)
        instance = self.from_json(json_representation)
        self.attr_defs = instance.attr_defs


    def save(self, text_object_id=None):
        """
        Save the data of the current instance
        to the underlying text object.

        If the text_object_id parameter is provided,
        it will be used to replace the stored text object ID
        before the save will take place.
        """
        if text_object_id:
            self.text_object_id = text_object_id
        text_object = get_text_object(self.text_object_id)
        json_string = dumps(self,
                            cls=AttributeDefinitionStorageEncoder,
                            indent=4)
        text_object.Text(json_string)
        text_object.Commit()


def init(overwrite=False):
    """
    Initialize the presistent storage of objects
    representing the prime brokerage attribute definitions.
    """
    # Try to get an existing text object which holds
    # the prime brokerage attribute definition storage.
    text_object_id = AttributeDefinitionStorage.cls_text_object_id
    try:
        get_text_object(text_object_id)
        if not overwrite:
            return
    except NoSuchTextObject:
        create_text_object(text_object_id, subtype=TEXT_OBJECT_SUBTYPE)
    # Save a valid content to this text object.
    tmp_attr_def_storage = AttributeDefinitionStorage()
    tmp_attr_def_storage.save()


class AttributeDefinitionStorageEncoder(AttributeDefinitionEncoder):

    """
    A class which supports encoding
    of AttributeDefinitionStorage objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, AttributeDefinitionStorage):
            attr_def_storage_s = {"type": type(obj).__name__,
                                  "attr_defs": obj.attr_defs}
            return attr_def_storage_s
        else:
            return super(AttributeDefinitionStorageEncoder, self).default(obj)
