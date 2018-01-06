"""
Intersection Panel

"""

from dependencies import *

class Intersection_Panel(wx.Panel):  
      
    def __init__(self, parent):  
        super(Intersection_Panel, self).__init__(parent) 

        label = wx.StaticText(self, label = "hello", pos = (0,0))