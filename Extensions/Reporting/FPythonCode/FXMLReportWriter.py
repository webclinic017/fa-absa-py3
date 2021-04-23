from __future__ import print_function
"""
   Efficient and safe production of XML that is conformant
   with the FRONT Reporting XML SCHEMA.

   2005-04-22 - Daniel R - Initial version, limited validation

"""

import cStringIO
import re


class _ElementProxy:
    def __init__(self, elem, writer):
        self.elem = elem
        self.writer = writer
    def __call__(self, textcontent=None):
        self.writer.start_tag(self)
        if textcontent:
            self.writer.add_text(textcontent)
        return self
    def done(self):
        """Close all open elements up to and including this one"""
        self.writer.close_tags_to(self)
        self.writer = None # we are finnished, prevent further operations

class _ElementDescriptor(object):
    def __init__(self, elemname):
        self.elemname = elemname
    def __get__(self, obj, objtype=None):
        return _ElementProxy(self.elemname, obj)

class FXMLWriter:
    """SAX style XML writer that validates against a schema while
       writing
    """

    translation_matcher = re.compile(r"([\s]*)(.*?)([\s]*)\Z")

    def __init__(self, outputhandler, schema=None, translatedict={}):
        """Iniitialize FAXMLReport

        outputhandler -- a SAX based XML writer, should perform full escaping
        schema        -- presently unused - planned, xmlshcema for validation
        translatedict -- optional dictionary object that provides table based
                         translation for all output
        """
        self._stack = []            # [(elem,ref)]
        self._out = outputhandler
        self._parent = None
        self._schema = schema
        self._translatedict = translatedict

    def make_file_writer(cls, fname, translatedict={}):
        """Construct an instance that writes to a file"""
        filehandle = open(fname, 'w')
        outputhandler = XMLWriter(filehandle)
        return cls(outputhandler, None, translatedict)
    make_file_writer = classmethod(make_file_writer)

    def make_iostring_writer(cls, translatedict={}):
        """Construct an instans that writes to an in memory string buff
           RETURNS writer, cIOString object
        """
        strbuf = cStringIO.StringIO()
        outputhandler = XMLWriter(strbuf)
        return cls(outputhandler, None, translatedict), strbuf
    make_iostring_writer = classmethod(make_iostring_writer)

    def start_tag(self, elem_cp):
        """Start an Element
            elem_cp -- an ElemCallProxy
        """
        self._out.start(elem_cp.elem)
        self._stack.append( elem_cp )

    def add_text(self, text):
        """Add text to the current element"""
        if not isinstance(text, str) and not isinstance(text, unicode):
            text = str(text) # handle various floats etc that might have been passed
        matched = self.__class__.translation_matcher.match(text)
        if matched:
            prewhite, word, postwhite = matched.groups()
            translatedword = self._translatedict.get(word, word)
            newtext = prewhite + translatedword + postwhite
            self._out.data(newtext)

    def end_tag(self):
        """Close currently open element"""
        elem_cp = self._stack.pop()
        if not elem_cp.writer:
            raise Exception("attempt to close tag that has already been closed")
        elem_cp.writer = None
        self._out.end()

    def close_tags_to(self, elem_cp):
        """Close all open tags up to ad including elem_cp"""
        while len(self._stack) and self._stack[-1] != elem_cp:
            self.end_tag()
        if len(self._stack):
            self.end_tag()

    def done(self):
        """Close all tags and flush to disk"""
        self.close_tags_to(None)

reportelems = """PRIMEReport Table Key Value ReportProperties 
Name Type Time LocalTime ReportContents TableProperties Property 
NumberOfColumns Columns Column ColumnId Label Rows Row RowId 
RowType Cells Cell RawData FormattedData FullData DefaultData"""

class FXMLReportWriter(FXMLWriter):
    def __init__(self, outputhandler, schema=None, translatedict={}):
        FXMLWriter.__init__(self, outputhandler, schema, translatedict)

# Add all Report elements onto FXMLReportWriter class
for elemname in reportelems.split(" "):
    elemname = elemname.strip()
    setattr(FXMLReportWriter, elemname, _ElementDescriptor(elemname))


#
# SimpleXMLWriter
# Id: //modules/elementtree/elementtree/SimpleXMLWriter.py#1 
#
# a simple XML writer
#
# history:
# 2001-12-28 fl   created
# 2002-11-25 fl   fixed attribute encoding
# 2002-12-02 fl   minor fixes for 1.5.2
#
# Copyright (c) 2001-2003 by Fredrik Lundh
#
# fredrik@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# The SimpleXMLWriter module is
#
# Copyright (c) 2001-2003 by Fredrik Lundh
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

