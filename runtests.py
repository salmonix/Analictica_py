#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
import unittest

TESTED_CODE = "src/"  # Path to tested code.
TEST_CODE = "test/"  # Path to test code.

sys.path.append(TESTED_CODE)
sys.path.append(TEST_CODE)

# Import all the tests from 'test/'.
for testFile in os.listdir(TEST_CODE):
    if re.match("^test_.+\.py$", testFile):
        exec "from %s import *" % testFile[0:-3]

# Run the tests.
if __name__ == "__main__":
    unittest.main()
