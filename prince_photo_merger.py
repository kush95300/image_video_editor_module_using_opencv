
# coding: utf-8

# In[1]:


from image_processing.functions import *


# In[2]:


photo1=read_image("images/test1.jpg")
photo2=read_image("images/test2.jpg")
photo3=read_image("images/test3.jpg")
photo4=read_image("images/test4.jpg")
photo5=read_image("images/test5.jpg")
photo6=read_image("images/test6.jpg")
photo7=read_image("images/test7.jpg")
pop=read_image("images/pop.jpg")


# In[3]:



show_image(pop)
show_image(photo4)

merged=choice_based_image_merger(img1=pop,img2=photo4,choice=[2,3,4])

show_image(merged)


# In[ ]:





# In[ ]:





# In[ ]:




