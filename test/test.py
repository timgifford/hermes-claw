import unittest
import datetime
import hook

class SomeTest(unittest.TestCase):
    def test_commitContainsStuff(self):
        actual = pretxncommit_messageStartsWithUSorDE()
        self.assertTrue(actual)

    def test_method(self):
        delta = datetime.timedelta(seconds=10)
        first_timestamp = datetime.datetime.now()
        second_timestamp = datetime.datetime.now()

        self.assertAlmostEqual(first_timestamp, second_timestamp, delta=delta)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
