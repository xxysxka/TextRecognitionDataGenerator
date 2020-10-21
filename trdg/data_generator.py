import os
import random as rnd

import math
import numpy as np

from PIL import Image, ImageFilter, ImageDraw

from trdg import computer_text_generator, background_generator, distorsion_generator

try:
    from trdg import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background_type,
        distorsion_type,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        fit,
        output_mask,
        word_split,
        image_dir,
        bounding_box,
        draw_bbox,
        radius,
    ):
        image = None

        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image, mask = handwritten_text_generator.generate(text, text_color)
        else:
            image, mask, boxs = computer_text_generator.generate(
                text,
                font,
                text_color,
                size,
                orientation,
                space_width,
                character_spacing,
                fit,
                word_split,
                radius,
            )
        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

        rotated_img = image.rotate(
            skewing_angle if not random_skew else random_angle, expand=True
        )

        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=True
        )
        
        ########## Written by xy.huang ##########
        ########## Rotate bounding_boxs########## 
        if bounding_box == True:
         
            expand_matrix = np.stack([
                (rotated_img.width - image.width) /2, 
                (rotated_img.height - image.height) /2
                ], axis=0)
            
            scaler = np.stack([rotated_img.width, rotated_img.height], axis=0)
            center = np.reshape(0.5*scaler, [1, 2])

            angle = skewing_angle if not random_skew else random_angle
            theta = (360 - angle) * ( math.pi/180.0)

            rotation = np.stack([np.cos(theta), np.sin(theta),-np.sin(theta), np.cos(theta)], axis=0)
            rotation_matrix = np.reshape(rotation, [2, 2])
            
            for i in range(len(boxs)):
                box = np.reshape(boxs[i], (4, 2))
                box = box + expand_matrix
                box = np.matmul(box - center, rotation_matrix) + center
                boxs[i] = np.reshape(box, (8, )).tolist()
            
        ########## Written by xy.huang ##########
        
        
        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
            distorted_mask = rotated_mask
        elif distorsion_type == 1:
            distorted_img, distorted_mask = distorsion_generator.sin(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        elif distorsion_type == 2:
            distorted_img, distorted_mask = distorsion_generator.cos(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        else:
            distorted_img, distorted_mask = distorsion_generator.random(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )

        ##################################
        # Resize image to desired format #
        ##################################

        original_width, original_height = distorted_img.size
        # Horizontal text
        if orientation == 0:
            new_width = int(
                distorted_img.size[0]
                * (float(size - vertical_margin) / float(distorted_img.size[1]))
            )
            resized_img = distorted_img.resize(
                (new_width, size - vertical_margin), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize((new_width, size - vertical_margin), Image.NEAREST)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size

            if bounding_box == True:
                width_scale = new_width/original_width
                height_scale = (size - vertical_margin)/original_height

        # Vertical text
        elif orientation == 1:
            new_height = int(
                float(distorted_img.size[1])
                * (float(size - horizontal_margin) / float(distorted_img.size[0]))
            )
            resized_img = distorted_img.resize(
                (size - horizontal_margin, new_height), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize(
                (size - horizontal_margin, new_height), Image.NEAREST
            )
            background_width = size
            background_height = new_height + vertical_margin
        
            if bounding_box == True:
                width_scale = (size - horizontal_margin)/original_width
                height_scale = new_height/original_height
        
        #Curved text
        elif orientation == 2:
            resized_img = distorted_img
            resized_mask = distorted_img
            background_width = resized_img.width
            background_height = resized_img.height
            
            if bounding_box == True:
                width_scale = 1
                height_scale = 1
        else:
            raise ValueError("Invalid orientation")
        
        ########## Written by xy.huang ##########
        if bounding_box == True:
            for box in boxs:
                for i in range(8):
                    if i%2 == 0 :
                        box[i] = box[i] * width_scale
                    else:
                        box[i] = box[i] * height_scale
        ########## Written by xy.huang ##########
        
        
        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_dir
            )
        background_mask = Image.new(
            "RGB", (background_width, background_height), (0, 0, 0)
        )
        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size

        if alignment == 0 or width == -1:
            background_img.paste(resized_img, (margin_left, margin_top), resized_img)
            background_mask.paste(resized_mask, (margin_left, margin_top))
            background_offset_width = margin_left
        elif alignment == 1:
            background_img.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (int(background_width / 2 - new_text_width / 2), margin_top),
            )
            background_offset_width = int(background_width / 2 - new_text_width / 2)
        else:
            background_img.paste(
                resized_img,
                (background_width - new_text_width - margin_right, margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (background_width - new_text_width - margin_right, margin_top),
            )
            background_offset_width = background_width - new_text_width - margin_right
        ########## Written by xy.huang ##########
        if bounding_box == True:
            for box in boxs:
                for i in range(8):
                    if i%2 == 0 :
                        box[i] = box[i] + background_offset_width 
                    else:
                        box[i] = box[i] + margin_top
        ########## Written by xy.huang ##########

        ##################################
        # Apply gaussian blur #
        ##################################

        gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        final_image = background_img.filter(gaussian_filter)
        final_mask = background_mask.filter(gaussian_filter)
        
        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
            txt_name = "{}_{}.txt".format(text, str(index))
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
            mask_name = "{}_{}_mask.png".format(str(index), text)
            txt_name = "{}_{}.txt".format(str(index), text)
        elif name_format == 2:
            image_name = "{}.{}".format(str(index), extension)
            mask_name = "{}_mask.png".format(str(index))
            txt_name = "{}.txt".format(str(index))
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
            txt_name = "{}_{}.txt".format(text, str(index))
        
        
        # Draw coordinate
        if draw_bbox == True:
            if bounding_box != True:
                raise ValueError("Draw bounding_box only works with -bb or --bounding_box")
            bboxDraw = ImageDraw.Draw(final_image)
            for box in boxs:
                bboxDraw.polygon(box, outline = (255, 0, 0))

        splitted_text = []
        for p in text:
            if p != ' ':
                splitted_text.append(p)
        
        # Save the image
        if out_dir is not None:
            final_image.convert("RGB").save(os.path.join(out_dir, image_name))
            if output_mask == 1:
                final_mask.convert("RGB").save(os.path.join(out_dir, mask_name))
            if bounding_box == True:
                with open (os.path.join(out_dir, txt_name), mode = 'w') as f:
                    for box, p  in zip(boxs, splitted_text):
                        f.writelines(str(box) + p)
                        f.write('\r\n')
        else:
            if output_mask == 1:
                #return final_image.convert("RGBA"), final_mask.convert("RGB"), boxs
                return final_image, final_mask, boxs
            #return final_image.convert("RGBA"), boxs
            return final_image, boxs
