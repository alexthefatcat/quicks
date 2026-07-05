# -*- coding: utf-8 -*-
"""Created on Mon Oct  9 12:10:06 2023@author: alexm

add canndy edge? here
maybe histogram

"""

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from numpy import array as Array

from quick_example import image



def image_read(filepath: str) -> Array:
    from PIL import Image
    img_pil = Image.open(filepath)
    img = np.asarray(img_pil)
    img = img/255
    return img

def image_show(*imgs, titles=None):
    '''
    Future pop out
     size of image should be exact so pixel for pixel image
     with titles as optional
     black and white
     detect variable name using inspect and have as title?
    '''
    def convert_to_image(arg):
        out = arg
        if isinstance(arg, str):
            fp1 = arg.lower()
            assert fp1.endswith('.jpg') or fp1.endswith('.png') 
            out = plt.imread(arg)
        assert not isinstance(arg, (int, dict, list, float))
        return out
    
    if isinstance(imgs, dict):  
        titles = list(imgs.keys())
        imgs = list(imgs.values())
        

    if isinstance(imgs[0], list):
        if  isinstance(imgs[0][0], list):
            if isinstance(imgs[0][0][0], np.ndarray):
                imgs = [np.block([[[eee for eee in ee] for ee in e] for e in imgs])]
                
    imgs = [convert_to_image(fp) for fp in imgs]                
    imgs = [img.squeeze() for img in imgs ]   
    
    ncols = len(imgs)
    img_size = (sum([e.shape[0] for e in imgs]), imgs[0].shape[1])
    global figsize
    figsize = (8, 8)
    figsize = [ max(a/100, b) for a,b in zip(img_size, figsize)]
    fig, axs = plt.subplots(nrows=1, ncols=ncols, gridspec_kw={'wspace':0, 'hspace':0}, figsize=figsize, squeeze=True)
    
    if isinstance(titles, str) and len(imgs)>1:
        fig.suptitle(titles, fontsize=13)
        titles = None
    
    axs = axs if ncols>1 else [axs]
    
    for i, (image, ax) in enumerate(zip(imgs, axs)):
        ax.axis("off")
        if not titles is None:
            ax.set_title(titles[i])
        if image.ndim == 2:
            ax.imshow(image, cmap='gray')
        else:
            ax.imshow(image)        

def is_image_color(img):
    if len(img.shape)==3 and img.shape[-1]==3:
        return True
    if len(img.shape)==3 and img.shape[-1]==1: 
        return False
    if len(img.shape)==2:
        return False
    assert False, 'Array is not Image'        

color_dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255),
              True:(0,255,0), False:(255,0,0), 'white':(255, 255, 255),
              'yellow':(255,255,0), 'black':(0,0,0)}


#-----------------------------------------------------------------------------

def add_box_to_image(fimg, box, clr = 'red', thickness=1):
    # (0,0) is top left (up-down, left-right)
    clr = color_dict.get(clr, clr)
    if isinstance(fimg, str):
        pimg = Image.open(fimg)
        data = np.asarray(pimg)
    elif isinstance(fimg, np.ndarray):
        data = fimg
    else:
        assert False, 'Bad type'
    data = data*(255/data.max())
    
    if len(data.shape)==2:
        data = np.stack([data]*3,2)
    data2 = data.copy()
    if isinstance(box, dict):
        x1,x2,y1,y2 = box['x'], box['x']+box['w'], box['y'], box['y']+box['h']
    if isinstance(box, (tuple, list)):
        (x1,y1),(x2,y2) = box[0], box[1]
    
    t = thickness
    data2[y1-t:y1+t,x1:x2,:]=clr
    data2[y2-t:y2+t,x1:x2,:]=clr
    data2[y1:y2,x1-t:x1+t,:]=clr
    data2[y1:y2,x2-t:x2+t,:]=clr
    return data2






def image_show_popout(img):
    from PIL import Image
    import numpy as np
    
    img = (img-img.min())/(img.max()-img.min())
    img = (255*img).astype(np.uint8)
    if len(img.shape)==2:
        img = np.stack((img,)*3, axis=2)
        
    pimg = Image.fromarray(img,'RGB')
    pimg.show()
   
    
    # #dont think i need this now
    # sz = img3.shape
    # new_img = Image.new('RGB', sz[:2])
    
    # for i in range(sz[0]):
    #     for j in range(sz[1]):
    #         r, g, b = img3[i,j,:]
    #         new_img.putpixel((i, j), (r, g, b))
    # new_img.show()
    
    
    




def color_apply(img, func):
    # Apply a function to the grey levels of a color image
    out = [func(img[:,:,i])  for i in range(img.shape[-1])]
    out = np.stack(out, axis=-1)
    return out

    
