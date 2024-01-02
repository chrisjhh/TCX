"""Class representing an Activity node of a TCX document"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName
from .TCXTraining import TCXTraining
from .TCXCreator import TCXCreator
from .TCXLap import TCXLap

class TCXActivity(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "Activity":
            raise TCXFormatError("Unexpected Activity tag {}".format(unqualifiedName(element.tag)))
        
    @property
    def sport(self):
        return self.getroot().get("Sport")

    @sport.setter
    def sport(self, value):
        self.getroot().set("Sport", value)

    @property
    def id(self):
        el = self.find("{*}Id")
        if el is None:
            raise TCXFormatError("No Activity Id element found")
        return el.text
    
    @id.setter
    def id(self, value):
        el = self.find("{*}Id")
        if el is None:
            raise TCXFormatError("No Activity Id element found")
        el.value = value

    @property 
    def training(self):
        el = self.find("{*}Training")
        if el is None:
            # This may be valid
            return None
        return TCXTraining(el)
    
    @property 
    def creator(self):
        el = self.find("{*}Creator")
        if el is None:
            # This may be valid
            return None
        return TCXCreator(el)

    def laps(self):
        parent = self.getroot()
        return [TCXLap(l,parent) for l in self.findall("{*}Lap")]