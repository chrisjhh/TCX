import xml.etree.ElementTree as ET
from typing import IO

def outputElement(el: ET.Element, stream: IO, ns:str=None, offset:str=""):
    tag = el.tag
    namespace=None
    if '}' in tag:
        (namespace, tag) = tag.split("}")
        namespace = namespace.replace("{", "")
    stream.write(offset)
    stream.write("<{}".format(tag))
    for key, value in el.attrib.items():
        if '}' in key:
            (xsi, key) = key.split("}")
            xsi = xsi.replace("{", "")
            key = "xsi:" + key
            stream.write(" {}=\"{}\"".format("xmlns:xsi", xsi))
        stream.write(" {}=\"{}\"".format(key, value))
    if namespace and namespace != ns:
        stream.write(" {}=\"{}\"".format("xmlns", namespace))
    if not len(el) and not el.text:
        stream.write("/>\n")
        return
    stream.write(">")
    if len(el):
        stream.write("\n")
        for child in el:
            outputElement(child, stream, namespace, offset + "  ")
        stream.write(offset)
    elif el.text:
        stream.write(el.text)
    stream.write("</{}>\n".format(tag))