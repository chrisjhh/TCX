"""Class representing the Activities node of a TCX document"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName
from .TCXActivity import TCXActivity

class TCXActivities(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "Activities":
            raise TCXFormatError("Unexpected Activities tag {}".format(unqualifiedName(element.tag)))
        
    def __getitem__(self, key) -> TCXActivity:
        return TCXActivity(self.getroot()[key])
    
    def __len__(self) -> int:
        return len(self.getroot())