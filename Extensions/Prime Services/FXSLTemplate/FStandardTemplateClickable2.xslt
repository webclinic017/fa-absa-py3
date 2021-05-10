<?xml version='1.0'?>
<!DOCTYPE stylesheet [
    <!ENTITY nbsp "<xsl:text>&#160;</xsl:text>">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html"/>
<xsl:variable name="cellWidth" select="80"/>
<xsl:variable name="rowHeaderWidth" select="250"/>

<xsl:template name="PrintSpaces">
  <xsl:param name="n" select="0"/>
  <xsl:if test="$n > 0">
    <xsl:call-template name="PrintSpaces">
      <xsl:with-param name="n" select="$n - 1" />
    </xsl:call-template>
    &nbsp;
  </xsl:if>
</xsl:template>

<xsl:template match="Table">
    <xsl:param name="numberOfColumns" select="NumberOfColumns"/>
    <table width="{$numberOfColumns * ($cellWidth + 4) + $rowHeaderWidth + 6}">
        <tr class="tblhdr">
            <xsl:for-each select="Columns/Column">
                <td width="{$cellWidth}"><xsl:value-of select="Label"/></td>
            </xsl:for-each>
        </tr>
        <xsl:apply-templates select="Rows/Row">
            <xsl:with-param name="treeDepth" select="1"/>
        </xsl:apply-templates>
    </table>
    <p/><p/>
</xsl:template>

<xsl:template match="Row">
    <xsl:param name = "treeDepth"/>
    <tr class="row" depth="{$treeDepth}">
        <xsl:for-each select="Cells/Cell">
            <td class="{concat('cell', $treeDepth)}">
                <xsl:value-of select="FormattedData"/>
            </td>
        </xsl:for-each>
    </tr>
    <xsl:apply-templates select="Rows/Row">
        <xsl:with-param name="treeDepth" select="$treeDepth + 1"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="ReportProperties">
    <table>
        <xsl:for-each select="Property">
            <tr>
                <td class="row" width="{$rowHeaderWidth}">
                    <xsl:value-of select="Key"/>
                </td>
                <td class="cell1" width="{$cellWidth * 2}">
                    <xsl:value-of select="Value"/>
                </td>
            </tr>
        </xsl:for-each>
    </table>
    <p/><p/>
</xsl:template>

<xsl:template match="TableProperties">
    <h3>
        <xsl:value-of select="Name"/>
    </h3>
    <table>
        <xsl:for-each select="Property">
            <tr>
                <td class="row" width="{$rowHeaderWidth}">
                    <xsl:value-of select="Key"/>
                </td>
                <td class="cell1" width="{$cellWidth}">
                    <xsl:value-of select="Value"/>
                </td>
            </tr>
        </xsl:for-each>
    </table>
    <p/><p/>
</xsl:template>

<xsl:template match="/">
    <html>
        <head/>
        <insertcss/>
        <body onload="init()">
            <script src="portfolio_report.js" type="text/javascript"></script>
            <h2>
                <xsl:value-of select="PRIMEReport/Type"/>:&nbsp;
                <xsl:value-of select="PRIMEReport/Name"/>&nbsp;
                <xsl:value-of select="PRIMEReport/Time"/>
            </h2>
            <p/>
            <xsl:apply-templates select="PRIMEReport/ReportContents/*"/>
        </body>
    </html>
</xsl:template>

</xsl:stylesheet>
