"""
Region Frame

"""

from dependencies import *
from gui_objects import intersection_panel

class Region_Frame(wx.Frame): 
    def __init__(self, *args, **kw):  
        super(Region_Frame, self).__init__(*args, **kw) 
        self.width, self.height = wx.GetDisplaySize()
        self.InitUI()
     
    def InitUI(self): 
        self.SetSize((self.width,self.height-30))  

        mpnl = intersection_panel.Intersection_Panel(self) 
 
        self.SetTitle('Blink')
        self.Centre()  
        self.Show(True)

    def add_intersection(self, intersection):
        pass