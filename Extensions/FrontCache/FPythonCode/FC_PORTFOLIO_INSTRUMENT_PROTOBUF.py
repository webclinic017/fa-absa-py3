# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='PortfolioInstrumentDefinition.proto',
  package='FrontCache.Contracts.Capital.Contracts.Sensitivity',
  serialized_pb='\n#PortfolioInstrumentDefinition.proto\x12\x32\x46rontCache.Contracts.Capital.Contracts.Sensitivity\"+\n\tBenchmark\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\x10\n\x05Value\x18\x02 \x01(\x01:\x01\x30\"\x8f\x01\n\x17PortfolioInstrumentData\x12t\n\x1bPortfolioInstrumentWorkbook\x18\x01 \x01(\x0b\x32O.FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook\"\xcd\x02\n\x1bPortfolioInstrumentWorkbook\x12\x15\n\rPortfolioName\x18\x01 \x01(\t\x12\x1a\n\x0fPortfolioNumber\x18\x02 \x01(\x05:\x01\x30\x12\x16\n\x0eInstrumentName\x18\x03 \x01(\t\x12\x1b\n\x10InstrumentNumber\x18\x04 \x01(\x05:\x01\x30\x12j\n\x16VerticalPortfolioSheet\x18\x05 \x01(\x0b\x32J.FrontCache.Contracts.Capital.Contracts.Sensitivity.VerticalPortfolioSheet\x12Z\n\x0ePortfolioSheet\x18\x06 \x01(\x0b\x32\x42.FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioSheet\"h\n\x0ePortfolioSheet\x12V\n\rSensitivities\x18\x01 \x03(\x0b\x32?.FrontCache.Contracts.Capital.Contracts.Sensitivity.Sensitivity\"-\n\x0bSensitivity\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\x10\n\x05Value\x18\x02 \x01(\x01:\x01\x30\"z\n\x16VerticalPortfolioSheet\x12`\n\x12YieldSensitivities\x18\x01 \x03(\x0b\x32\x44.FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldSensitivity\"m\n\nYieldCurve\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12Q\n\nBenchmarks\x18\x02 \x03(\x0b\x32=.FrontCache.Contracts.Capital.Contracts.Sensitivity.Benchmark\"u\n\x10YieldSensitivity\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12S\n\x0bYieldCurves\x18\x02 \x03(\x0b\x32>.FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldCurve')




_BENCHMARK = descriptor.Descriptor(
  name='Benchmark',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Benchmark',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='Name', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Benchmark.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='Value', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Benchmark.Value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=0,
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
  serialized_start=91,
  serialized_end=134,
)


_PORTFOLIOINSTRUMENTDATA = descriptor.Descriptor(
  name='PortfolioInstrumentData',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='PortfolioInstrumentWorkbook', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentData.PortfolioInstrumentWorkbook', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=137,
  serialized_end=280,
)


_PORTFOLIOINSTRUMENTWORKBOOK = descriptor.Descriptor(
  name='PortfolioInstrumentWorkbook',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='PortfolioName', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.PortfolioName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='PortfolioNumber', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.PortfolioNumber', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='InstrumentName', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.InstrumentName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='InstrumentNumber', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.InstrumentNumber', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='VerticalPortfolioSheet', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.VerticalPortfolioSheet', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='PortfolioSheet', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook.PortfolioSheet', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=283,
  serialized_end=616,
)


_PORTFOLIOSHEET = descriptor.Descriptor(
  name='PortfolioSheet',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioSheet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='Sensitivities', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioSheet.Sensitivities', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=618,
  serialized_end=722,
)


_SENSITIVITY = descriptor.Descriptor(
  name='Sensitivity',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Sensitivity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='Name', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Sensitivity.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='Value', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.Sensitivity.Value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=0,
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
  serialized_start=724,
  serialized_end=769,
)


_VERTICALPORTFOLIOSHEET = descriptor.Descriptor(
  name='VerticalPortfolioSheet',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.VerticalPortfolioSheet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='YieldSensitivities', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.VerticalPortfolioSheet.YieldSensitivities', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=771,
  serialized_end=893,
)


_YIELDCURVE = descriptor.Descriptor(
  name='YieldCurve',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldCurve',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='Name', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldCurve.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='Benchmarks', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldCurve.Benchmarks', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=895,
  serialized_end=1004,
)


_YIELDSENSITIVITY = descriptor.Descriptor(
  name='YieldSensitivity',
  full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldSensitivity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='Name', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldSensitivity.Name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=str("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='YieldCurves', full_name='FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldSensitivity.YieldCurves', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=1006,
  serialized_end=1123,
)

_PORTFOLIOINSTRUMENTDATA.fields_by_name['PortfolioInstrumentWorkbook'].message_type = _PORTFOLIOINSTRUMENTWORKBOOK
_PORTFOLIOINSTRUMENTWORKBOOK.fields_by_name['VerticalPortfolioSheet'].message_type = _VERTICALPORTFOLIOSHEET
_PORTFOLIOINSTRUMENTWORKBOOK.fields_by_name['PortfolioSheet'].message_type = _PORTFOLIOSHEET
_PORTFOLIOSHEET.fields_by_name['Sensitivities'].message_type = _SENSITIVITY
_VERTICALPORTFOLIOSHEET.fields_by_name['YieldSensitivities'].message_type = _YIELDSENSITIVITY
_YIELDCURVE.fields_by_name['Benchmarks'].message_type = _BENCHMARK
_YIELDSENSITIVITY.fields_by_name['YieldCurves'].message_type = _YIELDCURVE
DESCRIPTOR.message_types_by_name['Benchmark'] = _BENCHMARK
DESCRIPTOR.message_types_by_name['PortfolioInstrumentData'] = _PORTFOLIOINSTRUMENTDATA
DESCRIPTOR.message_types_by_name['PortfolioInstrumentWorkbook'] = _PORTFOLIOINSTRUMENTWORKBOOK
DESCRIPTOR.message_types_by_name['PortfolioSheet'] = _PORTFOLIOSHEET
DESCRIPTOR.message_types_by_name['Sensitivity'] = _SENSITIVITY
DESCRIPTOR.message_types_by_name['VerticalPortfolioSheet'] = _VERTICALPORTFOLIOSHEET
DESCRIPTOR.message_types_by_name['YieldCurve'] = _YIELDCURVE
DESCRIPTOR.message_types_by_name['YieldSensitivity'] = _YIELDSENSITIVITY

class Benchmark(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BENCHMARK
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.Benchmark)

class PortfolioInstrumentData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PORTFOLIOINSTRUMENTDATA
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentData)

class PortfolioInstrumentWorkbook(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PORTFOLIOINSTRUMENTWORKBOOK
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioInstrumentWorkbook)

class PortfolioSheet(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PORTFOLIOSHEET
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.PortfolioSheet)

class Sensitivity(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SENSITIVITY
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.Sensitivity)

class VerticalPortfolioSheet(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VERTICALPORTFOLIOSHEET
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.VerticalPortfolioSheet)

class YieldCurve(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _YIELDCURVE
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldCurve)

class YieldSensitivity(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _YIELDSENSITIVITY
  
  # @@protoc_insertion_point(class_scope:FrontCache.Contracts.Capital.Contracts.Sensitivity.YieldSensitivity)

# @@protoc_insertion_point(module_scope)