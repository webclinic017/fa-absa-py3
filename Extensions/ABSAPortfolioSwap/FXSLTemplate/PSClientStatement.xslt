<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://fron.com/arena/primereport">
	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="first" page-height="210mm" page-width="297mm" margin-top="0mm" margin-bottom="0mm" margin-left="0mm" margin-right="0mm">
					<!-- Make area's diff colurs so we can see -->
					<fo:region-body margin-bottom="20mm" margin-top="59mm"/>  
					<fo:region-before region-name="header-first"/> 	
					<fo:region-after region-name="footer-first" extent="20mm"/> 
				</fo:simple-page-master>
				<fo:simple-page-master master-name="rest" page-height="210mm" page-width="297mm" margin-top="0mm" margin-bottom="0mm" margin-left="0mm" margin-right="0mm">
					<fo:region-body margin-bottom="20mm" margin-top="20mm"/>
					<fo:region-before region-name="header-rest"/> 	
					<fo:region-after region-name="footer-rest" extent="20mm"/>
				</fo:simple-page-master>
				<!-- Determine the sequence -->
				<fo:page-sequence-master master-name="document">
					<fo:repeatable-page-master-alternatives>
						<fo:conditional-page-master-reference page-position="first" master-reference="first"/>
						<fo:conditional-page-master-reference page-position="rest"  master-reference="rest"/>
					</fo:repeatable-page-master-alternatives>
				</fo:page-sequence-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="document">
				<fo:static-content flow-name="header-first">
					<fo:block><fo:external-graphic src="y:/jhb/arena/prime/fop/images/CFDReportheader.jpg" content-width="292mm" scaling="uniform"/></fo:block>
					<fo:table table-layout="fixed" margin-left="8mm">
						<fo:table-column column-width="3cm"/>
						<fo:table-column column-width="0.5cm"/>
						<fo:table-column column-width="8cm"/>
						<fo:table-column column-width="7cm"/>
						<fo:table-column column-width="1.5cm"/>
						<fo:table-column column-width="1cm"/>
						<fo:table-column column-width="7cm"/>
						<fo:table-body>
							<fo:table-row background-color="#d5e0e4">
										<fo:table-cell border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" padding-before="2mm" number-columns-spanned="4" display-align="before"><fo:block text-align="left" font-size="9pt" font-weight="bold" font-family="Barclays"><xsl:value-of select="/Client_Statement/ClientDetails/ClientFullName"/></fo:block></fo:table-cell>
										<fo:table-cell border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" padding-before="2mm" number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-size="9pt" font-weight="bold" font-family="Barclays">Absa Capital Prime Services</fo:block></fo:table-cell>
							</fo:table-row>
							<fo:table-row background-color="#d5e0e4">
										<fo:table-cell border-left-width="1pt" border-left-style="solid" number-columns-spanned="4" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/ClientDetails/Address"/>,<xsl:value-of select="/Client_Statement/ClientDetails/Address2"/>,<xsl:value-of select="/Client_Statement/ClientDetails/City"/>,<xsl:value-of select="/Client_Statement/ClientDetails/ZipCode"/></fo:block></fo:table-cell>
										<fo:table-cell border-right-width="1pt" border-right-style="solid" number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Absa Bank Limited, 15 Alice Lane,Sandton,Johannesburg,2196</fo:block></fo:table-cell>
							</fo:table-row>
							<fo:table-row background-color="#d5e0e4">
										<fo:table-cell display-align="before" border-left-width="1pt" border-left-style="solid"><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Tel</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">:</fo:block></fo:table-cell>
										<fo:table-cell display-align="before" border-right-width="1pt" border-right-style="solid"><fo:block text-align="left" font-size="8pt" font-family="Barclays">011 895 5164</fo:block></fo:table-cell>
							</fo:table-row>
							<fo:table-row background-color="#d5e0e4">
										<fo:table-cell display-align="before" border-left-width="1pt" border-left-style="solid" ><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Email</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">:</fo:block></fo:table-cell>
										<fo:table-cell display-align="before" border-right-width="1pt" border-right-style="solid" ><fo:block text-align="left" font-size="8pt" font-family="Barclays">abcapprimesynthetics@absacapital.com</fo:block></fo:table-cell>
							</fo:table-row>
							<fo:table-row background-color="#d5e0e4">
										<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-left-width="1pt" border-left-style="solid" border-right-width="1pt" border-right-style="solid"  padding-before="2mm" display-align="before" number-columns-spanned="7"><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
							</fo:table-row>
						</fo:table-body>	
					</fo:table>	
				</fo:static-content>
				<!-- Maybe Apply Template here -->
				<!-- How do you make an every page footer -->
				<!-- What if body-first extends past first page -->
				<fo:static-content flow-name="footer-first">
					<fo:table table-layout="fixed" margin-left="4mm" margin-right="8mm">
						<fo:table-column column-width="14.5cm"/>
						<fo:table-column column-width="89mm"/>
						<fo:table-column column-width="5.5cm"/>
						<fo:table-body>
							<fo:table-row>
								<fo:table-cell display-align="left"><fo:block text-align="left"><fo:external-graphic left="0mm" src="y:/jhb/arena/prime/fop/images/FooterLeft.jpg" content-height="10mm" scaling="uniform"/></fo:block></fo:table-cell>
								<fo:table-cell display-align="center"><fo:block font-size="9pt" font-family="Times Roman"><fo:page-number/></fo:block></fo:table-cell>
								<fo:table-cell display-align="right"><fo:block text-align="right"><fo:external-graphic src="y:/jhb/arena/prime/fop/images/FooterRight.jpg" content-height="10mm" scaling="uniform"/></fo:block></fo:table-cell>
							</fo:table-row>
						</fo:table-body>	
					</fo:table>	
				</fo:static-content>
				<fo:static-content flow-name="header-rest">
					<fo:block><fo:external-graphic src="y:/jhb/arena/prime/fop/images/ABSACapitalHeader.jpg" content-width="291mm" scaling="uniform"/></fo:block>
				</fo:static-content>
				<fo:static-content flow-name="footer-rest">
					<fo:table table-layout="fixed" margin-left="4mm" margin-right="8mm">
						<fo:table-column column-width="14.5cm"/>
						<fo:table-column column-width="89mm"/>
						<fo:table-column column-width="5.5cm"/>
						<fo:table-body>
							<fo:table-row>
								<fo:table-cell><fo:block background-position-horizontal="left top"><fo:external-graphic src="y:/jhb/arena/prime/fop/images/FooterLeft.jpg" content-height="10mm" scaling="uniform"/></fo:block></fo:table-cell>
								<fo:table-cell display-align="center" ><fo:block font-size="9pt" font-family="Barclays"><fo:page-number/></fo:block></fo:table-cell>
								<fo:table-cell><fo:block text-align="right"><fo:external-graphic src="y:/jhb/arena/prime/fop/images/FooterRight.jpg" content-height="10mm" scaling="uniform"/></fo:block></fo:table-cell>
							</fo:table-row>
						</fo:table-body>	
					</fo:table>	
				</fo:static-content>

				<fo:flow flow-name="xsl-region-body">
					<xsl:for-each select="/Client_Statement/Strategy">
						<xsl:variable name="StrategyName"><xsl:value-of select="StrategyName"/></xsl:variable>
						<xsl:variable name="StrategyDate"><xsl:value-of select="StrategyDate"/></xsl:variable>
						<xsl:for-each select="PerformaceSummary">
							<!--CFD Performance Summary-->
							<fo:table table-layout="fixed"  margin-left="8mm">
								<fo:table-column column-width="3cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="4cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
									<fo:table-header>
									
										<fo:table-row>
											<fo:table-cell number-columns-spanned="8"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">CFD PERFORMANCE SUMMARY REPORT</fo:block></fo:table-cell>
										</fo:table-row>

										<fo:table-row>
											<fo:table-cell padding-before="1mm" padding-after="1mm" number-columns-spanned="6"><fo:block text-align="left" font-size="8pt" font-weight="bold" font-family="Barclays">Strategy : <xsl:value-of select="$StrategyName"/></fo:block></fo:table-cell>
											<fo:table-cell margin-right="6mm" padding-before="1mm" padding-after="1mm" number-columns-spanned="2"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="$StrategyDate"/></fo:block></fo:table-cell>
										</fo:table-row>
										
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Market</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Market</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Closing Market</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Closing Market</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Trading Profit/</fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-left-width="1pt" border-left-style="solid" ><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Name</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Position</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Price</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block margin-right="3mm" text-align="right" font-size="8pt" font-family="Barclays">Exposure</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Closing Position</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Price</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block margin-right="3mm" text-align="right" font-size="8pt" font-family="Barclays">Exposure</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="10mm" text-align="right" font-size="8pt" font-family="Barclays">(Loss)</fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-header>
									<fo:table-body>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										
										<xsl:for-each select="Positions/Position">
										<xsl:sort select="CFDName"/>
											<xsl:if test="position() mod 2 != 0"> 
												<fo:table-row>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningPosition"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketPrice"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketExposure"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingPosition"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketPrice"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketExposure"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradingProfitLoss"/></fo:block></fo:table-cell>
												</fo:table-row>
											</xsl:if>
											<xsl:if test="position() mod 2 = 0"> 
												<fo:table-row>
													<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningPosition"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketPrice"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketExposure"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingPosition"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketPrice"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketExposure"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradingProfitLoss"/></fo:block></fo:table-cell>
												</fo:table-row>	
											</xsl:if>
										</xsl:for-each>
										
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block/></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">TOTALS</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Positions/TotalOpeningMarketExposure"/></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Positions/TotalClosingMarketExposure"/></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Positions/TotalTradingProfitLoss"/></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-body>
							</fo:table>
						</xsl:for-each>	
						<!--Trade Activity Report-->
						<xsl:for-each select="TradingActivity">
							<fo:table table-layout="fixed" width ="100%" margin-top="4mm" margin-left="8mm">
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
									<fo:table-header>
										<fo:table-row>
											<fo:table-cell number-columns-spanned="5" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">CFD TRADE ACTIVITY REPORT</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" padding-after="1mm" number-columns-spanned="6"><fo:block text-align="left" font-size="8pt" font-weight="bold" font-family="Barclays">Strategy : <xsl:value-of select="$StrategyName"/></fo:block></fo:table-cell>
											<fo:table-cell margin-right="6mm" padding-before="1mm" padding-after="1mm" number-columns-spanned="2"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="$StrategyDate"/></fo:block></fo:table-cell>
										</fo:table-row>
						<!--
										
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Trade</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										
										-->
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Trade Reference</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Trade Time</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Trade Price</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Trade Quantity</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Buy / Sell</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Trade Exposure</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Execution Premium</fo:block></fo:table-cell>
											<fo:table-cell border-top-width="1pt" border-top-style="solid" border-bottom-width="1pt" border-bottom-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">All in Exposure</fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-header>
									<!--NOTE: remember you always need something inside the body-->
									<fo:table-body>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<xsl:for-each select="Trades/Security">
										
										
											<!-- MMM -->
											<xsl:sort select="TradeInstrument"/>
											<fo:table-row>
												<fo:table-cell number-columns-spanned="3" display-align="left"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeInstrument"/></fo:block></fo:table-cell>
											</fo:table-row>
											<xsl:for-each select="Trade">
											<xsl:if test="position() mod 2 = 0"> 
												<fo:table-row>
													<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeReference"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeTime"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradePrice"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeQuantity"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeBuySell"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeExposure"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeExectionPreium"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeAllInExpsoure"/></fo:block></fo:table-cell>
												</fo:table-row>
											</xsl:if>
											<xsl:if test="position() mod 2 != 0"> 
												<fo:table-row>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeReference"/></fo:block></fo:table-cell>-->
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeTime"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradePrice"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeQuantity"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeBuySell"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeExposure"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeExectionPreium"/></fo:block></fo:table-cell>
													<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TradeAllInExpsoure"/></fo:block></fo:table-cell>
												</fo:table-row>
											</xsl:if>	
											</xsl:for-each>	
											<fo:table-row background-color="#d5e0e4">
												<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											</fo:table-row>
											<xsl:if test="count(TotalLongTradeExposure)&gt;0">
												<fo:table-row background-color="#d5e0e4">
													<fo:table-cell number-columns-spanned="2" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Total Longs : <xsl:value-of select="TradeInstrument"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalLongTradePrice"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalLongTradeQuantity"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Buy</fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalLongTradeExposure"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalLongTradeExecutionPremium"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalLongTradeAllInExposure"/></fo:block></fo:table-cell>
												</fo:table-row>
											</xsl:if>
											<xsl:if test="count(TotalShortTradeExposure)&gt;0">
												<fo:table-row background-color="#d5e0e4">
													<fo:table-cell number-columns-spanned="2" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Total Shorts : <xsl:value-of select="TradeInstrument"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalShortTradePrice"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalShortTradeQuantity"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Sell</fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalShortTradeExposure"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalShortTradeExecutionPremium"/></fo:block></fo:table-cell>
													<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalShortTradeAllInExposure"/></fo:block></fo:table-cell>
												</fo:table-row>
											</xsl:if>
											<fo:table-row>
												<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block font-size="8pt"></fo:block></fo:table-cell>
											</fo:table-row>	
										</xsl:for-each>	
											<fo:table-row>
												<fo:table-cell padding-before="1mm" number-columns-spanned="8" display-align="before"><fo:block font-size="8pt"></fo:block></fo:table-cell>
											</fo:table-row>	
									</fo:table-body>
							</fo:table>	
						</xsl:for-each>
						<!--Manufatured Dividend Report-->
						<xsl:for-each select="ManufacturedDividends">
							<fo:table table-layout="fixed" margin-top="4mm" width="100%" margin-left="8mm" keep-together.within-page="always">
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
									<fo:table-header>
										<fo:table-row>
											<fo:table-cell number-columns-spanned="5" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">MANUFACTURED DIVIDEND REPORT</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										
										
										<fo:table-row>
											<fo:table-cell padding-before="1mm" padding-after="1mm" number-columns-spanned="6"><fo:block text-align="left" font-size="8pt" font-weight="bold" font-family="Barclays">Strategy : <xsl:value-of select="$StrategyName"/></fo:block></fo:table-cell>
											<fo:table-cell margin-right="6mm" padding-before="1mm" padding-after="1mm" number-columns-spanned="2"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="$StrategyDate"/></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell number-columns-spanned="3" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Name</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">LDT Position</fo:block></fo:table-cell>
											<fo:table-cell number-columns-spanned="2" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="right"><fo:block text-align="center" font-size="8pt" font-family="Barclays">DPS (rands)</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Total</fo:block></fo:table-cell>
											<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Type</fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-header>
									<fo:table-body>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<xsl:for-each select="Dividend">
										<xsl:sort select="CFDName"/>
										<xsl:if test="position() mod 2 != 0"> 
											<fo:table-row>
												<fo:table-cell background-color="#f1f1f1" number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="LDTPosition"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" number-columns-spanned="2" display-align="right"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="DPS"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Total"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Type"/></fo:block></fo:table-cell>
											</fo:table-row>
										</xsl:if>
										<xsl:if test="position() mod 2 = 0"> 
											<fo:table-row>
												<fo:table-cell number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="LDTPosition"/></fo:block></fo:table-cell>
												<fo:table-cell number-columns-spanned="2" display-align="right"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="DPS"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Total"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Type"/></fo:block></fo:table-cell>
											</fo:table-row>
										</xsl:if>											
										</xsl:for-each>	
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell padding-before="0mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">TOTALS</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell number-columns-spanned="2" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalDividends"/></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row>
											<fo:table-cell padding-before="2mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-body>
							</fo:table>	
						</xsl:for-each>	
						<!--Synthetic finacing Report -->	
						<xsl:for-each select="SyntheticFinacing">
							<fo:table break-after="page" margin-top="4mm" table-layout="fixed" width="100%" margin-left="8mm">
								<fo:table-column column-width="2.5cm"/>
								<fo:table-column column-width="3cm"/>
								<fo:table-column column-width="4.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="3.5cm"/>
								<fo:table-column column-width="4cm"/>
									<fo:table-header>
										<fo:table-row>
											<fo:table-cell number-columns-spanned="5" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">SYNTHETIC FINANCING REPORT</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" padding-after="1mm" number-columns-spanned="6"><fo:block text-align="left" font-size="8pt" font-weight="bold" font-family="Barclays">Strategy : <xsl:value-of select="$StrategyName"/></fo:block></fo:table-cell>
											<fo:table-cell margin-right="6mm" padding-before="1mm" padding-after="1mm" number-columns-spanned="2"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="$StrategyDate"/></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell padding-after='1mm' number-columns-spanned="2" border-bottom-width="1pt" border-top-width="1pt" border-top-style="solid" border-bottom-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Name</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Market Value</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Reference Rate</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Financing Spread</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Scrip Spread</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">All in financing rate</fo:block></fo:table-cell>
											<fo:table-cell padding-after='1mm' border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Overnight Premium</fo:block></fo:table-cell>
										</fo:table-row>
									</fo:table-header>
									<fo:table-body>
										<fo:table-row>
											<fo:table-cell padding-before="1mm" padding-after="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<xsl:for-each select="Instrument">
										<xsl:sort select="CFDName"/>
											<xsl:if test="position() mod 2 != 0"> 
											<fo:table-row>
												<fo:table-cell background-color="#f1f1f1" number-columns-spanned="2" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketValue"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ReferenceRate"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OverNightRate"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ShortRate"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="AllInFinacingRate"/></fo:block></fo:table-cell>
												<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OverNightPremium"/></fo:block></fo:table-cell>
											</fo:table-row>
											</xsl:if>
											<xsl:if test="position() mod 2 = 0"> 
											<fo:table-row>
												<fo:table-cell number-columns-spanned="2" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketValue"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ReferenceRate"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OverNightRate"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ShortRate"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="AllInFinacingRate"/></fo:block></fo:table-cell>
												<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OverNightPremium"/></fo:block></fo:table-cell>
											</fo:table-row>
											</xsl:if> 											
										</xsl:for-each>	
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row background-color="#d5e0e4">
											<fo:table-cell number-columns-spanned="2" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">TOTALS</fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalOpeningMarketValue"/></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
											<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="TotalOverNightPremium"/></fo:block></fo:table-cell>
										</fo:table-row>
										<fo:table-row>
											<fo:table-cell padding-before="2mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
										</fo:table-row>					
									</fo:table-body>
							</fo:table>
						</xsl:for-each>	
					</xsl:for-each>	
					<!-- ******************* End of Strategies ******************* -->
					<!--Margin Call Statement-->
					<xsl:if test="count(Client_Statement/Strategy)&gt;0">
					<fo:table table-layout="fixed" margin-top="4mm" width="100%" margin-left="8mm">
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="2cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="4cm"/>
						<fo:table-column column-width="4cm"/>
						<fo:table-column column-width="4cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
							<fo:table-header>
							<fo:table-row>
									<fo:table-cell number-columns-spanned="6" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">MARGIN CALL STATEMENT</fo:block></fo:table-cell>
									<fo:table-cell number-columns-spanned="2" margin-right="6mm" display-align="before"><fo:block text-align="right" font-weight="bold" font-size="8pt" font-family="Barclays">Date : <xsl:value-of select="/Client_Statement/MarginCallStatement/Date"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Closing</fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Market</fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Opening Margin</fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Closing Market</fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Change in Margin</fo:block></fo:table-cell>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Closing Margin</fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Name</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Category</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Margin%</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Exposure</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Requirement</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Exposure</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays">Requirement</fo:block></fo:table-cell>
									<fo:table-cell border-bottom-width="1pt" border-bottom-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Requirement</fo:block></fo:table-cell>
								</fo:table-row>
							</fo:table-header>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
							    <xsl:for-each select="/Client_Statement/MarginCallStatement/Position">
								<xsl:sort select="CFDName"/>
									<xsl:if test="position() mod 2 != 0"> 
									<fo:table-row>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="Category"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="MarginPercentage"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketValue"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarginRequirement"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketValue"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ChangeInMarginRequirement"/></fo:block></fo:table-cell>
										<fo:table-cell background-color="#f1f1f1" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="CloseInMarginRequirement"/></fo:block></fo:table-cell>
									</fo:table-row>
									</xsl:if>
									<xsl:if test="position() mod 2 = 0"> 
									<fo:table-row>
										<fo:table-cell display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="CFDName"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"><xsl:value-of select="Category"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="MarginPercentage"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarketValue"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="OpeningMarginRequirement"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ClosingMarketValue"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ChangeInMarginRequirement"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="CloseInMarginRequirement"/></fo:block></fo:table-cell>
									</fo:table-row>
									</xsl:if>
								</xsl:for-each>	
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block font-size="8pt"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Sub Totals</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/TotalOpeningMarketValue"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/TotalOpeningMarginRequirement"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/TotalClosingMarketValue"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/TotalChangeInMarginRequirement"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/TotalCloseInMarginRequirement"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Closing Cash Balance</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/ClosingCashBalance"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>		
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Margin available to you / (due by you)</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/MarginCallStatement/MarginAvailableToYou"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-before="2mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>	
							</fo:table-body>
					</fo:table>
					</xsl:if>					
					
					<!--Cash Transaction Report-->
					<xsl:if test="count(Client_Statement/Strategy)&gt;0">
					<fo:table break-before="page" margin-top="4mm" table-layout="fixed" width="100%" margin-left="8mm" keep-together.within-page="always">
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
							<fo:table-header>
							<fo:table-row>
									<fo:table-cell number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">CASH TRANSACTION REPORT - Account number <xsl:value-of select="/Client_Statement/CashTransactionReport/Account"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="6" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight rate : <xsl:value-of select="/Client_Statement/CashTransactionReport/FixedRate"/></fo:block></fo:table-cell>
									<fo:table-cell number-columns-spanned="2" margin-right="6mm" display-align="before"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="/Client_Statement/CashTransactionReport/Date"/></fo:block></fo:table-cell>
								</fo:table-row>								
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Amount</fo:block></fo:table-cell>
								</fo:table-row>
							</fo:table-header>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Opening Balance</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/OpeningBalance"/></fo:block></fo:table-cell>
								</fo:table-row>
								<!--
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Deposit / (Payment)</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/Deposits"/></fo:block></fo:table-cell>
								</fo:table-row>
								-->								
								<xsl:for-each select="/Client_Statement/CashTransactionReport/Payment">
									<xsl:sort select="Amount"/>
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Deposit / (Payment)</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Amount"/></fo:block></fo:table-cell>
									</fo:table-row>	
								</xsl:for-each>	
								
								
								<xsl:for-each select="/Client_Statement/CashTransactionReport/CFDProfitLoss">
									<xsl:sort select="Strategy"/>
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Total Profit / (Loss)  - <xsl:value-of select="Strategy"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Amount"/></fo:block></fo:table-cell>
									</fo:table-row>	
								</xsl:for-each>	

							    <xsl:if test="/Client_Statement/CashTransactionReport/OverNightInterest!=0">
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest capitilisation</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/OverNightInterest"/></fo:block></fo:table-cell>
									</fo:table-row>
								</xsl:if>	
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Closing Balance</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/ClosingBalance"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-before="2mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>	
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest accrual:</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/DailyAccruedInterest"/></fo:block></fo:table-cell>
								</fo:table-row>	
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest accrual:Month-to-date</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/MonthToDateAccruedInterest"/></fo:block></fo:table-cell>
								</fo:table-row>	
							</fo:table-body>
					</fo:table>	
					</xsl:if>	

					<xsl:if test="count(Client_Statement/Strategy) = 0">
					<fo:table margin-top="4mm" table-layout="fixed" width="100%" margin-left="8mm" keep-together.within-page="always">
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="3.5cm"/>
							<fo:table-header>
							<fo:table-row>
									<fo:table-cell number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">CASH TRANSACTION REPORT - Account number <xsl:value-of select="/Client_Statement/CashTransactionReport/Account"/></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="6" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight rate : <xsl:value-of select="/Client_Statement/CashTransactionReport/FixedRate"/></fo:block></fo:table-cell>
									<fo:table-cell number-columns-spanned="2" margin-right="6mm" display-align="before"><fo:block text-align="right" font-size="8pt" font-weight="bold" font-family="Barclays">Date : <xsl:value-of select="/Client_Statement/CashTransactionReport/Date"/></fo:block></fo:table-cell>
								</fo:table-row>								
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-bottom-width="1pt" border-bottom-style="solid" border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays">Amount</fo:block></fo:table-cell>
								</fo:table-row>
							</fo:table-header>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Opening Balance</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/OpeningBalance"/></fo:block></fo:table-cell>
								</fo:table-row>
								<!--
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Deposit / (Payment)</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/Deposits"/></fo:block></fo:table-cell>
								</fo:table-row>
								-->								
								<xsl:for-each select="/Client_Statement/CashTransactionReport/Payment">
									<xsl:sort select="Amount"/>
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Deposit / (Payment)</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Amount"/></fo:block></fo:table-cell>
									</fo:table-row>	
								</xsl:for-each>	
								
								
								<xsl:for-each select="/Client_Statement/CashTransactionReport/CFDProfitLoss">
									<xsl:sort select="Strategy"/>
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">CFD Total Profit / (Loss)  - <xsl:value-of select="Strategy"/></fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="Amount"/></fo:block></fo:table-cell>
									</fo:table-row>	
								</xsl:for-each>	

							    <xsl:if test="/Client_Statement/CashTransactionReport/OverNightInterest!=0">
									<fo:table-row>
										<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest capitilisation</fo:block></fo:table-cell>
										<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/OverNightInterest"/></fo:block></fo:table-cell>
									</fo:table-row>
								</xsl:if>	
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-before="1mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">Closing Balance</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/ClosingBalance"/></fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-before="2mm" number-columns-spanned="8" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>	
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest accrual:</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/DailyAccruedInterest"/></fo:block></fo:table-cell>
								</fo:table-row>	
								<fo:table-row>
									<fo:table-cell number-columns-spanned="7" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Overnight interest accrual:Month-to-date</fo:block></fo:table-cell>
									<fo:table-cell display-align="before"><fo:block margin-right="5mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="/Client_Statement/CashTransactionReport/MonthToDateAccruedInterest"/></fo:block></fo:table-cell>
								</fo:table-row>	
							</fo:table-body>
					</fo:table>	
					</xsl:if>	
				
					
					<!--Summary of Terms-->
					<xsl:if test="count(Client_Statement/Strategy) &gt;0">
					<fo:table padding-before="5pt" table-layout="fixed" margin-top="4mm" width="100%" margin-left="8mm">
						<fo:table-column column-width="5cm"/>
						<fo:table-column column-width="3.5cm"/>
						<fo:table-column column-width="4cm"/>
							<fo:table-header>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-weight="bold" font-size="8pt" font-family="Barclays">SUMMARY OF TERMS</fo:block></fo:table-cell>
								</fo:table-row>
								<fo:table-row background-color="#d5e0e4">
									<fo:table-cell padding-after="1mm" border-top-width="1pt" border-top-style="solid" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays">Strategy</fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Execution Premium</fo:block></fo:table-cell>
									<fo:table-cell padding-after="1mm" border-top-width="1pt" border-top-style="solid" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays">Reference funding rate</fo:block></fo:table-cell>
								</fo:table-row>
							</fo:table-header>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-before="1mm" number-columns-spanned="3" border-right-width="1pt" border-right-style="solid" border-left-width="1pt" border-left-style="solid" border-top-width="1pt" border-top-style="solid" display-align="before"><fo:block text-align="center" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>
							    <xsl:for-each select="/Client_Statement/SummaryOfTerms/Strategy">
									<fo:table-row>
										<fo:table-cell padding-before="1mm" border-left-width="1pt" border-left-style="solid" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"><xsl:value-of select="StrategyName"/></fo:block></fo:table-cell>
										<fo:table-cell padding-before="1mm" display-align="before"><fo:block margin-right="10mm" text-align="right" font-size="8pt" font-family="Barclays"><xsl:value-of select="ExecutionPremium"/></fo:block></fo:table-cell>
										<fo:table-cell padding-before="1mm" border-right-width="1pt" border-right-style="solid" display-align="before"><fo:block margin-right="10mm" text-align="right" font-size="8pt" font-family="Barclays">SAONBOR</fo:block></fo:table-cell>
									</fo:table-row>
								</xsl:for-each>	
								<fo:table-row>
									<fo:table-cell border-top-width="1pt" border-top-style="solid" number-columns-spanned="3" display-align="before"><fo:block text-align="left" font-size="8pt" font-family="Barclays"></fo:block></fo:table-cell>
								</fo:table-row>	
							</fo:table-body>
					</fo:table>
					</xsl:if>
					<fo:block padding-before="6mm" margin-left="8mm" text-align="left" font-size="8pt" font-family="Barclays">Note:</fo:block>
					<fo:block margin-left="8mm" text-align="left" font-size="8pt" font-family="Barclays">All prices are quoted in ZAR unless otherwise stated</fo:block>
					<fo:block margin-left="8mm" text-align="left" font-size="8pt" font-family="Barclays">All interest rates and spreads are quoted in percentage points unless otherwise stated</fo:block>
				</fo:flow>
			</fo:page-sequence>
		  </fo:root>
	</xsl:template>
</xsl:stylesheet>

		  
