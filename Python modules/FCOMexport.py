""" ConsolidatedRisk:1.0.0 """

"""-----------------------------------------------------------------------------
MODULE	    	FCOMexport

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

Version:    2.1.1

DESCRIPTION
    This function is used from other AEL-modules to export data and graphs to excel.
    
    The python library win32com.client is needed to run this module. You should also
    give the path to where this library is placed on your PC. 
    Ex. c:\\Program Files\\Python\\win32com\\client    
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
#import sys
#sys.path.append('c:\\Program Files\\Python\\win32com\\client')
try:
    import win32com
except:
    print 'Warning, extension module win32com not found'
try:
    import pythoncom
except:
    print 'PythonCom package not found'
import string
import win32com.client

#
#   This function initializes export to excel.
#
def ExportIni():

    #print 'Initializing export...'
    global rowlist
    global columns
    rowlist=[]
    columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'\
    	    , 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG'\
	    , 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU'\
	    , 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG'\
	    , 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU'\
	    , 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG'\
	    , 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU'\
	    , 'CV', 'CW', 'CX', 'CY', 'CZ']
    return ''
    
#   
#   This function exports figures to excel.   
#
def ExportFigures(xlww, data, labels, legend_list):

    try:
	nofc=0
	if labels != None:
    	    temp=[labels, data[0], data[1]]
	    data=temp
	for x in range(len(data)):
    	    for y in range(len(data[x])):
		xlww.Range(ComputeRange(x, y)).Value=(data[x][y])
	    nofc=nofc+1
	    rowlist.append(y+1)
    	
	# Adjust the width of the columns	
	endcolumn=columns[nofc-1]
	col=xlww.Columns("A:" + endcolumn)
	col.EntireColumn.AutoFit()
	col=xlww=None

	# Find out the range for the chart and return it
	a=0
	for x in rowlist:
    	    if x>a:
		a=x
	sa="%s" % a
	if labels != None:
	    entire_range=[str('B1:' + endcolumn + sa), str('A1:' + endcolumn + sa)]
	else:
    	    entire_range=[str('A1:' + endcolumn + sa)]
	return entire_range
    except:
    	print 'Failed to export figures'
	col=xlww=None
	return ''
    
#
#   This function calculates the range of all data.
#
def ComputeRange(listx, number):

    try:
	number=number+1
	column=columns[listx]
	snumber="%s" %number
	range=column+snumber
	return range
    except:
    	print 'Failed to compute range'
	return ''
    
#
#   This function creates charts in excel.
#
def CreateChart(xl, xlww, entire_range, settings, title, xlabel, ylabel, labels, legend_list):
    
    try:
	gallerylist=[1, 2, 3, 4, 5, -4151, -4169, -4111, -4098, -4099, -4100, -4101
    	    		-4102, -4103, -4120, -1]
	xlwRows=1
	xlwColumns=2		    
	plotbylist=[xlwRows, xlwColumns]
	sourcerange=xlww.Range(entire_range[0])
        xlc=xl.Charts.Add()
    	xlc.Activate()
	if settings == 3 and legend_list == 1:
    	    xlc.ChartWizard(Source=sourcerange, Gallery=gallerylist[settings], 
    	        	    Format=None, PlotBy=plotbylist[1], CategoryLabels=1,
		    	    SeriesLabels=1, HasLegend=1)	
    	else:
    	    xlc.ChartWizard(Source=sourcerange, Gallery=gallerylist[settings], 
    	        	    Format=None, PlotBy=plotbylist[1], CategoryLabels=1,
		    	    SeriesLabels=None, HasLegend=0)
	xlc.ChartGroups(1).GapWidth=0
	xlc.ChartGroups(1).Overlap=100
	xlc.HasTitle=1
	xlc.ChartTitle.Characters.Text=title	
	if settings == 6:
	    totalrange=xlww.Range(entire_range[1])
	    xl.Charts(1).SeriesCollection(1).HasDataLabels='True'
	    for i in range(totalrange.Rows.Count):
		xlc.SeriesCollection(1).Points(i+1).DataLabel.Text=totalrange.Cells(i+1, 1).Value
		xlc.SeriesCollection(1).Points(i+1).DataLabel.Font.Name='Arial'
		xlc.SeriesCollection(1).Points(i+1).DataLabel.Font.Size=8
	xlc=xlww=sourcerange=totalrange=None
	return 'ok'
    except:
	print 'Failed to create chart'
	xl=xlc=xlww=sourcerange=p=None
	return ''


#
#   This function checks if any interface is alive.
#
def CheckClean():

    interfaces = pythoncom._GetInterfaceCount()
    if interfaces:
    	print 'Warning - %d com interface objects still alive' % interfaces    

#
#   This is the main function that coordinates the exportation to excel.
# 
def Export_To_Excel(o,settings,data,title,xlabel,ylabel,legend_list,*rest):
    
    ExportIni()
    CheckClean()

    pythoncom.CoInitialize()

    
    try:
    	try:
	    xl=win32com.client.Dispatch("Excel.Application")
    	except:
	    import win32com
	    xl = win32com.client.Dispatch("Excel.Application")
    	xl.Visible=1
    	xlw=xlww=xl
    	if string.atoi(xl.Version[0])>=8:   
    	    xlw=xl.Workbooks.Add()
	    xlww=xlw.Worksheets(1)
    	else:
    	    xlw=xl.Workbooks().Add()
	    xlww=xlw.Worksheets(1)
    
    	labels=[]
    	if settings == 6:
	    labels=data[0]
	    temp=[data[1], data[2]]
	   
	    entire_range=ExportFigures(xlww, temp, labels, legend_list)
    	else:
	    
	    entire_range=ExportFigures(xlww, data, None, legend_list)
    	if entire_range != '':
    	    CreateChart(xl, xlww, entire_range, settings, title, xlabel, ylabel, labels, legend_list)
    	xl.Visible=1
    except:
    	print 'COMexport failed.'
        xlw=xlww=xl=None

    xlw=xlww=xl=None
    CheckClean()
    rowlist=[]
    columns=[]

    pythoncom.CoUninitialize()

    
    return ''

