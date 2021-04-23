import acm, ael

jurisdiction_codes = {'EU' : ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE',\
                       'DK', 'EE', 'EL', 'ES', 'FI', 'FR',\
                       'HR', 'HU', 'IE', 'IT', 'LI', 'LT',\
                       'LV', 'MT', 'NL', 'PL', 'PT', 'RO',\
                       'SE', 'SI', 'SK', 'UK'],
                      'EEA' : ['FL', 'NO', 'IS'],
                      'EFTA' : ['CH', 'FL', 'IS', 'NO'],
                      'Basel1988' : ['BE', 'CA', 'CH', 'DE', 'ES',\
                                     'FR', 'IT', 'JP', 'LU', 'NL',\
                                     'SE', 'UK', 'US']}

regulatory_authority = {'EU' : 'ESMA', 'US' : 'SEC',
                        'CN' : 'CSRC', 'AU' : 'ASIC',
                        'IN' : 'SEBI', 'NZ' : 'FMA',
                        'JP' : 'FSA'}

country_code_dict = {
    'Afghanistan': 'AF',
    'Islamic Republic of Afghanistan': 'AF',
    'Aland Islands': 'AX',
    'Albania': 'AL',
    'Algeria': 'DZ',
    'American Samoa': 'AS',
    'Andorra': 'AD',
    'Angola': 'AO',
    'Anguilla': 'AI',
    'Antarctica': 'AQ',
    'Antigua and Barbuda': 'AG',
    'Argentina': 'AR',
    'Armenia': 'AM',
    'Aruba': 'AW',
    'Australia': 'AU',
    'Austria': 'AT',
    'Azerbaijan': 'AZ',
    'Bahamas': 'BS',
    'Bahrain': 'BH',
    'Bangladesh': 'BD',
    'Barbados': 'BB',
    'Belarus': 'BY',
    'Belgium': 'BE',
    'Belgien': 'BE',
    'Belgique': 'BE',
    'BE': 'BE',
    'Belize': 'BZ',
    'Benin': 'BJ',
    'Bermuda': 'BM',
    'Bhutan': 'BT',
    'Bolivia': 'BO',
    'Bonaire, Sint Eustatius and Saba': 'BQ',
    'Bosnia and Herzegovina': 'BA',
    'Botswana': 'BW',
    'Bouvet Island': 'BV',
    'Brazil': 'BR',
    'British Indian Ocean Territory': 'IO',
    'Brunei Darussalam': 'BN',
    'Bulgaria': 'BG',
    'Burkina Faso': 'BF',
    'Burundi': 'BI',
    'Cabo Verde': 'CV',
    'Cambodia': 'KH',
    'Cameroon': 'CM',
    'Canada': 'CA',
    'Cayman Islands': 'KY',
    'Central African Republic': 'CF',
    'Chad': 'TD',
    'Chile': 'CL',
    'China': 'CN',
    'Christmas Island': 'CX',
    'Cocos Islands': 'CC',
    'Cocos (Keeling) Islands': 'CC',
    'Colombia': 'CO',
    'Comoros': 'KM',
    'Congo (the Democratic Republic of the)': 'CD',
    'Democratic Republic of Congo': 'CD',
    'DR Congo': 'CD',
    'DRC': 'CD',
    'Congo': 'CG',
    'Republic of the Congo': 'CG',
    'Cook Islands': 'CK',
    'Costa Rica': 'CR',
    "Cote d'Ivoire": 'CI',
    'Croatia': 'HR',
    'Cuba': 'CU',
    'Curacao': 'CW',
    'Cyprus': 'CY',
    'Czech Republic': 'CZ',
    'Denmark': 'DK',
    'Danmark': 'DK',
    'Danemark': 'DK',
    'DK': 'DK',
    'DEN': 'DK',
    'Djibouti': 'DJ',
    'Dominica': 'DM',
    'Dominican Republic': 'DO',
    'Ecuador': 'EC',
    'Egypt': 'EG',
    'El Salvador': 'SV',
    'Equatorial Guinea': 'GQ',
    'Eritrea': 'ER',
    'Estonia': 'EE',
    'Ethiopia': 'ET',
    'Falkland Islands': 'FK',
    'Malvinas': 'FK',
    'Faroe Islands': 'FO',
    'Fiji': 'FJ',
    'Finland': 'FI',
    'Suomi': 'FI',
    'SF': 'FI',
    'FIN': 'FI',
    'France': 'FR',
    'Frankreich': 'FR',
    'Frankrike': 'FR',
    'FR': 'FR',
    'French Guiana': 'GF',
    'French Polynesia': 'PF',
    'French Southern Territories': 'TF',
    'French Southern Lands ': 'TF',
    'French Southern and Antarctic Lands': 'TF',
    'Gabon': 'GA',
    'Gambia': 'GM',
    'Georgia': 'GE',
    'Germany': 'DE',
    'DE': 'DE',
    'Deutschland': 'DE',
    'Tyskland': 'DE',
    'Allemagne': 'DE',
    'Ghana': 'GH',
    'Gibraltar': 'GI',
    'Greece': 'GR',
    'Greenland': 'GL',
    'Grenada': 'GD',
    'Guadeloupe': 'GP',
    'Guam': 'GU',
    'Guatemala': 'GT',
    'Guernsey': 'GG',
    'Guinea': 'GN',
    'Guinea-Bissau': 'GW',
    'Guyana': 'GY',
    'Haiti': 'HT',
    'Heard Island and McDonald Islands': 'HM',
    'Holy See': 'VA',
    'Vatican City': 'VA',
    'Honduras': 'HN',
    'Hong Kong': 'HK',
    'Hungary': 'HU',
    'Iceland': 'IS',
    'India': 'IN',
    'Indonesia': 'ID',
    'Iran': 'IR',
    'Iraq': 'IQ',
    'Ireland': 'IE',
    'Isle of Man': 'IM',
    'Israel': 'IL',
    'Italy': 'IT',
    'Italia': 'IT',
    'Italien': 'IT',
    'IT': 'IT',
    'Jamaica': 'JM',
    'Japan': 'JP',
    'Jersey': 'JE',
    'Jordan': 'JO',
    'Kazakhstan': 'KZ',
    'Kenya': 'KE',
    'Kiribati': 'KI',
    "Korea (the Democratic People's Republic of)": 'KP',
    'Korea (the Republic of)': 'KR',
    "Democratic People's Republic of Korea ": 'KP',
    'Republic of Korea': 'KR',
    'Kuwait': 'KW',
    'Kyrgyzstan': 'KG',
    'Laos': 'LA',
    "Lao People's Democratic Republic": 'LA',
    'Latvia': 'LV',
    'Lebanon': 'LB',
    'Lesotho': 'LS',
    'Liberia': 'LR',
    'Libya': 'LY',
    'Liechtenstein': 'LI',
    'Lithuania': 'LT',
    'Luxembourg': 'LU',
    'Macao': 'MO',
    'Macedonia': 'MK',
    'Madagascar': 'MG',
    'Malawi': 'MW',
    'Malaysia': 'MY',
    'Maldives': 'MV',
    'Mali': 'ML',
    'Malta': 'MT',
    'Marshall Islands': 'MH',
    'Martinique': 'MQ',
    'Mauritania': 'MR',
    'Mauritius': 'MU',
    'Mayotte': 'YT',
    'Mexico': 'MX',
    'Micronesia': 'FM',
    'Federated States of Micronesia': 'FM',
    'Moldova': 'MD',
    'Republic of Moldova': 'MD',
    'Monaco': 'MC',
    'Mongolia': 'MN',
    'Montenegro': 'ME',
    'Montserrat': 'MS',
    'Morocco': 'MA',
    'Mozambique': 'MZ',
    'Myanmar': 'MM',
    'Namibia': 'NA',
    'Nauru': 'NR',
    'Nepal': 'NP',
    'Netherlands': 'NL',
    'The Netherlands': 'NL',
    'Nederlands': 'NL',
    'Holland': 'NL',
    'Pays bas': 'NL',
    'Pays-Bas': 'NL',
    'NE': 'NL',
    'New Caledonia': 'NC',
    'New Zealand': 'NZ',
    'Nicaragua': 'NI',
    'Niger': 'NE',
    'Nigeria': 'NG',
    'Niue': 'NU',
    'Norfolk Island': 'NF',
    'Northern Mariana Islands': 'MP',
    'Norway': 'NO',
    'Norwegen': 'NO',
    'Norge': 'NO',
    'Noreg': 'NO',
    'NO': 'NO',
    'Oman': 'OM',
    'Pakistan': 'PK',
    'Palau': 'PW',
    'Palestine, State of': 'PS',
    'Panama': 'PA',
    'Papua New Guinea': 'PG',
    'Paraguay': 'PY',
    'Peru': 'PE',
    'Philippines': 'PH',
    'Pitcairn': 'PN',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Puerto Rico': 'PR',
    'Qatar': 'QA',
    'Reunion': 'RE',
    'Romania': 'RO',
    'Russia': 'RU',
    'Russian Federation': 'RU',
    'Rwanda': 'RW',
    'Saint Barthelemy': 'BL',
    'Saint Helena, Ascension and Tristan da Cunha': 'SH',
    'Saint Helena': 'SH',
    'Saint Kitts and Nevis': 'KN',
    'Saint Lucia': 'LC',
    'Saint Martin': 'MF',
    'Saint Pierre and Miquelon': 'PM',
    'Saint Vincent and the Grenadines': 'VC',
    'Saint Vincent': 'VC',
    'Samoa': 'WS',
    'San Marino': 'SM',
    'Sao Tome and Principe': 'ST',
    'Saudi Arabia': 'SA',
    'Senegal': 'SN',
    'Serbia': 'RS',
    'Seychelles': 'SC',
    'Sierra Leone': 'SL',
    'Singapore': 'SG',
    'Sint Maarten': 'SX',
    'Slovakia': 'SK',
    'Slovenia': 'SI',
    'Solomon Islands': 'SB',
    'Somalia': 'SO',
    'South Africa': 'ZA',
    'South Georgia and the South Sandwich Islands': 'GS',
    'South Georgia': 'GS',
    'South Sudan': 'SS',
    'Spain': 'ES',
    'Espana': 'ES',
    'Spanien ': 'ES',
    'Espagne': 'ES',
    'ES': 'ES',
    'Sri Lanka': 'LK',
    'Sudan': 'SD',
    'Suriname': 'SR',
    'Svalbard and Jan Mayen': 'SJ',
    'Swaziland': 'SZ',
    'Sweden': 'SE',
    'Sverige': 'SE',
    'Suede': 'SE',
    'Schweden': 'SE',
    'SE': 'SE',
    'Switzerland': 'CH',
    'Schweitz': 'CH',
    'Suisse': 'CH',
    'la Suisse': 'CH',
    'Svizzera': 'CH',
    'CH': 'CH',
    'SUI': 'CH',
    'Syrian Arab Republic': 'SY',
    'Syria': 'SY',
    'Taiwan': 'TW',
    'Tajikistan': 'TJ',
    'Tanzania': 'TZ',
    'Thailand': 'TH',
    'Timor-Leste': 'TL',
    'Togo': 'TG',
    'Tokelau': 'TK',
    'Tonga': 'TO',
    'Trinidad and Tobago': 'TT',
    'Tunisia': 'TN',
    'Turkey': 'TR',
    'Turkmenistan': 'TM',
    'Turks and Caicos Islands': 'TC',
    'Tuvalu': 'TV',
    'Uganda': 'UG',
    'Ukraine': 'UA',
    'United Arab Emirates': 'AE',
    'Emirates': 'AE',
    'Great Britain': 'GB',
    'United Kingdom': 'GB',
    'UK': 'GB',
    'GB': 'GB',
    'United Kingdom of Great Britain': 'GB',
    'England': 'GB',
    'Wales': 'GB',
    'Scotland': 'GB',
    'Northern Ireland': 'GB',
    'United Kingdom of Great Britain and Northern Ireland': 'GB',
    'United States Minor Outlying Islands': 'UM',
    'USA': 'US',
    'United States of America (the)': 'US',
    'United States': 'US',
    'America': 'US',
    'the US': 'US',
    'US of A': 'US',
    'USofA': 'US',
    'US': 'US',
    'Uruguay': 'UY',
    'Uzbekistan': 'UZ',
    'Vanuatu': 'VU',
    'Venezuela': 'VE',
    'Viet Nam': 'VN',
    'Virgin Islands (British)': 'VG',
    'Virgin Islands (U.S.)': 'VI',
    'Wallis and Futuna': 'WF',
    'Western Sahara*': 'EH',
    'Yemen': 'YE',
    'Zambia': 'ZM',
    'Zimbabwe': 'ZW',	 
    'Brunei': 'BN',
    'Republic of Croatia': 'HR',
    'Vietnam': 'VN', 
}

