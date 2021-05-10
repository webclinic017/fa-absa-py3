<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns="urn:schemas-microsoft-com:office:spreadsheet"
        xmlns:o="urn:schemas-microsoft-com:office:office"
        xmlns:x="urn:schemas-microsoft-com:office:excel"
        xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
        xmlns:html="http://www.w3.org/TR/REC-html40" >
        
        <xsl:template match="/">

<Workbook
        xmlns="urn:schemas-microsoft-com:office:spreadsheet"
        xmlns:o="urn:schemas-microsoft-com:office:office"
        xmlns:x="urn:schemas-microsoft-com:office:excel"
        xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
        xmlns:html="http://www.w3.org/TR/REC-html40" >
        <DocumentProperties xmlns="urn:schemas-microsoft-com:office:office">
                <Author></Author>
                <LastAuthor></LastAuthor>
                <Created></Created>
                <Company>Absa</Company>
                <Version>1.0000</Version>
        </DocumentProperties>
        <Styles>
                <Style ss:ID="Default" ss:Name="Normal">
                        <Alignment ss:Vertical="Top" />
                        <Borders>
                                <Border ss:Position="Left" ss:LineStyle="None" />
                                <Border ss:Position="Bottom" ss:LineStyle="None" />
                                <Border ss:Position="Top" ss:LineStyle="None" />
                                <Border ss:Position="Right" ss:LineStyle="None" />
                        </Borders>
                        <Font ss:FontName="Arial" ss:size="10" />
                        <Interior ss:Color="#FFFFFF" ss:Pattern="Solid" />
                        <NumberFormat />
                        <Protection />
                </Style>
                <Style ss:ID="value_general" ss:Name="Value - general">
                        <Alignment ss:Horizontal="Right" />
                        <Font ss:FontName="Arial" ss:Size="10" />
                        <Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
                </Style>
                <Style ss:ID="numeric_value_general" ss:Name="Numeric value general">
                        <Alignment ss:Horizontal="Right" />
                        <Font ss:FontName="Arial" ss:Size="10" />
                        <Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
                        <NumberFormat ss:Format="#'###'###'###'###'##0.00" />
                </Style>
                <Style ss:ID="numeric_value_int" ss:Name="Numeric value int">
                        <Alignment ss:Horizontal="Right" />
                        <Font ss:FontName="Arial" ss:Size="10" />
                        <Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
                        <NumberFormat ss:Format="#'###'###'###'###'##0" />
                </Style>
                <Style ss:ID="report_title" ss:Name="Report title">
                        <Font ss:FontName="Arial" ss:Size="14" ss:Bold="1" />
                        <Interior ss:Color="#FFFFFF" ss:Pattern="Solid" />
                </Style>
                <Style ss:ID="columns_legend" ss:Name="Columns legend">
                        <Alignment ss:Horizontal="Center" />
                        <Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
                        <Interior ss:Color="#CCCCCC" ss:Pattern="Solid" />
                </Style>
                <Style ss:ID="client_title" ss:Name="Client title">
                        <Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
                        <Interior ss:Color="#C2D69A" ss:Pattern="Solid" />
                </Style>
        </Styles>
        <Worksheet ss:Name="No Match">
                <xsl:call-template name="GenerateOverview">
                        <xsl:with-param name="pmatched" select="0" />
                </xsl:call-template>
        </Worksheet>
        <Worksheet ss:Name="Match">
                <xsl:call-template name="GenerateOverview">
                        <xsl:with-param name="pmatched" select="1" />
                </xsl:call-template>
        </Worksheet>
</Workbook>

        </xsl:template>

        <xsl:template name="GenerateOverview">
                <xsl:param name="pmatched" />
                <Table>
                        <Column ss:Index="1" ss:Width="100"/>
                        <Column ss:Index="2" ss:Width="200"/>
                        <Column ss:Index="3" ss:Width="80"/>
                        <Column ss:Index="4" ss:Width="200"/>
                        <Column ss:Index="5" ss:Width="80"/>
                        <Column ss:Index="6" ss:Width="200"/>
                        <Row ss:Index="2">
                                <xsl:choose>
                                        <xsl:when test="$pmatched = 0">
                                                <Cell ss:MergeAcross="2" ss:StyleID="report_title">
                                                        <Data ss:Type="String">NON-MATCHED</Data>
                                                </Cell>
                                        </xsl:when>
                                        <xsl:when test="$pmatched = 1">
                                                <Cell ss:MergeAcross="2" ss:StyleID="report_title">
                                                        <Data ss:Type="String">MATCHED</Data>
                                                </Cell>
                                        </xsl:when>
                                </xsl:choose>
                        </Row>
                        <Row>
                        </Row>
                        <Row>
                                <xsl:for-each select="/report/columns">
                                        <Cell ss:StyleID="columns_legend">
                                                <Data ss:Type="String"></Data>
                                        </Cell>
                                        <xsl:for-each select="@*">
                                                <Cell ss:StyleID="columns_legend">
                                                        <Data ss:Type="String"><xsl:value-of select="name()"/></Data>
                                                </Cell>
                                        </xsl:for-each>
                                </xsl:for-each>
                        </Row>
                        <xsl:for-each select="/report/client">
                                <xsl:choose>
                                        <xsl:when test="@matched = $pmatched">
                                                <Row>
                                                </Row>
                                                <Row>
                                                        <Cell ss:StyleID="client_title">
                                                                <Data ss:Type="String"><xsl:value-of select="@name"/></Data>
                                                        </Cell>
                                                </Row>
                                                <xsl:for-each select="entity">
                                                <Row>
                                                        <Cell/>
                                                        <xsl:for-each select="@*" >
                                                                <xsl:choose>
                                                                        <xsl:when test="contains(name(),'_str')">
                                                                                <Cell ss:StyleID="value_general">
                                                                                        <Data ss:Type="String"><xsl:value-of select="."/></Data>
                                                                                </Cell>
                                                                        </xsl:when>
                                                                        <xsl:when test="contains(name(),'_d')">
                                                                                <Cell ss:StyleID="numeric_value_general">
                                                                                        <Data ss:Type="Number"><xsl:value-of select="."/></Data>
                                                                                </Cell>
                                                                        </xsl:when>
                                                                        <xsl:when test="contains(name(),'_int')">
                                                                                <Cell ss:StyleID="numeric_value_int">
                                                                                        <Data ss:Type="Number"><xsl:value-of select="."/></Data>
                                                                                </Cell>
                                                                        </xsl:when>
                                                                </xsl:choose>
                                                        </xsl:for-each>
                                                </Row>
                                                </xsl:for-each>
                                        </xsl:when>
                                </xsl:choose>
                        </xsl:for-each>
                </Table>
        </xsl:template>
</xsl:stylesheet>

