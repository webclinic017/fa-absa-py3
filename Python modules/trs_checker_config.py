email_template = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <style>
    body {
            font-family:Calibri;
        }
    table td th {
        border: 1px solid gray;
        border-spacing: 5px;
    }
    table {
        width:100%;
    }
    th {
        background-color: LightGreen
    }
    .oddrow {
        background-color: LightSalmon;
    }
    .evenrow {
        background-color: Tomato;
    }
    .bold {
        font-weight: bold;
    }
    </style>
</head>

<body>
    <div style="width=75%;">
    <div>Hi,</div>
    <br/>
    <div>please handle the following TRS issues:</div>
    $tables    
    <br/>
    <br/>
    <div>Thanks and Regards</div>
    <br/>
    <div>This message has been created automatically.</div>
    <div>Please do not reply to this email.</div>
    </div>
</body>
</html>
'''

table_row_template = '''
<tr class="$rowclass">
    <td>$instrument</td>
    <td>$leg_type</td>
    <td>$cash_flow_type</td>
    <td>$reset_type</td>
    <td>$issue_description</td>
</tr>
'''

table_template = '''
<br/>
<div class="issueType">Issue type: <span class="bold">$issue_type</span>:<div>
<br/>
<table>
    <tr>
        <th>Instrument</th>
        <th>Leg Type</th>
        <th>Cash Flow Type</th>
        <th>Reset Type</th>
        <th>Issue Description</th>
    </tr>
    $table_rows
</table>
'''
