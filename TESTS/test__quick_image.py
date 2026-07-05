# -*- coding: utf-8 -*-
"""Created on Wed Nov 29 15:21:05 2023@author: alexm


so color is a bit skward 0256 or 0-1


Future to Add
  -insert_image, so give (x,y) of top left corner and a array and inserts in other array
  -insert_text in image, (x,y), text, font_size insert this text into image, 
                    return_info, returns extra info like size of text rextangle
  -concatinate
  -mulitple images with titles, works with dicts
  -image normalization
  -segment_color
  -fill image ?
  -image histogram

"""


import quick_image
dir(quick_image)

from quick_image import image, image_show
RED = quick_image.color_dict['red']
BLUE = quick_image.color_dict['blue']

image_show(image)

image_blurred = quick_image.add_blurring_to_image(image)
image_show(image_blurred) 

image_new_box = quick_image.add_box_to_image(image, ((20,20), (120,200)), clr=BLUE)
image_show(image_new_box) 

image_noise = quick_image.add_noise_to_image(image, )
image_show(image_noise) 

quick_image.is_image_color(image) # simple justs tests if image is color



if True:
# These have Not been tested
 'color_apply',
 'image_show_popout',
