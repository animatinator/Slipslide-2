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

###################################################################### CANVAS DROP TARGET ###

class DropTarget(wx.DropTarget):
    """
A class used by the LevelCanvas class for recieving drag and drop operations.
    """
    def __init__(self, parent):
        wx.DropTarget.__init__(self)
        self.parent = parent
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data)

    def OnData(self, x, y, default):
        self.GetData()
        data = self.data.GetText()
        data = data.split("--")
        pos = (int(float(x)/24.0), int(float(y)/24.0))
        if data[1] == "C":
            self.parent.AddChar(pos)
        elif data[1] == "F":
            self.parent.AddGoal(pos)
        return default

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
        self.hole = wx.Image("Data\\slipinator\\hole.png").ConvertToBitmap()
        self.char = wx.Image("Data\\slipinator\\char.png").ConvertToBitmap()
        self.goal = wx.Image("Data\\slipinator\\goal.png").ConvertToBitmap()

        # Initialise variables
        self.pos = pos
        self.parent = parent
        self.blocks = []
        self.holes = []
        self.objects = []
        self.HasChar = False
        self.charpos = None
        self.HasGoal = False
        self.goalpos = None

        #Make it a drop target
        self.droptarget = DropTarget(self)
        self.SetDropTarget(self.droptarget)

        # Bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

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

        # Draw in the holes
        for pos in self.holes:
            dc.DrawBitmap(self.hole, pos[0], pos[1], True)

        # Draw in the character
        if self.HasChar == True:
            dc.DrawBitmap(self.char, self.charpos[0], self.charpos[1], True)

        # Draw in the goal
        if self.HasGoal == True:
            dc.DrawBitmap(self.goal, self.goalpos[0], self.goalpos[1], True)

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
        """
    A method for initialising the blocks and holes to match with the parent object's level data.
        """
        # Clear the block positions list
        self.blocks = []
        # Clear the hole positions list
        self.holes = []
        # Remove the character
        self.HasChar = False
        self.charpos = None
        # Remove the goal
        self.HasGoal = False
        self.goalpos = None
        # For each column in each line, check for symbols in that position and add a block or other
        # object where necessary
        for i in range(0, 20):
            line = i
            for i in range(0, 25):
                column = i
                if self.parent.leveldata[line][column] == "B":
                    self.AddBlock((column, line))
                elif self.parent.leveldata[line][column] == "H":
                    self.AddHole((column, line))
                elif self.parent.leveldata[line][column] == "C":
                    self.AddChar((column, line))
                elif self.parent.leveldata[line][column] == "F":
                    self.AddGoal((column, line))

    def OnLeftClick(self, event):
        """
    A method to process mouse left-click events.
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

            # If there's a hole there, remove it and replace it with a hole
            elif self.parent.leveldata[position[1]][position[0]] == "H":
                self.RemoveHole(position)
                self.AddBlock(position)

            # If there's a character, remove the character and replace it with a block
            elif self.parent.leveldata[position[1]][position[0]] == "C":
                self.HasChar = False
                self.charpos = None
                self.AddBlock(position)

            # If there's a goal, remove it and replace it with a block
            elif self.parent.leveldata[position[1]][position[0]] == "F":
                self.HasGoal = False
                self.goalpos = None
                self.AddBlock(position)

    def OnRightClick(self, event):
        """
    A method to process mouse right-click events.
        """
        # If the mouse click is inside the window
        rawpos = event.GetPosition()
        if rawpos[0]<600 and rawpos[1]<480:
            # Get the grid co-ordinates for the mouse click
            position = (rawpos[0]/24, rawpos[1]/24)

            # If there's nothing in that space, add a hole
            if self.parent.leveldata[position[1]][position[0]] == "0":
                self.AddHole(position)

            # If there's a hole there, remove it
            elif self.parent.leveldata[position[1]][position[0]] == "H":
                self.RemoveHole(position)

            # If there's a block there, remove it and replace it with a hole
            elif self.parent.leveldata[position[1]][position[0]] == "B":
                self.RemoveBlock(position)
                self.AddHole(position)

            # If there's a character, remove the character and replace it with a hole
            elif self.parent.leveldata[position[1]][position[0]] == "C":
                self.HasChar = False
                self.charpos = None
                self.AddHole(position)

            # If there's a goal, remove it and replace it with a hole
            elif self.parent.leveldata[position[1]][position[0]] == "F":
                self.HasGoal = False
                self.goalpos = None
                self.AddHole(position)

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

    def AddHole(self, pos):
        """
    A method which adds a hole to a given grid co-ordinate on the level canvas.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Append it to the list of hole drawing points
        self.holes.append(pixelpos)
        # Modify the parent object (main window)'s level data so there is now a hole in the given
        # position
        self.parent.leveldata[pos[1]][pos[0]] = "H"
        # Refresh the area of the screen in which the hole has been drawn
        self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))

    def RemoveHole(self, pos):
        """
    A method which removes the hole from a given grid co-ordinate on the level canvas.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Go through the list of positions until a position matching the give one is found.
        # "count" keeps a record of the item number
        count = 0
        for item in self.holes:
            # If it's found, remove it
            if str(item) == str(pixelpos):
                self.holes.pop(count)
            # Otherwise, increase the item number
            else:
                count = count+1
        # Modify the parent object (main window)'s level data so there is no longer a hole in the
        # given position
        self.parent.leveldata[pos[1]][pos[0]] = "0"
        # Refresh the area of the screen from which the hole has been erased
        self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))

    def AddChar(self, pos):
        """
    A method which adds the character to a given position.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Only add a character to empty spaces or the character position (bugfix...)
        if self.parent.leveldata[pos[1]][pos[0]] == "0" or self.parent.leveldata[pos[1]][pos[0]] == "C":
            # If there isn't already a character
            if self.HasChar == False:
                self.HasChar = True
                self.charpos = pixelpos
                self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))
            elif self.HasChar == True:
                self.charpos = pixelpos
                self.Refresh()
            self.parent.leveldata[pos[1]][pos[0]] = "C"

    def AddGoal(self, pos):
        """
    A method which adds the level goal to a given position.
        """
        # Get the pixel co-ordinates of the supplied grid position
        pixelpos = (pos[0]*24, pos[1]*24)
        # Only add the goal to empty spaces
        if self.parent.leveldata[pos[1]][pos[0]] == "0" or self.parent.leveldata[pos[1]][pos[0]] == "F":
            # If there isn't already a goal
            if self.HasGoal == False:
                self.HasGoal = True
                self.goalpos = pixelpos
                self.RefreshRect(wx.Rect(pixelpos[0], pixelpos[1], 24, 24))
            elif self.HasGoal == True:
                self.goalpos = pixelpos
                self.Refresh()
            self.parent.leveldata[pos[1]][pos[0]] = "F"

