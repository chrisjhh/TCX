"""Class representing the Author node of a TCX document"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName

class TCXAuthor(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "Author":
            raise TCXFormatError("Unexpected Author tag {}".format(unqualifiedName(element.tag)))
        
    @property
    def name(self) -> str:
        el = self.find("{*}Name")
        if el is None:
            raise TCXFormatError("No Name element found for Author")
        return el.text