import wx
from recognizer import Recognizer
from templates import *


class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, "Sample")  # add two lines here
		self.frame.Centre()
		self.frame.Show(True)
		return True


class MyFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.detected_shape = wx.StaticText(self, label='Detected shape:', pos=(10, 10))
		self.detected_score = wx.StaticText(self, label='Detected score:', pos=(10, 30))
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
		self.detected_shape.SetLabel('test')
		print self.previous_points

	def LeftDown(self, event):
		dc = wx.ClientDC(self)
		dc.Clear()

if __name__ == '__main__':
	app = MyApp()
	app.MainLoop()

