<?xml version="1.0" encoding="UTF-8"?>
<!-- &copy; Copyright 2007 SunGard FRONT ARENA -->
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xalan="http://xml.apache.org/xalan"
	exclude-result-prefixes="xalan">
	<xsl:output method="html"/>
	<xsl:variable name="numberofcolumns" select="//Table/NumberOfColumns"/>
	<xsl:variable name="numberofpages" select="count(//Rows/Row)"/>
	<xsl:variable name="TTP_skip" select="count(//Columns/Column[starts-with(Label,'TTP_skip')]/preceding-sibling::Column)"/>
	<xsl:variable name="TTP_skip_option" select="//Columns/Column[starts-with(Label,'TTP_skip')]/ColumnId"/>
	<xsl:variable name="time" select="concat(substring(//LocalTime[1],1,10),' ',substring(//LocalTime[1],12,8),' (UTC', substring(//LocalTime[1],20,6),')')"/>

	<xsl:template match="/">
			<html>
			 <body>
			 <style type="text/css">
@page { size:portrait; 21.0cm 29.7cm; margin:1cm 1cm 1.4cm 1cm; }
@media print, screen, handheld {
  /* ... define format for printing ... */
body {
  margin: 0;
  padding: 0;
  font: 12pt Garamond, Palatino, "Times New Roman", Times, serif;
  color: black;
  background: transparent;
}

h1, h2, h3, h4, h5, h6 {
  font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", "Lucida", Verdana, "Bitstream Vera Sans", sans-serif;
  font-weight: bold;
  margin: .75em 0 .5em 0;
  page-break-after: avoid;
}

h2 {
  font-size: 1.4em;
  text-transform: uppercase;
  letter-spacing: .05em;
  color: #4F9B74;
}

h3 {
  font-size: 1.3em;
}

h4 {
  font-size: 1.2em;
}

h5 {
  font-size: 1.0em;
}

h6 {
  font-size: .8em;
}

ol, ul, li {
  font-size: 1.0em;
  line-height: 1.8;
  margin-top: .2em;
  margin-bottom: .1em;
}

p {
  font-size: 1.0em;
  line-height: 1.5;
  margin: 0 0 1em 0;
}

#footer {
  border-top: 1.5pt solid;
  font-size: .95em;
  color: #333;
  text-align: center;
}

}

			</style>
			<xsl:apply-templates select="//Rows/Row" mode="prepare"/>
			 </body>
		 </html>
	</xsl:template>

<!-- Prepare a row, delete empty columns -->
	<xsl:template match="Row" mode="prepare">
		<xsl:variable name="rowtree" >
			<xsl:copy>
				<Row>
					<xsl:apply-templates select="@*|node()" mode="copy"/>
				</Row>
			</xsl:copy>
		</xsl:variable>
		<xsl:apply-templates select="xalan:nodeset($rowtree)/Row" mode="output"/>

		<xsl:if test="position() &lt; $numberofpages">
				<p style="page-break-after:always"></p>
		</xsl:if>

	</xsl:template>

