#grouping: aef reporting/secondary templates

<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY comma "<xsl:text>,</xsl:text>">
  <!ENTITY br "<xsl:text>&#13;</xsl:text>">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="ISO-8859-1"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/">
        <xsl:for-each select="//PRIMEReport">                         
            <xsl:apply-templates select="current()/ReportContents"/>             
     </xsl:for-each>     
</xsl:template>

<xsl:template match="Table">
    <xsl:for-each select="Columns/Column">
        <xsl:value-of select="Label"/>&comma;
    </xsl:for-each>&br;
        <xsl:choose>
                <xsl:when test="Rows/Row/Rows/Row">
                        <xsl:apply-templates select="Rows/Row/Rows/Row"/>
                </xsl:when>
                <xsl:otherwise>
                        <xsl:apply-templates select="Rows/Row"/>
                </xsl:otherwise>
        </xsl:choose>
</xsl:template>

<xsl:template match="Row">
    <xsl:for-each select="Cells/Cell">
        <xsl:choose>
                <xsl:when test="FullData/DateTime or FullData/String">
                        <xsl:value-of select="FormattedData"/>&comma;
                </xsl:when>
                <xsl:otherwise>
                        <xsl:value-of select="FullData"/>&comma;
                </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>&br;
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

        
</xsl:stylesheet>
