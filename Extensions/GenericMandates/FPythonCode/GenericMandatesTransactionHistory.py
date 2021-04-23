import acm


PREFIX = "TMP2/"


def GetMessagesFromBlob(blob):
    # Read AMBA messages from text file and return an array containing messages in text format
    messages = re.findall(r"\[MESSAGE\].*?\[/MESSAGE\]", fileContent, flags=re.DOTALL)
    return messages


def GetAcmObjectFromMessage(message):
    # Convert AMBA text message to ACM object
    acmObject = acm.AMBAMessage.CreateObjectFromMessage(message)
    # acmObject = acm.AMBAMessage.CreateCloneFromMessage(message)
    return acmObject


def GetTradeAMBA(trade):
    gen = acm.FAMBAMessageGenerator()

    newTrade = acm.FTrade()
    newTrade.Apply(trade.Clone())
    newTrade.OptionalKey('')
    newTrade.ConnectedTrdnbr(None)
    newTrade.ContractTrdnbr(None)
    newTrade.TrxTrade(None)
    newTrade.MirrorTrade(None)
    message = gen.Generate(newTrade)

    trdMessage = message.FindMessages("TRADE")
    trdMessage[0].RemoveKeyString("INSADDR.INSID")
    trdMessage[0].AtPut("INSADDR.INSID", "%s%s" % (PREFIX, trade.Instrument().Name()))

    return "%s" % message


def GetInstrumentAMBA(trade):
    gen = acm.FAMBAMessageGenerator()
    newIns = acm.DealCapturing.CreateNewInstrument('%s' % trade.Instrument().InsType())
    message = gen.Generate(trade.Instrument().Clone())

    insMessage = message.FindMessages('INSTRUMENT')
    insMessage[0].RemoveKeyString("INSID")
    insMessage[0].AtPut("INSID", "%s%s" % (PREFIX, trade.Instrument().Name()))
    return "%s" % message


def CreateTextObject(trade):
    blob = GetInstrumentAMBA(trade)
    blob += GetTradeAMBA(trade)

    if not acm.FCustomTextObject.Select('name="Violation%s"' % trade.Oid()):
        to = acm.FCustomTextObject()
        to.Name('Violation%s' % trade.Oid())
        to.Text(blob)
        to.Commit()
    else:
        print('Violation record already exists.')


def GetTradeFromViolation(trade):
    instrument = None
    trade = None
    blob = acm.FCustomTextObject['Violation%s' % trade.Oid()]
    messages = GetMessagesFromBlob(blob.Text())

    for message in messages:
        print('Processing AMBA message')

        obj = getAcmObjectFromMessage(message)

        # Trade Message
        if obj.ClassName().AsString() == 'FTrade':
            obj.Instrument(newIns)
            trade = obj

        # Instrument Message
        if obj.ClassName().AsString() == 'FBond':
            instrument = obj

    return trade, instrument


