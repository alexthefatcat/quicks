# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 05:20:30 2026

@author: alexm

Why Windows 11 Paint Files Miss Detection

    DPI Shift (96 DPI vs 72 DPI): Legacy MS Paint saved images at 72 DPI (2835 dots/meter). Modern Windows 11 Paint defaults to 96 DPI (3780 dots/meter) or adapts to your monitor's display scaling. The script's 72 DPI check fails on new files.

    No Software Tag: Neither legacy nor modern Paint explicitly writes "Microsoft Paint" into PNG tEXt chunks or JPEG EXIF software tags when creating a file from scratch.

    Overlapping Fingerprints: While Windows 11 Paint strips EXIF data and creates minimal PNG chunks, so do many other modern tools (Windows Snipping Tool, web image optimizers, Discord, and messaging apps). Since the script requires at least 2 out of 3 markers to flag an image, failing the 72 DPI check drops the score to 1/3 or 0/3.

Adjustments for Windows 11 Paint

To improve detection accuracy for files saved with modern Paint, adjust the heuristic checks:

    Include 96 DPI: Update the resolution check to look for 96 DPI alongside 72 DPI.

    Check for Missing Camera Tags in JPEGs: If a file is a .jpg but lacks standard camera EXIF metadata (Make, Model, Orientation) while maintaining standard sRGB color profiles, increase the Paint probability weight.

    PNG pHYs Unit Specifier: Windows 11 Paint saves PNG pHYs chunks with physical unit specifiers set to meters (unit specifier 1).








paint_edited_files
yes
maybe
no


paint_orign   yes maybe no
paint_edited  yes maybe no






