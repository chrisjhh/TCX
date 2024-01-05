from ..TCXLap import TCXLap
from ..TCXDocument import TCXDocument

def PoolLapIndexes(lap: TCXLap, poolLength: float):
    points = lap.trackpoints()
    last_distance = points[0].distance
    indexes = []
    for i in range(len(points)):
        point = points[i]
        dist = point.distance
        if int(dist) % poolLength != 0:
            continue
        if dist != last_distance:
            indexes.append(i)
            last_distance = dist
    return indexes


def CorrectedPoolLapIndexes(lap: TCXLap, poolLength: float, targetTime: float):
    indexes = PoolLapIndexes(lap, poolLength)
    # See if we are missing an index at the end
    maxIndex = len(lap.trackpoints()) - 1
    endIndex = indexes[-1] if len(indexes) > 0 else 0
    if maxIndex - endIndex > 0.6*targetTime:
        # Add another lap at the end
        indexes.append(maxIndex)
    corrected = []
    last_index = 0
    for i in indexes:
        gap = i - last_index
        # See if correction needed
        if gap > 1.5*targetTime:
            laps = round(gap/targetTime)
            interval = float(gap) / laps
            for x in range(laps - 1):
                corrected.append(round(last_index + interval * (x+1)))
        corrected.append(i)
        last_index = i
    return corrected

def ApplyCorrectedPoolLapIndexes(lap: TCXLap, indexes: list[int], poolLength: float, startingDistance: float):
    dist = startingDistance
    points = lap.trackpoints()
    for i in range(len(points)):
        if i in indexes:
            dist += poolLength
        points[i].distance = dist
    lapDist = dist - startingDistance
    lap.distance = lapDist
    return dist

def SetAllDistances(lap: TCXLap, dist: float):
    points = lap.trackpoints()
    for i in range(len(points)):
        points[i].distance = dist
    lap.distance = 0

def CorrectLaps(laps: list[TCXLap], poolLength: float, targetTime: float):
    dist = 0
    lastLapZero = False
    for lap in laps:
        if lap.distance == 0 and not lastLapZero:
            SetAllDistances(lap, dist)
            lastLapZero = True
            continue
        for i in (0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, 0):
            target = targetTime + i
            indexes = CorrectedPoolLapIndexes(lap, poolLength, target)
            if len(indexes) % 2 == 0:
                break
        dist = ApplyCorrectedPoolLapIndexes(lap, indexes, poolLength, dist)
        lastLapZero = False

def SplitLapsByTimes(tcx: TCXDocument, times: list[str]):
    """Split laps by list of times in 'mm:ss' format"""
    # Combine into single lap if not already
    laps = tcx.activity.laps()
    while len(laps) > 1:
        lap1 = laps[0]
        lap2 = laps[1]
        lap1.mergeWith(lap2)
        laps = tcx.activity.laps()
    # Now split them by the times 
    for t in times:
        (m, s) = t.split(':')
        secs = int(m) * 60 + int(s)
        laps = tcx.activity.laps()
        lastLap = laps[-1]
        lastLap.splitAtIndex(secs)

def CorrectSwimmingTCX(tcx: TCXDocument, poolLength: float, targetTime: float):
    tcx.activity.sport = "Swimming"
    laps = tcx.activity.laps()
    CorrectLaps(laps, poolLength, targetTime)
