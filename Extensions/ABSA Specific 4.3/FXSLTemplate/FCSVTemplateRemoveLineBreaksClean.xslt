#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
  <!ENTITY lf "<xsl:text>&#10;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
        
<!-- Reports -->
    <xsl:for-each select="//PRIMEReport">                         
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&comma;
</xsl:for-each>
&lf;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:for-each select="Cells/Cell">
        <xsl:call-template name="CellData" />&comma; 
    </xsl:for-each>
    &lf;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template name="CellData">
        <xsl:choose>
            <xsl:when test="RawData">
                <xsl:value-of select="translate(RawData,',&#9;&#10;', '')"/>
            </xsl:when>
            <xsl:when test="FormattedData">
                <xsl:value-of select="translate(FormattedData,',&#9;&#10;', '')"/>
            </xsl:when>
            <xsl:when test="DefaultData">
                <xsl:choose>
                        <xsl:when test="ValueType">
                                <xsl:text>#</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                                <xsl:value-of select="translate(DefaultData,',&#9;&#10;', '')"/>
                        </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                  <xsl:message terminate="yes"><xsl:text>No dataformat turned on</xsl:text></xsl:message>
            </xsl:otherwise>
        </xsl:choose>
</xsl:template>

</xsl:stylesheet>
