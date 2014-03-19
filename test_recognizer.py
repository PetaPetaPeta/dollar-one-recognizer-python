import unittest
import numpy as np
from recognizer import *


class TestRecognizer(unittest.TestCase):

	def setUp(self):
		pass

	def test_resample(self):
		points = [[0., 0.], [1., 0.], [1., 1.], [0., 1.]]
		points = np.array(points)
		recognizer = Recognizer()
		resampled = recognizer.resample(points, 8)
		expected_result = np.array([[0.5, 0.],
									[1., 0.],
									[1., 0.5],
									[1., 1.],
									[0.5, 1.],
									[0., 1.],
									[0., 0.5],
									[0., 0.]])
		self.assertTrue((expected_result == resampled).all())

	def test_rotate2D_center0(self):
		# Test rotation around 0,0
		points = [[0., 0.], [1., 0.], [1., 1.], [0., 1.]]
		points = np.array(points)
		expected_result = [[0., 0.],
							[-1., 0.],
							[-1., -1.],
							[-0., -1.]]
		rotated_points = rotate2D(points, 0, np.pi)
		self.assertTrue(np.allclose(rotated_points, expected_result, 1e-8))

	def test_rotate2D_center05(self):
		points = [[0., 0.], [1., 0.], [1., 1.], [0., 1.]]
		points = np.array(points)
		rotated_points = rotate2D(points, 0.5, np.pi)
		expected_result = [[1., 1.],
							[0., 1.],
							[0., 0.],
							[1., 0.]]
		self.assertTrue(np.allclose(rotated_points, expected_result, 1e-8))


if __name__ == '__main__':
	unittest.main()
