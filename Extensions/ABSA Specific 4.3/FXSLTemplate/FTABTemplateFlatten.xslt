#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates xls

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY tab "<xsl:text>&#9;</xsl:text>">
  <!ENTITY cr "<xsl:text>&#13;</xsl:text>">
]>
<!-- TAB Template to flatten report structure -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
    <!-- Reports -->
    <xsl:for-each select="//PRIMEReport">
        <xsl:apply-templates select="current()/ReportContents"/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="Table">
	&tab;
	<xsl:for-each select="Columns/Column">
		<xsl:value-of select="Label"/>&tab;
	</xsl:for-each>
	&cr;
	<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:param name="label"/>
	<xsl:variable name="newLabel">
		<xsl:choose>
			<xsl:when test="string-length($label) > 0">
                <xsl:value-of select="concat($label, '\', Label)"/>
			</xsl:when>
			<xsl:otherwise>
                <xsl:value-of select="Label"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
    <xsl:value-of select="$newLabel"/>&tab;
    <xsl:for-each select="Cells/Cell">
        <xsl:value-of select="RawData"/>&tab;
    </xsl:for-each>
    &cr;
    <xsl:apply-templates select="Rows/Row">
		<xsl:with-param name="label" select="$newLabel"/>
    </xsl:apply-templates>
</xsl:template>

</xsl:stylesheet>
