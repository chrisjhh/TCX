import unittest
import xml.etree.ElementTree as ET
from TCX.TCXFile import TCXFile
from .testData import getSwimData
from TCX.utils.SwimUtils import *

class TestSwimUtils(unittest.TestCase):

    def test_correction(self):
        # Load the data
        tcx = TCXFile(getSwimData())

        # Test the intial state
        laps = tcx.activity.laps()
        self.assertEqual(len(laps), 1)
        self.assertEqual(laps[0].distance, 525.0)
        self.assertEqual(laps[0].totalTime, 2247.0)
        self.assertEqual(len(laps[0].trackpoints()), 2244)

        # Split the lap into the actual laps by time
        times = ['21:15', '1:10', '4:11', '0:54', '4:18', '1:07', '4:22']
        SplitLapsByTimes(tcx, times)
        laps = tcx.activity.laps()
        self.assertEqual(len(laps), 8)
        expected =[
            (350.0, 1275),
            (0.0, 70),
            (25.0, 251),
            (0.0, 54),
            (50.0, 258),
            (0.0, 67),
            (100.0, 262),
            (0.0, 7)
        ]
        for i in range(len(expected)):
            dist, time = expected[i]
            self.assertEqual(laps[i].distance, dist)
            self.assertEqual(laps[i].totalTime, time)
            self.assertEqual(len(laps[i].trackpoints()), time)

        # Do the correction
        CorrectSwimmingTCX(tcx, 25, 33)
        laps = tcx.activity.laps()
        expected =[
            (1050.0, 1275),
            (0.0, 70),
            (200.0, 251),
            (0.0, 54),
            (200.0, 258),
            (0.0, 67),
            (200.0, 262),
            (0.0, 7)
        ]
        for i in range(len(expected)):
            dist, time = expected[i]
            self.assertEqual(laps[i].distance, dist)
            self.assertEqual(laps[i].totalTime, time)
            self.assertEqual(len(laps[i].trackpoints()), time)

