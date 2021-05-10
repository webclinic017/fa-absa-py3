<?xml version='1.0'?>
<!DOCTYPE stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
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
TrdNbr&comma;HVal&cr;&nl;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
        <xsl:if test="Label &gt; 0">
            <xsl:value-of select="Label"/>&comma;
            <xsl:for-each select="Cells/Cell">
                <xsl:value-of select="RawData"/>
            </xsl:for-each>
            &cr;&nl;
        </xsl:if>
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
