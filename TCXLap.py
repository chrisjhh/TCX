"""Class representing a Lap node of a TCX document"""

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName
from .TrackpointContainer import TrackpointContainer

class TCXLap(ET.ElementTree, TrackpointContainer):

    def __init__(self, element: ET.Element, parent: ET.Element=None):
        """Parent is needed to split laps"""
        super().__init__(element)
        self.parent = parent
        if unqualifiedName(element.tag) != "Lap":
            raise TCXFormatError("Unexpected Lap tag {}".format(unqualifiedName(element.tag)))
        
    @property
    def distance(self):
        dist = self.find("{*}DistanceMeters")
        if dist is None:
            return 0.0
        return float(dist.text)

    @distance.setter
    def distance(self, value):
        dist = self.find("{*}DistanceMeters")
        if dist is None:
            dist = ET.SubElement(self.getroot(), "DistanceMeters")
        dist.text = str(float(value))

    @property
    def totalTime(self):
        time = self.find("{*}TotalTimeSeconds")
        if time is None:
            return 0.0
        return float(time.text)

    @totalTime.setter
    def totalTime(self, value):
        time = self.find("{*}TotalTimeSeconds")
        if time is None:
            time = ET.SubElement(self.getroot(), "TotalTimeSeconds")
        time.text = str(float(value))

    @property
    def maximumSpeed(self):
        el = self.find("{*}MaximumSpeed")
        if el is None:
            return None
        return float(el.text)

    @maximumSpeed.setter
    def maximumSpeed(self, value):
        el = self.find("{*}MaximumSpeed")
        if el is None:
            el = ET.SubElement(self.getroot(), "MaximumSpeed")
        el.text = str(float(value))

    @property
    def calories(self):
        el = self.find("{*}Calories")
        if el is None:
            return None
        return int(el.text)
    
    @calories.setter
    def calories(self, value):
        el = self.find("{*}Calories")
        if el is None:
            el = ET.SubElement(self.getroot(), "Calories")
        el.text = str(int(value))

    @property
    def averageHeartRate(self):
        hr = self.find("{*}AverageHeartRateBpm/{*}Value")
        if hr is None:
            return None
        return int(hr.text)

    @averageHeartRate.setter
    def averageHeartRate(self, value):
        hr = self.find("{*}AverageHeartRateBpm")
        if hr is None:
            hr = ET.SubElement(self.getroot(), "AverageHeartRateBpm")
        val = hr.find("{*}Value")
        if val is None:
            val = ET.SubElement(hr, "Value")
        val.text = str(int(value))

    @property
    def maximumHeartRate(self):
        hr = self.find("{*}MaximumHeartRateBpm/{*}Value")
        if hr is None:
            return None
        return int(hr.text)

    @maximumHeartRate.setter
    def maximumHeartRate(self, value):
        hr = self.find("{*}MaximumHeartRateBpm")
        if hr is None:
            hr = ET.SubElement(self.getroot(), "MaximumHeartRateBpm")
        val = hr.find("{*}Value")
        if val is None:
            val = ET.SubElement(hr, "Value")
        val.text = str(int(value))

    @property
    def intensity(self):
        el = self.find("{*}Intensity")
        if el is None:
            return None
        return el.text
    
    @intensity.setter
    def intensity(self, value: str):
        el = self.find("{*}Intensity")
        if el is None:
            el = ET.SubElement(self.getroot(), "Intensity")
        el.text = value
    
    @property
    def cadence(self):
        el = self.find("{*}Cadence")
        if el is None:
            return None
        return int(el.text)
    
    @property
    def triggerMethod(self):
        el = self.find("{*}TriggerMethod")
        if el is None:
            return None
        return el.text
    
    @property
    def averageSpeed(self):
        el = self.find("{*}Extensions/{*}LX/{*}AvgSpeed")
        if el is None:
            return None
        return float(el.text)
    
    @property
    def averagePower(self):
        el = self.find("{*}Extensions/{*}LX/{*}AvgWatts")
        if el is None:
            return None
        return int(el.text)
    
    @property
    def maximumPower(self):
        el = self.find("{*}Extensions/{*}LX/{*}MaxWatts")
        if el is None:
            return None
        return int(el.text)