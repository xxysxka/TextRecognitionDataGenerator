import random as rnd
import math
import numpy as np

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def generate(
    text,
    font,
    text_color,
    font_size,
    orientation,
    space_width,
    character_spacing,
    fit,
    word_split,
    radius,
):
    if orientation == 0:
        return _generate_horizontal_text(
            text,
            font,
            text_color,
            font_size,
            space_width,
            character_spacing,
            fit,
            word_split,
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    elif orientation == 2:
        return _generate_curved_text(
            text, font, text_color, font_size, space_width, character_spacing, fit, word_split, radius,
        )

    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(
    text, font, text_color, font_size, space_width, character_spacing, fit, word_split
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_width = int(image_font.getsize(" ")[0] * space_width)

    if word_split:
        splitted_text = []
        for w in text.split(" "):
            splitted_text.append(w)
            splitted_text.append(" ")
        splitted_text.pop()
    else:
        splitted_text = text
    piece_widths = [
        image_font.getsize(p)[0] if p != " " else space_width for p in splitted_text
    ]
    piece_heights = [
        image_font.getsize(p)[1] if p != " " else space_width for p in splitted_text
    ] 
    text_width = sum(piece_widths)
    if not word_split:
        text_width += character_spacing * (len(text) - 1)

    text_height = max([image_font.getsize(p)[1] for p in splitted_text])

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask, mode="RGB")
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
        #128,
        )

    bboxs = []
    for i, p in enumerate(splitted_text):
        left_top_x = sum(piece_widths[0:i]) + i * character_spacing * int(not word_split)
        left_top_y = 0
        left_bottom_x = sum(piece_widths[0:i]) + i * character_spacing * int(not word_split)
        left_bottom_y = piece_heights[i]
        right_top_x = sum(piece_widths[0:i]) + i * character_spacing * int(not word_split) + piece_widths[i]
        right_top_y = 0
        right_bottom_x = sum(piece_widths[0:i]) + i * character_spacing * int(not word_split) + piece_widths[i]
        right_bottom_y = piece_heights[i]
        if p != ' ':
            bboxs.append([
                left_top_x, left_top_y, 
                right_top_x, right_top_y,
                right_bottom_x, right_bottom_y,
                left_bottom_x, left_bottom_y
                ])
        txt_img_draw.text(
            (left_top_x, left_top_y),
            p,
            fill=fill,
            font=image_font,
        )
        txt_mask_draw.text(
            (left_top_x, left_top_y),
            p,
            #fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            fill=(255, 255, 255),
            font=image_font,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox()), splitted_text_xy
    else:
        return txt_img, txt_mask, bboxs

def _generate_vertical_text(
    text, font, text_color, font_size, space_width, character_spacing, fit
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    char_widths = [
        image_font.getsize(c)[0] if c != " " else space_height for c in text
    ]    
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
        #128,
    )
    bboxs = []
    for i, c in enumerate(text):
        left_top_x = 0
        left_top_y = sum(char_heights[0:i]) + i * character_spacing
        right_top_x = char_widths[i]
        right_top_y = sum(char_heights[0:i]) + i * character_spacing
        right_bottom_x = char_widths[i]
        right_bottom_y = sum(char_heights[0:i]) + i * character_spacing + char_heights[i]
        left_bottom_x = 0 
        left_bottom_y = sum(char_heights[0:i]) + i * character_spacing + char_heights[i]
        if c != ' ':
            bboxs.append([
                    left_top_x, left_top_y,
                    right_top_x, right_top_y,
                    right_bottom_x, right_bottom_y,
                    left_bottom_x, left_bottom_y
                    ])
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            #fill=(i // (255 * 255), i // 255, i % 255), 
            fill=(255, 255, 255),
            font=image_font,
        )
    '''
    coordinateDraw = ImageDraw.Draw(txt_img)
    for coordinate in char_coordinates:
        coordinateDraw.polygon(coordinate, outline = (255, 0, 0))
    txt_img.show()
    '''
    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox()), char_coordinates
    else:
        return txt_img, txt_mask, bboxs


def _generate_curved_text(
    text, font, text_color, font_size, space_width, character_spacing, fit, word_split, r
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_width = int(image_font.getsize(" ")[0] * space_width)

    if word_split:
        splitted_text = []
        for w in text.split(" "):
            splitted_text.append(w)
            splitted_text.append(" ")
        splitted_text.pop()
    else:
        splitted_text = text

    piece_widths = [
        image_font.getsize(p)[0]+space_width*character_spacing if p != " " else space_width for p in splitted_text
    ]
    piece_heights = [
        image_font.getsize(p)[1] if p != " " else space_width for p in splitted_text
    ] 
    '''
    if not word_split:
        text_width += character_spacing * (len(text) - 1)
    '''
    img_width = math.ceil(2*r + 2*max(piece_heights))
    img_height = math.ceil(2*r + 2*max(piece_heights))
    
    txt_img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    mask_img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    
    txt_img_draw = ImageDraw.Draw(txt_img)
    mask_img_draw = ImageDraw.Draw(mask_img)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]
    
    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
        #128,
        )
    
    arclength = 0
    bboxs = []
    for i, c in enumerate(text):
        arclength += piece_widths[i]/2
        theta = math.pi + arclength /r
        x = r * math.cos(theta) + img_width/2
        y = r * math.sin(theta) + img_height/2

        char_img = Image.new('RGBA', (image_font.getsize(c)[0], piece_heights[i]), (255, 255, 255, 0))
        char_img_draw = ImageDraw.Draw(char_img)
        char_img_draw.text(
                (0,0),
                c,
                fill = fill,
                font = image_font,
                )
        '''
        char_img_draw.text(
                (char_img.width/2, char_img.height/2),
                "*",
                fill = fill,
                font = image_font,
                )
        '''
        theta = theta + math.pi/2
        angle = theta  * 180 / math.pi
        char_img_rotated = char_img.rotate((360-angle), expand = True,)
        x = round(x)
        y = round(y)
        txt_img.paste(char_img_rotated, (x, y), char_img_rotated)
        mask_img.paste(char_img_rotated, (x, y))
        
        if c != ' ':
            box = [
                x, y,
                x+image_font.getsize(c)[0], y,
                x+image_font.getsize(c)[0], y+piece_heights[i],
                x, y+piece_heights[i],
                ]
             
            expand_matrix = np.stack([
                (char_img_rotated.width - char_img.width) /2,
                (char_img_rotated.height - char_img.height) /2
                ], axis=0) 

            center = np.stack([x+char_img_rotated.width/2, y+char_img_rotated.height/2], axis=0)
            center = np.reshape(center, [1, 2])
                    
            rotation = np.stack([math.cos(theta), math.sin(theta), -math.sin(theta), math.cos(theta)], axis=0)
            rotation_matrix = np.reshape(rotation, [2, 2])

            b = np.reshape(box, (4, 2))
            b = b +  expand_matrix
            b = np.matmul(b - center, rotation_matrix) + center
            box = np.reshape(b, (8, )).tolist()
            
            bboxs.append(box)

        arclength += piece_widths[i]/2
    ''' 
    for coordinate in char_coordinates:
        txt_img_draw.polygon(coordinate, outline = (0, 255, 0))
    '''

    return txt_img, mask_img, bboxs
