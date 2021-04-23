

"""----------------------------------------------------------------------------
MODULE
    FHTML - Utility functions when generating html reports 

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

def anchor(txt, ref = None):  
    if not ref:
        ref=txt
    return """<A NAME=%s>%s</A>""" % (ref.replace(' ', '_'), txt)

def ref(txt, ref = None):
    if not ref:
        ref=txt
    return """<a href="#%s">%s</a>""" % (ref.replace(' ', '_'), txt)

def b(txt):         return '<b>%s</b>' % txt

def i(txt):         return '<i>%s</i>' % txt    

def hilite(text, bg="ddddff", title = None):
    if title:
        title = title.replace('"', "&quot;")
        return '<font title="%s" style="background-color:%s">%s</font>'% (title, bg, text)    
    return '<font style="background-color:%s">%s</font>'% (bg, text)

def h2(txt):        return '<h2>%s</h2>' % txt

def h3(txt):        return '<h3>%s</h3>' % txt

def h4(txt):        return '<h4>%s</h4>' % txt

def fmtadfl(txt):       return txt # return "<code>" + txt + "</code>"

def html_link(txt, link): return '<A href="%s">%s</A>' %(link, txt)

def html_link_noUL(txt, link): return '<A STYLE="text-decoration:none" href="%s">%s</A>' %(link, txt)

def html_link_button(txt, link): return '<button onClick="window.location=\'%s\'" >%s</button>' %(link, txt)

def html_link_button1(txt, link): 
    return '<FORM><INPUT TYPE="BUTTON" VALUE="%s" ONCLICK="window.location.href=\'%s\'"></FORM>' %(txt, link)

#def html_drop_down_menu(menu_list, execute_button = 'Go'):    
#    return_string = ['<FORM ACTION="../cgi-bin/redirect.pl" METHOD=POST onSubmit="return dropdown(this.gourl)">']
#    return_string.append('<SELECT NAME="gourl">')
#    
#    for menu in menu_list:
#        return_string.append('<OPTION VALUE="' + menu[0] + '">' + menu[1])
#
#    return_string.append('</SELECT> <INPUT TYPE=SUBMIT VALUE="' + execute_button + '"></FORM>')
#
#    return "\n".join(return_string)
    
    
def html_drop_down_menu(menu_list, name, execute_button = 'Go'):    
    return_string = ['<FORM NAME="'+ name +'" METHOD="POST" ACTION=URI>']
    return_string.append('<SELECT NAME="gourl">')
    
    for menu in menu_list:
        return_string.append('<OPTION VALUE="' + menu[0] + '">' + menu[1] + '</OPTION>')

    return_string.append('</SELECT> <INPUT TYPE ="button" onClick="location =')
    return_string.append('document.'+ name +'.gourl.options [document.'+ name +'.gourl.selectedIndex].value;"')
    return_string.append('value="' + execute_button + '"></FORM>')

    return "\n".join(return_string)
    
    
    
    
    
def update_tag(type, txt):
    if type == "ExtensionAttribute":
        return "<!-- Add update link for extension " + txt + "-->"
    if type == "ExtensionModule":
        return "<!-- Add update link for module " + txt + "-->"
    if type == "OneExtensionFromList":
        return "<!-- Add update drop down menu for module " + txt + "-->"
def get_update_tag(type):
    if type == "ExtensionAttribute":
        return "<!-- Add update link for extension ", "-->"
    if type == "ExtensionModule":
        return "<!-- Add update link for module ", "-->"
    if type == "OneExtensionFromList":
        return "<!-- Add update drop down menu for module ", "-->"




