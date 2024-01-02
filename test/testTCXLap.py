
import unittest
import xml.etree.ElementTree as ET
from TCX.TCXLap import TCXLap
from .testData import getIntervalData

class TestTCXDocument(unittest.TestCase):

    def setUp(self):
        filename = getIntervalData()
        with open(filename) as tcx:
            data = tcx.read()
        data = data.strip()
        root = ET.fromstring(data)
        self.lap = root.find("{*}Activities/{*}Activity/{*}Lap")

    def test_ElementAccess(self):
        lap = TCXLap(self.lap)
        track = lap.find("{*}Track")
        self.assertTrue(isinstance(track, ET.Element))

    def test_distance(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.distance, 194.0)

    def test_distance_setter(self):
        lap = TCXLap(self.lap)
        lap.distance = 200.1
        self.assertEqual(lap.getroot().find("{*}DistanceMeters").text, "200.1")
        self.assertEqual(lap.distance, 200.1)
        lap.distance = 194.0
        self.assertEqual(lap.getroot().find("{*}DistanceMeters").text, "194.0")
        self.assertEqual(lap.distance, 194.0)

    def test_totalTime(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.totalTime, 44.0)

    def test_totalTime_setter(self):
        lap = TCXLap(self.lap)
        lap.totalTime = 46.1
        self.assertEqual(lap.getroot().find("{*}TotalTimeSeconds").text, "46.1")
        self.assertEqual(lap.totalTime, 46.1)
        lap.totalTime = 44.0
        self.assertEqual(lap.getroot().find("{*}TotalTimeSeconds").text, "44.0")
        self.assertEqual(lap.totalTime, 44.0)

    def test_maximumSpeed(self):
        lap = TCXLap(self.lap)
        self.assertAlmostEqual(lap.maximumSpeed, 5.073, places=3)

    def test_maximumSpeed_setter(self):
        lap = TCXLap(self.lap)
        originalValue = lap.maximumSpeed
        lap.maximumSpeed = 6.1
        self.assertEqual(lap.getroot().find("{*}MaximumSpeed").text, "6.1")
        self.assertEqual(lap.maximumSpeed, 6.1)
        # Restore original value
        lap.maximumSpeed = originalValue
        self.assertAlmostEqual(lap.maximumSpeed, 5.073, places=3)

    def test_averageHeartRate(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.averageHeartRate, 101)

    def test_averageHeartRate_setter(self):
        lap = TCXLap(self.lap)
        lap.averageHeartRate = 120
        self.assertEqual(lap.getroot().find("{*}AverageHeartRateBpm/{*}Value").text, "120")
        self.assertEqual(lap.averageHeartRate, 120)
        lap.averageHeartRate = 101
        self.assertEqual(lap.getroot().find("{*}AverageHeartRateBpm/{*}Value").text, "101")
        self.assertEqual(lap.averageHeartRate, 101)

    def test_maximumHeartRate(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.maximumHeartRate, 125)

    def test_maximumHeartRate_setter(self):
        lap = TCXLap(self.lap)
        lap.maximumHeartRate = 130
        self.assertEqual(lap.getroot().find("{*}MaximumHeartRateBpm/{*}Value").text, "130")
        self.assertEqual(lap.maximumHeartRate, 130)
        lap.maximumHeartRate = 125
        self.assertEqual(lap.getroot().find("{*}MaximumHeartRateBpm/{*}Value").text, "125")
        self.assertEqual(lap.maximumHeartRate, 125)

    def test_calories(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.calories, 640)

    
if __name__ == "__main__":
    unittest.main()