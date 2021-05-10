#grouping: aef reporting/secondary templates

<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- Using comma as delimiter. -->
<xsl:variable name="delimiter"><xsl:text>,</xsl:text></xsl:variable>
<!-- Quote to use when encountering a field with the delimiters. -->
<xsl:variable name="quote"><xsl:text>"</xsl:text></xsl:variable>
<!-- Using CR as a newline character because acm.FXSLTTransform
     can not correctly handle any other standard type of newline. -->
<xsl:variable name="newline"><xsl:text>&#13;</xsl:text></xsl:variable>

<xsl:output method="text" encoding="ISO-8859-1"/>

<xsl:template match="/">
    <!-- Reports -->
    <xsl:for-each select="//PRIMEReport">
        <!-- Enclosing raw text into the xsl:text nodes, so that
             no indentation whitespace will sneak into the output. -->
        <xsl:text>Type:</xsl:text>
        <xsl:value-of select="$delimiter"/>
        <xsl:value-of select="current()/Type"/>
        <xsl:value-of select="$newline"/>
        <xsl:text>Name:</xsl:text>
        <xsl:value-of select="$delimiter"/>
        <xsl:value-of select="current()/Name"/>
        <xsl:value-of select="$newline"/>
        <xsl:text>Time:</xsl:text>
        <xsl:value-of select="$delimiter"/>
        <xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/>
        <xsl:value-of select="$newline"/>
        <xsl:apply-templates select="current()/ReportContents"/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="Table">
    <xsl:text>Table name:</xsl:text>
    <xsl:value-of select="$delimiter"/>
    <xsl:value-of select="Name"/>
    <xsl:value-of select="$newline"/>
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
        <xsl:if test="RawData != '[]'">
            <xsl:choose>
                <xsl:when test="DefaultData">
                    <xsl:if test="contains(DefaultData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                    <xsl:value-of select="DefaultData"/>
                    <xsl:if test="contains(DefaultData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                </xsl:when>
                <xsl:when test="FormattedData">
                    <xsl:if test="contains(FormattedData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                    <xsl:value-of select="FormattedData"/>
                    <xsl:if test="contains(FormattedData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                </xsl:when>
                <xsl:when test="RawData">
                    <xsl:if test="contains(RawData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                    <xsl:value-of select="RawData"/>
                    <xsl:if test="contains(RawData, ',')">
                        <xsl:value-of select="$quote"/>
                    </xsl:if>
                </xsl:when>
            </xsl:choose>
        </xsl:if>
        <xsl:value-of select="$delimiter"/>
    </xsl:for-each>
    <xsl:value-of select="$newline"/>
    <xsl:apply-templates select="Rows/Row"/>
</xsl:template>

</xsl:stylesheet>
