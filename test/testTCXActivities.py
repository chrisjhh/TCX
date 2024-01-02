
import unittest
import xml.etree.ElementTree as ET
from TCX.TCXActivities import TCXActivities
from TCX.TCXActivity import TCXActivity
from .testData import getIntervalData

class TestTCXDocument(unittest.TestCase):

    def setUp(self):
        filename = getIntervalData()
        with open(filename) as tcx:
            data = tcx.read()
        data = data.strip()
        root = ET.fromstring(data)
        self.activities = root.find("{*}Activities")

    def test_ElementAccess(self):
        acts = TCXActivities(self.activities)
        activity = acts.find("{*}Activity")
        self.assertTrue(isinstance(activity, ET.Element))

    def test_subscript(self):
        acts = TCXActivities(self.activities)
        activity = acts[0]
        self.assertTrue(isinstance(activity, TCXActivity))

    def test_len(self):
        acts = TCXActivities(self.activities)
        n = len(acts)
        self.assertEqual(n, 1, "Should be one activity")

    def test_iter(self):
        acts = TCXActivities(self.activities)
        looped = 0
        for activity in acts:
            looped += 1
            self.assertTrue(isinstance(activity, TCXActivity))
        self.assertEqual(looped, 1, "Should have looped once")

if __name__ == "__main__":
    unittest.main()