
import acm
import FUxCore
import FUxUtils
import string

connectedStrikeTypes = [acm.FSymbol('Absolute'), acm.FSymbol('Rel Spot'), acm.FSymbol('Rel Spot Pct')]
shiftDateFunction = acm.GetFunction('shiftVolatilityStructureDate', 2)

def isConnectedStrikeTypes(strikeTypeChosen, volStrikeType):
    return (acm.FSymbol(volStrikeType) in connectedStrikeTypes) and (acm.FSymbol(strikeTypeChosen) in connectedStrikeTypes)

def GenerateStrikeArrayFromVolatilityStructure(vs):
    bucketsset = set()
    for p in vs.Points():
        strike = p.ConvertedStrike()
        bucketsset.add( strike )
    bucketslist = list( bucketsset )
    bucketslist.sort()
    return bucketslist

def GenerateStrikeArray(nbrOfStrikes, firstStrike, offset):
    bucketslist = []
    referenceStrike = firstStrike
    strike = firstStrike
    nextStrike = firstStrike + offset
    for i in range(nbrOfStrikes):
        bucketslist.append( strike )
        strike = nextStrike
        referenceStrike += offset
        nextStrike = referenceStrike + offset
    return bucketslist

def AddGeneralAttributes(namedParameters, referenceInstrument, volFilter, additionalTimeBucket, strikeTypeChosen, groupingSensitive, useOnesidedShift):
    for namedParam in namedParameters:
        namedParam.AddParameter('useOnesidedShift', useOnesidedShift)
        namedParam.AddParameter('volatilityStructureFilter', volFilter)
        namedParam.AddParameter('referenceInstrument', referenceInstrument)
        namedParam.AddParameter('strikeType', strikeTypeChosen)
        namedParam.AddParameter('groupingSensitive', groupingSensitive)
        if additionalTimeBucket:
            namedParam.AddParameter('additionalTimeBucketStartDate', \
                additionalTimeBucket.StartDateForShift() )
            namedParam.AddParameter('additionalTimeBucketPeakDate', \
                additionalTimeBucket.BucketDate() )
            namedParam.AddParameter('additionalTimeBucketEndDate', \
                additionalTimeBucket.EndDateForShift() )
            namedParam.AddParameter('additionalTimeBucketDateStartsBucket', \
                additionalTimeBucket.DateStartsBucket() )
        else:
            namedParam.AddParameter('additionalTimeBucketStartDate', \
                None )
            namedParam.AddParameter('additionalTimeBucketPeakDate', \
                None )
            namedParam.AddParameter('additionalTimeBucketEndDate', \
                None )
            namedParam.AddParameter('additionalTimeBucketDateStartsBucket', \
                False )

def GenerateStrikeBucketsArray( parameters ):
    volatilityStructure = parameters[acm.FSymbol('volatilityStructure')]
    useVolatilityStructureStrikes = parameters[acm.FSymbol('useVolatilityStructureStrikes')]
    nbrOfStrikes = parameters[acm.FSymbol('strikeBuckets')]
    firstStrike = parameters[acm.FSymbol('firstStrikeValue')]
    offset = parameters[acm.FSymbol('strikeInterval')]
    strikeBuckets = None
    if useVolatilityStructureStrikes:
        strikeBuckets = GenerateStrikeArrayFromVolatilityStructure(volatilityStructure)
    else:
        strikeBuckets = GenerateStrikeArray(nbrOfStrikes, firstStrike, offset)
    return strikeBuckets

def GenerateBuckets( dictResult ):
    try:
        strikeBuckets = GenerateStrikeBucketsArray( dictResult )
        bucketsstring = string.join([str(i) for i in strikeBuckets], ',')
        return bucketsstring
    except Exception as e:
        pass

def GenerateBucketsForUpgradability( dictResult ):
    try:
        bucketsstring = GenerateBuckets( dictResult )
        dictResult.AtPut(acm.FSymbol('strikeBucketsString'), bucketsstring)
    except Exception as e:
        pass

