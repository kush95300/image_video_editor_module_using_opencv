
# coding: utf-8

# In[13]:


import cv2
import subprocess as sp
import numpy as np
from tkinter import * 
import random
from tkinter.ttk import *


# In[14]:


def read_image(image_full_path):
    """
    Example: 
    
    image= read_image("path_to_image")
    
    
    Inputs Parameters:
    Image_full_path: enter image_path as string.
    
    Output:
    return numpy array of image.
    
    
    """
    return cv2.imread(image_full_path)


# In[15]:


def split_color(image):
    """
    Example: 
    
    image= split_color(image)
    
    
    Inputs Parameters:
    Image: enter image as numpy array.
    
    Output:
    return tuple of colors list ( like RGB).
    
    
    """
    if image.shape[2] == 2:
        color1,color2=cv2.split(image)
        return (color1,color2)
    elif image.shape[2] == 3:
        color1,color2,color3=cv2.split(image)
        return (color1,color2,color3)
    else:
        print("Image shape not defined.")
        return null
    


# In[16]:


def show_image(image):
    """
    Example: 
    
    image= show_image(image)
    
    Inputs Parameters:
    Image: enter image as numpy array.
    
   
    Output:
    shows image.
    
    
    """
   
    cv2.imshow("change_photo",image)
    cv2.waitKey()
    cv2.destroyAllWindows()


# In[17]:


def show_multi_image(images, time=1):
    """
    Example: 
    
    image= show_multi_image(image, time=2)    # Here images are list of image.
    or
    image = show_multi_image([img1,img2,img3....]) # pass as list with default time 1 sec
    
    Inputs Parameters:
    Images: enter image as list of numpy array. 
    time: time to show one image ( in sec)
    
   
    Output:
    shows image.
    
    
    """

    if type(images) != list:
        show_image(images)
    else:
        for image in images:
            cv2.imshow("change_photo",image)
            cv2.waitKey(time*1000)
        cv2.destroyAllWindows()


# In[18]:


def image_merger(img1, img2, merge_type="first_max", path=False):
    """
    Example: 
    
    image= image_merger(image1, image2, merge_type="first_max")    
    or
    image= image_merger(image1, image2, merge_type="second_max") 
    or
    image= image_merger("path_to_img1", "path_to_img2", merge_type="second_max", path=True)   
    
    Inputs Parameters:
    Img1 , img2: enter image as numpy array or if path is true then path as strings. 
    merge_type: Available merge types are first_merge, second_merge and dummy_color
    path = image path true  ( image path are provide in imag1 and img2)
    
   
    Output:
    merged image in form of numpy array.
    
    
    """
    if path:
        img1=read_image(img1)
        img2=read_image(img2)
    img1 = resize_image(img1,720,1280)
    img2 = resize_image(img2,720,1280)
    image1_color = split_color(img1)
    image2_color = split_color(img2)
    if merge_type=="dummy_color":
        dummy_color=np.zeros((720,1280),dtype="uint8")
        newphoto = cv2.merge((image1_color[0],dummy_color,image2_color[2]))
    elif merge_type == "second_max":
        newphoto = cv2.merge((image1_color[0],image2_color[1],image2_color[2]))
    else:
        newphoto = cv2.merge((image1_color[0],image1_color[1],image2_color[2]))
    crop1=resize_image(img1,90,160)
    crop2=resize_image(img2,90,160)
    newphoto[0:90,0:160]=crop1
    newphoto[0:90,1120:1280]=crop2
    return newphoto

    


# In[19]:


