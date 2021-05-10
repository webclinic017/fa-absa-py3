#grouping: aef reporting/secondary templates

<?xml version='1.0'?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="ISO-8859-1"/>
  <xsl:strip-space elements="*"/>
  <xsl:param name="tabChar" select="string('&#x9;')" />
  <xsl:param name="comma" select="string('&#x2c;')" />
  <xsl:param name="eoln" select="string('&#xD;&#xA;')" />

  <xsl:template match="/">
    <xsl:apply-templates select="PRIMEReport/ReportContents/Table"/>
  </xsl:template>
  <xsl:template match="Table">
    <xsl:value-of select="'Trade'"/>
    <xsl:value-of select="$tabChar"/>
    <xsl:for-each select="Columns/Column">
      <xsl:value-of select="Label"/>
      <xsl:if test="position() != last()">
        <xsl:value-of select="$tabChar" />
      </xsl:if>
    </xsl:for-each>
    <xsl:value-of select="$eoln" />    
    <xsl:apply-templates select="Rows/Row"/>
  </xsl:template>

  <xsl:template match="Row">    
    <xsl:value-of select="Label"/>
    <xsl:value-of select="$tabChar" />
    <xsl:for-each select="Cells/Cell"> 
         <xsl:choose>
                <xsl:when test="DefaultData">
                        <xsl:call-template name="formatData">
                                <xsl:with-param name="inputData" select="DefaultData"/>
                        </xsl:call-template>
                </xsl:when>
                <xsl:when test="FormattedData">
                        <xsl:call-template name="formatData">
                                <xsl:with-param name="inputData" select="FormattedData"/>
                        </xsl:call-template>
                </xsl:when>
                <xsl:when test="not(ValueType) and RawData">
                        <xsl:call-template name="formatData">
                                <xsl:with-param name="inputData" select="RawData"/>
                        </xsl:call-template>
                </xsl:when>
                <xsl:when test="RawData">
                        <!-- Some kind of error occurred -->
                        <xsl:text>ERROR</xsl:text>
                </xsl:when>
        </xsl:choose>
      
      <xsl:if test="position() != last()">
        <xsl:value-of select="$tabChar" />
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
											<xsl:value-of select="translate($inputData,$comma,'')" />
					</xsl:otherwise>
			</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
