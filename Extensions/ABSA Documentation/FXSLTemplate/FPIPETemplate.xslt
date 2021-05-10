#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY VerticalLine "<xsl:text>&#124;</xsl:text>">
  <!ENTITY lf "<xsl:text>&#10;</xsl:text>">
]>

<!-- 
  This template is used to create a pipe delimited file that will be used by the IntelliMatch team.
  This template was requested in FAOPS-412
 -->
 

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
        
<!-- Reports -->
    <xsl:for-each select="//PRIMEReport">                         
            Type:&VerticalLine;<xsl:value-of select="current()/Type"/>&lf;
            Name:&VerticalLine;<xsl:value-of select="current()/Name"/>&lf;
            Time:&VerticalLine;<xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/>&lf;
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
Table name:&VerticalLine;<xsl:value-of select="Name"/>&lf;
&VerticalLine;
<xsl:for-each select="Columns/Column">
    <xsl:value-of select="Label"/>&VerticalLine;
</xsl:for-each>
&lf;
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>&VerticalLine;
    <xsl:for-each select="Cells/Cell">
      <xsl:value-of select="translate(RawData,',[]','')"/>&VerticalLine;
    </xsl:for-each>
    &lf;
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
