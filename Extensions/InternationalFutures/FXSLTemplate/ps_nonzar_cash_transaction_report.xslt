#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">
	<!-- set the number of data columns on one page of the report -->
	<xsl:variable name="columns_per_page" select="6"/>

	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="first" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="5mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="45mm" margin-bottom="25mm"/>
					<fo:region-before extent="45mm"/>
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
										<fo:block>
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
					<fo:block text-align="left" font-size="8pt"> - All amounts are in ZAR</fo:block>
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
											<fo:external-graphic left="0mm" content-height="10mm" scaling="uniform">
												<xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
														file:Y:/Jhb/Arena/Prime/FOP/images/FooterLeft.jpg
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
					<xsl:call-template name="loop-up-to-over">
						<xsl:with-param name="over" select="$columns_per_page"/>
						<xsl:with-param name="count" select="count(/PRIMEReport/ReportContents/Table/Rows/Row/Rows/Row)"/>
						<xsl:with-param name="scope" select="/PRIMEReport/ReportContents/Table/Rows/Row/Rows"/>
					</xsl:call-template>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>

	<!-- generates the given $content $count-times -->
	<xsl:template name="generate-columns">
		<xsl:param name="count"/>
		<xsl:param name="content"/>
		<xsl:if test="$count > 0">
			<xsl:copy-of select="$content"/>
			<xsl:call-template name="generate-columns">
				<xsl:with-param name="count" select="$count - 1"/>
				<xsl:with-param name="content" select="$content"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>

	<xsl:template name="generate-cell">
		<xsl:param name="content"/>
		<xsl:choose>
			<xsl:when test="Cells/Cell[4]/FormattedData = 'BASE'">
				<fo:table-cell padding="2.5pt" border-left-style="dotted" border-left-color="black">
					<fo:block text-align="right"><xsl:value-of select="$content"/></fo:block>
				</fo:table-cell>
			</xsl:when>
			<xsl:otherwise>
				<fo:table-cell padding="2.5pt">
					<fo:block text-align="right"><xsl:value-of select="$content"/></fo:block>
				</fo:table-cell>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="Rows">
		<xsl:param name="i"/>
		<xsl:param name="count"/>

		<!--
			$i contains the number of the first column, that will be displayed on a page
			$count contains the total number of currencies

			(The "Cells/Cell[4]/FormattedData" selector determines the account type
			(LOCAL or BASE) for each row.)
		-->

		<!-- calculate the required number of columns -->
		<xsl:variable name="stop" select="$i+$columns_per_page"/>
		<xsl:variable name="current_column_count">
			<xsl:choose>
				<xsl:when test="$stop > ($count+1)"><xsl:value-of select="$count - $i + 1"/></xsl:when>
				<xsl:otherwise><xsl:value-of select="$columns_per_page"/></xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" break-after="page">
			<fo:table-column column-width="proportional-column-width(1)"/>
            <xsl:if test="$count &gt; 1">

                <!-- generate the column specifications -->
                <xsl:call-template name="generate-columns">
                    <xsl:with-param name="count" select="$current_column_count"/>
                    <xsl:with-param name="content">
                        <fo:table-column column-width="35mm"/>
                    </xsl:with-param>
                </xsl:call-template>

                <fo:table-header>
                    <fo:table-row>
                        <fo:table-cell>
                            <fo:block></fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding="2.5pt" border-left-style="dotted" border-left-color="black">
                            <xsl:attribute name="number-columns-spanned"><xsl:value-of select="$current_column_count - 1"/></xsl:attribute>
                            <fo:block text-align="center" font-weight="bold"><fo:inline>Settlement currency</fo:inline></fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding="2.5pt" border-left-style="dotted" border-left-color="black">
                            <fo:block text-align="center" font-weight="bold"><fo:inline>Reporting currency</fo:inline></fo:block>
                        </fo:table-cell>
                    </fo:table-row>
                    <fo:table-row border-top="solid black 1pt" border-bottom-style="dotted" border-bottom-color="Gray">
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left" font-weight="bold"><fo:inline>Currency</fo:inline></fo:block>
                        </fo:table-cell>
                        <!-- generate the column headers -->
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/><!-- Put the BASE account on the last position. -->
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:choose>
                                    <xsl:when test="Cells/Cell[4]/FormattedData = 'BASE'">
                                        <fo:table-cell padding="2.5pt" border-left-style="dotted" border-left-color="black">
                                            <fo:block text-align="right" font-weight="bold">
                                                <xsl:value-of select="Cells/Cell[3]/FormattedData"/>
                                            </fo:block>
                                        </fo:table-cell>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <fo:table-cell padding="2.5pt">
                                            <fo:block text-align="right" font-weight="bold">
                                                <xsl:value-of select="Cells/Cell[3]/FormattedData"/>
                                            </fo:block>
                                        </fo:table-cell>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                </fo:table-header>
                <fo:table-body table-layout="fixed" font-size="8pt" border-spacing="2pt">
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Opening Balance</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[1]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Daily PnL</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[2]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Execution fees rebate</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[8]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Margin Payments</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[7]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Interest Capitalised &amp; Adjustments</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[6]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Sundry Charges</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[9]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <!-- fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Interest Capitalised</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[5]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row-->
                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Closing Balance</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[11]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Payments In Processing</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[15]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>

                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <fo:table-cell padding="2.5pt">
                            <xsl:attribute name="number-columns-spanned"><xsl:value-of select="$current_column_count + 1"/></xsl:attribute>
                            <fo:block text-align="center" font-weight="bold"><fo:inline></fo:inline></fo:block>
                        </fo:table-cell>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Initial Margin</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[19]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Variation Margin</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[20]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Total Portfolio Margin Requirement</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[12]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>

                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <fo:table-cell padding="2.5pt">
                            <xsl:attribute name="number-columns-spanned"><xsl:value-of select="$current_column_count + 1"/></xsl:attribute>
                            <fo:block text-align="center" font-weight="bold"><fo:inline></fo:inline></fo:block>
                        </fo:table-cell>
                    </fo:table-row>

                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Due to you</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[16]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>

                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Due to you [indicative ZAR amount]</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[17]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="solid" border-bottom-color="black">
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Call Account Interest</fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding="2.5pt">
                            <xsl:attribute name="number-columns-spanned"><xsl:value-of select="$current_column_count"/></xsl:attribute>
                            <fo:block text-align="center" font-weight="bold"><fo:inline></fo:inline></fo:block>
                        </fo:table-cell>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Client Interest Rate</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[22]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Daily Interest Accrued</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[21]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">Month to Date Interest Accrued</fo:block>
                        </fo:table-cell>
                        <xsl:for-each select="Row">
                            <xsl:sort select="Cells/Cell[4]/FormattedData" order="descending"/>
                            <xsl:if test="(position() >= $i) and (position() &lt; ($i + $current_column_count))">
                                <xsl:call-template name="generate-cell">
                                    <xsl:with-param name="content" select="Cells/Cell[18]/FormattedData"/>
                                </xsl:call-template>
                            </xsl:if>
                        </xsl:for-each>
                    </fo:table-row>
                </fo:table-body>
            </xsl:if>
            <xsl:if test="$count &lt;= 1">
                <fo:table-body table-layout="fixed" font-size="8pt" border-spacing="2pt">
                    <fo:table-row border-bottom-style="dotted" border-bottom-color="Gray">
                        <fo:table-cell padding="2.5pt">
                            <fo:block text-align="left">
                                No active international accounts.
                            </fo:block>
                        </fo:table-cell>
                    </fo:table-row>
                </fo:table-body>
            </xsl:if>
		</fo:table>
	</xsl:template>

	<!--
		loops for XSLT
		loop-from-to-over: a general loop
		loop-up-to-over: a shortcut for the general loop from 1

		all loops require a scope parameter:
			scope must be absolute
			it points to the scope in which apply-templates will be called (useful for callback templates)


		the apply-templates passes the parameters $count, $over and $i, which contains the current position in the loop
	-->


	<!--
		cycle from 1 to $count over $over positions in each step in the given $scope
		i.e. up-to 10 over 5: [1,6]
	-->
	<xsl:template name="loop-up-to-over">
		<xsl:param name="count"/>
		<xsl:param name="scope"/>
		<xsl:param name="over"/>

		<xsl:call-template name="loop-from-to-over">
			<xsl:with-param name="i" select="1"/>
			<xsl:with-param name="count" select="$count"/>
			<xsl:with-param name="scope" select="$scope"/>
			<xsl:with-param name="over" select="$over"/>
		</xsl:call-template>
	</xsl:template>


	<!--
		loop from $i to $count over $over positions in each step
		loop-from 3 to 13 over 3: [3, 6, 9, 12]
	-->
	<xsl:template name="loop-from-to-over">
		<xsl:param name="count"/>
		<xsl:param name="i"/>
		<xsl:param name="scope"/>
		<xsl:param name="over"/>

		<!-- callback dispatcher is not assigned -->
		<xsl:apply-templates select="$scope">
			<xsl:with-param name="i" select="$i"/>
			<xsl:with-param name="count" select="$count"/>
			<xsl:with-param name="over" select="$over"/>
		</xsl:apply-templates>

		<xsl:if test="($i+$over) &lt;= $count">
			<xsl:call-template name="loop-from-to-over">
				<xsl:with-param name="count" select="$count"/>
				<xsl:with-param name="over" select="$over"/>
				<xsl:with-param name="i" select="$i+$over"/>
				<xsl:with-param name="scope" select="$scope"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
