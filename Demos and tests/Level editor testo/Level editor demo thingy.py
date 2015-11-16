#!/usr/bin/env python

##### Image drawing test #####
# A test for the Slipslide level editor which contains a large 25*20 grid. Clicking within a square
# on the grid adds a block in that square (filling the square perfectly). The system also records
# additions in a massive array of ones and zeroes.

import wx


class ImageDrawingThingy(wx.Window):
    def __init__(self, parent, image):
        wx.Window.__init__(self, parent)
        self.photo = image.ConvertToBitmap()
        self.positions = []

        self.array = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.bg = wx.Image("background.png").ConvertToBitmap()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    def OnPaint(self, event):
        buffer = wx.EmptyBitmap(600, 480)
        dc = wx.BufferedPaintDC(self, buffer)
        brush = wx.Brush("#000000")
        dc.SetBackground(brush)
        dc.Clear()
        dc.DrawBitmap(self.bg, 0, 0, True)
        
        for x, y in self.positions:
            dc.DrawBitmap(self.photo, x, y, True)

    def OnClick(self, event):
        rawpos = event.GetPosition()
        if rawpos[0]<600 and rawpos[1]<480:
            arrayposx = int(rawpos[0]/24)
            arrayposy = int(rawpos[1]/24)
            self.array[arrayposy][arrayposx] = "B"
            position = (int(rawpos[0]/24)*24, int(rawpos[1]/24)*24)
            self.positions.append(position)
            self.Refresh()
            # Just gettin' and printing the level data
            leveldata = []
            for line in self.array:
                for item in line:
                    leveldata.append(str(item))
                leveldata.append("\n")
            leveldata.pop(len(leveldata)-1)
            leveldata = "".join(leveldata)
            print "\n\n\n\n\n\n\n\n\n\nThe level so far:\n%s" % leveldata

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Slipinator test thimgamadoodle - copyright David Barker ofc", size=(800, 600))
        img = wx.Image("block.png")
        win = ImageDrawingThingy(self, img)

app = wx.PySimpleApp()
frame = TestFrame()
frame.Show()
app.MainLoop()
