#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">
	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="all_pages" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="50mm" margin-bottom="10mm"/>
					<fo:region-before region-name="xsl-region-before" extent="50mm"/>
					<fo:region-after region-name="xsl-region-after" extent="10mm"/>
				</fo:simple-page-master>
				<fo:simple-page-master master-name="last_page" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="50mm" margin-bottom="30mm"/>
					<fo:region-before region-name="xsl-region-before" extent="50mm"/>
					<fo:region-after region-name="xsl-region-after-last" extent="30mm"/>
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
					<fo:block font-size="12pt" font-family="Barclays" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="60mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="after">
										<fo:block text-align="left" font-weight="bold" font-size="14pt">
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
									<fo:table-cell number-rows-spanned="2">
										<fo:block>
											<fo:external-graphic src="file:y:/Jhb/Arena/Prime/FOP/images/AbsaCapital.png" content-width="60mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-top="15pt" display-align="after">
										<fo:block text-align="left" font-weight="bold" font-size="14pt">
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
					<fo:block font-size="8pt" font-family="Barclays" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="80mm"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="90mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block>
											<fo:external-graphic left="0mm" src="file:y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg" content-height="10mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
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
											<fo:external-graphic src="file:y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg" content-height="10mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:static-content flow-name="xsl-region-after-last">
					<fo:block text-align="left" font-weight="bold" font-size="8pt">Note:</fo:block>
					<fo:block text-align="left" font-size="8pt">Unless stated otherwise:</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All prices are in ZAR</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All amounts are in ZAR</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All rates are in percentage points</fo:block>
					<fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
					<fo:block font-size="8pt" font-family="Barclays" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="80mm"/>
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="90mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block>
											<fo:external-graphic left="0mm" src="file:y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg" content-height="10mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
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
											<fo:external-graphic src="file:y:/Jhb/Arena/Prime/FOP/images/FooterRight.jpg" content-height="10mm" scaling="uniform"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
					</fo:block>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="page">
						<!-- Row Label Column width -->
						<xsl:for-each select="//ReportParameters/ColumnWidths/c">
							<xsl:if test="@id = 0">
								<xsl:variable name="colWidth" select="text()"/>
								<fo:table-column>
									<xsl:attribute name="column-width"><xsl:value-of select="$colWidth"/></xsl:attribute>
								</fo:table-column>
							</xsl:if>
						</xsl:for-each>
						<!-- Set all columns to proportional width -->
						<xsl:for-each select="//Columns/Column">
							<xsl:variable name="colPos" select="position()"/>
							<xsl:for-each select="//ReportParameters/ColumnWidths/c">
								<xsl:if test="$colPos = @id">
									<xsl:variable name="colWidth" select="text()"/>
									<fo:table-column>
										<xsl:attribute name="column-width"><xsl:value-of select="$colWidth"/></xsl:attribute>
									</fo:table-column>
								</xsl:if>
							</xsl:for-each>
						</xsl:for-each>
						<fo:table-header>
							<fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt" display-align="center">
								<!--Row Label Column-->
								<fo:table-cell>
									<fo:block text-align="left" font-weight="bold" padding-bottom="0.5mm" padding-top="0.5mm" padding-right="0.5mm">
										</fo:block>
								</fo:table-cell>
								<!--Worksheet Columns-->
								<xsl:for-each select="//Columns/Column">
									<fo:table-cell>
										<fo:block text-align="right" font-weight="bold" padding-bottom="0.5mm" padding-top="0.5mm" padding-right="0.5mm">
											<xsl:value-of select="Label"/>
										</fo:block>
									</fo:table-cell>
								</xsl:for-each>
							</fo:table-row>
						</fo:table-header>
						<fo:table-body>
							<xsl:apply-templates/>
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
		<fo:table-row border-bottom-style="dotted">
			<xsl:if test="$treeDepth='1' ">
				<!--Sets Top Level grouping format-->
				<xsl:attribute name="font-weight">bold</xsl:attribute>
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour1"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='2' ">
				<!--Sets 2nd Level grouping format-->
				<xsl:attribute name="font-weight">bold</xsl:attribute>
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour2"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='3' ">
				<!--Sets 3rd Level grouping format-->
				<xsl:attribute name="font-weight">bold</xsl:attribute>
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour3"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="$treeDepth='4' ">
				<!--Sets 4th Level grouping format-->
				<xsl:attribute name="font-weight">bold</xsl:attribute>
				<xsl:attribute name="background-color"><xsl:value-of select="//ReportParameters/GroupingLevelBackgroundColour/colour4"/></xsl:attribute>
			</xsl:if>
			<!-- Row Label -->
			<fo:table-cell display-align="center">
				<xsl:attribute name="padding-left"><xsl:value-of select="($treeDepth - 1) * 6"/>pt
				</xsl:attribute>
				<xsl:if test="$treeDepth='1'">
					<xsl:attribute name="padding-top">2pt</xsl:attribute>
					<xsl:attribute name="padding-bottom">2pt</xsl:attribute>
				</xsl:if>
				<fo:block text-align="left" vertical-align="middle">
					<xsl:value-of select="Label"/>
				</fo:block>
			</fo:table-cell>
			<!-- Data Columns -->
			<xsl:for-each select="Cells/Cell">
				<fo:table-cell display-align="center">
					<xsl:if test="$treeDepth='1'">
					<xsl:attribute name="padding-top">2pt</xsl:attribute>
					<xsl:attribute name="padding-bottom">2pt</xsl:attribute>
					</xsl:if>
					<fo:block text-align="right" vertical-align="middle">
						<xsl:value-of select="FormattedData"/>
					</fo:block>
				</fo:table-cell>
			</xsl:for-each>
		</fo:table-row>
		<xsl:apply-templates select="Rows/Row">
			<xsl:with-param name="treeDepth" select="$treeDepth + 1"/>
		</xsl:apply-templates>
	</xsl:template>
</xsl:stylesheet>

