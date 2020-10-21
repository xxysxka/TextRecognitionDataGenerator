import random as rnd
import os
import copy
from PIL import Image, ImageDraw, ImageFilter

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)

img_width = 400
img_height = 200
out_dir = "./output/"
count = 10
first_line_strings = ["NSFJS","SFSJF","FSFDJKS"]
second_line_strings = ["23235","12378","8975"] 

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
        generator_list.append([img, bbox, lb])
    return generator_list

def main():
    generator1 = GeneratorFromStrings(
    strings=first_line_strings,
    count=len(first_line_strings),
    size=60,
    bounding_box=True,
    )
    generator1_list = unpack_generator(generator1)

    generator2 = GeneratorFromStrings(
    strings=second_line_strings,
    size=40,
    count=len(second_line_strings),
    bounding_box=True,
    )
    generator2_list = unpack_generator(generator2)
    
    for i in range(count):
        first_line = copy.deepcopy(rnd.choice(generator1_list))
        second_line = copy.deepcopy(rnd.choice(generator2_list))
        img1, bbox1, lb1 = first_line
        img2, bbox2, lb2 = second_line

        img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        img_draw = ImageDraw.Draw(img)

        x = rnd.randint(0, img_width-max(img1.width, img2.width))
        y = rnd.randint(0, img_height-img1.height-img2.height)
        

        ###### paste first line ######
        img.paste(img1, (x, y)) 
        bbox1 = paste_bbox(bbox1, x, y)
         
        for box in bbox1:
            img_draw.polygon(box, outline = (255, 0, 0), )
        ###### paste first line ######
        
        ###### paste second line　###### 
        img.paste(img2, (x, y+img1.height))
        bbox2 = paste_bbox(bbox2, x, y+img1.height)

        for box in bbox2:
            img_draw.polygon(box, outline = (0, 255, 0), )
        ###### paste second line　######
        img = img.convert("RGB")
        img.save(out_dir+lb1+lb2+".jpg")
        
        with open (os.path.join(out_dir, lb1+lb2+'.txt'), mode = 'w') as f:
            for box, p  in zip(bbox1+bbox2, lb1+lb2):
                f.write(str(box) + p)
                f.write('\r\n')

        
if __name__ == "__main__":
    main()

