#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf
#grouping: aef reporting/style sheets

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://fron.com/arena/primereport">
	<xsl:template match="/">
		<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
			<fo:layout-master-set>
				<fo:simple-page-master master-name="BSB_REPO_A4" page-width="210mm" page-height="297mm" margin-top="10mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="40mm" margin-bottom="30mm" margin-left="10mm" margin-right="10mm"/>
				</fo:simple-page-master>
				<fo:simple-page-master master-name="LAST_A4" page-width="210mm" page-height="297mm" margin-top="10mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
                                                                                <fo:region-body margin-top="50mm" margin-bottom="30mm" margin-left="10mm" margin-right="10mm"/>
                                                                                <fo:region-before region-name="xsl-region-before-last" extent="50mm"/>
				</fo:simple-page-master>
				
				<fo:page-sequence-master master-name="page_sequence">
					<fo:repeatable-page-master-alternatives>
						<fo:conditional-page-master-reference master-reference="LAST_A4" page-position="last"/>
						<fo:conditional-page-master-reference master-reference="BSB_REPO_A4"/>
					</fo:repeatable-page-master-alternatives>
				</fo:page-sequence-master>				
			</fo:layout-master-set>
			

			<fo:page-sequence master-reference="page_sequence">
				<fo:static-content flow-name="xsl-region-before-last">
                                                                                <fo:block margin-left="80" padding-top="7.5pt"  font-size="10pt" font-family="Arial" >
                                                                                        <xsl:value-of select="//ReturnConfirmationReport/ConfirmationReport/Date"/>
                                                                                </fo:block>
                                                                                
                                                                                <fo:block margin-left="297" padding-top="109pt"  font-size="10pt" font-family="Arial" text-transform="uppercase" font-weight="bolder" color="black">
                                                                                        <xsl:value-of select="//ReturnConfirmationReport/ConfirmationReport/Date"/>
                                                                                </fo:block>
                                                                </fo:static-content>
				
				<fo:flow flow-name="xsl-region-body">
                                                                                <xsl:apply-templates select="//ReturnConfirmationReport/ConfirmationReport"/>
				</fo:flow>

			</fo:page-sequence>

		</fo:root>
	</xsl:template>
	
	
	<xsl:template match="//ReturnConfirmationReport/ConfirmationReport">
		<fo:block break-before="page" font-size="10pt" font-family="Barclays" color="black" margin-left="35mm"  margin-bottom="5mm" font-weight="bold">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="100%"/>
								
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="ConfirmationHead/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block  font-size="10pt" font-family="Barclays" color="black" margin-left="75"  margin-bottom="13mm" font-weight="bold">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="100%"/>				
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="HeadingDetail/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block font-size="10pt" font-family="Barclays" color="black" margin-bottom="10mm" font-weight="bold">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="20%"/>
				<fo:table-column column-width="80%"/>
				
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="ClientDetail/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block margin-bottom="5mm"><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block font-size="10pt" font-family="Barclays" color="black" margin-bottom="4mm" font-weight="bold">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="100%"/>
				
				
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="Notice/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block margin-bottom="5mm"><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block font-size="10pt" font-family="Barclays" color="black" margin-bottom="5mm">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="50%"/>
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="ReportDetail/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block font-size="10pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block font-size="10pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>

		<fo:block font-size="9pt" font-family="Barclays" color="black" margin-bottom="5mm" text-align = "justify">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="100%"/>
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="FooterDetail/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block font-size="9pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block font-size="9pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
		<fo:block font-size="9pt" font-family="Barclays" color="black" margin-bottom="5mm" font-weight="bold">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="100%"/>
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="Computer/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block font-size="9pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block font-size="9pt" font-family="Barclays" color="black" padding-bottom="4mm"><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>		
	</xsl:template>
</xsl:stylesheet>

