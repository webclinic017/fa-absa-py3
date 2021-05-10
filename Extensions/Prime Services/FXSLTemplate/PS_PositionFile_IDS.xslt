#grouping: aef reporting/print templates
#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates csv
#grouping: aef reporting/style sheets

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
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
		<!-- Apply the table template -->
		<xsl:apply-templates select="ReportContents/Table"/>
	</xsl:template>

	<!-- Template for processing the report table -->
	<xsl:template match="Table">
		<!-- Write the header row -->
		<xsl:call-template name="WriteHeader"/>

		<!-- Now call the grouping rows -->
		<xsl:apply-templates select="Rows/Row/Rows/Row" mode="Grouping"/>
	</xsl:template>

	<xsl:template match="Row" mode="Grouping">
		<!-- Now call the detail rows -->
		<xsl:apply-templates select="Rows/Row" mode="Detail"/>
	</xsl:template>

	<xsl:template match="Row" mode="Detail">
		<!-- Portfolio -->
		<xsl:variable name="Portfolio" select="../../Label"/>
		<xsl:value-of select="concat(translate($Portfolio,',',''),$comma)"/>
		<!-- Instrument Type -->
		<xsl:variable name="InstrumentType" select="Cells/Cell[3]/FormattedData"/>
		<xsl:value-of select="concat(translate($InstrumentType,',',''),$comma)"/>
		<!-- Instrument Identifier -->
		<xsl:variable name="Identifier" select="Cells/Cell[1]/FormattedData" />
		<xsl:value-of select="concat(translate($Identifier,',',''),$comma)"/>
		<!-- Instrument Name -->
		<xsl:variable name="InstrumentName" >
			<xsl:call-template name="string-replace-all">
				<xsl:with-param name="text" select="Instrument"/>
				<xsl:with-param name="replace" select="'ZAR/'"/>
				<xsl:with-param name="by" select="$emptyString"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:value-of select="concat(translate($InstrumentName,',',''),$comma)"/>
		<!-- Quantity -->
		<xsl:variable name="Quantity" select="number(translate(Cells/Cell[7]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($Quantity)='NaN'">
				<xsl:value-of select="concat(0,$comma)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="concat(format-number($Quantity, $qtyfmt),$comma)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- Closing Price -->
		<xsl:variable name="ClosingPrice" select="number(translate(Cells/Cell[8]/FormattedData,',',''))"/>
		<xsl:choose>
			<xsl:when test="string($ClosingPrice)='NaN' or string($ClosingPrice)=''">
				<xsl:value-of select="0"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="format-number($ClosingPrice,$pricefmt)"/>
			</xsl:otherwise>
		</xsl:choose>
		<!-- Break Line -->
		<xsl:value-of select="$eoln"/>
	</xsl:template>

	<!-- Template for writing out the header row -->
	<xsl:template name="WriteHeader">
		<!-- Portfolio -->
		<xsl:value-of select="concat('Portfolio',$comma)"/>
		<!-- Instrument Type -->
		<xsl:value-of select="concat('InstrumentType',$comma)"/>
		<!-- Identifier -->
		<xsl:value-of select="concat('Identifier',$comma)"/>
		<!-- Long Descritpion -->
		<xsl:value-of select="concat('LongDescription',$comma)"/>
		<!-- Quantity -->
		<xsl:value-of select="concat('Quantity',$comma)"/>
		<!-- ClosingPrice -->
		<xsl:value-of select="'ClosingPrice'"/>
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

</xsl:stylesheet>