subjurisdiction_codes = {
    'Canada': {
        'Alberta': 'AB',
        'British Columbia': 'BC',
        'Manitoba': 'MB',
        'New Brunswick': 'NB',
        'Newfoundland and Labrador': 'NL',
        'Nova Scotia': 'NS',
        'Ontario': 'ON',
        'Prince Edward Island': 'PE',
        'Quebec': 'QC',
        'Saskatchewan': 'SK',
        'Northwest Territories': 'NT',
        'Nunavut': 'NU',
        'Yukon': 'YT',
    },
    'Australia': {
        'New South Wales': 'NSW',
        'Queensland': 'QLD',
        'South Australia': 'SA',
        'Tasmania': 'TAS',
        'Victoria': 'VIC',
        'Western Australia': 'WA',
        'Australian Capital Territory': 'ACT',
        'Northern Territory': 'NT',
        'Jervis Bay Territory': 'JBT',
    },
}

cfi_char_dict = {'E': {
                        'S': 'Equities - Shares & Depositary Receipts', 
                        'P': 'Other instruments', 
                        'C': 'Other instruments', 
                        'F': 'Other instruments', 
                        'L': 'Other instruments', 
                        'D': 'Equities - Shares & Depositary Receipts',
                        'Y': 'Structured finance instruments',
                        'M': 'Other instruments',
                        },
                'C': {
                        'B': 'Other instruments', 
                        'E': 'Exchange traded products (Exchange traded funds, exchange traded notes and exchange traded commodities)',
                        'F': 'Other instruments', 
                        'H': 'Other instruments', 
                        'I': 'Other instruments', 
                        'M': 'Other instruments', 
                        'P': 'Other instruments', 
                        'S': 'Other instruments', 
                        },
                'D': {
                        'A': 'Structured finance instruments',
                        'B': 'Debt instruments - Bonds',
                        'C': 'Other instruments',
                        'D': 'Other instruments',
                        'E': 'Structured finance instruments',
                        'G': 'Structured finance instruments',
                        'M': 'Other instruments',
                        'N': 'Debt instruments - Bonds',
                        'S': 'Structured finance instruments',
                        'T': 'Debt instruments - Bonds',
                        'W': 'Debt instruments - Bonds',
                        'Y': 'Debt instruments - Money markets instruments',
                       },
                'R': {
                        'A': 'Securitized Derivatives - Warrants and Certificate Derivatives',
                        'D': 'Securitized Derivatives - Warrants and Certificate Derivatives',
                        'F': 'Securitized Derivatives - Other securitized derivatives',
                        'M': 'Securitized Derivatives - Other securitized derivatives',
                        'P': 'Securitized Derivatives - Warrants and Certificate Derivatives',
                        'S': 'Securitized Derivatives - Warrants and Certificate Derivatives',
                        'W': 'Securitized Derivatives - Warrants and Certificate Derivatives',
                      },
                'O': {
                        '*': { '*': {
                                        'B': 'Other instruments',
                                        'C': 'Currency derivatives - Futures and options admitted to trading on a trading venue',
                                        'D': 'Other instruments',
                                        'F': 'Other instruments',
                                        'I': 'Other instruments',
                                        'M': 'Other instruments',
                                        'N': 'Interest rates derivatives-Futures and options admitted to trading on a trading venue',
                                        'O': 'Other instruments',
                                        'S': 'Equity Derivatives - Options and Futures admitted to trading on a trading venue',
                                        'T': 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue',
                                        'W': 'Other instruments',
                                      },
                              },
                        'M': 'Other instruments',
                      },
                'F': {
                        'C': 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue',
                        'F': {
                                    'B': 'Other instruments',
                                    'C': 'Currency derivatives - Futures and options admitted to trading on a trading venue',
                                    'D': 'Other instruments',
                                    'F': 'Other instruments',
                                    'I': 'Other instruments',
                                    'M': 'Other instruments',
                                    'N': 'Interest rates derivatives-Futures and options admitted to trading on a trading venue',
                                    'O': 'Other instruments',
                                    'S': 'Equity Derivatives - Options and Futures admitted to trading on a trading venue',
                                    'V': 'Other instruments',
                                    'W': 'Other instruments',
                                },                        
                      },
                'S': {
                        'C': 'Credit Derivatives - Other credit derivatives',
                        'E': 'Equity Derivatives - Swaps and other equity derivatives',
                        'F': 'Currency derivatives - Swaps, forwards, and other currency derivatives',
                        'M': 'Other instruments',
                        'R': 'Interest Rate Deriviatives - Swaps, forwards, and other interest rates derivatives',
                        'T': 'Commodities derivatives and emission allowances Derivatives - Other commodities derivatives and emission allowances derivatives',
                      },
                'H': {
                        'C': 'Credit Derivatives - Futures and options admitted to trading on a trading venue',
                        'E': 'Equity Derivatives - Options and Futures admitted to trading on a trading venue',
                        'F': 'Currency derivatives - Futures and options admitted to trading on a trading venue',
                        'M': 'Other instruments',
                        'R': 'Interest Rate Deriviatives - Futures and options admitted to trading on a trading venue',
                        'T': 'Commodities derivatives and emission allowances Derivatives - Options and Futures admitted to trading on a trading venue',
                      },
                'J': {
                        'C': {'*' : {'*' : {'F' : 'Credit Derivatives - Futures and options admitted to trading on a trading venue'}}},
                        'E': {'*' : {'*' : {'C' : 'Contracts for difference', '*' : 'Equity Derivatives - Options and Futures admitted to trading on a trading venue'}}},
                        'F': 'Currency derivatives - Swaps, forwards, and other currency derivatives',
                        'R': 'Interest Rate Deriviatives - Swaps, forwards, and other interest rates derivatives',
                        'T': {'*' : {'*' : {'C' : 'Contracts for difference', 'F' : 'Currency derivatives - Futures and options admitted to trading on a trading venue'}}},
                      },
                'K': 'Other instruments',
                'L': 'Other instruments',
                'T': 'Other instruments',
                'M': 'Other instruments',
                }

