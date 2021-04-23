""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FACABTradingCapacityMessages.py"
# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='FACABTradingCapacityMessages.proto',
  package='FACABTradingCapacity',
  serialized_pb='\n\"FACABTradingCapacityMessages.proto\x12\x14\x46\x41\x43\x41\x42TradingCapacity\"8\n\nDefinition\x12\x12\n\ncreateUser\x18\x01 \x01(\t\x12\x16\n\x0emarketserverid\x18\x02 \x01(\t\"\x1c\n\tResultKey\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\"\xa9\x01\n\x06Result\x12\x45\n\x0fvalidationState\x18\x01 \x01(\x0e\x32,.FACABTradingCapacity.Result.ValidationState\x12\x1a\n\x12timestampReference\x18\x02 \x01(\t\"<\n\x0fValidationState\x12\x07\n\x03RED\x10\x00\x12\n\n\x06YELLOW\x10\x01\x12\t\n\x05GREEN\x10\x02\x12\t\n\x05WHITE\x10\x03\x42\x12\n\x0e\x63om.frontarenaH\x03')



_RESULT_VALIDATIONSTATE = descriptor.EnumDescriptor(
  name='ValidationState',
  full_name='FACABTradingCapacity.Result.ValidationState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='RED', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='YELLOW', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='GREEN', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='WHITE', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=258,
  serialized_end=318,
)


_DEFINITION = descriptor.Descriptor(
  name='Definition',
  full_name='FACABTradingCapacity.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='createUser', full_name='FACABTradingCapacity.Definition.createUser', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='marketserverid', full_name='FACABTradingCapacity.Definition.marketserverid', index=1,
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
  serialized_start=60,
  serialized_end=116,
)


_RESULTKEY = descriptor.Descriptor(
  name='ResultKey',
  full_name='FACABTradingCapacity.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='account', full_name='FACABTradingCapacity.ResultKey.account', index=0,
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
  serialized_start=118,
  serialized_end=146,
)


_RESULT = descriptor.Descriptor(
  name='Result',
  full_name='FACABTradingCapacity.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='validationState', full_name='FACABTradingCapacity.Result.validationState', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestampReference', full_name='FACABTradingCapacity.Result.timestampReference', index=1,
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
    _RESULT_VALIDATIONSTATE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=149,
  serialized_end=318,
)

_RESULT.fields_by_name['validationState'].enum_type = _RESULT_VALIDATIONSTATE
_RESULT_VALIDATIONSTATE.containing_type = _RESULT;
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

class Definition(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DEFINITION
  
  # @@protoc_insertion_point(class_scope:FACABTradingCapacity.Definition)

class ResultKey(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULTKEY
  
  # @@protoc_insertion_point(class_scope:FACABTradingCapacity.ResultKey)

class Result(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULT
  
  # @@protoc_insertion_point(class_scope:FACABTradingCapacity.Result)

# @@protoc_insertion_point(module_scope)