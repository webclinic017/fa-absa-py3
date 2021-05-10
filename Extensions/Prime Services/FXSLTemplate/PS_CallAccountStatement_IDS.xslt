<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">

	<xsl:template match="/STATEMENT">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master master-name="first" page-width="210mm" page-height="297mm" margin-top="5mm" margin-bottom="5mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="71mm" margin-bottom="30mm"/>
					<fo:region-before extent="50mm"/>
					<fo:region-after extent="30mm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="first">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="Arial" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="65mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell padding-top="0pt" font-family="Arial" >
										<fo:block text-align="left" font-weight="bold" font-size="8pt" font-style="italic" >
											<xsl:value-of select="'Return address:'"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt">
											<xsl:value-of select="concat(CUSTLIN1/BAD1,', ', CUSTLIN1/BAD2,', ',CUSTLIN1/BAD3,', ',CUSTLIN1/BAD4 )" />
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="12pt" space-before="35pt">
											<xsl:value-of select="CLIENTDETAIL/CNAM"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="CLIENTDETAIL/ADDR1"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="CLIENTDETAIL/ADDR2"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="CLIENTDETAIL/CIT"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="CLIENTDETAIL/ZIP"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt">
											<xsl:value-of select="CLIENTDETAIL/CTY"/>
										</fo:block>
										<fo:block text-align="left" font-weight="bold" font-size="10pt" space-before="15pt">
											<xsl:value-of select="concat('Attention: ',PRIMEDETAIL/ATT)"/>
										</fo:block>

									</fo:table-cell>
									<fo:table-cell padding-top="0pt">
										<fo:block>
											<fo:external-graphic content-width="65mm" scaling="uniform">
												<xsl:attribute name="src">
