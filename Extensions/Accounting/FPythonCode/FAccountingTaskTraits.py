""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskTraits.py"
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AccountingTaskMessages.proto

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
  name='AccountingTaskMessages.proto',
  package='',
  serialized_pb=_b('\n\x1c\x41\x63\x63ountingTaskMessages.proto\"\xaf\x02\n\nDefinition\x12,\n\x0btargetClass\x18\x01 \x01(\x0e\x32\x17.Definition.TargetClass\x12\x12\n\x06objIds\x18\x02 \x03(\x03\x42\x02\x10\x01\x12\x11\n\tstartDate\x18\x03 \x01(\t\x12\x0f\n\x07\x65ndDate\x18\x04 \x01(\t\x12\x14\n\x0c\x65ndOfDayDate\x18\x05 \x01(\t\x12\x13\n\x0bprocessDate\x18\x06 \x01(\t\x12\x13\n\x07\x62ookIds\x18\x07 \x03(\x03\x42\x02\x10\x01\x12\x18\n\x0ctreatmentIds\x18\x08 \x03(\x03\x42\x02\x10\x01\x12\x11\n\x05\x61iIds\x18\t \x03(\x03\x42\x02\x10\x01\x12\x10\n\x08testMode\x18\n \x01(\x08\x12\x0c\n\x04guid\x18\x0b \x01(\t\".\n\x0bTargetClass\x12\x0c\n\x08TC_TRADE\x10\x00\x12\x11\n\rTC_SETTLEMENT\x10\x01\"_\n\tResultKey\x12)\n\nresultType\x18\x01 \x01(\x0e\x32\x15.ResultKey.ResultType\"\'\n\nResultType\x12\n\n\x06RT_LOG\x10\x00\x12\r\n\tRT_RESULT\x10\x01\"\xb1\x01\n\x06Result\x12\x18\n\x03log\x18\x01 \x01(\x0b\x32\x0b.Result.Log\x12\x1e\n\x06result\x18\x02 \x01(\x0b\x32\x0e.Result.Result\x1a\x19\n\x03Log\x12\x12\n\nlogMessage\x18\x01 \x01(\t\x1aR\n\x06Result\x12\x0f\n\x07\x63reated\x18\x01 \x01(\x03\x12\x0f\n\x07updated\x18\x02 \x01(\x03\x12\x12\n\nexceptions\x18\x03 \x01(\x03\x12\x12\n\x06objIds\x18\x04 \x03(\x03\x42\x02\x10\x01\x42\x02H\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_DEFINITION_TARGETCLASS = _descriptor.EnumDescriptor(
  name='TargetClass',
  full_name='Definition.TargetClass',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TC_TRADE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TC_SETTLEMENT', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=290,
  serialized_end=336,
)
_sym_db.RegisterEnumDescriptor(_DEFINITION_TARGETCLASS)

_RESULTKEY_RESULTTYPE = _descriptor.EnumDescriptor(
  name='ResultType',
  full_name='ResultKey.ResultType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RT_LOG', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RT_RESULT', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=394,
  serialized_end=433,
)
_sym_db.RegisterEnumDescriptor(_RESULTKEY_RESULTTYPE)


_DEFINITION = _descriptor.Descriptor(
  name='Definition',
  full_name='Definition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='targetClass', full_name='Definition.targetClass', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objIds', full_name='Definition.objIds', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='startDate', full_name='Definition.startDate', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endDate', full_name='Definition.endDate', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endOfDayDate', full_name='Definition.endOfDayDate', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='processDate', full_name='Definition.processDate', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bookIds', full_name='Definition.bookIds', index=6,
      number=7, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='treatmentIds', full_name='Definition.treatmentIds', index=7,
      number=8, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='aiIds', full_name='Definition.aiIds', index=8,
      number=9, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='testMode', full_name='Definition.testMode', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='guid', full_name='Definition.guid', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEFINITION_TARGETCLASS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=33,
  serialized_end=336,
)


