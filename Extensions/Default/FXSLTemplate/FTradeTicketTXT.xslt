#grouping: aef reporting/secondary templates
#grouping: aef reporting/secondary templates txt

<?xml version="1.0" encoding="UTF-8"?>
<!-- &copy; Copyright 2011 SunGard FRONT ARENA -->
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xalan="http://xml.apache.org/xalan"
    exclude-result-prefixes="xalan">
    <xsl:output method="text" media-type="text/plain"/>
    <xsl:variable name="numberofcolumns" select="//Table/NumberOfColumns"/>
    <xsl:variable name="numberofpages" select="count(//Rows/Row)"/>
    <xsl:variable name="TTP_skip" select="count(//Columns/Column[starts-with(Label,'TTP_skip')]/preceding-sibling::Column)"/>
    <xsl:variable name="TTP_skip_option" select="//Columns/Column[starts-with(Label,'TTP_skip')]/ColumnId"/>
                <xsl:variable name="time" select="concat(substring(//LocalTime[1],1,10),' ',substring(//LocalTime[1],12,8),' (UTC', substring(//LocalTime[1],20,6),')')"/>

    <xsl:template match="/">
            <xsl:apply-templates select="//Rows/Row" mode="prepare"/>
    </xsl:template>

<!-- Prepare a row, delete empty columns -->    
    <xsl:template match="Row" mode="prepare">
        <xsl:variable name="rowtree" >
            <xsl:copy>  
                <Row>
                    <xsl:apply-templates select="@*|node()" mode="copy"/>
                </Row>
                <Time>
                    <xsl:value-of select="$time"/>
                </Time>
            </xsl:copy>
        </xsl:variable>

        <xsl:apply-templates select="xalan:nodeset($rowtree)/Row" mode="output"/>

        <xsl:if test="position() &lt; $numberofpages">
            <xsl:text>Formfeed&#x0A;</xsl:text>
        </xsl:if>

    </xsl:template>

<!-- Copy and alter Row-->
    <xsl:template match="Cells/Cell" mode="copy">   
        <xsl:variable name="pos" select="position()"/>  
        <xsl:variable name="label" select="//Columns//Column[$pos]/Label"/>
        
        <xsl:choose>
            <xsl:when test="starts-with($label,'TTP_skip')"/>
            <xsl:when test="starts-with($label,'TTBS_') and count(../../Queries/query[@name=$label]/data) = 0"/>
            <xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'None') and FormattedData = 'None'"/> 
            <xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'zero') and number(RawData) = 0"/>
            <xsl:when test="$TTP_skip > 0 and $pos > $TTP_skip and not(starts-with($label,'TT')) and contains($TTP_skip_option,'empty') and FormattedData = ''"/>
            <xsl:otherwise>
                <xsl:copy>  
                    <xsl:apply-templates select="@*|node()" mode="copy"/>   
                    <Label>
                        <xsl:value-of select="$label"/>
                    </Label>
                </xsl:copy>
                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="@*|node()" mode="copy">    
        <xsl:copy>  
            <xsl:apply-templates select="@*|node()" mode="copy"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="Row" mode="output">
        <xsl:call-template name="align">
            <xsl:with-param name="str" select="'TRADE TICKET'"/>
            <xsl:with-param name="siz" select="92"/>
            <xsl:with-param name="pos" select="'center'"/>
        </xsl:call-template>
        <xsl:text>&#x0A;</xsl:text>
        <xsl:call-template name="repeat-string">
            <xsl:with-param name="str" select="'-'"/>
            <xsl:with-param name="cnt" select="92"/>
        </xsl:call-template>
        <xsl:text>&#x0A;</xsl:text>
        
        <xsl:call-template name="PrintRow">
            <xsl:with-param name="column" select="1"/>
            <xsl:with-param name="dcol" select="0"/>
            <xsl:with-param name="numberofcolumns" select="count(Row/Cells/Cell)"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="query" mode="output">
        <xsl:text>&#x0A;</xsl:text>
        <xsl:for-each select="header/column">
            <xsl:value-of select="."/><xsl:text> </xsl:text>
        </xsl:for-each>
        <xsl:text>&#x0A;</xsl:text>
        
        <xsl:for-each select="header/column">
            <xsl:call-template name="repeat-string">
                <xsl:with-param name="str" select="'-'"/>
                <xsl:with-param name="cnt" select="string-length(.)"/>
            </xsl:call-template>
            <xsl:text> </xsl:text>
        </xsl:for-each>
        
        <xsl:text>&#x0A;</xsl:text>
        <xsl:for-each select="data">
            <xsl:for-each select="column">
                <xsl:variable name="pos" select="position()"/>
                <xsl:call-template name="align">
                    <xsl:with-param name="str" select="."/>
                    <xsl:with-param name="siz" select="string-length(../../header/column[$pos])"/>
                    <xsl:with-param name="pos" select="'left'"/>
                </xsl:call-template>
                <xsl:text> </xsl:text>
            </xsl:for-each>
            <xsl:text>&#x0A;</xsl:text>
        </xsl:for-each>

    </xsl:template>

    <xsl:template name="PrintRow">
        <xsl:param name="column"/>
        <xsl:param name="dcol"/>
        <xsl:param name="numberofcolumns"/>

        <xsl:variable name="header" select="Row/Cells/Cell[$column]/Label"/>