def EndStrikePoint( strike, useOnesidedShift ):
    if useOnesidedShift:
        return float('+inf')
    return strike

def GenerateStrikeBuckets( parameters ):
    useOnesidedShift = parameters[acm.FSymbol('useOneSidedShift')]
    volatilityStructure = parameters[acm.FSymbol('volatilityStructure')]
    useRestBucket = parameters[acm.FSymbol('restBucket')]
    referenceInstrument = parameters[acm.FSymbol('referenceInstrument')]
    strikeTypeChosen = parameters[acm.FSymbol('strikeLadderType')]
    storedStrikeBucketsString = parameters[acm.FSymbol('strikeBucketsString')]
    useVolatilityStructureStrikes = parameters[acm.FSymbol('useVolatilityStructureStrikes')]
    groupingSensitive = parameters[acm.FSymbol('groupingSensitive')]

    if useVolatilityStructureStrikes:
        storedStrikeBucketsString = GenerateBuckets( parameters )
    elif not storedStrikeBucketsString:
        #Upgradability!
        GenerateBucketsForUpgradability( parameters )
        storedStrikeBucketsString = parameters[acm.FSymbol('strikeBucketsString')]

    strikeBuckets = len(storedStrikeBucketsString) and [float(i) for i in string.split(storedStrikeBucketsString, ',')] or []
    names = list(strikeBuckets)
 
    shiftToDate = 0
    if acm.IsHistoricalMode():
        shiftToDate = acm.Time().DateToday()
    volFilter = volatilityStructure and shiftDateFunction(volatilityStructure, shiftToDate)

    length = len(strikeBuckets)
    if length < 2:
        if length == 1:
            strikeBuckets.append( ( parameters[acm.FSymbol('firstStrikeValue')] or 0.0 ) + ( parameters[acm.FSymbol('strikeInterval')] or 0.0 ) )
        elif length == 0:
            strikeBuckets.append( ( parameters[acm.FSymbol('firstStrikeValue')] or 0.0 ) )
            strikeBuckets.append( ( parameters[acm.FSymbol('firstStrikeValue')] or 0.0 ) + ( parameters[acm.FSymbol('strikeInterval')] or 0.0) )

    resultVector = []
    previousStrike = float('-inf')
    if useRestBucket:
        params = acm.FNamedParameters()
        params.Name('Rest<')
        params.UniqueTag('preRest')
        params.AddParameter('strikeStart', previousStrike)
        strike = strikeBuckets[0] - (strikeBuckets[1] - strikeBuckets[0])
        nextStrike = strikeBuckets[0]
        params.AddParameter('strikeMid', strike)
        params.AddParameter('strikeEnd', nextStrike)
        resultVector.append(params)
        previousStrike = strike

    for idx, name in enumerate(names):
        params = acm.FNamedParameters()
        params.Name(str(name))
        params.UniqueTag(str(idx))
        if 0 == idx:
            params.AddParameter('strikeStart', previousStrike)
        else:
            params.AddParameter('strikeStart', strikeBuckets[idx - 1])
        params.AddParameter('strikeMid', strikeBuckets[idx])
        if length - 1 == idx:
            if useRestBucket:
                params.AddParameter('strikeEnd', strikeBuckets[idx] + strikeBuckets[idx] - previousStrike)
            else:
                params.AddParameter('strikeEnd', float('+inf'))
        else:
            params.AddParameter('strikeEnd', strikeBuckets[idx + 1])
        resultVector.append(params)
        previousStrike = strikeBuckets[idx]

    if useRestBucket:
        params = acm.FNamedParameters()
        params.Name('>Rest')
        params.UniqueTag('postRest')
        if length < 2:
            params.AddParameter('strikeStart', strikeBuckets[0])
            params.AddParameter('strikeMid', strikeBuckets[1])
        else:
            params.AddParameter('strikeStart', strikeBuckets[length - 1])
            params.AddParameter('strikeMid', strikeBuckets[length - 1] + strikeBuckets[length - 1] - strikeBuckets[length - 2])
        params.AddParameter('strikeEnd', float('+inf'))
        resultVector.append(params)
    timeBuckets = parameters.At(acm.FSymbol('additionalTimeBuckets'))
    timeBucket = None
    if timeBuckets:
        idx = parameters.At(acm.FSymbol('additionalTimeBucketIdx'))
        timeBucket = timeBuckets.At( idx - 1 )
    for params in resultVector:
        params.AddParameter('strikeEnd', EndStrikePoint( params.Parameter('strikeEnd'), useOnesidedShift ))
    AddGeneralAttributes( resultVector, referenceInstrument, volFilter, timeBucket, strikeTypeChosen, groupingSensitive, useOnesidedShift)

    return resultVector