city_state_dict = {

    'Calgary': 'Alberta',
    'Edmonton': 'Alberta',
    'Red Deer': 'Alberta',
    'Strathcona County': 'Alberta',
    'Lethbridge': 'Alberta',
    'Wood Buffalo': 'Alberta',
    'St. Albert': 'Alberta',
    'Medicine Hat': 'Alberta',
    'Grande Prairie': 'Alberta',
    'Airdrie': 'Alberta',
    'Vancouver': 'British Columbia',
    'Surrey': 'British Columbia',
    'Burnaby': 'British Columbia',
    'Richmond': 'British Columbia',
    'Langley': 'British Columbia',
    'Abbotsford': 'British Columbia',
    'Coquitlam': 'British Columbia',
    'North Vancouver': 'British Columbia',
    'Kelowna': 'British Columbia',
    'Winnipeg': 'Manitoba',
    'Brandon': 'Manitoba',
    'Morden': 'Manitoba',
    'Steinbach': 'Manitoba',
    'Thompson': 'Manitoba',
    'Portage la Prairie': 'Manitoba',
    'Winkler': 'Manitoba',
    'Selkirk': 'Manitoba',
    'Dauphin': 'Manitoba',
    'Moncton': 'New Brunswick',
    'Saint John': 'New Brunswick',
    'Fredericton': 'New Brunswick',
    'Dieppe': 'New Brunswick',
    'Riverview': 'New Brunswick',
    'Quispamsis': 'New Brunswick',
    'Edmundston': 'New Brunswick',
    'Miramichi': 'New Brunswick',
    "St. John's": 'Newfoundland and Labrador',
    'Conception Bay South': 'Newfoundland and Labrador',
    'Mount Pearl': 'Newfoundland and Labrador',
    'Paradise': 'Newfoundland and Labrador',
    'Corner Brook': 'Newfoundland and Labrador',
    'Grand Falls ': 'Newfoundland and Labrador',
    'Gander': 'Newfoundland and Labrador',
    'Portugal Cove': 'Newfoundland and Labrador',
    'Happy Valley': 'Newfoundland and Labrador',
    'Torbay': 'Newfoundland and Labrador',
    'Halifax': 'Nova Scotia',
    'Cape Breton ': 'Nova Scotia',
    'Truro': 'Nova Scotia',
    'Amherst': 'Nova Scotia',
    'New Glasgow ': 'Nova Scotia',
    'Bridgewater': 'Nova Scotia',
    'Yarmouth': 'Nova Scotia',
    'Kentville': 'Nova Scotia',
    'Charlottetown': 'Prince Edward Island',
    'Summerside': 'Prince Edward Island',
    'Toronto': 'Ontario',
    'Ottawa': 'Ontario',
    'Mississauga': 'Ontario',
    'Brampton': 'Ontario',
    'Hamilton': 'Ontario',
    'London': 'Ontario',
    'Markham': 'Ontario',
    'Vaughan': 'Ontario',
    'Kitchener': 'Ontario',
    'Montreal': 'Quebec',
    'Quebec City': 'Quebec',
    'Laval': 'Quebec',
    'Gatineau': 'Quebec',
    'Longueuil': 'Quebec',
    'Saguenay': 'Quebec',
    'Levis': 'Quebec',
    'Sherbrooke': 'Quebec',
    'Saint-Jean-sur-Richelieu': 'Quebec',
    'Chicoutimi': 'Quebec',
    'Drummondville': 'Quebec',
    'Saint-jerome': 'Quebec',
    'Granby': 'Quebec',
    'Saint-Hyacinthe': 'Quebec',
    'Terrebonne': 'Quebec',
    'Trois-Rivieres': 'Quebec',
    'Saskatoon': 'Saskatchewan',
    'Regina': 'Saskatchewan',
    'Prince Albert': 'Saskatchewan',
    'Moose Jaw': 'Saskatchewan',
    'Swift Current': 'Saskatchewan',
    'Yorkton': 'Saskatchewan',
    'North Battleford': 'Saskatchewan',
    'Estevan': 'Saskatchewan',
    'Warman': 'Saskatchewan',
    'Weyburn': 'Saskatchewan',
    'Yellowknife': 'Northwest Territories',
    'Iqaluit': 'Nunavut',
    'Whitehorse': 'Yukon',
    'Sydney': 'New South Wales',
    'Albury': 'New South Wales',
    'Tweed Heads': 'New South Wales',
    'Newcastle - Maitland': 'New South Wales',
    'Maitland': 'New South Wales',
    'Port Macquarie': 'New South Wales',
    'Wollongong': 'New South Wales',
    'Shellharbour': 'New South Wales',
    'Taree': 'New South Wales',
    'Penrith': 'New South Wales',
    'Coffs Harbour': 'New South Wales',
    'Blacktown': 'New South Wales',
    'Gosford': 'New South Wales',
    'Wagga Wagga': 'New South Wales',
    'Tamworth': 'New South Wales',
    'Brisbane': 'Queensland',
    'Bundaberg': 'Queensland',
    'Cairns': 'Queensland',
    'Caloundra': 'Queensland',
    'Charters Towers': 'Queensland',
    'Gladstone': 'Queensland',
    'Gold Coast': 'Queensland',
    'Gympie': 'Queensland',
    'Hervey Bay': 'Queensland',
    'Ipswich': 'Queensland',
    'Logan City‎': 'Queensland',
    'Mackay': 'Queensland',
    'Maryborough': 'Queensland',
    'Mount Isa‎': 'Queensland',
    'Redland City‎': 'Queensland',
    'Rockhampton‎': 'Queensland',
    'Toowoomba': 'Queensland',
    'Townsville‎': 'Queensland',
    'Warwick': 'Queensland',
    'Sunshine Coast': 'Queensland',
    'Townsville': 'Queensland',
    'Toowoomba': 'Queensland',
    'Mackay': 'Queensland',
    'Rockhampton': 'Queensland',
    'Adelaide': 'South Australia',
    'Hobart': 'Tasmania',
    'Launceston': 'Tasmania',
    'Devonport': 'Tasmania',
    'Melbourne': 'Victoria',
    'Geelong': 'Victoria',
    'Ballarat': 'Victoria',
    'Bendigo': 'Victoria',
    'Albury - Wodonga': 'Victoria',
    'Mildura': 'Victoria',
    'Shepparton': 'Victoria',
    'Traralgon': 'Victoria',
    'Wangaratta': 'Victoria',
    'Warrnambool': 'Victoria',
    'Perth': 'Western Australia',
    'Bunbury': 'Western Australia',
    'Geraldton': 'Western Australia',
    'Busselton': 'Western Australia',
    'Albany': 'Western Australia',
    'Kalgoorlie-Boulder': 'Western Australia',
    'Rockingham': 'Western Australia',
    'Mandurah': 'Western Australia',
    'Darwin': 'Northern Territory',
    'Alice Springs': 'Northern Territory',
    'Palmerston': 'Northern Territory',
    'Darwin': 'Northern Territory',
}

