
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PositionEngineCreateValueSession.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='PositionEngineCreateValueSession.proto',
  package='PositionSheetEngine.CreateValueSession.Msg',
  serialized_pb=_b('\n&PositionEngineCreateValueSession.proto\x12*PositionSheetEngine.CreateValueSession.Msg\"+\n\x11SessionParameters\x12\x16\n\x0ehistoricalDate\x18\x01 \x01(\t\"\xa1\x02\n\nDefinition\x12 \n\x18\x64\x61taDispositionStorageId\x18\x01 \x01(\x03\x12\x13\n\x0bsessionType\x18\x02 \x01(\t\x12\x10\n\x08uniqueId\x18\x03 \x01(\t\x12\x12\n\nchannelKey\x18\x04 \x01(\t\x12\x1d\n\x15\x61mendSessionStorageId\x18\x05 \x01(\x03\x12\x13\n\x0b\x63reateAudit\x18\x07 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\x12\x1a\n\x12positionFilterName\x18\t \x01(\t\x12Q\n\nparameters\x18\x0b \x03(\x0b\x32=.PositionSheetEngine.CreateValueSession.Msg.SessionParameters\"\x95\x01\n\x06Result\x12\x18\n\x10sessionStorageId\x18\x01 \x01(\x03\x12\x18\n\x10\x61mendedSessionId\x18\x02 \x01(\x03\x12\x16\n\x0e\x63reatedRecords\x18\x03 \x01(\x03\x12\x14\n\x0cmovedRecords\x18\x04 \x01(\x03\x12\x11\n\terrorText\x18\x05 \x01(\t\x12\x16\n\x0ehistoricalDate\x18\x06 \x01(\t\"\x17\n\tResultKey\x12\n\n\x02id\x18\x01 \x01(\x05\x42\x02H\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SESSIONPARAMETERS = _descriptor.Descriptor(
  name='SessionParameters',
  full_name='PositionSheetEngine.CreateValueSession.Msg.SessionParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='historicalDate', full_name='PositionSheetEngine.CreateValueSession.Msg.SessionParameters.historicalDate', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=86,
  serialized_end=129,
)


_DEFINITION = _descriptor.Descriptor(
  name='Definition',
  full_name='PositionSheetEngine.CreateValueSession.Msg.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dataDispositionStorageId', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.dataDispositionStorageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sessionType', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.sessionType', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uniqueId', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.uniqueId', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channelKey', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.channelKey', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amendSessionStorageId', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.amendSessionStorageId', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createAudit', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.createAudit', index=5,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.description', index=6,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='positionFilterName', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.positionFilterName', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='PositionSheetEngine.CreateValueSession.Msg.Definition.parameters', index=8,
      number=11, type=11, cpp_type=10, label=3,
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
  serialized_start=132,
  serialized_end=421,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='PositionSheetEngine.CreateValueSession.Msg.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessionStorageId', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.sessionStorageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amendedSessionId', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.amendedSessionId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createdRecords', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.createdRecords', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='movedRecords', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.movedRecords', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errorText', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.errorText', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='historicalDate', full_name='PositionSheetEngine.CreateValueSession.Msg.Result.historicalDate', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=424,
  serialized_end=573,
)


_RESULTKEY = _descriptor.Descriptor(
  name='ResultKey',
  full_name='PositionSheetEngine.CreateValueSession.Msg.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PositionSheetEngine.CreateValueSession.Msg.ResultKey.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
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
  serialized_start=575,
  serialized_end=598,
)

_DEFINITION.fields_by_name['parameters'].message_type = _SESSIONPARAMETERS
DESCRIPTOR.message_types_by_name['SessionParameters'] = _SESSIONPARAMETERS
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY

SessionParameters = _reflection.GeneratedProtocolMessageType('SessionParameters', (_message.Message,), dict(
  DESCRIPTOR = _SESSIONPARAMETERS,
  __module__ = 'PositionEngineCreateValueSession_pb2'
  # @@protoc_insertion_point(class_scope:PositionSheetEngine.CreateValueSession.Msg.SessionParameters)
  ))
_sym_db.RegisterMessage(SessionParameters)

Definition = _reflection.GeneratedProtocolMessageType('Definition', (_message.Message,), dict(
  DESCRIPTOR = _DEFINITION,
  __module__ = 'PositionEngineCreateValueSession_pb2'
  # @@protoc_insertion_point(class_scope:PositionSheetEngine.CreateValueSession.Msg.Definition)
  ))
_sym_db.RegisterMessage(Definition)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'PositionEngineCreateValueSession_pb2'
  # @@protoc_insertion_point(class_scope:PositionSheetEngine.CreateValueSession.Msg.Result)
  ))
_sym_db.RegisterMessage(Result)

ResultKey = _reflection.GeneratedProtocolMessageType('ResultKey', (_message.Message,), dict(
  DESCRIPTOR = _RESULTKEY,
  __module__ = 'PositionEngineCreateValueSession_pb2'
  # @@protoc_insertion_point(class_scope:PositionSheetEngine.CreateValueSession.Msg.ResultKey)
  ))
_sym_db.RegisterMessage(ResultKey)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
