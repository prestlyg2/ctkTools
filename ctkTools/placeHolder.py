import customtkinter as ctk
import tkinter as tk

def _noop_activate_placeholder(self):
    return

ctk.CTkEntry._activate_placeholder = _noop_activate_placeholder

class placeHolder:
    def __init__(self, entry: ctk.CTkEntry, placeHolderText: str, textColor: str = "#000000", function = lambda x: None):
        self.entry = entry
        self.placeHolderText = placeHolderText
        self.textColor = textColor
        self.function = function

        self.placeHolderTextColor = "#7A7a7a"
        self._active = False

        self.apply_placeholder()

    def _widget_exists(self):
        try:
            self.entry.winfo_exists()
            return True
        except tk.TclError:
            return False

    def apply_placeholder(self):
        #check if the widget exists
        if not self._widget_exists():
            return

        current = self.entry.get()
        if current is None or current == "" or current == "None" or current == self.placeHolderText:
            # entry is empty — show placeholder
            self.entry.delete(0, "end")
            self.entry.insert(0, self.placeHolderText)
            self.entry.configure(text_color=self.placeHolderTextColor)
            self._active = True
        else:
            # entry already has user text — keep it and normal color
            self.entry.configure(text_color=self.textColor)
            self._active = False

        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restor_placeholder)
        self.entry.bind("<Return>", self.restor_placeholder)

    def clear_placeholder(self, event):
        #check if the widget exists
        if not self._widget_exists():
            return

        # only clear if the placeholder is active and the content matches it
        if self._active and self.entry.get() == self.placeHolderText:
            self.entry.delete(0, "end")
            self.entry.configure(text_color=self.textColor)
            self._active = False

    def restor_placeholder(self, event):
        #check if the widget exists 
        if not self._widget_exists():
            return

        text = self.entry.get()
        # empty => restore placeholder
        if text == "" or text is None:
            self.entry.delete(0, "end")
            self.entry.insert(0, self.placeHolderText)
            self.entry.configure(text_color=self.placeHolderTextColor)
            self._active = True
        else:
            # real user text — mark inactive and call the provided function
            self._active = False
            self.entry.configure(text_color=self.textColor)
            try:
                self.function(text)
            except Exception:
                pass