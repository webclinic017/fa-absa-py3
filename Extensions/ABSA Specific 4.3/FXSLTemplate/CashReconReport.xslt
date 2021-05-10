<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:x="urn:schemas-microsoft-com:office:excel"
	xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:html="http://www.w3.org/TR/REC-html40" >

	<xsl:template match="/">

<Workbook
	xmlns="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:x="urn:schemas-microsoft-com:office:excel"
	xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:html="http://www.w3.org/TR/REC-html40" >
	<DocumentProperties xmlns="urn:schemas-microsoft-com:office:office">
		<Author></Author>
		<LastAuthor></LastAuthor>
		<Created></Created>
		<Company>Absa</Company>
		<Version>1.0000</Version>
	</DocumentProperties>
	<Styles>
		<Style ss:ID="Default" ss:Name="Normal">
			<Alignment ss:Vertical="Top" />
			<Borders>
				<Border ss:Position="Left" ss:LineStyle="None" />
				<Border ss:Position="Bottom" ss:LineStyle="None" />
				<Border ss:Position="Top" ss:LineStyle="None" />
				<Border ss:Position="Right" ss:LineStyle="None" />
			</Borders>
			<Font ss:FontName="Arial" ss:size="10" />
			<Interior ss:Color="#FFFFFF" ss:Pattern="Solid" />
			<NumberFormat />
			<Protection />
		</Style>
		<Style ss:ID="value_general" ss:Name="Value - general">
			<Font ss:FontName="Arial" ss:Size="10" />
			<Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="not_a_number" ss:Name="Not a Number">
			<Alignment ss:Horizontal="Right" />
			<Font ss:FontName="Arial" ss:Size="10" />
			<Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="numeric_value_general" ss:Name="Numeric value general">
			<Font ss:FontName="Arial" ss:Size="10" />
			<Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
		<Style ss:ID="numeric_value_gray" ss:Name="Numeric value gray">
			<Font ss:FontName="Arial" ss:Size="10" />
			<Interior ss:Color="#F2F2F2" ss:Pattern="Solid" />
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
		<Style ss:ID="numeric_value_left" ss:Name="Numeric value left">
			<Alignment ss:Horizontal="Left" />
			<Font ss:FontName="Arial" ss:Size="10" />
			<Interior ss:Color="#EAF1DD" ss:Pattern="Solid" />
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
		<Style ss:ID="report_title" ss:Name="Report title">
			<Font ss:FontName="Arial" ss:Size="14" ss:Bold="1" />
			<Interior ss:Color="#FFFFFF" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="columns_legend" ss:Name="Columns legend">
			<Alignment ss:Horizontal="Right" ss:WrapText="1" />
			<Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
			<Interior ss:Color="#CCCCCC" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="client_title" ss:Name="Client title">
			<Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
			<Interior ss:Color="#C2D69A" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="client_header" ss:Name="Client title number">
			<Alignment ss:Horizontal="Right" ss:WrapText="1" />
			<Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
			<Interior ss:Color="#C2D69A" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="position_title" ss:Name="Position title">
			<Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
			<Interior ss:Color="#D7E4BC" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="position_title_status" ss:Name="Position title status">
			<Alignment ss:Horizontal="Right" />
			<Font ss:FontName="Arial" ss:Size="10" ss:Bold="1" />
			<Interior ss:Color="#D7E4BC" ss:Pattern="Solid" />
		</Style>
		<Style ss:ID="status_ok" ss:Name="Status Ok">
			<Alignment ss:Horizontal="Right" />
			<Font ss:FontName="Arial" ss:Size="10"  />
			<Interior ss:Color="#EAF1DD" ss:Pattern="Solid"/>
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
		<Style ss:ID="status_break" ss:Name="Status Break">
			<Alignment ss:Horizontal="Right" />
			<Font ss:FontName="Arial" ss:Size="10" ss:Color="#FFFFFF"/>
			<Interior ss:Color="#C00000" ss:Pattern="Solid" />
			<NumberFormat ss:Format="#,###,###,###,###,##0.00" />
		</Style>
	</Styles>
	<Worksheet ss:Name="Detailed Recon">
		<xsl:call-template name="GenerateOverview">
			<xsl:with-param name="HideNoBreakInstruments" select="0" />
		</xsl:call-template>
	</Worksheet>
	<Worksheet ss:Name="Break Summary">
		<xsl:call-template name="GenerateOverview">
			<xsl:with-param name="HideNoBreakInstruments" select="1" />
		</xsl:call-template>
	</Worksheet>
	<xsl:if test="not(/report/@lookup)">
	<Worksheet ss:Name="Settlement Control">
		<xsl:call-template name="SettlementsView">
			<xsl:with-param name="HideNoBreakInstruments" select="0" />
		</xsl:call-template>
	</Worksheet>
	<Worksheet ss:Name="SC Break Summary">
		<xsl:call-template name="SettlementsView">
			<xsl:with-param name="HideNoBreakInstruments" select="1" />
		</xsl:call-template>
	</Worksheet>
	</xsl:if>
