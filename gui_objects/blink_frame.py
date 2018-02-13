"""
Blink GUI Setup

"""

from dependencies import *
from gui_objects import intersection_panel
from gui_objects import region_panel

class Blink_Frame(wx.Frame): 
    def __init__(self, *args, **kw):  
        super(Blink_Frame, self).__init__(*args, **kw) 
        self.width, self.height = wx.GetDisplaySize()
        self.panels = {}
    
    def setGrid(self,x,y):
        self.grid_x = x
        self.grid_y = y

    def InitUI(self): 
        self.SetSize((self.width ,self.height))
        self.SetTitle('Blink')

        self.panel_width = self.width/self.grid_x
        self.panel_height = self.height/self.grid_y
        self.panel_count = 0

    def addIntersection(self, name, roads):
        x = int(self.panel_count%self.grid_x) * self.panel_width
        y = int(self.panel_count/self.grid_x) * self.panel_height
        # title = wx.StaticText(self, label = name)
        self.panels[name] = intersection_panel.Intersection_Panel(self, name, roads, (x+10, y+10), (self.panel_width-20, self.panel_height-20) )
        self.panel_count+=1
        return self.panels[name]