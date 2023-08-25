import os
import glob
from constants import *

def get_image_pairs(keyword=""):

    folder_path = FOLDER
    original_image_extension = IMAGE_FORMAT
    masked_image_suffix = MASK_SUFFIX

    image_pairs = []
    for extension in original_image_extension:
        original_images = glob.glob(os.path.join(folder_path, '*' + extension))
        for original_image in original_images:
            masked_image_name = os.path.splitext(original_image)[0] + masked_image_suffix + os.path.splitext(original_image)[1]
            if os.path.exists(masked_image_name) and keyword in original_image:
                image_pairs.append((original_image, masked_image_name))
    return image_pairs



def save_img_with_suffix(original_path, image_to_save, suffix):
    # Split original path into directory, base name, and extension
    directory, filename = os.path.split(original_path)
    base_name, ext = os.path.splitext(filename)
    
    # Add suffix to the base name
    new_name = f"{base_name}_{suffix}{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, new_name)

    # Combine to get new path
    new_path = os.path.join(directory, output_path)
    
    # Save mask to new path
    image_to_save.save(new_path)
    print("---- Image saved to path: ", new_path)
    return new_path