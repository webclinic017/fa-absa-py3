import acm

instrumentSet = ['158519-ZAR-2201-01',
'159160-ZAR-2203-01',
'613166-ZAR-2201-04',
'620559-ZAR-2201-01',
'731646-ZAR-2201-01',
'732065-ZAR-2201-01',
'455353-ZAR-2201-01',
'455353-ZAR-2201-01',
'1858340-ZAR-2201-01',
'3316252-ZAR-2201-01',
'4671732-ZAR-2201-01',
'4814391-ZAR-2201-01',
'5417195-ZAR-2201-01',
'610329-ZAR-2201-01',
'2337922-ZAR-2201-01',
'2431581-ZAR-2201-01',
'416483-ZAR-2201-01',
'2107299-ZAR-2201-01',
'1796739-ZAR-2201-01',
'4467420-ZAR-2201-01',
'4336085-ZAR-2201-01',
'435610-ZAR-2201-01',
'4467420-ZAR-2201-01',
'437742-ZAR-2201-01',
'4494943-ZAR-2201-01',
'1231533-ZAR-2201-01',
'6185854-ZAR-2201-01',
'5253685-ZAR-2203-01',
'736199-ZAR-2201-01'
]

for i in instrumentSet:
    try: 
        ins = acm.FInstrument[i]
        ins.Touch()
        ins.Commit()
        print('Instrument %s touched successfully' %i)

    except:
        print('could not touch instrument %s' %i)
