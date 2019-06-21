"""
Main API test cases
"""

import znap_test_case1
import znap_test_case2
from threading import Thread
import server
import client_lite
import time
import gc


def main():
    chat_server = Thread(target=server.run)
    chat_server.start()
    time.sleep(1)
    user = input("Enter user name: ")
    print("{} test positive result: {}".format("welcome", client_lite.run("welcome", user)))
    print("{} test positive result: {}".format("goodbye", client_lite.run("goodbye", user)))


if __name__ == "__main__":
    main()

"""
tests = [znap_test_case1, znap_test_case2]

trials = len(tests)
counter = 0
for test in tests:
    if test.main():
        counter += 1
    time.sleep(0.5)
    gc.collect()
print("{} passed from {}".format(counter, trials))

"""
