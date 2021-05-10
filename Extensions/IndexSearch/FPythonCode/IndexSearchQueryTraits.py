
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Contracts/IndexSearch/Messages/IndexSearchQuery.proto

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
  name='Contracts/IndexSearch/Messages/IndexSearchQuery.proto',
  package='IndexSearch.Query.Msg',
  serialized_pb=_b('\n5Contracts/IndexSearch/Messages/IndexSearchQuery.proto\x12\x15IndexSearch.Query.Msg\x1a&Contracts/Tk/Messages/TkMessages.proto\"I\n\nDefinition\x12\r\n\x05query\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x03\x12\x10\n\x08pageSize\x18\x03 \x01(\x03\x12\x0c\n\x04uuid\x18\x04 \x01(\t\"\x17\n\tResultKey\x12\n\n\x02id\x18\x01 \x01(\x03\"&\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\xa1\x01\n\x11ResultDescription\x12 \n\x07moniker\x18\x01 \x01(\x0b\x32\x0f.Tk.Msg.Moniker\x12\x32\n\tkeyValues\x18\x02 \x03(\x0b\x32\x1f.IndexSearch.Query.Msg.KeyValue\x12\x36\n\x12\x64isplayInformation\x18\x03 \x01(\x0b\x32\x1a.Tk.Msg.DisplayInformation\"\xd3\x01\n\x06Result\x12?\n\rsearchResults\x18\x01 \x03(\x0b\x32(.IndexSearch.Query.Msg.ResultDescription\x12\x12\n\nfoundCount\x18\x02 \x01(\x03\x12\x0c\n\x04page\x18\x03 \x01(\x03\x12\x11\n\tpageCount\x18\x04 \x01(\x03\x12\x12\n\npageLength\x18\x05 \x01(\x03\x12\x0e\n\x06offset\x18\x06 \x01(\x03\x12\r\n\x05total\x18\x07 \x01(\x03\x12\x0c\n\x04type\x18\x08 \x01(\t\x12\x12\n\nsuggestion\x18\t \x01(\tB)\n com.frontarena.indexsearch.queryB\x03MsgH\x03')
  ,
  dependencies=[Contracts_Tk_Messages_TkMessages.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DEFINITION = _descriptor.Descriptor(
  name='Definition',
  full_name='IndexSearch.Query.Msg.Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='IndexSearch.Query.Msg.Definition.query', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='page', full_name='IndexSearch.Query.Msg.Definition.page', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pageSize', full_name='IndexSearch.Query.Msg.Definition.pageSize', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='IndexSearch.Query.Msg.Definition.uuid', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=120,
  serialized_end=193,
)


_RESULTKEY = _descriptor.Descriptor(
  name='ResultKey',
  full_name='IndexSearch.Query.Msg.ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='IndexSearch.Query.Msg.ResultKey.id', index=0,
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
  serialized_start=195,
  serialized_end=218,
)


_KEYVALUE = _descriptor.Descriptor(
  name='KeyValue',
  full_name='IndexSearch.Query.Msg.KeyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='IndexSearch.Query.Msg.KeyValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='IndexSearch.Query.Msg.KeyValue.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=220,
  serialized_end=258,
)


_RESULTDESCRIPTION = _descriptor.Descriptor(
  name='ResultDescription',
  full_name='IndexSearch.Query.Msg.ResultDescription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='moniker', full_name='IndexSearch.Query.Msg.ResultDescription.moniker', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='keyValues', full_name='IndexSearch.Query.Msg.ResultDescription.keyValues', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='displayInformation', full_name='IndexSearch.Query.Msg.ResultDescription.displayInformation', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=261,
  serialized_end=422,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='IndexSearch.Query.Msg.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='searchResults', full_name='IndexSearch.Query.Msg.Result.searchResults', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='foundCount', full_name='IndexSearch.Query.Msg.Result.foundCount', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='page', full_name='IndexSearch.Query.Msg.Result.page', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pageCount', full_name='IndexSearch.Query.Msg.Result.pageCount', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pageLength', full_name='IndexSearch.Query.Msg.Result.pageLength', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='offset', full_name='IndexSearch.Query.Msg.Result.offset', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total', full_name='IndexSearch.Query.Msg.Result.total', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='IndexSearch.Query.Msg.Result.type', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='suggestion', full_name='IndexSearch.Query.Msg.Result.suggestion', index=8,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_start=425,
  serialized_end=636,
)

_RESULTDESCRIPTION.fields_by_name['moniker'].message_type = Contracts_Tk_Messages_TkMessages._MONIKER
_RESULTDESCRIPTION.fields_by_name['keyValues'].message_type = _KEYVALUE
_RESULTDESCRIPTION.fields_by_name['displayInformation'].message_type = Contracts_Tk_Messages_TkMessages._DISPLAYINFORMATION
_RESULT.fields_by_name['searchResults'].message_type = _RESULTDESCRIPTION
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['KeyValue'] = _KEYVALUE
DESCRIPTOR.message_types_by_name['ResultDescription'] = _RESULTDESCRIPTION
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Definition = _reflection.GeneratedProtocolMessageType('Definition', (_message.Message,), dict(
  DESCRIPTOR = _DEFINITION,
  __module__ = 'Contracts.IndexSearch.Messages.IndexSearchQuery_pb2'
  # @@protoc_insertion_point(class_scope:IndexSearch.Query.Msg.Definition)
  ))
_sym_db.RegisterMessage(Definition)

ResultKey = _reflection.GeneratedProtocolMessageType('ResultKey', (_message.Message,), dict(
  DESCRIPTOR = _RESULTKEY,
  __module__ = 'Contracts.IndexSearch.Messages.IndexSearchQuery_pb2'
  # @@protoc_insertion_point(class_scope:IndexSearch.Query.Msg.ResultKey)
  ))
_sym_db.RegisterMessage(ResultKey)

KeyValue = _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), dict(
  DESCRIPTOR = _KEYVALUE,
  __module__ = 'Contracts.IndexSearch.Messages.IndexSearchQuery_pb2'
  # @@protoc_insertion_point(class_scope:IndexSearch.Query.Msg.KeyValue)
  ))
_sym_db.RegisterMessage(KeyValue)

ResultDescription = _reflection.GeneratedProtocolMessageType('ResultDescription', (_message.Message,), dict(
  DESCRIPTOR = _RESULTDESCRIPTION,
  __module__ = 'Contracts.IndexSearch.Messages.IndexSearchQuery_pb2'
  # @@protoc_insertion_point(class_scope:IndexSearch.Query.Msg.ResultDescription)
  ))
_sym_db.RegisterMessage(ResultDescription)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'Contracts.IndexSearch.Messages.IndexSearchQuery_pb2'
  # @@protoc_insertion_point(class_scope:IndexSearch.Query.Msg.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n com.frontarena.indexsearch.queryB\003MsgH\003'))
# @@protoc_insertion_point(module_scope)