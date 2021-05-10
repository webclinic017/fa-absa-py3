#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates xls

<?xml version='1.0'?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<xsl:strip-space elements="*"/>

	<xsl:template match="/">
		<xsl:for-each select="//PRIMEReport">
			Type:<xsl:text>&#9;</xsl:text><xsl:value-of select="current()/Type"/>
			Name:<xsl:text>&#9;</xsl:text><xsl:value-of select="current()/Name"/>
			Time:<xsl:text>&#9;</xsl:text><xsl:value-of select="current()/Time"/>
			<xsl:apply-templates select="current()/ReportContents"/>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="Table">
		Table name:<xsl:text>&#9;</xsl:text><xsl:value-of select="Name"/><xsl:text>&#13;</xsl:text>
		<xsl:text>&#9;</xsl:text>
		<xsl:for-each select="Columns/Column">
			<xsl:value-of select="Label"/>
			<xsl:text>&#9;</xsl:text>
		</xsl:for-each>
		<xsl:text>&#13;</xsl:text>
		<xsl:apply-templates select="Rows/Row"/>
	</xsl:template>

	<xsl:template match="Row">
		<xsl:if test="not(Label = 'No Issuer')">
			<xsl:choose>
				<xsl:when test="count(Rows/Row) &gt; 1">
					<xsl:call-template name="getData">
						<xsl:with-param name="Row"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:if test="not(./Rows/Row/Label = 'No Issuer')">
						<xsl:call-template name="getData">
							<xsl:with-param name="Row"/>
						</xsl:call-template>
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="Rows/Row"/>
		</xsl:if>
	</xsl:template>

	<!-- Template to retreive and output the data-->
	<xsl:template name="getData">
		<xsl:param name="currentRow"/>
		<xsl:value-of select="Label"/>
		<xsl:text>&#9;</xsl:text>
		<xsl:for-each select="Cells/Cell">
			<xsl:if test="RawData">
				<xsl:call-template name="formatData">
					<xsl:with-param name="inputData" select="RawData"/>
				</xsl:call-template>
			</xsl:if>
			<xsl:text>&#9;</xsl:text>
		</xsl:for-each>
		<xsl:text>&#13;</xsl:text>
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
