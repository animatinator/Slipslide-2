#!/usr/bin/env python

## Slipinator - the Penuine level editor
# Used for creating levels quickly and easily
# Copyright ExeSoft 2007
#
# Update history:
# Created: Sunday 23rd December 2007
# Version 1.0 finished - *

import os
import shutil
import wx
import wx.lib.buttons as buttons

###################################################################### LEVEL CANVAS ##########

class LevelCanvas(wx.Window):
    """
The special canvas class for making the level on. This adds blocks when clicked, and other objects
can be dragged onto it.
    """
    def __init__(self, parent, pos, *args, **kwargs):
        """
    The initialisation method, which loads the images, creates the variables and binds the events.
        """
        wx.Window.__init__(self, parent, -1, style = wx.NO_BORDER)

        # Get the images
        self.bg = wx.Image("Data\\slipinator\\background.png").ConvertToBitmap()
        self.block = wx.Image("Data\\slipinator\\block.png").ConvertToBitmap()

        # Initialise variables
        self.pos = pos
        self.parent = parent
        self.blocks = []

        # Bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    def OnPaint(self, event):
        """
    The level canvas redraw method, which draws in the images and then the grid.
        """
        # Create the buffer and the buffered device context
        imagebuffer = wx.EmptyBitmap(600, 480)
        dc = wx.BufferedPaintDC(self, imagebuffer)

        # Clear the backgound
        brush = wx.Brush("#000000")
        dc.SetBackground(brush)
        dc.Clear()
        # Draw the backgorund image
        dc.DrawBitmap(self.bg, 0, 0, True)

        # Draw in the blocks
        for pos in self.blocks:
            dc.DrawBitmap(self.block, pos[0], pos[1], True)

        # If the parent object is set to show the grid
        if self.parent.showgrid == True:
            # Draw in the grid lines along the x-axis
            for i in range(1, 25):
                dc.DrawLine(i*24, 0, i*24, 480)

            # Draw in the grid lines along the y-axis
            for i in range(1, 20):
                dc.DrawLine(0, i*24, 600, i*24)

        # Set the position and size of the level canvas window
        self.SetPosition(self.pos)
        self.SetSize((600, 480))

    def InitPositions(self):
        self.blocks = []
        for i in range(0, 20):
            line = i
            for i in range(0, 25):
                row = i
                if self.parent.leveldata[line][row] == "B":
                    self.AddBlock((row, line))

    def OnClick(self, event):
        """
    A method to process mouse click events.
        """
        # If the mouse click is inside the window
        rawpos = event.GetPosition()
        if rawpos[0]<600 and rawpos[1]<480:
            # Get the grid co-ordinates for the mouse click
            position = (rawpos[0]/24, rawpos[1]/24)

            # If there's nothing in that space, add a block
            if self.parent.leveldata[position[1]][position[0]] == "0":
                self.AddBlock(position)

            # If there's a block there, remove it
            elif self.parent.leveldata[position[1]][position[0]] == "B":
                self.RemoveBlock(position)

    def AddBlock(self, pos):
        """
    A method which adds a block to a given grid co-ordinate on the level canvas.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Append it to the list of block drawing points
        self.blocks.append(pixelpos)
        # Modify the parent object (main window)'s level data so there is now a block in the given
        # position
        self.parent.leveldata[pos[1]][pos[0]] = "B"
        # Refresh the area of the screen in which the block has been drawn
        self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))

    def RemoveBlock(self, pos):
        """
    A method which removes the block from a given grid co-ordinate on the level canvas.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Go through the list of positions until a position matching the give one is found.
        # "count" keeps a record of the item number
        count = 0
        for item in self.blocks:
            # If it's found, remove it
            if str(item) == str(pixelpos):
                self.blocks.pop(count)
            # Otherwise, increase the item number
            else:
                count = count+1
        # Modify the parent object (main window)'s level data so there is no longer a block in the
        # given position
        self.parent.leveldata[pos[1]][pos[0]] = "0"
        # Refresh the area of the screen from which the block has been erased
        self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))

###################################################################### MAIN FRAME ##########

