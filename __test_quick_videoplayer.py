# -*- coding: utf-8 -*-
"""Created on Wed Sep 18 15:29:42 2024@author: Alexm"""

   



def make_images0():
    import numpy as np
    import os
    
    def imshow(image, title=''):
        import matplotlib.pyplot as plt
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.axis('off')  # Hide axes
        plt.show()
        
    def resize_with_padding(image_path, target_width, target_height):
        from PIL import Image, ImageOps
        image = Image.open(image_path)
        image.thumbnail((target_width, target_height), Image.ANTIALIAS)
        new_image = Image.new("RGB", (target_width, target_height), (0, 0, 0))
        paste_position = ((target_width - image.width) // 2, (target_height - image.height) // 2)
        new_image.paste(image, paste_position)
        image_array = np.array(new_image)
        return image_array    
        
    folder = r'C:\Users\Alexm\Desktop\Organized Images\_FacesWomen\_New'
    filepaths = os.listdir(folder)
    filepaths = [os.path.join(folder, f) for f in filepaths]
    filepaths = [f for f in filepaths if '.jpg' in f]   
    images0 = [resize_with_padding(filepath,  300, 400) for filepath in filepaths]
    images0 = np.stack(images0, -1)
    return images0



images0 = make_images0()

from quick_videoplayer import videoplayer
videoplayer(images0)