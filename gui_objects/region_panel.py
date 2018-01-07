"""
Region Panel

"""

from dependencies import *

class Region_Panel(wx.Panel):  
      
    def __init__(self, parent):  
        super(Region_Panel, self).__init__(parent) 

        label = wx.StaticText(self, label = "hello", pos = (0,0))