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
            Type:&comma;<xsl:value-of select="current()/Type"/>&lf;
            Name:&comma;<xsl:value-of select="current()/Name"/>&lf;
            Time:&comma;<xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/>&lf;
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
Table name:&comma;<xsl:value-of select="Name"/>&lf;
&comma;
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&comma;
</xsl:for-each>
&lf;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>&comma;
    <xsl:for-each select="Cells/Cell">
        <xsl:value-of select="FormattedData"/>&comma;
    </xsl:for-each>
    &lf;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
