import unittest
import xml.etree.ElementTree as ET
import tempfile

from TCX.TCXFile import TCXFile, loadTCX, saveTCX
from TCX.TCXDocument import TCXDocument
from .testData import getIntervalData
from .testEquals import testEquals, ElementDifference

class TestTCXFile(unittest.TestCase):

    def test_loadAndSave(self):
        filename = getIntervalData()

        # Check it loads correctly
        doc = loadTCX(filename)
        self.assertTrue(isinstance(doc, TCXDocument))
        self.assertEqual(doc.activity.sport, "Running")

        # Save to a temp file
        with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
            fp.close()
            saveTCX(fp.name, doc)
            # Read it in again
            doc2 = loadTCX(fp.name)
        # Temp file is now deleted
            
        self.assertTrue(isinstance(doc2, TCXDocument))
        self.assertEqual(doc2.activity.sport, "Running")
        
        # Check that saving and loading produces same result
        try:
            testEquals(doc.getroot(), doc2.getroot())
        except ElementDifference as e:
            self.fail(e)
        