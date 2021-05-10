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

			<!--Trade reference number -->
			<xsl:value-of select="concat('Trade reference number',$comma)" />

			<!--Fund Identifier -->
			<xsl:value-of select="concat('Fund Identifier',$comma)" />

			<!--Instrument Identification code -->
			<xsl:value-of select="concat('Instrument Identification code',$comma)" />

			<!--ISIN -->
			<xsl:value-of select="concat('ISIN',$comma)" />

			<!--Broker Identifier -->
			<xsl:value-of select="concat('Broker Identifier',$comma)" />

			<!--Transaction Type -->
			<xsl:value-of select="concat('Transaction Type',$comma)" />

			<!--Trade date -->
			<xsl:value-of select="concat('Trade date',$comma)" />

			<!--Settlement date -->
			<xsl:value-of select="concat('Settlement date',$comma)" />

			<!--Currency -->
			<xsl:value-of select="concat('Currency',$comma)" />

			<!--Nominal -->
			<xsl:value-of select="concat('Nominal',$comma)" />

                                                <!--Trade price -->
			<xsl:value-of select="concat('Trade price',$comma)" />

			<!--Vat -->
			<xsl:value-of select="concat('Vat',$comma)" />

			<!--Brokerage -->
			<xsl:value-of select="concat('Brokerage',$comma)" />

			<!--Securities Transfer Tax -->
			<xsl:value-of select="concat('Securities Transfer Tax',$comma)" />

			<!--Gross consideration -->
			<xsl:value-of select="concat('Gross consideration',$comma)" />

			<!--Net consideration -->
			<xsl:value-of select="concat('Net consideration',$comma)" />

			<!--Trade status -->
			<xsl:value-of select="concat('Trade Status',$comma)" />

			<!--Original Reference number -->
			<xsl:value-of select="concat('Original reference number',$comma)" />

			<!--Instrument Type -->
			<xsl:value-of select="concat('Instrument Type',$comma)" />

			<!--Start Date-->
			<xsl:value-of select="concat('Start Date',$comma)" />

			<!--Maturity Date -->
			<xsl:value-of select="concat('Maturity Date',$comma)" />

			<!--Pay Leg Type -->
			<xsl:value-of select="concat('Pay Leg Type',$comma)" />

			<!--Pay Fixed Rate -->
			<xsl:value-of select="concat('Pay Fixed Rate',$comma)" />

			<!--Pay Setlement Frequency -->
			<xsl:value-of select="concat('Pay Settlement Frequency',$comma)" />

			<!--Pay Floating Reference -->
			<xsl:value-of select="concat('Pay Floating Reference',$comma)" />

			<!--Receive Leg Type -->
			<xsl:value-of select="concat('Receive Leg Type',$comma)" />

			<!--Receive Fixed Rate -->
			<xsl:value-of select="concat('Receive Fixed Rate',$comma)" />

			<!--Receive Settlement Frequency -->
			<xsl:value-of select="concat('Receive Settlement Frequency',$comma)" />

			<!--Receive Floating Reference -->
			<xsl:value-of select="concat('Receive Floating Reference',$comma)" />

			<!--Clean Price -->
			<xsl:value-of select="concat('Clean Price',$comma)" />

			<!--Accrued Interest Amount -->
			<xsl:value-of select="concat('Accrued Interest Amount',$comma)" />

			<!--Derivative Type -->
			<xsl:value-of select="concat('Derivative Type',$comma)" />

			<!--Contract Type -->
			<xsl:value-of select="concat('Contract Type',$comma)" />

			<!--Strike Price -->
			<xsl:value-of select="concat('Strike Price',$comma)" />

			<!--Underlying Instrument -->
			<xsl:value-of select="concat('Underlying Instrument',$comma)" />

			<!--Underlying Type -->
			<xsl:value-of select="concat('Underlying Type',$comma)" />

			<!--Yield Leg 1-->
			<xsl:value-of select="concat('Yield Leg 1',$comma)" />

			<!--Yield Leg 2 -->
			<xsl:value-of select="concat('Yield Leg 2',$comma)" />

			<!--Total Consideration Leg 1-->
			<xsl:value-of select="concat('Total Consideration Leg 1',$comma)" />

			<!--Total Consideration Leg 2-->
			<xsl:value-of select="concat('Total Consideration Leg 2',$comma)" />

			<!--Repo Rate-->
			<xsl:value-of select="concat('Repo Rate',$comma)" />

                                                <!--Fully Funded-->
			<xsl:value-of select="concat('Fully Funded',$comma)" />

			<!--Clean Consideration Leg 1-->
			<xsl:value-of select="concat('Clean Consideration Leg 1',$comma)" />

			<!--Clean Consideration Leg 2-->
			<xsl:value-of select="concat('Clean Consideration Leg 2',$comma)" />

                                                <!--Accrued Interest Leg 1-->
			<xsl:value-of select="concat('Accrued Interest Leg 1',$comma)" />

                                                <!--Accrued Interest Leg 2-->
			<xsl:value-of select="'Accrued Interest Leg 2'" />

			<!--Break line -->
			<xsl:value-of select="$eoln" />

			<!--Apply rows -->
			<xsl:apply-templates select="ReportContents/Table/Rows/Row" />
	</xsl:template>



	<xsl:template match="Row" >

		<!--Trade Reference Number -->
		<xsl:value-of select="concat(Label, $comma)" />

		<!--Fund Identifier -->
		<xsl:value-of select="concat(Cells/Cell[47]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[1]/RawData, ',' , '')-->

		<!--Instrument Identification code-->
		<xsl:variable name="InstrumentName">
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="Cells/Cell[3]/FormattedData"/>
				<xsl:with-param name="replace" select="'ZAR/'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($InstrumentName,',',''),$comma)"/>
		<!--translate(Cells/Cell[3]/RawData, ',' , '')-->

		<!--ISIN-->
		<xsl:value-of select="concat(Cells/Cell[4]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[4]/RawData, ',' , '')-->

		<!--Broker Identifier-->
		<xsl:value-of select="concat(Cells/Cell[2]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[2]/RawData, ',' , '')-->

		<!--Transaction Type-->
		<xsl:value-of select="concat(Cells/Cell[7]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[7]/RawData, ',' , '')-->

		<!--Trade date-->
		<xsl:variable name="date" select="translate(Cells/Cell[54]/FormattedData,'PM','')"/>
		<xsl:value-of select="concat($date,$comma)" />

		<!--Settlement date-->
		<xsl:value-of select="concat(Cells/Cell[9]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[9]/RawData, ',' , '')-->

		<!--Currency-->
		<xsl:value-of select="concat(Cells/Cell[6]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[6]/RawData, ',' , '')-->

		<!--Nominal-->
		<xsl:variable name="nominal" select="translate(Cells/Cell[10]/FormattedData,',','')"/>
		<xsl:value-of select="concat($nominal,$comma)" />

                                <!--Trade price-->
		<xsl:variable name="tprice" select="translate(Cells/Cell[11]/FormattedData,',','')"/>
		<xsl:value-of select="concat($tprice,$comma)" />

		<!--Vat-->
		<xsl:variable name="vat" select="translate(Cells/Cell[12]/FormattedData,',','')"/>
		<xsl:value-of select="concat($vat,$comma)" />

		<!--Brokerage-->
		<xsl:variable name="brokerage" select="translate(Cells/Cell[13]/FormattedData,',','')"/>
		<xsl:value-of select="concat($brokerage,$comma)" />

		<!--Securities Transfer Tax-->
		<xsl:variable name="stt" select="translate(Cells/Cell[15]/FormattedData,',','')"/>
		<xsl:value-of select="concat($stt,$comma)" />

		<!--Gross consideration-->
		<xsl:variable name="gross" select="translate(Cells/Cell[46]/FormattedData,',','')"/>
		<xsl:value-of select="concat($gross,$comma)" />

		<!--Net consideration-->
		<xsl:variable name="net" select="translate(Cells/Cell[45]/FormattedData,',','')"/>
		<xsl:value-of select="concat($net,$comma)" />

		<!--Trade status-->
		<xsl:value-of select="concat(Cells/Cell[17]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[17]/RawData, ',' , '')-->

		<!--Original Reference number-->
		<xsl:value-of select="concat(Cells/Cell[19]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[20]/RawData, ',' , '')-->

		<!--Instrument Type -->
		<xsl:value-of select="concat(Cells/Cell[5]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[5]/RawData, ',' , '')-->

		<!--Start Date-->
		<xsl:value-of select="concat(Cells/Cell[30]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[30]/RawData, ',' , '')-->

		<!--Maturity Date-->
		<xsl:value-of select="concat(Cells/Cell[26]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[26]/RawData, ',' , '')-->

		<!--Pay Leg Type-->
		<xsl:value-of select="concat(Cells/Cell[31]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[31]/RawData, ',' , '')-->

		<!--Pay Fixed Rate-->
		<xsl:variable name="payfix" select="translate(Cells/Cell[32]/FormattedData,',','')"/>
		<xsl:value-of select="concat($payfix,$comma)" />

		<!--Pay Settlement Frequency-->
		<xsl:value-of select="concat(Cells/Cell[33]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[33]/RawData, ',' , '')-->

		<!--Pay Float Ref-->
		<xsl:value-of select="concat(Cells/Cell[34]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[34]/RawData, ',' , '')-->

		<!--Receive Leg Type-->
		<xsl:value-of select="concat(Cells/Cell[35]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[35]/RawData, ',' , '')-->

		<!--Receive Fixed Rate-->
		<xsl:variable name="recfix" select="translate(Cells/Cell[36]/FormattedData,',','')"/>
		<xsl:value-of select="concat($recfix,$comma)" />

		<!--Receive Settlement Frequency-->
		<xsl:value-of select="concat(Cells/Cell[37]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[37]/RawData, ',' , '')-->

		<!--Receive Float Ref-->
		<xsl:value-of select="concat(Cells/Cell[38]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[38]/RawData, ',' , '')-->

		<!--Clean Price-->
		<xsl:variable name="CleanPrice">
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="Cells/Cell[23]/FormattedData"/>
				<xsl:with-param name="replace" select="'#'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($CleanPrice,',',''),$comma)"/>
		<!--translate(Cells/Cell[23]/RawData, ',' , '')-->

		<!--Accrued Interest Amount-->
		<xsl:variable name="Accrued">
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="Cells/Cell[25]/FormattedData"/>
				<xsl:with-param name="replace" select="'#'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($Accrued,',',''),$comma)"/>
		<!--translate(Cells/Cell[25]/RawData, ',' , '')-->


		<!--Derivative Type-->
		<xsl:value-of select="concat(Cells/Cell[5]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[5]/RawData, ',' , '')-->

		<!--Contract Type-->
		<xsl:value-of select="concat(Cells/Cell[28]/FormattedData,$comma)" />
		<!--translate(Cells/Cell[28]/RawData, ',' , '')-->

		<!--Strike Price-->
		<xsl:variable name="strike" select="translate(Cells/Cell[27]/FormattedData,',','')"/>
		<xsl:value-of select="concat($strike,$comma)" />

                                <!--Underlying Instrument-->
		<xsl:variable name="UndInsName">
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="Cells/Cell[29]/FormattedData"/>
				<xsl:with-param name="replace" select="'ZAR/'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($UndInsName,',',''),$comma)"/>
		<!--translate(Cells/Cell[29]/RawData, ',' , '')-->


		<!--Underlying Type-->
		<xsl:variable name="utype" select="translate(Cells/Cell[40]/FormattedData,',','')"/>
		<xsl:value-of select="concat($utype,$comma)" />

		<!--Start Price-->
		<xsl:variable name="sprice" select="translate(Cells/Cell[11]/FormattedData,',','')"/>
		<xsl:value-of select="concat($sprice,$comma)" />

		<!--End Price-->
		<xsl:variable name="endprice" select="translate(Cells/Cell[41]/FormattedData,',','')"/>
		<xsl:value-of select="concat($endprice,$comma)" />

		<!--Start Cash-->
		<xsl:variable name="startcash" select="translate(Cells/Cell[42]/FormattedData,',','')"/>
		<xsl:value-of select="concat($startcash,$comma)" />

		<!--End Cash-->
		<xsl:variable name="endcash" select="translate(Cells/Cell[43]/FormattedData,',','')"/>
		<xsl:value-of select="concat($endcash,$comma)" />


		<!--Repo Rate-->
		<xsl:variable name="reporate" select="translate(Cells/Cell[44]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($reporate,$comma)" />
		<!--translate(Cells/Cell[44]/RawData, ',' , '')-->

		<!--Fully Funded-->
		<xsl:variable name="fullyfunded" select="translate(Cells/Cell[48]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($fullyfunded,$comma)" />
		<!--translate(Cells/Cell[48]/FormattedData, ',' , '')-->

		<!--Clean Consideration Leg 1-->
		<xsl:variable name="cleanCons1" select="translate(Cells/Cell[50]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($cleanCons1,$comma)" />
		<!--translate(Cells/Cell[50]/RawData, ',' , '')-->

		<!--Clean Consideration Leg 2-->
		<xsl:variable name="cleanCons2" select="translate(Cells/Cell[51]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($cleanCons2,$comma)" />
		<!--translate(Cells/Cell[51]/RawData, ',' , '')-->

		<!--Accrued Interest Leg 1-->
		<xsl:variable name="accInt1" select="translate(Cells/Cell[52]/FormattedData,',','')"/>
                                <xsl:value-of select="concat($accInt1,$comma)" />
		<!--translate(Cells/Cell[52]/RawData, ',' , '')-->

		<!--Accrued Interest Leg 2-->
		<xsl:variable name="accInt2" select="translate(Cells/Cell[53]/FormattedData,',','')"/>
                                <xsl:value-of select="$accInt2" />
		<!--translate(Cells/Cell[53]/RawData, ',' , '')-->

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


