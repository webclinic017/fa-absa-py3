<?xml version='1.0'?>
<!-- &copy; Copyright 2008 SunGard FRONT ARENA
       FStandardTemplate is able to produce colored output for RiskMatrixSheets when DefaultData is turned on
       Added support for Transhist output
-->
<!DOCTYPE xsl:stylesheet [
    <!ENTITY nbsp "<xsl:text>&#160;</xsl:text>">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:param name="clickable" select="1"/>
<xsl:param name="autoupdate" select="0"/>
<xsl:output method="html"/>
<xsl:variable name="cellWidth" select="80"/>
<xsl:variable name="rowHeaderWidth" select="250"/>
<xsl:variable name="useLabelColumn" select="//PRIMEReport/Type !='ASQL Table'"/>


<xsl:template name="PrintSpaces">
  <xsl:param name="n" select="0"/>
  <xsl:if test="$n > 0">
    <xsl:call-template name="PrintSpaces">
      <xsl:with-param name="n" select="$n - 1" />
    </xsl:call-template>
    &nbsp;
  </xsl:if>
</xsl:template>

<xsl:template match="ReportContents">
	 <xsl:apply-templates select="Table"/>
</xsl:template>

<xsl:template match="Table" mode="ChildReport">
	<xsl:param name = "treeDepth"/>
    <xsl:apply-templates select="Settings"/>

    <xsl:variable name="numberOfColumns" select="NumberOfColumns"/>

	<tr class="tblhdr" depth="{$treeDepth}">
	   <xsl:if test="$useLabelColumn">
		<td width="{$rowHeaderWidth}">
			<xsl:call-template name="PrintSpaces">
				<xsl:with-param name="n" select="($treeDepth -1) * 6"/>
			</xsl:call-template>
		<img src="report_plus.gif" />&nbsp;</td>
		</xsl:if>
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
		<xsl:with-param name="treeDepth" select="$treeDepth"/>
		<xsl:with-param name="colorStep" select="0"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="Table">
    <xsl:apply-templates select="Settings"/>

    <xsl:variable name="numberOfColumns" select="NumberOfColumns"/>

    <xsl:variable name="colorStep" >
        <xsl:choose>
                <xsl:when test="(Type = 'RiskMatrixSheet') and current()//DefaultData">
                    <xsl:variable name="maxvalue">
                        <xsl:call-template name="max">
                                <xsl:with-param name="nodes" select="current()//DefaultData"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:value-of select="$maxvalue div 255" ></xsl:value-of>
                </xsl:when>
                <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <table width="{$numberOfColumns * ($cellWidth + 4) + $rowHeaderWidth + 6}">
        <tr class="tblhdr">
           <xsl:if test="$useLabelColumn">
            <td width="{$rowHeaderWidth}">&nbsp;</td>
            </xsl:if>
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
            <xsl:with-param name="colorStep" select="$colorStep"/>
        </xsl:apply-templates>
    </table>
    <p/><p/>
</xsl:template>

<xsl:template match="Row">
    <xsl:param name = "treeDepth"/>
    <xsl:param name = "colorStep"/>
    <xsl:variable name="rwId" select="RowId"/>
    <tr class="{concat('cell', $treeDepth)}" depth="{$treeDepth}">
        <xsl:if test="$useLabelColumn">
                <td class="row">
                <xsl:call-template name="PrintSpaces">
                        <xsl:with-param name="n" select="($treeDepth - 1) * 6"/>
                </xsl:call-template>
                <xsl:if test="$clickable = '1'">
                        <img src="report_plus.gif"/>
                </xsl:if>
                <xsl:value-of select="Label"/>
                </td>
        </xsl:if>
    <xsl:apply-templates select="Cells/Cell">
        <xsl:with-param name="colorStep" select="$colorStep" />
    </xsl:apply-templates>
    </tr>
    <xsl:if test="ancestor::ReportContents/ChildReports/ChildReport[ChildReportId = $rwId]">
	    <xsl:apply-templates select="ancestor::ReportContents/ChildReports/ChildReport[ChildReportId = $rwId]/PRIMEReport/ReportContents/Table" mode="ChildReport">
			<xsl:with-param name="treeDepth" select="$treeDepth +1" />
		</xsl:apply-templates>
    </xsl:if>
    <xsl:apply-templates select="Rows/Row">
        <xsl:with-param name="treeDepth" select="$treeDepth + 1" />
        <xsl:with-param name="colorStep" select="$colorStep" />
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="Cell">
    <xsl:param name = "colorStep"/>
    <td>
        <xsl:if test="DefaultData and $colorStep > 0 and string(number(DefaultData)) !='NaN'">
                <xsl:attribute name="style">background-color:
                        <xsl:call-template name="color">
                                <xsl:with-param name="colorStep" select="$colorStep"/>
                                <xsl:with-param name="value" select="DefaultData"/>
                        </xsl:call-template>
                </xsl:attribute>
        </xsl:if>
        <xsl:choose>
                <xsl:when test="ValueType and DefaultData">
                        <acronym>
                                <xsl:attribute name="title">
                                        <xsl:value-of select="DefaultData"/>
                                </xsl:attribute>
                        <xsl:call-template name="CellData" />
                        </acronym>
                </xsl:when>
                <xsl:otherwise>
                        <xsl:call-template name="CellData" />
                </xsl:otherwise>
        </xsl:choose>
    </td>
</xsl:template>

<xsl:template name="CellData">
        <xsl:choose>
            <xsl:when test="FormattedData">
                <xsl:value-of select="FormattedData"/>
            </xsl:when>
            <xsl:when test="RawData">
                <xsl:value-of select="RawData"/>
            </xsl:when>
            <xsl:when test="DefaultData">
                <xsl:choose>
                        <xsl:when test="ValueType">
                                <xsl:text>#</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                                <xsl:value-of select="DefaultData"/>
                        </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
            <xsl:message terminate="yes"><xsl:text>No dataformat turned on</xsl:text></xsl:message>
            </xsl:otherwise>
        </xsl:choose>
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
                        <xsl:call-template name="CellData" />
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
        <xsl:if test="$autoupdate = '1'">
                <meta http-equiv="REFRESH" content="10"></meta>
        </xsl:if>
        </head>
        <insertcss/>
        <body>
        <xsl:if test="$clickable = '1'">
                <xsl:attribute name="onload">init()</xsl:attribute>
                <script src="portfolio_report.js" type="text/javascript"></script>
        </xsl:if>

        <!-- Table of contents, only viewed if more than one report -->

        <xsl:if test="/MultiReport">
                <table>
                    <xsl:for-each select="/MultiReport/PRIMEReport">
                            <tr><td>
                                <td><xsl:value-of select="Type"/></td>
                                <td><xsl:value-of select="Name"/></td>
                                <td><xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/></td>
                            </td></tr>
                   </xsl:for-each>
                </table>
        </xsl:if>

        <!-- Reports -->
        <xsl:for-each select="/MultiReport/PRIMEReport|/PRIMEReport">
            <h3>
                    <xsl:value-of select="Type"/>:&nbsp;
                    <xsl:value-of select="Name"/>&nbsp;
                    <xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/>
             </h3>

             <xsl:apply-templates select="current()/ReportContents"/>
        </xsl:for-each>
        </body>
    </html>
</xsl:template>

<!-- derived from http://www.exslt.org/math/functions/max/index.html -->
<xsl:template name="max">
   <xsl:param name="nodes" select="/.." />
   <xsl:choose>
      <xsl:when test="not($nodes)">0</xsl:when>
      <xsl:otherwise>
         <xsl:for-each select="$nodes">
            <xsl:sort select="translate(.,'-','')" data-type="number" order="descending" />
            <xsl:if test="position( ) = 1">
               <xsl:value-of select="number(translate(.,'-',''))" />
            </xsl:if>
         </xsl:for-each>
      </xsl:otherwise>
   </xsl:choose>
</xsl:template>

<xsl:template name="color">
   <xsl:param name="value"/>
   <xsl:param name = "colorStep"/>
   <xsl:variable name="rgbval">
	   <xsl:choose>
	      <xsl:when test="$value > 0" >
	      	<xsl:value-of select="255 - round($value div $colorStep)"/>
      	</xsl:when>
		<xsl:otherwise>
	      	<xsl:value-of select="255 - round($value div $colorStep * -1)"/>
		</xsl:otherwise>
	   </xsl:choose>

   </xsl:variable>
   <xsl:choose>
     	<xsl:when test="$value > 0 and $rgbval &lt; 0">
			<xsl:text>rgb(255,0,0)</xsl:text>
	    	</xsl:when>
     	<xsl:when test="$value &lt; 0 and $rgbval &lt; 0">
			<xsl:text>rgb(0,255,0)</xsl:text>
	    	</xsl:when>
     	<xsl:when test="$value > 0">
      		<xsl:value-of select="concat('rgb(',$rgbval,',255,',$rgbval,')')"/>
	    	</xsl:when>
      <xsl:otherwise>
      		<xsl:value-of select="concat('rgb(255,',$rgbval,',',$rgbval,')')"/>
      </xsl:otherwise>
   </xsl:choose>
</xsl:template>


</xsl:stylesheet>