/apps/services/front/FOP/fop-1.0/Images/AbsaCapital.png
												</xsl:attribute>
											</fo:external-graphic>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-style="italic">
											<xsl:value-of select="'Write to us at:'"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-family="Arial">
											<xsl:value-of select="PRIMEDETAIL/CNAM"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-family="Arial">
											<xsl:value-of select="PRIMEDETAIL/ADDR"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-family="Arial">
											<xsl:value-of select="PRIMEDETAIL/CIT"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-family="Arial">
											<xsl:value-of select="PRIMEDETAIL/ZIP"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" font-family="Arial">
											<xsl:value-of select="PRIMEDETAIL/CTY"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt" space-before="10pt" font-style="italic">
											<xsl:value-of select="'Enquiries:'"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt">
											<xsl:value-of select="concat('Tel: ', PRIMEDETAIL/TEL)"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="8pt">
											<xsl:value-of select="concat('E-mail: ', PRIMEDETAIL/EMAIL)"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell padding-top="0pt">
										<fo:block text-align="left" font-weight="bold" font-size="11pt" space-before="10pt" font-family="Barclays">
											<xsl:value-of select="'Call Deposit NonDTI Statement for the period'"/>
										</fo:block>
										<fo:block text-align="left" font-weight="normal" font-size="10pt">
											<xsl:value-of select="header2/H2"/>
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
					<fo:block text-align="left" font-size="8pt"> - All prices are in ZAc</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All amounts are in ZAR</fo:block>
					<fo:block text-align="left" font-size="8pt"> - All rates are in percentage points</fo:block>
					<fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
					<fo:block font-size="8pt" font-family="Arial" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column />
							<fo:table-column />
							<fo:table-column />
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="1">
										<fo:block>
											<fo:external-graphic left="0mm" content-height="10mm" scaling="uniform">
												<xsl:attribute name="src">
														/apps/services/front/FOP/fop-1.0/Images/FooterLeft.jpg
												</xsl:attribute>
											</fo:external-graphic>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="2">
										<fo:block text-align="center">
											<fo:inline>Page <fo:page-number/></fo:inline>
										</fo:block>
										<fo:block text-align="center">
											<fo:inline>
												<xsl:value-of select="concat('Statement Date: ',header2/CDATE)"/>
											</fo:inline>
										</fo:block>
										<fo:block text-align="center">
											<fo:inline>
												<xsl:value-of select="concat('Account number: ',CUSTLIN2/CACC)"/>
											</fo:inline>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell column-number="3">
										<fo:block text-align="left">
											<fo:external-graphic content-height="10mm" scaling="uniform">
												<xsl:attribute name="src">
													/apps/services/front/FOP/fop-1.0/Images/FooterRight.jpg
												</xsl:attribute>
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
						<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
							<fo:table-row>
								<fo:table-cell>
										<!-- Account number -->
										<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt">
											<fo:table-column column-width="100%"/>
												<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
													<fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt">
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-weight="bold">Account Number: <xsl:value-of select="CUSTLIN2/CACC"/></fo:block>
														</fo:table-cell>
													</fo:table-row>
												</fo:table-body>
										</fo:table>
								</fo:table-cell>
							</fo:table-row>
							<fo:table-row>
								<fo:table-cell>
									<!-- Account summary -->
									<fo:table table-layout="fixed" font-size="10pt"  font-weight="Bold" border-spacing="2pt">
											<fo:table-column column-width="100%"/>
												<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
													<fo:table-row >
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-weight="Bold" font-size="10pt" space-before="5pt" padding="5pt">Account Summary</fo:block>
														</fo:table-cell>
													</fo:table-row>
												</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

							<fo:table-row>
								<fo:table-cell>
									<!-- Summary Detail -->
									<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt">
											<fo:table-column column-width="proportional-column-width(1)"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-header>
													<fo:table-row border-bottom="dotted black 0.5pt" border-top="solid black 1pt">
														<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">Description</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right" font-style="italic">Amount</fo:block>
														</fo:table-cell>
													</fo:table-row>
											</fo:table-header>
											<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
												<fo:table-row border-bottom="dotted black 0.5pt">
													<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left">Opening balance</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="ACCSUM/OBAL"/></fo:block>
														</fo:table-cell>
												</fo:table-row>
												<fo:table-row border-bottom="dotted black 0.5pt">
													<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left">Total credits</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="ACCSUM/TCRED"/></fo:block>
														</fo:table-cell>
												</fo:table-row>
												<fo:table-row border-bottom="dotted black 0.5pt">
													<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left">Total debits</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="ACCSUM/TDEB"/></fo:block>
														</fo:table-cell>
												</fo:table-row>
												<fo:table-row border-bottom="solid black 0.5pt">
													<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left">Total interest</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="ACCSUM/TINT"/></fo:block>
														</fo:table-cell>
												</fo:table-row>
												<fo:table-row border-bottom="solid black 1pt">
													<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-weight="Bold" >Closing balance</fo:block>
														</fo:table-cell>
														<fo:table-cell  padding="5pt">
															<fo:block text-align="right" font-weight="Bold"><xsl:value-of select="ACCSUM/CBAL"/></fo:block>
														</fo:table-cell>
												</fo:table-row>

											</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

							<fo:table-row>
								<fo:table-cell>
									<!-- Cash Transactions summary -->
									<fo:table table-layout="fixed" font-size="10pt" border-spacing="2pt" font-weight="Bold" width="100%">
											<fo:table-column column-width="100%"/>
												<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
													<fo:table-row >
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-weight="Bold"  font-size="10pt" space-before="15pt" padding="5pt">Cash Transactions</fo:block>
														</fo:table-cell>
													</fo:table-row>
												</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

							<fo:table-row>
								<fo:table-cell>
									<!-- Cash Transaction Detail -->
									<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" width="100%">
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="60mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-header>
													<fo:table-row border-bottom="dotted black 0.5pt" border-top="solid black 1pt">
														<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">value date</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">posting date</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">deal number</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">transaction description / client reference</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">transaction amount</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">account balance</fo:block>
														</fo:table-cell>
													</fo:table-row>
											</fo:table-header>
											<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
												<fo:table-row>
													<fo:table-cell>
														<fo:block text-align="right"><xsl:value-of select="''" /></fo:block>
													</fo:table-cell>
												</fo:table-row>
												<xsl:for-each select="TRANLIN">
													<fo:table-row>
														<xsl:attribute name="border-bottom">
															<xsl:choose>
																<xsl:when test="position() = last()">dotted black 1pt</xsl:when>
																<xsl:otherwise>dotted black 0.5pt</xsl:otherwise>
															</xsl:choose>
														</xsl:attribute>
														<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left"><xsl:value-of select="VDAT"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left"><xsl:value-of select="PDAT"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left"><xsl:value-of select="DLNO"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left"><xsl:value-of select="CDES"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="TAMT"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="TABAL"/></fo:block>
														</fo:table-cell>
													</fo:table-row>

												</xsl:for-each>


											</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

							<fo:table-row>
								<fo:table-cell>
									<!-- Interest -->
									<fo:table table-layout="fixed" font-size="10pt" border-spacing="2pt" font-weight="Bold" width="100%">
											<fo:table-column column-width="100%"/>
												<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
													<fo:table-row >
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-weight="Bold"  font-size="10pt" space-before="15pt" padding="5pt">Interest</fo:block>
														</fo:table-cell>
													</fo:table-row>
												</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

							<fo:table-row>
								<fo:table-cell>
									<!-- Interest Detail -->
									<fo:table table-layout="fixed" font-size="8pt" border-spacing="2pt" width="100%">
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-column column-width="25mm"/>
											<fo:table-header>
													<fo:table-row border-bottom="dotted black 0.5pt" border-top="solid black 1pt">
														<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left" font-style="italic">value date</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right" font-style="italic">interest amount</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right" font-style="italic">interest rate</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right" font-style="italic">interest balance</fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right" font-style="italic">account balance</fo:block>
														</fo:table-cell>
													</fo:table-row>
											</fo:table-header>
											<fo:table-body  table-layout="fixed" font-size="8pt" border-spacing="2pt">
												<fo:table-row>
													<fo:table-cell>
														<fo:block text-align="right"><xsl:value-of select="''" /></fo:block>
													</fo:table-cell>
												</fo:table-row>
												<xsl:for-each select="INTLIN">
													<fo:table-row>
														<xsl:attribute name="border-bottom">
															<xsl:choose>
																<xsl:when test="position() = last()">dotted black 1pt</xsl:when>
																<xsl:otherwise>dotted black 0.5pt</xsl:otherwise>
															</xsl:choose>
														</xsl:attribute>
														<xsl:attribute name="background-color">#f1f1f1</xsl:attribute>
														<fo:table-cell padding="5pt">
															<fo:block text-align="left"><xsl:value-of select="VDAT"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="IAMNT"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="IRATE"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="IBAL"/></fo:block>
														</fo:table-cell>
														<fo:table-cell padding="5pt">
															<fo:block text-align="right"><xsl:value-of select="ABAL"/></fo:block>
														</fo:table-cell>
													</fo:table-row>

												</xsl:for-each>


											</fo:table-body>
										</fo:table>

								</fo:table-cell>
							</fo:table-row>

						</fo:table-body>
					</fo:table>

				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>

</xsl:stylesheet>