rts2_ins_type_lookup = {
    'CreditDefaultSwap': 'FUNCTION',
    'CLN': 'Structured Finance Products',
    'Bill': 'Bonds',
    'Bond': 'Bonds',
    'CD': 'Bonds',
    'Basket CDS': 'Structured Finance Products',
    'CDS': 'Credit Derivatives',
    'Combination': 'Structured Finance Products',
    'Convertible': 'FUNCTION',
    'Credit Balance': 'Credit Derivatives',
    'CreditIndex': 'Credit Derivatives',
    'DualCurrBond': 'Bonds',
    'Flexi Bond': 'Bonds',
    'FRN': 'Bonds',
    'Future/Forward': 'FUNCTION',
    'MBS/ABS': 'Structured Finance Products',
    'Fund': 'Structured Finance Products',
    'Option': 'FUNCTION',
    'Portfolio Swap': 'Structured Finance Products',
    'PromisLoan': 'Structured Finance Products',
    'TotalReturnSwap': 'FUNCTION',
    'Zero': 'Bonds',
    'Deposit': 'Structured Finance Products',
    'Curr': 'Foreign Exchange Derivatives',
    'CFD': 'CFDs',
    'FXOptionDatedFwd': 'Foreign Exchange Derivatives',
    'FxSwap': 'Foreign Exchange Derivatives',
    'Average Future/Forward': 'Commodity Derivatives',
    'Commodity': 'Commodity Derivatives',
    'Commodity Index': 'Commodity Derivatives',
    'Commodity Variant': 'Commodity Derivatives',
    'PriceSwap': 'Commodity Derivatives',
    'Rolling Schedule': 'Commodity Derivatives',
    'Certificate': 'Structured Finance Products',
    'Depositary Receipt': 'Equity Derivatives',
    'Dividend Point Index': 'Equity Derivatives',
    'EquityIndex': 'Equity Derivatives',
    'ETF': 'Equity Derivatives',
    'SecurityLoan': 'Structured Finance Products',
    'Stock': '',
    'VarianceSwap': 'Equity Derivatives',
    'VolatilitySwap': 'Equity Derivatives',
    'Warrant': 'Equity Derivatives',
    'BasketRepo/Reverse': 'Structured Finance Products',
    'BasketSecurityLoan': 'Structured Finance Products',
    'BuySellback': 'Structured Finance Products',
    'Cap': 'Interest Rate Derivatives',
    'FreeDefCF': 'Structured Finance Products',
    'CurrSwap': 'Structured Finance Products',
    'Floor': 'Interest Rate Derivatives',
    'Collar': 'Interest Rate Derivatives',
    'FRA': 'Structured Finance Products',
    'IndexLinkedBond': 'Bonds',
    'IndexLinkedSwap': 'Structured Finance Products',
    'PriceIndex': 'Structured Finance Products',
    'RateIndex': 'Structured Finance Products',
    'Repo/Reverse': 'Structured Finance Products',
    'Swap': 'Interest Rate Derivatives',
    'Deposit': 'Structured Finance Products',
}
rts2_sub_ins_type_lookup = {
    'CreditDefaultSwap': 'FUNCTION',
    'CLN': 'DERIVE_FROM_VALGROUP',
    'Bill': 'DERIVE_FROM_VALGROUP',
    'Bond': 'DERIVE_FROM_VALGROUP',
    'CD': 'DERIVE_FROM_VALGROUP',
    'CDS': 'Index or Single name CDS',
    'Credit Balance': 'Other Credit Derivatives',
    'CreditIndex': 'Other Credit Derivatives',
    'DualCurrBond': 'DERIVE_FROM_VALGROUP',
    'Flexi Bond': 'DERIVE_FROM_VALGROUP',
    'FRN': 'DERIVE_FROM_VALGROUP',
    'Future/Forward': 'FUNCTION',
    'Option': 'FUNCTION',
    'Zero': 'DERIVE_FROM_VALGROUP',
    'Curr': 'Other Foreign Exchange Derivatives',
    'CFD': 'FUNCTION',
    'FXOptionDatedFwd': 'Non-Deliverable Forward',
    'FxSwap': 'Non-Deliverable FX Swaps',
    'Average Future/Forward': 'Other Commodity Derivatives',
    'Commodity': 'Other Commodity Derivatives',
    'Commodity Index': 'Other Commodity Derivatives',
    'Commodity Variant': 'Other Commodity Derivatives',
    'PriceSwap': 'Other Commodity Derivatives',
    'Rolling Schedule': 'Other Commodity Derivatives',
    'Depositary Receipt': 'Other Equity Derivatives',
    'Dividend Point Index': 'Dividend Index Options',
    'EquityIndex': 'Stock Index Options',
    'ETF': 'Other Equity Derivatives',
    'Stock': '',
    'VarianceSwap': 'Other Equity Derivatives',
    'VolatilitySwap': 'Other Equity Derivatives',
    'Warrant': 'Other Equity Derivatives',
    'IndexLinkedBond': 'DERIVE_FROM_VALGROUP',
    'Swap': 'Other Interest Rate Derivatives',
    'Cap': 'Other Interest Rate Derivatives',
    'Floor': 'Other Interest Rate Derivatives',
    'FRA': 'Other Interest Rate Derivatives',
    'TotalReturnSwap': 'FUNCTION',
}

