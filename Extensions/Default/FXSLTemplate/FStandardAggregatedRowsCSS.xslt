#grouping: aef reporting/style sheets


@page {

    margin-top: 50px;
    margin-bottom: 50px;

    @top-center {
        content: flow(header);
        margin-top:20px;
    }

}

.headerImage {
        text-align:center;
        flow: static(header)
}

/* Report Title */
.reportHeader td{
    font-weight:bold;
    font-size: 18px;
    text-align:left;
}

/* General appearance of the table */
.reportTable{
    padding-top: 20px;
    padding-bottom: 30px;
    font-family: arial;
}

thead {
    display:table-header-group 
}

/* Zebra stripes table header  */
.reportTable tr:nth-child(2n+1) {
   /* background-color: #d2daec; */
}

/* Zebra stripes table  */
.reportTable tbody tr:nth-child(2n+1) {
    background-color:#d2daec;
}

/* Column Widths*/
.reportTable td:nth-child(1) {
    width: 120px;
}
.reportTable td:nth-child(2),
.reportTable td:nth-child(3), 
.reportTable td:nth-child(4),
.reportTable td:nth-child(5),
.reportTable td:nth-child(6),
.reportTable td:nth-child(8),
.reportTable td:nth-child(9),
.reportTable td:nth-child(10),
.reportTable td:nth-child(11) {
   width: 80px;
}

/* Cell appearance */
thead td {
    font-size: 13px;
    text-align:center;
}

tbody td {
    font-size: 13px;
    text-align:right;
}

/* Row Apperances */
.groupLabelRow td {
    border-bottom: 1px solid black;
}

/* Indentation of different grouping levels */
.parentRowHeader1 {
    padding-left: 3px;
    text-align: left;
    font-weight: bold;
}

.parentRowHeader2 {
    text-align: left;
    padding-left: 23px;
    font-weight: bold;
}

.parentRowHeader3 {
    padding-left: 43px;
    text-align: left;
    font-weight: bold;
}

.leafRowHeader1 {
    text-align: left;
    padding-left: 0;
}


.leafRowHeader2 {
    text-align: left;
    padding-left: 20px;
}


.leafRowHeader3 {
    text-align: left;
    padding-left: 40px;
}

.leafRowHeader4 {
    text-align: left;
    padding-left: 60px;
}

.leafRowHeader5 {
    text-align: left;
    padding-left: 80px;
}

.aggregatedRowHeader1 {
    font-weight: bold;
    text-align: right;
    padding-right: 5px;

}

.aggregatedRowHeader2 {
    font-weight: bold;
    text-align: right;
    padding-right: 20px;
}

.aggregatedRowHeader3 {
    font-weight: bold;
    text-align: right;
    padding-right: 35px;
}

.aggregatedRowHeader4 {
    font-weight: bold;
    text-align: right;
    padding-right: 50px;
}