<!-- Copy and alter Row-->
	<xsl:template match="Cells/Cell" mode="copy">
		<xsl:variable name="pos" select="position()"/>
		<xsl:variable name="label" select="//Columns//Column[$pos]/Label"/>

		<xsl:choose>
			<xsl:when test="starts-with($label,'TTP_skip')"/>
			<xsl:when test="starts-with($label,'TTBS_') and count(../../Queries/query[@name=$label]/data) = 0"/>
			<xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'None') and FormattedData = 'None'"/>
			<xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'zero') and number(RawData) = 0"/>
			<xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'empty') and FormattedData = ''"/>
			<xsl:otherwise>
				<xsl:copy>
					<xsl:apply-templates select="@*|node()" mode="copy"/>
					<Label>
						<xsl:value-of select="$label"/>
					</Label>
				</xsl:copy>

			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="@*|node()" mode="copy">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" mode="copy"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="Row" mode="output">
				<h2>Trade Ticket</h2>
				<hr></hr>
				<xsl:call-template name="PrintRow">
					<xsl:with-param name="column" select="1"/>
					<xsl:with-param name="dcol" select="0"/>
					<xsl:with-param name="numberofcolumns" select="count(Row/Cells/Cell)"/>
				</xsl:call-template>
				<br /><br /><br /><br />
				<div id="footer">
				<xsl:value-of select="$time"/>
				</div>

	</xsl:template>

	<xsl:template match="query" mode="output">
		<xsl:variable name="count" select="count(header/column)"/>
		<table width="100%">
		<colgroup span="{$count}">
			<xsl:for-each select="header/column">
				<xsl:variable name="width" select="@size"/>
				<col width="{$width}%"></col>
			</xsl:for-each>
		</colgroup>

		<xsl:for-each select="header/column">
		   <td>
				<b>
					<xsl:value-of select="."/>
				</b>
			</td>
		</xsl:for-each>

		<xsl:for-each select="data">
			<tr>
				<xsl:for-each select="column">
					<td>
						<xsl:value-of select="."/>
					</td>
				</xsl:for-each>
			</tr>
		</xsl:for-each>

	</table>
	</xsl:template>

	<xsl:template name="PrintRow">
		<xsl:param name="column"/>
		<xsl:param name="dcol"/>
		<xsl:param name="numberofcolumns"/>

		<xsl:variable name="header" select="Row/Cells/Cell[$column]/Label"/>
		<xsl:choose>
			<xsl:when test="$column>$numberofcolumns"/>
			<xsl:when test="starts-with($header,'TTBS_')">
				<xsl:variable name="ttbpos" select="count(Row/Cells/Cell[$column]/following-sibling::Cell[starts-with(Label,'TTB')][1]/preceding-sibling::Cell)"/>
				<xsl:variable name="nextpos" select="($ttbpos > 0) * $ttbpos + ($ttbpos = 0) * $numberofcolumns"/>

				<xsl:apply-templates select="node()/Queries/query[@name=$header]" mode="output"/>

				<xsl:call-template name="PrintTable">
					<xsl:with-param name="column" select="$column+starts-with($header,'TTB')"/>
					<xsl:with-param name="endcol" select="$nextpos"/>
					<xsl:with-param name="dcol" select="0"/>
				</xsl:call-template>


				<xsl:call-template name="PrintRow">
					<xsl:with-param name="column" select="$nextpos+1"/>
					<xsl:with-param name="dcol" select="$dcol"/>
					<xsl:with-param name="numberofcolumns" select="$numberofcolumns"/>
				</xsl:call-template>

			</xsl:when>
			<xsl:when test="starts-with($header,'TTB_') or $column = 1">
				<xsl:variable name="ttbpos" select="count(Row/Cells/Cell[$column]/following-sibling::Cell[starts-with(Label,'TTB')][1]/preceding-sibling::Cell)"/>
				<xsl:variable name="nextpos" select="($ttbpos > 0) * $ttbpos + ($ttbpos = 0) * $numberofcolumns"/>

				<xsl:if test="(1+$nextpos - $column - starts-with($header,'TTB_') + starts-with(Row/Cells/Cell[$column+1]/Label,'TTBS')) > 0">

					<xsl:if test="starts-with($header,'TTB_')">

						<h3><xsl:value-of select="substring-after($header,'TTB_')"/></h3>
						<hr></hr>
					</xsl:if>

					<table width="100%">
						<colgroup span="4">
							<col width="20%"></col>
							<col width="30%"></col>
							<col width="20%"></col>
							<col width="30%"></col>
						</colgroup>
						<xsl:call-template name="PrintTable">
							<xsl:with-param name="column" select="$column + starts-with($header,'TTB_')"/>
							<xsl:with-param name="endcol" select="$nextpos"/>
							<xsl:with-param name="dcol" select="0"/>
						</xsl:call-template>
					</table>
				</xsl:if>

				<xsl:call-template name="PrintRow">
					<xsl:with-param name="column" select="$nextpos+1"/>
					<xsl:with-param name="dcol" select="$dcol"/>
					<xsl:with-param name="numberofcolumns" select="$numberofcolumns"/>
				</xsl:call-template>
			</xsl:when>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="PrintTable">
		<xsl:param name="column"/>
		<xsl:param name="dcol"/>
		<xsl:param name="endcol"/>

		<xsl:choose>
			<xsl:when test="$column>$endcol"/>
			<xsl:otherwise>
				<tr>
					<xsl:call-template name="PrintColumn">
						<xsl:with-param name="column" select="$column"/>
						<xsl:with-param name="colspan" select="starts-with(Row/Cells/Cell[$column+1]/Label,'TTV_Void')+1"/>
					</xsl:call-template>
					<xsl:call-template name="PrintColumn">
						<xsl:with-param name="column" select="$column+1"/>
						<xsl:with-param name="colspan" select="1"/>
					</xsl:call-template>
				</tr>
				<xsl:call-template name="PrintTable">
					<xsl:with-param name="column" select="$column+2"/>
					<xsl:with-param name="dcol" select="$dcol"/>
					<xsl:with-param name="endcol" select="$endcol"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>


	<xsl:template name="PrintColumn">
		<xsl:param name="column"/>
		<xsl:param name="colspan"/>
		<xsl:variable name="header" select="Row/Cells/Cell[$column]/Label"/>
		<xsl:choose>
			<xsl:when test="starts-with($header,'TTV_Void') or starts-with($header,'TTB')">
			<td></td><td></td>
			</xsl:when>
			<xsl:otherwise>
				<td>
					<b><xsl:value-of select="$header"/></b>
				</td>
				<td colspan="{$colspan}">
					<xsl:value-of select="Row/Cells/Cell[$column]/FormattedData"/>
				</td>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

</xsl:stylesheet>
