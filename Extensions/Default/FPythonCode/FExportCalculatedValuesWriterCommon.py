
from collections import namedtuple

ScenarioInformation = namedtuple('ScenarioInformation',
                               ['storageName',
                                'dimensionCardinalities',
                                'dimensionNames'])

VectorInformation = namedtuple('VectorInformation',
                                ['dimensionNames'])


ColumnInformation = namedtuple('ColumnInformation',
                               ['name',  #unique identifier
                                'columnID',
                                'columnPartNames',
                                'isDynamic',
                                'scenarioInformation',
                                'vectorInformation'])


RootPositionInformation = namedtuple('RootPositionInformation',
                                     ['name',
                                      'acmDomainName'])


PositionInformation = namedtuple('PositionInformation',
                                 ['rootPositionInformationID',
                                  'parentInfoID',
                                  'name',
                                  'acmDomainName',
                                  'dimensionName'])

CalculationInformation = namedtuple('CalculationInformation',
                                    ['projectionCoordinates',
                                     'values'])
