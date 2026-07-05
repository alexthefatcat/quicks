# -*- coding: utf-8 -*-
"""Created on Mon Oct  9 12:10:06 2023@author: alexm"""

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

'''
Future:-
   normalize
   concat
   imshow given mulitple images and titles
'''

def is_image_color(img):
    if len(img.shape)==3 and img.shape[-1]==3:
        return True
    if len(img.shape)==3 and img.shape[-1]==1: 
        return False
    if len(img.shape)==2:
        return False
    assert False, 'Array is not Image'


def image_show(*imgs, titles=None):
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
        
    imgs = [convert_to_image(fp) for fp in imgs]  
    imgs = [img.squeeze() for img in imgs ]   
    
    ncols = len(imgs)    
    fig, axs = plt.subplots(nrows=1, ncols=ncols, gridspec_kw={'wspace':0, 'hspace':0},figsize=(8, 8), squeeze=True)
    
    if isinstance(titles, str) and len(imgs)>1:
        fig.suptitle(titles, fontsize=13)
        titles = None
    
    axs = axs if ncols>1 else [axs]
    for i, (image, ax) in enumerate(zip(imgs, axs)):
        ax.axis("off")
        if not titles is None:
            ax.set_title(titles[i])
        ax.imshow(image)

color_dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255),
              True:(0,255,0), False:(255,0,0), 'white':(255, 255, 255),
              'yellow':(255,255,0), 
              'black':(0,0,0)}


def add_box_to_image(fimg, box, clr = 'red'):
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
    x1,x2,y1,y2 = box['x'], box['x']+box['w'], box['y'], box['y']+box['h']
    
    t = 1 # thickness
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
        






def quick_example_image():
    import numpy as np
    img = np.zeros([400,400,3])
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            #red square
            if 190>i>10:
                if 190>j>10:
                    img[i,j,0] = 1
                    
            #blue circle
            if (i-100)**2 +(j-300)**2 <90**2:
                img[i,j,2] = 1
                continue                 
            
            #white lines
            if j in (200,80,160):
                img[i,j,:] = 1
                continue
                    
            #green traingle
            n = (3/2)**0.5
            i2, j2 = i-250, j-300        
            if i<350:
                if i2+(n*j2)>0:
                    if i2-(n*j2)>0:
                        img[i,j,1] = 1
                        continue
    
            #small colored boxs
            if 390>i>370 and 360>j>240:
                for ii,cc in enumerate([(1,1,0), (0,1,1), (1,0,1), (1,1,1),(1,0.5,0),(0,1,0.5)]):
                    if (j-240)//20==ii:
                        img[i,j,:]=cc
                        
            #black-white chess board spectrum
            if 219>i>205:        
                if 270>j>205:
                    img[i,j,:] = (i+j)%2==0 if j<240 else (j-240)/30 
                    continue                    
    
    
            # yellow point spread function
            z = 30/(30+(i-250)**2 +(j-245)**2)
            if z>0.01:
                img[i,j,:2] = z      
    
            # spectrum square
            if 110>i>90:        
                if 140>j>60:
                    img[i,j,:] = ((i-90)/(110-90), (j-60)/(140-60),0)                  
            
            #spectrum cross
            if 390>i>210 and 190>j>10:
                if abs((i-300)+(j-100))<10 or abs((i-300)-(j-100))<10:
                    a = max(0,(60-abs(j-10))/60)+max(0,(60-abs(j-190))/40)
                    b = max(0,(60-abs(j-70))/60) 
                    c = max(0,(60-abs(j-130))/60)
                    img[i,j,:] = (a,b,c)
                    
    return img
        



if __name__ == '__main__':
    if True:
        img = quick_example_image() 
        image_show_popout(add_noise_to_image(add_blurring_to_image(img)))
        image_show_popout(img)       
    else:
    
        #image_show_popout(img)
    
        #image_show_popout(add_noise_to_image(img))
        
        img2 = img[:,:,0]
        
        imgb1 = add_blurring_to_image(img2, mode=0)    
        imgb2 = add_blurring_to_image(img2, mode=1)
        image_show_popout(imgb1)
        image_show_popout(imgb2)
        
        imgb = add_blurring_to_image(img, mode=0)
        
        image_show_popout(imgb)
        
        
    












