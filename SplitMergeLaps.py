import xml.etree.ElementTree as ET
import copy
from typing import Protocol
from .TCXTrackpoint import TCXTrackpoint
from .errors import TCXFormatError

class TCXSplitMergeError(Exception):
    pass

# Get prompts without circular include
class LapLike(Protocol):
    def findall(self, path: str, namespaces: dict[str, str] | None = None) -> list[ET.Element]: ...
    def find(self, path: str, namespaces: dict[str, str] | None = None) -> (ET.Element | None): ...
    def getroot(self) -> ET.Element: ...
    def trackpoints(self) -> list[TCXTrackpoint]: ...
    def distance(self) -> float: ...
    def totalTime(self) -> float: ...
    def indexOfDistance(self, distance: float) -> int: ...
    def truncate(self, index: int) -> None: ...
    def trimStart(self, index: int) -> None: ...

def mergeLaps(activity: ET.Element, lap1: LapLike, lap2: LapLike):
    if not lap1.getroot() in activity or not lap2.getroot() in activity:
        raise Exception("Laps not in activity")
    track = lap1.find("{*}Track")
    if track is None:
        raise TCXFormatError("No Track subelement of Lap")
    trackpoints = lap2.trackpoints()
    for point in trackpoints:
        track.append(point.getroot())
    lap1.distance = lap1.distance + lap2.distance
    lap1.totalTime = lap1.totalTime + lap2.totalTime
    activity.remove(lap2.getroot())

def splitLap(activity: ET.Element, lap: LapLike, index: int):
        # Find index of lap
        lapIndex = None
        i = 0
        for el in activity:
            if el == lap.getroot():
                lapIndex = i
                break
            i += 1
        if lapIndex is None:
            raise TCXSplitMergeError("Laps not in activity")
        # Make a deepcopy
        lap2 = copy.deepcopy(lap)
        # Insert it after original lap
        activity.insert(lapIndex + 1, lap2.getroot())
        # Strip out the uneeded track points and update distance and times
        lap.truncate(index)
        lap2.trimStart(index)

def splitLapAtDistance(activity: ET.Element, lap: LapLike, distance: float):
    index = lap.indexOfDistance(distance)
    if index == -1:
        raise TCXSplitMergeError("Insufficient distance in lap to split at this value")
    splitLap(activity, lap, index)