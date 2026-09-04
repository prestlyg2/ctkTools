import customtkinter as ctk
#takes in a list of lists (the interior lists contain the colors for the color scheme)
#makes a window that is a child of the parent and displays the color scheme
def color_schemes_tester(parent, color_schemes: list):
    #get the screen width and height
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    #create a window that is a child of the parent window
    win = ctk.CTkToplevel(parent)
    win.title("Color Scheme Tester")
    #set the win size
    winSize = [900, 450]
    #set the starting x and y location of the window so it is in the middle of the screen
    winStartX = int((screen_width/2) - (winSize[0]/2))
    winStartY = int((screen_height/2) - (winSize[1]/2))

    #set the geometry of the window
    win.geometry(f"{winSize[0]}x{winSize[1]}+{winStartX}+{winStartY}")
    win.minsize(*winSize)

    #loop through the nubmer of color schemes in color_schemes
    for i in range(len(color_schemes)):
        #create a scrollable frame to hold all of the colors for the color scheme
        scrollableFrame = ctk.CTkScrollableFrame(
            win,
            orientation="vertical"
        )
        scrollableFrame.place(relx=((1/(i+1))*i), rely=0.0, relwidth=(1/len(color_schemes)), relheight=1.0)

        #populate the scrollable frame with the boxes of the colors of the colorscheme
        for j in range(len(color_schemes[i])):
            #create a box to hold the color
            box = ctk.CTkFrame(
                scrollableFrame,
                fg_color=color_schemes[i][j],
                height=100
            )
            box.pack(fill="x")