#grouping: aef reporting/secondary templates

<?xml version='1.0' ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="xml"/>
	<xsl:template match="/">
		<FrontArenaMessage>
			<Timestamp>
				<xsl:value-of select="PRIMEReport/Time"/>
			</Timestamp>
				<xsl:for-each select="PRIMEReport/ReportContents/Table/Rows/Row">
				<Book>
                                                                                <BookId>
						<xsl:for-each select="Cells/Cell[ColumnId='Portfolio AssignInfo']">
							<xsl:value-of select="RawData"/>
						</xsl:for-each>
					</BookId>
					<BookName>
                                                                                                <xsl:value-of select="Portfolio/Name"/>
					</BookName>
					<xsl:for-each select="Rows/Row">
						<Instrument>
							<InstrumentName>
								<xsl:value-of select="Label"/>
							</InstrumentName>
							<SecurityType>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Instrument Type']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</SecurityType>
							<Currency>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Instrument Curr']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</Currency>
							<PositionCurrency>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Currency']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PositionCurrency>
							<SecurityID>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Instrument SEDOL']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</SecurityID>
							<SecurityIDType>SEDOL</SecurityIDType>
							<Market>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Counterparty']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</Market>
							<Quantity>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Profit Loss Position End']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</Quantity>
							<SODQuantity>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Profit Loss Position SOD']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</SODQuantity>
							<Price>
								<xsl:for-each select="Cells/Cell[ColumnId='ADS Last Price In Rands']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</Price>
							<Bought>
								<xsl:for-each select="Rows/Row[Label='Buy']">
									<xsl:for-each select="Rows/Row/Cells/Cell[ColumnId='Portfolio Profit Loss Position Daily']">
										<xsl:value-of select="round(RawData)"/>
									</xsl:for-each>
								</xsl:for-each>
							</Bought>
							<Sold>
								<xsl:for-each select="Rows/Row[Label='Sell']">
									<xsl:for-each select="Rows/Row/Cells/Cell[ColumnId='Portfolio Profit Loss Position Daily']">
										<xsl:value-of select="round(RawData)"/>
									</xsl:for-each>
								</xsl:for-each>
							</Sold>
							<AvgCostBought>
								<xsl:for-each select="Rows/Row[Label='Buy']">
									<xsl:for-each select="Rows/Row/Cells/Cell[ColumnId='Portfolio Average Price Daily In Rands']">
										<xsl:value-of select="RawData"/>
									</xsl:for-each>
								</xsl:for-each>
							</AvgCostBought>
							<AvgCostSold>
								<xsl:for-each select="Rows/Row[Label='Sell']">
									<xsl:for-each select="Rows/Row/Cells/Cell[ColumnId='Portfolio Average Price Daily In Rands']">
										<xsl:value-of select="RawData"/>
									</xsl:for-each>
								</xsl:for-each>
							</AvgCostSold>
							<TradePL>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Total Profit and Loss Daily']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</TradePL>
							<SODPL>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Total Profit and Loss SOD']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</SODPL>
							<TotalPL>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Total Profit and Loss']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</TotalPL>
							<NetValue>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Delta Cash Global']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</NetValue>
							<YTDPL>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Total Profit and Loss Yearly']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</YTDPL>
							<MTDPL>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Total Profit and Loss Monthly']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</MTDPL>
                                                                                                                <UnderlyingRIC>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity UnderlyingRIC']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</UnderlyingRIC>
                                                                                                                <ContractSize>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Contract Size']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</ContractSize>
							<ExpiryDate>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Expiry Date']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</ExpiryDate>
						</Instrument>
					</xsl:for-each>
					<ZARtoUSD>
						<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Fx Rate[0] Standard']">
							<xsl:value-of select="RawData"/>
						</xsl:for-each>
					</ZARtoUSD>
					<ZARtoGBP>
						<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Fx Rate[1] Standard']">
							<xsl:value-of select="RawData"/>
						</xsl:for-each>
					</ZARtoGBP>
				</Book>
			</xsl:for-each>
		</FrontArenaMessage>
	</xsl:template>
</xsl:stylesheet>
