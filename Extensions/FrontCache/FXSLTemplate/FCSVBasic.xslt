<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY pipe "<xsl:text>|</xsl:text>">
  <!ENTITY newline "<xsl:text>&#xa;</xsl:text>">
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
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&pipe;
</xsl:for-each>
&newline;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>&pipe;
    <xsl:for-each select="Cells/Cell">
      <xsl:value-of select="translate(RawData,',[]','')"/>&pipe;
    </xsl:for-each>
&newline;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<!-- Template for replacing text -->
<xsl:template name="formatData">
  <xsl:param name="inputData"/>
    <xsl:choose>
      <xsl:when test="$inputData = '[]'">
        <xsl:value-of select="''"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$inputData"/>
      </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
