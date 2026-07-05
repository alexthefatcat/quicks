# -*- coding: utf-8 -*-
"""Created on Mon Jul 15 14:42:24 2024@author: AlexMilroy
main others

image_show(pop_out=True)
image_save
image_blur
iamge_add_noise
image_affine_transform
image_warp
image_normalize
image_hsv
image_add_text
images_to_video


"""
image_colors = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255),
              True:(0,255,0), False:(255,0,0), 'white':(255, 255, 255),
              'yellow':(255,255,0), 
              'black':(0,0,0)}

def image_read(img_filepath, mode='pil'):
    mode = mode.lower().replace(' ','')
    assert mode in ('cv2','pil')
    if   mode == 'cv2':    
        import cv2
        image = cv2.imread(img_filepath, 1)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif mode == 'pil':
        from PIL import Image
        import numpy as np
        image_from_pil = Image.open(img_filepath).convert("RGB")
        img = np.array(image_from_pil)
    return img


def image_resize(img, *, mode='cv2', ratio=None, height=None, width=None, return_ratio=False):
    old_height, old_width, *bytesPerComponent = img.shape
    
    if ratio is not None:
        assert (height is None) and (width is None)
        width = round(old_width * ratio)
        height = round(old_height * ratio)
    else:
        assert not ((height is None) and (width is None))
        if height is None:
            ratio = width/old_width 
            height = round(old_height * ratio)                  
        if width is None:
            ratio = height/old_height 
            width = round(old_width * ratio)  
    size_new = (width, height)
    if   mode == 'cv2':
       import cv2          
       img = cv2.resize(img, size_new )
    elif mode == 'pil':
       from PIL import Image
       import numpy as np
       pimg = Image.fromarray(img)
       pimg = pimg.resize(size_new )  
       img = np.array(pimg)

    if return_ratio:
        return img, ratio
    return img     

def image_is_color(img):
    if len(img.shape)==3 and img.shape[-1]==3:
        return True
    if len(img.shape)==3 and img.shape[-1]==1: 
        return False
    if len(img.shape)==2:
        return False
    assert False, 'Array is not Image'

def image_add_box(fimg, box, clr = 'red'):
    import numpy as np
    # (0,0) is top left (up-down, left-right)
    clr = image_colors.get(clr, clr)
    if isinstance(fimg, str):
        data = image_read(fimg)
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





# img0 = image_read(fp, mode='cv2')
# img1 = image_read(fp, mode='pil')


def crosshair(img, point, width = 60, thickness=3):
    # width = 40
    # img = image_read(fp)    
    # point = (100,100)
    point = (int(point[0]), int(point[1]))
    width4 = int(width//4)
    offsets = (-2*width4, 2*width4)
    corners = [(point[0]+xx, point[1]+yy) for xx in offsets for yy in offsets]
    corners.insert(3, corners.pop(2))
    corners = corners+[corners[0]]
    lines = [((point[0]+x1, point[1]+y1),(point[0]+(2*x1), point[1]+(2*y1))) for x1,y1 in ((0,width4),(0,-width4),(width4,0),(-width4,0)) ]
    for line in lines:
        xx, yy = zip(*line)
        img[min(xx)-thickness:max(xx)+1+thickness, min(yy)-thickness:max(yy)+1+thickness,:]=(255,0,0)
    for line in zip(corners,corners[1:]):
        xx, yy = zip(*line)
        img[min(xx)-thickness:max(xx)+1+thickness, min(yy)-thickness:max(yy)+1+thickness,:]=(255,0,0)   
    return img



def images_save_to_mp4(frames, vfilepath, frame_rate = 30, make_color=True):
    #probably has to be uint8
    import cv2
    import numpy as np
    width, height, nframes = frames.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(vfilepath, fourcc, frame_rate, (width, height))
    for i in range(nframes):
        frame = frames[:,:,i]
        if make_color:
            frame = np.stack(3*[frame],2)
        video.write(frame)
    video.release()


def volume_image_rotate(img_vol, degrees):
    import cv2
    import numpy as np    
    from math import cos, sin, pi       
    import scipy
    radians = degrees*(2*pi/360)
    x_size, y_size,*_ = img_vol.shape
    affine1 = cv2.getRotationMatrix2D((x_size/2, y_size/2), degrees, scale=1)
    dx0, dy0 = affine1[:,-1]
    
    cos_angle = cos(radians)
    sin_angle = sin(radians)
    
    affine = np.array([[ cos_angle, sin_angle, 0, dx0],
                       [-sin_angle, cos_angle, 0, dy0],
                       [         0,         0, 1,   0]])
    
    img_vol3 = scipy.ndimage.affine_transform(img_vol, affine)
    return img_vol3













