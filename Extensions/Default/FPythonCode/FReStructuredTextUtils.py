
import sys
import acm
from docutils import core, io, languages

def getStyleSheet():
    ctx = acm.GetDefaultContext()
    cssObject = ctx.GetExtension('FXSLTemplate', 'FObject', 'AEFBrowserCSS')
    if cssObject :
        return [cssObject.Value()]
    
    return [''] #no stylesheet found

def rstToHtml(rst): 
    try:
        output, pub = core.publish_programmatically(
                source=rst, source_path=None, source_class=io.StringInput,
                destination_class=io.StringOutput,
                destination=None, destination_path=None,
                reader=None, reader_name='standalone',
                parser=None, parser_name='restructuredtext',
                writer=None, writer_name='html',
                settings=None, settings_spec=None,
                settings_overrides=None,
                config_section=None,
                enable_exit_status=None)


        pub.writer.document = pub.document
        pub.writer.language = languages.get_language(pub.document.settings.language_code)
        pub.writer.destination = pub.destination

        res = ''.join(pub.writer.head_prefix + pub.writer.head
                               + getStyleSheet() + pub.writer.body_prefix
                               + pub.writer.body_pre_docinfo + pub.writer.docinfo
                               + pub.writer.body + pub.writer.body_suffix) 
                               
        res = pub.destination.write(res)
    
    except:
        print (sys.exc_info())
        res = "Unable to generate html"
        
    return res