_RESULTKEY = _descriptor.Descriptor(
  name='ResultKey',
  full_name='ResultKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultType', full_name='ResultKey.resultType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RESULTKEY_RESULTTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=338,
  serialized_end=433,
)


_RESULT_LOG = _descriptor.Descriptor(
  name='Log',
  full_name='Result.Log',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='logMessage', full_name='Result.Log.logMessage', index=0,
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
  serialized_start=504,
  serialized_end=529,
)

_RESULT_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Result.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='created', full_name='Result.Result.created', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updated', full_name='Result.Result.updated', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exceptions', full_name='Result.Result.exceptions', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objIds', full_name='Result.Result.objIds', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
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
  serialized_start=531,
  serialized_end=613,
)

_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='log', full_name='Result.log', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='result', full_name='Result.result', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESULT_LOG, _RESULT_RESULT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=436,
  serialized_end=613,
)

_DEFINITION.fields_by_name['targetClass'].enum_type = _DEFINITION_TARGETCLASS
_DEFINITION_TARGETCLASS.containing_type = _DEFINITION
_RESULTKEY.fields_by_name['resultType'].enum_type = _RESULTKEY_RESULTTYPE
_RESULTKEY_RESULTTYPE.containing_type = _RESULTKEY
_RESULT_LOG.containing_type = _RESULT
_RESULT_RESULT.containing_type = _RESULT
_RESULT.fields_by_name['log'].message_type = _RESULT_LOG
_RESULT.fields_by_name['result'].message_type = _RESULT_RESULT
DESCRIPTOR.message_types_by_name['Definition'] = _DEFINITION
DESCRIPTOR.message_types_by_name['ResultKey'] = _RESULTKEY
DESCRIPTOR.message_types_by_name['Result'] = _RESULT

Definition = _reflection.GeneratedProtocolMessageType('Definition', (_message.Message,), dict(
  DESCRIPTOR = _DEFINITION,
  __module__ = 'AccountingTaskMessages_pb2'
  # @@protoc_insertion_point(class_scope:Definition)
  ))
_sym_db.RegisterMessage(Definition)

ResultKey = _reflection.GeneratedProtocolMessageType('ResultKey', (_message.Message,), dict(
  DESCRIPTOR = _RESULTKEY,
  __module__ = 'AccountingTaskMessages_pb2'
  # @@protoc_insertion_point(class_scope:ResultKey)
  ))
_sym_db.RegisterMessage(ResultKey)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(

  Log = _reflection.GeneratedProtocolMessageType('Log', (_message.Message,), dict(
    DESCRIPTOR = _RESULT_LOG,
    __module__ = 'AccountingTaskMessages_pb2'
    # @@protoc_insertion_point(class_scope:Result.Log)
    ))
  ,

  Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
    DESCRIPTOR = _RESULT_RESULT,
    __module__ = 'AccountingTaskMessages_pb2'
    # @@protoc_insertion_point(class_scope:Result.Result)
    ))
  ,
  DESCRIPTOR = _RESULT,
  __module__ = 'AccountingTaskMessages_pb2'
  # @@protoc_insertion_point(class_scope:Result)
  ))
_sym_db.RegisterMessage(Result)
_sym_db.RegisterMessage(Result.Log)
_sym_db.RegisterMessage(Result.Result)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
_DEFINITION.fields_by_name['objIds'].has_options = True
_DEFINITION.fields_by_name['objIds']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_DEFINITION.fields_by_name['bookIds'].has_options = True
_DEFINITION.fields_by_name['bookIds']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_DEFINITION.fields_by_name['treatmentIds'].has_options = True
_DEFINITION.fields_by_name['treatmentIds']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_DEFINITION.fields_by_name['aiIds'].has_options = True
_DEFINITION.fields_by_name['aiIds']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_RESULT_RESULT.fields_by_name['objIds'].has_options = True
_RESULT_RESULT.fields_by_name['objIds']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
