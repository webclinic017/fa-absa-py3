<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:x="urn:schemas-microsoft-com:office:excel"
	xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:html="http://www.w3.org/TR/REC-html40" >
	
	<xsl:template match="/">

<Workbook
	xmlns="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:x="urn:schemas-microsoft-com:office:excel"
	xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:html="http://www.w3.org/TR/REC-html40" >
	<DocumentProperties xmlns="urn:schemas-microsoft-com:office:office">
		<Author></Author>
		<LastAuthor></LastAuthor>
		<Created></Created>
		<Company>Absa</Company>
		<Version>1.0000</Version>
	</DocumentProperties>
	<Styles>
		<Style ss:ID="Default" ss:Name="Normal">
			<Alignment ss:Vertical="Top" />
			<Borders>
				<Border ss:Position="Left" ss:LineStyle="None" />
				<Border ss:Position="Bottom" ss:LineStyle="None" />
				<Border ss:Position="Top" ss:LineStyle="None" />
				<Border ss:Position="Right" ss:LineStyle="None" />
			</Borders>
			<Font ss:FontName="Arial" ss:size="10" />
			<Interior ss:Color="#FFFFFF" ss:Pattern="Solid" />
			<NumberFormat />
			<Protection />
		</Style>
		<Style ss:ID="title" ss:Name="Heading" ss:Parent="Default" >
			<Font ss:Bold="1" />
		</Style>
		<Style ss:ID="value_general" ss:Name="Value: General">
		</Style>
		<Style ss:ID="value_date" ss:Name="Value: Date" ss:Parent="value_general">
			<Font ss:Color="#333399"/>
			<NumberFormat ss:Format="[ENG][$-409]d\-mmm\-yy;@" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="value_gbp_zar" ss:Name="Value: GBP-ZAR" ss:Parent="value_general">
			<Font ss:Color="#FF0000"/>
			<NumberFormat ss:Format="#0.000 00" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="value_notional" ss:Name="Value: Notional" ss:Parent="value_general">
			<Font ss:Color="#333399"/>
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="value_rate" ss:Name="Value: Rate" ss:Parent="value_general">
			<NumberFormat ss:Format="#0.000 00" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="value_rate_purple" ss:Name="Value: Rate purple" ss:Parent="value_general">
			<Font ss:Bold="1" ss:Color="#993366"/>
			<NumberFormat ss:Format="#0.00" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="value_sum" ss:Name="Value: Sum" ss:Parent="value_general">
			<Font ss:Bold="1" ss:Color="#FF0000"/>
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
			<Alignment ss:Horizontal="Right" ss:Vertical="Top"/>
		</Style>
		<Style ss:ID="table_headlines" ss:Name="Table headlines" ss:Parent="value_general">
			<Font ss:Bold="1" ss:Color="#FFFFFF"/>
			<Alignment ss:Horizontal="Center" ss:Vertical="Top"/>
			<Interior ss:Color="#666699" ss:Pattern="Solid"/>
			<Borders>
				<Border ss:Position="Top" ss:Color="#000000" ss:LineStyle="Continuous" ss:Weight="1" />
				<Border ss:Position="Bottom" ss:Color="#000000" ss:LineStyle="Continuous" ss:Weight="1" />
			</Borders>
		</Style>
		<Style ss:ID="note_nacc" ss:Name="Note: NACC">
			<Font ss:Color="#993366"/>
		</Style>
		<Style ss:ID="description_text" ss:Name="Description text">
			<Font ss:Color="#333399"/>
			<Alignment ss:WrapText="1" ss:Vertical="Bottom" ss:Horizontal="Center" />
		</Style>
		<Style ss:ID="table_data_date" ss:Name="Table data: date" ss:Parent="value_general">
			<NumberFormat ss:Format="[ENG][$-409]d\-mmm\-yy;@" />
		</Style>
		<Style ss:ID="table_data_amount" ss:Name="Table data: amount" ss:Parent="value_general">
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
		<Style ss:ID="table_data_rate" ss:Name="Table data: rate" ss:Parent="value_general">
			<NumberFormat ss:Format="#,###,###,###,###,##0.00%" />
		</Style>
		<Style ss:ID="table_data_integer" ss:Name="Table data: integer" ss:Parent="value_general">
			<NumberFormat ss:Format="#,###,###,###,###,###" />
		</Style>
		<Style ss:ID="table_data_coefficient_9" ss:Name="Table data: coefficient 9" ss:Parent="value_general">
			<NumberFormat ss:Format="#,###,###,###,###,##0.000 000 000" />
		</Style>
		<Style ss:ID="table_data_projected_value" ss:Name="Table data: projected value" ss:Parent="table_data_amount">
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
			<Interior ss:Color="#BBBBBB" ss:Pattern="Solid"/>
		</Style>
	</Styles>
	<Worksheet ss:Name="Absa Trade ######">
		<Table ss:ExpandedColumnCount="24" ss:ExpandedRowCount="100" x:FullColumns="1" x:FullRows="1">
			<Column ss:Index="1" ss:Width="120"/>
			<Column ss:Index="2" ss:Width="100"/>
			<Column ss:Index="3" ss:Width="10"/>
			<Column ss:Index="4" ss:Width="80"/>
			<Column ss:Index="5" ss:Width="80"/>
			<Column ss:Index="6" ss:Width="80"/>
			<Column ss:Index="7" ss:Width="80"/>
			<Column ss:Index="8" ss:Width="80"/>
			<Column ss:Index="9" ss:Width="80"/>
			<Column ss:Index="10" ss:Width="80"/>
			<Column ss:Index="11" ss:Width="80"/>
			<Column ss:Index="12" ss:Width="20"/>
			<Column ss:Index="13" ss:Width="10"/>
			<Column ss:Index="14" ss:Width="80"/>
			<Column ss:Index="15" ss:Width="80"/>
			<Column ss:Index="16" ss:Width="80"/>
			<Column ss:Index="17" ss:Width="80"/>
			<Column ss:Index="18" ss:Width="80"/>
			<Column ss:Index="19" ss:Width="80"/>
			<Column ss:Index="20" ss:Width="80"/>
			<Column ss:Index="21" ss:Width="80"/>
			<Column ss:Index="22" ss:Width="20"/>
			<Column ss:Index="23" ss:Width="10"/>
			<Column ss:Index="24" ss:Width="80"/>
			<Row>
				<Cell ss:StyleID="title">
					<Data ss:Type="String"><xsl:value-of select="/Report/@Title"/></Data>
				</Cell>
			</Row>
			<Row ss:Index="2">
				<Cell ss:Index="6" ss:MergeAcross="6" ss:MergeDown="5" ss:StyleID="description_text">
					<Data ss:Type="String">This deal has been valued using mid-market rates and provides an indication of the value of the deal for audit and valuation purposes only. The valuation excludes any Credit and/or Funding adjustments These values do not represent valuations at which this position may be closed out. This valuation is from the bank's point of view.</Data>
				</Cell>
			</Row>
			<Row ss:Index="3">
				<Cell><Data ss:Type="String">Value date</Data></Cell>
				<Cell ss:StyleID="value_date">
					<Data ss:Type="DateTime"><xsl:value-of select="/Report/@Date"/></Data>
				</Cell>
			</Row>
			<Row ss:Index="5">
				<Cell><Data ss:Type="String"><xsl:value-of select="/Report/General/ReceiveLeg/@Currency" />/<xsl:value-of select="/Report/General/PayLeg/@Currency" /> spot</Data></Cell>
				<Cell ss:StyleID="value_gbp_zar">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/@FXSpotRatio"/></Data>
				</Cell>
			</Row>
			<Row ss:Index="7">
				<Cell><Data ss:Type="String"><xsl:value-of select="/Report/General/ReceiveLeg/@Currency" /> Notional</Data></Cell>
				<Cell ss:StyleID="value_notional">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/ReceiveLeg/@NominalAmount" /></Data>
				</Cell>
			</Row>
			<Row ss:Index="8">
				<Cell><Data ss:Type="String"><xsl:value-of select="/Report/General/PayLeg/@Currency" /> Notional</Data></Cell>
				<Cell ss:StyleID="value_notional">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/PayLeg/@NominalAmount" /></Data>
				</Cell>
			</Row>
			<Row ss:Index="10">
				<Cell><Data ss:Type="String"><xsl:value-of select="/Report/General/ReceiveLeg/@Currency" /> Rate</Data></Cell>
				<Cell ss:StyleID="value_rate_purple">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/ReceiveLeg/@FixedRate" /></Data>
				</Cell>
			</Row>
			<Row ss:Index="11">
				<Cell><Data ss:Type="String"><xsl:value-of select="/Report/General/PayLeg/@Currency" /> Rate</Data></Cell>
				<Cell ss:StyleID="value_rate_purple">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/PayLeg/@FixedRate" /></Data>
				</Cell>
			</Row>
			<Row ss:Index="13">
				<Cell><Data ss:Type="String">Sum of PVs</Data></Cell>
				<Cell ss:StyleID="value_sum">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/@SumOfPVs" /></Data>
				</Cell>
				<Cell ss:Index="10" ss:StyleID="table_data_amount">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/PayLeg/@ProjectedValuesSum" /></Data>
				</Cell>
				<Cell ss:Index="11" ss:StyleID="table_data_projected_value">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/PayLeg/@PresentValuesSum" /></Data>
				</Cell>
				<Cell ss:Index="12" ss:StyleID="note_nacc">
					<Data ss:Type="String">NACC</Data>
				</Cell>
				<Cell ss:Index="20" ss:StyleID="table_data_amount">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/ReceiveLeg/@ProjectedValuesSum" /></Data>
				</Cell>
				<Cell ss:Index="21" ss:StyleID="table_data_projected_value">
					<Data ss:Type="Number"><xsl:value-of select="/Report/General/ReceiveLeg/@PresentValuesSum" /></Data>
				</Cell>
				<Cell ss:Index="22" ss:StyleID="note_nacc">
					<Data ss:Type="String">NACC</Data>
				</Cell>
			</Row>
			<Row ss:Index="14">
				<Cell ss:Index="12" ss:StyleID="note_nacc">
					<Data ss:Type="String"><xsl:value-of select="/Report/General/PayLeg/@DayCountMethod" /></Data>
				</Cell>
				<Cell ss:Index="22" ss:StyleID="note_nacc">
					<Data ss:Type="String"><xsl:value-of select="/Report/General/ReceiveLeg/@DayCountMethod" /></Data>
				</Cell>
			</Row>
			<Row ss:Index="16">
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">Settlement Date</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">Days</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">Zar Zero</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR/USD Basis</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Basis Zero</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Balance</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Capital</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Interest</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Net</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">ZAR Basis PV</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">DF</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Zero</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP/USD Basis</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Basis Zero</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Balance</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Capital</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Interest</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Net</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">GBP Basis PV</Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">DF</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell ss:StyleID="table_headlines">
					<Data ss:Type="String">FX Forward</Data>
				</Cell>
			</Row>
			<xsl:for-each select="/Report/Valuation/Point">
			<Row>
				<Cell ss:StyleID="table_data_date">
					<Data ss:Type="DateTime"><xsl:value-of select="@PayDate"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_integer">
					<Data ss:Type="Number"><xsl:value-of select="@Days"/></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<xsl:call-template name="CashFlow">
					<xsl:with-param name="Data" select="PayData" />
				</xsl:call-template>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<xsl:call-template name="CashFlow">
					<xsl:with-param name="Data" select="ReceiveData" />
				</xsl:call-template>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell ss:StyleID="value_rate">
					<Data ss:Type="Number"><xsl:value-of select="@FXRate"/></Data>
				</Cell>
			</Row>
    		</xsl:for-each>
		</Table>
	</Worksheet>
	<Worksheet ss:Name="Curves">
		<Table ss:ExpandedColumnCount="7" ss:ExpandedRowCount="100" x:FullColumns="1" x:FullRows="1">
			<Column ss:Index="1" ss:Width="80"/>
			<Column ss:Index="2" ss:Width="60"/>
			<Column ss:Index="3" ss:Width="60"/>
			<Column ss:Index="4" ss:Width="10"/>
			<Column ss:Index="5" ss:Width="10"/>
			<Column ss:Index="6" ss:Width="60"/>
			<Column ss:Index="7" ss:Width="100"/>
			<Row>
				<Cell>
					<Data ss:Type="String">CURVE</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String">M_MATDATE</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String">M_ZCMID</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String">MATLABEL</Data>
				</Cell>
				<Cell>
					<Data ss:Type="String">M_ZCMID</Data>
				</Cell>
			</Row>
			<xsl:for-each select="/Report/YieldCurves/YieldCurve">
			<Row>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
			</Row>
				<xsl:for-each select="Point">
			<Row>
				<Cell>
					<Data ss:Type="String"><xsl:value-of select="../@Name"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_date">
					<Data ss:Type="DateTime"><xsl:value-of select="@Date"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_rate">
					<Data ss:Type="Number"><xsl:value-of select="@ValueRounded"/></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"><xsl:value-of select="@Period"/></Data>
				</Cell>
				<Cell>
					<Data ss:Type="Number"><xsl:value-of select="@Value"/></Data>
				</Cell>
			</Row>
    			</xsl:for-each>
    		</xsl:for-each>
		</Table>
	</Worksheet>
</Workbook>

	</xsl:template>

	<xsl:template name="CashFlow">
		<xsl:param name="Data" />
				<Cell ss:StyleID="table_data_rate">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@ForwardRate"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_rate">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@CurrSwap"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_rate">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@CurrBasis"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_amount">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@Nominal"/></Data>
				</Cell>
				<Cell>
					<Data ss:Type="String"></Data>
				</Cell>
				<Cell ss:StyleID="table_data_amount">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@ProjectedValue"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_amount">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@ProjectedValue"/></Data>
				</Cell>
				<Cell ss:StyleID="table_data_projected_value">
					<Data ss:Type="Number"><xsl:value-of select="$Data/@PresentValue"/></Data>
				</Cell>
				<Cell>
				<xsl:choose>
					<xsl:when test="$Data/@Difference != 0">
					<xsl:attribute name="ss:StyleID">table_data_coefficient_9</xsl:attribute>
					<Data ss:Type="Number"><xsl:value-of select="$Data/@Difference"/></Data>
					</xsl:when>
					<xsl:otherwise>
					<Data ss:Type="String"></Data>
					</xsl:otherwise>
				</xsl:choose>
				</Cell>

	</xsl:template>

</xsl:stylesheet>
