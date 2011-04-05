"""
some helper methods for XML handling
"""

from types import StringTypes


def setAttr(doc, node, key, value):
    """ little helper to abbrev. the process of setting an XML-Attribute """
    if type(value) not in StringTypes:
        value = repr(value)

    attr = doc.createAttribute(key)
    node.setAttributeNode(attr)
    node.setAttribute(key, value)
    return attr


def appendNode(doc, parent, key):
    """ little helper to abbrev. the process of creating a simple node """
    node = doc.createElement(key)
    parent.appendChild(node)
    return node


def appendText(doc, parent, key, content):
    """ little helper to abbrev. the process of creating a text-node """
    node = appendNode(doc, parent, key)
    textnode = doc.createTextNode(content)
    node.appendChild(textnode)
    return node


def getData(parent):
    data = ""
    for child in parent.childNodes:
        if child.data:
            data+=child.data.strip()
    return data


def getCDATA(parent):
    cdatanode = [child for child in parent.childNodes if child.nodeType == child.CDATA_SECTION_NODE]
    if cdatanode and len(cdatanode)>0:
        return cdatanode[0].data

    # may be we have a old/buggy xml implementation:
    # it can handle CDATA Nodes, but return it as a textnode
    return getData(parent)


def getChildrenByTagName(parent, name):
    nodes = []
    for child in parent.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == name:
                nodes.append(child)
    return nodes

#backward - check if needed
getNodes = getChildrenByTagName
