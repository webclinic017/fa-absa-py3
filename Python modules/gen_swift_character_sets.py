'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Validates SWIFT character sets
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  695005
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 686159    Francois Truter           Initial Implementation
2011-06-24 695005    Francois Truter           Added RemoveInvalidCharacters
'''

class CharacterSetBase:
    VALID_CHARACTERS = []
    NAME = ''
    
    @staticmethod
    def ConvertToString(_list):
        if not _list:
            return ''

        _str = ''
        delimiter = ''
        for item in _list:
            _str += delimiter + str(item)
            delimiter = ','

        return _str

    @classmethod
    def _getInvalidCharacters(cls, _str):
        invalid = set()
        for character in _str:
            if character not in cls.VALID_CHARACTERS:
                invalid.add(character)
        return invalid
    
    @classmethod
    def ValidateFieldStr(cls, fieldName, _str):
        if not _str:
            return

        invalid = cls._getInvalidCharacters(_str)
        
        if invalid:
            if len(invalid) > 1:
                message = '%s: [%s] are not valid characters for %s'
            else:
                message = '%s: [%s] is not a valid character for %s'
            
            raise Exception(message % (fieldName, CharacterSetBase.ConvertToString(invalid), cls.NAME))
        
    
    @classmethod
    def ValidateField(cls, field):
        if field.Value:
            cls.ValidateFieldStr(field.Name, str(field.Value))
            
    @classmethod
    def RemoveInvalidCharacters(cls, _str):
        invalid = cls._getInvalidCharacters(_str)
        for character in invalid:
            _str = _str.replace(character, '')
        
        return _str

class CharacterSetX(CharacterSetBase):

    VALID_CHARACTERS = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '/', '-', '?', ':', '(', ')', '.', ',', "'", '+', '{', '}',
        '\r', '\n', ' '
    ]

    NAME = 'CHARACTER SET X'

class CharacterSetN(CharacterSetBase):
    
    VALID_CHARACTERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    NAME = 'CHARACTER SET N'
    
class CharacterSetA(CharacterSetBase):
    
    VALID_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    NAME = 'CHARACTER SET A'

class CharacterSetC(CharacterSetBase):
    
    VALID_CHARACTERS = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ]
    NAME = 'CHARACTER SET C'

