import customtkinter as ctk

class CTkTickSlider(ctk.CTkFrame):
    def __init__(self, parent, steps=10, numbers = False, tick_color="gray80", **slider_kwargs):
        super().__init__(parent, fg_color="transparent")

        self.steps = steps
        self.numbers = numbers
        self.tick_color = tick_color

        # Canvas for tick marks
        self.tick_canvas = ctk.CTkCanvas(
            self,
            height=25,
            bg=slider_kwargs.get('bg_color'),
            highlightthickness=0
        )
        self.tick_canvas.grid(row=1, column=0, sticky="ew")

        # Remove number_of_steps if passed twice
        slider_kwargs.pop("number_of_steps", None)

        # Slider widget
        self.slider = ctk.CTkSlider(
            self,
            number_of_steps=self.steps-1,
            **slider_kwargs
        )
        self.slider.grid(row=0, column=0, sticky="ew")

        # Make the frame responsive
        self.grid_columnconfigure(0, weight=1)

        # Redraw ticks when resized
        self.tick_canvas.bind("<Configure>", self._draw_ticks)

    # Draw tick marks
    def _draw_ticks(self, event=None):
        self.tick_canvas.delete("all")
        width = self.tick_canvas.winfo_width()
        if width <= 1:
            return
        
        #slider bar padding (internal CTkSlider value)
        pad = self.slider._corner_radius

        #usable width where the ticks shoudl be drawn
        usable_width = width-pad * 2

        offset = 7.5

        for i in range(self.steps):
            # x = int(pad + (i/self.steps) * usable_width)
            # x = int((i/(self.steps-1)) * width)
            x = int((i*1.02) * (width/self.steps) + offset)
            self.tick_canvas.create_line(
                x, 0, x, 10,
                fill=self.tick_color,
                width=2
            )
            if self.numbers:
                #create the numbers below the lines
                self.tick_canvas.create_text(
                    x,
                    18,
                    text=str(i+1),
                    fill=self.tick_color
                )

    # Convenience passthroughs
    def get(self):
        return self.slider.get()

    def set(self, value):
        self.slider.set(value)

    def configure(self, **kwargs):
        self.slider.configure(**kwargs)

    def update_ticks(self, bg_color):
        self.tick_canvas.configure(bg=bg_color)
