import PIL as pil #import pil so we can load images and make a dictionary with all of the images
import glob #used for looping through files in directories
import customtkinter as ctk #used for loading the image as a CTkImage



#load all of the images (loop through all of the images and load them into the dictionary with a proper name)
def loadImages(imagesPath: str, imageSize: int, multipleColorModes = False):
    # *imagesPath = "Images" #the directory that the images are located inside of
    #this is the dictionary that will be returned with all of the information about the images
        #* information stored:
            #* image Name
            #* ctk.CTkImage
            #* aspect ratio
    images = {} #the images that are used in the program 

    numImages = 0 #the number of iterations where an image is added to images

    #loop through the directory
    for image in glob.glob(f"{imagesPath}/*.png"):
        #print(image) #the path of the image
        lightImage = True #is this the light image or the light image that we are working with

        # #condence the image path by getting rid of the imagesPath/ and the .png at the end
        condensedImage = image[(len(imagesPath)+1):(len(image)-4)] #the image name

        #find the _light or _dark in the image
        imageMode = condensedImage.find("_light")
        if imageMode == -1:
            imageMode = condensedImage.find("_dark")
            lightImage = False #we are working with the dark image

        #use the imageMode information to condense the image further
        condensedImage = condensedImage[:imageMode]

        if multipleColorModes:
            #loop through the images to see if the dark (or light) of the image has already been added
            imageExists = False # a boolean that says if the image exists in the dictionary that is getting returned
            for i in images:
                if i == condensedImage:
                    imageExists = True
                    break

            if not imageExists:
                #increase the num of images
                numImages += 1

                if lightImage:
                    #load the light image using PIL
                    imagePilLight = pil.Image.open(image)
                    #load the dark image
                    imagePilDark = pil.Image.open(f"{imagesPath}/{condensedImage}_dark.png")
                    
                    #print out the light and dark image
                    # print(f"#{numImages} | light Image: {image}\n  - darkImage: {f"{imagesPath}/{condensedImage}_dark.png"}")
                else:
                    #load the dark image
                    imagePilDark = pil.Image.open(image)
                    #load the light image
                    imagePilLight = pil.Image.open(f"{imagesPath}/{condensedImage}_light.png")

                    #print out the light and dark image
                    # print(f"# {numImages} | light Image: {f"{imagesPath}/{condensedImage}_light.png"}\n  - darkImage: {image}")

                
                #get the aspect ratio
                aspectRatio = imagePilLight.width / imagePilDark.height

                #create the ctkImage
                imageCTK = ctk.CTkImage(light_image=imagePilDark, dark_image=imagePilLight, size=(imageSize, imageSize))

                #add the information to the dictionary
                images[condensedImage] = {
                    'ctkImage': imageCTK,
                    'aspectRatio': aspectRatio,
                    'pilLight' : imagePilLight,
                    'pilDark' : imagePilDark
                }

        else:#if the user doesn't want multiple color modes and their images do not reflect that they do
            #increase the num of images
            numImages += 1

            #load the image using PIL
            imagePil = pil.Image.open(image)

            #get the aspect ratio
            aspectRatio = imagePil.width / imagePil.height

            #create the ctk Image
            imageCTK = ctk.CTkImage(light_image=imagePil, size=(imageSize, imageSize))

            #add the information to the dictionary
            images[condensedImage] = {
                    'ctkImage': imageCTK,
                    'aspectRatio': aspectRatio,
                    'pilLight' : imagePil
                }

    # print(numImages)
    return images
