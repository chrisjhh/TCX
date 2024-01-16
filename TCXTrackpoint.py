"""Class representing a TrackPoint node of a TCX document"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName

class TCXTrackpoint(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "Trackpoint":
            raise TCXFormatError("Unexpected Lap tag {}".format(unqualifiedName(element.tag)))
        
    @property
    def distance(self):
        dist = self.find("{*}DistanceMeters")
        if dist is None:
            return 0
        return float(dist.text)

    @distance.setter
    def distance(self, value):
        dist = self.find("{*}DistanceMeters")
        if dist is not None:
            dist.text = str(float(value))
        else:
            if float(value) == 0.0:
                # Nothing needs to be done
                return
            # Add subelement and set distance in this
            dist = ET.SubElement(self.getroot(), "DistanceMeters")
            dist.text = str(float(value))

    @property
    def cadence(self):
        cad = self.find("{*}Cadence")
        if cad is None:
            return None
        return int(cad.text)

    def position(self):
        pos = self.find("{*}Position")
        if pos is None:
            return None
        lat = pos.find("{*}LatitudeDegrees")
        lon = pos.find("{*}LongitudeDegrees")
        if lat is None or lon is None:
            return None
        return (float(lat.text), float(lon.text))