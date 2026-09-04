import tkinter as tk
import customtkinter as ctk

#create a class that will create tooltips to pop up when buttons are hovered over!
class ToolTip:
    #define a constructor
    def __init__(self, widget, text, color, txtColor):
        self.widget = widget #the widget (parent) that the tool tip needs to describe
        self.text = text
        self.color = color
        self.txtColor = txtColor
        self.tip_window = None
        self.label = None   # store label reference

        #bind the functions
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
        widget.bind("<Motion>", self.follow_mouse)  # Track mouse movement

    #define a function that makes the tooltip pop up
    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return

        #create a small window for the tooltip to appear in
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)

        #create the tool tip
        self.label = tk.Label(
            tw,
            text=self.text,
            background=self.color,
            foreground=self.txtColor,
            relief="solid",
            borderwidth=1,
            font=("Arial", 12)
        )
        self.label.pack(ipadx=5, ipady=2)

        #call the follow mouse function
        self.follow_mouse(event)  # Position it initially

    #define a function to make the tooltip follow the mouse
    def follow_mouse(self, event):
        if self.tip_window:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tip_window.wm_geometry(f"+{x}+{y}")

    #create a function to hide the tooltip
    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    #update the tool tip when the color scheme changes
    def update_colors(self, bg, fg):
        self.color = bg
        self.txtColor = fg

        # If tooltip is currently visible, update it live
        if self.label and self.label.winfo_exists():
            self.label.configure(background=bg, foreground=fg)
        if self.tip_window and self.tip_window.winfo_exists():
            self.tip_window.configure(background=bg)
