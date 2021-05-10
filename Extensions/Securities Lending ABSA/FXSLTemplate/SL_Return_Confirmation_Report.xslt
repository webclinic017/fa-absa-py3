#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://fron.com/arena/primereport">
	<xsl:template match="/">
		<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
			<fo:layout-master-set>
				<fo:simple-page-master master-name="SL_Return_Confirmation_A4" page-width="210mm" page-height="297mm" margin-top="10mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
					<fo:region-body margin-top="50mm" margin-bottom="30mm" margin-left="10mm" margin-right="10mm"/>
					<fo:region-before extent="50mm"/>
					<fo:region-after extent="30mm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="SL_Return_Confirmation_A4">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block font-size="12pt" font-family="Barclays" color="black">
						<fo:table table-layout="fixed" width="100%">
							<fo:table-column column-width="proportional-column-width(1)"/>
							<fo:table-column column-width="60mm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell column-number="2">
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
					<fo:block font-size="12pt" font-family="Barclays" color="black">
						<fo:external-graphic src="file:images/barclaysENG.jpg" content-width="50mm" scaling="uniform"/>
					</fo:block>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<xsl:apply-templates select="//ReturnConfirmationReport"/>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	<xsl:template match="//ReturnConfirmationReport">
		<fo:block break-before="page" font-size="12pt" font-family="Barclays" color="black">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="30mm"/>
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<xsl:for-each select="ClientDetail/ReportElement">
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
		<fo:block margin-left="5mm" margin-top="15mm" font-size="12pt" font-family="Barclays" color="black">
			<fo:table table-layout="fixed" width="100%">
				<fo:table-column column-width="5mm"/>
				<fo:table-column column-width="70mm"/>
				<fo:table-column column-width="proportional-column-width(1)"/>
				<fo:table-body>
					<fo:table-row>
						<fo:table-cell text-decoration="underline" number-columns-spanned="3">
							<fo:block margin-bottom="5mm">
								<fo:inline>We hereby confirm the </fo:inline>
								<fo:inline color="red">RETURN </fo:inline>
								<fo:inline>of the following security </fo:inline>
								<fo:inline color="red">TO YOU</fo:inline>
							</fo:block>
						</fo:table-cell>
					</fo:table-row>
					<xsl:for-each select="ReportDetail/ReportElement">
						<fo:table-row>
							<fo:table-cell>
								<fo:block/>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block margin-bottom="3mm"><xsl:value-of select="Label"/></fo:block>
							</fo:table-cell>
							<fo:table-cell>
								<fo:block><xsl:value-of select="Value"/></fo:block>
							</fo:table-cell>
						</fo:table-row>
					</xsl:for-each>
				</fo:table-body>
			</fo:table>
		</fo:block>
	</xsl:template>
</xsl:stylesheet>

