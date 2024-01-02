"""Class representing the root node of a TCX document"""

from .TCXActivities import TCXActivities
from .TCXActivity import TCXActivity
from .TCXAuthor import TCXAuthor

import xml.etree.ElementTree as ET
from .errors import TCXFormatError
from .utils import unqualifiedName

class TCXDocument(ET.ElementTree):

    def __init__(self, element: ET.Element):
        super().__init__(element)
        if unqualifiedName(element.tag) != "TrainingCenterDatabase":
            raise TCXFormatError("Unexpected document tag {}".format(unqualifiedName(element.tag)))
        
    @property
    def activities(self) -> TCXActivities:
        el = self.find("{*}Activities")
        if el is None:
            raise TCXFormatError("No Activities element found")
        return TCXActivities(el)
    
    @property
    def activity(self) -> TCXActivity:
        el = self.find("{*}Activities/{*}Activity")
        if el is None:
            raise TCXFormatError("No Activity element found")
        return TCXActivity(el)
    
    @property
    def author(self) -> TCXActivities:
        el = self.find("{*}Author")
        if el is None:
            # It may be valid to have no author
            # So don't raise exception
            raise None
        return TCXAuthor(el)