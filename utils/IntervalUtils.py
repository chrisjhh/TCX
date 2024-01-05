import numpy as np
from scipy.signal import savgol_filter
from ..TCXDocument import TCXDocument

def getDistanceArray(tcx: TCXDocument):
    da = []
    laps = tcx.activity.laps()
    for l in laps:
        d = [x.distance for x in l.trackpoints()]
        da.extend(d)
    return da

def getVelocityArray(tcx: TCXDocument):
    da = getDistanceArray(tcx)
    a = np.array(da)
    b = np.gradient(a)
    # Filter it
    w = savgol_filter(b, 31, 2)
    return w

def getIntervals(tcx: TCXDocument):
    """Return the intervals as an array of (index, distance, time, 1/0 for on/off)
    """
    # Get the velocity array
    w = getVelocityArray(tcx)
    min = np.min(w)
    max = np.max(w)
    mid = (min + max) / 2
    i = list(map(lambda v: 1 if v > mid else 0, w))
    a = getDistanceArray(tcx)
    lastValue = None
    lastDistance = 0
    lastTime = 0
    intervals = []
    for x in range(len(a)):
        val = i[x]
        if lastValue is not None and val != lastValue:
            distance = a[x]
            span = distance - lastDistance
            t = x - lastTime
            intervals.append((x, span, t, lastValue))
            lastDistance = distance
            lastTime = x
        lastValue = val

def intervalSession(tcx: TCXDocument):
    reps = getIntervals(tcx)

    rs = RepSet()
    effort = 0
    first = True
    for r in reps:
        # Ignore an intial recovery
        if r[3] == 0 and first:
            continue
        first = False
        if r[3] == 1:
            effort = r[1]
        else:
            recovery = r[1]
            rs.addRep(Rep(effort, recovery))
    return str(rs)

class Rep():
    def __init__(self, effort, recovery):
        self.effort = round(effort/50) * 50
        self.recovery = round(recovery/50) * 50
        self.repeats = 1

    def __eq__(self, other: object) -> bool:
        return self.effort == other.effort and self.recovery == other.recovery
    
    def __ne__(self, other: object) -> bool:
        return self.effort != other.effort or self.recovery != other.recovery
    
    def __str__(self) -> str:
        if self.repeats == 1:
            return "{}m {}R".format(self.effort, self.recovery)
        return "{} x {}m {}R".format(self.repeats, self.effort, self.recovery)
    
class RepSet():
    def __init__(self) -> None:
        self.repeats = 1
        self.recovery = None
        self.reps: list[Rep] = []

    def addRep(self, rep: Rep):
        if len(self.reps) == 0 or rep != self.reps[-1]:
            self.reps.append(rep)
        else:
            self.reps[-1].repeats += 1

    def __str__(self) -> str:
        return ", ".join(self.reps)