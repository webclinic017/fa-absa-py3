<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:FA="http://fron.com/arena/primereport">
                <!-- If there are more columns than this value they will not be included in the output document -->
                <xsl:variable name="maxNrOfColumns" select="11"/>
                <xsl:variable name="isMultiReport" select="count(/MultiReport)"/>

	<xsl:template match="/">
		<fo:root>
			<fo:layout-master-set>
				<fo:simple-page-master margin-right="1cm" margin-left="1cm" margin-bottom="1.3cm" margin-top="1cm" page-width="21cm" page-height="29.7cm" master-name="first">
					<fo:region-body margin-top="1.5cm" margin-bottom="1.5cm"/>
					<fo:region-before extent="2cm"/>
					<fo:region-after extent="1.5cm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			<fo:page-sequence master-reference="first">
				<fo:static-content flow-name="xsl-region-before">
					<fo:block text-align-last="justify" font-size="10pt">
                                                                                                <xsl:choose>
                                                                                                <!-- Multiple reports in document -->
                                                                                                <xsl:when test="$isMultiReport = '1'">
                                                                                                    <fo:inline>
                                                                                                            Multiple Report
                                                                                                    </fo:inline>
                                                                                                    <fo:leader/>
                                                                                                </xsl:when>
                                                                                                <!-- Only one report in document -->
                                                                                                <xsl:otherwise>
                                                                                                        <fo:inline>
							<xsl:value-of select="//Type"/>
                                                                                                        </fo:inline>
                                                                                                        <fo:leader/>
                                                                                                        <fo:inline>
                                                                                                                <xsl:value-of select="//Name"/>
                                                                                                        </fo:inline>
                                                                                                </xsl:otherwise>
						</xsl:choose>
					</fo:block>
					<fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
				</fo:static-content>

				<fo:static-content flow-name="xsl-region-after">
                                                                                <fo:block>
						<fo:leader leader-length="100%" leader-pattern="rule" rule-thickness="1pt"/>
					</fo:block>
                                                                                <fo:block text-align-last="justify" font-size="10pt">
                                                                                                <!-- Only one report in document -->
                                                                                                <xsl:if test="$isMultiReport = '0'">
                                                                                                    <fo:inline>
                                                                                                            <xsl:value-of select="concat(substring(//LocalTime[1],1,10),' ',substring(//LocalTime[1],12,8),' (UTC', substring(//LocalTime[1],20,6),')')"/>
                                                                                                    </fo:inline>
						</xsl:if>
						<fo:leader/>
						<fo:inline>
                                                                                                                Page <fo:page-number/>
						</fo:inline>
					</fo:block>
				</fo:static-content>

				<fo:flow flow-name="xsl-region-body">

                                                                    <xsl:if test="$isMultiReport = '1'">
                                                                        <!-- Multiple reports in document -->
                                                                        <!-- List of reports -->
                                                                        <fo:table table-layout="fixed" width="100%">
                                                                        <fo:table-column column-width="5cm"/>
                                                                        <fo:table-column column-width="9cm"/>
                                                                        <fo:table-column column-width="5cm"/>
                                                                        <fo:table-body>
                                                                        <xsl:for-each select="//PRIMEReport">
                                                                            <fo:table-row>
                                                                                <fo:table-cell>
                                                                                    <fo:block line-height="14pt" font-size="8pt"><xsl:value-of select="Type"/></fo:block>
                                                                                </fo:table-cell>
                                                                                <fo:table-cell>
                                                                                    <fo:block line-height="14pt" font-size="8pt"><xsl:value-of select="Name"/></fo:block>
                                                                                </fo:table-cell>
                                                                                <fo:table-cell>
                                                                                    <fo:block line-height="14pt" font-size="8pt"><xsl:value-of select="concat(substring(LocalTime,1,10),' ',substring(LocalTime,12,8),' (UTC', substring(LocalTime,20,6),')')"/></fo:block>
                                                                                </fo:table-cell>
                                                                            </fo:table-row>
                                                                        </xsl:for-each>
                                                                        </fo:table-body>
                                                                        </fo:table>
                                                                    </xsl:if>

                                                                    <xsl:apply-templates/>
				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>
	<xsl:template match="Table">

                                <xsl:comment> Variables used to set columns widths, depending on how many columns there are. </xsl:comment>
		<xsl:variable name="numberOfColumns" select="count(Columns/Column)"/>
                                <xsl:variable name="colWidth" select="3.3 - (($numberOfColumns - 1)*0.2)"/>
                                <xsl:variable name="colWidth2" select="3.3 - (($maxNrOfColumns - 1)*0.2)"/>

		<fo:block space-before="1cm"/>

                                <xsl:if test="$isMultiReport = '1'">
                                <!-- Multiple reports in document -->
                                    <fo:block line-height="14pt" font-size="8pt">
                                       <!-- Report header -->
                                        <xsl:value-of select="./../../Type"/>
                                        <xsl:text>:   </xsl:text>
                                        <xsl:value-of select="./../../Name"/>
                                        <xsl:text>   </xsl:text>
                                        <xsl:value-of select="concat(substring(../../LocalTime,1,10),' ',substring(../../LocalTime,12,8),' (UTC', substring(../../LocalTime,20,6),')')"/>
                                    </fo:block>
		</xsl:if>

		<fo:table table-layout="fixed" width="100%">
			<fo:table-column column-width="3cm"/>
			<xsl:comment> Setting column widhts </xsl:comment>
			<xsl:for-each select="Columns/Column[position()]">
                                                                <xsl:choose>
                                                                <xsl:when test="$numberOfColumns > $maxNrOfColumns">
                                                                    <fo:table-column column-width="{$colWidth2}cm"/>
                                                                </xsl:when>
                                                                <xsl:otherwise>
                                                                    <fo:table-column column-width="{$colWidth}cm"/>
                                                                </xsl:otherwise>
                                                                </xsl:choose>
			</xsl:for-each>
			<fo:table-header>
				<fo:table-row>
					<fo:table-cell background-color="#cccccc">
						<fo:block font-weight="bold" text-align="center" vertical-align="middle" border-width="1pt" border-color="black" background-color="#cccccc">

						</fo:block>
					</fo:table-cell>
					<xsl:for-each select="Columns/Column[position()]">
						<fo:table-cell>
							<fo:block font-size="6pt" font-weight="bold" text-align="right" vertical-align="middle" border-width="1pt" border-color="black" background-color="#cccccc">
                                                                                                                    <xsl:if test="position() &lt;= $maxNrOfColumns">
                                                                                                                        <xsl:value-of select="Label"/>
                                                                                                                    </xsl:if>
							</fo:block>
						</fo:table-cell>
					</xsl:for-each>
				</fo:table-row>
			</fo:table-header>
			<fo:table-body>
				<xsl:apply-templates select="Rows/Row">
					<xsl:with-param name="treeDepth" select="1"/>
				</xsl:apply-templates>
			</fo:table-body>
		</fo:table>
	</xsl:template>
	<xsl:template match="Row">
		<xsl:param name="treeDepth"/>
		<xsl:if test="$treeDepth='1'">
			<fo:table-row>
				<fo:table-cell>
					<fo:block>
						 <fo:leader/>
					</fo:block>
				</fo:table-cell>
			</fo:table-row>
		</xsl:if>
		<fo:table-row>
			<xsl:if test="$treeDepth='1'">
				<xsl:attribute name="font-weight">bold</xsl:attribute>
			</xsl:if>
			<fo:table-cell>
				<xsl:attribute name="padding-left"><xsl:value-of select="($treeDepth - 1) * 6"/>pt
				</xsl:attribute>
				<fo:block font-weight="bold" border-right-width="0.5pt" text-align="left" vertical-align="middle" font-size="6pt">
					<xsl:value-of select="Label"/>
				</fo:block>
			</fo:table-cell>
			<xsl:for-each select="Cells/Cell">
                                                                <xsl:if test="position() &lt;= $maxNrOfColumns">
                                                                    <fo:table-cell>
                                                                            <fo:block border-right-width="0.5pt" text-align="right" vertical-align="middle" font-size="6pt">
                                                                                    <xsl:if test="$treeDepth='1'">
                                                                                            <xsl:attribute name="font-weight">bold</xsl:attribute>
                                                                                    </xsl:if>
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
