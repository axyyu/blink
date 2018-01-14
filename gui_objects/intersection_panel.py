"""
Intersection Panel

"""

from dependencies import *

class Intersection_Panel(wx.Panel):  
      
    def __init__(self, parent, name, pos, size):  
        super(Intersection_Panel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        # self.SetBackgroundColour(wx.BLUE)
        self.SetPosition(pos)
        self.SetSize(size)

        self.name = name
        self.InitUI()

    def InitUI(self):
        self.title = wx.StaticText(self, label = self.name, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.vehicle = wx.StaticText(self, label = self.name, style=wx.ALIGN_CENTER)

    """
    Intersection Update
    """

    """
    Road Update
    """
    def setRoad(self, road_list):
        pass
    
    """
    Car Update
    """
    def addCar(self):
        pass