#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version='1.0'?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="ISO-8859-1"/>
  <xsl:strip-space elements="*"/>
  <xsl:param name="comma" select="string('&#x9;')" />
  <xsl:param name="eoln" select="string('&#xD;&#xA;')" />

  <xsl:template match="/">
    <xsl:apply-templates select="PRIMEReport/ReportContents/Table"/>
  </xsl:template>
  <xsl:template match="Table">
    <xsl:value-of select="'Trade'"/>
    <xsl:value-of select="$comma"/>
    <xsl:for-each select="Columns/Column">
      <xsl:value-of select="Label"/>
      <xsl:if test="position() != last()">
        <xsl:value-of select="$comma" />
      </xsl:if>
    </xsl:for-each>
    <xsl:value-of select="$eoln" />    
    <xsl:apply-templates select="Rows/Row"/>
  </xsl:template>

  <xsl:template match="Row">    
    <xsl:value-of select="Label"/>
    <xsl:value-of select="$comma" />
    <xsl:for-each select="Cells/Cell">      
      <xsl:value-of select="translate(RawData,',','')"/>
      <xsl:if test="position() != last()">
        <xsl:value-of select="$comma" />
      </xsl:if>
    </xsl:for-each>
    <xsl:value-of select="$eoln" />
    <xsl:apply-templates select="Rows/Row"/>
  </xsl:template>

</xsl:stylesheet>
