'''-----------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : Creates the blocks of a SWIFT message
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Francois Truter
CR NUMBER               : XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''

from gen_fixed_length_record_2 import Field
from gen_fixed_length_record_2 import ListField
from gen_fixed_length_record_2 import StringField
from gen_fixed_length_record_2 import IntField

from gen_swift_common import CRLF
from gen_swift_common import ComplexFieldBase
from gen_swift_mt_fields import TerminalAddress

from gen_absa_xml_config_settings import SwiftParamXmlConfig

SWIFT_NODE = 'AbcapSwiftParameters'

class TagField(Field):

    def __init__(self, name, tagId):
        Field.__init__(self, name, '', False)
        self._tagId = tagId
        
    def __str__(self):
        if self._value:
            return '{%(id)s:%(value)s}' % {'id': self._tagId, 'value': self._value}
        else:
            return ''

class Block(ComplexFieldBase):

    def __init__(self, name, blockId, fields):
        super(Block, self).__init__(name, fields)
        self._blockId = blockId
        
    def __str__(self):
        try:
            _str = ''
            for field in self._fields:
                _str += str(field)
            
            if _str:
                return '{%(id)i:%(value)s}' % {'id': self._blockId, 'value': _str}
            else:
                return ''
        except Exception as ex:
            raise Exception('Could not convert record [%(name)s] to string: %(ex)s' % {'name': self._name, 'ex': ex})
        
class BasicHeaderBlock(Block):

    def __init__(self):
        super(BasicHeaderBlock, self).__init__('Basic Header Block 1', 1, [
             ListField('ApplicationId', 1, ['F', 'A', 'L'], 'F', True),
             ListField('ServiceId', 2, ['01', '21'], '01', True),
             TerminalAddress('LogicalTerminal', True),
             IntField('SessionNumber', False, 4, 9999),
             IntField('SequenceNumber', False, 6, 999999)
        ])
        
        swiftParameters = SwiftParamXmlConfig(SWIFT_NODE)
        
        self.LogicalTerminal.BicCode = swiftParameters.LogicalTerminalBic
        self.LogicalTerminal.TerminalId = 'A'
    
class ApplicationHeaderBlock(Block):
    
    def __init__(self):
        Block.__init__(self, 'Application Header Block', 2, [
            ListField('InputOutput', 1, ['I', 'O'], 'I', True),
            IntField('MessageType', False, 3, None),
            TerminalAddress('Address', True),
            ListField('Priority', 1, ['S', 'N', 'U'], 'N', True)
        ])
        
        self.Address.TerminalId = 'X'
        
class UserHeaderBlock(Block):
    
    def __init__(self):
        Block.__init__(self, 'User Header Block', 3, [
            TagField('BankingPriorityCode', 113),
            TagField('MessageUserReference', 108)
        ])
        

class TrailerBlock(Block):

    def __init__(self):
        Block.__init__(self, 'Trailer Block', 5, [
            TagField('MessageAuthenticationCode', 'MAC'),
            TagField('Checksum', 'CHK')
        ])
        
class Body(Block):

    def __init__(self, fields):
        Block.__init__(self, 'Body', 4, fields)
    
    def __str__(self):
        try:
            _str = '{' + str(self._blockId) + ':' + CRLF
            for field in self._fields:
                fieldStr = str(field)
                if fieldStr:
                    _str += fieldStr + CRLF
            _str += '-}'

            return _str
        except Exception as ex:
            raise Exception('Could not convert record [%(name)s] to string: %(ex)s' % {'name': self._name, 'ex': ex})
