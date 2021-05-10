#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/style sheets

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
  <!ENTITY cr "<xsl:text>&#13;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
        
<!-- Reports -->
    <xsl:for-each select="//PRIMEReport">                                                                                                 
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
<xsl:value-of select="'Instrument'"/>&comma;
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&comma;
</xsl:for-each>
&cr;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>&comma;
    <xsl:for-each select="Cells/Cell">
        <xsl:value-of select="RawData"/>&comma;
    </xsl:for-each>
    &cr;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