class VegaDynamicStrikeBucketsDialogBase (FUxCore.LayoutDialog):

    def __init__(self):
        self.m_bindings = None
        self.m_initialData = None
        self.m_volStruct = None
        self.m_volStructControl = None
        self.m_useVolStructStrikes = None
        self.m_strikeLadderType = None
        self.m_strikeBucketsCount = None
        self.m_firstStrike = None
        self.m_strikeBucketsInterval = None
        self.m_referenceInstrument = None
        self.m_referenceInstrumentControl = None
        self.m_includeRestBucket = None
        self.m_includeAdditionalDimension = None
        self.m_additionalTimeBuckets = None
        self.m_additionalTimeBucketsEdit = None
        self.m_additionalTimeBucketsBtn = None
        self.m_additionalTimeBucketIdx = None
        self.m_additionalTimeBucket = None
        self.m_storedTimeBuckets = None
        self.m_strikeBucketsString = None
        self.m_groupingSensitive = None
        self.m_useOneSidedShift = None

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()

    def HandleApply( self ):
        if not self.m_bindings.Validate(True):
            return None
        dictResult = self.m_bindings.GetValuesByName()   
        dictResult.AtPut(acm.FSymbol('additionalTimeBuckets'), self.m_additionalTimeBuckets)
        dictResult.AtPut(acm.FSymbol('referenceInstrument'), self.m_referenceInstrument)
        dictResult.AtPut(acm.FSymbol('volatilityStructure'), self.m_volStruct)
        dictResult.AtPut(acm.FSymbol('strikeLadderType'), str(self.m_strikeLadderType.GetData()))
        try:
            GenerateStrikeBuckets( dictResult )
        except Exception as e:
            acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', str(e), 'Ok', None, None, 'Button1', 'Button1')
            return
        return dictResult

    def CreateToolTip(self):
        self.m_volStructControl.ToolTip( 'The volatility structure filtering the calculation. Only structures that satisifies the filter are shifted.' )
        self.m_strikeLadderType.ToolTip( 'Determines the strike type of the strike buckets.' )
        self.m_strikeBucketsCount.ToolTip( 'The number of strike buckets.' )
        self.m_firstStrike.ToolTip( 'The initial strike bucket value.' )
        self.m_strikeBucketsInterval.ToolTip( 'The distance between the strike buckets.' )
        self.m_referenceInstrumentControl.ToolTip( 'A reference instrument is needed in order to generate absolute strikes from relative' )
        self.m_includeRestBucket.ToolTip( 'Add opening and closing rest strike buckets.' )
        self.m_useVolStructStrikes.ToolTip( 'Generate strike buckets from the selected volatility structure.' )
        self.m_includeAdditionalDimension.ToolTip( 'Use an additional time bucket to define maturity coordinate.' )
        self.m_additionalTimeBucketIdx.ToolTip( 'Which time bucket should be used. First time bucket has index 1. \nNote: Bucket Dates =  Starts Buckets should be used for Rectangle shifts.' )
        self.m_strikeBucketsString.ToolTip( 'The actual strike buckets generated, can be edited.' )
        self.m_groupingSensitive.ToolTip( 'Use portfolio sheet underlying grouper to dynamically find volatility structure' )
        self.m_useOneSidedShift.ToolTip( 'By using one-sided shifts, the numerical behavior of the calculations increases the likelyhood of vega buckets sum being equal to the total vega.' )

    def PopulateVolStructs(self):
        volatilityStructures = acm.FVolatilityStructure.Select('')
        volatilityStructures = volatilityStructures.SortByProperty('Name')
        self.m_volStructControl.Populate(volatilityStructures)

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg

        self.m_additionalTimeBucketsEdit = layout.GetControl('additionalTimeBuckets')
        self.m_additionalTimeBucketsBtn = layout.GetControl('additionalTimeBucketsBtn')

        self.m_fuxDlg.Caption('Vega Strike Buckets Configuration')
        self.m_bindings.AddLayout(layout)
        self.m_strikeBucketsCount.SetValue( 5 )
        self.m_useVolStructStrikes.Enabled( False )
        if self.m_initialData:
            self.m_bindings.SetValuesByName(self.m_initialData)
            if 'referenceInstrument' in self.m_initialData:
                self.m_referenceInstrument = self.m_initialData['referenceInstrument']

        self.m_volStructControl = layout.GetControl('volatilityStructure')
        self.m_volStructControl.AddCallback('Changed', self.OnVolatilityStructureChanged, self)
        self.PopulateVolStructs()

        layout.GetControl('useVolatilityStructureStrikes').AddCallback('Activate', self.OnUseVolStructStrikesChanged, self)
        layout.GetControl('groupingSensitive').AddCallback('Activate', self.OnGroupingSensitiveChanged, self)

        self.m_strikeLadderType = layout.GetControl('strikeLadderType')
        self.m_strikeLadderType.AddCallback('Changed', self.OnChangeStrikeType, self)
        if self.m_initialData and ('strikeLadderType' in self.m_initialData):
            self.m_strikeLadderType.AddItem(acm.FSymbol(self.m_initialData['strikeLadderType']))
            self.m_strikeLadderType.SetData(acm.FSymbol(self.m_initialData['strikeLadderType']))
 
        layout.GetControl('strikeBuckets').AddCallback('Changed', self.OnChangeStrikeBuckets, self)
        layout.GetControl('firstStrikeValue').AddCallback('Changed', self.OnChangeFirstStrikeValue, self)
        layout.GetControl('strikeInterval').AddCallback('Changed', self.OnChangeStrikeInterval, self)
        layout.GetControl('strikeBucketsString').AddCallback('Changed', self.OnChangeStrikeBucketsString, self)

        layout.GetControl('includeAdditionalDimension').AddCallback('Activate', self.OnIncludeAdditionalDimension, self) 

        self.m_referenceInstrumentControl = layout.GetControl('referenceInstrument')
        self.m_okBtn = layout.GetControl('ok')

        self.m_additionalTimeBucketsEdit.Editable( False )
        self.m_additionalTimeBucketsBtn.AddCallback('Activate', self.OnSelectTimeBuckets, self)
        self.m_additionalTimeBucketsEdit.Enabled( False ) 
        self.m_additionalTimeBucketsBtn.Enabled( False ) 
        self.m_additionalTimeBucketIdx.Enabled( False )
        self.m_additionalTimeBucket.Enabled( False )
        self.m_additionalTimeBucket.Editable( False )

        self.m_groupingSensitive.Visible( False )
        self.m_useOneSidedShift.Visible( False )

        self.m_okBtn.Enabled( False )
        self.m_referenceInstrumentControl.Enabled( False )

        layout.GetControl('additionalTimeBucketIdx').AddCallback('Changed', self.OnChangeTimeBucketIdx, self)

        self.CreateToolTip()
        self.UpdateControls()

    def UpdateControls( self ):
        if self.m_additionalTimeBuckets:
            self.m_additionalTimeBucketsEdit.SetData(self.m_additionalTimeBuckets.StringKey())
        else:
            self.m_additionalTimeBucketsEdit.SetData( '' )
        bucketsString = self.m_strikeBucketsString.GetValue()
        self.m_okBtn.Enabled(len(bucketsString) > 0)

    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )

        self.m_useOneSidedShift = \
            self.m_bindings.AddBinder('useOneSidedShift', acm.GetDomain('bool') )
        self.m_strikeBucketsCount = \
            self.m_bindings.AddBinder('strikeBuckets', acm.GetDomain('int'))
        self.m_firstStrike = \
            self.m_bindings.AddBinder('firstStrikeValue', acm.GetDomain('double'))
        self.m_strikeBucketsInterval = \
            self.m_bindings.AddBinder('strikeInterval', acm.GetDomain('double'))
        self.m_useVolStructStrikes = \
            self.m_bindings.AddBinder('useVolatilityStructureStrikes', acm.GetDomain('bool'))
        self.m_includeRestBucket = \
            self.m_bindings.AddBinder('restBucket', acm.GetDomain('bool'))
        self.m_includeAdditionalDimension = \
            self.m_bindings.AddBinder('includeAdditionalDimension', acm.GetDomain('bool'))
        self.m_additionalTimeBucketIdx = \
            self.m_bindings.AddBinder('additionalTimeBucketIdx', acm.GetDomain('int'))
        self.m_additionalTimeBucket = \
            self.m_bindings.AddBinder('additionalTimeBucket', acm.GetDomain('string'))
        self.m_strikeBucketsString = \
            self.m_bindings.AddBinder('strikeBucketsString', acm.GetDomain('string'))
        self.m_groupingSensitive = \
            self.m_bindings.AddBinder('groupingSensitive', acm.GetDomain('bool'))

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        self.m_useOneSidedShift.BuildLayoutPart(b, 'Use One-sided shift')
        b.    AddPopuplist('volatilityStructure', 'Volatility Structure')
        b.    AddInput('referenceInstrument', 'Reference Instrument' )
        self.m_groupingSensitive.BuildLayoutPart(b, 'Volatility Greek Grouping Sensitive')
        b.  EndBox()
        b.BeginVertBox('EtchedIn', 'Strike Buckets')
        self.m_useVolStructStrikes.BuildLayoutPart(b, 'Use Structure Strikes')
        b.    AddOption('strikeLadderType', 'Strike Ladder Type')
        b.  BeginVertBox('EtchedIn', 'Generate Strike Buckets')
        self.m_strikeBucketsCount.BuildLayoutPart(b, 'Strike Buckets Count')
        self.m_firstStrike.BuildLayoutPart(b, 'First Strike Value')
        self.m_strikeBucketsInterval.BuildLayoutPart(b, 'Strike Buckets Interval')
        b.  EndBox()
        self.m_strikeBucketsString.BuildLayoutPart(b, 'Buckets')
        self.m_includeRestBucket.BuildLayoutPart(b, 'Include Rest Buckets')
        b.EndBox()
        b.BeginVertBox('EtchedIn')
        self.m_includeAdditionalDimension.BuildLayoutPart(b, 'Use Maturity Bucket')
        b.  BeginHorzBox('None')
        b.    AddInput('additionalTimeBuckets', 'Time Buckets' )
        b.    AddButton('additionalTimeBucketsBtn', '...', False, True )
        b.  EndBox()
        self.m_additionalTimeBucketIdx.BuildLayoutPart(b, 'Maturity Bucket Index')
        self.m_additionalTimeBucket.BuildLayoutPart(b, 'Time Bucket')
        b.EndBox()
        b.AddSpace(8)
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def Generate(self):
        try:
            dictResult = self.m_bindings.GetValuesByName()
            dictResult[acm.FSymbol('volatilityStructure')] = self.m_volStruct
            bucketsstring = GenerateBuckets( dictResult )
            self.m_strikeBucketsString.SetValue( bucketsstring )
        except Exception as e:
            pass

    def OnVolatilityStructureChanged(self, cd, ud):
        self.m_volStruct = acm.FVolatilityStructure[self.m_volStructControl.GetData()]
        if self.m_volStruct:
            self.m_useVolStructStrikes.Enabled( True )
            self.m_referenceInstrument = self.m_volStruct.ReferenceInstrument()
            self.m_referenceInstrumentControl.SetData(self.m_referenceInstrument.Name() if self.m_referenceInstrument else '')
            self.UpdateStrikeTypeSelection()
        self.m_groupingSensitive.Enabled( self.m_volStruct == None )
        self.Generate()

    def UpdateStrikeGenerationChoices(self):
        useStrikes = self.m_useVolStructStrikes.GetValue()
        self.m_strikeLadderType.Enabled( not useStrikes )
        self.m_strikeBucketsCount.Enabled( not useStrikes )
        self.m_firstStrike.Enabled( not useStrikes )
        self.m_strikeBucketsInterval.Enabled( not useStrikes )

    def OnUseVolStructStrikesChanged(self, cd, ud):
        self.UpdateStrikeGenerationChoices()
        self.Generate()

    def OnGroupingSensitiveChanged(self, cd, ud):
        self.UpdateStrikeGenerationChoices()
        self.m_volStructControl.Enabled( not self.m_groupingSensitive.GetValue() )
        self.Generate()

    def UpdateStrikeTypeSelection(self):
        volStrikeType = None
        strikeTypeChosen = self.m_strikeLadderType.GetData()

        if self.m_volStruct:
            volStrikeType = self.m_volStruct.StrikeType()
        if volStrikeType:
            if not isConnectedStrikeTypes(strikeTypeChosen, volStrikeType):
                self.m_strikeLadderType.SetData( acm.FSymbol(volStrikeType) )
        elif (not self.m_groupingSensitive.GetValue()) or (not acm.FSymbol(strikeTypeChosen) in connectedStrikeTypes) or (not self.m_strikeLadderType.GetData()):
            self.m_strikeLadderType.SetData( acm.FSymbol('Absolute') )

    def OnChangeStrikeType(self, cd, ud):
        self.UpdateStrikeTypeSelection()
        self.Generate()

    def OnChangeStrikeBuckets(self, cd, ud):
        self.Generate()

    def OnChangeFirstStrikeValue(self, cd, ud):
        self.Generate()

    def OnChangeStrikeInterval(self, cd, ud):
        self.Generate()

    def OnIncludeAdditionalDimension(self, cd, ud):
        self.m_additionalTimeBucketsEdit.Enabled( self.m_includeAdditionalDimension.GetValue() ) 
        self.m_additionalTimeBucketsBtn.Enabled( self.m_includeAdditionalDimension.GetValue() ) 
        self.m_additionalTimeBucketIdx.Enabled( self.m_includeAdditionalDimension.GetValue() ) 
        self.m_additionalTimeBucket.Enabled( self.m_includeAdditionalDimension.GetValue() ) 

    def OnSelectTimeBuckets(self, cd, ud):
        timeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_fuxDlg.Shell(), self.m_storedTimeBuckets)
        if timeBuckets:
            self.m_storedTimeBuckets = timeBuckets
            self.m_additionalTimeBuckets = timeBuckets.TimeBuckets()
        self.UpdateControls()

    def OnChangeTimeBucketIdx(self, cd, ud):
        if self.m_additionalTimeBuckets:
            timeBucket = self.m_additionalTimeBuckets[int(self.m_additionalTimeBucketIdx.GetValue()) - 1]
            if timeBucket:
                self.m_additionalTimeBucket.SetValue(timeBucket.StringKey())
        self.UpdateControls()

    def OnChangeStrikeBucketsString(self, cd, ud):
        self.UpdateControls()

