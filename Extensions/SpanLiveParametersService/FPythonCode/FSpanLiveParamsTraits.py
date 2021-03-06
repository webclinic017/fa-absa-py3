"""
option optimize_for = LITE_RUNTIME;

package FLiveSpanParameters;

message Definition
{
    optional int64 query_oid = 1;
}

message ResultKey
{
     optional int64 ins_oid = 1;
}

message Result
{
    repeated double riskarray = 1;
    optional string timestamp = 2;
    optional double delta = 3;
}
"""
# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='FSpanLiveParameters.proto',
  package='FLiveSpanParameters',
  serialized_pb='\n\x19\x46SpanLiveParameters.proto\x12\x13\x46LiveSpanParameters\"\x1f\n\nDefinition\x12\x11\n\tquery_oid\x18\x01 \x01(\x03\"\x1c\n\tResultKey\x12\x0f\n\x07ins_oid\x18\x01 \x01(\x03\"=\n\x06Result\x12\x11\n\triskarray\x18\x01 \x03(\x01\x12\x11\n\ttimestamp\x18\x02 \x01(\t\x12\r\n\x05\x64\x65lta\x18\x03 \x01(\x01\x42\x02H\x03')




_DEFINITION = descriptor.Descriptor(
  name='Definition',
  full_name='FLiveSpanParameters.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='query_oid', full_name='FLiveSpanParameters.Definition.query_oid', index=0,
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
  serialized_start=50,
  serialized_end=81,
)


_RESULTKEY = descriptor.Descriptor(
  name='ResultKey',
  full_name='FLiveSpanParameters.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ins_oid', full_name='FLiveSpanParameters.ResultKey.ins_oid', index=0,
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
  serialized_start=83,
  serialized_end=111,
)


_RESULT = descriptor.Descriptor(
  name='Result',
  full_name='FLiveSpanParameters.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='riskarray', full_name='FLiveSpanParameters.Result.riskarray', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='FLiveSpanParameters.Result.timestamp', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='delta', full_name='FLiveSpanParameters.Result.delta', index=2,
      number=3, type=1, cpp_type=5, label=1,
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
  serialized_start=113,
  serialized_end=174,
)

DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

class Definition(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DEFINITION
  
  # @@protoc_insertion_point(class_scope:FLiveSpanParameters.Definition)

class ResultKey(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULTKEY
  
  # @@protoc_insertion_point(class_scope:FLiveSpanParameters.ResultKey)

class Result(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULT
  
  # @@protoc_insertion_point(class_scope:FLiveSpanParameters.Result)

# @@protoc_insertion_point(module_scope)
