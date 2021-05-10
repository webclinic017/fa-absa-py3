<?xml version="1.0"?>
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
					<BookName>a
						<xsl:value-of select="Portfolio/Name"/>
					</BookName>
					<xsl:for-each select="Rows/Row">
						<Instrument>
							<InstrumentName>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Instrument Name']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
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
									<xsl:call-template name="formatData">
										<xsl:with-param name="inputData" select="RawData"/>
									</xsl:call-template>
								</xsl:for-each>
							</Quantity>
							<SODQuantity>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Profit Loss Position SOD']">
									<xsl:call-template name="formatData">
										<xsl:with-param name="inputData" select="RawData"/>
									</xsl:call-template>
								</xsl:for-each>
							</SODQuantity>
							<Price>
								<xsl:for-each select="Cells/Cell[ColumnId='ADS Last Price In Rands']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</Price>
							<Bought>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Daily Bought']">
									<xsl:call-template name="formatNumericData">
										<xsl:with-param name="inputData" select="RawData"/>
									</xsl:call-template>
								</xsl:for-each>
							</Bought>
							<Sold>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Daily Sold']">
									<xsl:call-template name="formatNumericData">
										<xsl:with-param name="inputData" select="RawData"/>
									</xsl:call-template>
								</xsl:for-each>
							</Sold>
							<AvgCostBought>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Average Price Bought']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</AvgCostBought>
							<AvgCostSold>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity Average Price Sold']">
									<xsl:value-of select="RawData"/>
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
									<xsl:call-template name="getDateFormat">
								            <xsl:with-param name="date" select="normalize-space(RawData)"/>
									</xsl:call-template>
								</xsl:for-each>
							</ExpiryDate>
							<!--  Underlying SEDOL  -->
							<UnderlyingSEDOL>
								<xsl:for-each select="Cells/Cell[ColumnId='Instrument.Underlying.AdditionalInfo.SEDOL']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</UnderlyingSEDOL>
							<!--  Call Put  -->
							<CallPut>
								<xsl:for-each select="Cells/Cell[ColumnId='Call or Put']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</CallPut>
							<!--  ExerciseType American/European  -->
							<ExerciseType>
								<xsl:for-each select="Cells/Cell[ColumnId='ExerciseType']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</ExerciseType>
							<!--  Price Delta Instrument  -->
							<PriceDeltaInstrument>
								<xsl:for-each select="Cells/Cell[ColumnId='Instrument Delta']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PriceDeltaInstrument>
							<!--  Vega Instrument  -->
							<VegaInstrument>
								<xsl:for-each select="Cells/Cell[ColumnId='Instrument Vega']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</VegaInstrument>
							<!--  Price Gamma Instrument  -->
							<GammaInstrument>
								<xsl:for-each select="Cells/Cell[ColumnId='Instrument Gamma']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</GammaInstrument>
							<!--  Theta Instrument  -->
							<ThetaInstrument>
								<xsl:for-each select="Cells/Cell[ColumnId='Instrument Theta One Day']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</ThetaInstrument>

							<!--  Portfolio Vega   -->
							<PortfolioVega>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Vega']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioVega>

							<!-- Portfolio Theta One Day -->
							<PortfolioTheta>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Theta One Day']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioTheta>
							<TheoreticalPrice>
								<xsl:for-each select="Cells/Cell[ColumnId='Price Theor']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</TheoreticalPrice>
							<!-- Portfolio Delta Implicit Cash Equity -->
							<PortfolioDeltaCash>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Delta Implicit Cash Equity']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioDeltaCash>
							<!-- Market Exchange-->
							<MarketExchange>
								<xsl:for-each select="Cells/Cell[ColumnId='Cash Equity MarketExchange']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</MarketExchange>
							<!-- Strike Price -->
							<StrikePrice>
								<xsl:for-each select="Cells/Cell[ColumnId='Strike Price']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</StrikePrice>
							<!-- Gamma Cash -->
							<PortfolioDelta>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Delta Cash']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioDelta>
							<PortfolioGamma>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Gamma Cash']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioGamma>
							<PortfolioRho>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Rho']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</PortfolioRho>
							<ImpliedVolatility>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Volatility']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</ImpliedVolatility>
							<NAV>
								<xsl:for-each select="Cells/Cell[ColumnId='Portfolio Net Asset Value']">
									<xsl:value-of select="RawData"/>
								</xsl:for-each>
							</NAV>
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
	<xsl:template name="getDateFormat">
                        <xsl:param name="date"/>
                        <xsl:variable name="CCYY" select="substring($date,7,4)"/>
                        <xsl:variable name="MMM" select="substring($date,4,2)"/>
                        <xsl:variable name="DD" select="substring($date,1,2)"/>
                        <xsl:value-of select="concat($CCYY,'-',$MMM,'-',$DD)"/>
	</xsl:template>
	<xsl:template name="formatData">
		<xsl:param name="inputData"/>
		<xsl:choose>
			<xsl:when test="$inputData = '[]'">
				<xsl:value-of select="'0.0'"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$inputData"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="formatNumericData">
		<xsl:param name="inputData"/>
		<xsl:choose>
			<xsl:when test="$inputData != ''">
				<xsl:value-of select="format-number($inputData, '###')"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="'0.0'"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
