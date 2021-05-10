#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates xls

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
      <xsl:value-of select="Label"/>
      <xsl:text>&#9;</xsl:text>
    </xsl:for-each>
    <xsl:text>&#13;</xsl:text>
    <xsl:apply-templates select="Rows/Row" mode="First"/>
  </xsl:template>

  <xsl:template name="RowTemplate">
    <xsl:value-of select="Label"/>
    <xsl:text>&#9;</xsl:text>
    <xsl:for-each select="Cells/Cell">

      <xsl:choose>
        <xsl:when test="DefaultData">
          <xsl:value-of select="DefaultData"/>
        </xsl:when>
        <xsl:when test="FormattedData">
          <xsl:value-of select="FormattedData"/>
        </xsl:when>
        <xsl:when test="not(ValueType) and RawData">
          <xsl:value-of select="RawData"/>
        </xsl:when>
        <xsl:when test="RawData">
          <!-- Some kind of error occurred -->
          <xsl:text>ERROR</xsl:text>
        </xsl:when>
      </xsl:choose>
      <xsl:text>&#9;</xsl:text>
    </xsl:for-each>
    <xsl:text>&#13;</xsl:text>
  </xsl:template>
  
  <xsl:template match="Row" mode="First">
    <xsl:call-template name="RowTemplate" />
    <xsl:apply-templates select="Rows/Row" mode="Second"  />
  </xsl:template>

  <xsl:template match="Row" mode="Second">
    <xsl:call-template name="RowTemplate" />
    <xsl:apply-templates select="Rows/Row/Rows/Row" mode="Fourth"  />
  </xsl:template>
  
  <!-- skip third descendant (portfolio name grouping) -->

  <xsl:template match="Row" mode="Fourth">
    <xsl:call-template name="RowTemplate" />
    <xsl:apply-templates select="Rows/Row" mode="Fourth"  />
  </xsl:template>

</xsl:stylesheet>
