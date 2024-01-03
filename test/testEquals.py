import xml.etree.ElementTree as ET

class ElementDifference(Exception):
    pass

def testEquals(el1: ET.Element, el2: ET.Element):
    if el1.tag != el2.tag:
        raise ElementDifference("Tag names are different. {} != {}".format(el1.tag, el2.tag))
    text1 = el1.text.strip() if el1.text else ""
    text2 = el2.text.strip() if el2.text else ""
    if text1 != text2:
        raise ElementDifference("Text values of <{}> are different. {} != {}".format(el1.tag, text1, text2))
    if el1.attrib != el2.attrib:
        raise ElementDifference("Attributes of <{}> are different. {} != {}".format(el1.tag, el1.attrib, el2.attrib))
    if len(el1) != len(el2):
        raise ElementDifference("Number of children of <{}> are different.{} != {}".format(el1.tag, len(el1), len(el2)))
    for i in range(len(el1)):
        testEquals(el1[i], el2[i])                            