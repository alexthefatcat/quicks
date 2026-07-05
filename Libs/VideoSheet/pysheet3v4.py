# -*- coding: utf-8 -*-
"""Created on Sat Dec 11 22:48:17 2021@author: Alexm




2026
create a libary from this
backuplocation only works if it exists
move to git, update git, then try git on the other machine





# change to pillow
# better subprocess
# has to be divisable by 5? what does this mean

# I think json is saved now add hash and file size raw to it
# easy hash and json reader so others can use it
# save date  that is was created
# save info to pandas dataframe
# call it a Video+Facade
# , maybe include filepath_out as global variable
# check if sheet already exists
# date ran
# create two images one stored complete backup




# check hasing is done correctly
# seperate some of the stuff into two classes- video, video_advanced type of thing
# add date scanned to csv
# if file of identical video exists dont overwrite





"""

# from .utils_pysheet3v4 import tryify, , py_filepath_info, find_unused_filepath
from .utils_pysheet3v4 import Popen2, cut,  ImageConcat, batcher, hash_file, get_drive_info, save_pil_image_with_metadata, read_pil_image_with_metadata as _read_pil_image_with_metadata
from .utils_pysheet3v4 import colors, multiply_lists, get_todays_date, filepaths_date

from PIL import Image, ImageDraw, ImageFont, ImageChops # pillow
import PIL
from io import BytesIO 
import os
import numpy as np







#------------------------------------------------------------------------------ 
class Video: # Facade
    # info about the video as well as functions to extract thumbnails
    def __init__(self,filename, nthumbs=None, thumbsize=None):
        self.get_video_info(filename)       
        self.thumbnails_dic = {}
        self.thumbsize = None
        if nthumbs is not None:
            self.create_thumbs( nthumbs, thumbsize)
            
    def get_video_info(self, filename):
        self.filename = filename
        self.filesize = self.getFileSize(filename)
        self.first_frame = self.getFrameAt(filename)
        self.resolution = self.first_frame.size
        self.image_mode = self.first_frame.mode
        self.duration = self.getVideoDuration(filename)
        self.filesizeraw = self.getFileSizeRaw(filename)
        self.hashcode = hash_file(filename)
        self.driveinfo = get_drive_info(filename)
        self.filedates = self.getFileDate(filename)

    @property
    def thumbnails(self):
        return list(self.thumbnails_dic.values())       
        
    @property
    def thumbcount(self):
        return len(self.thumbnails)        
    
    @staticmethod
    def getFileSizeRaw(fp):
        return os.stat(fp).st_size
    
    @staticmethod
    def getFileSize(fp):
        return os.stat(fp).st_size / 1048576.0
    
    @staticmethod    
    def getFileDate(fp):
        return filepaths_date(fp)

    @staticmethod    
    def convertTime(seconds=0):
        if isinstance(seconds,(int,float)):
            hours, hours_rem = divmod(seconds,3600)
            mins, mins_rem = divmod(hours_rem,60)
            return f'{int(hours)}:{int(mins):02d}:{int(mins_rem):02d}'
        if isinstance(seconds,str): 
            h_m_s =[int(float(e)) for e in seconds.split(':')]
            return sum(multiply_lists(h_m_s,(3600, 60, 1)))

    @staticmethod
    def getVideoDuration(filename):
        p,error = Popen2(["ffmpeg","-i",filename])
        time_string = cut(p.decode(),'Duration:',',')
        return Video.convertTime(time_string)

    @staticmethod    
    def getFrameAt(fp, seektime=0):
        timestring = Video.convertTime(int(seektime))
        
        command_frame = ["ffmpeg","-ss",timestring,"-i",fp,"-f","image2","-frames:v","1","-c:v","png","-loglevel","8","-"]        
        try:
            pout, error = Popen2(command_frame)
        except Exception as e:
            raise Exception("FFmpeg is missing or could not be executed") from e
        return Image.open( BytesIO(pout) )   

    @staticmethod
    def makeThumbnails(fp, nthumbs, duration, thumbsize):
        frame_secs = [int(duration*(n/nthumbs)) for n in range(nthumbs)]
        thumbsList = {}
        for time in frame_secs:
            try:
                thumbsList[time] = Video.getFrameAt(fp, time)
            except PIL.UnidentifiedImageError:
                print('   *  Error at',time)
                thumbsList[time] = None
        #thumbsList = { time:Video.getFrameAt(fp, time) for time in frame_secs}
        thumbsList = { time:img for time,img in thumbsList.items() if img is not None}
        if thumbsize is not None:
            for time,img in thumbsList.items():
                img.thumbnail(thumbsize) 
        return thumbsList   

    def create_thumbs(self, nthumbs, thumbsize=None):
        self.thumbnails_dic = self.makeThumbnails(self.filename, nthumbs, self.duration, thumbsize)
        self.thumbsize = self.thumbnails[0].size    

    def get_info(self):
        width, height = self.resolution
        duration = self.duration
        timestring = self.convertTime(duration)
        filename = os.path.basename(self.filename)
        filesize = self.filesize
        filepath = self.filename
        filesizeraw = self.filesizeraw
        hashcode = self.hashcode
        driveinfo = self.driveinfo
        filedates = self.filedates

        info ={"File Name"     : f"{filename}",
               "File Size"     : f"{filesize:10.2f} MB",
               "Resolution"    : f"{width}x{height}",
               "Duration"      : f"    {timestring}",
               "File Path"     : f"{filepath}",
               "File Size Raw" : f"{filesizeraw}",
               "Hash Code"     : f"{hashcode}",
               "Hash Code30"   : f"{hashcode[:30]}",
               'DriveInfo'     : f"DriveInfo: {driveinfo}",
               'script'        :  "pysheet3v3",
               'Date Processed': f'Date Processed: {get_todays_date()}',
               'FileDates'     : f'FileDates: {filedates}',               
               "Keys2Write"    : ("File Name", "File Size", "Resolution", "Duration", "File Path"),
               "Keys2Write2"   : ("File Size Raw", 'Date Processed', "FileDates", "Hash Code", "Hash Code30", "DriveInfo", 'script','Middle Image Pixel Loc'),}
        
        if hasattr(self, 'info_middle_image_loc'):
            info['Middle Image Pixel Loc'] = str(self.info_middle_image_loc)

        return info

        
    def example(self):
        print('''
                    blade_vs = Video('blade_1998.mkv', 20)
                    thumbs = blade_vs.thumbnails  ''')
 

 

