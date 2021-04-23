
import FXMLReportWriter

class CalculatedValueXMLWriter(object):

    def __init__(self, reportName):
        self.m_reportName = reportName
        self.m_values = {}
        self.m_positionKeyTable = {}
        self.m_positionInfoTable = {}
        
    def addColumn(self, info, ID):
        pass

    def addRootPosition(self, info, ID):
        pass

    def positionKey(self, info):
        if info.parentInfoID:
            positionKey = self.positionKey(self.m_positionInfoTable[info.parentInfoID]) + '|' + info.name
        else:
            positionKey = info.acmDomainName + '|' + info.name
        return positionKey

    def addPosition(self, info, ID):
        self.m_positionInfoTable[ID] = info
        self.m_positionKeyTable[ID] = self.positionKey(info)

    def addResult(self, posInfoID, storedSpecName, calculationInfos):
        if len(calculationInfos) > 0:
            keyString = self.m_positionKeyTable[posInfoID]
            
            forPosId = self.m_values.setdefault( keyString, {} )
            try:
                for calcInfo in calculationInfos:
                    if calcInfo.values is not None:
                        if len(calcInfo.projectionCoordinates) > 0:
                            forCalcId = forPosId.setdefault( storedSpecName, {} )
                            forCalcId[ str(calcInfo.projectionCoordinates) ] = calcInfo.values
                        else:
                            forPosId[ storedSpecName ] = calcInfo.values
            except Exception as e:
                print (e)
        
    def CreateRows( self, dictionary, writer, path ):
        xRows = writer.Rows()

        for key in dictionary:
            xRow = writer.Row()
            writer.Label( key ).done()
            writer.RowId( path + "/" + key ).done()
            val = dictionary[ key ]
            if isinstance(val, dict):
                if len(val) > 0:
                    self.CreateRows( val, writer, path + "/" + key )
            else:
                xCells = writer.Cells()
                xCell = writer.Cell()
                value = None
                try:
                    value = float( val )
                except:
                    value = val
                writer.RawData( value ).done()
                writer.FormattedData( value ).done()
                    
                xCell.done()
                xCells.done()
            xRow.done()
        xRows.done()
    
    def CreateReport(self):
        writer, strBuf = FXMLReportWriter.FXMLReportWriter.make_iostring_writer()
        primeReport = writer.PRIMEReport()
        writer.Name( self.m_reportName ).done()
        writer.Type( "Calc Report" ).done()
        writer.ReportContents()
        table = writer.Table()
        writer.Type( "Calculations" ).done()
        writer.NumberOfColumns(1).done()
        xcolumns = writer.Columns()

        xCol = writer.Column()
        writer.ColumnId( "Value" ).done()
        writer.Label( "Value" ).done()
        xCol.done()

        xcolumns.done()
    
        self.CreateRows( self.m_values, writer, "" )
    
        writer.done()
        return writer, strBuf

    def XmlText( self ):
        writer, strbuf = self.CreateReport()
        return strbuf.getvalue()
