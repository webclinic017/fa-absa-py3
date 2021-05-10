<?xml version="1.0" encoding="UTF-8"?>
<!-- &copy; Copyright 2007 SunGard FRONT ARENA -->
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fo="http://www.w3.org/1999/XSL/Format"
	xmlns:xalan="http://xml.apache.org/xalan"
	exclude-result-prefixes="xalan">
	<xsl:output method="xml" version="1.0" encoding="iso-8859-1" indent="yes"/>
	<xsl:variable name="numberofcolumns" select="//Table/NumberOfColumns"/>
	<xsl:variable name="numberofpages" select="count(//Table/Rows/Row)"/>
	<xsl:variable name="TTP_skip" select="count(//Columns/Column[starts-with(Label,'TTP_skip')]/preceding-sibling::Column)"/>
	<xsl:variable name="TTP_skip_option" select="//Columns/Column[starts-with(Label,'TTP_skip')]/ColumnId"/>
                <xsl:variable name="time" select="concat(substring(//LocalTime[1],1,10),' ',substring(//LocalTime[1],12,8),' (UTC', substring(//LocalTime[1],20,6),')')"/>

	<xsl:template match="/">
                                <fo:root>
                                        <fo:layout-master-set>
                                                <fo:simple-page-master margin-right="1cm" margin-left="1cm" margin-bottom="1.3cm" margin-top="1cm" page-width="21cm" page-height="29.7cm" master-name="first">
                                                <fo:region-body margin-top="1.5cm" margin-bottom="1.5cm"/>
			<fo:region-before extent="2cm"/>
			<fo:region-after extent="1.5cm"/>
			</fo:simple-page-master>
			</fo:layout-master-set>
                                        <xsl:apply-templates select="//Rows/Row" mode="prepare"/>
		</fo:root>
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
		<fo:page-sequence master-reference="first">
			<fo:static-content flow-name="xsl-region-before">
				<fo:block font-size="10pt">TRADE TICKET</fo:block>
				<fo:block>
					<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
				</fo:block>
			</fo:static-content>
			<fo:static-content flow-name="xsl-region-after">
				<fo:block>
					<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
				</fo:block>
				<fo:block font-size="10pt">
					<xsl:value-of select="$time"/>
				</fo:block>
			</fo:static-content>
			<fo:flow flow-name="xsl-region-body">
				<xsl:call-template name="PrintRow">
					<xsl:with-param name="column" select="1"/>
					<xsl:with-param name="dcol" select="0"/>
					<xsl:with-param name="numberofcolumns" select="count(Row/Cells/Cell)"/>
				</xsl:call-template>

			</fo:flow>
		</fo:page-sequence>
	</xsl:template>

	<xsl:template match="query" mode="output">
		<xsl:variable name="count" select="count(header/column)"/>
		<xsl:if test="count(data)>0">

		<fo:table table-layout="fixed" width="100%">
			<xsl:for-each select="header/column">
				<xsl:variable name="width" select="@size"/>
				<fo:table-column column-width="{$width * 1.8}mm"/>
			</xsl:for-each>

			<fo:table-header>
				<fo:table-row>
					<xsl:for-each select="header/column">
						<fo:table-cell>
							<fo:block font-size="8pt" font-weight="bold" text-align="right" vertical-align="middle" border-width="1pt" border-color="black" background-color="#cccccc">
								<xsl:value-of select="."/>
							</fo:block>
						</fo:table-cell>
			</xsl:for-each>
				</fo:table-row>
			</fo:table-header>

			<fo:table-body>
			<xsl:for-each select="data">
				<fo:table-row>	<xsl:for-each select="column"><fo:table-cell>
							<fo:block font-size="8pt">
								<xsl:value-of select="."/>
							</fo:block>
						</fo:table-cell>
					</xsl:for-each></fo:table-row>
			</xsl:for-each>
			</fo:table-body>
		</fo:table>
		</xsl:if>
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

				<xsl:if test="($column+1-$nextpos) > 1">
					<fo:table table-layout="fixed" width="100%">
						<fo:table-column column-width="50mm"/>
						<fo:table-column column-width="40mm"/>
						<fo:table-column column-width="50mm"/>
						<fo:table-column column-width="40mm"/>
						<fo:table-body>
							<xsl:call-template name="PrintTable">
								<xsl:with-param name="column" select="$column+1"/>
								<xsl:with-param name="endcol" select="$nextpos"/>
								<xsl:with-param name="dcol" select="$dcol+1"/>
							</xsl:call-template>
						</fo:table-body>
					</fo:table>
				</xsl:if>

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

				<fo:block font-size="12pt" font-weight="bold">
					<xsl:value-of select="substring-after($header,'TTB_')"/>

				</fo:block>
				<fo:block>
					<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
				</fo:block>
				</xsl:if>

					<xsl:if test="starts-with(Row/Cells/Cell[$column+1]/Label,'TTBS')=0">

					<fo:table table-layout="fixed" width="100%">
						<fo:table-column column-width="50mm"/>
						<fo:table-column column-width="40mm"/>
						<fo:table-column column-width="50mm"/>
						<fo:table-column column-width="40mm"/>
						<fo:table-body>
							<xsl:call-template name="PrintTable">
								<xsl:with-param name="column" select="$column+starts-with($header,'TTB_')"/>
								<xsl:with-param name="endcol" select="$nextpos"/>
								<xsl:with-param name="dcol" select="0"/>
							</xsl:call-template>
						</fo:table-body>
					</fo:table>
					</xsl:if>
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
					<fo:table-row>
						<xsl:call-template name="PrintColumn">
							<xsl:with-param name="column" select="$column"/>
							<xsl:with-param name="colspan" select="starts-with(Row/Cells/Cell[$column+1]/Label,'TTV_Void')+1"/>
						</xsl:call-template>
						<xsl:call-template name="PrintColumn">
							<xsl:with-param name="column" select="$column+1"/>
							<xsl:with-param name="colspan" select="1"/>
						</xsl:call-template>
					</fo:table-row>
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
		<xsl:param name="colspan" select="1"/>
		<xsl:variable name="header" select="Row/Cells/Cell[$column]/Label"/>

		<xsl:choose>
			<xsl:when test="starts-with($header,'TTV_Void') or starts-with($header,'TTB')">
				<fo:table-cell>
					<fo:block/>
				</fo:table-cell>
				<fo:table-cell>
					<fo:block/>
				</fo:table-cell>
			</xsl:when>
			<xsl:otherwise>
				<fo:table-cell>
					<fo:block font-size="8pt" font-weight="bold">
						<xsl:value-of select="$header"/>
					</fo:block>
				</fo:table-cell>
				<fo:table-cell number-columns-spanned="{$colspan}">
					<fo:block font-size="8pt">
						<xsl:value-of select="Row/Cells/Cell[$column]/FormattedData"/>
					</fo:block>
				</fo:table-cell>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
