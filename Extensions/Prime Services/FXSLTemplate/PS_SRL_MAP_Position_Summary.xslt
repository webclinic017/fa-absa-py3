#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">

	<xsl:output method="text" encoding="ISO-8859-1"/>

	<!-- Constants -->
	<xsl:param name="comma" select="string(',')"/>
	<xsl:param name="doubleQuote" select="string('&#x22;')"/>
	<xsl:param name="eoln" select="string('&#13;')"/>
	<xsl:param name="datefmt" select="string('dd/mm/yyyy')"/>
	<xsl:variable name="emptyString" select="string('')"/>

	<xsl:template match="/PRIMEReport">

			<!--Instrument Description -->
			<xsl:value-of select="concat('Instrument Description',$comma)" />

			<!--Portfolio -->
			<xsl:value-of select="concat('Portfolio',$comma)" />

			<!--Position Date -->
			<xsl:value-of select="concat('Position Date',$comma)" />

			<!--Financed or Funded -->
			<xsl:value-of select="concat('Financed or Funded',$comma)" />

			<!--OTC or Exchange -->
			<xsl:value-of select="concat('OTC or Exchange',$comma)" />

			<!--Instrument Type -->
			<xsl:value-of select="concat('Instrument Type',$comma)" />

			<!--Instrument Identifier -->
			<xsl:value-of select="concat('Instrument Identifier',$comma)" />

			<!--Instrument Identifier Type -->
			<xsl:value-of select="concat('Instrument Identifier Type',$comma)" />

			<!--Underlying Identifier -->
			<xsl:value-of select="concat('Underlying Identifier',$comma)" />

			<!--Underlying Identifier Type -->
			<xsl:value-of select="concat('Underlying Identifier Type',$comma)" />

                                                <!--Opening Position -->
			<xsl:value-of select="concat('Opening Position',$comma)" />

			<!--Closing Position -->
			<xsl:value-of select="concat('Closing Position',$comma)" />

			<!--Closing Price Dirty -->
			<xsl:value-of select="concat('Closing Price Dirty',$comma)" />

			<!--Price Currency -->
			<xsl:value-of select="concat('Price Currency',$comma)" />

			<!--Price Multiplier -->
			<xsl:value-of select="concat('Price Multiplier',$comma)" />

			<!--Closing Market Value -->
			<xsl:value-of select="concat('Closing Market Value',$comma)" />

			<!--Closing Market Exposure -->
			<xsl:value-of select="concat('Closing Market Exposure',$comma)" />

			<!--MTM Change -->
			<xsl:value-of select="concat('MTM Change',$comma)" />

			<!--Daily Provision -->
			<xsl:value-of select="concat('Daily Provision',$comma)" />

			<!--Daily Funding-->
			<xsl:value-of select="concat('Daily Funding',$comma)" />

			<!--Execution Charge -->
			<xsl:value-of select="concat('Execution Charge',$comma)" />

			<!--STT -->
			<xsl:value-of select="concat('STT',$comma)" />

			<!--VAT -->
			<xsl:value-of select="concat('VAT',$comma)" />

			<!--Daily PnL -->
			<xsl:value-of select="concat('Daily PnL',$comma)" />

			<!--Yearly PnL -->
			<xsl:value-of select="concat('Yearly PnL',$comma)" />

			<!--Funding Rate (%) -->
			<xsl:value-of select="concat('Funding Rate (%)',$comma)" />

			<!--Maturity Date -->
			<xsl:value-of select="concat('Maturity Date',$comma)" />

			<!--CouponRate (%) -->
			<xsl:value-of select="concat('CouponRate (%)',$comma)" />

			<!--Option Type -->
			<xsl:value-of select="concat('Option Type',$comma)" />

			<!--Option Strike -->
			<xsl:value-of select="concat('Option Strike',$comma)" />

			<!--Closing Price Clean -->
			<xsl:value-of select="concat('Closing Price Clean',$comma)" />

			<!--Currency2 -->
			<xsl:value-of select="concat('Currency2',$comma)" />

                                                <!--RepoRate (%) -->
			<xsl:value-of select="'RepoRate (%) '" />

			<!--Break line -->
			<xsl:value-of select="$eoln" />

			<!--Apply rows -->
			<xsl:apply-templates select="ReportContents/Table/Rows/Row/Rows/Row" />
	</xsl:template>



	<xsl:template match="Row" >

		<!--Instrument Description -->
		<xsl:value-of select="concat(Label, $comma)" />

		<!--Portfolio -->
		<xsl:value-of select="concat(Cells/Cell[1]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[2]/RawData, ',' , '')-->

		<!--Position Date-->
		<xsl:value-of select="concat(Cells/Cell[2]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[3]/RawData, ',' , '')-->

		<!--Financed or Funded-->
		<xsl:value-of select="concat(Cells/Cell[3]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[4]/RawData, ',' , '')-->

		<!--OTC or Exchange-->
		<xsl:value-of select="concat(Cells/Cell[4]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[5]/RawData, ',' , '')-->

		<!--Instrument Type-->
		<xsl:value-of select="concat(Cells/Cell[5]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[6]/RawData, ',' , '')-->

		<!--Instrument Identifier-->
		<xsl:value-of select="concat(Cells/Cell[6]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[7]/RawData, ',' , '')-->

		<!--Instrument Identifier Type-->
		<xsl:value-of select="concat(Cells/Cell[7]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[8]/RawData, ',' , '')-->

		<!--Underlying Identifier-->
		<xsl:value-of select="concat(Cells/Cell[8]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[9]/RawData, ',' , '')-->

		<!--Underlying Identifier Type-->
		<xsl:value-of select="concat(Cells/Cell[9]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[10]/RawData, ',' , '')-->

                                <!--Opening Position-->
                                <xsl:variable name="openingpos" select="translate(Cells/Cell[10]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($openingpos,$comma)" />
                                <!--translate(Cells/Cell[11]/RawData, ',' , '')-->

                                <!--Closing Position-->
                                <xsl:variable name="closingpos" select="translate(Cells/Cell[11]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($closingpos,$comma)" />
                                <!--translate(Cells/Cell[12]/RawData, ',' , '')-->

                                <!--Closing Price Dirty-->
                                <xsl:variable name="ClosingDirtyPrice">
                                        <xsl:call-template name="string-replace-all">
                                                <xsl:with-param name="text" select="Cells/Cell[12]/FormattedData"/>
                                                <xsl:with-param name="replace" select="'Nan'"/>
                                                <xsl:with-param name="by" select="$emptyString"/>
                                        </xsl:call-template>
                                </xsl:variable>
                                <xsl:value-of select="concat(translate($ClosingDirtyPrice,',',''),$comma)"/>
                                <!--translate(Cells/Cell[13]/RawData, ',' , '')-->

		<!--Price Currency-->
		<xsl:value-of select="concat(Cells/Cell[13]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[14]/RawData, ',' , '')-->

		<!--Price Multiplier-->
		<xsl:value-of select="concat(Cells/Cell[14]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[15]/RawData, ',' , '')-->

		<!--Closing Market Value-->
		<xsl:variable name="closingmarketval" select="translate(Cells/Cell[15]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($closingmarketval,$comma)" />
		<!--translate(Cells/Cell[16]/RawData, ',' , '')-->

		<!--Closing Market Exposure-->
		<xsl:variable name="closingmarketexp" select="translate(Cells/Cell[16]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($closingmarketexp,$comma)" />
		<!--translate(Cells/Cell[17]/RawData, ',' , '')-->

		<!--MTM Change-->
		<xsl:variable name="mtmchange" select="translate(Cells/Cell[17]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($mtmchange,$comma)" />
		<!--translate(Cells/Cell[18]/RawData, ',' , '')-->

		<!--Daily Provision -->
		<xsl:variable name="dailyprov" select="translate(Cells/Cell[18]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($dailyprov,$comma)" />
		<!--translate(Cells/Cell[19]/RawData, ',' , '')-->

		<!--Daily Funding-->
		<xsl:variable name="dailyfund" select="translate(Cells/Cell[19]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($dailyfund,$comma)" />
		<!--translate(Cells/Cell[20]/RawData, ',' , '')-->

		<!--Execution Charge-->
		<xsl:variable name="execution" select="translate(Cells/Cell[20]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($execution,$comma)" />
		<!--translate(Cells/Cell[21]/RawData, ',' , '')-->

		<!--STT-->
		<xsl:variable name="stt" select="translate(Cells/Cell[21]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($stt,$comma)" />
		<!--translate(Cells/Cell[22]/RawData, ',' , '')-->

		<!--VAT-->
		<xsl:variable name="vat" select="translate(Cells/Cell[22]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($vat,$comma)" />
		<!--translate(Cells/Cell[23]/RawData, ',' , '')-->

		<!--Daily PnL-->
		<xsl:variable name="dpnl" select="translate(Cells/Cell[23]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($dpnl,$comma)" />
		<!--translate(Cells/Cell[24]/RawData, ',' , '')-->

		<!--Yearly PnL-->
		<xsl:variable name="ypnl" select="translate(Cells/Cell[24]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($ypnl,$comma)" />
		<!--translate(Cells/Cell[25]/RawData, ',' , '')-->

		<!--Funding Rate (%)-->
		<xsl:value-of select="concat(Cells/Cell[25]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[26]/RawData, ',' , '')-->

		<!--Maturity Date-->
		<xsl:value-of select="concat(Cells/Cell[26]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[27]/RawData, ',' , '')-->

		<!--CouponRate (%)-->
		<xsl:value-of select="concat(Cells/Cell[27]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[28]/RawData, ',' , '')-->

		<!--Option Type-->
		<xsl:value-of select="concat(Cells/Cell[28]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[29]/RawData, ',' , '')-->

		<!--Option Strike-->
		<xsl:value-of select="concat(Cells/Cell[29]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[30]/RawData, ',' , '')-->

		<!--Closing Price Clean-->
		<xsl:variable name="ClosingCleanPrice">
                                        <xsl:call-template name="string-replace-all">
                                                <xsl:with-param name="text" select="Cells/Cell[30]/FormattedData"/>
                                                <xsl:with-param name="replace" select="'Nan'"/>
                                                <xsl:with-param name="by" select="$emptyString"/>
                                        </xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($ClosingCleanPrice,',',''),$comma)"/>
		<!--translate(Cells/Cell[31]/RawData, ',' , '')-->

		<!--Currency2-->
		<xsl:value-of select="concat(Cells/Cell[31]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[32]/RawData, ',' , '')-->

		<!--RepoRate (%)-->
		<xsl:variable name="reporate" select="translate(Cells/Cell[32]/FormattedData,',','')"/>
                                <xsl:value-of select="$reporate" />
		<!--translate(Cells/Cell[33]/RawData, ',' , '')-->

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
