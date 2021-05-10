#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version='1.0'?><!-- This is a descendant of FCSVTemplate, just with a different header. -->
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
            Generated Time:&comma;<xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/>
            Report Date:&comma;<xsl:value-of select="current()/ReportParameters/DateToday"/>
            Version:&comma;<xsl:value-of select="current()/ReportParameters/FrameworkVersion"/>
            <xsl:apply-templates select="current()/ReportContents"/>
     </xsl:for-each>
</xsl:template>

<xsl:template match="Table">
&cr;&cr;&comma;
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&comma;
</xsl:for-each>
&cr;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>&comma;
    <xsl:for-each select="Cells/Cell">
         <xsl:choose>
         <xsl:when test="not(contains(RawData, 'could not be'))">
           <xsl:value-of select="translate(RawData,',[]','')"/>&comma;
         </xsl:when>
         <xsl:otherwise>&comma;</xsl:otherwise>
       </xsl:choose>
        
            
            
    </xsl:for-each>
    &cr;
    <xsl:apply-templates select="Rows/Row"/>
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
