#grouping: aef reporting/print templates

<?xml version='1.0'?>
<!-- &copy; Copyright 2011 SunGard FRONT ARENA
       FStandardTemplate is able to produce colored output for RiskMatrixSheets when DefaultData is turned on
       Added support for Transhist output
-->
<!DOCTYPE xsl:stylesheet [
  <!ENTITY nbsp "<xsl:text>&#160;</xsl:text>">
]>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html"/>
  <xsl:variable name="useLabelColumn" select="//PRIMEReport/Type !='ASQL Table'"/>
  <xsl:variable name="maxNrOfCols" select="15"/>
  
  <xsl:template match="ReportContents">
    <xsl:apply-templates select="Table"/>
  </xsl:template>


  <xsl:template name="ColumnGroupLabels">
    <xsl:param name = "columnSpan"/>
    <xsl:param name = "columnIndex"/>
    
    <xsl:choose>
      <xsl:when test="count(Columns/Column) + 1 > $columnIndex and $columnIndex &lt;= $maxNrOfCols">
        <xsl:choose>
          <xsl:when test="Columns/Column[$columnIndex]/GroupLabel = Columns/Column[($columnIndex)-1]/GroupLabel ">
            <xsl:call-template name="ColumnGroupLabels">
              <xsl:with-param name="columnSpan" select="$columnSpan + 1"/>
              <xsl:with-param name="columnIndex" select="$columnIndex + 1"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <td colspan="{$columnSpan}">
              <xsl:value-of select="Columns/Column[($columnIndex)-1]/GroupLabel"/>
            </td>
            <xsl:call-template name="ColumnGroupLabels">
              <xsl:with-param name="columnSpan" select="1"/>
              <xsl:with-param name="columnIndex" select="$columnIndex + 1"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <td colspan="{$columnSpan}">
          <xsl:value-of select="Columns/Column[($columnIndex)-1]/GroupLabel"/>
        </td>
      </xsl:otherwise>  
    </xsl:choose> 

  </xsl:template>

  <xsl:template name="ColumnLabels">
    
      <xsl:if test="$useLabelColumn">
        <th/>
      </xsl:if>

      <xsl:for-each select="Columns/Column">
        <xsl:if test="position() &lt;= $maxNrOfCols">
          <xsl:choose>
            <xsl:when test="TemplateId != ''">
              <td>
                <xsl:value-of select="TemplateId"/>
                <br />
                <xsl:value-of select="Label"/>
              </td>
            </xsl:when>
            <xsl:otherwise>
              <td>
                <xsl:value-of select="Label"/>
              </td>
            </xsl:otherwise>
          </xsl:choose>
         </xsl:if>
      </xsl:for-each>
   
  </xsl:template>


  <xsl:template name="ColumnHeaders">
    <thead>
    <tr class="groupLabelRow">
      <th/>
      <xsl:call-template name="ColumnGroupLabels">
        <xsl:with-param name="columnIndex" select="2"/>
        <xsl:with-param name="columnSpan" select="1"/>
      </xsl:call-template>
    </tr>
    <tr class="columnLabelRow">
      <xsl:call-template name="ColumnLabels"/>
    </tr>
   </thead>
  </xsl:template>

  <xsl:template match="breakPage">
  </xsl:template>

  <xsl:template match="Table">
    <xsl:variable name="numberOfColumns" select="NumberOfColumns"/>

    <table class="reportTable">
      <xsl:call-template name="ColumnHeaders"/>
      <xsl:apply-templates select="Rows/Row">
        <xsl:with-param name="treeDepth" select="1"/>
      </xsl:apply-templates>
    </table>
    <p/>
    <p/>
  </xsl:template>

  <xsl:template name="RowHeader">
    <xsl:param name = "treeDepth"/>
    <xsl:param name = "type"/>
    <xsl:if test="$useLabelColumn">
      <td class="{concat($type, 'RowHeader', $treeDepth)}">
        <xsl:choose>
          <xsl:when test="$type = 'aggregated'">
            <xsl:value-of select="concat('Total ', Label)"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="Label"/>
          </xsl:otherwise>
        </xsl:choose>
      </td>
    </xsl:if>
  </xsl:template>

  <xsl:template name="Cells">
    <xsl:param name = "treeDepth"/>
    <xsl:param name = "colorStep"/>

    <tr class="{concat('leafRow', $treeDepth)}" depth="{$treeDepth}">
      
      <xsl:call-template name="RowHeader">
        <xsl:with-param name="treeDepth" select="$treeDepth" />
        <xsl:with-param name="type" select="'leaf'" />
      </xsl:call-template>
      <xsl:apply-templates select="Cells/Cell"/>
    </tr>
  </xsl:template>

  <xsl:template match="Cell" mode="empty">
    <xsl:if test="position() &lt;= $maxNrOfCols">
      <th/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="ParentRow">
    <xsl:param name = "treeDepth"/>
    <xsl:param name = "colorStep"/>
    <tr class="{concat('parentRow', $treeDepth)}" depth="{$treeDepth}">
      <xsl:call-template name="RowHeader">
        <xsl:with-param name="treeDepth" select="$treeDepth" />
        <xsl:with-param name="type" select="'parent'" />
      </xsl:call-template>
      <xsl:apply-templates select="Cells/Cell" mode="empty"/>
    </tr>
  </xsl:template>

  <xsl:template name="AggregatedRow">
    <xsl:param name = "treeDepth"/>
    <tr class="{concat('aggregatedRow', $treeDepth)}" depth="{$treeDepth}">
      <xsl:call-template name="RowHeader">
        <xsl:with-param name="treeDepth" select="$treeDepth" />
        <xsl:with-param name="type" select="'aggregated'" />
      </xsl:call-template>
      <xsl:apply-templates select="Cells/Cell">
        <xsl:with-param name="type" select="'aggregated'" />
      </xsl:apply-templates>
    </tr>
  </xsl:template>

  <xsl:template match="Row">
    <xsl:param name = "treeDepth"/>

   
    <xsl:choose>
      <xsl:when test="count(Rows/Row) = '0'">
        <xsl:call-template name="Cells">
          <xsl:with-param name="treeDepth" select="$treeDepth"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="ParentRow">
          <xsl:with-param name="treeDepth" select="$treeDepth"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:variable name="rwId" select="RowId"/>

    <xsl:apply-templates select="Rows/Row">
      <xsl:with-param name="treeDepth" select="$treeDepth + 1" />
    </xsl:apply-templates>

    <xsl:if test="count(Rows/Row) != '0'">
      <xsl:call-template name = "AggregatedRow">
        <xsl:with-param name="treeDepth" select="$treeDepth"/>
      </xsl:call-template>

    </xsl:if>

  </xsl:template>
  
  <xsl:template match="Cell">
    <xsl:param name = "columnCounter"/>
    <xsl:if test="position() &lt;= $maxNrOfCols">
      <td>
        <xsl:choose>
          <xsl:when test="ValueType and DefaultData">
            <acronym>
              <xsl:attribute name="title">
                <xsl:value-of select="DefaultData"/>
              </xsl:attribute>
              <xsl:call-template name="CellData" />
            </acronym>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="CellData" />
          </xsl:otherwise>
        </xsl:choose>
      </td>
    </xsl:if>
  </xsl:template>

  <xsl:template name="CellData">
    <xsl:choose>
      <xsl:when test="FormattedData">
        <xsl:value-of select="FormattedData"/>
      </xsl:when>
      <xsl:when test="RawData">
        <xsl:value-of select="RawData"/>
      </xsl:when>
      <xsl:when test="DefaultData">
        <xsl:choose>
          <xsl:when test="ValueType">
            <xsl:text>#</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="DefaultData"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <xsl:message terminate="yes">
          <xsl:text>No dataformat turned on</xsl:text>
        </xsl:message>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="/">
    <html>
      <head>
      <insertcss/>
      </head>
      <body>
        <p class="headerImage">
            <headerImage/>
        </p>
        <!-- Reports -->
        <xsl:for-each select="/MultiReport/PRIMEReport|/PRIMEReport">
          <table class ="reportHeader">
            <tr>
              <td class="Name" colspan="2">
                <xsl:value-of select="Name"/>&nbsp;
              </td>
            </tr>
            <tr>
              <td>Valuation Date:</td>
              <td>
                <xsl:value-of select="ReportContents/Table/Settings/Groups/Group[Label='Pricing']/Cell/FormattedData"/>&nbsp;
              </td>
            </tr>
          </table>
        <xsl:apply-templates select="current()/ReportContents"/>
    </xsl:for-each>
      </body>
    </html>
  </xsl:template>
  
</xsl:stylesheet>

