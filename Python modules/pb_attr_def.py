"""
A module implementing the AttributeDefinition class.
"""

from json import JSONEncoder


class AttributeDefinition(object):

    """
    A class used for storing name, description and other properties
    of individual fund attributes.
    """

    STRING_TYPE = "string"
    BOOL_TYPE = "bool"
    INT_TYPE = "int"
    FLOAT_TYPE = "float"
    DATE_TYPE = "date"

    MAIN_CATEGORY = "main"
    REFERENCES_CATEGORY = "references"
    IDS_CATEGORY = "ids"
    RATES_CATEGORY = "rates"
    SPREADS_CATEGORY = "spreads"
    PRODUCT_TYPE_CATEGORY = "product_type"
    ADD_PRODUCT_TYPE_CATEGORY = "add_product_type"

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the AttributeDefinition class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        attr_id = json_representation["attr_id"]
        name = json_representation["name"]
        description = json_representation["description"]
        data_type = json_representation["data_type"]
        category = json_representation["category"]
        editable = json_representation["editable"]
        attr_def = cls(attr_id=attr_id,
                       name=name,
                       description=description,
                       data_type=data_type,
                       category=category,
                       editable=editable)
        return attr_def


    def __init__(self,
                 attr_id,
                 name=None,
                 description=None,
                 data_type=None,
                 category=None,
                 editable=True):
        self.attr_id = attr_id
        if name is None:
            name = attr_id
        self.name = name
        self.description = description
        if data_type is None:
            data_type = self.STRING_TYPE
        self.data_type = data_type
        if category is None:
            category = self.MAIN_CATEGORY
        # FIXME: Not sure if this assert makes sense.
        assert category in (self.MAIN_CATEGORY,
                            self.REFERENCES_CATEGORY,
                            self.IDS_CATEGORY,
                            self.RATES_CATEGORY,
                            self.SPREADS_CATEGORY,
                            self.PRODUCT_TYPE_CATEGORY,
                            self.ADD_PRODUCT_TYPE_CATEGORY)
        self.category = category
        self.editable = editable


    def __repr__(self):
        representation = ("{0}(attr_id={1}, "
                          "name={2}, "
                          "description={3}, "
                          "data_type={4}, "
                          "category={5}, "
                          "editable={6})").format(type(self).__name__,
                                                  repr(self.attr_id),
                                                  repr(self.name),
                                                  repr(self.description),
                                                  repr(self.data_type),
                                                  repr(self.category),
                                                  repr(self.editable))
        return representation


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.attr_id == other.attr_id
                    and self.name == other.name
                    and self.description == other.description
                    and self.data_type == other.data_type
                    and self.category == other.category
                    and self.editable == other.editable)
        else:
            return False


class AttributeDefinitionEncoder(JSONEncoder):

    """
    A class which supports encoding of AttributeDefinition objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, AttributeDefinition):
            attr_def_s = {"type": type(obj).__name__,
                          "attr_id": obj.attr_id,
                          "name": obj.name,
                          "description": obj.description,
                          "data_type": obj.data_type,
                          "category": obj.category,
                          "editable": obj.editable}
            return attr_def_s
        else:
            return super(AttributeDefinitionEncoder, self).default(obj)
