
# coding: utf-8

# In[7]:


import cv2, numpy as np


# In[8]:


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


# In[9]:


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
    


# In[10]:


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


# In[11]:

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
    img1 = cv2.resize(img1,(1280,720))
    img2 = cv2.resize(img2,(1280,720))
    image1_color = split_color(img1)
    image2_color = split_color(img2)
    if merge_type=="dummy_color":
        dummy_color=np.zeros((720,1280),dtype="uint8")
        newphoto = cv2.merge((image1_color[0],dummy_color,image2_color[2]))
    elif merge_type == "second_max":
        newphoto = cv2.merge((image1_color[0],image2_color[1],image2_color[2]))
    else:
        newphoto = cv2.merge((image1_color[0],image1_color[1],image2_color[2]))
    crop1=cv2.resize(img1,(160,90))
    crop2=cv2.resize(img2,(160,90))
    newphoto[0:90,0:160]=crop1
    newphoto[0:90,1120:1280]=crop2
    return newphoto

    

    
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
    
    img1 = cv2.resize(img1,(1280,720))
    img2 = cv2.resize(img2,(1280,720))
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
    crop1=cv2.resize(img1,(160,90))
    crop2=cv2.resize(img2,(160,90))
    newphoto[0:90,0:160]=crop1
    newphoto[0:90,1120:1280]=crop2
    return newphoto

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
        
    
    
    
