#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<!-- A descendant of ps_cash_transaction_report, meant to be used in conjunction with the PBA_CallAccount workbook. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">
	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="first" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="5mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="50mm" margin-bottom="25mm"/>
					<fo:region-before extent="50mm"/>
					<fo:region-after extent="25mm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="first">
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
										<fo:block text-align="right">
											
											<fo:external-graphic content-height="25mm" scaling="uniform" padding-top="15pt">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
											file:y:/Jhb/Arena/Prime/FOP/images/absa_barclays_combined.png
											</xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
											/apps/services/front/FOP/fop-1.0/Images/absa_barclays_combined.png
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
					<fo:block text-align="left" font-weight="bold" font-size="8pt">Notes:</fo:block>
					<fo:block text-align="left" font-size="8pt">Unless stated otherwise:</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All amounts are in account's currency</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All rates are in percentage points</fo:block>
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
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/>
											</fo:inline>
										</fo:block>
										<fo:block text-align="center">
											<fo:inline>
												<xsl:if test="//PRIMEReport/ReportParameters/FrameworkVersion">Generated using <xsl:value-of select="//PRIMEReport/ReportParameters/FrameworkVersion"/> at </xsl:if>
												<xsl:value-of select="//Time"/>
											</fo:inline>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="3">
										<fo:block>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<xsl:apply-templates select="/PRIMEReport/ReportContents/Table/Rows/Row/Rows"/>
					<xsl:apply-templates select="/PRIMEReport/ReportContents/Table/Rows/Row/Rows/Row" mode="details"/>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	
	<xsl:template match="Rows">
		<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="page">
			<fo:table-column column-width="proportional-column-width(1)"/>
			<fo:table-body>
				<fo:table-row>
					<fo:table-cell>
						<fo:block>
							<xsl:apply-templates select="Row" mode="summary"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row>
					<fo:table-cell>
						<fo:block>
							<fo:table margin-top="10mm" table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="auto" keep-together.within-column="always">
								<!--<xsl:attribute name="background-color">#D5F3FF</xsl:attribute>-->
								<xsl:attribute name="background-color">#E2F0FF</xsl:attribute>
								<fo:table-column column-width="proportional-column-width(1)"/>
								<fo:table-column column-width="25mm"/>
								<fo:table-body table-layout="fixed" font-size="8pt" border-spacing="2pt">
									<fo:table-row border-top="double black 2pt" border-bottom="solid black 2pt" >
										<fo:table-cell padding="2.5pt">
											<fo:block font-weight="bold" >Total Closing Balance in USD:</fo:block>
										</fo:table-cell>
										<fo:table-cell padding="2.5pt">
											<fo:block text-align="right" font-weight="bold">
												<xsl:value-of select="//PRIMEReport/ReportContents/Table/Rows/Row/Cells/Cell[15]/FormattedData"/>
											</fo:block>
										</fo:table-cell>
									</fo:table-row>
								</fo:table-body>
							</fo:table>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
			</fo:table-body>
		</fo:table>
	</xsl:template>
	
	<!-- Single Summary Page template -->
	<xsl:template match="Row" mode="summary">
		<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="auto" keep-together.within-column="always">
			<fo:table-column column-width="proportional-column-width(1)"/>
			<fo:table-column column-width="25mm"/>
			<fo:table-header>
				<fo:table-row border-top="solid black 1pt">
					<fo:table-cell padding="2.5pt">
						<fo:table>
							<fo:table-column/>
							<fo:table-column/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell>
										<fo:block font-weight="bold">Account Number: <xsl:value-of select="/Cells/Cell[18]/FormattedData"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell>
										<fo:block text-align="left" font-weight="bold">Currency: <xsl:value-of select="Cells/Cell[13]/FormattedData"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right" font-weight="bold">Amount</fo:block>
					</fo:table-cell>
				</fo:table-row>
			</fo:table-header>
			<fo:table-body table-layout="fixed" font-size="8pt" border-spacing="2pt">
				<fo:table-row border-top-style="solid">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Closing Balance</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[8]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-top-style="dotted">
					<!--<xsl:attribute name="background-color">#D5F3FF</xsl:attribute>-->
					<xsl:attribute name="background-color">#E2F0FF</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Closing Balance in USD</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[15]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<!-- START: ver2 -->
				<fo:table-row border-top-style="dotted" border-top-color="Gray" border-bottom-style="solid" border-bottom-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">USD/<xsl:value-of select="Cells/Cell[13]/FormattedData"/> FX Rate</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[17]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<!-- END: ver2 -->
				<!-- START: ver1 -->
				<!--
			<fo:table-row border-top-style="dotted" border-top-color="Gray">
				<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
				<fo:table-cell padding="2.5pt">
					<fo:block text-align="left">USD/<xsl:value-of select="Cells/Cell[13]/FormattedData"/> FX Rate</fo:block>
				</fo:table-cell>
				<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
					<fo:block text-align="right">
						<xsl:value-of select="Cells/Cell[17]/FormattedData"/>
					</fo:block>
				</fo:table-cell>
			</fo:table-row>
