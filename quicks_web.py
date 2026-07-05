
import requests
from PIL import Image
from io import BytesIO
import os

def save_image_from_url(url, folder = r"C:\Users\Alexm\Desktop\gynoid_zzz",width_minimum=200):
    def split_url(url):
        a,b = os.path.split(url)
        a = a+'/'
        c = ''
        if '.' in b:
            b,c = b.rsplit('.',1)
            c = '.'+c
        return (a,b,c)
    
    url0 = split_url(url)
    response = requests.get(url)
    header_dict = response.headers
    msg = 'Success: No Duplicates'
    
    if response.status_code == 200:
        return 'Failed: status code incorrect', None
    
    content_type = header_dict.get('Content-Type','')
    if 'image' in content_type:
        return 'Failed: content_type not image', None
        
    image = Image.open(BytesIO(response.content))
    if width_minimum is not None:
        if image.width < width_minimum:
            return 'Failed: Too Small', None
    
    filepath = folder+'//'+url0[1]+url0[2]
    msg = 'Success: file downloaded'
    counter = 1

    while os.path.exists(filepath):
        filepath = f"{folder}//{url0[1]}({counter}){url0[2]}"
        counter += 1
        msg = 'Success: filepath used, new found'
    image.save(filepath)
    
    return msg, filepath