class Sheet:
    def __init__(self, video):
        fontfile = "Cabin-Regular-TTF.ttf"
        self.default_settings = dict(
                font = ImageFont.truetype(fontfile, 15),
                font_small = ImageFont.truetype(fontfile, 10),
                backgroundColour = colors.beige,
                textColour = colors.black,
                headerSize = 110,
                gridColumn = 5,
                nthumbs = 25,
                maxThumbSize = (300,300),
                border = 2,
                timestamp = True,)
        
        for setting,value in self.default_settings.items():
            setattr(self,setting,value)
            
        self.header_includes_pyvideosheet3 = True
        self.video = video
        
    def writetext(self, img, loc, text, font=None, fill=None):
        fill = self.textColour if fill is None else fill
        font = self.font if font is None else font  
        d = ImageDraw.Draw(img)             
        d.text(loc, text, font=font, fill=fill)
        
    def setProperty(self,prop,value):
        if prop not in self.default_settings.keys():
            raise Exception('Invalid Sheet property') 
        if prop  in ('font'):
            self.font = ImageFont.truetype(value[0], value[1])
        else:
            setattr(self,prop,value)
                      
    def makeHeader(self):
        # Header Approx size 1508, 103
        info = self.video.get_info()
        texts = [': '.join([k, info[k]]) for k in info["Keys2Write"] if k in info.keys()]
        textsb = [': '.join([k, info[k]]) for k in info["Keys2Write2"] if k in info.keys()]
        global desciption_text
        self.header_text = '\n'.join(texts)
        self.desciption_text = '\n'.join(texts+textsb)##<<<
        desciption_text = self.desciption_text
        
        
        header = Image.new(self.grid.mode, (self.grid.width,self.headerSize), self.backgroundColour) 
        for i,text in enumerate(texts):
            self.writetext(header,(10, 8+(18*i)),text) 
        if self.header_includes_pyvideosheet3:
            self.writetext(header,(1430, 8),'pyvideosheet3',font=self.font_small)
            
        across = 1300 
        if 'Middle Image Pixel Loc' in info:
            shift =-11
        
        self.writetext(header,(across, 51+shift), info["Date Processed"], font=self.font_small)              
        self.writetext(header,(across, 62+shift), info["DriveInfo"], font=self.font_small)  
        self.writetext(header,(across, 73+shift), info["File Size Raw"], font=self.font_small)
        if 'Middle Image Pixel Loc' in info:
            self.writetext(header,(across, 73), info['Middle Image Pixel Loc'], font=self.font_small)  
        self.writetext(header,(across, 84), info['FileDates'], font=self.font_small)      
        self.writetext(header,(across, 95), info["Hash Code30"], font=self.font_small)            
        self.header = header
        self.info = info
        return header



    def _get_location_of_middle_image_from_grid(self):
        self._middle_image_ltrb = list(self._middle_image_ltrb)
        self._middle_image_ltrb[0] = self._middle_image_ltrb[0] + (1*self.border)  
        self._middle_image_ltrb[1] = self._middle_image_ltrb[1] + (2*self.border) + self.headerSize
        self._middle_image_ltrb[2] = self._middle_image_ltrb[2] + (1*self.border) 
        self._middle_image_ltrb[3] = self._middle_image_ltrb[3] + (2*self.border) + self.headerSize
        return f'Middle Image Pixel Loc: {tuple(self._middle_image_ltrb)}'        


    def createVideoSheet(self, columns=None, rows=None, nthumbs=None):
        self.video.create_thumbs(self.nthumbs, self.maxThumbSize)
        self.makeGrid() # self.grid
        self.info_middle_image_loc = self._get_location_of_middle_image_from_grid()
        self.video.info_middle_image_loc = self.info_middle_image_loc
        self.makeHeader() # self.header
        self.sheet = ImageConcat([[self.header], [self.grid]], self.border, color=self.backgroundColour)
        return self.sheet

    def makeGrid(self ):
        img_dic = self.video.thumbnails_dic

        if self.timestamp:
            for i,(frame_time,img) in enumerate(img_dic.items()):
                img_black = img.copy()
                img_white = img.copy() 
                
                self.writetext(img_black, (2,0), self.video.convertTime(frame_time), fill=colors.black)
                self.writetext(img_white, (2,0), self.video.convertTime(frame_time), fill=colors.white)
                
                black_ds = 2*np.asarray(ImageChops.difference(img, img_black), dtype="int32").sum()
                white_ds = np.asarray(ImageChops.difference(img, img_white), dtype="int32").sum()                
                if black_ds>white_ds:
                    img_dic[frame_time] = img_black
                else:
                    img_dic[frame_time] = img_white
        global imgs_nlis
        imgs_nlis = list(batcher(list(img_dic.values()), self.gridColumn))
        
        self.grid, self._middle_image_ltrb = ImageConcat(imgs_nlis, self.border, color=self.backgroundColour, get_middle_image_ltrb=True)


        
