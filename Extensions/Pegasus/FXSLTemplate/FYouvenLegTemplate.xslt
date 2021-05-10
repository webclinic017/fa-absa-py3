#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates txt
#grouping: aef reporting/secondary templates xls

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<xsl:strip-space elements="*"/>
	<xsl:template match="/">
		<xsl:for-each select="//PRIMEReport">
			<xsl:if test="contains(current()/Name,'LEG')">
				<xsl:apply-templates select="ReportContents/Table"/>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
	<xsl:template match="Table">
		<xsl:value-of select="concat('tradeLegNumber','&#9;')"/>
		<xsl:for-each select="Columns/Column">
		<xsl:if test="position()>1">
			<xsl:value-of select="Label"/>
			<xsl:text>&#9;</xsl:text>
			</xsl:if>
		</xsl:for-each>
		<xsl:text>&#13;</xsl:text>
		
		<xsl:apply-templates select="Rows/Row[1]/Rows/Row" mode="trade"/>
	</xsl:template>
	<xsl:template match="Row" mode="trade">
		<xsl:value-of select="Label"/><!--<xsl:text>&#9;</xsl:text>-->
		<xsl:apply-templates select="Rows/Row[1]/Rows/Row" mode="leg"/>
		
		<xsl:text>&#13;</xsl:text>
		
		</xsl:template>
		
		<xsl:template match="Row" mode="leg">
		 <xsl:for-each select="Cells/Cell">
		 
		 <xsl:value-of select="translate(FormattedData,',','')"/>
		 <xsl:text>&#9;</xsl:text>
		
		 </xsl:for-each>
		
		</xsl:template>
</xsl:stylesheet>


