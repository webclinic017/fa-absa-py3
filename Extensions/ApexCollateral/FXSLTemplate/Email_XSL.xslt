<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  
  <xsl:apply-templates/>

  <br/>
  
  <img id="barclays-logo" height="30"  src="http://now.barclays.com/CI_S/assets/images/barclays_logo.gif"/>

</body>


</html>

</xsl:template>

<xsl:template match="message/type">
  <xsl:choose>
         <xsl:when test="'Technical' = .">
                <font color="red">
                <h3>Front/Apex Integration Technical Error</h3>
                </font>
         </xsl:when>
         <xsl:otherwise>
                <font color="#0099FF">
                <h3>Front/Apex Integration Functional Error</h3>
                </font>
         </xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="message/description">
<p>
<b>Description:</b>
<xsl:value-of select="."/>
</p>
 
</xsl:template>

<xsl:template match="message/logMessages">
<xsl:if test="*">
<b>Log messages:</b>
    <ol>
    <xsl:for-each select="logMessage">
      <li><xsl:value-of select="." /></li>
    </xsl:for-each>
    </ol>
</xsl:if>
</xsl:template>

<xsl:template match="message/stackTraces">
<xsl:if test="*">
<font color="red">
<b>Stack traceback:</b>
    <ol>
    <xsl:for-each select="stackTrace">
      <li><xsl:value-of select="." /></li>
    </xsl:for-each>
    </ol>
</font>
</xsl:if>
</xsl:template>

<xsl:template match="message/hostname">
This email was sent from host: <span style="color:#CC6600">
  <xsl:value-of select="."/></span>
</xsl:template>

<xsl:template match="message/environmentName">
using the environment settings: <span style="color:#CC6600">
  <xsl:value-of select="."/></span>
<hr/>
</xsl:template>


</xsl:stylesheet>
