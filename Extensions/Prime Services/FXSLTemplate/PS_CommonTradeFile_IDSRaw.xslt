#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: sheet columns/tradesheet

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<!-- Constants -->
	<xsl:strip-space elements="*"/>
	<xsl:variable name="comma" select="string(',')"/>
	<xsl:variable name="doubleQuote" select="string('&#x22;')"/>
	<xsl:variable name="eoln">
		<xsl:text>&#13;&#10;</xsl:text>
	</xsl:variable>
	<xsl:variable name="pricefmt" select="string('#0.000000')"/>
	<xsl:variable name="qtyfmt" select="string('#0')"/>
	<xsl:variable name="emptyString" select="string('')"/>
	<!-- Main Entry Point -->
	<xsl:template match="PRIMEReport">
		<!-- Apply the table template -->
		<xsl:apply-templates select="ReportContents/Table"/>
	</xsl:template>
	<!-- Table template -->
	<xsl:template match="Table">
		<xsl:value-of select="concat('TradeNumber',$comma)"/>
		<xsl:for-each select="Columns/Column">
		  <xsl:value-of select="Label"/>
		  <xsl:if test="position() != last()">
			<xsl:value-of select="$comma" />
		  </xsl:if>
		</xsl:for-each>
		<xsl:value-of select="$eoln" />

		<xsl:apply-templates select="Rows/Row"/>
	</xsl:template>
	<!-- Template for writing out each data row -->
	<xsl:template match="Row">
		<xsl:value-of select="Label"/>
		<xsl:value-of select="$comma" />
		<xsl:for-each select="Cells/Cell">
		  <xsl:value-of select="translate(FormattedData,',','')"/>
		  <xsl:if test="position() != last()">
			<xsl:value-of select="$comma" />
		  </xsl:if>
		</xsl:for-each>
		<xsl:value-of select="$eoln" />
		<xsl:apply-templates select="Rows/Row"/>
    </xsl:template>

</xsl:stylesheet>


