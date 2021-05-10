#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">

	<xsl:output method="text" encoding="ISO-8859-1"/>

	<!-- Constants -->
	<xsl:param name="comma" select="string(',')"/>
	<xsl:param name="underscore" select="string('_')"/>
	<xsl:param name="doubleQuote" select="string('&#x22;')"/>
	<xsl:param name="eoln" select="string('&#13;')"/>
	<xsl:param name="datefmt" select="string('dd/mm/yyyy')"/>
	<xsl:variable name="emptyString" select="string('')"/>

	<xsl:template match="/PRIMEReport">

			<!--Instrument -->
			<xsl:value-of select="concat('Instrument',$comma)" />

			<!--Type -->
			<xsl:value-of select="concat('Type',$comma)" />

			<!--OTC/Exchange -->
			<xsl:value-of select="concat('OTC/Exchange',$comma)" />

			<!--Expiry -->
			<xsl:value-of select="concat('Expiry',$comma)" />

			<!--Opening Position -->
			<xsl:value-of select="concat('Opening Position',$comma)" />

			<!--Opening Price -->
			<xsl:value-of select="concat('Opening Price',$comma)" />

			<!--Opening Market Value -->
			<xsl:value-of select="concat('Opening Market Value',$comma)" />

			<!--Closing Position -->
			<xsl:value-of select="concat('Closing Position',$comma)" />

			<!--Closing Price -->
			<xsl:value-of select="concat('Closing Price',$comma)" />

			<!--Closing Market Value -->
			<xsl:value-of select="concat('Closing Market Value',$comma)" />

                                                <!--PLPos -->
			<xsl:value-of select="concat('PLPos',$comma)" />

			<!--Daily MTM -->
			<xsl:value-of select="concat('Daily MTM',$comma)" />

                                                <!--Market Exposure -->
			<xsl:value-of select="'Market Exposure'" />

			<!--Break line -->
			<xsl:value-of select="$eoln" />

			<!--Apply rows -->
			<xsl:apply-templates select="ReportContents/Table/Rows/Row/Rows/Row/Rows/Row" />
	</xsl:template>



	<xsl:template match="Row" >

		<!--Instrument -->
		<xsl:variable name="synopskey" select="concat(Label, $underscore)"/>
		<xsl:variable name="synopskey2" select="concat($synopskey, ../../Label)"/>
		<xsl:value-of select="concat($synopskey2,$comma)" />

		<!--Type -->
		<xsl:value-of select="concat(Cells/Cell[1]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[1]/RawData, ',' , '')-->

		<!--OTC/Exchange-->
		<xsl:value-of select="concat(Cells/Cell[2]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[2]/RawData, ',' , '')-->

		<!--Expiry-->
		<xsl:value-of select="concat(Cells/Cell[3]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[3]/RawData, ',' , '')-->

		<!--Opening Position-->
		<xsl:variable name="openingpos" select="translate(Cells/Cell[4]/FormattedData,',','')"/>
		<xsl:value-of select="concat($openingpos,$comma)" />
		<!--translate(Cells/Cell[4]/RawData, ',' , '')-->

		<!--Opening Price-->
		<xsl:variable name="openingprice" select="translate(Cells/Cell[5]/FormattedData,',','')"/>
		<xsl:value-of select="concat($openingprice,$comma)" />
		<!--translate(Cells/Cell[5]/RawData, ',' , '')-->

		<!--Opening Market Value-->
		<xsl:variable name="openingmarketval" select="translate(Cells/Cell[6]/FormattedData,',','')"/>
		<xsl:value-of select="concat($openingmarketval,$comma)" />
		<!--translate(Cells/Cell[6]/RawData, ',' , '')-->

		<!--Closing Position-->
		<xsl:variable name="closingpos" select="translate(Cells/Cell[7]/FormattedData,',','')"/>
		<xsl:value-of select="concat($closingpos,$comma)" />
		<!--translate(Cells/Cell[7]/RawData, ',' , '')-->

                                <!--Closing Price-->
		<xsl:variable name="closingprice" select="translate(Cells/Cell[8]/FormattedData,',','')"/>
		<xsl:value-of select="concat($closingprice,$comma)" />
		<!--translate(Cells/Cell[8]/RawData, ',' , '')-->

		<!--Closing Market Value-->
		<xsl:variable name="closingmarketval" select="translate(Cells/Cell[9]/FormattedData,',','')"/>
		<xsl:value-of select="concat($closingmarketval,$comma)" />
		<!--translate(Cells/Cell[9]/RawData, ',' , '')-->

		<!--PLPos-->
		<xsl:value-of select="concat(Cells/Cell[10]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[10]/RawData, ',' , '')-->

		<!--Daily MTM -->
		<xsl:variable name="dailymtm" select="translate(Cells/Cell[11]/FormattedData,',','')"/>
		<xsl:value-of select="concat($dailymtm,$comma)" />
		<!--translate(Cells/Cell[11]/RawData, ',' , '')-->

		<!--Market Exposure-->
		<xsl:variable name="marketexp" select="translate(Cells/Cell[12]/FormattedData,',','')"/>
                                <xsl:value-of select="$marketexp" />
		<!--translate(Cells/Cell[12]/RawData, ',' , '')-->

		<!--Break line -->
		<xsl:value-of select="$eoln" />
	</xsl:template>

<!-- Template for replacing text -->
	<xsl:template name="string-replace-all">
		<xsl:param name="text"/>
		<xsl:param name="replace"/>
		<xsl:param name="by"/>
		<xsl:choose>
			<xsl:when test="contains($text, $replace)">
				<xsl:value-of select="substring-before($text,$replace)"/>
				<xsl:value-of select="$by"/>
				<xsl:call-template name="string-replace-all">
					<xsl:with-param name="text" select="substring-after($text,$replace)"/>
					<xsl:with-param name="replace" select="$replace"/>
					<xsl:with-param name="by" select="$by"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

</xsl:stylesheet>


