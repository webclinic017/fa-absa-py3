<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">
    <!-- Element-matching templates -->
    <xsl:variable name="isNewLoan" select="/DOCUMENT/DUCUMENT_TYPE = 'NEW_LOAN'" />
    <xsl:template match="/">
        <xsl:variable name="isNewLoan" select="/DOCUMENT/DUCUMENT_TYPE = 'NEW_LOAN'" />
        <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
            <fo:layout-master-set>
                <!-- Display header and footer on page 1 only -->
                <fo:page-sequence-master master-name="SecurityLoanConfirmation">
                    <fo:repeatable-page-master-alternatives>
                        <fo:conditional-page-master-reference page-position="first" master-reference="first_only" />
                        <fo:conditional-page-master-reference master-reference="other_pages"/>
                    </fo:repeatable-page-master-alternatives>
                </fo:page-sequence-master>

                <xsl:variable name="width">
                    <xsl:text>297mm</xsl:text>
                </xsl:variable>

                <xsl:variable name="height">
                    <xsl:text>210mm</xsl:text>
                </xsl:variable>

                <fo:simple-page-master master-name="first_only" margin-top="10mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
                    <xsl:attribute name="page-width">
                        <xsl:value-of select="$width" />
                    </xsl:attribute>
                    <xsl:attribute name="page-height">
                        <xsl:value-of select="$height" />
                    </xsl:attribute>
                    <fo:region-body margin-bottom="25mm" />
                    <fo:region-after extent="15mm" />
                </fo:simple-page-master>

                <fo:simple-page-master master-name="other_pages" margin-top="20mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
                    <xsl:attribute name="page-width">
                        <xsl:value-of select="$width" />
                    </xsl:attribute>
                    <xsl:attribute name="page-height">
                        <xsl:value-of select="$height" />
                    </xsl:attribute>
                    <fo:region-body margin-bottom="25mm" />
                    <fo:region-after extent="15mm" />
                </fo:simple-page-master>
            </fo:layout-master-set>

            <fo:page-sequence master-reference="SecurityLoanConfirmation">
                <fo:static-content flow-name="xsl-region-after" font-family="Helvetica" font-size="9pt">
                    <fo:block margin-bottom="4mm" text-align="justify">
                        All Securities Lending Transactions between yourself and ABSA Bank Limited ("ABSA") shall be promptly confirmed by ABSA by Confirmation exchanged electronically. Unless you object to the terms and of the Securities Lending Transaction contained in the Confirmation within 24 hours of receipt thereof, the terms of such Confirmation shall be deemed correct and accepted absent manifest error. Furthermore, please note that this confirmation is electronically generated and requires no signature by ABSA
                    </fo:block>
                    <fo:block padding-bottom="2mm" font-size="6pt" color="grey">
                        <xsl:value-of select="/DOCUMENT/__XMLReportResources/txt-absareg" />
                    </fo:block>
                </fo:static-content>

                <fo:flow flow-name="xsl-region-body" font-size="9pt" font-family="Helvetica">
                    <!-- Header is included in the body as its height is variable because of client address -->
                    <fo:table table-layout="fixed" width="100%">
                        <fo:table-column column-width="140mm" />
                        <fo:table-column column-width="135mm" />
                        <fo:table-body>
                            <fo:table-row>
                                <fo:table-cell>
                                    <fo:block margin-bottom="10mm">
                                        <fo:external-graphic content-width="27mm" scaling="uniform">
                                            <xsl:attribute name="src">
                                                <xsl:value-of select="/DOCUMENT/__XMLReportResources/img-absa-logo"/>
                                            </xsl:attribute>
                                        </fo:external-graphic>
                                    </fo:block>
                                    <fo:block font-size="9pt" font-family="Helvetica" margin-bottom="5mm" >
                                        <xsl:apply-templates select="/DOCUMENT/TO" />
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-family="Helvetica" font-size="10pt" color="rgb(220, 0, 50)" margin-top="2mm" margin-bottom="3mm" text-align="right">Corporate and Investment Banking</fo:block>
                                    <fo:block font-family="Helvetica" font-size="10pt" color="rgb(220, 0, 50)" font-weight="bold" margin-bottom="3mm" text-align="right">CONFIDENTIAL</fo:block>
                                    <fo:block font-family="Helvetica" font-size="9pt" color="#303030" text-align="right">
                                        <xsl:apply-templates select="/DOCUMENT/FROM" />
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                    <xsl:apply-templates select="/DOCUMENT/SUBJECT" />
                    <xsl:apply-templates select="/DOCUMENT/ATTENTION_MESSAGE/SUMMERY1" />
                    <xsl:apply-templates select="/DOCUMENT/ATTENTION_MESSAGE/SUMMERY2" />
                    <xsl:apply-templates select="/DOCUMENT/TRADES" />
                </fo:flow>
            </fo:page-sequence>
        </fo:root>

    </xsl:template>

    <xsl:template match="/DOCUMENT/SUBJECT">
        <fo:block keep-with-next="always" font-weight="bold" margin-bottom="5mm" font-size="10pt">
			<xsl:choose>
				<xsl:when test="@fontsize">
					<xsl:attribute name="font-size">
						<xsl:value-of select="@fontsize"/>
					</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="font-size">10</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="@marginbottom">
					<xsl:attribute name="margin-bottom">
						<xsl:value-of select="@marginbottom"/>
					</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="margin-bottom">5</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
            <xsl:value-of select="." />
        </fo:block>
    </xsl:template>

    <xsl:template match="/DOCUMENT/FROM">
        <xsl:call-template name="Contact" />
        <xsl:for-each select="TEL">
            <fo:block>
                <xsl:text>T </xsl:text>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="EMAIL">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="WEBSITE">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="DATE">
            <fo:block >
                <xsl:attribute name="padding-top">2mm</xsl:attribute>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="/DOCUMENT/TO">
        <xsl:for-each select="NAME">
            <fo:block>
                <xsl:attribute name="padding-bottom">4mm</xsl:attribute>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:call-template name="Contact" />
        <xsl:for-each select="TO_ATTENTION">
            <fo:block>
                <xsl:text >Contact:   </xsl:text> <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="TO_TELEPHONE">
            <fo:block>
                <xsl:text >Telephone:   </xsl:text> <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="SHORTCODE">
            <fo:block>
                <xsl:text >Client Code:  </xsl:text> <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="/DOCUMENT/TRADES">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="/DOCUMENT/ATTENTION_MESSAGE/SUMMERY1">
        <fo:block keep-with-next="always" margin-bottom="1mm" font-size="9pt" text-align="center">
            <xsl:value-of select="." />
        </fo:block>
    </xsl:template>
    <xsl:template match="/DOCUMENT/ATTENTION_MESSAGE/SUMMERY2">
        <fo:block keep-with-next="always" margin-bottom="2mm" font-size="9pt" text-align="center">
            <xsl:value-of select="." />
        </fo:block>
    </xsl:template>

    <xsl:template match="/DOCUMENT/TRADES">
        <xsl:choose>
            <xsl:when test="@tableheader">
                <fo:block keep-with-next.within-page="always" font-weight="bold" font-size="10pt" margin-top="5mm" text-align="center">
                    <xsl:value-of select="@tableheader"/>
                </fo:block>
            </xsl:when>
        </xsl:choose>
        <fo:block border-top-color="rgb(220, 0, 50)" border-top-width="0.5mm" padding-top="2mm" padding-bottom="2mm" padding-right="1mm" margin-bottom="10mm" border-top-style="solid" border-bottom-style="solid" font-weight="normal" font-size="9pt" text-align="center">
            <fo:table table-layout="auto">
                <fo:table-header font-weight="bold" font-size="9pt" text-align="center">
                    <fo:table-row>
                        <fo:table-cell padding-left="1mm">
                            <fo:block margin-bottom="2mm" text-align="left">
                                Trade Ref
                            </fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding-left="2mm">
                            <fo:block margin-bottom="2mm">
                                ISIN
                            </fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding-left="2mm">
                            <fo:block margin-bottom="2mm">
                                Security
                            </fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding-left="2mm">
                            <fo:block margin-bottom="2mm" text-align="right">
                                Quantity
                            </fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding-left="2mm">
                            <fo:block margin-bottom="2mm">
                                Trade Date
                            </fo:block>
                        </fo:table-cell>
                        <fo:table-cell padding-left="2mm">
                            <fo:block margin-bottom="2mm">
                                Settlement
                            </fo:block>
                        </fo:table-cell>
                        <xsl:choose>
                            <xsl:when test="$isNewLoan">
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Rate (Excl. Vat)
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Rate (Incl. Vat)
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Loan Price
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm" text-align="right">
                                        Loan Value
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        VAT
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Delivery
                                    </fo:block>
                                </fo:table-cell>
                            </xsl:when>
                            <xsl:otherwise>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Delivery
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Loan Quantity
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm">
                                        Loan Date
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm" text-align="right">
                                        Loan Rate
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-left="2mm">
                                    <fo:block margin-bottom="2mm" text-align="right">
                                        Loan Price
                                    </fo:block>
                                </fo:table-cell>
                            </xsl:otherwise>
                        </xsl:choose>
                    </fo:table-row>
                </fo:table-header>


                <fo:table-body>
                    <xsl:for-each select="/DOCUMENT/TRADES/TRADE">
                        <fo:table-row text-align="center">
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm" text-align="left">
                                    <xsl:value-of select="TRADE_DNUMBER"/>
                                </fo:block>
                            </fo:table-cell>
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm">
                                    <xsl:value-of select="ISIN"/>
                                </fo:block>
                            </fo:table-cell>
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm">
                                    <xsl:value-of select="SECURITY"/>
                                </fo:block>
                            </fo:table-cell>
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm" text-align="right">
                                    <xsl:value-of select="QUANTITY"/>
                                </fo:block>
                            </fo:table-cell>
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm">
                                    <xsl:value-of select="TRADE_DATE"/>
                                </fo:block>
                            </fo:table-cell>
                            <fo:table-cell>
                                <fo:block margin-bottom="1.5mm">
                                    <xsl:value-of select="SETTLEMENT_DATE"/>
                                </fo:block>
                            </fo:table-cell>
                            <xsl:choose>
                                <xsl:when test="$isNewLoan">
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm" >
                                            <xsl:value-of select="RATE_EXL_VAT"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="RATE_INC_VAT"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="LOAN_PRICE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm" text-align="right">
                                            <xsl:value-of select="LOAN_VALUE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="VATABLE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="DELIVERY_MODE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                </xsl:when>
                                <xsl:otherwise>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="DELIVERY_MODE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm" text-align="right">
                                            <xsl:value-of select="ORIGINAL_QUANTITY"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm">
                                            <xsl:value-of select="ORIGINAL_DATE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm" text-align="right">
                                            <xsl:value-of select="ORIGINAL_RATE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell>
                                        <fo:block margin-bottom="1.5mm" text-align="right">
                                            <xsl:value-of select="ORIGINAL_PRICE"/>
                                        </fo:block>
                                    </fo:table-cell>
                                </xsl:otherwise>
                            </xsl:choose>

                        </fo:table-row>
                    </xsl:for-each>
                    <!-- At least one row must be present -->
                    <xsl:if test="not(/DOCUMENT/TRADES/TRADE)">
                        <fo:table-cell><fo:block /></fo:table-cell>
                    </xsl:if>
                </fo:table-body>
            </fo:table>
        </fo:block>
    </xsl:template>

    <xsl:template name="Contact">

        <xsl:for-each select="ADDRESS/LINE1">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="ADDRESS/LINE2">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="ADDRESS/CITY">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="ADDRESS/COUNTRY">
            <fo:block>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
        <xsl:for-each select="ADDRESS/ZIPCODE">
            <fo:block>
                <xsl:attribute name="padding-bottom">2mm</xsl:attribute>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
