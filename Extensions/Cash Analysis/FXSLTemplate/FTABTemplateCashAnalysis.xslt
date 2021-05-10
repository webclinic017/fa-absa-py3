#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates xls

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<xsl:strip-space elements="*"/>
	<xsl:variable name="comma" select="string(',')"/>
	<xsl:variable name="tab" select="string('&#9;')"/>
	<xsl:variable name="eoln">
		<xsl:text>&#13;</xsl:text>
	</xsl:variable>
	
	<xsl:template match="PRIMEReport">
		<xsl:value-of select="'Type:'"/><xsl:value-of select="$tab"/><xsl:value-of select="Type"/><xsl:value-of select="$eoln"/>
		<xsl:value-of select="'Name:'"/><xsl:value-of select="$tab"/><xsl:value-of select="Name"/><xsl:value-of select="$eoln"/>
		<xsl:value-of select="'Time:'"/><xsl:value-of select="$tab"/><xsl:value-of select="Time"/><xsl:value-of select="$eoln"/>
		<xsl:apply-templates select="ReportContents/Table"/>
		<xsl:apply-templates select="ReportContents/Table/Rows/Row"/>
		<xsl:value-of select="$eoln"/>
	</xsl:template>

	<xsl:template match="Table">
		<xsl:value-of select="'Table Name:'"/><xsl:value-of select="$tab"/><xsl:value-of select="Name"/><xsl:value-of select="$eoln"/>
		<xsl:value-of select="$tab"/>
		<xsl:for-each select="Columns/Column">
			<xsl:value-of select="Label"/><xsl:value-of select="$tab"/>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template match="Row">
		<xsl:variable name="rowLabel" select="Label"/>
		<xsl:choose>
			<xsl:when test="$rowLabel!='Reset'">
                                                                <xsl:value-of select="$eoln"/>
				<xsl:value-of select="Label"/>
                                                                <xsl:value-of select="$tab"/>
				<xsl:for-each select="Cells/Cell">
					<xsl:value-of select="RawData"/>
					<xsl:value-of select="$tab"/>
				</xsl:for-each>
				<xsl:apply-templates select="Rows/Row"/>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
</xsl:stylesheet>
