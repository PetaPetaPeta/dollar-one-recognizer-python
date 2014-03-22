# Author: Peter Poulsen
# Date: 2014-03-22
import wx
from recognizer import Recognizer
from template import *
import tuio
import time

tracking = None
recognizer = None
frame_height = 400
frame_width = 400


class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, "Tuio Recognizer", (frame_height, frame_width))
		self.frame.Centre()
		self.frame.Show(True)
		self.keepGoing = True
		return True

	def MainLoop(self):
		evtloop = wx.GUIEventLoop()
		old = wx.EventLoop.GetActive()
		wx.EventLoop.SetActive(evtloop)

		# Main loop of the frame
		while self.keepGoing:
			# Get the position of the tracking app
			tracking.update()
			for obj in tracking.objects():
				self.frame.TuioMove(obj.xpos*frame_width, obj.ypos*frame_height, obj.angle)

			while evtloop.Pending():
				evtloop.Dispatch()

			time.sleep(0.01)
			evtloop.ProcessIdle()

		wx.EventLoop.SetActive(old)


class MyFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self, parent, title=title, size=size)
		wx.StaticText(self, label='Detected shape:', pos=(10, 10))
		wx.StaticText(self, label='Detected score:', pos=(10, 30))
		# wx.StaticText(self, label='Detected rotation:', pos=(10, 50))
		self.detected_shape = wx.StaticText(self, label='', pos=(95, 10))
		self.detected_score = wx.StaticText(self, label='', pos=(93, 30))
		self.detected_rotation = wx.StaticText(self, label='', pos=(106, 50))
		self.previous_points = []

	def TuioMove(self, x, y, angle):
		if angle > 60 and angle < 120:
			self.previous_points.append([x, y])
			dc = wx.ClientDC(self)
			dc.SetPen(wx.Pen(wx.BLACK, 1))
			dc.DrawCircle(x, y, 3)
		else:
			if len(self.previous_points) > 30:
				matched_template, score, rotation = recognizer.recognize(self.previous_points)
				self.detected_shape.SetLabel(matched_template.name)
				self.detected_score.SetLabel("{0:.2f}".format(score*100))
			self.previous_points = []
			dc = wx.ClientDC(self)
			dc.Clear()

if __name__ == '__main__':
	# Initialize the TUIO and gesture recognizer
	tracking = tuio.Tracking()
	print "Initializing recognizer"
	recognizer = Recognizer()
	for template in templates:
		recognizer.addTemplate(template)
	print "Initilized recognizer!"
	# Start the main loop of the GUI drawing
	app = MyApp(recognizer)
	app.MainLoop()
