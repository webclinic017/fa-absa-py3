#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates xls

<?xml version="1.0" encoding="utf-8"?>
<!-- 
XML to XML Spreadsheet template with support for multiple sheets 
AUTHOR: Lukas Paluzga
DATE: 31/10/2012
UPDATE: 18/04/2013 Conicov Andrei
-->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xmlns="urn:schemas-microsoft-com:office:spreadsheet"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:x="urn:schemas-microsoft-com:office:excel"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes"><![CDATA[
<?mso-application progid="Excel.Sheet"?>
]]></xsl:text>
        <Workbook>
            <x:ExcelWorkBook>
                <x:ActiveSheet>
                    <xsl:value-of select="count(/MultiReport/PRIMEReport)"/>
                </x:ActiveSheet>
            </x:ExcelWorkBook>

            <Styles>
                <Style ss:ID="sHeader">
                    <Font ss:Bold="1"/>
                </Style>

                <Style ss:ID="sNumberFixed">
                    <NumberFormat ss:Format="Standard"/>
                </Style>
                
                <Style ss:ID="sNumber">
                    <NumberFormat ss:Format="#,##0"/>
                </Style>
                
            </Styles>

            <!-- Data sheets -->
            <xsl:apply-templates select="PRIMEReport | MultiReport/PRIMEReport" />

            <!-- Settings -->
            <Worksheet ss:Name="_">
                <xsl:call-template name="settings"/>
            </Worksheet>
        </Workbook>
    </xsl:template>
    
    <!-- Data sheet -->
    <xsl:template match="PRIMEReport">
        <xsl:element name="Worksheet">
            <!-- The excel sheet title can be at most 31 chars long -->
            <xsl:attribute name="ss:Name"><xsl:value-of select="substring(Name,1,31)"/></xsl:attribute>
            <xsl:apply-templates select="ReportContents/Table" />
        </xsl:element>
    </xsl:template>

    <!-- Data table -->
    <xsl:template match="Table">
        <!-- This ugly part computes the indendation of data cells. If you know how to do it better email me. -->
        <xsl:variable name="maxDepth">
            <xsl:choose>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">10</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">9</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">8</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">7</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">6</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows/Row">5</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row/Rows/Row">4</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row/Rows/Row">3</xsl:when>
                <xsl:when test="Rows/Row/Rows/Row">2</xsl:when>
                <xsl:when test="Rows/Row">1</xsl:when>
                <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <Table>
            
            <!-- Column group labels -->
            <Row>
                <!-- Indent the column labels -->
                <xsl:call-template name="cellPad">
                    <xsl:with-param name="cellCount" select="$maxDepth" />
                </xsl:call-template>

                <xsl:for-each select="Columns/Column">

                    <Cell ss:StyleID="sHeader">
                        <!-- Display group label only once -->
                        <!-- Comment the if statement in order to display repeating column titles -->
                        <!--<xsl:if test="not (preceding-sibling::Column[1])or (GroupLabel/text() != preceding-sibling::Column[1]/GroupLabel/text()) ">-->
                            <Data ss:Type="String">
                                <xsl:value-of select="GroupLabel" />
                            </Data>
                        <!--</xsl:if>-->
                    </Cell>
                    
                </xsl:for-each>
            </Row>
            
            <!-- Column labels -->
            <Row>
                <!-- Indent the column labels -->
                <xsl:call-template name="cellPad">
                    <xsl:with-param name="cellCount" select="$maxDepth" />
                </xsl:call-template>
                
                <xsl:for-each select="Columns/Column">
                    <Cell ss:StyleID="sHeader">
                        <Data ss:Type="String">
                            <xsl:value-of select="Label" />
                        </Data>
                    </Cell>
                </xsl:for-each>
            </Row>
                     
            <!-- Data rows -->
            <xsl:for-each select="Rows/Row">
                <xsl:apply-templates select=".">
                    <xsl:with-param name="maxDepth" select="$maxDepth" />
                    <xsl:with-param name="currentDepth" select="0" />
                </xsl:apply-templates>
            </xsl:for-each>
        </Table>
    </xsl:template>

    <!-- Data row -->
    <xsl:template match="Row">
        <xsl:param name="maxDepth" />
        <xsl:param name="currentDepth" />
        
        <Row>
            <!-- Pad before row label -->
            <xsl:call-template name="cellPad">
                <xsl:with-param name="cellCount" select="$currentDepth" />
            </xsl:call-template>

            <!-- Row label -->
            <Cell>
                <Data ss:Type="String">
                    <xsl:value-of select="Label"/>
                </Data>
            </Cell>

            <!-- Pad after row label -->
            <xsl:call-template name="cellPad">
                <xsl:with-param name="cellCount" select="$maxDepth - $currentDepth - 1" />
            </xsl:call-template>

            <!-- Row data -->
            <xsl:for-each select="Cells/Cell">
                <xsl:apply-templates  select=".">
                    <xsl:with-param name="cell" select="." />
                </xsl:apply-templates>
            </xsl:for-each>
        </Row>
      
        <!-- Process all child rows -->
        <xsl:apply-templates select="Rows/Row">
            <xsl:with-param name="currentDepth" select="$currentDepth +1" />
            <xsl:with-param name="maxDepth" select="$maxDepth" />
        </xsl:apply-templates>
    </xsl:template>

    <!-- Data cell -->
    <xsl:template match="Cell">
        <xsl:variable name="cellType">
            <xsl:choose>
                <xsl:when test="string(number(RawData)) != 'NaN'">Number</xsl:when>
                <xsl:otherwise>String</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <Cell>
            <xsl:if test="$cellType = 'Number'">
            	<xsl:if test="contains(FormattedData/text(), '.')">
                	<xsl:attribute name="ss:StyleID">sNumberFixed</xsl:attribute>
                </xsl:if>
                <xsl:if test="not(contains(FormattedData/text(), '.'))">
                	<xsl:attribute name="ss:StyleID">sNumber</xsl:attribute>
                </xsl:if>
            </xsl:if>

            <xsl:if test="FormattedData != ''">
                <xsl:element name="Data">
                    <xsl:attribute name="ss:Type">
                        <xsl:value-of select="$cellType"/>
                    </xsl:attribute>
                    <xsl:value-of select="FormattedData"/>
                </xsl:element>
            </xsl:if>
        </Cell>
    </xsl:template>

    <!-- Padding by empty cells -->
    <xsl:template name="cellPad">
        <xsl:param name="cellCount" />
        <xsl:if test="$cellCount &gt; 0">
            <Cell></Cell>
            <xsl:call-template name="cellPad">
                <xsl:with-param name="cellCount" select="$cellCount - 1" />
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

    <!-- Report settings sheet -->
    <xsl:template name="settings">
        <Table>
            <Row ss:StyleID="sHeader">
                <Cell></Cell>
                <Cell>
                    <Data ss:Type="String">Time</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">Start Date</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">Custom Start Date</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">End Date</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">Custom End Date</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">Use MtM Price Today</Data>
                </Cell>
                <Cell>
                    <Data ss:Type="String">Trade Filter Match Choice</Data>
                </Cell>
            </Row>
            <xsl:for-each select="//PRIMEReport">
                <Row>
                    <Cell ss:StyleID="sHeader">
                        <Data ss:Type="String">
                            <xsl:value-of select="Name" />
                        </Data>
                    </Cell>
                    <Cell>
                        <Data ss:Type="String">
                            <xsl:value-of select="Time"/>
                        </Data>
                    </Cell>
                    <xsl:apply-templates select="ReportContents/Table/Settings/Groups/Group[Label/text()='Profit/Loss']" mode="settingsGroup" />
                </Row>
            </xsl:for-each>
        </Table>
    </xsl:template>

    <!-- Report settings sheet data -->
    <xsl:template match="Group" mode="settingsGroup">
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='StartDate']/FormattedData"/>
            </Data>
        </Cell>
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='Custom StartDate']/FormattedData"/>
            </Data>
        </Cell>
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='EndDate']/FormattedData"/>
            </Data>
        </Cell>
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='Custom EndDate']/FormattedData"/>
            </Data>
        </Cell>
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='Use MtM Price Today']/FormattedData"/>
            </Data>
        </Cell>
        <Cell>
            <Data ss:Type="String">
                <xsl:value-of select="Cell[preceding-sibling::Column[1]/Label/text()='Trade Filter Match Choice']/FormattedData"/>
            </Data>
        </Cell>
    </xsl:template>
</xsl:stylesheet>