def choice_based_image_merger(img1, img2, choice=[1,2,5], path=False):
    """
    Example: 
    
    image= image_merger(image1, image2, choice=[2,3,4])    
    or
    image= image_merger(image1, image2, chice=[4,2,4]) 
    or
    image= image_merger("path_to_img1", "path_to_img2", merge_type="second_max", path=True)   
    
    Inputs Parameters:
    Img1 , img2: enter image as numpy array or if path is true then path as strings. 
    choice: Available merge types on the basis of input list or all. 
    path = image path true  ( image path are provide in imag1 and img2)
    
    
   
    Output:
    merged image in form of numpy array. If choice is all, then return list of images in form of numpy array.
    
    
    """
    if choice=="all":
        images=[]
        for i in range(7):
            for j in range(7):
                for k in range(7):
                    newimg = choice_based_image_merger(img1,img2,path=path,choice=[i,j,k])
                    images.append(newimg)
        return images
    if path:
        img1=read_image(img1)
        img2=read_image(img2)
    
    img1 = resize_image(img1,720,1280)
    img2 = resize_image(img2,720,1280)
    image1_color = split_color(img1)
    image2_color = split_color(img2)
    dummy_color=np.zeros((720,1280),dtype="uint8")
    colors=[]
    for color in choice:
        color = color%7
        if color==0:
            colors.append(image1_color[0])
        if color==1:
            colors.append(image1_color[1])
        if color==2:
            colors.append(image1_color[2])
        if color==3:
            colors.append(dummy_color)
        if color==4:
            colors.append(image2_color[0])
        if color==5:
            colors.append(image2_color[1])
        if color==6:
            colors.append(image2_color[2])
            
    newphoto = cv2.merge(colors)
    crop1=resize_image(img1, 90,160)
    crop2=resize_image(img2,90,160)
    newphoto[0:90,0:160]=crop1
    newphoto[0:90,1120:1280]=crop2
    return newphoto

    


# In[20]:


def create_random_image(shape=(720,1080,3)):
    """
    Example: 
    
    image= create_random_image()    
    or
    image= create_random_image( shape=(1000,1200,3)) 
    or
    image= create_random_image(shape=img2.shape)   
    
    Inputs Parameters:
    shape = shape of desired created image (optional)
    
   
    Output:
    return image in form of numpy array.
    
    """
    colors=[]
    for i in range(shape[2]):
        colors.append(np.random.randint(low=4,high=200,size=(shape[0],shape[1]),dtype="uint8"))
    image= cv2.merge(tuple(colors))
    return image
        
    
    
    


# In[21]:


def randomly_created_image_show(shape=(720,1080,3),number_of_images=150,time=0):
    """
    Example: 
    
    randomly_created_image_show()    
    or
    randomly_created_image_show(img2.shape, number_of_images=100)
    or
    randomly_created_image_show(img2.shape, number_of_images=100, time=1)
    
    Inputs Parameters:
    shape = shape of desired created image (optional)
    number_of_images =  number of times image created.
    time = time to show a image. 'O' means change on pressing space key.
    
   
    Output:
    show images views. ( like a old TV screen)
    
    """
    images=[]
    for i in range(number_of_images):
        images.append(create_random_image(shape))
    show_multi_image(images,time)
        


# In[22]:


def resize_image(image, rows, columns):
    """
    Example: 
    
    resize_image(img,900,1600)      # gives image in 900x1600 dimentions    
    
    Inputs Parameters:
    image = image as numpy array.
    rows =  number of rows of desired image 
    columns =  number of columns of desired image 
    
   
    Output:
    return desired shape image as numpy array.    
    """
    return cv2.resize(image,(columns,rows))


# In[24]:


def get_screen_resolution(): 
    """
    Example: 
    
    frame=get_screen_resolution()      # gives your screen dimentions    
    
    Output:
    return desired shape image as tupe (column x rows).    
    """
    root=Tk()
    h=root.winfo_screenheight()
    w=root.winfo_screenwidth()
    return (w,h)


# In[43]:


def get_random_color():

    """
    Example: 
    
    color=get_random_color()      # gives random color     
    
    Output:
    return color tuple containing (b,g,r) format.    
    """

    b=random.randint(0,255)
    g=random.randint(0,255)
    r=random.randint(0,255)
    return (b,g,r)

def get_random_coordinate(image):
    """
    Example: 
    
    coordinates= get_random_coordinates()     # gives random x-y coordinates inside image     
    
    Output:
    return tupe (x,y).    
    """
    x,y,z=image.shape
    return (random.randint(0,y),random.randint(0,x))

