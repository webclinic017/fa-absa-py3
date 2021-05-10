<?xml version='1.0'?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="ISO-8859-1"/>
  <xsl:strip-space elements="*"/>
  <xsl:param name="comma" select="string(',')" />
  <xsl:param name="eoln" select="string('&#xD;&#xA;')" />

  <xsl:template match="/">
    <xsl:apply-templates select="PRIMEReport/ReportContents/Table"/>
  </xsl:template>


  <xsl:template match="Table">
    <xsl:value-of select="'Instrument'"/>
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
      <xsl:value-of select="translate(RawData,',[]','')"/>
      <xsl:if test="position() != last()">
        <xsl:value-of select="$comma" />
      </xsl:if>
    </xsl:for-each>
    <xsl:value-of select="$eoln" />
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
