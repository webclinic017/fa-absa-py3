#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/secondary templates xls

<?xml version='1.0'?>
<!DOCTYPE stylesheet [
  <!ENTITY tab "<xsl:text>&#9;</xsl:text>">
  <!ENTITY cr "<xsl:text>&#13;</xsl:text>">
  <!ENTITY nl "<xsl:text>&#10;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
<xsl:apply-templates select="PRIMEReport/ReportContents/Table"/>
</xsl:template>
<xsl:template match="Table">
Trdnbr&tab;Instrument&tab;Price&tab;Used Price End&tab;Qty&tab;Acquire Day&tab;Portfolio&tab;TradeCurr&tab;Fees&tab;Status&tab;Counterparty&tab;Trader&tab;BS&tab;Execution&tab;Isin
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>
<xsl:template match="Row">
        <xsl:if test="Label &gt; 0">
                <xsl:value-of select="Label"/>
                        <xsl:for-each select="Cells/Cell">&tab;
                                <xsl:value-of select="FormattedData"/>
                        </xsl:for-each>
                        &nl;
        </xsl:if>
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>
</xsl:stylesheet>