def random_angle():
    """
    Example: 
    
    angle = random_angle()      # gives random angle     
    
    Output:
    return int angle value in arnge 0-360..    
    """
    return random.randint(0,360)


# In[26]:


def add_text_to_image(image ,message="your msg",font_type=0,font_size=1,color="green",line_type=4,message_postion=1,thickness=2,move=10):
    """
    Example: 
    
    image= add_text_to_image(image)  
    or
    image= add_text_to_image(image, msg="hi world")  
    image= add_text_to_image(image, msg="hi world", color="random")      
    
    inputs:
    
    1. IMage: Image as numpy array
    2. message: text to add to image
    3. color: color of the text. Available colrs are : red, green, blue, black, white, pink, yellow cyan and random.
    4. line_type: type of ;ine to writtern ( any value in 1-4)
    5. message_position : postion where message print . ( any integer number)
    6. Thickness: thickness of text.
    7. Move: space from left to text.
    
    Output:
    return image with added text in numpy array form.    
    """

    if(line_type==0):
        line_type=cv2.FILLED
    elif line_type==1:
        line_type=cv2.LINE_4
    elif line_type==2:
        line_type=cv2.LINE_8
    else:
        line_type=cv2.LINE_AA
    
    if color=="random":
        color=get_random()
    elif color=='black' or color==0:
        color=(0,0,0)
    elif color=="white" or color==1:
        color=(255,255,255)
    elif color=="pink" or color==2:
        color=(255,0,255)
    elif color=="yellow" or color==3:
        color=(0,255,255)
    elif color=="cyan" or color==4:
        color=(255,255,0)
    elif color=="blue" or color==5:
        color=(255,0,0)
    elif color=="green" or color==6:
        color=(0,255,0)
    else:
        color=(0,0,255)
        
    shape=image.shape
   
        
    if  message_postion % 3 == 0:
        message_postion=(move,30)
    elif message_postion % 3 == 1:
    
        message_postion=(move,int((shape[1]/2)))
    else :
        message_postion=(move,shape[1])
   
        
    return cv2.putText(image,message,message_postion, font_type, font_size,color,thickness,line_type)


# In[27]:


#Random Image Creation Functions

# Line Image

def random_line(img,thickness=random.randint(1,20)):
    cv2.line(img,get_random_coordinate(img),get_random_coordinate(img),get_random_color(),thickness)
    
def random_line_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    img = np.zeros(shape, np.uint8)
    
    for i in range(random.randint(1,150)):
        random_line(img)
    return img

def random_line_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_line_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()


# Rectangle Image

def random_rectangle(img,thickness=random.randint(1,15)):
    cv2.rectangle(img,get_random_coordinate(img),get_random_coordinate(img),get_random_color(),thickness)
    
    
def random_rectangle_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    img = np.zeros(shape, np.uint8)
    
    for i in range(random.randint(1,150)):
        random_rectangle(img)
    return img

def random_rectangle_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_rectangle_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()

# Circle Image       

def random_circle(img,thickness=random.randint(1,20),radius=random.randint(1,300)):
    cv2.circle(img,get_random_coordinate(img),radius,get_random_color(),thickness)
    
    
def random_circle_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    img = np.zeros(shape, np.uint8)
    
    for i in range(random.randint(1,50)):
        random_circle(img)
    return img

def random_circle_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_circle_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()


# Ellipse Image
    
def random_ellipse(img,thickness=random.randint(1,15)):
    #cv2.ellipse(img,get_random_coordinate(img),radius,get_random_color(),thickness)
    cv2.ellipse(img,get_random_coordinate(img),(200,100),random_angle(),0,360,get_random_color(),thickness)
    
    
def random_ellipse_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    img = np.zeros(shape, np.uint8)
     
    for i in range(random.randint(1,150)):
        random_ellipse(img)
    return img

def random_ellipse_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_ellipse_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()

# Random Image

def random_shape_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    choose = random.randint(0,3)
    img=0
    if choose==0:
        img = random_line_image(shape)
    elif choose==1:
        img = random_rectangle_image(shape)
    elif choose==2:
        img = random_circle_image(shape)
    elif choose==3:
        img = random_ellipse_image(shape)
        
    return img


