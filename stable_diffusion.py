# 1. 
#  Install CUDA + torch using commandline or provided conda environment.yaml:
# 'conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia'
# Please Check website for latest version: https://pytorch.org/get-started/locally/  


# 1.1 Input images 
img_keyword = input("==== Please enter image name, if empty, the model will run all images in folder.: \n")
prompt = input("==== Please enter text prompt: \n")

# 2.
# setup where to store downloaded model cache
import os
os.environ['TRANSFORMERS_CACHE'] = r'F:\huggingface_cache'
os.environ['TORCH_HOME'] = r'F:\huggingface_cache'
os.environ["CACHE_DIR"] = r'F:\huggingface_cache'
os.environ["HF_HOME"] = r'F:\huggingface_cache'
os.environ["HF_DATASETS_CACHE"] = r'F:\huggingface_cache'


# 3.
# Setup Access token and image print
# from huggingface_hub.hf_api import HfFolder;
# ACCESS_TOKEN = ""
# HfFolder.save_token(ACCESS_TOKEN)
import sys
sys.path.append('./utils')
from functions import *
import matplotlib.pyplot as plt
import PIL
from diffusers import StableDiffusionInpaintPipeline



# 4.
# Create pipeline using optimal devices
print("\n---- Loading Model ----")
pipeline = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
)
# Determine Platform
try:
    pipeline.to("cuda")
    print("---- Using CUDA to compute ---- ")
except:
    try: 
        pipeline.to("mps")
        pipeline.enable_attention_slicing()
        print("---- Using Apple Silicon to compute ---- ")
    except:
        print("---- Using CPU to compute ---- ")


# 5.
def generate(img_keyword, prompt):
    """Use a function to wrap up so we can generate many times."""
    out_list = []
    img_name_list = get_image_pairs(img_keyword)
    for img, mask in img_name_list:
        # pass to model
        print("-- Processing IMAGE: " + img + " MASK: " + mask)
        init_image = PIL.Image.open(img)
        mask_image = PIL.Image.open(mask)
        output = pipeline(prompt=prompt, image=init_image, mask_image=mask_image).images[0]

        save_img_with_suffix(img, output, "output")
        out_list.append(output)
    print("---- Output Images has been saved in the local Folder. ----")
    for i in out_list:
        plt.figure(figsize=(12, 12))
        plt.imshow(i)
        plt.show()


generate(img_keyword, prompt)
while True:
    new_prompt = input("Input a new prompt to Regenerate OR type 'exit': \n")
    if new_prompt=="exit":
        break
    generate(img_keyword, new_prompt)
