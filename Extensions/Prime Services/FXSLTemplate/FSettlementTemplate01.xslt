<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html"/>
  <xsl:template match="/">
  <html>
    <style type="text/css">
      h1
      {
        font-weight: bold;
        font-size: small;
        border-bottom-style: solid;
        border-width: 1px;
      }
      table.framed
      {
        border-color: #cc99cc;
        border-top-style: solid;
        border-bottom-style: solid;
        border-width: 1px;
      }
      td
      {
        width: 180px;
        font-size: x-small
      }
      td.col2
      {
        width: 420px
      }
      caption
      {
        text-align: left;
        font-size: x-small;
      }
      caption.major
      {
        font-weight: bold
      }
      caption.minor
      {
        font-style: italic;
      }
    </style>
    <xsl:apply-templates/>
  </html>
  </xsl:template>
  <xsl:template match="FSettlement">
    <head>
      <title>Printout for Settlement(s)</title>
    </head>
    <body>
    <xsl:call-template name="General"/>
    </body>
  </xsl:template>
  <xsl:template name="General">
    <h1>Settlement Id: <xsl:value-of select="name"/></h1>
    <table>
      <tr><td>Trade Number:</td><td class="col2"><xsl:value-of select="trade"/></td></tr>
      <tr><td>Amount:</td><td class="col2"><xsl:value-of select="amount"/></td></tr>
      <tr><td>Currency:</td><td class="col2"><xsl:value-of select="currency"/></td></tr>
      <tr><td>Value Date:</td><td class="col2"><xsl:value-of select="valueDay"/></td></tr>
      <tr><td>Status:</td><td class="col2"><xsl:value-of select="status"/></td></tr>
      <tr><td>Type:</td><td class="col2"><xsl:value-of select="type"/></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Acquirer</caption>
        <tr><td>Name:</td><td><xsl:value-of select="acquirerName"/></td></tr>
        <tr><td>Account:</td><td><xsl:value-of select="acquirerAccName"/></td></tr>
        <tr><td>Account Number:</td><td><xsl:value-of select="acquirerAccount"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Counterparty</caption>
        <tr><td>Name:</td><td><xsl:value-of select="counterpartyName"/></td></tr>
        <tr><td>Account:</td><td><xsl:value-of select="counterpartyAccName"/></td></tr>
        <tr><td>Account Number:</td><td><xsl:value-of select="counterpartyAccount"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td>Create Time:</td><td class="col2"><xsl:value-of select="createTime"/></td></tr>
    </table>
  </xsl:template>
</xsl:stylesheet>
