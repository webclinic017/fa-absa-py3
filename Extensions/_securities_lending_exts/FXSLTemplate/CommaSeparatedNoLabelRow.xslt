#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/secondary templates txt

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
  <!ENTITY lf "<xsl:text>&#10;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
    <xsl:for-each select="//PRIMEReport">                         
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:for-each select="Cells/Cell">
        <xsl:variable name="formattedData" select="FormattedData"/>
        <xsl:value-of select="translate($formattedData,',','.')"/>
        <xsl:if test="position() != last()">&comma;</xsl:if>
    </xsl:for-each>
    &lf;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
