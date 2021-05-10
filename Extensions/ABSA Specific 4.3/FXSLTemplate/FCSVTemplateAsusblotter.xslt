#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/style sheets

<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:variable name="delimiter"><xsl:text>,</xsl:text></xsl:variable>

<xsl:variable name="quote"><xsl:text>"</xsl:text></xsl:variable>
<xsl:variable name="newline"><xsl:text>&#13;</xsl:text></xsl:variable>

<xsl:output method="text" encoding="ISO-8859-1"/>

<xsl:template match="/">
    <!-- Reports -->
    <xsl:for-each select="//PRIMEReport">
        <xsl:apply-templates select="current()/ReportContents"/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="Table">
        <xsl:value-of select="'Trade Number'"/>
        <xsl:value-of select="$delimiter"/>
    <xsl:for-each select="Columns/Column">
        <xsl:value-of select="Label"/>
        <xsl:value-of select="$delimiter"/>
    </xsl:for-each>
    <xsl:value-of select="$newline"/>
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

<xsl:template match="Row">
    <xsl:value-of select="Label"/>
    <xsl:value-of select="$delimiter"/>
    <xsl:for-each select="Cells/Cell">
    
     
    <xsl:variable name ="pos" select="position()"/>
    <xsl:variable name ="columnId" select="//Columns/Column[$pos]/ColumnId "/>
        <xsl:if test="RawData != '[]'">
            <xsl:choose>            
                <xsl:when test="FormattedData">
                    <xsl:choose> 
                        <xsl:when test="$columnId='Trade Premium' or $columnId='Trade Quantity' or $columnId='Trade Nominal' or $columnId='Portfolio Accrued Interest' or $columnId='FaceValue' or $columnId='PremiumUSD'">                    
                        <xsl:if test="starts-with(FormattedData, '-')">
                            <xsl:value-of select="$quote"/>
                            <xsl:value-of select="substring(FormattedData,2)"/>
                            <xsl:value-of select="$quote"/>
                        </xsl:if>  
                        
                        <xsl:if test="not(starts-with(FormattedData, '-')) and FormattedData !=''">
                            <xsl:value-of select="$quote"/>
                            <xsl:value-of select="concat('-',FormattedData)"/>
                            <xsl:value-of select="$quote"/>
                        </xsl:if> 
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:choose>
                             <xsl:when test="FormattedData = 'Buy'">
                                <xsl:value-of select="$quote"/>
                                <xsl:value-of select="'Sell'"/>
                                <xsl:value-of select="$quote"/>
                             </xsl:when>
                             <xsl:when test="FormattedData = 'Sell'">
                                <xsl:value-of select="$quote"/>
                                <xsl:value-of select="'Buy'"/>
                                <xsl:value-of select="$quote"/>
                             </xsl:when>
                             <xsl:otherwise>
                                <xsl:value-of select="$quote"/>
                                <xsl:value-of select="FormattedData"/>
                                <xsl:value-of select="$quote"/>
                             </xsl:otherwise>
                           </xsl:choose>
                    </xsl:otherwise>  
                 </xsl:choose> 
                </xsl:when>
            </xsl:choose>
        </xsl:if>
        <xsl:value-of select="$delimiter"/>
        
        
    </xsl:for-each>
    <xsl:value-of select="$newline"/>
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