</Workbook>

	</xsl:template>

	<xsl:template name="GenerateOverview">
		<xsl:param name="HideNoBreakInstruments" />
		<Table>
			<Column ss:Index="1" ss:Width="120"/>
			<Column ss:Index="2" ss:Width="80"/>
			<Column ss:Index="3" ss:Width="80"/>
			<Column ss:Index="4" ss:Width="80"/>
			<Column ss:Index="5" ss:Width="80"/>
			<Column ss:Index="6" ss:Width="80"/>
			<Column ss:Index="7" ss:Width="90"/>
			<Column ss:Index="8" ss:Width="100"/>
			<Row ss:Index="2">
				<Cell ss:MergeAcross="6" ss:StyleID="report_title">
					<Data ss:Type="String">Cash Recon: Call Account vs. <xsl:value-of select="/report/@type" /> TPL</Data>
				</Cell>
			</Row>
			<Row>
			</Row>
			<Row>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String"/>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Inception TPL</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Inception TPL</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Inception TPL</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Call Account</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Call Account</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Break Amount</Data>
				</Cell>
				<Cell ss:StyleID="columns_legend">
					<Data ss:Type="String">Break Status</Data>
				</Cell>
			</Row>
			<xsl:for-each select="/report/client">
				<xsl:choose>
					<xsl:when test="@status = 'OK' and $HideNoBreakInstruments = 1">
					</xsl:when>
					<xsl:otherwise>
						<Row/>
						<Row/>
						<Row>
							<Cell ss:StyleID="client_title">
								<Data ss:Type="String"><xsl:value-of select="@name"/></Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String"><xsl:value-of select="@start_date"/></Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String"><xsl:value-of select="@end_date"/></Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String">Change</Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String">Cash</Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String">Back Dated</Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String">Diff (Inception)</Data>
							</Cell>
							<Cell ss:StyleID="client_header">
								<Data ss:Type="String">Status (Inception)</Data>
							</Cell>
						</Row>
							<xsl:for-each select="position">
							<Row>
								<Cell ss:StyleID="position_title" ss:MergeAcross="6">
									<Data ss:Type="String"><xsl:value-of select="@type"/></Data>
								</Cell>
								<Cell ss:StyleID="position_title_status">
									<Data ss:Type="String"><xsl:value-of select="@status"/></Data>
								</Cell>
							</Row>
								<xsl:for-each select="instrument">
									<xsl:choose>
										<xsl:when test="@status != 'Break' and $HideNoBreakInstruments = 1">
										</xsl:when>
										<xsl:otherwise>
											<Row>
												<Cell ss:StyleID="value_general">
													<Data ss:Type="String"><xsl:value-of select="@type"/></Data>
												</Cell>
												<xsl:element name="Cell">
													<xsl:choose>
														<xsl:when test="@start_val != 'nan'">
															<xsl:attribute name="ss:StyleID">numeric_value_general</xsl:attribute>
															<Data ss:Type="Number"><xsl:value-of select="@start_val" /></Data>
														</xsl:when>
														<xsl:otherwise>
															<xsl:attribute name="ss:StyleID">not_a_number</xsl:attribute>
															<Data ss:Type="String"><xsl:value-of select="@start_val" /></Data>
														</xsl:otherwise>
													</xsl:choose>
												</xsl:element>
												<xsl:element name="Cell">
													<xsl:choose>
														<xsl:when test="@end_val != 'nan'">
															<xsl:attribute name="ss:StyleID">numeric_value_general</xsl:attribute>
															<Data ss:Type="Number"><xsl:value-of select="@end_val" /></Data>
														</xsl:when>
														<xsl:otherwise>
															<xsl:attribute name="ss:StyleID">not_a_number</xsl:attribute>
															<Data ss:Type="String"><xsl:value-of select="@end_val" /></Data>
														</xsl:otherwise>
													</xsl:choose>
												</xsl:element>
												<xsl:element name="Cell">
													<xsl:choose>
														<xsl:when test="@change != 'nan'">
															<xsl:attribute name="ss:StyleID">numeric_value_general</xsl:attribute>
															<Data ss:Type="Number"><xsl:value-of select="@change" /></Data>
														</xsl:when>
														<xsl:otherwise>
															<xsl:attribute name="ss:StyleID">not_a_number</xsl:attribute>
															<Data ss:Type="String"><xsl:value-of select="@change" /></Data>
														</xsl:otherwise>
													</xsl:choose>
												</xsl:element>
												<Cell ss:StyleID="numeric_value_general">
													<Data ss:Type="Number"><xsl:value-of select="@cash"/></Data>
												</Cell>
												<Cell ss:StyleID="numeric_value_general">
													<Data ss:Type="Number"><xsl:value-of select="@backdated"/></Data>
												</Cell>
												<xsl:element name="Cell">
													<xsl:choose>
														<xsl:when test="@diff != 'nan'">
															<xsl:attribute name="ss:StyleID">numeric_value_general</xsl:attribute>
															<Data ss:Type="Number"><xsl:value-of select="@diff" /></Data>
														</xsl:when>
														<xsl:otherwise>
															<xsl:attribute name="ss:StyleID">not_a_number</xsl:attribute>
															<Data ss:Type="String"><xsl:value-of select="@diff" /></Data>
														</xsl:otherwise>
													</xsl:choose>
												</xsl:element>
												<xsl:element name="Cell">
													<xsl:choose>
														<xsl:when test="@status != 'Break'">
															<xsl:attribute name="ss:StyleID">status_ok</xsl:attribute>
														</xsl:when>
														<xsl:otherwise>
															<xsl:attribute name="ss:StyleID">status_break</xsl:attribute>
														</xsl:otherwise>
													</xsl:choose>
													<Data ss:Type="String"><xsl:value-of select="@status"/></Data>
												</xsl:element>
											</Row>
										</xsl:otherwise>
									</xsl:choose>
								</xsl:for-each>
							</xsl:for-each>
						</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
		</Table>
	</xsl:template>
	<!--Settlements tab template-->
	<xsl:template name="SettlementsView">
		<xsl:param name="HideNoBreakInstruments" />
		<Table>
			<Column ss:Index="1" ss:Width="120"/>
			<Column ss:Index="2" ss:Width="75"/>
			<Column ss:Index="3" ss:Width="75"/>
			<Column ss:Index="4" ss:Width="75"/>
			<Column ss:Index="5" ss:Width="75"/>
			<Column ss:Index="6" ss:Width="75"/>
			<Column ss:Index="7" ss:Width="75"/>
			<Column ss:Index="8" ss:Width="75"/>
			<Column ss:Index="9" ss:Width="75"/>
			<Column ss:Index="10" ss:Width="75"/>
			<Column ss:Index="11" ss:Width="75"/>
			<Column ss:Index="12" ss:Width="75"/>
			<Column ss:Index="13" ss:Width="75"/>
			<Column ss:Index="14" ss:Width="75"/>
			<Column ss:Index="15" ss:Width="75"/>
			<Column ss:Index="16" ss:Width="75"/>
			<Column ss:Index="17" ss:Width="75"/>
			<Row ss:Index="2">
				<Cell ss:MergeAcross="6" ss:StyleID="report_title">
					<Data ss:Type="String">Cash Recon: Call Account vs. <xsl:value-of select="/report/@type" /> TPL</Data>
				</Cell>
			</Row>
			<xsl:for-each select="/report/client">
				<xsl:choose>
					<xsl:when test="not(.//value[@style='status_break']) and $HideNoBreakInstruments = 1">
					</xsl:when>
				<xsl:otherwise>
				<Row/>
				<Row/>
				<Row>
					<Cell ss:StyleID="client_title" ss:MergeAcross="15">
						<Data ss:Type="String"><xsl:value-of select="@name"/></Data>
					</Cell>
					<Cell ss:StyleID="client_title">
						<Data ss:Type="String"><xsl:value-of select="@sc_status"/></Data>
					</Cell>
				</Row>
				<xsl:for-each select="settlement">
				<Row>
					<Cell ss:StyleID="value_general">
						<Data ss:Type="String"><xsl:value-of select="@header"/></Data>
					</Cell>
					<Cell ss:StyleID="numeric_value_left">
						<Data ss:Type="Number"><xsl:value-of select="value"/></Data>
					</Cell>
					<Cell ss:StyleID="value_general">
						<Data ss:Type="String">Backdated</Data>
					</Cell>
					<Cell ss:StyleID="numeric_value_left" ss:MergeAcross="13">
						<Data ss:Type="Number"><xsl:value-of select="backdated"/></Data>
					</Cell>
				</Row>
				</xsl:for-each>
				<Row>
					<xsl:for-each select="(position/sinstrument[1])[1]/value">
					<Cell ss:StyleID="client_header">
						<Data ss:Type="String"><xsl:value-of select="@header"/></Data>
					</Cell>
					</xsl:for-each>
				</Row>
				<Row>
					<xsl:for-each select="(position/sinstrument[1])[1]/value">
					<Cell ss:StyleID="client_header">
						<Data ss:Type="String"><xsl:value-of select="@header2"/></Data>
					</Cell>
					</xsl:for-each>
				</Row>
				<xsl:for-each select="position">
				<Row>
					<Cell ss:StyleID="position_title" ss:MergeAcross="16">
						<Data ss:Type="String"><xsl:value-of select="@type"/></Data>
					</Cell>
				</Row>
				<xsl:for-each select="sinstrument">
					<xsl:choose>
						<xsl:when test="not(value[@style='status_break']) and $HideNoBreakInstruments = 1">
						</xsl:when>
					<xsl:otherwise>
						<Row>
							<xsl:for-each select="value">
							<Cell ss:StyleID="{@style}">
								<Data ss:Type="{@type}"><xsl:value-of select="."/></Data>
							</Cell>
							</xsl:for-each>
						</Row>
					</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
				</xsl:for-each>
				</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
		</Table>
	</xsl:template>
</xsl:stylesheet>
