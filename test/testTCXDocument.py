
import unittest
import xml.etree.ElementTree as ET
from TCX.TCXDocument import TCXDocument
from TCX.TCXActivities import TCXActivities
from TCX.TCXActivity import TCXActivity
from TCX.TCXAuthor import TCXAuthor
from .testData import getIntervalData

class TestTCXDocument(unittest.TestCase):

    def setUp(self):
        filename = getIntervalData()
        with open(filename) as tcx:
            data = tcx.read()
        data = data.strip()
        self.root = ET.fromstring(data)

    def test_ElementAccess(self):
        doc = TCXDocument(self.root)
        activity = doc.find("{*}Activities/{*}Activity")
        self.assertTrue(isinstance(activity, ET.Element))

    def test_activities(self):
        doc = TCXDocument(self.root)
        activities = doc.activities
        self.assertTrue(isinstance(activities, TCXActivities))

    def test_activity(self):
        doc = TCXDocument(self.root)
        activity = doc.activity
        self.assertTrue(isinstance(activity, TCXActivity))

    def test_author(self):
        doc = TCXDocument(self.root)
        author = doc.author
        self.assertTrue(isinstance(author, TCXAuthor))
        self.assertCountEqual(author.name, "Polar Flow Mobile Viewer Android")

if __name__ == "__main__":
    unittest.main()