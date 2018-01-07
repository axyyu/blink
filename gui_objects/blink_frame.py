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
        self.InitUI()
     
    def InitUI(self): 
        self.SetSize((self.width ,self.height))
        # self.SetSize( (100,100) )
        self.SetPosition( (0,0) ) 
        self.SetTitle('Blink')