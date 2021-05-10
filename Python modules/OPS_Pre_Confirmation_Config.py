email_template = r'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns:v="urn:schemas-microsoft-com:vml"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:w="urn:schemas-microsoft-com:office:word"
    xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"
    xmlns="http://www.w3.org/TR/REC-html40">

    <head>
        <meta http-equiv=Content-Type content="text/html; charset=windows-1252">
        <meta name=ProgId content=Word.Document>
        <meta name=Generator content="Microsoft Word 12">
        <meta name=Originator content="Microsoft Word 12">
        
        <style type="text/css">
            .css_class {
                font-weight:bold;
                font-size:14px;
            }
        </style>
            
    </head>
    <body>
        <div>Hi </div>
        <br/>
        <div class="css_class">We confirm settlement of below:</div>
        <div>Kindly provide your agreement of the details below:</div>
        <br/>
        <div class="css_class">Value date:</div>
        <div>$value_date</div>
        <br/>
        <div class="css_class">$action:</div>
        <div>$currency $projected_payment</div>
        <br/>
        <div>Please confirm the following:</div>
        <div>Settlement will  be on a net basis</div>
        <div>Kindly confirm that you are in agreement with the SSI details provided below.</div>
        <br/>
        <table>
            <tr>
                <td><p>Bank:</p></td>
                <td><p>$bank</p></td>
            </tr>
            <tr>
                <td><p>a/c number:</p></td>
                <td><p>$account_number</p></td>
            </tr>
            <tr>
                <td><p>Branch code:</p></td>
                <td><p>$branch_code</p></td>
            </tr>
            <tr>
                <td><p>Swift Address:</p></td>
                <td><p>$swift_addr</p></td>
            </tr>
        </table>
        <br>
        </br>
        <table border = "1">
            <tr>
                <td><p class="css_class">Counterparty</p></td>
                <td><p class="css_class">Trade Nbr</p></td>
                <td><p class="css_class">InsType</p></td>
                <td><p class="css_class">Trade Nominal</p></td>
                <td><p class="css_class">PayD</p></td>
                <td><p class="css_class">Curr</p></td>
                <td><p class="css_class">Proj</p></td>
            </tr>
            $table_rows
            $table_sum
        </table>
        <br/>
        <div>Thanks and Regards</div>
    </body>
</html>'''

table_row_template = '''
<tr>
    <td><p>$counterparty</p></td>
    <td><p>$trade_number</p></td>
    <td><p>$instype</p></td>
    <td><p>$trade_nominal</p></td>
    <td><p>$pay_date</p></td>
    <td><p>$currency</p></td>
    <td><p>$projected</p></td>
</tr>
'''
