#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
  <!ENTITY cr "<xsl:text>&#13;</xsl:text>">
]>

<!--
CSV Template for task OPS_CashAnalysis_CapitalMarket_Recon_SERVER
specific for Cash Analysis sheets to include only report date valid data
but exclude Security Nominal and End Security.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>
<!--<xsl:variable name="reportDate" select="concat(substring(//PRIMEReport/Time,9,2),'/',substring(//PRIMEReport/Time,6,2),'/',substring(//PRIMEReport/Time,1,4))"/>
<xsl:variable name="reportDate" select="substring(//PRIMEReport/Time,1,10)"/>-->

<xsl:template match="/">
    <!-- Reports -->
    <xsl:for-each select="//PRIMEReport">                         
	    <xsl:apply-templates select="current()/ReportContents"/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="Table">
	&comma;
	<xsl:for-each select="Columns/Column">
		<xsl:value-of select="Label"/>&comma;
	</xsl:for-each>
	&cr;
	<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
	<xsl:if test="Label != 'Security Nominal' and Label != 'End Security' and Label != 'SAOPS_CA_Capital_Markets'">
		<xsl:value-of select="Label"/>&comma;
		<xsl:for-each select="Cells/Cell">
			<xsl:choose>
                <xsl:when test="DefaultData">
                    <xsl:value-of select="translate(DefaultData,',','')"/>
                </xsl:when>
                <xsl:when test="FormattedData">
                    <xsl:value-of select="translate(FormattedData,',','')"/>
                </xsl:when>
                <xsl:when test="RawData">
                    <xsl:value-of select="translate(RawData,',','')"/>
                </xsl:when>
            </xsl:choose>&comma;
		</xsl:for-each>
		&cr;
	</xsl:if>
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
