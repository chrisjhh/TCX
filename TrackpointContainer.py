"""Mixin class for elements containing Trackpoints"""
from .TCXTrackpoint import TCXTrackpoint
import xml.etree.ElementTree as ET

class TrackpointContainer:
      
    def trackpoints(self: ET.ElementTree):
        return [TCXTrackpoint(t) for t in self.findall(".//{*}Trackpoint")]

    def polyline(self):
        pl = []
        points = self.trackpoints()
        for p in points:
            pos = p.position()
            if pos is not None:
                pl.append(pos)
        return pl