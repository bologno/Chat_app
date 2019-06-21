"""
Main GUI test cases
"""

import znap_test_case1
import znap_test_case2
import time
import gc


tests = [znap_test_case1, znap_test_case2]

trials = len(tests)
counter = 0
for test in tests:
    if test.main():
        counter += 1
    time.sleep(0.5)
    gc.collect()
print("{} passed from {}".format(counter, trials))
