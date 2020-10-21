import random as rnd
import os
import sys
import copy
from PIL import Image, ImageDraw, ImageFilter

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)
from trdg.string_generator import (
    create_strings_from_dict,
    create_strings_from_file,
    create_strings_from_wikipedia,
    create_strings_randomly,
)

from trdg.utils import load_dict, load_fonts

image_width = 0
image_height = 0
out_dir = "./output/"
count = 2
length = [5, 3]
random_length = [False, True]
font_size = [20, 15]
dict_dir = "/home/smartmore/tools/trdg/TextRecognitionDataGenerator/trdg/dicts/en.txt"
font = []
font_dir = "../TraditionalChinese_fonts"
background_img_dir = "./test/"
line_space = 5
language = "en"

def paste_bbox(bboxs, x, y):
    for box in bboxs:
        for i in range(8):
            if i %2 == 0:
                box[i] = box[i] + x
            else:
                box[i] = box[i] + y
    return bboxs

#### convert generator((img, bbox), label) to list[img, bbox, label]
def unpack_generator(generator):
    generator_list = []
    for res, lb in generator:
        img = res[0]
        bbox = res[1]
    return img, bbox, lb

def multiline_load_fonts(font_dir, font):
    #Create font (path) list
    if font_dir != "":
        fonts = [
            os.path.join(font_dir, p)
            for p in os.listdir(font_dir)
            if os.path.splitext(p)[1] == ".ttf"
        ]
    elif font != []:
        if os.path.isfile(font):
            fonts = [font]
        else:
            sys.exit("Cannot open font")
    else:
        fonts = []
    return fonts

def generate_background_img(image_dir, width, height):
    if image_dir != "":
        images = os.listdir(image_dir)
        if len(images) > 0:
            pic = Image.open(
                os.path.join(image_dir, images[rnd.randint(0, len(images) - 1)])
            )
            pic = pic.resize((max(pic.width, width), max(pic.height, height)), Image.ANTIALIAS
            )
        else:
            raise Exception("No images where found in the images folder!")
    else :
        pic = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    return pic


def main():
    fonts = multiline_load_fonts(font_dir, font)
   
    lang_dict = []
    if os.path.isfile(dict_dir):
        with open(dict_dir, "r", encoding="utf8", errors="ignore") as d:
            lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
    
    else:
        sys.exit("Cannot open dict")
    
    strings1 = create_strings_from_dict(length[0], random_length[0], count, lang_dict)
    strings2 = create_strings_from_dict(length[1], random_length[1], count, lang_dict)

    
    for i in range(count):
        generator1 = GeneratorFromStrings(
            strings=rnd.choices(strings1),
            count=len(strings1),
            size=font_size[0],
            bounding_box=True,
            fonts=fonts,
            background_type=1,
            text_color ="#FFFFFF"
        )
        img1, bbox1, lb1 = unpack_generator(generator1)

        generator2 = GeneratorFromStrings(
            strings = rnd.choices(strings2),
            size=font_size[1],
            count=len(strings2),
            bounding_box=True,
            fonts=fonts,
            background_type=1,
            text_color="#FFFFFF"
        )
        img2, bbox2, lb2 = unpack_generator(generator2)
        #first_line = copy.deepcopy(rnd.choice(generator1_list))
        #second_line = copy.deepcopy(rnd.choice(generator2_list))
        #img1, bbox1, lb1 = first_line
        #img2, bbox2, lb2 = second_line

        img = generate_background_img(background_img_dir, image_width, image_height)
        img_draw = ImageDraw.Draw(img)
        x = rnd.randint(0, img.width-max(img1.width, img2.width))
        y = rnd.randint(0, img.height-img1.height-img2.height)
        

        ###### paste first line ######
        img.paste(img1, (x, y), img1) 
        bbox1 = paste_bbox(bbox1, x, y)
        
        ''' 
        for box in bbox1:
            img_draw.polygon(box, outline = (255, 0, 0), )
        '''
        ###### paste first line ######
        
        ###### paste second line　###### 
        img.paste(img2, (x, y+img1.height+line_space), img2)
        bbox2 = paste_bbox(bbox2, x, y+img1.height+line_space)
        
        '''
        for box in bbox2:
            img_draw.polygon(box, outline = (0, 255, 0), )
        '''
        ###### paste second line　######
        img = img.convert("RGB")
        img.save(out_dir+lb1+lb2+".jpg")
        
        with open (os.path.join(out_dir, lb1+lb2+'.txt'), mode = 'w') as f:
            for box, p  in zip(bbox1+bbox2, lb1+lb2):
                f.write(str(box)+p)
                f.write('\r\n')

        
if __name__ == "__main__":
    main()

