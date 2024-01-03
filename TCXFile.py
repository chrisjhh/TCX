from .TCXDocument import TCXDocument
import xml.etree.ElementTree as ET
from .outputElement import outputElement


def loadTCX(filename: str) -> TCXDocument:
    with open(filename, "r") as tcx:
        data = tcx.read()
    data = data.strip()
    root = ET.fromstring(data)
    return TCXDocument(root)

def saveTCX(filename: str, doc: TCXDocument) -> None:
    with open(filename, "w") as fh:
        fh.write("<?xml version='1.0' encoding='UTF-8'?>")
        outputElement(doc.getroot(), fh)
    
class TCXFile(TCXDocument):

    def __init__(self, filename: str):
        super().__init__(loadTCX(filename).getroot())
        self.filename = filename

    def save(self):
        saveTCX(self.filename, self)

    def saveAs(self, filename: str):
        saveTCX(filename, self)
