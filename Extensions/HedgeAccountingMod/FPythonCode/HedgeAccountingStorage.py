'''
===================================================================================================
PURPOSE: This module manages Text Object operations including functions to save and retrieve
            Hedge Effectiveness Text Objects from the database and also include XML helper
            functions in order to update the Hedge Relationship XML in the Text Object.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import acm
import ael
import FLogger

LOGGER = FLogger.FLogger(__name__)


class TextObjectManager(object):
    """class for managing text object"""

    @classmethod
    def get_textobject(cls, name, m_type):
        return ael.TextObject.read('type="%s" and name="%s"' % (m_type, name))

    @classmethod
    def get_acm_textobject(cls, name, m_type):
        return acm.FCustomTextObject.Select01('cid="%s" and name="%s"' % (m_type, name),
                                              'No text object named %s' % name)

    @classmethod
    def set_textobject(cls, name, m_type, text):
        textObject = TextObjectManager.get_textobject(name, m_type)
        if textObject:
            if text:
                textObject_clone = textObject.clone()
                textObject_clone.data = text
                textObject_clone.commit()
            else:
                textObject.delete()
            ael.poll()
        else:
            if text:
                textObject = ael.TextObject.new()
                textObject.name = name
                textObject.type = m_type
                textObject.data = text
                # commit the text object with temp Oid in name
                textObject.commit()

                # reset name with persisted Oid
                textObject.name = '{0}{1}'.format(name, textObject.seqnbr)

                # Update TextObject with persisted Oid in the Name
                textObject.commit()
                ael.poll()

        return textObject

    @classmethod
    def del_textobject(cls, name, m_type):
        textObject = cls.get_textobject(name, m_type)
        if textObject:
            try:
                textObject.delete()
                ael.poll()
            except:
                LOGGER.ELOG("ERROR. Unable to delete.")


def get_element_tag_value(node2, tag):
    elements = get_elements(node2, tag)
    if not elements:
        return ""
    element = elements[0]
    rc = []
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return str(''.join(rc))


def set_element_tag_value(xml, node, tag, value):

    elements = get_elements(node, tag)
    if elements:
        element = elements[0]
        childNodes = element.childNodes
        if not childNodes:
            data = xml.createTextNode(str(value))
            element.appendChild(data)
        else:
            for c_node in element.childNodes:
                c_node.data = value
    else:
        tag = xml.createElement(tag)
        data = xml.createTextNode(str(value))
        tag.appendChild(data)
        node.appendChild(tag)


def append_element_with_value(xml, node, tag, value):
    '''Append new xml element to 'node' with name 'tag' and text set to 'value'
        xml -- [xml DOM object]
        node -- [xml DOM Node object]
        tag -- [string] name of new child node
        value -- [object] string value of object will to be stored in new child node
    '''

    tag = xml.createElement(tag)
    data = xml.createTextNode(str(value))
    tag.appendChild(data)
    node.appendChild(tag)


def get_elements(node, tag):
    result = []
    try:
        for child in node.childNodes:
            if child.tagName == tag:
                result.append(child)
        return result
    except:
        return result
