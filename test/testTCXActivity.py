
import unittest
import xml.etree.ElementTree as ET
from TCX.TCXActivity import TCXActivity
from TCX.TCXTraining import TCXTraining
from TCX.TCXCreator import TCXCreator
from TCX.TCXLap import TCXLap
from .testData import getIntervalData

class TestTCXDocument(unittest.TestCase):

    def setUp(self):
        filename = getIntervalData()
        with open(filename) as tcx:
            data = tcx.read()
        data = data.strip()
        root = ET.fromstring(data)
        self.activity = root.find("{*}Activities/{*}Activity")

    def test_ElementAccess(self):
        act = TCXActivity(self.activity)
        lap = act.find("{*}Lap")
        self.assertTrue(isinstance(lap, ET.Element))

    def test_sport(self):
        act = TCXActivity(self.activity)
        self.assertEqual(act.sport, "Running")

    def test_sport_setter(self):
        act = TCXActivity(self.activity)
        act.sport = "Swimming"
        self.assertEqual(act.getroot().get("Sport"), "Swimming")
        act.sport = "Running"
        self.assertEqual(act.getroot().get("Sport"), "Running")

    def test_training(self):
        act = TCXActivity(self.activity)
        training = act.training
        self.assertTrue(isinstance(training, TCXTraining))

    def test_creator(self):
        act = TCXActivity(self.activity)
        creator = act.creator
        self.assertTrue(isinstance(creator, TCXCreator))
        self.assertEqual(creator.name, "Polar Pacer Pro")

    def test_laps(self):
        act = TCXActivity(self.activity)
        laps = act.laps()
        self.assertEqual(len(laps), 64)
        for l in laps:
            self.assertTrue(isinstance(l, TCXLap))
            self.assertEqual(l.parent, act.getroot())

if __name__ == "__main__":
    unittest.main()