#!/usr/bin/env python
"""
Unit tests for cstyle.
"""
import cstyle
import os.path
import unittest
import sys

class CStyleTestCase(unittest.TestCase):
    """Base test case for testing CStyle."""
    def __init__(self, name, basename, expected_errors):
        self._basename = basename
        self._expected_errors = (expected_errors if expected_errors is not None
                                 else [])
        super(CStyleTestCase, self).__init__(name)

    def runTest(self):
        """Test case"""
        # output our name as all tests are called runTest so too hard to
        # distinguish
        sys.stderr.write(self._basename + ' ... ')
        base = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'test', self._basename)
        errors = cstyle.CStyle(base + '.conf',
                               [base + '.c']).check()
        self.assertEqual(errors, self._expected_errors)

class CStyleGenerateConfigTestCase(unittest.TestCase):
    """Test generation of configuration file."""
    def runTest(self):
        """Test configuration file generation."""
        cstyle.CStyle(None, []).generate_config()

class CStyleTestSuite(unittest.TestSuite):
    """Test suite for cstyle."""
    def __init__(self):
        super(CStyleTestSuite, self).__init__()
        tests = {'0001_pointer_prefix':
                 [
                     {'column': 27,
                      'file': '/home/amurray/cstyle/test/0001_pointer_prefix.c',
                      'line': 1,
                      'reason': '"rgv" is invalid - failed pattern check "[A-Z][A-Za-z_]+"'}
                 ],
                 '0002_pointer_prefix_repeat':
                 [
                     {'column': 27,
                      'file': '/home/amurray/cstyle/test/0002_pointer_prefix_repeat.c',
                      'line': 1,
                      'reason': '"pArgv" is invalid - expected pointer prefix "pp"'}
                 ],
                 '0003_no_goto':
                 [
                     {'column': 3,
                      'file': '/home/amurray/cstyle/test/0003_no_goto.c',
                      'line': 3,
                      'reason': 'goto considered harmful'},
                     {'column': 3,
                      'file': '/home/amurray/cstyle/test/0003_no_goto.c',
                      'line': 6,
                      'reason': 'goto considered harmful'}
                 ],
                 '0004_prefer_goto':
                 [
                     {'column': 5,
                      'file': '/home/amurray/cstyle/test/0004_prefer_goto.c',
                      'line': 8,
                      'reason': 'Only 1 return statement per function (prefer_goto)'},
                     {'column': 12,
                      'file': '/home/amurray/cstyle/test/0004_prefer_goto.c',
                      'line': 8,
                      'reason': 'Only 1 return statement per function (prefer_goto)'}
                 ]
        }
        for (basename, expected_errors) in tests.iteritems():
            test = CStyleTestCase('runTest', basename, expected_errors)
            self.addTest(test)
        self.addTest(CStyleGenerateConfigTestCase())

if __name__ == '__main__':
    unittest.TextTestRunner().run(CStyleTestSuite())
