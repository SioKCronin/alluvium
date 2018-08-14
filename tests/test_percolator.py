import unittest

term = "lovely"
target = ["today", "is", "a", "lovely", "day"]

class TestPercolator(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(percolate(term, target))

def percolate(term, target):
    if term in target:
        return True

if __name__ == '__main__':
    unittest.main()
