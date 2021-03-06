""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/../../Pace/Messages/Contracts/SingleValue/Messages/Contracts_SingleValue_Messages_SingleValueMessages.py"
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Contracts/SingleValue/Messages/SingleValueMessages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Contracts_Tk_Messages_TkMessages


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Contracts/SingleValue/Messages/SingleValueMessages.proto',
  package='SingleValue.Msg',
  serialized_pb=_b('\n8Contracts/SingleValue/Messages/SingleValueMessages.proto\x12\x0fSingleValue.Msg\x1a&Contracts/Tk/Messages/TkMessages.proto\"F\n\nDefinition\x12\x12\n\nmoduleName\x18\x02 \x01(\t\x12\x11\n\tclassName\x18\x03 \x01(\t\x12\x11\n\targuments\x18\x04 \x03(\t\"\x17\n\tResultKey\x12\n\n\x02id\x18\x01 \x01(\x03\"(\n\x06Result\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.Tk.Msg.VariantB#\n\x1a\x63om.frontarena.singlevalueB\x03MsgH\x03')
  ,
  dependencies=[Contracts_Tk_Messages_TkMessages.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DEFINITION = _descriptor.Descriptor(
  name='Definition',
  full_name='SingleValue.Msg.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='moduleName', full_name='SingleValue.Msg.Definition.moduleName', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='className', full_name='SingleValue.Msg.Definition.className', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='SingleValue.Msg.Definition.arguments', index=2,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=187,
)


_RESULTKEY = _descriptor.Descriptor(
  name='ResultKey',
  full_name='SingleValue.Msg.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='SingleValue.Msg.ResultKey.id', index=0,
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
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=212,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='SingleValue.Msg.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='SingleValue.Msg.Result.value', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=254,
)

_RESULT.fields_by_name['value'].message_type = Contracts_Tk_Messages_TkMessages._VARIANT
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Definition = _reflection.GeneratedProtocolMessageType('Definition', (_message.Message,), dict(
  DESCRIPTOR = _DEFINITION,
  __module__ = 'Contracts.SingleValue.Messages.SingleValueMessages_pb2'
  # @@protoc_insertion_point(class_scope:SingleValue.Msg.Definition)
  ))
_sym_db.RegisterMessage(Definition)

ResultKey = _reflection.GeneratedProtocolMessageType('ResultKey', (_message.Message,), dict(
  DESCRIPTOR = _RESULTKEY,
  __module__ = 'Contracts.SingleValue.Messages.SingleValueMessages_pb2'
  # @@protoc_insertion_point(class_scope:SingleValue.Msg.ResultKey)
  ))
_sym_db.RegisterMessage(ResultKey)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'Contracts.SingleValue.Messages.SingleValueMessages_pb2'
  # @@protoc_insertion_point(class_scope:SingleValue.Msg.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\032com.frontarena.singlevalueB\003MsgH\003'))
# @@protoc_insertion_point(module_scope)
