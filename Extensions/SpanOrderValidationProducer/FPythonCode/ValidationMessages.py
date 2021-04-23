""" Compiled: 2015-09-23 14:33:50 """

# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='ValidationMessages.proto',
  package='PaceValidation',
  serialized_pb='\n\x18ValidationMessages.proto\x12\x0ePaceValidation\"\xc9\x06\n\nDefinition\x12\x11\n\trequestid\x18\x01 \x01(\t\x12\x37\n\toperation\x18\x02 \x01(\x0e\x32$.PaceValidation.Definition.Operation\x12\x39\n\nvalidation\x18\x03 \x03(\x0b\x32%.PaceValidation.Definition.Validation\x12\x16\n\x0emarketserverid\x18\x04 \x01(\t\x1a\x90\x04\n\nValidation\x12\x37\n\tbuyorsell\x18\x01 \x01(\x0e\x32$.PaceValidation.Definition.BuyOrSell\x12\x10\n\x08quantity\x18\x02 \x01(\x01\x12\x41\n\x0epricecondition\x18\x03 \x01(\x0e\x32).PaceValidation.Definition.PriceCondition\x12\r\n\x05price\x18\x04 \x01(\x01\x12\x13\n\x0borderbookid\x18\x05 \x01(\t\x12\x11\n\treference\x18\x06 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x07 \x01(\t\x12\x0e\n\x06trader\x18\x08 \x01(\t\x12H\n\x0c\x65xtendeddata\x18\t \x03(\x0b\x32\x32.PaceValidation.Definition.Validation.ExtendedData\x12\x14\n\x0cvalidationno\x18\n \x01(\x05\x12\x15\n\rmarketorderid\x18\x0b \x01(\t\x12\x15\n\rdeltaquantity\x18\x0c \x01(\x01\x12\x0f\n\x07orderid\x18\r \x01(\t\x12\x37\n\toperation\x18\x0e \x01(\x0e\x32$.PaceValidation.Definition.Operation\x12\x19\n\x11origmarketorderid\x18\x0f \x01(\t\x1a)\n\x0c\x45xtendedData\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t\";\n\tOperation\x12\x0e\n\nENTERORDER\x10\x00\x12\x0f\n\x0bMODIFYORDER\x10\x01\x12\r\n\tSHAPEDEAL\x10\x02\"\x1e\n\tBuyOrSell\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\",\n\x0ePriceCondition\x12\x0b\n\x07LIMITED\x10\x01\x12\r\n\tUNLIMITED\x10\x02\"\xd2\x01\n\x06Result\x12\x11\n\trequestid\x18\x01 \x01(\t\x12\x17\n\x0frequestaccepted\x18\x02 \x01(\x08\x12\x41\n\x11validationreplies\x18\x03 \x03(\x0b\x32&.PaceValidation.Result.ValidationReply\x1aY\n\x0fValidationReply\x12\x14\n\x0cvalidationno\x18\x01 \x01(\x05\x12\x14\n\x0c\x65rrormessage\x18\x02 \x01(\t\x12\x1a\n\x12validationaccepted\x18\x03 \x01(\x08\"\x18\n\tResultKey\x12\x0b\n\x03key\x18\x01 \x01(\tB&\n\x0e\x63om.frontarenaB\x12ValidationMessagesH\x03')



_DEFINITION_OPERATION = descriptor.EnumDescriptor(
  name='Operation',
  full_name='PaceValidation.Definition.Operation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='ENTERORDER', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='MODIFYORDER', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='SHAPEDEAL', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=749,
  serialized_end=808,
)

_DEFINITION_BUYORSELL = descriptor.EnumDescriptor(
  name='BuyOrSell',
  full_name='PaceValidation.Definition.BuyOrSell',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='BUY', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='SELL', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=810,
  serialized_end=840,
)

_DEFINITION_PRICECONDITION = descriptor.EnumDescriptor(
  name='PriceCondition',
  full_name='PaceValidation.Definition.PriceCondition',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='LIMITED', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='UNLIMITED', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=842,
  serialized_end=886,
)


_DEFINITION_VALIDATION_EXTENDEDDATA = descriptor.Descriptor(
  name='ExtendedData',
  full_name='PaceValidation.Definition.Validation.ExtendedData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='PaceValidation.Definition.Validation.ExtendedData.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='PaceValidation.Definition.Validation.ExtendedData.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=706,
  serialized_end=747,
)

