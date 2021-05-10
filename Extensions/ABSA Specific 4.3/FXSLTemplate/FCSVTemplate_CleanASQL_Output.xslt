#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/secondary templates xls

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
    <xsl:for-each select="Columns/Column">
      <xsl:value-of select="Label"/>
      <xsl:value-of select="$comma"/>
    </xsl:for-each>
    <xsl:value-of select="$eoln" />
    <xsl:apply-templates select="Rows/Row"/>
  </xsl:template>

  <xsl:template match="Row">
    <xsl:for-each select="Cells/Cell">
         <xsl:choose>
         <xsl:when test="not(contains(RawData, 'could not be'))">
           <xsl:value-of select="translate(RawData,',[]','')"/>
           <xsl:value-of select="$comma"/>
         </xsl:when>
         <xsl:otherwise><xsl:value-of select="$comma"/></xsl:otherwise>
       </xsl:choose>

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
