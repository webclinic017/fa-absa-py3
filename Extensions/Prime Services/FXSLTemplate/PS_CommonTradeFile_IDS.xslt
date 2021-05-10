#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv

<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
	<xsl:output method="text" encoding="ISO-8859-1"/>
	<!-- Constants -->
	<xsl:strip-space elements="*"/>
	<xsl:variable name="comma" select="string(',')"/>
	<xsl:variable name="doubleQuote" select="string('&#x22;')"/>
	<xsl:variable name="eoln">
		<xsl:text>&#13;&#10;</xsl:text>
	</xsl:variable>
	<xsl:variable name="pricefmt" select="string('#0.000000')"/>
	<xsl:variable name="qtyfmt" select="string('#0')"/>
	<xsl:variable name="emptyString" select="string('')"/>
	<!-- Main Entry Point -->
	<xsl:template match="PRIMEReport">
		<!-- Write the header row -->
		<xsl:call-template name="WriteHeader"/>
		<!-- Apply the table template -->
		<xsl:apply-templates select="ReportContents/Table"/>
	</xsl:template>
	<!-- Table template -->
	<xsl:template match="Table">

		<!-- Apply the row template for each row -->
		<xsl:apply-templates select="Rows/Row"/>
	</xsl:template>
	<!-- Template for writing out each data row -->
	<xsl:template match="Row">
		<!-- *************************************************** -->
		<!-- Mapping the values for each row to variables -->
		<!-- *************************************************** -->
		<!-- Write ClientTradeReference -->
		<xsl:variable name="ClientTradeReference" select="translate(Label,',','')"/>
		<xsl:value-of select="concat($ClientTradeReference,$comma)"/>
		<!-- *************************************************** -->
		<!-- Account -->
		<xsl:variable name="Account" select="translate(Cells/Cell[1]/FormattedData,',','')"/>
		<xsl:value-of select="concat($Account,$comma)"/>
		<!-- *************************************************** -->
		<!-- Broker -->
		<xsl:variable name="Broker" select="translate(Cells/Cell[2]/FormattedData,',','')"/>
		<xsl:value-of select="concat($Broker,$comma)"/>
		<!-- *************************************************** -->
		<!-- TransactionStatus -->
		<!-- Notes: Remove commas -->
		<xsl:variable name="TransactionStatus" select="translate(Cells/Cell[17]/FormattedData,',','')"/>
		<xsl:value-of select="concat($TransactionStatus,$comma)"/>
		<!-- *************************************************** -->
		<!-- Instrument Identifier & Instrument Name -->
		<!-- Notes: If ISIN empty, use instrument name -->
		<xsl:variable name="InstrumentName">
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="translate(Cells/Cell[3]/FormattedData,',','')"/>
				<xsl:with-param name="replace" select="'ZAR/'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="Identifier" select="translate(Cells/Cell[4]/FormattedData,',','')"/>
		<xsl:choose>
			<xsl:when test="$Identifier=''">
				<xsl:value-of select="concat($InstrumentName,$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat($Identifier,$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- Description -->
		<!-- Notes: Use instrument name -->
		<xsl:value-of select="concat($InstrumentName,$comma)"/>
		<!-- *************************************************** -->
		<!-- LongDescription -->
		<!-- Notes: Use instrument name -->
		<xsl:value-of select="concat($InstrumentName,$comma)"/>
		<!-- *************************************************** -->
		<!-- InstrumentClass -->
		<!-- Notes: Remove commas -->
		<xsl:variable name="InstrumentClass" select="translate(Cells/Cell[5]/FormattedData,',','')"/>
		<xsl:value-of select="concat($InstrumentClass,$comma)"/>
		<!-- *************************************************** -->
		<!-- BuySell -->
		<!-- Notes: Only use first letter B or S -->
		<xsl:variable name="BuySell" select="substring(Cells/Cell[7]/FormattedData,1,1)"/>
		<xsl:value-of select="concat($BuySell,$comma)"/>
		<!-- *************************************************** -->
		<!-- TradeDate -->
		<!-- Notes: Remove commas and format dd/mm/yyyy -->
		<xsl:variable name="TradeDate">
			<xsl:choose>
				<xsl:when test="Cells/Cell[8]/FormattedData=''">
					<xsl:value-of select="$emptyString"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="formatDate">
						<xsl:with-param name="dateTime" select="translate(Cells/Cell[8]/FormattedData,',','')" />
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:value-of select="concat($TradeDate,$comma)"/>
		<!-- *************************************************** -->
		<!-- SettlementDate -->
		<!-- Notes: Remove commas and format dd/mm/yyyy -->
		<xsl:variable name="SettlementDate">
			<xsl:choose>
				<xsl:when test="Cells/Cell[9]/FormattedData=''">
					<xsl:value-of select="$emptyString"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="formatDate">
						<xsl:with-param name="dateTime" select="translate(Cells/Cell[9]/FormattedData,',','')" />
					</xsl:call-template>
				</xsl:otherwise>
				</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="concat($SettlementDate,$comma)"/>
		<!-- *************************************************** -->
		<!-- Quantity -->
		<!-- Notes: Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="Quantity" select="number(translate(Cells/Cell[10]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($Quantity)='NaN' or string($Quantity)=''">
				<xsl:value-of select="concat(0,$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat($Quantity,$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- Price -->
		<!-- Notes: Remove commas, if bond, use clean price, 0 if NaN or empty string -->
		<xsl:variable name="Price" select="number(translate(Cells/Cell[11]/FormattedData,',',''))"/>
		<xsl:variable name="CleanPrice" select="number(translate(Cells/Cell[23]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="$InstrumentClass='Bond'">
				<xsl:choose>
					<xsl:when test="string($CleanPrice)='NaN' or string($CleanPrice)=''">
						<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="concat(format-number($CleanPrice,$pricefmt),$comma)"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="string($Price)='NaN' or string($Price)=''">
						<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="concat(format-number($Price,$pricefmt),$comma)"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- AllInPrice -->
		<!-- Notes: Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="AllInPrice" select="number(translate(Cells/Cell[24]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($AllInPrice)='NaN' or string($AllInPrice)=''">
				<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat(format-number($AllInPrice,$pricefmt),$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- SettlementAmount  -->
		<!-- Notes: Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="SettlementAmount" select="number(translate(Cells/Cell[46]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($SettlementAmount)='NaN' or string($SettlementAmount)=''">
				<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat(format-number($SettlementAmount,$pricefmt),$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- Commission   -->
		<!-- Notes: Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="Commission" select="number(translate(Cells/Cell[13]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($Commission)='NaN' or string($Commission)=''">
				<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat(format-number($Commission,$pricefmt),$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- TaxFees    -->
		<!-- Notes: Add VAT and STT, Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="VAT" select="number(translate(Cells/Cell[12]/FormattedData,',',''))"/>
                                <xsl:variable name="STT" select="number(translate(Cells/Cell[15]/FormattedData,',',''))"/>

		<xsl:variable name="TaxFees" />
		<xsl:choose>
                                        <xsl:when test="string($VAT)='NaN' or string($VAT)=''">
                                                <xsl:choose>
                                                        <xsl:when test="string($STT)='NaN' or string($STT)=''">
                                                                        <xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
				<xsl:value-of select="concat(format-number($STT,$pricefmt),$comma)"/>
                                                        </xsl:otherwise>
                                                </xsl:choose>
                                        </xsl:when>
                                        <xsl:otherwise>
                                                <xsl:choose>
                                                        <xsl:when test="string($STT)='NaN' or string($STT)=''">
                                                                        <xsl:value-of select="concat(format-number($VAT,$pricefmt),$comma)"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
				<xsl:value-of select="concat(format-number($VAT+$STT,$pricefmt),$comma)"/>
                                                        </xsl:otherwise>
                                                </xsl:choose>
                                        </xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- Interest    -->
		<!-- Notes: Remove commas, 0 if NaN or empty string -->
		<xsl:variable name="Interest" select="number(translate(Cells/Cell[25]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($Interest)='NaN' or string($Interest)=''">
				<xsl:value-of select="concat(format-number(0,$pricefmt),$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat(format-number($Interest,$pricefmt),$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- Repo    -->
		<!-- If BSB or Repo/Reverse, then Repo else  -->
		<xsl:variable name="UnderlyingInstrumentClass" select="translate(Cells/Cell[40]/FormattedData,',','')"/>
		<xsl:choose>
			<xsl:when test="$InstrumentClass='Bond'">
				<xsl:value-of select="concat('Outright',$comma)"/>
			</xsl:when>
			<xsl:when test="($InstrumentClass='BuySellback' or $InstrumentClass='Repo/Reverse') and $UnderlyingInstrumentClass='Bond'">
				<xsl:value-of select="concat('Repo',$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat('NA',$comma)"/>
			</xsl:otherwise>
		</xsl:choose>

		<!-- *************************************************** -->
		<!-- Currency  -->
		<!-- Notes: Remove commas-->
		<xsl:variable name="Currency" select="translate(Cells/Cell[6]/FormattedData,',','')"/>
		<xsl:value-of select="concat($Currency,$comma)"/>
		<!-- *************************************************** -->
		<!-- Exchange  -->
		<!-- Notes: Remove commas, if acquirer is PRIME SERVICES DESK, use Counterparty, else Other-->
		<xsl:variable name="Exchange" select="translate(Cells/Cell[22]/FormattedData,',','')"/>
		<xsl:variable name="Acquirer" select="translate(Cells/Cell[39]/FormattedData,',','')"/>
		<xsl:choose>
			<xsl:when test="$Exchange='JSE' or $Exchange='SAFEX' or $Exchange='JSE SECURITIES EXCHANGE SOUTH AFRICA' or $Exchange='JSE CLEAR'">
				<xsl:value-of select="concat($Exchange,$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat('NA',$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- OriginalRefNumber  -->
		<xsl:variable name="OriginalRefNumber" select="translate(Cells/Cell[19]/FormattedData,',','')"/>
		<xsl:choose>
			<xsl:when test="not($OriginalRefNumber) or $OriginalRefNumber=''">
				<xsl:value-of select="concat(0,$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat($OriginalRefNumber,$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- *************************************************** -->
		<!-- FixedRate -->
		<xsl:variable name="FixedRate" select="translate(Cells/Cell[27]/FormattedData,',','')"/>
		<xsl:value-of select="concat($FixedRate,$comma)"/>
		<!-- *************************************************** -->
		<!-- FullyFunded -->
		<xsl:variable name="FullyFunded" select="translate(Cells/Cell[48]/FormattedData,',','')"/>
		<xsl:value-of select="$FullyFunded"/>
		<!-- *************************************************** -->

		<!-- Break Line -->
		<xsl:value-of select="$eoln"/>
	</xsl:template>
	<!-- Template for writing out the header row -->
	<xsl:template name="WriteHeader">
		<!-- ClientTradeReference -->
		<xsl:value-of select="concat('ClientTradeReference',$comma)"/>
		<!-- Account -->
		<xsl:value-of select="concat('Account',$comma)"/>
		<!-- Broker -->
		<xsl:value-of select="concat('Broker',$comma)"/>
		<!-- TransactionStatus -->
		<xsl:value-of select="concat('TransactionStatus',$comma)"/>
		<!-- Identifier -->
		<xsl:value-of select="concat('Identifier',$comma)"/>
		<!-- Description -->
		<xsl:value-of select="concat('Description',$comma)"/>
		<!-- LongDescription -->
		<xsl:value-of select="concat('LongDescription',$comma)"/>
		<!-- InstrumentClass -->
		<xsl:value-of select="concat('InstrumentClass',$comma)"/>
		<!-- BuySell -->
		<xsl:value-of select="concat('BuySell',$comma)"/>
		<!-- TradeDate -->
		<xsl:value-of select="concat('TradeDate',$comma)"/>
		<!-- SettlementDate -->
		<xsl:value-of select="concat('SettlementDate',$comma)"/>
		<!-- Quantity -->
		<xsl:value-of select="concat('Quantity',$comma)"/>
		<!-- Price -->
		<xsl:value-of select="concat('Price',$comma)"/>
		<!-- AllInPrice -->
		<xsl:value-of select="concat('AllInPrice',$comma)"/>
		<!-- SettlementAmount  -->
		<xsl:value-of select="concat('SettlementAmount',$comma)"/>
		<!-- Commission   -->
		<xsl:value-of select="concat('Commission',$comma)"/>
		<!-- TaxFees    -->
		<xsl:value-of select="concat('TaxFees',$comma)"/>
		<!-- Interest     -->
		<xsl:value-of select="concat('Interest',$comma)"/>
		<!-- Repo      -->
		<xsl:value-of select="concat('Repo',$comma)"/>
		<!-- Currency  -->
		<xsl:value-of select="concat('Currency',$comma)"/>
		<!-- Exchange  -->
		<xsl:value-of select="concat('Exchange',$comma)"/>
		<!-- OriginalRefNumber  -->
		<xsl:value-of select="concat('OriginalRefNumber',$comma)"/>
                                <!-- FixedRate  -->
		<xsl:value-of select="concat('FixedRate',$comma)"/>
                                <!-- FullyFunded  -->
		<xsl:value-of select="'FullyFunded'"/>
		<!-- Break Line -->
		<xsl:value-of select="$eoln"/>
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
	<!-- Template for formatting dates -->
	<xsl:template name="formatDate">
		<xsl:param name="dateTime"/>
		<xsl:variable name="date" select="substring($dateTime,1,10)" />
		<xsl:variable name="year" select="substring($date,1,4)"/>
		<xsl:variable name="month" select="substring($date,6,2)"/>
		<xsl:variable name="day" select="substring($date,9,2)"/>
		<xsl:value-of select="concat($day, '/', $month, '/', $year)"/>
	</xsl:template>
</xsl:stylesheet>



