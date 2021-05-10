<!-- 
<?xml version="1.0" encoding="utf-8"?>
Special XML to XML Spreadsheet template created for a custom Risk Matrix View report 
AUTHOR: Conicov Andrei
DATE: 19.07.2013
-->
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:x="urn:schemas-microsoft-com:office:excel"
	xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
	xmlns:html="http://www.w3.org/TR/REC-html40">

	<xsl:template match="/">

		<Workbook
			xmlns="urn:schemas-microsoft-com:office:spreadsheet"
			xmlns:o="urn:schemas-microsoft-com:office:office"
			xmlns:x="urn:schemas-microsoft-com:office:excel"
			xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
			xmlns:html="http://www.w3.org/TR/REC-html40">
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
					<Borders />
					<Font ss:FontName="Arial" ss:size="10" />
					<Interior />
					<NumberFormat />
					<Protection />
				</Style>
				<Style ss:ID="NormalBold" ss:Parent="Default">
					<Font ss:FontName="Arial" ss:size="11" ss:Bold="1"/>
					<Alignment ss:Horizontal="Center" ss:Vertical="Top"/>
				</Style>
				<Style ss:ID="signNumber" ss:Parent="Default">
					<NumberFormat ss:Format="[Blue]#,##0,\ &quot;k&quot;;[Red]\-#,##0,\ &quot;k&quot;"/>
				</Style>
				<Style ss:ID="signPercent" ss:Parent="Default">
					<NumberFormat ss:Format="[Blue]#,##0.00%;[Red]\-#,##0.00%"/>
				</Style>
				<Style ss:ID="groupHeader" ss:Parent="NormalBold"/>
				<Style ss:ID="columnHeader" ss:Parent="NormalBold"/>
				<Style ss:ID="titleHeader" ss:Parent="NormalBold"/>
				<Style ss:ID="styleRef" ss:Parent="NormalBold">
					<Font ss:FontName="Arial" ss:size="1" ss:Bold="1"/>
				</Style>
				<Style ss:ID="styleGray" ss:Parent="Default">
					<Interior ss:Color="#FFFF00" ss:Pattern="Solid"/>
				</Style>
				<Style ss:ID="styleYellow" ss:Parent="Default">
					<Interior ss:Color="#A5A5A5" ss:Pattern="Solid"/>
				</Style>
				<Style ss:ID="titleRowHeader" ss:Parent="NormalBold">
					<Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:Rotate="90"/>
				</Style>
			</Styles>
			<Worksheet ss:Name="SheetName">
				<Table>
					<xsl:for-each select="/Report/row">
						<Row>
							<xsl:attribute name="ss:Index">
								<xsl:value-of select="@index" />
							</xsl:attribute>
							
							<xsl:for-each select="cell">
								<Cell>
									<xsl:attribute name="ss:Index">
										<xsl:value-of select="@index" />
									</xsl:attribute>
									<xsl:choose>
										<xsl:when test="@style != 'None'">
											<xsl:attribute name="ss:StyleID">
												<xsl:value-of select="@style" />
											</xsl:attribute>
										</xsl:when>
									</xsl:choose>
									<xsl:choose>
										<xsl:when test="@xLength > 1">
											<xsl:attribute name="ss:MergeAcross">
												<xsl:value-of select="@xLength" />
											</xsl:attribute>
										</xsl:when>
									</xsl:choose>
									<xsl:choose>
										<xsl:when test="@yLength > 1">
											<xsl:attribute name="ss:MergeDown">
												<xsl:value-of select="@yLength" />
											</xsl:attribute>
										</xsl:when>
									</xsl:choose>
									<xsl:choose>
										<xsl:when test="@isFormula = 'True'">
											<xsl:attribute name="ss:Formula">
												<xsl:value-of select="." />
											</xsl:attribute>
											<Data>
												<xsl:attribute name="ss:Type">
													<xsl:value-of select="@valueType" />
												</xsl:attribute>
											</Data>
										</xsl:when>
										<xsl:otherwise>
											<Data>
												<xsl:attribute name="ss:Type">
													<xsl:value-of select="@valueType" />
												</xsl:attribute>
												<xsl:value-of select="."/>
											</Data>
										</xsl:otherwise>
									</xsl:choose>
								</Cell>
							</xsl:for-each>
						</Row>
					</xsl:for-each>
				</Table>
			</Worksheet>
		</Workbook>

	</xsl:template>
</xsl:stylesheet>
