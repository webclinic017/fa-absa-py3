#grouping: aef reporting/secondary templates

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:strip-space elements="*"/>
	<xsl:output method="xml" indent="yes"/>
	<xsl:template match="PRIMEReport">
		<xsl:variable name="rootElementName" select="translate(Name,' ','')"/>
		<xsl:element name="{$rootElementName}">
			<xsl:variable name="reportColumns" select="ReportContents/Table/Columns"/>
			<TRADES>
				<xsl:for-each select="ReportContents/Table/Rows/Row">
					<TRADE>
						<TRDNBR>
							<xsl:value-of select="Label"/>
						</TRDNBR>
						<!--<xsl:for-each select="Cells/Cell">
							<xsl:variable name="tradeCellPosition" select="position()"/>
							<xsl:variable name="tradeElementName" select="translate($reportColumns/Column[$tradeCellPosition]/Label,' ','')"/>
							<xsl:element name="{$tradeElementName}">
								<xsl:value-of select="FormattedData"/>
							</xsl:element>
						</xsl:for-each>-->
						<xsl:variable name="moneyFlowCount" select="count(Rows/Row)"/>
						<xsl:if test="$moneyFlowCount>0">
							<MONEY_FLOWS>
								<xsl:for-each select="Rows/Row">
									<MONEY_FLOW>
										<ROW_TYPE>
											<xsl:value-of select="Label"/>
										</ROW_TYPE>
										<xsl:for-each select="Cells/Cell">
											<xsl:variable name="moneyFlowCellPosition" select="position()"/>
											<xsl:variable name="moneyFlowElementName" select="translate($reportColumns/Column[$moneyFlowCellPosition]/Label,' ','')"/>
											<xsl:element name="{$moneyFlowElementName}">
												<xsl:value-of select="FormattedData"/>
											</xsl:element>
										</xsl:for-each>
										<xsl:variable name="resetCount" select="count(Rows/Row)"/>
										<xsl:if test="$resetCount>0">
											<RESETS>
												<xsl:for-each select="Rows/Row">
													<RESET>
														<xsl:for-each select="Cells/Cell">
															<xsl:variable name="resetCellPosition" select="position()"/>
															<xsl:variable name="resetElementName" select="translate($reportColumns/Column[$resetCellPosition]/Label,' ','')"/>
															<xsl:element name="{$resetElementName}">
																<xsl:value-of select="FormattedData"/>
															</xsl:element>
														</xsl:for-each>
													</RESET>
												</xsl:for-each>
											</RESETS>
										</xsl:if>
									</MONEY_FLOW>
								</xsl:for-each>
							</MONEY_FLOWS>
						</xsl:if>
					</TRADE>
				</xsl:for-each>
			</TRADES>
		</xsl:element>
	</xsl:template>
</xsl:stylesheet>
