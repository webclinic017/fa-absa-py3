#grouping: aef reporting/secondary templates

<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<xsl:strip-space elements="*"/>
	<xsl:param name="comma" select="string(',')" />
	<xsl:param name="eoln" select="string('&#xD;&#xA;')" />

	<!-- Replace all template. Used for backslashing commas -->
	<xsl:template name="string-replace-all">
		<xsl:param name="text" />
		<xsl:param name="replace" />
		<xsl:param name="by" />
		<xsl:choose>
			<xsl:when test="contains($text, $replace)">
				<xsl:value-of select="substring-before($text, $replace)" />
				<xsl:value-of select="$by" />
				<xsl:call-template name="string-replace-all">
					<xsl:with-param name="text" select="substring-after($text, $replace)" />
					<xsl:with-param name="replace" select="$replace" />
					<xsl:with-param name="by" select="$by" />
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text" />
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="/">
		<xsl:apply-templates select="PRIMEReport/ReportContents/Table"/>
	</xsl:template>

	<!-- Remove parent row's data - Row with trade filter / portfolio -->
	<xsl:template match="Table / Rows / Row / Label" />
	<xsl:template match="Table / Rows / Row / RowId" />
	<xsl:template match="Table / Rows / Row / Cells" />

	<!-- Remove parent Row element but keep the content -->
	<xsl:template match="Table / Rows / Row">
		<xsl:apply-templates select="node()|@*"/>
	</xsl:template>

	<!-- Remove parent Rows element but keep the content -->
	<xsl:template match="Table / Rows">
		<xsl:apply-templates select="node()|@*"/>
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
                                                <xsl:call-template name="string-replace-all">
                                                        <xsl:with-param name="text" select="RawData" />
                                                        <xsl:with-param name="replace" select="','" />
                                                        <xsl:with-param name="by" select="'\,'" />
			</xsl:call-template>
			<!-- <xsl:value-of select="translate(RawData,',[]','')"/> -->
			<xsl:if test="position() != last()">
				<xsl:value-of select="$comma" />
			</xsl:if>
		</xsl:for-each>
		<xsl:value-of select="$eoln" />
		<xsl:apply-templates select="Rows/Row"/>
	</xsl:template>

	<!-- Remove [] from input data -->
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
