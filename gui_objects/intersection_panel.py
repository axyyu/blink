"""
Intersection Panel

"""

from dependencies import *
from gui_objects import road_panel

class Intersection_Panel(wx.Panel):  
      
    def __init__(self, parent, name, roads, pos, size):  
        super(Intersection_Panel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        # self.SetBackgroundColour(wx.BLUE)
        self.SetPosition(pos)
        self.SetSize(size)

        self.name = name
        self.height_interval = 20
        self.size = size

        self.road_names = roads.keys()
        self.road_status = {}

        self.fonts = {
            "title": wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD),
            # "efficiency": wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL),
            # "red": wx.Font(14, wx.DECORATIVE, wx.ITALIC, wx.NORMAL, ),
            # "green": wx.Font(14, wx.DECORATIVE, wx.ITALIC, wx.NORMAL),
            # "yellow": wx.Font(14, wx.DECORATIVE, wx.ITALIC, wx.NORMAL),
        }

        self.InitUI()

    def InitUI(self):
        self.title = wx.StaticText(self, label = self.name, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.title.SetFont(self.fonts["title"])
         
        self.efficiency = wx.StaticText(self, label = '0', style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(0,25))
        self.efficiency.SetForegroundColour((0,0,255))

        init_y = 50
        roads = 0

        for n in self.road_names:
            self.road_status[n] = [
                wx.StaticText(self, label = ' ', style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(10, init_y + self.height_interval*roads)),
                wx.StaticText(self, label = n, style=wx.ALIGN_CENTRE_HORIZONTAL, pos=(20, init_y + self.height_interval*roads)),
                wx.StaticText(self, label = '0', style=wx.ALIGN_RIGHT, pos=(self.size[0] - 40, init_y + self.height_interval*roads))
            ]
            roads+=1
        
        road_panel.Road_Panel(self, "test", (10, 10), (self.size[0]-20, self.size[1]) )

    """
    Intersection Update
    """
    def updateStatus(self, intersection):
        try:
            self.efficiency.SetLabel( str(intersection.eval()['SMA']) )
            for n in self.road_names:
                if intersection.lights[n] == 0: # Yellow
                    self.road_status[n][0].SetBackgroundColour((255,255,0))
                if intersection.lights[n] == 1: # Green
                    self.road_status[n][0].SetBackgroundColour((0,255,0))
                if intersection.lights[n] == -1: # Red
                    self.road_status[n][0].SetBackgroundColour((255,0,0))
                
                self.road_status[n][2].SetLabel( str(len(intersection.roads[n]["enter"].queue)) )
        except:
            pass