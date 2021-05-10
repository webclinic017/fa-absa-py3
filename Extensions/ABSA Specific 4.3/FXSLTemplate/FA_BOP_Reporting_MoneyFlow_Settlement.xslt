#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format"  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<xsl:strip-space elements="*"/>
	<xsl:variable name="pipe" select="string('|')"/>
	<xsl:variable name="eoln">
		<xsl:text>&#13;</xsl:text>
	</xsl:variable>
	
	<xsl:template match="PRIMEReport">
		<xsl:apply-templates select="ReportContents/Table/Columns/Column"/>
		<xsl:value-of select="$eoln"/>
		<xsl:apply-templates select="ReportContents/Table/Rows/Row/Rows/Row"/>
	</xsl:template>
			
	<xsl:template match="Column">
		<xsl:if test="position() != 12">
			<xsl:value-of select="Label"/>
		</xsl:if>
		<xsl:if test="position() &lt; 11">
			<xsl:value-of select="$pipe"/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Row">
        <xsl:variable name="moneyFlowType" select="Cells/Cell[8]/RawData"/>
        <xsl:variable name="callAccountInterestFlag" select="Cells/Cell[12]/RawData"/>
        <xsl:if test="($moneyFlowType != 'None') and ($moneyFlowType != 'Redemption Amount') and ($moneyFlowType != 'Security Nominal') and ($moneyFlowType != 'Stand Alone Payment') and ($moneyFlowType != 'End Security') and ($moneyFlowType != 'Aggregate Security') and ($moneyFlowType != 'Aggregate Cash')">
			<xsl:choose>
				<xsl:when test="($moneyFlowType = 'Call Fixed Rate Adjustable') or ($moneyFlowType = 'Fixed Rate Adjustable')">
					<xsl:if test="$callAccountInterestFlag = 'true'">
						<xsl:apply-templates select="Cells/Cell"/>
						<xsl:value-of select="$eoln"/>
					</xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="Cells/Cell"/>
					<xsl:value-of select="$eoln"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="Cell">
		<xsl:if test="position() != 12">
			<xsl:value-of select="RawData"/>
		</xsl:if>
		<xsl:if test="position() &lt; 11">
			<xsl:value-of select="$pipe"/>
		</xsl:if>
	</xsl:template>	
</xsl:stylesheet>
