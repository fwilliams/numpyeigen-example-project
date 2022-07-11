from __future__ import print_function
import unittest
import os


class TestExample(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "..", "data")

    def test_example(self):
        from example import example_function
        import numpy as np

        # v is a nv by 3 NumPy array of vertices
        # f is an nf by 3 NumPy array of face indexes into v
        # n is a nv by 3 NumPy array of vertex normals if they are specified, otherwise an empty array
        a1, a2 = np.random.rand(100, 3), np.random.rand(100, 5)
        b1, b2 = example_function(a1, a2)
        self.assertTrue(np.all(a1 == b1))
        self.assertTrue(np.all(a2 == b2))


if __name__ == '__main__':
    unittest.main()
