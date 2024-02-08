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
        with tempfile.NamedTemporaryFile() as fp:
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

        # Just to be sure testEquals is working - make a small change
        doc2.activity.laps()[0].distance = 0
        with self.assertRaises(ElementDifference):
            testEquals(doc.getroot(), doc2.getroot())

    def test_TCXFile(self):
        filename = getIntervalData()
        tcx = TCXFile(filename)
        self.assertTrue(isinstance(tcx, TCXFile))
        self.assertTrue(isinstance(tcx, TCXDocument))
        self.assertEqual(tcx.activity.sport, "Running")
        self.assertEqual(tcx.filename, filename)

        # Save to a temp file
        with tempfile.NamedTemporaryFile() as fp:
            fp.close()
            tcx.saveAs(fp.name)
            # Read it in again
            tcx2 = TCXFile(fp.name)
        # Temp file is now deleted

        self.assertTrue(isinstance(tcx2, TCXFile))    
        self.assertTrue(isinstance(tcx2, TCXDocument))
        self.assertEqual(tcx2.activity.sport, "Running")
        self.assertNotEqual(tcx.filename, tcx2.filename)
        
        # Check that saving and loading produces same result
        try:
            testEquals(tcx.getroot(), tcx2.getroot())
        except ElementDifference as e:
            self.fail(e)
        