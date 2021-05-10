<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://fron.com/arena/primereport">
	<xsl:template match="/">
		<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
			<fo:layout-master-set>
				<fo:simple-page-master master-name="SL_Return_Confirmation_A4" page-width="210mm" page-height="297mm" reference-orientation="90" margin-top="10mm" margin-bottom="10mm" margin-left="15mm" margin-right="10mm">
					<fo:region-body margin-top="30mm" margin-bottom="30mm"/>
					<fo:region-before extent="20mm"/>
					<fo:region-after extent="20mm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="SL_Return_Confirmation_A4">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="Barclays" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="60mm"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="60mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="2">
										<fo:block text-align="center"><fo:inline font-weight="bold">RETURN CONFIRMATION</fo:inline></fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="3">
										<fo:block>
											<fo:external-graphic src="file:images/AbsaCapital.png" content-width="60mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:static-content flow-name="xsl-region-after">
					<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block font-size="12pt" font-family="Barclays" color="black">
											<fo:external-graphic src="file:images/barclaysENG.jpg" content-width="50mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
										<fo:block text-align="center" font-size="12pt" font-family="Barclays" color="black">Page <fo:page-number/> of <fo:page-number-citation ref-id="last-page"/></fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<xsl:apply-templates select="//ReturnConfirmationReport"/>
				<fo:block id="last-page"/>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	<xsl:template match="//ReturnConfirmationReport">
		<fo:block break-before="page" font-size="12pt" font-family="Barclays" color="black">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-body>
					<fo:table-row>
							<fo:table-cell>
								<fo:block>
									<fo:table table-layout="fixed" width="100%">
										<fo:table-column column-width="30mm"/>
										<fo:table-column column-width="proportional-column-width(1)"/>
										<fo:table-body>
											<xsl:for-each select="ClientDetail/ReportElement">
												<fo:table-row>
													<fo:table-cell>
														<fo:block font-weight="bold"><xsl:value-of select="Label"/></fo:block>
													</fo:table-cell>
													<fo:table-cell>
														<fo:block><xsl:value-of select="Value"/></fo:block>
													</fo:table-cell>
												</fo:table-row>
											</xsl:for-each>
										</fo:table-body>
									</fo:table>
								</fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block>
									<fo:table table-layout="fixed" width="100%">
										<fo:table-column column-width="30mm"/>
										<fo:table-column column-width="proportional-column-width(1)"/>
										<fo:table-body>
											<fo:table-row>
												<fo:table-cell number-columns-spanned="2">
													<fo:block><fo:inline font-weight="bold">For ABSA Stock Brokers</fo:inline></fo:block>
												</fo:table-cell>
											</fo:table-row>
											<fo:table-row>
												<fo:table-cell>
													<fo:block><fo:inline font-weight="bold">Trading:</fo:inline></fo:block>
												</fo:table-cell>
												<fo:table-cell>
													<fo:block>Linda Breytenbach</fo:block>
												</fo:table-cell>
											</fo:table-row>
											<fo:table-row>
												<fo:table-cell>
													<fo:block><fo:inline font-weight="bold">Telephone:</fo:inline></fo:block>
												</fo:table-cell>
												<fo:table-cell>
													<fo:block>+2711 895 5105</fo:block>
												</fo:table-cell>
											</fo:table-row>
											<fo:table-row>
												<fo:table-cell>
													<fo:block><fo:inline font-weight="bold">Operations:</fo:inline></fo:block>
												</fo:table-cell>
												<fo:table-cell>
													<fo:block>Nicolene Bezuidenhout</fo:block>
												</fo:table-cell>
											</fo:table-row>
											<fo:table-row>
												<fo:table-cell>
													<fo:block><fo:inline font-weight="bold">Telephone:</fo:inline></fo:block>
												</fo:table-cell>
												<fo:table-cell>
													<fo:block>+2711 895 7662</fo:block>
												</fo:table-cell>
											</fo:table-row>
										</fo:table-body>
									</fo:table>
								</fo:block>
							</fo:table-cell>
						</fo:table-row>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block margin-top="4mm" margin-bottom="2mm" font-size="12pt" font-family="Barclays" color="black" text-align="center">
			<fo:inline>We hereby confirm the </fo:inline>
			<fo:inline color="red">RETURN </fo:inline>
			<fo:inline>of the following security </fo:inline>
			<fo:inline color="red">TO YOU</fo:inline>
		</fo:block>
		<fo:block font-size="10pt" font-family="Barclays" color="black">
			<fo:table border-spacing="3pt" table-layout="auto">
				<xsl:for-each select="ReportDetail/HeaderRow/Field">
					<fo:table-column>
						<xsl:attribute name="column-width"><xsl:value-of select="Width"/></xsl:attribute>
					</fo:table-column>
				</xsl:for-each>
				<fo:table-header>
					<fo:table-row>
						<xsl:for-each select="ReportDetail/HeaderRow/Field">
							<fo:table-cell padding="6pt" border="0.5pt solid black" background-color="rgb(0,84,160)">
								<fo:block color="white">
									<xsl:attribute name="text-align"><xsl:value-of select="Alignment"/></xsl:attribute>
									<xsl:value-of select="Value"/>
								</fo:block>
							</fo:table-cell>
						</xsl:for-each>
					</fo:table-row>
				</fo:table-header>
				<fo:table-body>
					<xsl:for-each select="ReportDetail/DataRow">
						<fo:table-row>
							<xsl:for-each select="Field">
								<fo:table-cell padding="6pt" border="0.5pt solid black">
									<fo:block>
										<xsl:attribute name="text-align"><xsl:value-of select="Alignment"/></xsl:attribute>
										<xsl:value-of select="Value"/>
									</fo:block>
								</fo:table-cell>
							</xsl:for-each>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
	</xsl:template>
</xsl:stylesheet>