-->
				<!-- START: small gap -->
				<!--				<fo:table-row border-top-style="dotted" border-top-color="Gray" border-bottom-style="solid" border-bottom-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
				</fo:table-row>-->
				<!-- END: small gap -->
				<!-- END: ver1 -->
			</fo:table-body>
		</fo:table>
	</xsl:template>
	<!-- END: Single Summary Page template -->
	
	<xsl:template match="Row" mode="details">
		<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="page">
			<fo:table-column column-width="proportional-column-width(1)"/>
			<fo:table-column column-width="25mm"/>
			<fo:table-header>
				<fo:table-row border-top="solid black 1pt">
					<fo:table-cell padding="2.5pt">
						<fo:table>
							<fo:table-column/>
							<fo:table-column/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell>
										<fo:block font-weight="bold">Account Number: <xsl:value-of select="Cells/Cell[18]/FormattedData"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell>
										<fo:block text-align="left" font-weight="bold">Currency: <xsl:value-of select="Cells/Cell[13]/FormattedData"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right" font-weight="bold">Amount</fo:block>
					</fo:table-cell>
				</fo:table-row>
			</fo:table-header>
			<fo:table-body table-layout="fixed" font-size="8pt" border-spacing="2pt">
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray" border-top-style="solid">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Opening Balance</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[1]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Movement</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[2]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Execution Fee Rebate</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[3]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Margin Payment</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[4]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Stock Lending Fees Earned</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[5]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Sundry Charges</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[6]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Interest Capitalised</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[7]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Closing Balance</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[8]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Due <xsl:if test="Cells/Cell[9]/RawData &lt; 0">From You</xsl:if>
							<xsl:if test="Cells/Cell[9]/RawData &gt; 0">To You</xsl:if>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt" border-bottom-style="double" border-bottom-width="3pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[9]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row>
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray" border-top-style="solid" border-top-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Closing Balance in ZAR</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[14]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="solid" border-bottom-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">ZAR/<xsl:value-of select="Cells/Cell[13]/FormattedData"/> FX Rate</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[16]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<!-- START: small gap -->
				<fo:table-row>
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
					<fo:table-cell padding="3pt">
						<fo:block/>
					</fo:table-cell>
				</fo:table-row>
				<!-- END: small gap -->
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray" border-top-style="solid" border-top-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Closing Balance in USD</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[15]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="solid" border-bottom-color="Black">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">USD/<xsl:value-of select="Cells/Cell[13]/FormattedData"/> FX Rate</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt" border-top-style="solid" border-top-width="1pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[17]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="solid">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="10pt">
						<fo:block/>
					</fo:table-cell>
					<fo:table-cell padding="10pt">
						<fo:block/>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="solid">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left" font-weight="bold">Call Account Interest</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right"/>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Current Rate</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[10]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Daily Interest Accrual</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[11]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
				<fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
					<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="left">Monthly Interest Accrual</fo:block>
					</fo:table-cell>
					<fo:table-cell padding="2.5pt">
						<fo:block text-align="right">
							<xsl:value-of select="Cells/Cell[12]/FormattedData"/>
						</fo:block>
					</fo:table-cell>
				</fo:table-row>
			</fo:table-body>
		</fo:table>
	</xsl:template>
</xsl:stylesheet>
