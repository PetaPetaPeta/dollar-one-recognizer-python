import numpy as np
import numpy.linalg as linalg
from itertools import izip
from template import templates

phi = 0.5 * (-1 + np.sqrt(5))
numPoints = 255


class Recognizer(object):
	"""docstring for Recognizer"""
	def __init__(self, angle_range=45., angle_step=2., square_size=250.):
		super(Recognizer, self).__init__()
		self.angle_range = angle_range
		self.angle_step = angle_step
		self.square_size = square_size
		self.templates = []

	def resample(self, points, n):
		# Get the length that should be between the returned points
		path_length = pathLength(points) / float(n-1)
		newPoints = [points[0]]
		D = 0.0
		i = 1
		while i < len(points):
			point = points[i-1]
			next_point = points[i]
			d = getDistance(point, next_point)
			if D + d >= path_length:
				delta_distance = float((path_length-D)/d)
				q = [0., 0.]
				q[0] = point[0] + delta_distance * (next_point[0] - point[0])
				q[1] = point[1] + delta_distance * (next_point[1] - point[1])
				newPoints.append(q)
				points.insert(i, q)
				D = 0.
			else:
				D += d
			i += 1
		if len(newPoints) == n - 1:  # Fix a possible roundoff error
			newPoints.append(points[0])
		return newPoints

	def addTemplate(self, template):
		template.points = self.resample(template.points, numPoints)
		template.points = self.rotateToZero(template.points)
		template.points = self.scaleToSquare(template.points)
		template.points = self.translateToOrigin(template.points)
		self.templates.append(template)

	def indicativeAngle(self, points):
		''' Returns the angle (radians) to rotate to get the indicative angle '''
		centroid = np.mean(points, 0)
		angle_to_rotate = np.arctan2(centroid[1]-points[0][1], centroid[0]-points[0][0])
		return angle_to_rotate

	def rotateToZero(self, points):
		''' Rotates the points to the indicative angle '''
		angle_to_rotate = self.indicativeAngle(points)
		newPoints = rotate2D(points, 0, -angle_to_rotate)
		return newPoints

	def rotateBy(self, points, angle):
		centroid = np.mean(points, 0)
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = (point[0]-centroid[0]) * np.cos(angle) - (point[1] - centroid[1]) * np.sin(angle) + centroid[0]
			q[1] = (point[0]-centroid[0]) * np.sin(angle) + (point[1] - centroid[1]) * np.cos(angle) + centroid[1]
			newPoints = np.append(newPoints, [q], 0)
		return newPoints[1:]

	def scaleToSquare(self, points):
		max_x, max_y = np.max(points, 0)
		min_x, min_y = np.min(points, 0)
		b_width = max_x - min_x
		b_height = max_y - min_y
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = point[0] * (self.square_size / b_width)
			q[1] = point[1] * (self.square_size / b_height)
			newPoints = np.append(newPoints, [q], 0)
		return newPoints[1:]

	def translateToOrigin(self, points):
		centroid = np.mean(points, 0)
		newPoints = np.zeros((1, 2))
		for point in points:
			q = np.array([0., 0.])
			q[0] = point[0] - centroid[0]
			q[1] = point[1] - centroid[1]
			newPoints = np.append(newPoints, [q], 0)
		return newPoints[1:]

	def recognize(self, points):
		b = np.inf
		selected_template = None
		for template in self.templates:
			d = self.distanceAtBestAngle(points, template.points, -self.angle_range, self.angle_range, self.angle_step)
			if d < b:  # Get the best distance and template
				b = d
				selected_template = template
		score = 1 - b / (0.5 * np.sqrt(self.square_size**2 + self.square_size**2))
		return selected_template, score

	def distanceAtBestAngle(self, points, template, angle_a, angle_b, angle_step):
		x_1 = phi * angle_a + (1 - phi) * angle_b
		f_1 = self.distanceAtAngle(points, template, x_1)
		x_2 = (1 - phi) * angle_a + phi * angle_b
		f_2 = self.distanceAtAngle(points, template, x_2)
		while np.abs(angle_b - angle_a) > angle_step:
			if f_1 < f_2:
				angle_b = x_2
				x_2 = x_1
				f_2 = f_1
				x_1 = phi * angle_a + (1 - phi) * angle_b
				f_1 = self.distanceAtAngle(points, template, x_1)
			else:
				angle_a = x_1
				x_1 = x_2
				f_1 = f_2
				x_2 = (1 - phi) * angle_a + phi * angle_b
				f_2 = self.distanceAtAngle(points, template, x_2)
		return min(f_1, f_2)

	def distanceAtAngle(self, points, template, angle):
		newPoints = self.rotateBy(points, angle)
		d = pathDistance(newPoints, template)
		return d


def pathDistance(path1, path2):
	''' Calculates the distance between two paths. Fails if len(path1) != len(path2) '''
	if len(path1) != len(path2):
		raise Exception('Path lengths do not match!')
	d = 0
	for p_1, p_2 in izip(path1, path2):
		d = d + getDistance(p_1, p_2)
	return d / len(path1)


def getDistance(point1, point2):
	return linalg.norm(np.array(point2) - np.array(point1))


def rotate2D(pts, cnt, ang=np.pi/4):
	''' pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian
		http://gis.stackexchange.com/questions/23587/how-do-i-rotate-the-polygon-about-an-anchor-point-using-python-script'''
	return np.dot(np.array(pts)-cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]]))+cnt


def pathLength(points):
	length = 0
	for (i, j) in izip(points, points[1:]):
		length += getDistance(i, j)
	return length


def pairwiseIterator(elems):
	for (i, j) in izip(elems, elems[1:]):
		yield (i, j)
	yield (elems[-1], elems[0])