class VideoSheet:
    r''' filename = r"C:\Users\Alexm\Desktop\AV\MD new, tnshd - 9395 Mini Diva Homemade Sextape.mp4"
        folder_out = r"C:\Users\Alexm\Desktop\pyVideoSheets3\out"
        videosheet = VideoSheet()
        videosheet.create( filename, folder_out)
        videosheet_fp = videosheet.filename_videosheet_out
        img, mdata = videosheet.read_pil_image_with_metadata(videosheet_fp) 
    '''
    def __init__(self):
        self.infos = []
    
    def create(self,filepath_in, folder_out):
        global sheet, video, vsheet
        
        self.video = Video(filepath_in)
        self.sheet = Sheet(self.video)
        self.vsheet = self.sheet.createVideoSheet()  
        
        video = self.video
        sheet = self.sheet
        vsheet = self.vsheet
        
        self.current_mdata = sheet.desciption_text
        self.infos.append(self.video.get_info())
        self._save(filepath_in, folder_out, vsheet, self.current_mdata)
        
    @staticmethod
    def read_pil_image_with_metadata(filepath):
        return _read_pil_image_with_metadata(filepath)
        
    def _save(self,filepath_in, folder_out, vsheet, mdata=None):
        
        global fnn,  filepath_in_folder, folder 
        
        filepath_dir, filename = os.path.split(filepath_in)
        _,filepath_in_folder = os.path.split(filepath_dir)  
        filename_vs = filename.rsplit('.',1)[0] + '.vs.jpg'


        self.filename_videosheet_out = os.path.join(folder_out, filename_vs)
        
        if mdata is None:
            mdata = False # function then just saves normally
        save_pil_image_with_metadata(self.filename_videosheet_out, vsheet, mdata)


        


                

        