_DEFINITION_VALIDATION = descriptor.Descriptor(
  name='Validation',
  full_name='PaceValidation.Definition.Validation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='buyorsell', full_name='PaceValidation.Definition.Validation.buyorsell', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='quantity', full_name='PaceValidation.Definition.Validation.quantity', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pricecondition', full_name='PaceValidation.Definition.Validation.pricecondition', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='price', full_name='PaceValidation.Definition.Validation.price', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='orderbookid', full_name='PaceValidation.Definition.Validation.orderbookid', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='reference', full_name='PaceValidation.Definition.Validation.reference', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='account', full_name='PaceValidation.Definition.Validation.account', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='trader', full_name='PaceValidation.Definition.Validation.trader', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='extendeddata', full_name='PaceValidation.Definition.Validation.extendeddata', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='validationno', full_name='PaceValidation.Definition.Validation.validationno', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='marketorderid', full_name='PaceValidation.Definition.Validation.marketorderid', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='deltaquantity', full_name='PaceValidation.Definition.Validation.deltaquantity', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='orderid', full_name='PaceValidation.Definition.Validation.orderid', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='operation', full_name='PaceValidation.Definition.Validation.operation', index=13,
      number=14, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='origmarketorderid', full_name='PaceValidation.Definition.Validation.origmarketorderid', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DEFINITION_VALIDATION_EXTENDEDDATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=219,
  serialized_end=747,
)

_DEFINITION = descriptor.Descriptor(
  name='Definition',
  full_name='PaceValidation.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='requestid', full_name='PaceValidation.Definition.requestid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='operation', full_name='PaceValidation.Definition.operation', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='validation', full_name='PaceValidation.Definition.validation', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='marketserverid', full_name='PaceValidation.Definition.marketserverid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DEFINITION_VALIDATION, ],
  enum_types=[
    _DEFINITION_OPERATION,
    _DEFINITION_BUYORSELL,
    _DEFINITION_PRICECONDITION,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=45,
  serialized_end=886,
)


_RESULT_VALIDATIONREPLY = descriptor.Descriptor(
  name='ValidationReply',
  full_name='PaceValidation.Result.ValidationReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='validationno', full_name='PaceValidation.Result.ValidationReply.validationno', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='errormessage', full_name='PaceValidation.Result.ValidationReply.errormessage', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='validationaccepted', full_name='PaceValidation.Result.ValidationReply.validationaccepted', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1010,
  serialized_end=1099,
)

_RESULT = descriptor.Descriptor(
  name='Result',
  full_name='PaceValidation.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='requestid', full_name='PaceValidation.Result.requestid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='requestaccepted', full_name='PaceValidation.Result.requestaccepted', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='validationreplies', full_name='PaceValidation.Result.validationreplies', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESULT_VALIDATIONREPLY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=889,
  serialized_end=1099,
)


_RESULTKEY = descriptor.Descriptor(
  name='ResultKey',
  full_name='PaceValidation.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='PaceValidation.ResultKey.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1101,
  serialized_end=1125,
)

_DEFINITION_VALIDATION_EXTENDEDDATA.containing_type = _DEFINITION_VALIDATION;
_DEFINITION_VALIDATION.fields_by_name['buyorsell'].enum_type = _DEFINITION_BUYORSELL
_DEFINITION_VALIDATION.fields_by_name['pricecondition'].enum_type = _DEFINITION_PRICECONDITION
_DEFINITION_VALIDATION.fields_by_name['extendeddata'].message_type = _DEFINITION_VALIDATION_EXTENDEDDATA
_DEFINITION_VALIDATION.fields_by_name['operation'].enum_type = _DEFINITION_OPERATION
_DEFINITION_VALIDATION.containing_type = _DEFINITION;
_DEFINITION.fields_by_name['operation'].enum_type = _DEFINITION_OPERATION
_DEFINITION.fields_by_name['validation'].message_type = _DEFINITION_VALIDATION
_DEFINITION_OPERATION.containing_type = _DEFINITION;
_DEFINITION_BUYORSELL.containing_type = _DEFINITION;
_DEFINITION_PRICECONDITION.containing_type = _DEFINITION;
_RESULT_VALIDATIONREPLY.containing_type = _RESULT;
_RESULT.fields_by_name['validationreplies'].message_type = _RESULT_VALIDATIONREPLY
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY

class Definition(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Validation(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    
    class ExtendedData(message.Message):
      __metaclass__ = reflection.GeneratedProtocolMessageType
      DESCRIPTOR = _DEFINITION_VALIDATION_EXTENDEDDATA
      
      # @@protoc_insertion_point(class_scope:PaceValidation.Definition.Validation.ExtendedData)
    DESCRIPTOR = _DEFINITION_VALIDATION
    
    # @@protoc_insertion_point(class_scope:PaceValidation.Definition.Validation)
  DESCRIPTOR = _DEFINITION
  
  # @@protoc_insertion_point(class_scope:PaceValidation.Definition)

class Result(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class ValidationReply(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RESULT_VALIDATIONREPLY
    
    # @@protoc_insertion_point(class_scope:PaceValidation.Result.ValidationReply)
  DESCRIPTOR = _RESULT
  
  # @@protoc_insertion_point(class_scope:PaceValidation.Result)

class ResultKey(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULTKEY
  
  # @@protoc_insertion_point(class_scope:PaceValidation.ResultKey)

# @@protoc_insertion_point(module_scope)