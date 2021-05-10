<?xml version='1.0'?>


<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<!-- edit by Rolf Stenholm for proper handling of raw data -->

<xsl:template match="/">
        
<!-- Reports -->
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
    <xsl:value-of select="Label"/><xsl:text>&#9;</xsl:text>
</xsl:for-each>
<xsl:text>&#13;</xsl:text>
<xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>
    <xsl:text>&#9;</xsl:text>
    <xsl:for-each select="Cells/Cell">
    	
        <xsl:choose>
		
                <xsl:when test="DefaultData">
					<xsl:call-template name="formatData">
						<xsl:with-param name="inputData" select="DefaultData"/>
					</xsl:call-template>
									
                </xsl:when>        
                <xsl:when test="FormattedData">
					<xsl:call-template name="formatData">
						<xsl:with-param name="inputData" select="FormattedData"/>
					</xsl:call-template>
					
                </xsl:when>
                <xsl:when test="not(ValueType) and RawData">                
                        
                </xsl:when>
				
                <xsl:when test="RawData">
                		<!-- Some kind of error occurred -->
                		<xsl:text>ERROR</xsl:text>
                </xsl:when>
        </xsl:choose>
        <xsl:text>&#9;</xsl:text>        
    </xsl:for-each>
    	<xsl:text>&#13;</xsl:text>
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