rts_28_ins_type = {
    'Stock': 'Equities - Shares & Depositary Receipts',
    'Depositary Receipt': 'Equities - Shares & Depositary Receipts',
    'Option': 'Futures and options admitted to trading on a trading venue',
    'LEPO': 'Futures and options admitted to trading on a trading venue',
    'Cap': 'Futures and options admitted to trading on a trading venue',
    'Floor': 'Futures and options admitted to trading on a trading venue',
    'Future/Forward': 'Futures and options admitted to trading on a trading venue',
    'Warrant': 'Warrants and Certificate Derivatives',
    'Bond': 'Bonds',
    'FRN': 'Bonds',
    'Zero': 'Bonds',
    'Convertible': 'Bonds',
    'IndexLinkedBond': 'Bonds',
    'DualCurrBond': 'Bonds',
    'Flexi Bond': 'Bonds',
    'PromisLoan': 'Money Market Instruments',
    'Bill': 'Money Market Instruments',
    'CD': 'Money Market Instruments',
    'Deposit': 'Money Market Instruments',
    'Repo/Reverse': 'Money Market Instruments',
    'BuySellback': 'Money Market Instruments',
    'BasketRepo/Reverse': 'Money Market Instruments',
    'Certificate': 'Money Market Instruments',
    'Swap': 'Swaps, forwards and other interest rate derivatives',
    'FRA': 'Swaps, forwards and other interest rate derivatives',
    'CurrSwap': 'Swaps, forwards and other currency derivatives',
    'FxSwap': 'Swaps, forwards and other currency derivatives',
    'FXOptionDatedFwd': 'Swaps, forwards and other currency derivatives',
    'TotalReturnSwap': 'Swaps and other equity derivatives',
    'EquitySwap': 'Swaps and other equity derivatives',
    'CreditDefaultSwap': 'Other credit derivatives',
    'CLN': 'Other credit derivatives',
    'VarianceSwap': 'Other Equity Derivatives',
    'PriceSwap': 'Structured Finance Instruments',
    'VolatilitySwap': 'Structured Finance Instruments',
    'Average Future/Forward': 'Structured Finance Instruments',
    'Portfolio Swap': 'Structured Finance Instruments',
    'MultiOption': 'Structured Finance Instruments',
    'MultiAsset ': 'Structured Finance Instruments',
    'Combination': 'Structured Finance Instruments',
    'FreeDefCF': 'Structured Finance Instruments',
    'MBS/ABS': 'Structured Finance Instruments',
    'Certificate': 'Structured Finance Instruments',
    'IndexLinkedSwap': 'Other securitized derivatives',
    'CFD': 'Contracts for Difference',
    'ETF': 'Exchange Traded Products',
    'Commodity Variant': 'Other commodities derivatives and Emission Allowances Derivatives',
    'Rolling Schedule': 'Other commodities derivatives and Emission Allowances Derivatives',
    'Commodity': 'Other Instruments',
    'Curr': 'Other Instruments',
    'EquityIndex': 'Other Instruments',
    'BondIndex': 'Other Instruments',
    'RateIndex': 'Other Instruments',
    'Collateral': 'Other Instruments',
    'SecurityLoan': 'Other Instruments',
    'PriceIndex': 'Other Instruments',
    'UnKnown': 'Other Instruments',
    'CallAccount': 'Other Instruments',
    'CashCollateral': 'Other Instruments',
    'CreditIndex': 'Other Instruments',
    'BasketSecurityLoan': 'Other Instruments',
    'Fund': 'Other Instruments',
    'Fx Rate': 'Other Instruments',
    'Commodity Index': 'Other Instruments',
    'Credit Balance': 'Other Instruments',
    'Dividend Point Index': 'Other Instruments',
}
city_code_lookup = {'United States': { 'Wichita': 'USWT', 
                                        'Honolulu': 'USHL', 
                                        'Mobile': 'USMB',
                                        'Minneapolis': 'USMN',
                                        'Detroit': 'USDT',
                                        'Denver': 'USDN',
                                        'Washington': 'USDC',
                                        'Charlotte': 'USCR', }, 
                    'Trinidad and Tobago': {'Port of Spain': 'TTPS', }, 
                    'Tanzania': {'Dar es Salaam': 'TZDA', }, 
                    'Philippines': {'Makati': 'PHMK', }, 
                    'Cayman Islands': {'George Town': 'KYGE', }, 
                    'Canada': {'Calgary': 'CACL', }, 
                    'Brazil': {'Brasilia' : 'BRDB', 'Rio de Janeiro' : 'BRDB'},
                    }
