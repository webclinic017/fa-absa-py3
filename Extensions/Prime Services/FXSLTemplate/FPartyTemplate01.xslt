<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:param name="sections" select="'GENERAL'"/>
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
  <xsl:template match="/*">
  <head>
  <title>Printout for Party:<xsl:value-of select="name"/></title>
  </head>
  <body>
    <xsl:if test="contains($sections,'GENERAL')"><xsl:call-template name="General"/></xsl:if>
    <xsl:if test="contains($sections,'DETAILS')"><xsl:call-template name="Details"/></xsl:if>
    <xsl:if test="contains($sections,'ACCOUNTS')"><xsl:apply-templates select="accounts"/></xsl:if>
    <xsl:if test="contains($sections,'SETTLEINSTRUCTIONS')"><xsl:apply-templates select="settleInstructions"/></xsl:if>
    <xsl:if test="contains($sections,'CONTACTS')"><xsl:apply-templates select="contacts"/></xsl:if>
    <xsl:if test="contains($sections,'ALIAS')"><xsl:apply-templates select="aliases"/></xsl:if>
    <xsl:if test="contains($sections,'AGREEMENTS')"><xsl:apply-templates select="agreements"/></xsl:if>
    <xsl:if test="contains($sections,'NETTINGRULES')"><xsl:apply-templates select="nettingRuleLinks"/></xsl:if>
    <xsl:if test="contains($sections,'BROKERFEES')"><xsl:apply-templates select="brokerFeeRates"/></xsl:if>
    <xsl:if test="contains($sections,'CONFINSTRUCTIONS')"><xsl:apply-templates select="confInstructions"/></xsl:if>
  </body>
  </xsl:template>
  <xsl:template name="General">
    <h1>General</h1>
    <table>
      <tr><td>Name:</td><td class="col2"><xsl:value-of select="id"/></td></tr>
      <tr><td>Alias:</td><td class="col2"><xsl:value-of select="id2"/></td></tr>
      <tr><td>Fullname:</td><td class="col2"><xsl:value-of select="fullname"/></td></tr>
      <tr><td>Additional Fullname:</td><td class="col2"><xsl:value-of select="fullname2"/></td></tr>
      <tr><td>RED:</td><td class="col2"><xsl:value-of select="redCode"/></td></tr>
      <tr><td>Attention:</td><td class="col2"><xsl:value-of select="attention"/></td></tr>
      <tr><td>Host ID:</td><td class="col2"><xsl:value-of select="hostId"/></td></tr>
      <tr><td>Address:</td><td class="col2"><xsl:value-of select="address"/></td></tr>
      <tr><td>Additional Address:</td><td class="col2"><xsl:value-of select="address2"/></td></tr>
      <tr><td>Zip Code:</td><td class="col2"><xsl:value-of select="zipCode"/></td></tr>
      <tr><td>City:</td><td class="col2"><xsl:value-of select="city"/></td></tr>
      <tr><td>Country:</td><td class="col2"><xsl:value-of select="country"/></td></tr>
      <tr><td>Contact/Tel:</td><td class="col2"><xsl:value-of select="contact1"/></td></tr>
      <tr><td/><td class="col2"><xsl:value-of select="contact2"/></td></tr>
      <tr><td>Telephone:</td><td class="col2"><xsl:value-of select="telephone"/></td></tr>
      <tr><td>Telefax:</td><td class="col2"><xsl:value-of select="fax"/></td></tr>
      <tr><td>Telex:</td><td class="col2"><xsl:value-of select="telex"/></td></tr>
      <tr><td>Email:</td><td class="col2"><xsl:value-of select="email"/></td></tr>
      <tr><td>BIC:</td><td class="col2"><xsl:value-of select="swift"/></td></tr>
      <tr><td>BIS Status:</td><td class="col2"><xsl:value-of select="bisStatus"/></td></tr>:
      <tr><td>Document Type:</td><td class="col2"><xsl:value-of select="documentType"/></td></tr>
      <tr><td>Business Status:</td><td class="col2"><xsl:value-of select="businessStatus"/></td></tr>
      <tr><td>Legal Form:</td><td class="col2"><xsl:value-of select="legalForm"/></td></tr>
      <tr><td>Document Date:</td><td class="col2"><xsl:value-of select="documentDate"/></td></tr>
      <tr><td>Consolidate:</td><td class="col2"><xsl:value-of select="Consolidate"/></td></tr>
      <tr><td>Type:</td><td class="col2"><xsl:value-of select="type"/></td></tr>
      <tr><td>Issuer:</td><td class="col2"><xsl:choose><xsl:when test="issuer=1">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Correspondent Bank:</td><td class="col2"><xsl:choose><xsl:when test="correspondentBank=1">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>ISDA Member:</td><td class="col2"><xsl:choose><xsl:when test="isdaMember=1">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Cash Flow Netting:</td><td class="col2"><xsl:choose><xsl:when test="netting='true'">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Notification to Receipt:</td><td class="col2"><xsl:choose><xsl:when test="notifyReceipt=1">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Not Trading:</td><td class="col2"><xsl:value-of select="notTrading"/></td></tr>
      <tr><td>Time Zone:</td><td class="col2"><xsl:value-of select="timeZone"/></td></tr>
      <tr><td>External Cut-off Time:</td><td class="col2"><xsl:if test="externalCutOff!=0"><xsl:value-of select="externalCutOff"/></xsl:if></td></tr>
      <tr><td>Internal Offset Time:</td><td class="col2"><xsl:if test="internalCutOff!=0"><xsl:value-of select="internalCutOff"/></xsl:if></td></tr>
      <tr><td>Parent:</td><td class="col2"><xsl:value-of select="parent"/></td></tr>
      <tr><td>Rel. to Parent:</td><td class="col2"><xsl:value-of select="relation"/></td></tr>
      <tr><td>Guarantor:</td><td class="col2"><xsl:value-of select="guarantor"/></td></tr>
      <tr><td>Group Limit:</td><td class="col2"><xsl:choose><xsl:when test="groupLimit=1">Yes</xsl:when><xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
      <tr><td>CLS Bank Type:</td><td class="col2"><xsl:value-of select="cls"/></td></tr>
    </table>
    <p>
    <table class="framed">
      <caption class="major">Ratings</caption>
      <tr><td>Our Rate:</td><td class="col2"><xsl:value-of select="rating1"/></td></tr>
      <tr><td>Moodys:</td><td class="col2"><xsl:value-of select="rating2"/></td></tr>
      <tr><td>S&amp;P:</td><td class="col2"><xsl:value-of select="rating3"/></td></tr>
      <tr><td>Rating:</td><td class="col2"><xsl:value-of select="rating"/></td></tr>
      <tr><td>Rating Agency:</td><td class="col2"><xsl:value-of select="ratingAgency"/></td></tr>
      <tr><td>Country of Risk:</td><td class="col2"><xsl:value-of select="riskCountry"/></td></tr>
      <tr><td>User Rating:</td><td class="col2"><xsl:value-of select="userRating"/></td></tr>
      <tr><td>Rating date:</td><td class="col2"><xsl:value-of select="ratingDate"/></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template name="Details">
    <h1>Details</h1>
    <p>
    <table class="framed">
      <caption class="major">Credit Events</caption>
        <xsl:variable name="bankruptcy" select="bankruptcy" />
        <tr><td>Bankruptcy:</td><td class="col2"><xsl:choose>
          <xsl:when test="$bankruptcy='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="failureToPay" select="failureToPay" />
        <tr><td>Failure to Pay:</td><td class="col2"><xsl:choose>
          <xsl:when test="$failureToPay='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="oblAcceleration" select="oblAcceleration" />
        <tr><td>Obl. Acceleration:</td><td class="col2"><xsl:choose>
          <xsl:when test="$oblAcceleration='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="oblDefault" select="oblDefault" />
        <tr><td>Obl. Default:</td><td class="col2"><xsl:choose>
          <xsl:when test="$oblDefault='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="repudiation" select="repudiation" />
        <tr><td>Repudiation:</td><td class="col2"><xsl:choose>
          <xsl:when test="$repudiation='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="restructuring" select="restructuring" />
        <tr><td>Restructuring:</td><td class="col2"><xsl:choose>
          <xsl:when test="$restructuring='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
    </table>
    </p>
    <table>

        <xsl:variable name="priceAccessControl" select="priceAccessControl" />
        <tr><td>Price Access Control:</td><td class="col2"><xsl:choose>
          <xsl:when test="$priceAccessControl='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>
        <xsl:variable name="issuerAccounts" select="issuerAccounts" />
        <tr><td>Issuer Accounts:</td><td class="col2"><xsl:choose>
          <xsl:when test="$issuerAccounts='true'">Yes</xsl:when>
          <xsl:otherwise>No</xsl:otherwise></xsl:choose></td></tr>

      <tr><td>Free Choice List 1:</td><td class="col2"><xsl:value-of select="free1ChoiceList"/></td></tr>
      <tr><td>Free Choice List 2:</td><td class="col2"><xsl:value-of select="free2ChoiceList"/></td></tr>
      <tr><td>Free Choice List 3:</td><td class="col2"><xsl:value-of select="free3ChoiceList"/></td></tr>
      <tr><td>Free Choice List 4:</td><td class="col2"><xsl:value-of select="free4ChoiceList"/></td></tr>
      <tr><td>Free Text 1:</td><td class="col2"><xsl:value-of select="free1"/></td></tr>
      <tr><td>Free Text 2:</td><td class="col2"><xsl:value-of select="free2"/></td></tr>
      <tr><td>Free Text 3:</td><td class="col2"><xsl:value-of select="free3"/></td></tr>
      <tr><td>Free Text 4:</td><td class="col2"><xsl:value-of select="free4"/></td></tr>
    </table>
  </xsl:template>
  <xsl:template match="accounts">
    <h1>Accounts</h1>
    <xsl:apply-templates select="FAccount"/>
  </xsl:template>
  <xsl:template match="FAccount">
    <p>
    <table class="framed">
      <caption class="major">Account: <xsl:value-of select="name"/></caption>
      <tr><td>Currency:</td><td class="col2"><xsl:value-of select="currency"/></td></tr>
      <tr><td>Account Type:</td><td class="col2"><xsl:value-of select="accountType"/></td></tr>
      <tr><td>Details of Charges:</td><td class="col2"><xsl:value-of select="detailsOfCharges"/></td></tr>
      <tr><td>Network:</td><td class="col2"><xsl:value-of select="networkAliasType"/></td></tr>
      <tr><td>Free Text:</td><td class="col2"><xsl:value-of select="accounting"/></td></tr>
      <tr><td>External Cut-off:</td><td class="col2"><xsl:value-of select="externalCutOff"/></td></tr>
      <tr><td>Internal Cut-off:</td><td class="col2"><xsl:value-of select="internalCutOff"/></td></tr>
      <tr><td>Network Alias:</td><td class="col2"><xsl:value-of select="networkAlias"/></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Correspondent Bank: <xsl:value-of select="correspondentBank"/></caption>
        <tr><td>Account Number:</td><td><xsl:value-of select="account"/></td></tr>
        <tr><td>CP Code:</td><td><xsl:value-of select="bic"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Intermediary 1: <xsl:value-of select="correspondentBank2"/></caption>
        <tr><td>Account Number:</td><td><xsl:value-of select="account2"/></td></tr>
        <tr><td>CP Code:</td><td><xsl:value-of select="bic2"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Intermediary 2: <xsl:value-of select="correspondentBank3"/></caption>
        <tr><td>Account Number:</td><td><xsl:value-of select="account3"/></td></tr>
        <tr><td>CP Code:</td><td><xsl:value-of select="bic3"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Intermediary 3: <xsl:value-of select="correspondentBank4"/></caption>
        <tr><td>Account Number:</td><td><xsl:value-of select="account4"/></td></tr>
        <tr><td>CP Code:</td><td><xsl:value-of select="bic4"/></td></tr>
      </table></td></tr>
      <tr><td><br/></td><td><br/></td></tr>
      <tr><td colspan="2" class="col2"><table class="framed">
        <caption class="minor">Additional Account: <xsl:value-of select="correspondentBank5"/></caption>
        <tr><td>Account Number:</td><td><xsl:value-of select="account5"/></td></tr>
        <tr><td>CP Code:</td><td><xsl:value-of select="bic5"/></td></tr>
      </table></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template match="settleInstructions">
    <h1>Settle Instructions</h1>
    <xsl:apply-templates select="FSettleInstruction"/>
  </xsl:template>
  <xsl:template match="FSettleInstruction">
    <table class="framed">
      <caption class="major">Settle Instruction: <xsl:value-of select="name"/></caption>
      <tr><td>From Party:</td><td class="col2"><xsl:choose><xsl:when test="fromParty='&lt;none&gt;'">None</xsl:when><xsl:otherwise><xsl:value-of select="fromParty"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Ins Category:</td><td class="col2"><xsl:choose><xsl:when test="settleCategoryChlItem='&lt;none&gt;'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="settleCategoryChlItem"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Trade Category:</td><td class="col2"><xsl:choose><xsl:when test="tradeCategory='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="tradeCategory"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Instrument Type:</td><td class="col2"><xsl:choose><xsl:when test="instrumentType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="instrumentType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Und Ins Type:</td><td class="col2"><xsl:choose><xsl:when test="undInsType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="undInsType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Currency:</td><td class="col2"><xsl:value-of select="currency"/></td></tr>
      <tr><td>Cash CF Type:</td><td class="col2"><xsl:choose><xsl:when test="accountType='Security'">n/a</xsl:when><xsl:when test="cashSettleCashFlowType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="cashSettleCashFlowType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Sec CF Type:</td><td class="col2"><xsl:choose><xsl:when test="accountType='Cash'">n/a</xsl:when><xsl:when test="secSettleCashFlowType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="secSettleCashFlowType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Settle Delivery Type:</td><td class="col2"><xsl:value-of select="settleDeliveryType"/></td></tr>
      <tr><td>Account Type:</td><td class="col2"><xsl:value-of select="accountType"/></td></tr>
      <tr><td>OTC:</td><td class="col2"><xsl:choose><xsl:when test="otcInstr='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="otcInstr"/></xsl:otherwise></xsl:choose></td></tr>
      <xsl:apply-templates select="rules"/>
    </table>
  </xsl:template>
  <xsl:template match="confInstructions">
    <h1>Confirmation Instructions</h1>
    <xsl:apply-templates select="FConfInstruction"/>
  </xsl:template>
  <xsl:template match="FConfInstruction">
    <table class="framed">
      <caption class="major">Confirmation Instruction: <xsl:value-of select="name"/></caption>
      <tr><td>Active:</td><td class="col2"><xsl:value-of select="active"/></td></tr>
      <tr><td>Department:</td><td class="col2"><xsl:choose><xsl:when test="internalDepartment='&lt;none&gt;'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="internalDepartment"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Instrument Type:</td><td class="col2"><xsl:choose><xsl:when test="insType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="insType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Underlying Instr Type:</td><td class="col2"><xsl:choose><xsl:when test="undInsType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="undInsType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Product Type:</td><td class="col2"><xsl:choose><xsl:when test="productTypeChlItem='&lt;none&gt;'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="productTypeChlItem"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Document:</td><td class="col2"><xsl:choose><xsl:when test="documentTypeChlItem='&lt;none&gt;'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="documentTypeChlItem"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Event:</td><td class="col2"><xsl:choose><xsl:when test="eventChlItem='&lt;none&gt;'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="eventChlItem"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Leg Type:</td><td class="col2"><xsl:choose><xsl:when test="legType='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="legType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>OTC:</td><td class="col2"><xsl:choose><xsl:when test="otcInstr='None'">&lt;All&gt;</xsl:when><xsl:otherwise><xsl:value-of select="otcInstr"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Template:</td><td class="col2"><xsl:value-of select="confTemplateChlItem"/></td></tr>
      <tr><td>Transport:</td><td class="col2"><xsl:value-of select="transport"/></td></tr>
      <tr><td>Group 1:</td><td class="col2"><xsl:choose><xsl:when test="signOffGroup1='&lt;none&gt;'">None</xsl:when><xsl:otherwise><xsl:value-of select="signOffGroup1"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Group 2:</td><td class="col2"><xsl:choose><xsl:when test="signOffGroup2='&lt;none&gt;'">None</xsl:when><xsl:otherwise><xsl:value-of select="signOffGroup2"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Method:</td><td class="col2"><xsl:value-of select="chaserCutoffMethod"/></td></tr>
      <tr><td>Chaser Cutoff Period:</td><td class="col2"><xsl:value-of select="chaserCutoffPeriodCount"/></td></tr>
      <tr><td>STP:</td><td class="col2"><xsl:value-of select="stp"/></td></tr>
    </table>
  </xsl:template>
  <xsl:template match="rules">
    <xsl:apply-templates select="FSettleInstructionRule"/>
  </xsl:template>
  <xsl:template match="FSettleInstructionRule">
    <tr><td><br/></td><td><br/></td></tr>
    <tr><td colspan="2" class="col2"><table class="framed">
      <caption class="minor">Settlement Instruction Rule: <xsl:value-of select="oid"/></caption>
      <tr><td>Settle Instruction:</td><td><xsl:value-of select="settleInstruction"/></td></tr>
      <tr><td>Effective From:</td><td><xsl:value-of select="effectiveFrom"/></td></tr>
      <tr><td>Effective To:</td><td><xsl:value-of select="effectiveTo"/></td></tr>
      <tr><td>Cash Account:</td><td><xsl:value-of select="cashAccount"/></td></tr>
      <tr><td>Sec Account:</td><td><xsl:value-of select="secAccount"/></td></tr>
      <tr><td>CLS Account:</td><td><xsl:value-of select="clsAccount"/></td></tr>
    </table></td></tr>
  </xsl:template>
  <xsl:template match="aliases">
    <h1>Alias</h1>
    <xsl:apply-templates select="FPartyAlias"/>
  </xsl:template>
  <xsl:template match="FPartyAlias">
    <p>
    <table class="framed">
    <caption class="minor">Alias:y</caption>
    <tr><td>Alias Type:</td><td class="col2"><xsl:value-of select="type"/></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template match="contacts">
    <h1>Contacts</h1>
    <xsl:apply-templates select="FContact"/>
  </xsl:template>
  <xsl:template match="FContact">
    <table class="framed">
      <caption class="major">Contact: <xsl:value-of select="fullname"/></caption>
      <tr><td>Attention:</td><td class="col2"><xsl:value-of select="attention"/></td></tr>
      <tr><td>Address:</td><td class="col2"><xsl:value-of select="address"/></td></tr>
      <tr><td>Address2:</td><td class="col2"><xsl:value-of select="address2"/></td></tr>
      <tr><td>Zip Code:</td><td class="col2"><xsl:value-of select="zipcode"/></td></tr>
      <tr><td>City:</td><td class="col2"><xsl:value-of select="city"/></td></tr>
      <tr><td>Country:</td><td class="col2"><xsl:value-of select="country"/></td></tr>
      <tr><td>Telephone:</td><td class="col2"><xsl:value-of select="telephone"/></td></tr>
      <tr><td>Fax:</td><td class="col2"><xsl:value-of select="fax"/></td></tr>
      <tr><td>Email:</td><td class="col2"><xsl:value-of select="email"/></td></tr>
      <tr><td>Network:</td><td class="col2"><xsl:value-of select="networkAliasType"/></td></tr>
      <tr><td>Network Alias:</td><td class="col2"><xsl:value-of select="networkAlias"/></td></tr>
      <tr><td>Network2:</td><td class="col2"><xsl:value-of select="network2AliasType"/></td></tr>
      <tr><td>Network2 Alias:</td><td class="col2"><xsl:value-of select="network2Alias"/></td></tr>
    <xsl:apply-templates select="contactRules"/>
    </table>
  </xsl:template>
  <xsl:template match="contactRule">
    <xsl:apply-templates select="FContactRule"/>
  </xsl:template>
  <xsl:template match="FContactRule">
    <tr><td><br/></td><td><br/></td></tr>
    <tr><td colspan="2" class="col2"><table class="framed">
      <caption class="minor">Contact Rule</caption>
      <tr><td>Department:</td><td><xsl:value-of select="acquirer"/></td></tr>
      <tr><td>Instrument Type:</td><td><xsl:value-of select="insType"/></td></tr>
      <tr><td>Und Ins Type:</td><td><xsl:value-of select="undInsType"/></td></tr>
      <tr><td>Product:</td><td><xsl:value-of select="productTypeChlItem"/></td></tr>
      <tr><td>Event:</td><td><xsl:value-of select="eventChlItem"/></td></tr>
      <tr><td>Currency:</td><td><xsl:value-of select="currency"/></td></tr>
    </table></td></tr>
  </xsl:template>
  <xsl:template match="aliases">
    <h1>Alias</h1>
    <xsl:apply-templates select="FPartyAlias"/>
  </xsl:template>
  <xsl:template match="FPartyAlias">
    <p>
    <table class="framed">
      <caption class="major">Alias: <xsl:value-of select="alias"/></caption>
      <tr><td>Alias Type:</td><td class="col2"><xsl:value-of select="type"/></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template match="agreements">
    <h1>Agreements</h1>
    <xsl:apply-templates select="FAgreement"/>
  </xsl:template>
  <xsl:template match="FAgreement">
    <p>
    <table class="framed">
      <caption class="major">Agreement: <xsl:value-of select="documentTypeChlItem"/></caption>
      <tr><td>Department:</td><td class="col2"><xsl:value-of select="internalDepartment"/></td></tr>
      <tr><td>Instrument Type:</td><td class="col2"><xsl:value-of select="insType"/></td></tr>
      <tr><td>Und Ins Type:</td><td class="col2"><xsl:choose><xsl:when test="undInsType='None'">All</xsl:when><xsl:otherwise><xsl:value-of select="undInsType"/></xsl:otherwise></xsl:choose></td></tr>
      <tr><td>Document:</td><td class="col2"><xsl:value-of select="documentTypeChlItem"/></td></tr>
      <tr><td>Dated:</td><td class="col2"><xsl:value-of select="dated"/></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template match="nettingRuleLinks">
    <h1>Netting Rule Links</h1>
    <xsl:apply-templates select="FNettingRuleLink">
      <xsl:sort select="orderNumber"/>
    </xsl:apply-templates>
  </xsl:template>
  <xsl:template match="FNettingRuleLink">
    <p>
    <table class="framed">
      <caption class="major">#<xsl:value-of select="orderNumber"/></caption>
      <tr><td>Netting Rule:</td><td class="col2"><xsl:value-of select="nettingRule"/></td></tr>
      <tr><td>Enabled:</td><td class="col2"><xsl:value-of select="enabled"/></td></tr>
    </table>
    </p>
  </xsl:template>
  <xsl:template match="brokerFeeRates">
    <h1>Broker Fee Rates</h1>
    <xsl:apply-templates select="FBrokerFeeRate"/>
  </xsl:template>
  <xsl:template match="FBrokerFeeRate">
    <p>
    <table class="framed">
      <caption class="major">Broker Fee Rate</caption>
      <tr><td>Instrument Type:</td><td class="col2"><xsl:value-of select="insType"/></td></tr>
      <tr><td>Underlying Instrument Type:</td><td class="col2"><xsl:value-of select="undInsType"/></td></tr>
      <tr><td>Broker Fee Rate:</td><td class="col2"><xsl:value-of select="brokerFeeRate"/></td></tr>
    </table>
    </p>
  </xsl:template>
</xsl:stylesheet>