<!--
                <xsl:value-of select="$header"/><xsl:text>&#x0A;</xsl:text>
                <xsl:value-of select="$column"/><xsl:text>&#x0A;</xsl:text>
                <xsl:value-of select="$dcol"/><xsl:text>&#x0A;</xsl:text>
                <xsl:value-of select="$numberofcolumns"/><xsl:text>&#x0A;</xsl:text>
-->         
        <xsl:choose>
            <xsl:when test="$column>$numberofcolumns"/>
            <xsl:when test="starts-with($header,'TTBS_')">
                <xsl:variable name="ttbpos" select="count(Row/Cells/Cell[$column]/following-sibling::Cell[starts-with(Label,'TTB')][1]/preceding-sibling::Cell)"/>
                <xsl:variable name="nextpos" select="($ttbpos > 0) * $ttbpos + ($ttbpos = 0) * $numberofcolumns"/>

                <xsl:apply-templates select="node()/Queries/query[@name=$header]" mode="output"/>

                <xsl:call-template name="PrintTable"> 
                    <xsl:with-param name="column" select="$column+starts-with($header,'TTB')"/>
                    <xsl:with-param name="endcol" select="$nextpos"/>
                    <xsl:with-param name="dcol" select="0"/>
                </xsl:call-template>


                <xsl:call-template name="PrintRow">
                    <xsl:with-param name="column" select="$nextpos+1"/>
                    <xsl:with-param name="dcol" select="$dcol"/>
                    <xsl:with-param name="numberofcolumns" select="$numberofcolumns"/>
                </xsl:call-template>

            </xsl:when>
            <xsl:when test="starts-with($header,'TTB_') or $column = 1">
                <xsl:variable name="ttbpos" select="count(Row/Cells/Cell[$column]/following-sibling::Cell[starts-with(Label,'TTB')][1]/preceding-sibling::Cell)"/>
                <xsl:variable name="nextpos" select="($ttbpos > 0) * $ttbpos + ($ttbpos = 0) * $numberofcolumns"/>

                <xsl:if test="(1+$nextpos - $column - starts-with($header,'TTB_') + starts-with(Row/Cells/Cell[$column+1]/Label,'TTBS')) > 0">

                    <xsl:if test="starts-with($header,'TTB_')">

                        <xsl:text>&#x0A;</xsl:text>
                        <xsl:value-of select="substring-after($header,'TTB_')"/>
                        <xsl:text>&#x0A;</xsl:text>
                        <xsl:call-template name="repeat-string">
                            <xsl:with-param name="str" select="'-'"/>
                            <xsl:with-param name="cnt" select="string-length(substring-after($header,'TTB_'))"/>
                        </xsl:call-template>
                        <xsl:text>&#x0A;&#x0A;</xsl:text>
                    </xsl:if>

                    <xsl:call-template name="PrintTable"> 
                        <xsl:with-param name="column" select="$column+starts-with($header,'TTB_')"/>
                        <xsl:with-param name="endcol" select="$nextpos"/>
                        <xsl:with-param name="dcol" select="0"/>
                    </xsl:call-template>
                </xsl:if>

                <xsl:call-template name="PrintRow">
                    <xsl:with-param name="column" select="$nextpos+1"/>
                    <xsl:with-param name="dcol" select="$dcol"/>
                    <xsl:with-param name="numberofcolumns" select="$numberofcolumns"/>
                </xsl:call-template>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="PrintTable">
        <xsl:param name="column"/>
        <xsl:param name="dcol"/>
        <xsl:param name="endcol"/>
        
        <xsl:choose>
            <xsl:when test="$column>$endcol"/>
            <xsl:otherwise>
                        <xsl:call-template name="PrintColumn">
                            <xsl:with-param name="column" select="$column"/>
                            <xsl:with-param name="colspan" select="starts-with(Row/Cells/Cell[$column+1]/Label,'TTV_Void')+1"/>
                        </xsl:call-template>
                    <xsl:text>  </xsl:text>
                        <xsl:call-template name="PrintColumn">
                            <xsl:with-param name="column" select="$column+1"/>
                            <xsl:with-param name="colspan" select="1"/>
                        </xsl:call-template>
                    <xsl:text>&#x0A;</xsl:text>
                <xsl:call-template name="PrintTable">
                    <xsl:with-param name="column" select="$column+2"/>
                    <xsl:with-param name="dcol" select="$dcol"/>
                    <xsl:with-param name="endcol" select="$endcol"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>


    <xsl:template name="PrintColumn">
        <xsl:param name="column"/>
        <xsl:param name="colspan" select="1"/>
        <xsl:variable name="header" select="Row/Cells/Cell[$column]/Label"/>
        <xsl:choose>
            <xsl:when test="starts-with($header,'TTV_Void') or starts-with($header,'TTB')">
                <xsl:call-template name="align">
                    <xsl:with-param name="str" select="''"/>
                    <xsl:with-param name="siz" select="15"/>
                    <xsl:with-param name="pos" select="'left'"/>
                </xsl:call-template>
                <xsl:call-template name="align">
                    <xsl:with-param name="str" select="''"/>
                    <xsl:with-param name="siz" select="30"/>
                    <xsl:with-param name="pos" select="'right'"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="align">
                    <xsl:with-param name="str" select="$header"/>
                    <xsl:with-param name="siz" select="15"/>
                    <xsl:with-param name="pos" select="'left'"/>
                </xsl:call-template>
                <xsl:choose>
                    <xsl:when test="$colspan>1 and string-length(Row/Cells/Cell[$column]/FormattedData)>30">
                        <xsl:value-of select="Row/Cells/Cell[$column]/FormattedData" />
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="align">
                            <xsl:with-param name="str" select="Row/Cells/Cell[$column]/FormattedData"/>
                            <xsl:with-param name="siz" select="30"/>
                            <xsl:with-param name="pos" select="'right'"/>
                        </xsl:call-template>
                </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- derived from http://www.exslt.org/str/functions/align/index.html -->
    <!-- aligns a string within another string. -->

    <xsl:template name="align">
        <xsl:param name="str" select="''" />
        <xsl:param name="siz" select="15" />
        <xsl:param name="alignment" select="'left'" />

        <xsl:variable name="padding">
              <xsl:call-template name="repeat-string">
                <xsl:with-param name="str" select=" ' ' "/>
                <xsl:with-param name="cnt" select="$siz"/>
              </xsl:call-template>
        </xsl:variable>
                
        <xsl:variable name="string" select="substring($str,1,$siz)"/>
        <xsl:variable name="str-length" select="string-length($string)" />
        
       <xsl:choose>
          <xsl:when test="$alignment = 'center'">
             <xsl:variable name="half-remainder" select="floor(($siz - $str-length) div 2)" />
             <xsl:value-of select="substring($padding, 1, $half-remainder)" />
             <xsl:value-of select="$string" />
             <xsl:value-of select="substring($padding, $str-length + $half-remainder + 1)" />
          </xsl:when>
          <xsl:when test="$alignment = 'right'">
             <xsl:value-of select="substring($padding, 1, $siz - $str-length)" />
             <xsl:value-of select="$string" />
          </xsl:when>
          <xsl:otherwise>
             <xsl:value-of select="$string" />
             <xsl:value-of select="substring($padding, $str-length + 1)" />
          </xsl:otherwise>
       </xsl:choose>
    </xsl:template>
    
    <!-- http://aspn.activestate.com/ASPN/Cookbook/XSLT/Recipe/148987 -->
    <!-- Repeat the string 'str' 'cnt' times -->
    <xsl:template name="repeat-string">
      <xsl:param name="str"/><!-- The string to repeat -->
      <xsl:param name="cnt"/><!-- The number of times to repeat the string -->
      <xsl:param name="pfx"/><!-- The prefix to add to the string -->
      <xsl:choose>
        <xsl:when test="$cnt = 0">
          <xsl:value-of select="$pfx"/>
        </xsl:when>
        <xsl:when test="$cnt mod 2 = 1">
          <xsl:call-template name="repeat-string">
          <xsl:with-param name="str" select="concat($str,$str)"/>
          <xsl:with-param name="cnt" select="($cnt - 1) div 2"/>
          <xsl:with-param name="pfx" select="concat($pfx,$str)"/>
        </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
        <xsl:call-template name="repeat-string">
          <xsl:with-param name="str" select="concat($str,$str)"/>
          <xsl:with-param name="cnt" select="$cnt div 2"/>
          <xsl:with-param name="pfx" select="$pfx"/>
        </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
