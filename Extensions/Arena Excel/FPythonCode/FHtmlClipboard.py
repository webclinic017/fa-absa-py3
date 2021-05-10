""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/FHtmlClipboard.py"
import FClipboard


class HtmlClipboard(object):

    GMEM_DDESHARE = 0x2000 

    MARKER_BLOCK_OUTPUT = (
        'Version:1.0\r\n'
        'StartHTML:%09d\r\n'
        'EndHTML:%09d\r\n'
        'StartFragment:%09d\r\n'
        'EndFragment:%09d\r\n'
        )

    HTML_BODY = (
        '<html xmlns:o="urn:schemas-microsoft-com:office:office"'
        'xmlns:x="urn:schemas-microsoft-com:office:excel"'
        'xmlns="http://www.w3.org/TR/REC-html40">\r\n'
        '<body>\r\n'
        '<!--StartFragment-->\r\n'
        '%s\r\n'
        '<!--EndFragment-->\r\n'
        '</body>\r\n'
        '</html>'
        )

    def Copy(self, text):
        self._SetClipboardText(self.GetSource(text))
        
    def GetSource(self, text):
        html = self.HTML_BODY % text
        fragmentStart = html.index(text)
        fragmentEnd = fragmentStart + len(text)
        return self._EncodeClipboardSource(html, fragmentStart, fragmentEnd)

    def _SetClipboardText(self, source):
        FClipboard.Copy(source, FClipboard.CF_HTML)

    def _EncodeClipboardSource(self, html, fragmentStart, fragmentEnd):
        dummyPrefix = self.MARKER_BLOCK_OUTPUT % (0, 0, 0, 0)
        lenPrefix = len(dummyPrefix)
        prefix = self.MARKER_BLOCK_OUTPUT % (
            lenPrefix, 
            len(html)+lenPrefix,
            fragmentStart+lenPrefix, 
            fragmentEnd+lenPrefix
            )
        return (prefix + html)


def Copy(text):
    cb = HtmlClipboard()
    cb.Copy(text)
