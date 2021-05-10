#grouping: aef reporting/secondary templates

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY delimiter "<xsl:text>&#161;</xsl:text>">
  <!ENTITY cr "<xsl:text>&#13;</xsl:text>">]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:variable name="NumberOfRows" select="count(//Rows/Row/Rows/Row/Rows/Row)"/>

<xsl:template match="/">
	<xsl:for-each select="//PRIMEReport">
		<xsl:text>H</xsl:text>&delimiter;FA&delimiter;<xsl:value-of select="concat(substring(//PRIMEReport/LocalTime,1,4),substring(//PRIMEReport/LocalTime,6,2),substring(//PRIMEReport/LocalTime,9,2))"/>&cr;Trade&delimiter;
		<xsl:apply-templates select="current()/ReportContents"/>
	</xsl:for-each>
	<xsl:text>F</xsl:text>&delimiter;<xsl:value-of select="$NumberOfRows" />
</xsl:template>

<xsl:template match="Table">
	<xsl:for-each select="Columns/Column">
		<xsl:if test="position() != last()">
			<xsl:value-of select="Label"/>&delimiter;
		</xsl:if>
		<xsl:if test="position() = last()">
			<xsl:value-of select="Label"/>
		</xsl:if>
	</xsl:for-each>
	&cr;
	<xsl:apply-templates select="Rows/Row/Rows/Row/Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
	<xsl:value-of select="Label"/>&delimiter;
	<xsl:for-each select="Cells/Cell">
		<xsl:if test="position() != last()">
			<xsl:value-of select="RawData"/>&delimiter;
		</xsl:if>
		<xsl:if test="position() = last()">
			<xsl:value-of select="RawData"/>
		</xsl:if>
	</xsl:for-each>
	&cr;
</xsl:template>

</xsl:stylesheet>
