#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf
#grouping: aef reporting/style sheets

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
				<fo:simple-page-master master-name="last_page" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="45mm" margin-bottom="25mm"/>
					<fo:region-before region-name="xsl-region-before" extent="45mm"/>
					<fo:region-after region-name="xsl-region-after-last" extent="24mm"/>
				</fo:simple-page-master>
				<fo:page-sequence-master master-name="page_sequence">
					<fo:repeatable-page-master-alternatives>
						<fo:conditional-page-master-reference master-reference="last_page" page-position="last"/>
						<fo:conditional-page-master-reference master-reference="all_pages"/>
					</fo:repeatable-page-master-alternatives>
				</fo:page-sequence-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="page_sequence">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="SansSerif" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="65mm"/>
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
										<fo:block>
											<fo:external-graphic content-width="65mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
											file:y:/Jhb/Arena/Prime/FOP/images/AbsaCapital.png
											</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
											/apps/services/front/FOP/fop-1.0/Images/AbsaCapital.png
											</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="before">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
											<xsl:value-of select="//ReportParameters/ReportName"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="//ReportParameters/DateToday"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell padding-top="15pt" display-align="after">
										<fo:block text-align="left" font-weight="bold" font-size="12pt">
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
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
											file:y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg
											</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
											/apps/services/front/FOP/fop-1.0/Images/FooterLeft.jpg
											</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/></fo:inline>
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
											file:y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg
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
				<fo:static-content flow-name="xsl-region-after-last">
					<fo:block text-align="left" font-weight="bold" font-size="8pt">Notes:</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All exposures are stated in ZAR</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All returns are stated in percentage points</fo:block>
					<fo:block text-align="left" font-size="8pt"> - Equity exposure represents market exposure</fo:block>
					<fo:block text-align="left" font-size="8pt"> - Fixed Income exposure represents market value</fo:block>
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
											file:y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg
											</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
											/apps/services/front/FOP/fop-1.0/Images/FooterLeft.jpg
											</xsl:if></xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/></fo:inline>
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
											file:y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg
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
					<fo:table table-layout="fixed" font-size="9pt" border-spacing="2pt" break-after="page">
						<fo:table-column column-width="60mm"/><!-- Label -->
						<fo:table-column column-width="proportional-column-width(1)"/><!-- White Space -->
						<fo:table-column column-width="40mm"/><!-- Gross Exposure -->
						<fo:table-column column-width="40mm"/><!-- Net Exposure -->


						<fo:table-header>
							<fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt">
								<fo:table-cell>
									<fo:block text-align="left"  font-weight="bold"></fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right"  font-weight="bold"></fo:block>
								</fo:table-cell>
								<fo:table-cell>
									<fo:block text-align="right"  font-weight="bold">Gross</fo:block>
									<fo:block text-align="right"  font-weight="bold">Exposure</fo:block>
								</fo:table-cell>
								<fo:table-cell padding-right='5pt'>
									<fo:block text-align="right"  font-weight="bold">Net</fo:block>
									<fo:block text-align="right"  font-weight="bold">Exposure</fo:block>
								</fo:table-cell>

							</fo:table-row>
						</fo:table-header>
						<fo:table-body>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='Equity']"/>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='FixedIncome']"/>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='Cash']"/>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='Total']"/>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='Leverage']"/>
							<xsl:apply-templates select="PRIMEReport/ReportDetail/ReportSection[@Name='NAV']"/>
						</fo:table-body>
					</fo:table>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	<xsl:template match="ReportSection">
		<xsl:if test="@Name='Equity'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">Equity</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

		<xsl:if test="@Name='FixedIncome'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">Fixed Income</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid' border-top-style='solid'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid' border-top-style='solid' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

		<xsl:if test="@Name='Cash'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">Cash</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid' border-top-style='solid'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-bottom-style='solid' border-top-style='solid' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

		<xsl:if test="@Name='Total'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">Total Exposure</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-top-style='solid'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' border-top-style='solid' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

		<xsl:if test="@Name='Leverage'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">Leverage</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

		<xsl:if test="@Name='NAV'">
			<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
				<fo:table-cell padding-top='10pt' padding-left='5pt'>
					<fo:block text-align="left"  font-weight="bold">NAV</fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/GrossExposure"/></fo:block>
				</fo:table-cell>
				<fo:table-cell padding-top='10pt' padding-right='5pt'>
					<fo:block text-align="right"  font-weight="bold"><xsl:value-of select="ReportRow[@Label='Total']/NetExposure"/></fo:block>
				</fo:table-cell>
			</fo:table-row>
			<xsl:apply-templates select="ReportRow"/>
		</xsl:if>

	</xsl:template>

	<xsl:template match="ReportRow">
		<xsl:if test="@Label != 'Total'">
		<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
			<fo:table-cell padding-left='10pt'>
				<fo:block text-align="left"  font-weight="normal"><xsl:value-of select="@Label"/></fo:block>
			</fo:table-cell>
				<fo:table-cell padding-top='10pt'>
					<fo:block text-align="left"  font-weight="bold"></fo:block>
				</fo:table-cell>
			<fo:table-cell background-color='#d1d1d1' border-left-style='solid' >
				<fo:block text-align="right"  font-weight="normal"><xsl:value-of select="GrossExposure"/></fo:block>
			</fo:table-cell>
			<fo:table-cell background-color='#d1d1d1' border-right-style='solid' padding-right='5pt'>
				<fo:block text-align="right"  font-weight="normal"><xsl:value-of select="NetExposure"/></fo:block>
			</fo:table-cell>
		</fo:table-row>
		</xsl:if>
	</xsl:template>

</xsl:stylesheet>