######################################################################TOOLBOX OBJECT #####

class ToolboxObject(wx.Control):
    """
A draggable bitmap used for dragging and dropping objects onto the level canvas.
    """
    def __init__(self, parent, imagepath, objectcode, size=(24, 24), pos=(0, 0)):
        wx.Control.__init__(self, parent, -1, size=size, pos=pos, style=wx.SIMPLE_BORDER)
        self.SetMinSize(size)

        self.imagepath = imagepath
        self.image = wx.Image(self.imagepath).ConvertToBitmap()
        self.objectcode = objectcode
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        background = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(background)
        dc.Clear()
        dc.DrawBitmap(self.image, 0, 0, True)

    def OnLeftDown(self, event):
        data = "%s--%s" % (self.imagepath, self.objectcode)
        dataobject = wx.TextDataObject(data)
        dropsource = wx.DropSource(self)
        dropsource.SetData(dataobject)
        result = dropsource.DoDragDrop(wx.Drag_CopyOnly)

###################################################################### TOOLBOX #############

class Toolbox(wx.MiniFrame):
    def __init__(self, parent):
        wx.MiniFrame.__init__(self, parent, -1, "Toolbox", size=(100, 300))
        self.parent = parent
        self.SetPosition((self.parent.GetPosition()[0]+10, self.parent.GetPosition()[1]+50))
        self.panel = wx.Panel(self, -1)
        self.charbutton = ToolboxObject(self.panel, imagepath="Data\\slipinator\\char.png", objectcode="C", pos=(0, 0))
        self.goalbutton = ToolboxObject(self.panel, imagepath = "Data\\slipinator\\goal.png", objectcode="F", pos=(30, 0))

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
        # Set the frame's icon
        icon = wx.Icon("Data\\slipinator\\icon_small.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # Centre the frame and set its background colour
        self.Centre()
        self.SetBackgroundColour("#FFFFFF")

        # Initialise the level name
        self.levelname = "New level"
        
        # Initialise a variable for whether or not to display the grid
        self.showgrid = True
        
        # Create the massive level data array
        self.leveldata = [
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
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

        # Create and show the toolbox window
        self.toolbox = Toolbox(self)
        self.toolbox.Show()

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
        filedelete = filemenu.Append(-1, "Delete levels", "Delete Slipslide custom levels")
        filemenu.AppendSeparator()
        fileexit = filemenu.Append(-1, "Exit", "Exit the application")
        # Bind file menu events
        self.Bind(wx.EVT_MENU, self.FileNew, filenew)
        self.Bind(wx.EVT_MENU, self.FileOpen, fileopen)
        self.Bind(wx.EVT_MENU, self.FileSave, filesave)
        self.Bind(wx.EVT_MENU, self.FileDelete, filedelete)
        self.Bind(wx.EVT_MENU, self.FileExit, fileexit)
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

        # The help menu
        helpmenu = wx.Menu()
        # Add options
        helptutorial = helpmenu.Append(-1, "How to make levels",
                "A tutorial explaining how to use Slipinator")
        helptips = helpmenu.Append(-1, "Handy tips",
                "A few helpful tips that will help you produce great levels")
        helpmenu.AppendSeparator()
        helpabout = helpmenu.Append(-1, "About", "Information about Slipinator")
        # Bind the help menu events
        self.Bind(wx.EVT_MENU, self.HelpTutorial, helptutorial)
        self.Bind(wx.EVT_MENU, self.HelpTips, helptips)
        self.Bind(wx.EVT_MENU, self.HelpAbout, helpabout)
        # Append the help menu to the menu bar
        self.menubar.Append(helpmenu, "Help")
        
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
        self.canvas.InitPositions()

    def FileNew(self, event):
        self.leveldata = [
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
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
        self.canvas.blocks = []
        self.canvas.holes = []
        self.canvas.HasChar = False
        self.canvas.charpos = None
        self.canvas.HasGoal = None
        self.canvas.goalpos = None
        self.canvas.Refresh()
        self.levelname = "New level"
        self.UpdateTitle()

    def FileOpen(self, event):
        """
    A method which shows a dialog allowing the user to pick a level to open (level names are read
    from the file "Data\\customlevels.dat"), and then opens that level.
        """
        infile = open("Data\\customlevels.dat", "r")
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
                self.levelname = selection
                self.UpdateTitle()
                    

    def FileSave(self, event):
        """
    A method which saves the current file to a Slipslide 2 level folder.
        """
        # The level must have a character start point and a goal to work! Don't save it otherwise
        if self.canvas.HasChar and self.canvas.HasGoal:
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
            shutil.copyfile("Data\\slipinator\\goal.png", "%s\\goal.png" % fixedlevelname)
            # Copy the music to the newly-created folder
            shutil.copyfile("Data\\slipinator\\music.ogg", "%s\\music.ogg" % fixedlevelname)
            # Append the level's name to the list of custom levels, keeping the existing list data
            datafile = open("Data\\customlevels.dat", "r")
            contents = datafile.read().split("\n")
            for i in range(0, len(contents)):
                # Temporary solution to the "Index out of range!!" bug
                try:
                    if contents[i] == fixedlevelname:
                        contents.pop(i)
                except:
                    pass
            contents = "\n".join(contents)
            data = [contents, "\n%s" % fixedlevelname]
            datafile.close()
            data = "".join(data)
            datafile = open("Data\\customlevels.dat", "w")
            datafile.write(data)
            datafile.close()
        else:
            if self.canvas.HasChar == False and self.canvas.HasGoal == False:
                items = ["character", "finish point"]
            elif self.canvas.HasChar == False and self.canvas.HasGoal == True:
                items = ["character"]
            elif self.canvas.HasChar == True and self.canvas.HasGoal == False:
                items = ["finish point"]
            if len(items) == 2:
                message = "The level cannot be saved as you need to add a %s and a %s first!" % (items[0], items[1])
            elif len(items) == 1:
                message = "The level cannot be saved as it needs a %s to work!" % items[0]
            dlg = wx.MessageDialog(self, message, "Level will not work yet!", style = wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def FileDelete(self, event):
        infile = open("Data\\customlevels.dat", "r")
        data = infile.read().split("\n")
        infile.close()
        topline = data[0]
        data.pop(0)
        if len(data) < 1:
            dlg = wx.MessageDialog(self, "No Slipslide 2 custom level files have been saved!",
                    "No levels exist", style = wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            dlg = wx.SingleChoiceDialog(self, "Select a level to delete", "Delete a level", data)
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetSelection()
                dlg = wx.MessageDialog(self,
                        "Are you sure you want to delete %s? Once deleted, it cannot be recovered!" % data[selection],
                        "Confirm level deletion", style=wx.OK|wx.CANCEL|wx.ICON_ERROR)
                if dlg.ShowModal() == wx.ID_OK:
                    data.pop(selection)
                    data = "\n".join(data)
                    data = "%s\n%s" % (topline, data)
                    datafile = open("Data\customlevels.dat", "w")
                    datafile.write(data)
                    datafile.close()
                    ##### THE FOLDER SHOULD THEN BE DELETED AT THIS POINT #####

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
        # If the item is checked, the grid should be shown
        if event.IsChecked():
            self.showgrid = True
        # If it isn't, the grid shouldn't be shown
        else:
            self.showgrid = False
        # Refresh the canvas
        self.canvas.Refresh()

    def HelpTutorial(self, event):
        pass

    def HelpTips(self, event):
        pass

    def HelpAbout(self, event):
        pass

    def UpdateTitle(self):
        newtitle = "%s -- ExeSoft Slipinator (Slipslide 2 level editor)" % self.levelname
        self.SetTitle(newtitle)

###################################################################### MAINLOOP ##########

if __name__ == "__main__":
    app = wx.App()
    frame = Slipinator(None)
    frame.Show(True)
    app.MainLoop()
