#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">
	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="all_pages" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="45mm" margin-bottom="10mm"/>
					<fo:region-before region-name="xsl-region-before" extent="45mm"/>
					<fo:region-after region-name="xsl-region-after" extent="10mm"/>
				</fo:simple-page-master>
				<fo:page-sequence-master master-name="page_sequence">
					<fo:repeatable-page-master-alternatives>
						<fo:conditional-page-master-reference master-reference="all_pages"/>
					</fo:repeatable-page-master-alternatives>
				</fo:page-sequence-master>
			</fo:layout-master-set>
			<!-- Main Report -->
			<fo:page-sequence master-reference="page_sequence">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="SansSerif" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="80mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="before">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/FullName"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/Address"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/City"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/ZipCode"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/Country"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell number-rows-spanned="1">
										<fo:block text-align="right">
											<fo:external-graphic content-width="65mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/AbsaCapital.png
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/AbsaCapital.png
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="after">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
											<xsl:value-of select="//ReportParameters/ReportName"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/PortfolioEndDate"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:static-content flow-name="xsl-region-after">
					<fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
					<fo:block font-size="8pt" font-family="SansSerif" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="80mm"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="90mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block>
											<fo:external-graphic left="0mm" content-height="10mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/FooterLeft.jpg
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2" display-align="center">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/>
											</fo:inline>
										</fo:block>
										<fo:block text-align="center">
											<fo:inline>
												<xsl:value-of select="//Time"/>
											</fo:inline>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="3">
										<fo:block>
											<fo:external-graphic content-height="10mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/FooterRight.jpg
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<fo:table table-layout="fixed" font-size="7pt" border-spacing="2pt" break-after="page">
						<fo:table-column column-width="17mm"/><!-- Trade -->
						<fo:table-column column-width="17mm"/><!-- Date and Time -->
						<fo:table-column column-width="15mm"/><!-- OTC / Exchange -->
						<fo:table-column column-width="15mm"/><!-- Instrument Type -->
						<fo:table-column column-width="proportional-column-width(1)"/><!-- Instrument -->
						<fo:table-column column-width="15mm"/><!-- Traded Currency -->
						<fo:table-column column-width="17mm"/><!-- Expiry Date -->
						<fo:table-column column-width="7mm"/><!-- B/S -->
						<fo:table-column column-width="7mm"/><!-- Qty -->
						<fo:table-column column-width="15mm"/><!-- Price -->
						<fo:table-column column-width="20mm"/><!-- Barclays Principal fee (settlement) -->
						<fo:table-header>
							<fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt">
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">Trade</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">Date &amp; Time</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">OTC / Exchange</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">Instrument Type</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">Instrument</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold">Traded Currency</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right" font-weight="bold">Expiry Date</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right" font-weight="bold">B/S</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right" font-weight="bold">Qty</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right" font-weight="bold">Price</fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right" font-weight="bold">Barclays Principal fee (settlement)</fo:block>
								</fo:table-cell>
							</fo:table-row>
						</fo:table-header>
                            <xsl:if test="/PRIMEReport/ReportContents">
                                <fo:table-body>
                                    <xsl:apply-templates/>
                                </fo:table-body>
                            </xsl:if>
                            <xsl:if test="not(/PRIMEReport/ReportContents)">
                                <fo:table-body>
								    <fo:table-row>
                                        <fo:table-cell>
                                            <fo:block>
                                                No data.
                                            </fo:block>
                                        </fo:table-cell>
								    </fo:table-row>
                                </fo:table-body>
                            </xsl:if>
					</fo:table>
				</fo:flow>
			</fo:page-sequence>
			<!-- Disclaimer -->
			<fo:page-sequence master-reference="page_sequence">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="SansSerif" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="80mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="before">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/FullName"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/Address"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/City"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/ZipCode"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/ClientDetails/Country"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell number-rows-spanned="1">
										<fo:block text-align="right">
											<fo:external-graphic content-width="65mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/AbsaCapital.png
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/AbsaCapital.png
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="after">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
											<xsl:value-of select="//ReportParameters/ReportName"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/PortfolioEndDate"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:static-content flow-name="xsl-region-after">
					<fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
					<fo:block font-size="8pt" font-family="SansSerif" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="80mm"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="90mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block>
											<fo:external-graphic left="0mm" content-height="10mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/FooterLeft.jpg
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2" display-align="center">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/>
											</fo:inline>
										</fo:block>
										<fo:block text-align="center">
											<fo:inline>
												<xsl:value-of select="//Time"/>
											</fo:inline>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="3">
										<fo:block>
											<fo:external-graphic content-height="10mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg
														</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
														/apps/services/front/FOP/fop-1.0/Images/FooterRight.jpg
												</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="page">
						<fo:table-column column-width="proportional-column-width(1)"/>
						<!-- Label -->
						<fo:table-header>
							<fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt">
								<fo:table-cell>
									<fo:block text-align="left" font-family="SansSerif" font-weight="bold">Notes</fo:block>
								</fo:table-cell>
							</fo:table-row>
						</fo:table-header>
						<fo:table-body>
							<fo:table-row border-top="solid black 1pt">
								<fo:table-cell>
									<fo:block text-align="left" font-family="SansSerif" font-size="8pt">1) All Barclays Principal fees are zero rated for VAT purposes.</fo:block>
								</fo:table-cell>
							</fo:table-row>
						</fo:table-body>
					</fo:table>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	<xsl:template match="Table">
		<xsl:apply-templates select="Rows/Row">
			<xsl:with-param name="treeDepth" select="1"/>
		</xsl:apply-templates>
	</xsl:template>
	<xsl:template match="Row">
		<xsl:param name="treeDepth"/>
		<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
			<xsl:if test="$treeDepth='1' ">
				<!--Sets Top Level grouping format-->
				<!-- <xsl:attribute name="font-weight">bold</xsl:attribute> -->
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour1"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='2' ">
				<!--Sets 2nd Level grouping format-->
				<!-- <xsl:attribute name="font-weight">bold</xsl:attribute> -->
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour2"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='3' ">
				<!--Sets 3rd Level grouping format-->
				<!-- <xsl:attribute name="font-weight">bold</xsl:attribute> -->
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour3"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='4' ">
				<!--Sets 4th Level grouping format-->
				<!-- <xsl:attribute name="font-weight">bold</xsl:attribute> -->
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour4"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='5' ">
				<!--Sets 5th Level grouping format-->
				<!-- <xsl:attribute name="font-weight">bold</xsl:attribute> -->
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour5"/></xsl:attribute>
			</xsl:if>
			<fo:table-cell display-align="center">
				<xsl:attribute name="padding-left"><xsl:value-of select="($treeDepth - 1) * 6"/>pt
				</xsl:attribute>
				<xsl:if test="$treeDepth='1' ">
					<fo:block text-align="left" vertical-align="middle">
					</fo:block>
				</xsl:if>
				<xsl:if test="$treeDepth &gt; '1' ">
					<fo:block text-align="left" vertical-align="middle">
						<xsl:value-of select="Label"/>
					</fo:block>
				</xsl:if>
			</fo:table-cell>
			<!-- Instrument Type Column -->
			<xsl:for-each select="Cells/Cell">
				<xsl:if test="position() &lt;= 5">
					<fo:table-cell display-align="center">
						<fo:block text-align="left">
							<xsl:value-of select="FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</xsl:if>
			</xsl:for-each>
			<!-- Other Columns -->
			<xsl:for-each select="Cells/Cell">
				<xsl:if test="position() > 5">
					<fo:table-cell display-align="center">
						<fo:block text-align="right">
							<xsl:value-of select="FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</xsl:if>
			</xsl:for-each>
		</fo:table-row>
		<xsl:apply-templates select="Rows/Row">
			<xsl:with-param name="treeDepth" select="$treeDepth + 1"/>
		</xsl:apply-templates>
	</xsl:template>
</xsl:stylesheet>