class Slipinator(wx.Frame):
    """
The main Slipinator window, containing all globally used variables, GUI elements and methods.
    """
    def __init__(self, parent):
        """
    The initialisation method which creates the GUI and defines the starting variables.
        """
        wx.Frame.__init__(self, parent, -1, "ExeSoft Slipinator (Slipslide 2 level editor)",
            size=(800, 600), style=wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.CAPTION)
        # Centre the frame and set its background colour
        self.Centre()
        self.SetBackgroundColour("#FFFFFF")

        # Initialise the level name
        self.levelname = "New level"
        
        # Initialise a variable for whether or not to display the grid
        self.showgrid = True
        
        # Create the massive level data array
        self.leveldata = [
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "0", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "0", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "W", "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                ]

        # Create the GUI elements
        self.CreateMenuBar()
        self.InitialiseStatusbar()
        self.CreateCanvas()
        # Update the window title
        self.UpdateTitle()

    def CreateMenuBar(self):
        """
    A method which creates the window's menu bar.
        """
        # Create the menu bar
        self.menubar = wx.MenuBar()
        
        # The file menu
        filemenu = wx.Menu()
        # Add options
        filenew = filemenu.Append(-1, "New", "Create a new level")
        fileopen = filemenu.Append(-1, "Open", "Open a previously saved level for editing")
        filesave = filemenu.Append(-1, "Save", "Save the current level")
        filemenu.AppendSeparator()
        fileexit = filemenu.Append(-1, "Exit", "Exit the application")
        # Bind file menu events
        self.Bind(wx.EVT_MENU, self.FileExit, fileexit)
        self.Bind(wx.EVT_MENU, self.FileNew, filenew)
        self.Bind(wx.EVT_MENU, self.FileOpen, fileopen)
        self.Bind(wx.EVT_MENU, self.FileSave, filesave)
        # Append the file menu to the menu bar
        self.menubar.Append(filemenu, "File")
        
        # The edit menu
        editmenu = wx.Menu()
        # Add options
        editrename = editmenu.Append(-1, "Rename level", "Rename the current level")
        # Bind edit menu events
        self.Bind(wx.EVT_MENU, self.EditRename, editrename)
        # Append the edit menu to the menu bar
        self.menubar.Append(editmenu, "Edit")

        # The view menu
        viewmenu = wx.Menu()
        # Add options
        viewshowgrid = viewmenu.AppendCheckItem(-1, "Show grid",
                "Toggle the grid on the level canvas on and off")
        viewshowgrid.Check(True) # Make the "show grid" method checked by default
        # Bind the view menu events
        self.Bind(wx.EVT_MENU, self.ViewShowGrid, viewshowgrid)
        # Append the view menu to the menu bar
        self.menubar.Append(viewmenu, "View")
        
        # Set the window's menu bar to the newly created menu bar
        self.SetMenuBar(self.menubar)

    def InitialiseStatusbar(self):
        """
    A method which creates the window's status bar and gives it two text fields.
        """
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)

    def CreateCanvas(self):
        """
    A method which creates the main level canvas.
        """
        self.canvas = LevelCanvas(self, (100, 25))

    def FileNew(self, event):
        pass

    def FileOpen(self, event):
        infile = open("customlevels.dat", "r")
        data = infile.read().split("\n")
        infile.close()
        data.pop(0)
        if len(data) < 1:
            dlg = wx.MessageDialog(self, "No Slipslide 2 custom level files have been saved!",
                    "No levels to open", style = wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dlg = wx.SingleChoiceDialog(self, "Select a level to open", "Open level", data)
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetSelection()
                selection = data[selection]
                infile = open("%s\\layout.slf" % selection, "r")
                rawdata = infile.readlines()
                data = []
                for rawline in rawdata:
                    line = []
                    for item in rawline:
                        if item == "\n":
                            pass
                        else:
                            line.append(item)
                    data.append(line)
                self.leveldata = data
                self.canvas.InitPositions()
                self.canvas.Refresh()
                    

    def FileSave(self, event):
        """
    A method which saves the current file to a Slipslide 2 level folder.
        """
        # Make sure the filename is safe
        fixedlevelname = self.levelname.replace(" ", "_")
        fixedlevelname = fixedlevelname.replace("\\", "")
        # Make a folder if one doesn't already exist
        try:
            os.mkdir(fixedlevelname)
        except:
            pass
        # Create the layout file
        outfile = open("%s\\layout.slf" % fixedlevelname, "w")
        # Create a list out of all items in the leveldata, with a newline character between each line
        leveldata = []
        for line in self.leveldata:
            for item in line:
                leveldata.append(str(item))
            leveldata.append("\n")
        # Remove the last newline
        leveldata.pop(len(leveldata)-1)
        # Turn it into a string
        leveldata = "".join(leveldata)
        # Write out the data and close the file
        outfile.write(leveldata)
        outfile.close()
        # Copy the background image, block image and hole image to the newly-created level folder
        shutil.copyfile("Data\\slipinator\\background.png", "%s\\background.png" % fixedlevelname)
        shutil.copyfile("Data\\slipinator\\block.png", "%s\\block.png" % fixedlevelname)
        shutil.copyfile("Data\\slipinator\\hole.png", "%s\\hole.png" % fixedlevelname)
        # Copy the music to the newly-created folder
        shutil.copyfile("Data\\slipinator\\music.ogg", "%s\\music.ogg" % fixedlevelname)
        # Append the level's name to the list of custom levels, keeping the existing list data
        datafile = open("customlevels.dat", "r")
        contents = datafile.read()
        data = [contents, "\n%s" % fixedlevelname]
        datafile.close()
        data = "".join(data)
        datafile = open("customlevels.dat", "w")
        datafile.write(data)
        datafile.close()

    def FileExit(self, event):
        """
    The application's quit method.
        """
        self.Destroy()

    def EditRename(self, event):
        """
    A method for renaming the level.
        """
        dlg = wx.TextEntryDialog(self, "Enter a name for the current level:", "Rename level",
                self.levelname, style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.levelname = dlg.GetValue()
        self.UpdateTitle()

    def ViewShowGrid(self, event):
        """
    A method which toggles the grid on the level canvas on and off.
        """
        # If the box is checked, the grid should be shown
        if event.IsChecked():
            self.showgrid = True
        # If it isn't, the grid shouldn't be shown
        else:
            self.showgrid = False
        # Refresh the canvas
        self.canvas.Refresh()

    def UpdateTitle(self):
        newtitle = "%s -- ExeSoft Slipinator (Slipslide 2 level editor)" % self.levelname
        self.SetTitle(newtitle)

###################################################################### MAINLOOP ##########

if __name__ == "__main__":
    app = wx.App()
    frame = Slipinator(None)
    frame.Show(True)
    app.MainLoop()