def add_noise_to_image(img, mean=0, sigma=0.1, gaussian=None):
    if gaussian is None:
        gaussian = np.random.normal(mean, sigma, (img.shape[0], img.shape[1])) 
    
    if is_image_color(img):
        return color_apply(img, lambda x: add_noise_to_image(x, mean, sigma, gaussian))  
    
    return img +gaussian

                

def add_blurring_to_image(img, sigma=3, mode=0):
    from scipy.ndimage import gaussian_filter    
    import scipy
    # if is_image_color(img):
    #     imgb = [add_blurring_to_image(img[:,:,i], sigma=sigma, mode=mode)  for i in range(3)]
    #     imgb = np.stack(imgb, axis=-1)
    #     return imgb
    if is_image_color(img):
        return color_apply(img, lambda x: add_blurring_to_image(x, sigma, mode))
    
    if mode==0:
        imgb = gaussian_filter(img, sigma=sigma)
    if mode==1:
        def gaussian_kernal(kernel_size=7, sigma=1):
            x, y = np.meshgrid(np.linspace(-2, 2, kernel_size),np.linspace(-2, 2, kernel_size))
            dst = np.sqrt(x**2+y**2)
            gauss = np.exp(-(dst**2 / (2.0 * sigma**2)))
            return gauss/gauss.sum()
         
        kernel_size = max(3, int(2.2*sigma)) 
        kernel_size = kernel_size+1-(kernel_size%2)# round up to higher odd number
        kernel = gaussian_kernal(kernel_size=kernel_size, sigma=sigma)
        imgb = scipy.signal.convolve2d(img, kernel, mode='full', boundary='fill', fillvalue=0)
        # scipy.ndimage.correlate    # prevents kernal flipping
    return imgb


def convert_to_color(img, inverse=False):
    ndim = len(img.shape)
    assert ndim in (2,3)
    if not inverse:
        if ndim==3 and img.shape[-1]==2:
            # this will crash is_iamge_color so before
            blank = np.zeros(img.shape[:2])
            return np.stack([img[:,:,0], img[:,:,1], blank], axis=-1)        
        if is_image_color(img):
            return img        
        img_slice = img if ndim==2 else img[:,:,0]
        return np.stack([img_slice, img_slice, img_slice], axis=-1)
    if ndim==2:
        return img
    return img.mean(axis=-1)
    
def insert_image(img_into, img_from, loc=(0,0)):
    print('overreach not implemented yet')
    if is_image_color(img_into) != is_image_color(img_from):
        img_from = convert_to_color(img_from)
        img_into = convert_to_color(img_into)        
    x,y = loc    
    x2,y2 = x+img_from.shape[0], y+img_from.shape[1]
    img_into[x:x2, y:y2, :] = img_from
    return img_into  


# why is this so slow
def flood_fill(img, seed, mode= 'fast', add_cross=True):
    if mode == 'fast':
        import cv2    
        value = img[seed[0], seed[1]]
        img = (img==value).astype(int)
        img_flood = cv2.floodFill(img, None, seed, newVal=2)[1]
        return (img_flood ==2).astype(int)


    if mode == 'slow':
        from scipy.signal import convolve2d
        conv = [[0,1,0],[1,0,1],[0,1,0]]
        
        value = img[seed]
        img3 = (img==value).astype(int)
        img3[img3==1] = 3
        img3[img3==0] = 2
        img3[seed] = 1
        
        # change this
        # 0 filled
        # 1 filling
        # 2 not-fillable
        # 3 filliable
        
        if add_cross:
            outs = (np.flip(img3[seed[0], :seed[1]]), img3[seed[0], (seed[1]+1):], np.flip(img3[:seed[0], seed[1]]), img3[(seed[0]+1):, seed[1]],)
            for e in outs:
                e[-1] = 0
            outs1 = [np.where(e!=3)[0] for e in outs]
            outs2 = [e[0] for e in outs1]
            outs3 = [seed[1]-outs2[0],seed[1]+outs2[1], seed[0]-outs2[2],seed[0]+outs2[3]]
            img3[outs3[2]:outs3[3],seed[1]] = 1
            img3[seed[0],outs3[0]:outs3[1]] = 1
        
        while True:
            near_filling = (convolve2d(img3==1, conv, boundary='symm', mode='same')>0.5) & (img3==3)
            img3[img3==1] = 0
            img3[near_filling] = 1
            if near_filling.sum()==0:
                break
        img_out = (img3==0).astype(int)
        return img_out


def get_points_of_lines_between_two_points(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    out = []
    while True:
        out.append([x1, y1])
        if x1 == x2 and y1 == y2:
            return out
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def get_points_of_unit_regular_ploygon(n, offset=0, include_angle=True):
    constant = (2*math.pi)/n
    if offset !=0:
        offset = offset *constant
    for i in range(n):
        angle = (constant * i) + offset
        if include_angle:
           yield (math.cos(angle), math.sin(angle), angle)
        else:
           yield (math.cos(angle), math.sin(angle))     








    