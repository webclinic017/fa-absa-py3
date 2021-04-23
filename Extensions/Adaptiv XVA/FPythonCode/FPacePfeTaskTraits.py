""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/FPacePfeTaskTraits.py"
from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='CvaTaskv2.proto',
  package='',
  serialized_pb='\n\x0f\x43vaTaskv2.proto\"*\n\nDefinition\x12\x0e\n\x06trdnbr\x18\x01 \x02(\x05\x12\x0c\n\x04guid\x18\x02 \x02(\t\"\x1d\n\tResultKey\x12\x10\n\x08updateId\x18\x01 \x02(\x05\">\n\x06Result\x12\x0f\n\x07success\x18\x01 \x02(\x08\x12\x0e\n\x06\x61mount\x18\x02 \x02(\x02\x12\x13\n\x0b\x63urrencyOid\x18\x03 \x02(\x05\x42\x02H\x03')




_DEFINITION = descriptor.Descriptor(
  name='Definition',
  full_name='Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='trdnbr', full_name='Definition.trdnbr', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='guid', full_name='Definition.guid', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=19,
  serialized_end=61,
)


_RESULTKEY = descriptor.Descriptor(
  name='ResultKey',
  full_name='ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='updateId', full_name='ResultKey.updateId', index=0,
      number=1, type=5, cpp_type=1, label=2,
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
  serialized_start=63,
  serialized_end=92,
)


_RESULT = descriptor.Descriptor(
  name='Result',
  full_name='Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='success', full_name='Result.success', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='IncPFE', full_name='Result.IncPFE', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='PFE', full_name='Result.PFE', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='AfterPFE', full_name='Result.AfterPFE', index=2,
      number=4, type=9, cpp_type=9, label=2,
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
  serialized_start=94,
  serialized_end=156,
)

DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

class Definition(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DEFINITION
  
  # @@protoc_insertion_point(class_scope:Definition)

class ResultKey(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULTKEY
  
  # @@protoc_insertion_point(class_scope:ResultKey)

class Result(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESULT
  
  # @@protoc_insertion_point(class_scope:Result)

# @@protoc_insertion_point(module_scope)
