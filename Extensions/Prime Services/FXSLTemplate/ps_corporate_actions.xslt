#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates pdf

<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://front.com/arena/primereport">
    <xsl:template match="/PRIMEReport">
        <fo:root>
            <fo:layout-master-set>
                <fo:simple-page-master master-name="all_pages" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
                    <fo:region-body margin-top="50mm" margin-bottom="25mm"/>
                    <fo:region-before region-name="xsl-region-before" extent="50mm"/>
                    <fo:region-after region-name="xsl-region-after-last" extent="22mm"/>
                </fo:simple-page-master>
                <fo:simple-page-master master-name="last_page" page-width="297mm" page-height="210mm" margin-top="5mm" margin-bottom="10mm" margin-left="10mm" margin-right="10mm">
                    <fo:region-body margin-top="50mm" margin-bottom="25mm"/>
                    <fo:region-before region-name="xsl-region-before" extent="50mm"/>
                    <fo:region-after region-name="xsl-region-after-last" extent="27mm"/>
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
                                        <fo:block text-align="right">
                                            <fo:external-graphic content-height="25mm" scaling="uniform" padding-top="15pt">
                                                <xsl:attribute name="src"><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'FrontEnd'">
                                            file:y:/Jhb/Arena/Prime/FOP/images/absa.png
                                            </xsl:if><xsl:if test="//PRIMEReport/ReportParameters/RunLocation = 'BackEnd'">
                                            /apps/services/front/FOP/fop-1.0/Images/absa.png
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
                <fo:static-content flow-name="xsl-region-after-last">
                    <fo:block text-align="left" font-weight="bold" font-size="8pt">Notes:</fo:block>
                    <fo:block text-align="left" font-size="8pt">Unless stated otherwise:</fo:block>
                    <fo:block text-align="left" font-size="8pt"> - All amounts are in ZAR</fo:block>
                    <fo:block text-align="left" font-size="8pt"> - All rates are in percentage points</fo:block>
                    <fo:block text-align="left" font-size="8pt">For CFD and Financed Cash Equities dividends are settled on dividend Ex-div date, for fully financed equities dividends are settled on the dividend pay date</fo:block>
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
                                            <fo:inline>Page <fo:page-number/></fo:inline>
                                        </fo:block>
                                        <fo:block text-align="center">
                                            <fo:inline>
                                                <xsl:if test="//PRIMEReport/ReportParameters/FrameworkVersion">Generated using <xsl:value-of select="//PRIMEReport/ReportParameters/FrameworkVersion"/> at </xsl:if><xsl:value-of select="//Time"/> 
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
                    <fo:table table-layout="fixed" font-size="7pt" border-spacing="2pt" break-after="page">
                        <fo:table-column column-width="proportional-column-width(1)"/><!-- Instrument -->
                        <fo:table-column column-width="15mm"/><!-- Financed -->
                        <fo:table-column column-width="15mm"/><!-- Instrument Type -->
                        <fo:table-column column-width="26mm"/><!-- Underlying -->
                        <fo:table-column column-width="15mm"/><!-- Underlying Type -->
                        <fo:table-column column-width="17mm"/><!-- ISIN -->
                        <fo:table-column column-width="24mm"/><!-- Closing Position -->
                        <fo:table-column column-width="22mm"/><!-- LDT Position -->
                        <fo:table-column column-width="19mm"/><!-- LDT -->
                        <fo:table-column column-width="19mm"/><!-- Pay Day -->
                        <fo:table-column column-width="17mm"/><!-- Factor -->
                        <fo:table-column column-width="15mm"/><!-- Currency -->
                        <fo:table-column column-width="19mm"/><!-- Value -->
                        <fo:table-column column-width="18mm"/><!-- Type -->
                        <fo:table-header>
                            <fo:table-row border-top="solid black 1pt" border-bottom="solid black 1pt">
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">Instrument</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">Financing</fo:block>
                                    <fo:block text-align="left"  font-weight="bold">Method</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">Instrument</fo:block>
                                    <fo:block text-align="left"  font-weight="bold">Type</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">Underlying</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">Underlying</fo:block>
                                    <fo:block text-align="left"  font-weight="bold">Type</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold">ISIN</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">Closing Position</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">CAction</fo:block>
                                    <fo:block text-align="right"  font-weight="bold">LDT Position</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">CAction</fo:block>
                                    <fo:block text-align="right"  font-weight="bold">LDT</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">CAction</fo:block>
                                    <fo:block text-align="right"  font-weight="bold">Pay Date</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">CAction</fo:block>
                                    <fo:block text-align="right"  font-weight="bold">Factor</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">Currency</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="right"  font-weight="bold">CAction</fo:block>
                                    <fo:block text-align="right"  font-weight="bold">Value</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="5pt" padding-top="5pt">
                                    <fo:block text-align="left"  font-weight="bold" margin-left = "10pt">CAction</fo:block>
                                    <fo:block text-align="left"  font-weight="bold" margin-left = "10pt">Type</fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-header>
                        <fo:table-body>
                             <xsl:apply-templates select="ReportContents/Table"/>
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
     <fo:table-row><fo:table-cell><fo:block></fo:block></fo:table-cell></fo:table-row>
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
                <fo:table-cell>
                    <xsl:attribute name="padding-left">
                        <xsl:value-of select="($treeDepth - 1) * 6"/>pt
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
                    <xsl:if test="position() &lt;= 4">
                        <fo:table-cell display-align="center">
                            <fo:block text-align="left">
                                <xsl:value-of select="FormattedData"/>
                            </fo:block>
                        </fo:table-cell>
                    </xsl:if>
                </xsl:for-each>
                <!-- Other Columns -->
                <xsl:for-each select="Cells/Cell">
                    <xsl:if test="position() > 4">
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