import re, sys, locale, acm

try:
    unicode("")
except NameError:
    def encode(s, encoding):
        # 1.5.2: application must use the right encoding
        return s
    _escape = re.compile(r"[&<>\"\x80-\xff]+") # 1.5.2
else:
    def encode(s, encoding):
        languge, locale_encoding = locale.getdefaultlocale()
        if locale_encoding:
            u = s.decode(locale_encoding)
        else:
            u = s
        return u.encode(encoding)
    _escape = re.compile(eval(r'u"[&<>\"\u0080-\uffff]+"'))

def encode_entity(text, pattern=_escape):
    # map reserved and non-ascii characters to numerical entities
    def escape_entities(m):
        out = []
        for char in m.group():
            out.append("&#%d;" % ord(char))
        return "".join(out)
    return encode(pattern.sub(escape_entities, text), "ascii")

del _escape

#
# the following functions assume an ascii-compatible encoding
# (or "utf-16")

def escape_cdata(s, encoding=None):
    if re.search("[&<>]", s):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
    if encoding == "utf-8" and acm.IsUnicodeEnabled():
        return s
    elif encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)
    return s

def escape_attrib(s, encoding=None):
    s = s.replace( "&", "&amp;")
    s = s.replace( "'", "&apos;")
    s = s.replace( "\"", "&quot;")
    s = s.replace( "<", "&lt;")
    s = s.replace( ">", "&gt;")
    if encoding == "utf-8" and acm.IsUnicodeEnabled():
        return s
    elif encoding:
        try:
            return encode(s, encoding)
        except UnicodeError:
            return encode_entity(s)
    return s

class XMLWriter:

    def __init__(self, file, encoding="utf-8"):
        self.__write = file.write
        self.__open = 0 # true if start tag is open
        self.__tags = []
        self.__data = []
        self.__encoding = encoding
        self.__write( """<?xml version="1.0" encoding="utf-8" ?>""")


    def __flush(self):
        if self.__open:
            self.__write(">")
            self.__open = 0
        if self.__data:
            for data in self.__data:
                e = escape_cdata(data, self.__encoding)
                self.__write(e)
            self.__data = []

    def start(self, tag, attrib={}, **extra):
        self.__flush()
        tag = escape_cdata(tag, self.__encoding)
        self.__data = []
        self.__tags.append(tag)
        self.__write("<%s" % tag)
        if attrib or extra:
            attrib = attrib.copy()
            attrib.update(extra)
            attrib = attrib.items()
            attrib.sort()
            for k, v in attrib:
                k = escape_cdata(k, self.__encoding)
                v = escape_attrib(v, self.__encoding)
                self.__write(" %s=\"%s\"" % (k, v))
        self.__open = 1
        return len(self.__tags)-1

    def comment(self, comment):
        # add comment to output stream
        self.__flush()
        self.__write("<!-- %s -->\n" % escape_cdata(comment, self.__encoding))

    def data(self, text):
        # add data to output stream
        self.__data.append(text)

    def end(self, tag=None):
        if tag:
            assert self.__tags, "unbalanced end(%s)" % tag
            assert escape_cdata(tag, self.__encoding) == self.__tags[-1],\
                   "expected end(%s), got %s" % (self.__tags[-1], tag)
        else:
            assert self.__tags, "unbalanced end()"
        tag = self.__tags.pop()
        if self.__data:
            self.__flush()
        elif self.__open:
            self.__open = 0
            self.__write(" />")
            return
        self.__write("</%s>" % tag)

    def close(self, id):
        # close current element, and all elements up to
        # the one identified by the given identifier (as
        # returned by start)
        while len(self.__tags) > id:
            self.end()

    def element(self, xmltag, xmltext=None, xmlattrib={}, **xmlextra):
        # create a full element
        self.start(xmltag, xmlattrib, **xmlextra)
        if xmltext:
            self.data(xmltext)
        self.end()

if __name__ == '__main__':
    rep = FXMLReportWriter.make_file_writer("c:\\newtest.xml")
    print (dir(rep))
    pr = rep.PRIMEReport()
    rep.Row()
    t = rep.Table("kkk")
    t.done()
    pr.done()

