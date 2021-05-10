<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet [
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
    <xsl:apply-templates select="Settings"/>
    <xsl:param name="numberOfColumns" select="NumberOfColumns"/>
    <table width="{$numberOfColumns * ($cellWidth + 4) + $rowHeaderWidth + 6}">
        <tr class="tblhdr">
            <td width="{$rowHeaderWidth}">&nbsp;</td>
            <xsl:for-each select="Columns/Column">
                <xsl:choose>
                <xsl:when test="TemplateId != ''">
                    <td width="{$cellWidth * 2}">
                    <xsl:value-of select="TemplateId"/><br />
                    <xsl:value-of select="Label"/>
                    </td>
                </xsl:when>
                <xsl:otherwise>
                    <td width="{$cellWidth}"><xsl:value-of select="Label"/></td>
                </xsl:otherwise>
                </xsl:choose>
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
    <tr class="{concat('cell', $treeDepth)}" depth="{$treeDepth}">
        <td class="row">
            <xsl:call-template name="PrintSpaces">
                <xsl:with-param name="n" select="($treeDepth - 1) * 6"/>
            </xsl:call-template>
            <xsl:value-of select="Label"/>
        </td>
        <xsl:for-each select="Cells/Cell">
            <td>
                <xsl:value-of select="FormattedData"/>
            </td>
        </xsl:for-each>
    </tr>
    <xsl:apply-templates select="Rows/Row">
        <xsl:with-param name="treeDepth" select="$treeDepth + 1"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="Settings">
    <table>
    <tr>
        <xsl:for-each select="Groups/Group">
            <xsl:if test="Label = 'Profit/Loss'">
                <tr class="tblhdr">
                <xsl:for-each select="Column">
                    <td class="row" width="{$cellWidth}">
                    <xsl:choose>
                        <xsl:when test="Label != ''">
                            <xsl:value-of select="Label"/>
                        </xsl:when>
                        <xsl:otherwise>
                             <xsl:value-of select="ColumnId"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    </td>
                </xsl:for-each>
                </tr>
                <tr class="row" depth="1">
                <xsl:for-each select="Cell">
                    <td class="cell1">
                    <xsl:value-of select="FormattedData"/>
                    </td>
                </xsl:for-each>
                </tr>

            </xsl:if>
        </xsl:for-each>
        </tr>
    </table>
    <p/><p/>
</xsl:template>

<xsl:template match="/">
    <html>
        <head>
            <meta http-equiv="REFRESH" content="10"></meta>
        </head>
        <insertcss/>
        <body>
            <h2>
                <xsl:value-of select="PRIMEReport/Type"/>:&nbsp;
                <xsl:value-of select="PRIMEReport/Name"/>&nbsp;
                <xsl:value-of select="concat(substring(PRIMEReport/LocalTime,1,10),' ',substring(PRIMEReport/LocalTime,12,8),' (UTC', substring(PRIMEReport/LocalTime,20,6),')')"/>
            </h2>
            <p/>
            <xsl:apply-templates select="PRIMEReport/ReportContents/*"/>
        </body>
    </html>
</xsl:template>

</xsl:stylesheet>
