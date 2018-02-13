"""
Road Panel

"""

from dependencies import *

class Road_Panel(wx.Panel):  
      
    def __init__(self, parent, name, pos, size):  
        super(Road_Panel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        # self.SetBackgroundColour(wx.BLUE)
        self.SetPosition(pos)
        self.SetSize(size)

        self.name = name

        self.InitUI()

    def InitUI(self):
        # self.title = wx.StaticText(self, label = self.name, style=wx.ALIGN_CENTRE_HORIZONTAL)
        for a in range(10):
            b = wx.Panel(self, pos=(a*5, 0), size=(5, 5))
            b.SetBackgroundColour((255,255,0))

    """
    Road Update
    """
    def updateStatus(self, intersection):
        pass