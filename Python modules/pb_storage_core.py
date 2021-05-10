"""
A module which contains an exception class and functions
for persistently storing the data
into Front Arena's custom text objects.
"""


TEXT_OBJECT_SUBTYPE = "prime brokerage"


class NoSuchTextObject(RuntimeError):

    """
    Custom exception class which indicates
    that a text object with the provided name/ID does not exist.
    """

    def __init__(self, text_object_id):
        exception_message = ("Text object with name/ID {0} "
                             "does not exist.").format(repr(text_object_id))
        super(NoSuchTextObject, self).__init__(exception_message)


def get_text_object(text_object_id):
    """
    Return the text object with the provided name/ID.

    If no such text object exists, raise an exception.
    """
    import acm
    text_object = acm.FCustomTextObject[text_object_id]
    if text_object is None:
        raise NoSuchTextObject(text_object_id)
    return text_object


def create_text_object(text_object_id, subtype=None):
    """
    Return a new text object with the provided name/ID
    and optionally also with the provided subtype.
    """
    import acm
    text_object = acm.FCustomTextObject()
    text_object.Name(text_object_id)
    if subtype:
        text_object.SubType(subtype)
    text_object.Commit()
    return text_object
