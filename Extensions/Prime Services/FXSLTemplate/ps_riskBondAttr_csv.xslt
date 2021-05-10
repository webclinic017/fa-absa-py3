#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/style sheets

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
<!ENTITY comma "<xsl:text>,</xsl:text>">
<!ENTITY cr "<xsl:text>&#13;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">

<!-- Reports -->
<xsl:for-each select="//PRIMEReport">
Report Name:&comma;<xsl:value-of select="current()/ReportParameters/ReportName"/>
Generated Time:&comma;<xsl:value-of select="current()/ReportParameters/GeneratedTime"/>
Report Date:&comma;<xsl:value-of select="current()/ReportParameters/ReportDate"/>
Version:&comma;<xsl:value-of select="current()/ReportParameters/FrameworkVersion"/>&cr;&cr;

<xsl:value-of select="current()/ReportParameters/TradeFilter"/>
&comma;&comma;&comma;&comma;Benchmark Delta&comma;Curve Move
Benchmark&comma;Instrument Type&comma;Financing Type&comma;Position&comma;Total&comma;T-1&comma;T&comma;Change&comma;PnL Expect
<xsl:for-each select="//ReportDetail/ReportRow">
<xsl:value-of select="@Label"/>&comma;
<xsl:value-of select="InsType"/>&comma;
<xsl:value-of select="FinType"/>&comma;
<xsl:value-of select="Position"/>&comma;
<xsl:value-of select="Total"/>&comma;
<xsl:value-of select="CurveT1"/>&comma;
<xsl:value-of select="CurveT"/>&comma;
<xsl:value-of select="Change"/>&comma;
<xsl:value-of select="PnLExpect"/>&cr;
</xsl:for-each>

</xsl:for-each>
</xsl:template>


</xsl:stylesheet>