"""

import os
from PIL import Image, ExifTags


def detect_ms_paint(image_path):
    keywords = ["paint", "microsoft paint", "windows paint"]
    
    try:
        with Image.open(image_path) as img:
            # 1. Check PNG text metadata chunks (tEXt/iTXt)
            for key, val in img.info.items():
                if isinstance(val, str) and any(kw in val.lower() for kw in keywords):
                    return True, f"MS Paint detected in PNG info tag '{key}': {val}"

            # 2. Check EXIF metadata (JPEG/TIFF/WebP)
            exif_data = img.getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    
                    # Tag 305 corresponds to "Software"
                    if tag_name == "Software" and isinstance(value, str):
                        if any(kw in value.lower() for kw in keywords):
                            return True, f"MS Paint detected in EXIF Software tag: {value}"

    except Exception as e:
        return False, f"Error reading file: {e}"

    return False, "No explicit MS Paint software tag found."





def detect_paint_fingerprints_old(image_path):
    indicators = []
    
    with Image.open(image_path) as img:
        # 1. Check for complete lack of EXIF data
        exif = img.getexif()
        has_exif = len(exif) > 0
        if not has_exif:
            indicators.append("No EXIF metadata present (Paint strips EXIF on save)")

        # 2. Check PNG specific fingerprints
        if img.format == "PNG":
            # Paint PNGs contain almost no info keys (no tEXt/iTXt metadata)
            info_keys = list(img.info.keys())
            has_minimal_keys = set(info_keys).issubset({"dpi", "aspect", "srgb", "gamma"})
            if has_minimal_keys:
                indicators.append("PNG contains zero software/metadata text chunks")

        # 3. Check for MS Paint's default 72 DPI resolution (2835 pixels per meter)
        dpi = img.info.get("dpi")
        if dpi:
            # 72 DPI usually maps to ~72.0089 DPI (2835 dpm) in Paint
            if abs(dpi[0] - 72) < 0.1 and abs(dpi[1] - 72) < 0.1:
                indicators.append("Default Windows/Paint resolution found (72 DPI / 2835 dpm)")

        # Decision Logic
        score = len(indicators)
        is_likely_paint = score >= 2

        return {
            "likely_ms_paint": is_likely_paint,
            "confidence_score": f"{score}/3 markers matched",
            "detected_fingerprints": indicators
        }


def detect_paint_fingerprints(image_path):#wind11
    """
    Detects images created or modified by MS Paint, updated for Windows 11.
    Checks for 96 DPI (modern) and 72 DPI (legacy) resolutions, EXIF stripping,
    and minimal PNG metadata chunks.
    """
    indicators = []
    
    try:
        with Image.open(image_path) as img:
            fmt = img.format
            info = img.info
            
            # 1. Check Resolution (Handles 96 DPI Windows 11 & 72 DPI Legacy)
            dpi = info.get("dpi")
            if dpi:
                dpi_x, dpi_y = dpi
                # Windows 11 Paint defaults to 96 DPI (3780 dots/meter -> ~96.012 DPI in Pillow)
                is_96_dpi = any(abs(dpi_x - target) < 0.5 for target in (96.0, 96.012)) and \
                            any(abs(dpi_y - target) < 0.5 for target in (96.0, 96.012))
                # Legacy Paint defaulted to 72 DPI (2835 dots/meter)
                is_72_dpi = abs(dpi_x - 72.0) < 0.5 and abs(dpi_y - 72.0) < 0.5
                
                if is_96_dpi:
                    indicators.append("Windows 11 Paint resolution detected (96 DPI / 3780 dpm)")
                elif is_72_dpi:
                    indicators.append("Legacy Paint resolution detected (72 DPI / 2835 dpm)")

            # 2. Check for Stripped EXIF Data
            exif = img.getexif()
            has_exif = exif is not None and len(exif) > 0
            if not has_exif:
                indicators.append("Zero EXIF metadata present (Paint completely strips EXIF on save)")

            # 3. Check Format-Specific Cleanliness
            if fmt == "PNG":
                # Win 11 Paint PNGs only contain standard header/color keys, no software or text chunks
                info_keys = set(info.keys())
                standard_win_keys = {"dpi", "aspect", "srgb", "gamma", "chroma"}
                if info_keys.issubset(standard_win_keys):
                    indicators.append("PNG contains no software/comment text chunks")
            elif fmt in ("JPEG", "MPO") and not has_exif:
                indicators.append("JPEG lacks standard camera/editor EXIF software tags")

            # Decision Logic
            score = len(indicators)
            is_likely = score >= 2

            return {
                "filepath": image_path,
                "likely_ms_paint": is_likely,
                "confidence_score": f"{score}/3 markers matched",
                "detected_fingerprints": indicators
            }

    except Exception as e:
        return {
            "filepath": image_path,
            "likely_ms_paint": False,
            "confidence_score": "0/3 markers matched",
            "detected_fingerprints": [f"Error opening image: {e}"]
        }






def get_files_in_folder(folder_path, exts=['.png','.jpg']):
    if isinstance(folder_path, list):
        filepaths = []
        for folder_path_ in folder_path:
            filepaths_ = get_files_in_folder(folder_path_, exts=exts)
            filepaths.extend(filepaths_)
        return filepaths
        
    filepaths = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            for ext in exts:
                if filename.lower().endswith(ext):
                    filepath = os.path.join(root, filename)
                    filepaths.append(filepath)
    return filepaths





#%%----------------------------------------------------------------------------




folder_path = r"C:\Users\alexm\OneDrive\Pictures"   #1161 files
#folder_path = r"C:\Users\alexm\Downloads"
paint_files = []
not_paint = []
paint_dict = {}

filepaths = list(get_files_in_folder(folder_path))
for i,filepath in enumerate(filepaths):
    print(i)
    is_paint, reason = detect_ms_paint(filepath)
    if is_paint:
        paint_files.append(filepath)
    else:
        not_paint.append(filepath)
    response = detect_paint_fingerprints(filepath)
    key = response["confidence_score"]
    paint_dict[key] = paint_dict.get(key, []) +[filepath]




# Example Usage



paint_dict2 = {}
for k,v in paint_dict.items():
    for vv in v:
        if 'AoiT' in vv or 'FindImages_AV_DF_on_KS2__2025' in vv:
            paint_dict2[k] = paint_dict2.get(k, []) + [vv]








filepath = r"C:\Users\alexm\OneDrive\Pictures\FindImages_AV_DF_on_KS2__2025\find these.png"

detect_paint_fingerprints(filepath)

image_path = filepath





assert False

print(f"Is MS Paint: {is_paint} ({reason})")
k = [f for f in not_paint if 'aff' in f]
kk = 'C:\\Users\\alexm\\Downloads\\affleck casey fsdfsqcGc@._V1_FMjpg_UX986_.jpg'
is_paint, reason = detect_ms_paint(kk)
# Example Usage
result = detect_paint_fingerprints("sample_image.png")
print(result)



img = Image.open("image.jpg")
exif = img.getexif()

# Human-readable dictionary (e.g., {'Make': 'Apple', 'Model': 'iPhone 13'})
exif_dict = 



def get_exif_tag_dict(image_path):
    with Image.open(image_path) as img:
        # 2. Check for Stripped EXIF Data
        exif = img.getexif()
        has_exif = exif is not None and len(exif) > 0
        if not has_exif:
            return {}
        return {ExifTags.TAGS.get(key, key): value for key, value in exif.items()}
    
has_dict = {}
for filepath in filepaths:
    dic = get_exif_tag_dict(filepath)
    key = 'True' if len(dic)> 0 else 'False'
    has_dict[key] = has_dict.get(key, []) +[filepath]
    if len(dic)>0:
        for k in dic.keys():
            print(k, filepath)
    
    if 'aff' in filepath:
        break
    




dic = get_exif_tag_dict(filepath_not_paint)

dic = get_exif_tag_dict(filepath_not_paint)






from PIL import Image, ExifTags

def get_image_metadata(image_path):
    metadata = {}
    
    with Image.open(image_path) as img:
        # 1. Extract Adobe XMP metadata (stored in img.info)
        if "xmp" in img.info:
            # Contains the Adobe XML string seen in your text editor
            xmp_data = img.info["xmp"]
            metadata["XMP"] = xmp_data.decode("utf-8", errors="ignore") if isinstance(xmp_data, bytes) else xmp_data

        # 2. Extract standard EXIF data + SubIFDs
        exif = img.getexif()
        if exif:
            # Top-level EXIF tags
            for key, value in exif.items():
                metadata[ExifTags.TAGS.get(key, key)] = value
            
            # Fetch nested SubIFDs (Exif IFD: 0x8769, GPS IFD: 0x8825)
            for ifd_id in (34665, 34853):
                try:
                    sub_ifd = exif.get_ifd(ifd_id)
                    for key, value in sub_ifd.items():
                        metadata[ExifTags.TAGS.get(key, key)] = value
                except KeyError:
                    continue
                    
    return metadata

filepath = r"C:\Users\alexm\OneDrive\Pictures\AoiT\anh-gay-hoa-3-1754362266816-17543622672111788863690-1754621108520-17546211086161482045754.jpg"
metadata1 = get_image_metadata(filepath)
filepath_not_paint = r"C:\Users\alexm\OneDrive\Pictures\Doll\F_Uoe7CbkAAVJro.jpg"  
metadata2 = get_image_metadata(filepath_not_paint)
filepath = r'C:\Users\alexm\OneDrive\Pictures\Streamlit Block.png'
metadata3 = get_image_metadata(filepath)
filepath = r"C:\Users\alexm\OneDrive\Pictures\Streamlit Block Copy Delete.png"
metadata4 = get_image_metadata(filepath)
filepath_paint = r"C:\Users\alexm\OneDrive\Pictures\Whatever-Christiana.png"
metadata5 = get_image_metadata(filepath_paint)
filepath_paint = r"C:\Users\alexm\OneDrive\Pictures\TEST.png"
metadata6 = get_image_metadata(filepath_paint)




