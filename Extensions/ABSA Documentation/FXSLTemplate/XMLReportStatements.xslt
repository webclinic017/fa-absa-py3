<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

    <!-- Element-matching templates -->
    <xsl:template match="/XMLReport">
        <xsl:variable name="isLandscape" select="__XMLReportSettings/Landscape[1] = 'true'"/>

        <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
            <fo:layout-master-set>
                <!-- Display header and footer on page 1 only -->
                <fo:page-sequence-master master-name="BSB_REPO_A4">
                    <fo:repeatable-page-master-alternatives>
                        <fo:conditional-page-master-reference page-position="first" master-reference="first_only" />
                        <fo:conditional-page-master-reference master-reference="other_pages"/>
                    </fo:repeatable-page-master-alternatives>
                </fo:page-sequence-master>

                <xsl:variable name="width">
                    <xsl:choose>
                        <xsl:when test="$isLandscape">
                            <xsl:text>297mm</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>210mm</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>

                <xsl:variable name="height">
                    <xsl:choose>
                        <xsl:when test="$isLandscape">
                            <xsl:text>210mm</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>297mm</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>

                <fo:simple-page-master master-name="first_only" margin-top="10mm" margin-bottom="10mm" margin-left="20mm" margin-right="20mm">
                    <xsl:attribute name="page-width">
                        <xsl:value-of select="$width" />
                    </xsl:attribute>
                    <xsl:attribute name="page-height">
                        <xsl:value-of select="$height" />
                    </xsl:attribute>
                    <fo:region-body margin-bottom="25mm" />
                    <fo:region-after extent="15mm" />
                </fo:simple-page-master>

                <fo:simple-page-master master-name="other_pages" margin-top="20mm" margin-bottom="10mm" margin-left="20mm" margin-right="20mm">
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

            <fo:page-sequence master-reference="BSB_REPO_A4">
                <fo:static-content flow-name="xsl-region-after" font-family="Barclays" font-size="6pt">

                    <fo:block padding-bottom="2mm">
                        <xsl:value-of select="__XMLReportResources/txt-absareg" />
                    </fo:block>
                </fo:static-content>

                <fo:flow flow-name="xsl-region-body" font-size="8pt">
                    <!-- Header is included in the body as its height is variable because of client address -->
                    <fo:table table-layout="fixed" width="100%">
                        <xsl:choose>
                            <xsl:when test="$isLandscape">
                                <fo:table-column column-width="128.5mm" />
                                <fo:table-column column-width="128.5mm" />
                            </xsl:when>
                            <xsl:otherwise>
                                <fo:table-column column-width="85mm" />
                                <fo:table-column column-width="85mm" />
                            </xsl:otherwise>
                        </xsl:choose>

                        <fo:table-body>
                            <fo:table-row>
                                <fo:table-cell>
                                    <fo:block margin-bottom="10mm">
                                        <fo:external-graphic content-width="27mm" scaling="uniform">
                                            <xsl:attribute name="src">
                                                <xsl:value-of select="__XMLReportResources/img-absa-logo"/>
                                            </xsl:attribute>
                                        </fo:external-graphic>
                                    </fo:block>
                                    <fo:block font-size="9pt" font-family="Helvetica" margin-bottom="10mm" >
                                        <xsl:apply-templates select="Client" />
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-family="Helvetica" font-size="10pt" color="rgb(220, 0, 50)" margin-top="2mm" margin-bottom="3mm" text-align="right">Corporate and Investment Banking</fo:block>
                                    <fo:block font-family="Helvetica" font-size="10pt" color="rgb(220, 0, 50)" font-weight="bold" margin-bottom="3mm" text-align="right">CONFIDENTIAL</fo:block>
                                    <fo:block font-family="Helvetica" font-size="8pt" color="#303030" text-align="right">
                                        <xsl:apply-templates select="Bank" />
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>

                    <xsl:apply-templates select="Content" />
                </fo:flow>
            </fo:page-sequence>
        </fo:root>
    </xsl:template>

    <xsl:template match="/XMLReport/Bank">
        <xsl:call-template name="Contact" />
    </xsl:template>

    <xsl:template match="/XMLReport/Client">
        <xsl:call-template name="Contact" />
    </xsl:template>

    <xsl:template match="/XMLReport/Content">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="/XMLReport/Content/Caption">
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
    
	<xsl:template match="/XMLReport/Content/Table">
		<xsl:choose>
		    <xsl:when test="@tableheader">
                <fo:block keep-with-next.within-page="always" font-weight="bold" font-size="10pt" margin-top="5mm" text-align="left">
                    <xsl:value-of select="@tableheader"/>
                </fo:block>
		    </xsl:when>
		</xsl:choose>	
		<fo:block border-color="rgb(220, 0, 50)" padding-top="2mm" padding-bottom="2mm" padding-right="1mm" margin-bottom="10mm" border-top-style="solid" border-bottom-style="solid" font-weight="normal" font-size="8pt">
            <xsl:choose>
                <xsl:when test="@size = 'small'">
                    <xsl:attribute name="border-width">0.2mm</xsl:attribute>
                    <xsl:attribute name="font-size">8pt</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="border-width">0.5mm</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="@borderwidth">
                        <xsl:attribute name="border-width">
                                <xsl:value-of select="@borderwidth"/>
                        </xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="@alignment">
                        <xsl:attribute name="text-align">
                                <xsl:value-of select="@alignment"/>
                        </xsl:attribute>
                </xsl:when>
            </xsl:choose>

            <fo:table table-layout="auto">
                <xsl:for-each select="Columns/Column">
                    <fo:table-column>
                        <xsl:if test="@width">
                            <xsl:attribute name="column-width">
                                <xsl:value-of select="@width"/>
                            </xsl:attribute>
                        </xsl:if>
                        <xsl:if test="@type = 'currency'">
                            <xsl:attribute name="text-align">end</xsl:attribute>
                        </xsl:if>
                    </fo:table-column>
                </xsl:for-each>
                <fo:table-header font-weight="bold">
                    <fo:table-row>
                        <xsl:for-each select="Columns/Column">
                            <fo:table-cell padding-left="3mm">
                                <fo:block margin-bottom="2mm">
                                    <xsl:variable name="cellvalue" select="."/>
                                    <xsl:choose>
                                        <xsl:when test="contains($cellvalue,'/')">
                                            <xsl:value-of select="concat(substring-before($cellvalue,'/'),'&#8288;','/','&#8288;',substring-after($cellvalue,'/'))"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="$cellvalue"/>
                                        </xsl:otherwise>
                                    </xsl:choose>       
                                </fo:block>
                            </fo:table-cell>
                        </xsl:for-each>
                    </fo:table-row>
                </fo:table-header>
                <fo:table-body>
                    <xsl:for-each select="Rows/Row">
                        <fo:table-row>
                            <xsl:variable name="isSummary" select="@summary='true'"/>
                            <xsl:variable name="isFirstSummary" select="$isSummary and generate-id(.) = generate-id(../Row[@summary='true'][1])"/>
                            <xsl:for-each select="Cell">
                                <fo:table-cell>
                                    <fo:block margin-bottom="1mm">
                                        <!-- Make bold text for summary rows -->
                                        <xsl:if test="$isSummary">
                                            <xsl:attribute name="font-weight">
                                                <xsl:text>bold</xsl:text>
                                            </xsl:attribute>
                                        </xsl:if>
                                        <!-- Draw solid back line for first summary row -->
                                        <xsl:if test="$isFirstSummary">
                                            <xsl:attribute name="border-color">
                                                <xsl:text>black</xsl:text>
                                            </xsl:attribute>
                                            <xsl:attribute name="padding-top">
                                                <xsl:text>3mm</xsl:text>
                                            </xsl:attribute>
                                            <xsl:attribute name="border-top-style">
                                                <xsl:text>solid</xsl:text>
                                            </xsl:attribute>
                                        </xsl:if>
                                        <xsl:value-of select="."/>
                                    </fo:block>
                                </fo:table-cell>
                            </xsl:for-each>
                        </fo:table-row>
                    </xsl:for-each>
                    <!-- At least one row must be present -->
                    <xsl:if test="not(Rows/Row)">
                        <fo:table-cell><fo:block /></fo:table-cell>
                    </xsl:if>
                </fo:table-body>
            </fo:table>
        </fo:block>
        <xsl:choose>
            <xsl:when test="@tablefooter">
                <fo:block keep-with-previous="always" font-weight="normal" font-size="10pt" margin-top="0mm" margin-bottom="10mm" text-align="left">
                    <xsl:value-of select="@tablefooter"/>
                </fo:block>
            </xsl:when>
        </xsl:choose>
	</xsl:template>
	
	<xsl:template match="/XMLReport/Content/PageBreak">
		<fo:block break-after='page'/>
	</xsl:template>
	
    <xsl:template match="/XMLReport/Content/Values">
        <fo:table keep-together="always" table-layout="fixed" width="100%" margin-bottom="3mm">
            <fo:table-column>
                <xsl:choose>
                    <xsl:when test="@width">
                        <xsl:attribute name="column-width">
                            <xsl:value-of select="@width"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="column-width">100mm</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
            </fo:table-column>
            <fo:table-column>
                <xsl:choose>
                    <xsl:when test="@width">
                        <xsl:attribute name="column-width">
                            <xsl:value-of select="@width"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="column-width">proportional-column-width(1)</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
            </fo:table-column>
            <fo:table-body font-size="9pt">
                <xsl:for-each select="Value">
                    <fo:table-row>
                        <xsl:choose>
                            <xsl:when test="not(@key)">
                                <fo:table-cell number-columns-spanned="2">
                                    <fo:block margin-bottom="2mm" border-color="rgb(220, 0, 50)" border-bottom-style="solid" border-width="0.5mm" font-weight="bold">
                                        <xsl:value-of select="." />
                                    </fo:block>
                                </fo:table-cell>
                            </xsl:when>
                            <xsl:otherwise>
                                <fo:table-cell>
                                    <fo:block margin-bottom="2mm">
                                        <xsl:value-of select="@key" />
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block text-align="right">
                                        <xsl:value-of select="." />
                                    </fo:block>
                                </fo:table-cell>
                            </xsl:otherwise>
                        </xsl:choose>
                    </fo:table-row>
                </xsl:for-each>
            </fo:table-body>
        </fo:table>
    </xsl:template>

    <xsl:template match="/XMLReport/Content/Disclaimer">
        <fo:table table-layout="fixed" width="100%" margin-bottom="3mm" page-break-inside="avoid">
            <fo:table-column column-width="100%"/>
            <fo:table-body font-size="9pt">
                <fo:table-row>
                    <fo:table-cell>
                        <fo:block font-weight="bold" margin-bottom="2mm">
                            Disclaimer
                        </fo:block>
                        <xsl:for-each select="Value">
                            <fo:block margin-bottom="2mm" text-align="justify">
                                <xsl:value-of select="." />
                            </fo:block>
                        </xsl:for-each>
                    </fo:table-cell>
                </fo:table-row>
            </fo:table-body>
        </fo:table>
    </xsl:template>

    <xsl:template name="Contact">
    
        <xsl:for-each select="Name|AliasName">
            <fo:block>
                <xsl:if test="position() = last()">
                    <xsl:attribute name="padding-bottom">2mm</xsl:attribute>
                </xsl:if>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>

        <xsl:for-each select="Address/Value">
            <fo:block>
                <xsl:if test="position() = last()">
                    <xsl:attribute name="padding-bottom">2mm</xsl:attribute>
                </xsl:if>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>

        <xsl:for-each select="Tel|Fax|Email">
            <fo:block>
                <xsl:value-of select="name()"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>

        <xsl:for-each select="Web">
            <fo:block>
                <xsl:attribute name="padding-bottom">2mm</xsl:attribute>
                <xsl:value-of select="."/>
            </fo:block>
        </xsl:for-each>

        <xsl:for-each select="Date">
            <fo:block>
                <xsl:value-of select="." />
            </fo:block>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>


