<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:strip-space elements="*"/>
	<xsl:output method="xml" indent="yes"/>
	<xsl:template match="PRIMEReport">
		<xsl:variable name="rootElementName" select="translate(Name,' ','')"/>
		<xsl:element name="{$rootElementName}">
			<xsl:variable name="reportColumns" select="ReportContents/Table/Columns"/>
			<trades>
				<xsl:for-each select="ReportContents/Table/Rows/Row[1]/Rows/Row">
					<trade>
						<tradeNumber>
							<xsl:value-of select="Label"/>
						</tradeNumber>
						<!--<xsl:for-each select="Cells/Cell">
							<xsl:variable name="tradeCellPosition" select="position()"/>
							<xsl:variable name="tradeElementName" select="translate($reportColumns/Column[$tradeCellPosition]/Label,' ','')"/>
							<xsl:element name="{$tradeElementName}">
								<xsl:value-of select="FormattedData"/>
							</xsl:element>
						</xsl:for-each>-->
							<instrument>
								<instrumentId>
									<xsl:value-of select="Rows/Row[1]/Label"/>
								</instrumentId>
								<xsl:for-each select="Rows/Row[1]/Cells/Cell">
									<xsl:variable name="instrumentCellPosition" select="position()"/>
									<xsl:variable name="instrumentElementName" select="translate($reportColumns/Column[$instrumentCellPosition]/Label,' ','')"/>
									<xsl:element name="{$instrumentElementName}">
										<xsl:value-of select="FormattedData"/>
									</xsl:element>
								</xsl:for-each>
								<xsl:variable name="legCount" select="count(Rows/Row[1]/Rows/Row)"/>
								<xsl:if test="$legCount>0">
									<legs>
										<xsl:for-each select="Rows/Row[1]/Rows/Row">
											<leg>
												<xsl:for-each select="Cells/Cell">
													<xsl:variable name="legCellPosition" select="position()"/>
													<xsl:variable name="legElementName" select="translate($reportColumns/Column[$legCellPosition]/Label,' ','')"/>
													<xsl:element name="{$legElementName}">
														<xsl:value-of select="FormattedData"/>
													</xsl:element>
												</xsl:for-each>
											</leg>
										</xsl:for-each>
									</legs>
								</xsl:if>
							</instrument>
						
					</trade>
				</xsl:for-each>
			</trades>
		</xsl:element>
	</xsl:template>
</xsl:stylesheet>


