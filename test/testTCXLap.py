
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
        self.assertEqual(lap.find("{*}DistanceMeters").text, "200.1")
        self.assertEqual(lap.distance, 200.1)
        lap.distance = 194.0
        self.assertEqual(lap.find("{*}DistanceMeters").text, "194.0")
        self.assertEqual(lap.distance, 194.0)

    def test_distance_create(self):
        # Remove the distance element and check it is recreated by setter
        lap = TCXLap(self.lap)
        dist = lap.distance
        el = lap.find("{*}DistanceMeters")
        lap.getroot().remove(el)
        self.assertEqual(lap.distance, 0)
        self.assertIsNone(lap.find("{*}DistanceMeters"))
        lap.distance = dist
        self.assertEqual(lap.find("{*}DistanceMeters").text, "194.0")
        self.assertEqual(lap.distance, 194.)

    def test_totalTime(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.totalTime, 44.0)

    def test_totalTime_setter(self):
        lap = TCXLap(self.lap)
        lap.totalTime = 46.1
        self.assertEqual(lap.find("{*}TotalTimeSeconds").text, "46.1")
        self.assertEqual(lap.totalTime, 46.1)
        lap.totalTime = 44.0
        self.assertEqual(lap.find("{*}TotalTimeSeconds").text, "44.0")
        self.assertEqual(lap.totalTime, 44.0)

    def test_totalTime_create(self):
        # Remove the totaltime element and check it is recreated by setter
        lap = TCXLap(self.lap)
        time = lap.totalTime
        el = lap.find("{*}TotalTimeSeconds")
        lap.getroot().remove(el)
        self.assertEqual(lap.totalTime, 0)
        self.assertIsNone(lap.find("{*}TotalTimeSeconds"))
        lap.totalTime = time
        self.assertEqual(lap.find("{*}TotalTimeSeconds").text, "44.0")
        self.assertEqual(lap.totalTime, 44.0)


    def test_maximumSpeed(self):
        lap = TCXLap(self.lap)
        self.assertAlmostEqual(lap.maximumSpeed, 5.073, places=3)

    def test_maximumSpeed_setter(self):
        lap = TCXLap(self.lap)
        originalValue = lap.maximumSpeed
        lap.maximumSpeed = 6.1
        self.assertEqual(lap.find("{*}MaximumSpeed").text, "6.1")
        self.assertEqual(lap.maximumSpeed, 6.1)
        # Restore original value
        lap.maximumSpeed = originalValue
        self.assertAlmostEqual(lap.maximumSpeed, 5.073, places=3)

    def test_maximumSpeed_create(self):
        # Remove the maxspeed element and check it is recreated by setter
        lap = TCXLap(self.lap)
        speed = lap.maximumSpeed
        el = lap.find("{*}MaximumSpeed")
        lap.getroot().remove(el)
        self.assertIsNone(lap.maximumSpeed)
        self.assertIsNone(lap.find("{*}MaximumSpeed"))
        lap.maximumSpeed = speed
        self.assertIsNotNone(lap.find("{*}MaximumSpeed"))
        self.assertAlmostEqual(lap.maximumSpeed, 5.073, places=3)

    def test_averageHeartRate(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.averageHeartRate, 101)

    def test_averageHeartRate_setter(self):
        lap = TCXLap(self.lap)
        lap.averageHeartRate = 120
        self.assertEqual(lap.find("{*}AverageHeartRateBpm/{*}Value").text, "120")
        self.assertEqual(lap.averageHeartRate, 120)
        lap.averageHeartRate = 101
        self.assertEqual(lap.find("{*}AverageHeartRateBpm/{*}Value").text, "101")
        self.assertEqual(lap.averageHeartRate, 101)

    def test_averageHeartRate_create(self):
        # Remove the average hr element and check it is recreated by setter
        lap = TCXLap(self.lap)
        hr = lap.averageHeartRate
        el = lap.find("{*}AverageHeartRateBpm")
        self.assertIsNotNone(el)
        lap.getroot().remove(el)
        self.assertIsNone(lap.find("{*}AverageHeartRateBpm/{*}Value"))
        self.assertIsNone(lap.find("{*}AverageHeartRateBpm"))
        self.assertIsNone(lap.averageHeartRate)
        lap.averageHeartRate = hr
        self.assertIsNotNone(lap.find("{*}AverageHeartRateBpm"))
        self.assertIsNotNone(lap.find("{*}AverageHeartRateBpm/{*}Value"))
        self.assertEqual(lap.find("{*}AverageHeartRateBpm/{*}Value").text, "101")
        self.assertEqual(lap.averageHeartRate, 101)

    def test_maximumHeartRate(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.maximumHeartRate, 125)

    def test_maximumHeartRate_setter(self):
        lap = TCXLap(self.lap)
        lap.maximumHeartRate = 130
        self.assertEqual(lap.find("{*}MaximumHeartRateBpm/{*}Value").text, "130")
        self.assertEqual(lap.maximumHeartRate, 130)
        lap.maximumHeartRate = 125
        self.assertEqual(lap.find("{*}MaximumHeartRateBpm/{*}Value").text, "125")
        self.assertEqual(lap.maximumHeartRate, 125)

    def test_maximumHeartRate_create(self):
        # Remove the maximum hr element and check it is recreated by setter
        lap = TCXLap(self.lap)
        hr = lap.maximumHeartRate
        el = lap.find("{*}MaximumHeartRateBpm")
        self.assertIsNotNone(el)
        lap.getroot().remove(el)
        self.assertIsNone(lap.find("{*}MaximumHeartRateBpm/{*}Value"))
        self.assertIsNone(lap.find("{*}MaximumHeartRateBpm"))
        self.assertIsNone(lap.maximumHeartRate)
        lap.maximumHeartRate = hr
        self.assertIsNotNone(lap.find("{*}MaximumHeartRateBpm"))
        self.assertIsNotNone(lap.find("{*}MaximumHeartRateBpm/{*}Value"))
        self.assertEqual(lap.find("{*}MaximumHeartRateBpm/{*}Value").text, "125")
        self.assertEqual(lap.maximumHeartRate, 125)

    def test_calories(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.calories, 640)

    def test_calories_setter(self):
        lap = TCXLap(self.lap)
        lap.calories = 655
        self.assertEqual(lap.find("{*}Calories").text, "655")
        self.assertEqual(lap.calories, 655)
        lap.calories = 640
        self.assertEqual(lap.find("{*}Calories").text, "640")
        self.assertEqual(lap.calories, 640)

    def test_calories_create(self):
        # Remove the maxspeed element and check it is recreated by setter
        lap = TCXLap(self.lap)
        cal = lap.calories
        el = lap.find("{*}Calories")
        self.assertIsNotNone(el)
        lap.getroot().remove(el)
        self.assertIsNone(lap.calories)
        self.assertIsNone(lap.find("{*}Calories"))
        lap.calories = cal
        self.assertIsNotNone(lap.find("{*}Calories"))
        self.assertEqual(lap.find("{*}Calories").text, "640")
        self.assertEqual(lap.calories, 640)

    def test_intensity(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.intensity, "Active")

    def test_cadence(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.cadence, 87) 

    def test_triggerMethod(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.triggerMethod, "Manual")

    def test_averageSpeed(self):
        lap = TCXLap(self.lap)
        self.assertAlmostEqual(lap.averageSpeed, 4.059, places=3)

    def test_averagePower(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.averagePower, 293)

    def test_maximumPower(self):
        lap = TCXLap(self.lap)
        self.assertEqual(lap.maximumPower, 370)

    
if __name__ == "__main__":
    unittest.main()