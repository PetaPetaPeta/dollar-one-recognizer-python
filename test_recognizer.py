import unittest
import numpy as np
from recognizer import *
from template import *


class TestRecognizer(unittest.TestCase):

	def setUp(self):
		pass

	def test_resample(self):
		points = [[0., 0.], [1., 0.], [1., 1.], [0., 1.]]
		recognizer = Recognizer()
		resampled = np.array(recognizer.resample(points, 9))
		self.assertTrue(len(resampled) == 9)

	def test_resample_more_points(self):
		points = [[i, j] for i in range(10) for j in range(10)]
		recognizer = Recognizer()
		resampled = recognizer.resample(points, 256)
		self.assertTrue(len(resampled) == 256)

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

	def test_match_triangle(self):
		# Add the templates to the recognizer
		recognizer = Recognizer()
		for template in templates:
			recognizer.addTemplate(template)
		# Test that all the templates can be found
		for template in templates:
			matched_template, score = recognizer.recognize(template.points)
			if score < .8:
				continue
			self.assertEquals(matched_template.name, template.name)


if __name__ == '__main__':
	unittest.main()
