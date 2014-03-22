# Author: Peter Poulsen
# Date: 2014-03-22
import wx
from recognizer import Recognizer
from template import *

print "Initializing recognizer"
recognizer = Recognizer()
for template in templates:
	recognizer.addTemplate(template)
print "Initilized recognizer!"
frame_height = 400
frame_width = 400


class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, "Mouse recognizer", (frame_height, frame_width))  # add two lines here
		self.frame.Centre()
		self.frame.Show(True)
		return True


class MyFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self, parent, title=title, size=size)
		wx.StaticText(self, label='Detected shape:', pos=(10, 10))
		wx.StaticText(self, label='Detected score:', pos=(10, 30))
		wx.StaticText(self, label='Detected rotation:', pos=(10, 50))
		self.detected_shape = wx.StaticText(self, label='', pos=(95, 10))
		self.detected_score = wx.StaticText(self, label='', pos=(93, 30))
		self.detected_rotation = wx.StaticText(self, label='', pos=(106, 50))

		self.previous_points = []

		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_UP, self.LeftUp)
		self.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)

	def OnMotion(self, event):
		if event.LeftIsDown() and event.Dragging():
			x, y = event.GetPosition()
			self.previous_points.append([x, y])
			dc = wx.ClientDC(self)
			dc.SetPen(wx.Pen(wx.BLACK, 1))
			dc.DrawCircle(x, y, 3)

	def LeftUp(self, event):
		matched_template, score, rotation = recognizer.recognize(self.previous_points)
		self.detected_shape.SetLabel(matched_template.name)
		self.detected_score.SetLabel("{0:.2f}".format(score*100))
		self.detected_rotation.SetLabel(rotation)
		self.previous_points = []

	def LeftDown(self, event):
		dc = wx.ClientDC(self)
		dc.Clear()

if __name__ == '__main__':
	app = MyApp(recognizer)
	app.MainLoop()
