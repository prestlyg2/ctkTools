import tkinter as tk #used for creating the window
import customtkinter as ctk #used for creating the window (making it astetically appealing)
import glob #used for searching through the directory for files
import ctkTools #import ctkTools to use the image loader
import os #used for checking if a path is a file or a folder
import json #used for creating files


#create a class that will give a pop up window that allows the user to search for a file or a location to save the current file.
class FILEsearch:
    #MARK: -Constructor
    #define a constructor
    def __init__(self, parent, searchType: str = "open", saveType: str = ".json", fileTypes: list = [("All Files", "*.*")], startingLocation: str = "/Users/", colors: dict = {"fg": "#FFFFFF", "hover": "#CCCCCC", "txt": "#000000"}):
        self.parent = parent #the parent window that this window is a child of
        self.searchType = searchType #the type of search (open or save)
        self.saveType = saveType #the type of file to save as
        self.fileTypes = fileTypes #the types of files that can be searched for
        self.filepath = startingLocation #the directory that the window will open up in
        self.colors = colors #the colors for the window

        self.images = ctkTools.loadImages("/Users/prestlyg12/VScode/Python/ctkTools/ctkTools/FileSearchImages", 64, True) #load the images that will be used for the files and folders inside of the directories
        self.resize_buttons() #set up the back button image

        #create a variable to hold the name of the file being saved
        self.fileNameEntryVar = ctk.Variable(value="")

        #create a variable to hold the selected file path
        self.selectedFilePath = None

        self.setup_window() #set up the window

        self.directoryDisplay() #display the directory contents to begin

    #set up the back button image so that it is smaller than the other images
    def resize_buttons(self):
        #set a constant button size for the three buttons
        buttonSize = (40, 40) #the size of the button images

        #create new images that are resized for the buttons
        self.backButtonImage = ctk.CTkImage(
            light_image=self.images['arrowshape.backward@5x']['pilDark'],
            dark_image=self.images['arrowshape.backward@5x']['pilLight'],
            size=buttonSize
        )
        self.cancelButtonImage = ctk.CTkImage(
            light_image=self.images['x.circle@5x']['pilDark'],
            dark_image=self.images['x.circle@5x']['pilLight'],
            size=buttonSize
        )
        self.selectButtonImage = ctk.CTkImage(
            light_image=self.images['checkmark.circle@5x']['pilDark'],
            dark_image=self.images['checkmark.circle@5x']['pilLight'],
            size=buttonSize
        )

    #MARK: -Window Setup
    #set up the window
    def setup_window(self):
        #create the window
        self.win = ctk.CTkToplevel(self.parent)
        self.win.title(f"{self.searchType} -- {self.filepath}")
        #set the size of the window
        windowSize = [800, 500]
        windowStartx = int((self.parent.winfo_screenwidth()/2) - (windowSize[0]/2))
        windowStarty = int((self.parent.winfo_screenheight()/2) - (windowSize[1]/2))
        self.win.geometry(f"{windowSize[0]}x{windowSize[1]}+{windowStartx}+{windowStarty}")
        self.win.minsize(800, 500)
        self.win.maxsize(800, 500)

        #make the window stay on top of the parent window and focus on it
        self.win.grab_set() #make the window modal
        self.win.focus_set() #focus on the window
        self.win.transient(self.parent) #make the window a transient window (always on top of the parent)
        self.win.resizable(False, False) #make the window not resizable
        # self.wait_window(self.win) #wait for the window to be closed

    #create a function to select a file
    def select_file(self, path: str, scrollPos: tuple = (0.0, 1.0)):
        if path == self.selectedFilePath:
            self.selectedFilePath = None #deselect the file if it is already selected
        else:
            self.selectedFilePath = path #set the selected file path to the path that was passed in

        self.directoryDisplay(scrollPos) #redraw the directory display

    #create a function to open a folder
    def open_folder(self, path: str):
        self.filepath = path #set the current file path to the path that was passed in
        self.directoryDisplay() #redraw the directory display

    #create a function to go back a directory
    def go_back_directory(self):
        #get the parent directory of the current file path
        parentDirectory = os.path.dirname(self.filepath)
        #set the current file path to the parent directory
        self.filepath = parentDirectory
        self.directoryDisplay() #redraw the directory display

    #create a function to select the current selected file and close the window
    def select_current_file(self):
        if self.searchType == "save" or self.searchType == "export":
            #create a new file with the name in the entry box
            fileName = self.fileNameEntry.get() if hasattr(self, "fileNameEntry)") else self.fileNameEntryVar.get() #get the file name from the entry box
            if fileName:
                #create the full file path
                self.selectedFilePath = os.path.join(self.filepath, f"{fileName}{self.saveType}")
            else:
                self.cancel_selection() #if the file name is blank/ there is no file name, cancel the selection
                return

        self.win.destroy() #close the window
        return self.selectedFilePath #return the selected file path

    #create a function to get the selected file path
    def getSelectedFile(self):
        self.win.wait_window() #wait for the window to be closed
        return self.selectedFilePath #return the selected file path

    #create a function to cancel the file selection and close the window
    def cancel_selection(self):
        self.selectedFilePath = None #set the selected file path to None
        self.win.destroy() #close the window

    #MARK: -New Folder Creation
    #create a function to create a new folder in the current directory
    def create_new_folder(self):
        #create a popup window to get the name of the new folder
        newFolderWin = ctk.CTkToplevel(self.win)
        newFolderWin.title("Create New Folder")
        newFolderStartX = int((self.win.winfo_screenwidth()/2) - (300/2))
        newFolderStartY = int((self.win.winfo_screenheight()/2) - (100/2))
        newFolderWin.geometry(f"300x100+{newFolderStartX}+{newFolderStartY}")
        newFolderWin.minsize(300, 100)
        newFolderWin.maxsize(300, 100)
        #keep the new folder window on top
        newFolderWin.grab_set()
        newFolderWin.focus_set()
        newFolderWin.transient(self.win)
        newFolderWin.resizable(False, False)

        #create an entry box to hold the name of the new folder
        newFolderEntry = ctk.CTkEntry(
            newFolderWin,
            placeholder_text="Enter Folder Name",
            font=("Arial", 12),
            fg_color=self.colors['fg'],
            border_color=self.colors['txt'],
            text_color=self.colors['txt'],
            width=200
        )
        newFolderEntry.pack(pady=10)

        #create a button to create the new folder
        def create_folder():
            folderName = newFolderEntry.get() #get the name of the folder from the entry box
            if folderName:
                newFolderPath = os.path.join(self.filepath, folderName) #create the full path of the new folder
                try:
                    os.makedirs(newFolderPath) #create the new folder
                except FileExistsError:
                    pass #if the folder already exists, do nothing
                newFolderWin.destroy() #close the popup window
                # self.directoryDisplay() #redraw the directory display

            #set the current view to the new folder
            self.open_folder(newFolderPath)

        createButton = ctk.CTkButton(
            newFolderWin,
            text="Create Folder",
            font=("Arial", 16),
            text_color=self.colors['txt'],
            fg_color=self.colors['fg'],
            border_color=self.colors['txt'],
            border_width=2,
            hover_color=self.colors['hover'],
            command=create_folder
        )
        createButton.pack(pady=5)


    #MARK: -Click Effect
    # Hover effect
    def make_on_enter(self, frame, button, label):
        def on_enter(event):
            frame.configure(fg_color=self.colors['hover'])
            button.configure(fg_color=self.colors['hover'])
            label.configure(fg_color=self.colors['hover']) if label is not None else None
        return on_enter

    #when the mouse leaves the button
    def make_on_leave(self, frame, button, label):
        return lambda event: (frame.configure(fg_color=self.colors['fg']), button.configure(fg_color=self.colors['fg']), label.configure(fg_color=self.colors['fg'] if label is not None else None))

    # Click effect
    def make_on_click(self, frame, button, label, type="file", path="", scroll_getter=None):
        def on_click(event):
            #flash effect
            frame.configure(fg_color=self.colors['hover'])
            button.configure(fg_color=self.colors['hover'])
            label.configure(fg_color=self.colors['hover']) if label is not None else None

            def reset_color():
                frame.configure(fg_color=self.colors['fg'])
                button.configure(fg_color=self.colors['fg'])
                label.configure(fg_color=self.colors['fg']) if label is not None else None
            frame.after(100, reset_color) #reset the color after 100 milliseconds

            # obtain current scroll position via the provided getter (if any)
            try:
                current_scroll = scroll_getter() if callable(scroll_getter) else (0.0, 1.0)
            except Exception:
                current_scroll = (0.0, 1.0)

            if type == "file":
                self.select_file(path, current_scroll) #call the select file function with current scroll
            elif type == "folder":
                self.open_folder(path) #call the open folder function
        return on_click

    #MARK: -Directory Display
    #write a function to check if a file is allowed based on fileTypes
    def is_allowed_file(self, path):
        if not os.path.isfile(path):
            return True  # folders are always allowed
        for _, ext in self.fileTypes:
            if ext == "*.*":
                return True
            extensions = ext.split(';')
            for e in extensions:
                if e.startswith('*'):
                    suffix = e[1:]  # remove *
                    if path.lower().endswith(suffix.lower()):
                        return True
        return False

    #write a function to check the path and see what files are in the path before displaying thos files as files and folders
    def directoryDisplay(self, scrollPos: tuple = (0.0, 1.0)):
        #update the window title
        self.win.title(f"{self.searchType} -- {self.filepath}")
        #clear the window of all widgets
        for widget in self.win.winfo_children():
            widget.destroy()

        #add a frame inside of the window to hold the files and folders
        filesFrame = ctk.CTkScrollableFrame(
            self.win,
            fg_color=self.colors["fg"]
        )
        filesFrame.columnconfigure((0,1), weight=1) #make both columns expand equally

        # filesFrame.bind_all("<MouseWheel>", lambda event: print(filesFrame._scrollbar.get()))

        #set up the grid for the filesFrame
        maxColumns = 2 #the maximum number of columns that can be displayed
        colCount = 0 #the current column count
        rowCount = 0 #the current row count

        #loop through everything inside of the current directory and displaay it as a file or folder
        for path in glob.glob(f"{self.filepath}/*"):
            #skip files that are not in the allowed list of file types
            if not self.is_allowed_file(path):
                continue
            
            #check if the file is selected and add a border if it is
            if self.selectedFilePath == path:
                borderColor = "#1FFF71" #green border if the file is selected
            else:
                borderColor = self.colors["fg"] #no border if the file is not selected

            #create a frame that holds the files/folders and their names in a line
            fileFolderFrame = ctk.CTkFrame(
                filesFrame,
                fg_color=self.colors['fg'],
                border_color=borderColor,
                border_width=3
            )
            fileFolderFrame.grid(row=rowCount, column=colCount, sticky="w", padx=10, pady=2)
            fileFolderFrame.grid_columnconfigure((1), weight=1) #make the first column (the button) not expand and the second column (the label) expand

            #create a label that displays the name of the file or folder beside the button
            nameLabel = ctk.CTkLabel(
                fileFolderFrame,
                text=path.split("/")[-1],
                # fg_color=self.colors['fg'],
                text_color=self.colors['txt'],
                font=("Arial", 18),
                wraplength=250,
                justify="left"
            )
            nameLabel.grid(row=0, column=1, pady=5, padx=10, sticky="w")

            #check if the path is a file, and if the file ends with one of the allowed file types
            if os.path.isfile(path):
                #display the file using a button (making the tool tip the file name/ path)
                fileButton = ctk.CTkButton(
                    fileFolderFrame,
                    text=" ",
                    image=self.images["document@5x"]['ctkImage'],
                    fg_color=self.colors["fg"],
                    # border_color=borderColor,
                    # border_width=3,
                    hover_color=self.colors['hover'],
                    width=40,
                    height=40,
                    # command=lambda p=path: self.select_file(p) #use a lambda to pass in the path to the select_file function
                )
                #add a tooltip to the button that displays the file name
                # toolTip = ctkTools.ToolTip(
                #     fileButton,
                #     text=path.split("/")[-1],
                #     color=self.colors["fg"],
                #     txtColor=self.colors["txt"]
                # )
                fileButton.grid(row=0, column=0, pady=5, padx=5)

                #before binding the functions, check if the mode is save or export and if it is, disable selecting files
                if self.searchType == "save" or self.searchType == "export":
                    #disable the file button
                    fileButton.configure(state="disabled")
                else:
                    #file button bind
                    #so it is in sinc with the frame and label
                    fileButton.bind("<Enter>", self.make_on_enter(fileFolderFrame, fileButton, nameLabel))
                    fileButton.bind("<Leave>", self.make_on_leave(fileFolderFrame, fileButton, nameLabel))
                    fileButton.bind("<Button-1>", self.make_on_click(fileFolderFrame, fileButton, nameLabel, "file", path, scroll_getter=lambda: filesFrame._scrollbar.get()))

                    #bind the functions to the enter and leave of the mouse (and click)
                    fileFolderFrame.bind("<Enter>", self.make_on_enter(fileFolderFrame, fileButton, nameLabel))
                    fileFolderFrame.bind("<Leave>", self.make_on_leave(fileFolderFrame, fileButton, nameLabel))
                    fileFolderFrame.bind("<Button-1>", self.make_on_click(fileFolderFrame, fileButton, nameLabel, "file", path, scroll_getter=lambda: filesFrame._scrollbar.get()))
                    #name label bind
                    nameLabel.bind("<Enter>", self.make_on_enter(fileFolderFrame, fileButton, nameLabel))
                    nameLabel.bind("<Leave>", self.make_on_leave(fileFolderFrame, fileButton, nameLabel))
                    nameLabel.bind("<Button-1>", self.make_on_click(fileFolderFrame, fileButton, nameLabel, "file", path, scroll_getter=lambda: filesFrame._scrollbar.get()))
            elif os.path.isdir(path):
                #display the folder as a button (making the tool tip the folder name/ path)
                folderButton = ctk.CTkButton(
                    fileFolderFrame,
                    text=" ",
                    image=self.images["folder.fill@5x"]['ctkImage'],
                    fg_color=self.colors["fg"],
                    hover_color=self.colors['hover'],
                    width=40,
                    height=40,
                    command=lambda p=path: self.open_folder(p) #use a lambda to pass in the path to the open_folder function
                ) 
                #add a tooltip to the button that displays the folder name
                # toolTip = ctkTools.ToolTip(
                #     folderButton,
                #     text=path.split("/")[-1],
                #     color=self.colors["fg"],
                #     txtColor=self.colors["txt"]
                # )
                folderButton.grid(row=0, column=0, pady=5, padx=5)

                #folder button bind
                #so it is in sinc with the frame and label
                folderButton.bind("<Enter>", self.make_on_enter(fileFolderFrame, folderButton, nameLabel))
                folderButton.bind("<Leave>", self.make_on_leave(fileFolderFrame, folderButton, nameLabel))
                folderButton.bind("<Button-1>", self.make_on_click(fileFolderFrame, folderButton, nameLabel, "folder", path))

                #bind the functions to the enter and leave of the mouse (and click)
                fileFolderFrame.bind("<Enter>", self.make_on_enter(fileFolderFrame, folderButton, nameLabel))
                fileFolderFrame.bind("<Leave>", self.make_on_leave(fileFolderFrame, folderButton, nameLabel))
                fileFolderFrame.bind("<Button-1>", self.make_on_click(fileFolderFrame, folderButton, nameLabel, "folder", path))
                #name label bind
                nameLabel.bind("<Enter>", self.make_on_enter(fileFolderFrame, folderButton, nameLabel))
                nameLabel.bind("<Leave>", self.make_on_leave(fileFolderFrame, folderButton, nameLabel))
                nameLabel.bind("<Button-1>", self.make_on_click(fileFolderFrame, folderButton, nameLabel, "folder", path))
            colCount += 1
            if colCount >= maxColumns:
                colCount = 0
                rowCount += 1

        #create a frame that is invisible but holds the buttons at the bottom of the screen so that the buttons expand fulling to the width of the screen
        buttonFrame = ctk.CTkFrame(
            self.win,
            height=70,
            fg_color=self.colors['fg']
        )
        buttonFrame.pack(fill="x", side="bottom")

        buttonFrame.columnconfigure((0,1,2), weight=1) #make all three columns expand equally

        #check if the mode is save and if it is make an area for the file name and folder creation
        if self.searchType == "save" or self.searchType == "export":
            #create a frame to hold the file name entry and new folder button
            fileSaveFrame = ctk.CTkFrame(
                buttonFrame,
                fg_color=self.colors['fg']
            )
            fileSaveFrame.grid(row=0, column=0, columnspan=3, sticky="nesw")

            #configure the columns
            fileSaveFrame.columnconfigure((0), weight=1) #make both columns expand equally

            #define the placeholder text
            placeholderText = "Enter File Name"

            #create an entry box to hold the file name
            self.fileNameEntry = ctk.CTkEntry(
                fileSaveFrame,
                font=("Arial", 12),
                fg_color=self.colors['fg'],
                border_color=self.colors['txt'],
                # text_color="#7a7a7a" if self.fileNameEntryVar == "" else self.colors['txt'],
                text_color = self.colors['txt'],
                width=150,
                textvariable=self.fileNameEntryVar,
                placeholder_text=None
            )
            self.fileNameEntry._placeholder_text = None #disable the built in placeholder
            self.fileNameEntry.grid(row=0, column=0, sticky="nesw", padx=5)
            ctkTools.placeHolder(self.fileNameEntry, placeholderText, self.colors['txt']) #add a placeholder to the entry when the entry is empty


            #create a label to show the file type that will be exported
            fileTypeLabel = ctk.CTkLabel(
                fileSaveFrame,
                text=f"{self.saveType}",
                fg_color=self.colors['fg'],
                text_color=self.colors['txt'],
                font=("Arial", 16)
            )
            fileTypeLabel.grid(row=0, column=1, padx=5, sticky="nesw")


            #create a button that will make a popup window to create a new folder in the current directory
            newFolderButton = ctk.CTkButton(
                fileSaveFrame,
                text="New Folder",
                font=("Arial", 16),
                text_color=self.colors['txt'],
                fg_color=self.colors['fg'],
                border_color=self.colors['txt'],
                border_width=2,
                hover_color=self.colors['hover'],
                command=self.create_new_folder #call the create_new_folder function when clicked
            )
            newFolderButton.grid(row=0, column=2, sticky="nes", padx=5)

        #create a back button that will go back to the previous directory if possible and is located at the bottom of the screen
        backButton = ctk.CTkButton(
            buttonFrame,
            text=" ",
            image=self.backButtonImage,
            fg_color=self.colors['fg'],
            border_color=self.colors['txt'],
            border_width=2,
            hover_color=self.colors['hover'],
            command=self.go_back_directory #call the go_back_directory function when clicked
        )
        backButton.grid(row=1, column=0, pady=5, padx=5, sticky="nesw")

        #create a cancel button that will close the window without selecting a file
        cancelButton = ctk.CTkButton(
            buttonFrame,
            text=" ",
            image=self.cancelButtonImage,
            fg_color=self.colors['fg'],
            border_color=self.colors['txt'],
            border_width=2,
            hover_color=self.colors['hover'],
            command=self.cancel_selection #close the window when clicked
        )
        cancelButton.grid(row=1, column=1, pady=5, padx=5, sticky="nesw")

        #create a select button that will close the window and return the selected file path
        selectButton = ctk.CTkButton(
            buttonFrame,
            text=" ",
            image=self.selectButtonImage,
            fg_color=self.colors['fg'],
            border_color=self.colors['txt'],
            border_width=2,
            hover_color=self.colors['hover'],
            command=self.select_current_file #close the window when clicked and return the selected file path
        )
        selectButton.grid(row=1, column=2, pady=5, padx=5, sticky="nesw")

        #update the directory display so that it is always up to date with the selections
        # filesFrame.after(1000, self.directoryDisplay)
        # self.win.update_idletasks()

        #set the initial scroll position
        def restore_scroll_position():
            try:
                # ensure a valid tuple and clamp the value to [0,1]
                if scrollPos and isinstance(scrollPos, (list, tuple)) and len(scrollPos) >= 1:
                    val = float(scrollPos[0])
                    val = max(0.0, min(1.0, val))
                    filesFrame._parent_canvas.yview_moveto(val)
            except Exception as e:
                print("Scroll restore failed: " , e)

        #delay restoring the scroll position to ensure the frame is fully rendered
        # filesFrame.after(1, restore_scroll_position)
        filesFrame.update_idletasks()
        restore_scroll_position()

        #pack the files frame to fill the window
        filesFrame.pack(fill="both", expand=True)