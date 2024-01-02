import os.path

def getTestData(filename: str) -> str:
    """Return the path to a test data file"""
    this_dir = os.path.dirname(__file__)
    data_dir = os.path.join(this_dir, 'data')
    test_file = os.path.join(data_dir, filename)
    return test_file

def getIntervalData() -> str:
    """Return the path name to the standard TCX testdata file with running intervals"""
    return getTestData("SG1_Track_Session_Earn_your_Turkey_.tcx")

