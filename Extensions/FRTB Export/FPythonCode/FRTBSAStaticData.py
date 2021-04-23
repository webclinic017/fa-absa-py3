""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBSAStaticData.py"
from collections import namedtuple

FRTBTags = namedtuple('FRTBTags', [     'Commodity',
                                        'Economy',
                                        'ElectricityArea',
                                        'ElectricityTime',
                                        'FreightRoute',
                                        'FreightWeek',
                                        'MarketCap',
                                    ])

bucket_map = {
                '1': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '2': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '3': FRTBTags('Energy - Electricity and carbon trading', '', 'None', 'None', 'None', 'None', 'Large'),
                '4': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '5': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '6': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '7': FRTBTags('Precious Metals', '', 'None', 'None', 'None', 'None', 'Large'),
                '8': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '9': FRTBTags('', 'Emerging', '', '', '', '', 'Small'),
                '10': FRTBTags('', 'Emerging', '', '', '', '', 'Small'),
                '11': FRTBTags('', 'None', '', '', '', '', 'Small'),
                '12': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '13': FRTBTags('', 'Emerging', '', '', '', '', 'Large'),
                '14': FRTBTags('', 'Emerging', '', '', '', '', ''),
                '15': FRTBTags('', 'Emerging', '', '', '', '', ''),
                '16': FRTBTags('', 'Emerging', '', '', '', '', ''),
                '25': FRTBTags('', 'Emerging', '', '', '', '', ''),
                }

DefaultTranslator = 'Default'

HeaderTranslators = {
    DefaultTranslator : {'Instrument' : 'Reference', 'Currency' : 'FRTB Currencies'}
    }
