import numpy as np
import numpy.linalg as linalg
from itertools import izip

omega = 0.5 * (-1 + np.sqrt(5))

class Recognizer(object):
	"""docstring for Recognizer"""
	def __init__(self):
		super(Recognizer, self).__init__()

	def resample(self, points, n):
		path_length = getPathLength(points) / (n)
		newPoints = np.zeros((1, 2))
		D = 0
		i = 1
		no_of_points = len(points)
		while i <= no_of_points:
			point = points[i-1]
			next_point = points[i % no_of_points]
			d = getDistance(point, next_point)
			if D + d >= path_length:
				q = np.array([0., 0.])
				q[0] = point[0] + ((path_length-D)/d) * (next_point[0] - point[0])
				q[1] = point[1] + ((path_length-D)/d) * (next_point[1] - point[1])
				newPoints = np.append(newPoints, [q], 0)
				points = np.insert(points, i, q, 0)
				no_of_points += 1
				D = 0
			else:
				D += d
			i += 1
		newPoints = newPoints[1:]
		return newPoints

	def rotateToZero(self, points):
		centroid = np.mean(points, 0)
		angle_to_rotate = np.arctan2(centroid[1]-points[0][1], centroid[0]-points[0][0])
		newPoints = rotate2D(points, 0, -angle_to_rotate)
		return newPoints

	def rotateBy(self, points, angle):
		centroid = np.mean(points, 0)
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = (point[0]-centroid[0]) * np.cos(angle) - (point[1] - centroid[1]) * np.sin(angle) + centroid[0]
			q[1] = (point[0]-centroid[0]) * np.sin(angle) + (point[1] - centroid[1]) * np.cos(angle) + centroid[1]
			newPoints = np.append(newPoints, q, 0)
		return newPoints[1:]

	def scaleToSquare(self, points, size):
		max_x, max_y = np.max(points, 0)
		min_x, min_y = np.min(points, 0)
		b_width = max_x - min_x
		b_height = max_y - min_y
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = point[0] * (size / b_width)
			q[1] = point[1] * (size / b_height)
			newPoints = np.append(newPoints, q, 0)
		return newPoints[1:]

	def translateToOrigin(points):
		centroid = np.mean(points, 0)
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = point[0] - centroid[0]
			q[1] = point[1] - centroid[1]
			newPoints = np.append(newPoints, q, 0)
		return newPoints[1:]

	def recognize(self, points, templates):
		b = np.inf
		selected_template = None
		for template in templates:
			d = self.distanceAtBestAngle(points, template, -angle, angle, angle_step)
			if d < b:
				b = d
				selected_template = template
		score = 1 - b / (0.5 * np.sqrt(size**2 + size**2))
		return selected_template, score

	def distanceAtBestAngle(self, points, template, angle_a, angle_b, angle_step):
		x_1 = omega * angle_a + (1 - omega) * angle_b
		f_1 = self.distanceAtAngle(points, template, x_1)
		x_2 = (1 - omega) * angle_a + omega * angle_b
		f_2 = self.distanceAtAngle(points, template, x_2)
		while np.abs(angle_b, angle_a) > angle_step:
			if f_1 < f_2:
				angle_b = x_2
				x_2 = x_1
				f_2 = f_1
				x_1 = omega * angle_a + (1 - omega) * angle_b
				f_1 = self.distanceAtAngle(points, template, x_1)
			else:
				angle_a = x_1
				x_1 = x_2
				f_1 = f_2
				x_2 = (1 - omega) * angle_a + omega * angle_b
				f_2 = self.distanceAtAngle(points, template, x_2)
		return np.min(f_1, f_2)

	def distanceAtAngle(self, points, template, angle):
		newPoints = self.rotateBy(points, angle)
		d = pathDistance(newPoints, template)
		return d


def pathDistance(path1, path2):
	d = 0
	for p_1, p_2 in izip(path1, path2):
		d = d + getDistance(p_1, p_2)
	return d / len(path1)


def getDistance(point1, point2):
	return linalg.norm(point2 - point1)


def rotate2D(pts, cnt, ang=np.pi/4):
	''' pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian
		http://gis.stackexchange.com/questions/23587/how-do-i-rotate-the-polygon-about-an-anchor-point-using-python-script'''
	return np.dot(pts-cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]]))+cnt


def getPathLength(points):
	length = 0
	for (i, j) in pairwiseIterator(points):
		length += linalg.norm(i - j)
	return length


def pairwiseIterator(elems):
	for (i, j) in izip(elems, elems[1:]):
		yield (i, j)
	yield (elems[-1], elems[0])


points = [[0., 0.], [1., 1.], [2., 2.]]
points = np.array(points)
recognizer = Recognizer()
resampled = recognizer.resample(points, 10)
print resampled.shape
print recognizer.rotateToZero(resampled).shape

# print points