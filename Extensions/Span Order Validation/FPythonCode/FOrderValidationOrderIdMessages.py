""" Compiled: 2015-09-23 14:33:50 """

# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='OrderIds.proto',
  package='FValidationOrderIds',
  serialized_pb='\n\x0eOrderIds.proto\x12\x13\x46ValidationOrderIds\"#\n\nDefinition\x12\x15\n\rportfolio_oid\x18\x01 \x01(\x03\"4\n\tResultKey\x12\x15\n\rportfolio_oid\x18\x01 \x01(\x03\x12\x10\n\x08order_id\x18\x02 \x01(\t\"g\n\x06Result\x12\x34\n\x07version\x18\x01 \x03(\x0b\x32#.FValidationOrderIds.Result.Version\x1a\'\n\x07Version\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x01\x42\x12\n\x0e\x63om.frontarenaH\x03')




_DEFINITION = descriptor.Descriptor(
  name='Definition',
  full_name='FValidationOrderIds.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='portfolio_oid', full_name='FValidationOrderIds.Definition.portfolio_oid', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=39,
  serialized_end=74,
)


_RESULTKEY = descriptor.Descriptor(
  name='ResultKey',
  full_name='FValidationOrderIds.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='portfolio_oid', full_name='FValidationOrderIds.ResultKey.portfolio_oid', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_id', full_name='FValidationOrderIds.ResultKey.order_id', index=1,
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
  serialized_start=76,
  serialized_end=128,
)


_RESULT_VERSION = descriptor.Descriptor(
  name='Version',
  full_name='FValidationOrderIds.Result.Version',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='FValidationOrderIds.Result.Version.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='quantity', full_name='FValidationOrderIds.Result.Version.quantity', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=194,
  serialized_end=233,
)

_RESULT = descriptor.Descriptor(
  name='Result',
  full_name='FValidationOrderIds.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='version', full_name='FValidationOrderIds.Result.version', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESULT_VERSION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=130,
  serialized_end=233,
)

_RESULT_VERSION.containing_type = _RESULT;
_RESULT.fields_by_name['version'].message_type = _RESULT_VERSION
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

class Definition(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DEFINITION
  
  # @@protoc_insertion_point(class_scope:FValidationOrderIds.Definition)

class ResultKey(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULTKEY
  
  # @@protoc_insertion_point(class_scope:FValidationOrderIds.ResultKey)

class Result(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Version(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RESULT_VERSION
    
    # @@protoc_insertion_point(class_scope:FValidationOrderIds.Result.Version)
  DESCRIPTOR = _RESULT
  
  # @@protoc_insertion_point(class_scope:FValidationOrderIds.Result)

# @@protoc_insertion_point(module_scope)