class RTS2Classification(object):
    def __init__(self, instrument, current_date=None):
        self.__instrument = instrument
        self.current_date = current_date

    def CreditDefaultSwap_rts2(self):
        ins_type = 'CDS'
        rts2_instype = ''
        if self.__instrument.Underlying().InsType() in ['Combination', 'CreditIndex']:
            ins_type = 'Basket CDS'
        if ins_type in rts2_ins_type_lookup:
            rts2_instype = rts2_ins_type_lookup[ins_type]
        return rts2_instype

    def CreditDefaultSwap_rts2_sub_type(self):
        ins_type = 'CDS'
        rts2_subtype = ''
        if self.__instrument.Underlying().InsType() in ['Combination', 'CreditIndex']:
            ins_type = 'Basket CDS'
        if ins_type in rts2_sub_ins_type_lookup:
            rts2_subtype = rts2_sub_ins_type_lookup[ins_type]
        return rts2_subtype

    def Convertible_rts2(self):
        rts2_instype = 'Interest Rate Derivatives'
        if self.__instrument.Underlying().InsType() in ['Depositary Receipt', 'Stock', 'EquityIndex']:
            rts2_instype = 'Equity Derivatives'
        elif self.__instrument.Underlying().InsType() in ['Commodity Index', 'Commodity', 'Commodity Variant']:
            rts2_instype = 'Commodity Derivatives'
        return rts2_instype

    def Convertible_rts2_sub_type(self):
        rts2_subtype = 'Other Interest Rate Derivatives'
        if self.__instrument.Underlying().InsType() in ['Depositary Receipt', 'Stock', 'EquityIndex']:
            rts2_subtype = 'Other Equity Derivatives'
        elif self.__instrument.Underlying().InsType() in ['Commodity Index', 'Commodity', 'Commodity Variant']:  # TODO: Verify with Ishan
            rts2_subtype = 'Other Commodity Derivatives'
        return rts2_subtype

    def TotalReturnSwap_rts2(self):
        rts2_instype = 'Interest Rate Derivatives'
        total_return_leg = False
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Total Return':
                total_return_leg = True
        if total_return_leg:
            rts2_instype = 'Structured Finance Products'
        return rts2_instype

    def TotalReturnSwap_rts2_sub_type(self):
        rts2_subtype = 'Other Interest Rate Derivatives'
        total_return_leg = False
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Total Return':
                total_return_leg = True
        if total_return_leg:
            rts2_subtype = ''
        return rts2_subtype

    def Future_Forward_rts2(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_instype = self.__rts2_classification_with_underlyer(self.__instrument)
        return rts2_instype

    def Future_Forward_rts2_sub_type(self):
        rts2_subtype = ''
        if self.__instrument.Underlying().InsType() in ['CreditDefaultSwap', 'CLN']:
            rts2_subtype = 'Other Credit Derivatives'
        if self.__instrument.Underlying().InsType() in ['FRA', 'Swap']:
            rts2_subtype = 'IR Futures & FRA'
        if self.__instrument.Underlying().InsType() in ['FRN', 'IndexLinkedBond', 'RateIndex']:
            rts2_subtype = 'Other Interest Rate Derivatives'
        elif self.__instrument.Underlying().InsType() in ['Depositary Receipt', 'Dividend Point Index', 'EquityIndex', 'Stock', 'ETF']:
            rts2_subtype = 'Stock Futures/Forwards'
        elif self.__instrument.Underlying().InsType() in ['Commodity Index', 'Commodity', 'Commodity Variant', 'Average Future/Forward']:
            rts2_subtype = 'Metal/Agriculture/Energy/ Other Commodity Derivatives'
        elif self.__instrument.Underlying().InsType() in ['Curr']:
            if self.__instrument.PayType() == 'Future':
                rts2_subtype = 'FX Futures'
            elif self.__instrument.PayType() == 'Forward':
                rts2_subtype = 'Non-Deliverable Forward'
        elif self.__instrument.Underlying().InsType() in ['Bond', 'Zero', 'Bill']:
            rts2_subtype = 'Bond Futures/Forwards'
        return rts2_subtype

    def __rts2_classification_with_underlyer(self, instrument):
        rts2_instype = 'Interest Rate Derivatives'
        if instrument.Underlying().InsType() in ['CreditDefaultSwap', 'CLN']:
            rts2_instype = 'Credit Derivatives'
        elif instrument.Underlying().InsType() in ['Curr', 'CurrSwap']:
            rts2_instype = 'Foreign Exchange Derivatives'
        elif instrument.Underlying().InsType() in ['Average Future/Forward', 'Commodity Index', 'Commodity', 'Commodity Variant']:
            rts2_instype = 'Commodity Derivatives'
        elif instrument.Underlying().InsType() in ['Depositary Receipt', 'EquityIndex', 'Stock', \
                     'Warrant', 'Dividend Point Index']:
            rts2_instype = 'Equity Derivatives'
        elif instrument.Underlying().InsType() in ['IndexLinkedSwap', 'PromisLoan', 'Convertible', \
                                                            'Combination', 'ETF', 'Fund', \
                                                            'TotalReturnSwap', 'CFD', 'FreeDefCF', 'Deposit']:
            rts2_instype = 'Structured Finance Products'
        elif instrument.Underlying().InsType() in ['Future/Forward', 'VarianceSwap']:
            rts2_instype = self.__rts2_classification_with_underlyer(instrument.Underlying())
        return rts2_instype

    def Option_rts2(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_instype = self.__rts2_classification_with_underlyer(self.__instrument)
        return rts2_instype

    def __rts2_sub_type_classification_with_underlyer(self, instrument):
        rts2_subtype = ''
        if instrument.Underlying().InsType() in ['Zero']:
            rts2_subtype = 'IR Options'
        elif instrument.Underlying().InsType() in ['FRA']:
            rts2_subtype = 'IR Futures & FRA'
        elif instrument.Underlying().InsType() in ['CLN']:
            rts2_subtype = 'Other Credit Derivatives'
        elif instrument.Underlying().InsType() in ['CreditDefaultSwap']:
            rts2_subtype = 'CDS index options/Single name CDS options'
        elif instrument.Underlying().InsType() in ['CurrSwap']:
            rts2_subtype = 'Other Foreign Exchange Derivatives'
        elif instrument.Underlying().InsType() in ['Curr']:
            if instrument.SettlementType() == 'Cash':
                rts2_subtype = 'Non-Deliverable FX Options'
            else:
                rts2_subtype = 'Deliverable FX Options'
        elif instrument.Underlying().InsType() in ['Commodity Index', 'Commodity Variant', 'Average Future/Forward']:
            rts2_subtype = 'Other Commodity Derivatives'
        elif instrument.Underlying().InsType() in ['Commodity', ]:
            rts2_subtype = 'Agricultural/ Metal/ Energy/ Other Commodity Derivatives'
        elif instrument.Underlying().InsType() in ['Stock']:
            rts2_subtype = 'Stock Options'
        elif instrument.Underlying().InsType() in ['EquityIndex']:
            rts2_subtype = 'Stock Index Options'
        elif instrument.Underlying().InsType() in ['Bill', 'Bond']:
            rts2_subtype = 'Bond Options'
        elif instrument.Underlying().InsType() in ['Warrant', 'Depositary Receipt']:
            rts2_subtype = 'Other Equity Derivatives'
        elif instrument.Underlying().InsType() in ['Cap', 'Floor', 'FRA', 'FRN', 'RateIndex', 'Deposit']:
            rts2_subtype = 'Other Interest Rate Derivatives'
        elif instrument.Underlying().InsType() in ['TotalReturnSwap']:
            rts2_subtype = 'Other Structured Finance Products Derivatives'
        elif instrument.Underlying().InsType() in ['Swap']:
            rts2_subtype = 'Other Interest Rate Derivatives'
        elif instrument.Underlying().InsType() in ['Future/Forward', 'VarianceSwap']:
            rts2_subtype = self.__rts2_sub_type_classification_with_underlyer(instrument.Underlying())
        return rts2_subtype

    def Option_rts2_sub_type(self):
        rts2_subtype = ''
        rts2_subtype = self.__rts2_sub_type_classification_with_underlyer(self.__instrument)
        return rts2_subtype

    def CFD_rts2_sub_type(self):
        rts2_subtype = 'Equity CFDs'
        if self.__instrument.Underlying().InsType() in ['Bond']:
            rts2_subtype = 'Bond CFDs'
        return rts2_subtype

    def __derive_ins_sub_type_from_valgroup(self):
        sub_type = 'Other Bond'
        #this code was commented as only on the basis of this categorization, it is not fullproof to be applicable across insTypes
        #if self.__instrument.SeniorityChlItem() and self.__instrument.SeniorityChlItem().Name() == 'SNRFOR':
        #    sub_type = 'Covered Bond'
        if self.__instrument.CategoryChlItem():
            if self.__instrument.CategoryChlItem().Name().upper() in ['GOVERNMENT']:
                sub_type = 'Sovereign Bond'
            elif self.__instrument.CategoryChlItem().Name().upper() in ['MUNICIPAL']:
                sub_type = 'Other Public Bond'
            elif self.__instrument.CategoryChlItem().Name().upper() in ['CORPORATE']:
                sub_type = 'Corporate Bond'
        return sub_type

    def mifid2_rts2_instype(self):
        ins_type = ''
        if self.__instrument.InsType() in rts2_ins_type_lookup:
            ins_type = rts2_ins_type_lookup[self.__instrument.InsType()]
            if ins_type == 'FUNCTION':
                instrument_type = self.__instrument.InsType()
                if instrument_type.find('/') != -1:
                    instrument_type = instrument_type.replace('/', '_')
                ins_type = eval('self.' + instrument_type + '_rts2()')
        return ins_type

    def mifid2_rts2_inssubtype(self):
        ins_type = ''
        if self.__instrument.InsType() in rts2_sub_ins_type_lookup:
            ins_type = rts2_sub_ins_type_lookup[self.__instrument.InsType()]
            if ins_type == 'FUNCTION':
                instrument_type = self.__instrument.InsType()
                if instrument_type.find('/') != -1:
                    instrument_type = instrument_type.replace('/', '_')
                ins_type = eval('self.' + instrument_type + '_rts2_sub_type()')
            elif ins_type == 'DERIVE_FROM_VALGROUP':
                ins_type = self.__derive_ins_sub_type_from_valgroup()
        return ins_type

    def get_business_date_range(self):
        current_year = str(acm.Time().DateToYMD(self.current_date)[0])
        date_range_dict = {
            (ael.date(current_year + "-02-16"), ael.date(current_year + "-05-15")): (
            ael.date(current_year + "-01-31"), ael.date(str(int(current_year) - 1) + "-11-01")),
            (ael.date(current_year + "-05-16"), ael.date(current_year + "-08-15")): (
            ael.date(current_year + "-04-30"), ael.date(current_year + "-02-01")),
            (ael.date(current_year + "-08-16"), ael.date(current_year + "-11-15")): (
            ael.date(current_year + "-07-31"), ael.date(current_year + "-05-01")),
            (ael.date(current_year + "-11-16"), ael.date(current_year + "-12-31")): (
            ael.date(current_year + "-10-31"), ael.date(current_year + "-08-01")),
            (ael.date(current_year + "-01-01"), ael.date(current_year + "-02-15")): (
            ael.date(str(int(current_year) - 1) + "-10-31"), ael.date(str(int(current_year) - 1) + "-08-01")),
        }
        businessdays, dates = None, None
        from FOperationsDateUtils import GetAccountingCurrencyCalendar
        calendar = GetAccountingCurrencyCalendar()
        calInfo = calendar.CalendarInformation()
        if self.current_date <= ael.date("2018-05-15"):
            businessdays = calInfo.BankingDaysBetween(ael.date("2018-02-01"), ael.date("2018-01-03"))
            dates = (ael.date("2018-02-01"), ael.date("2018-01-03"))
        else:
            for date_range in date_range_dict:
                if self.current_date <= date_range[1] and self.current_date >= date_range[0]:
                    businessdays = calInfo.BankingDaysBetween(date_range_dict[date_range][0],
                                                              date_range_dict[date_range][1])
                    dates = date_range_dict[date_range]
                    break
        return businessdays, dates

    def get_total_nominal_value(self):
        trades = self.__instrument.Trades()
        nominal_value = 0
        businessdays, dates = self.get_business_date_range()
        if trades:
            for trade in trades:
                if ael.date(str(trade.TradeTime())[:10]) <= dates[0] and ael.date(str(trade.TradeTime())[:10]) >= dates[
                    1]:
                    nominal_value += trade.Nominal()
        return nominal_value, businessdays, dates

    def get_average_daily_trades(self, businessdays, dates):
        trades = self.__instrument.Trades()
        first_trade_ind = 0
        count_trade = 0
        trade_dates = set()
        for trade in trades:
            if ael.date(str(trade.TradeTime())[:10]) <= dates[0] and ael.date(str(trade.TradeTime())[:10]) >= dates[1]:
                count_trade += 1
                trade_dates.add(str(trade.TradeTime())[:10])
        if len(trade_dates) and min(trade_dates) <= dates[0] and ael.date(str(trade.TradeTime())[:10]) >= dates[1]:
            first_trade_ind = 1
        return dates, int(count_trade / businessdays), int(len(trade_dates) * 100.0 / businessdays), first_trade_ind

