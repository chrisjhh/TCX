"""Class representing the Training node of a TCX activity"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName

class TCXTraining(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "Training":
            raise TCXFormatError("Unexpected Training tag {}".format(unqualifiedName(element.tag)))
        