def random_shape_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_shape_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()


# Multi Shape Image

def random_shape(img,choose):
    if choose==0:
        random_line(img)
    elif choose==1:
        random_rectangle(img)
    elif choose==2:
        random_circle(img)
    elif choose==3:
        random_ellipse(img)
    return img


def multi_shape_image(shape=(random.randint(500,1020),random.randint(500,1600),3)):    
    img = np.zeros(shape, np.uint8)
    
    for i in range(random.randint(1,150)):
        choose = random.randint(0,3)
    
        img=random_shape(img,choose)
    return img


def multi_shape_image_show(shape=(random.randint(500,1020),random.randint(500,1600),3),time=1):    
    while(True):
        img = random_shape_image(shape)
        cv2.imshow("change_photo",img)
        if cv2.waitKey(time) == 27:
            break
    cv2.destroyAllWindows()




# In[28]:


def selfi_capture(camara_no=0,size_type=1, selfi_folder="selfi", text_move=True, text_moving_speed=10):
    """
    Example: 
    
    selfi_capture()  
    
    output: 
    none  but same image at path  selfi/image
    """
    if text_move:
        i = 10
    else:
        i=15
    size=(0,0)

    if selfi_folder=="selfi":
        try:
            sp.getoutput("mkdir {}".format(selfi_folder))
            print(selfi_folder + " Folder Created")
        except ValueError :
            print("Folder Selected")

    filename = "{}/selfi_{}_{}.jpg".format(selfi_folder, sp.getoutput("echo %time%")[:-3].replace(":","_"),sp.getoutput("echo %date%"))

    lappy = cv2.VideoCapture(camara_no)

    if size_type==0:
        size=(pic1.shape[1],pic1.shape[0])
    elif size_type==1:
        size=get_screen_resolution()
    elif size_type==2:
        size=(1500,900)
    elif size_type==3:
        size=(1200,850)
    elif size_type==4:
        size=(750,600)
    elif size_type==5:
        size=(700,500)
    elif size_type==6:
        size=(600,600)
    elif size_type==7:
        size=(500,500)
    elif size_type==8:
        size=(500,400)
    elif size_type==9:
        size=(400,400)
    elif size_type==10:
        size=(400,280)
    elif size_type==11:
        size=(350,350)
    elif size_type==12:
        size=(350,300)
    elif size_type==13:
        size=(350,250)
    while True:
        status1,pic1=lappy.read()
        if(status1==False):
            print("Camara not Connected..... Something Error...")
        else:
            if size_type==0:
                pic=pic1
            else :
                pic=cv2.resize(pic1,size)

            if(i>pic.shape[1]-100):
                i=0


            if cv2.waitKey(1) == 99:
                cv2.imwrite(filename,pic)
                cv2.destroyAllWindows()
                print("Image saved at "+filename)
                pic=add_text_to_image(image=pic,message="Image Captured",font_size=1,color='green',message_postion=0)
                show_image(pic)
                break


            pic=add_text_to_image(image=pic,message="Press: 'c' to capture selfi  or  'esc' key to stop",font_size=1,color='blue', move=i)

            cv2.imshow("Friend_Editor-Mirror",pic)
            i+=text_moving_speed
            if cv2.waitKey(1) == 27:
                break
    cv2.destroyAllWindows()
    lappy.release()    

    


# In[40]:


def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


def collage_maker(imgs, path=False,size=0.5):
    images=[]
    if path:
        for image_path in imgs:
            image=read_image(image_path)
            images.append(image)
    else:
        images = imgs
    print(len(images))
    
    if len(images) == None:
        return "No Image Specified"
    elif len(images) == 2:
        img=[]
        for i in images:
            i = cv2.resize(i, dsize=(0, 0), fx=size, fy=size)
            img.append(i)
            print(i.shape)
        print(img[0].shape)
        collage = concat_tile([[img[0],img[1]]])
        return collage
        
       
   
    else:
        return "you can make collage of 4 images only."
        return image