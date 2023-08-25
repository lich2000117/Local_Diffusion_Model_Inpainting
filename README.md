# Extract 3D information from Diffusion Model inpainting scene.

This project is a workable diffusion inpainting model.
It is currently **WIP**. 
The aim of this project is to extract 3D information (depth, Manhattan structure) from the inpainted image.

This project utilizes a Conda environment to manage its dependencies.

This app uses the model from: https://huggingface.co/docs/diffusers/using-diffusers/inpaint
which is also available here: https://huggingface.co/runwayml/stable-diffusion-inpainting

## Getting Started

To try diffusion model inpainting, follow these steps:

### System requirement

- conda environment
- CUDA or Apple Silicon (or CPU)

### 0. Setup Environment

1. Clone this repo.

   ```bash
   git clone this_repo_link
   cd your-repo
   ```
2. Create and Activate the Conda Environment:

   - CUDA environment

      ```bash
      conda env create -f ./utils/environment_cuda.yml
      conda activate dfs_cuda
      ```
   - OR Apple Silicon environment

      ```bash
      conda env create -f ./utils/environment_apple.yml
      conda activate dfs_apple
      ```

   - OR use this website to install torch and other packages independently

      ```bash
      https://pytorch.org/get-started/locally/
      ```

### 1. Use GUI to create Mask (Where to generate new object)

    - Note that only images with their mask will be used in the model.

1. put your image (**1:1 ratio, must be in png format**) in "./images/" folder.
2. run script to select your image and use your pointer to create a bounding box(This will create a new mask image under "images" folder, do not change their name).
   ```bash
   python make_mask_functions/GUI_make_bounding_box.py
   ```
3. close all the windows popped up with the program.

### 2. Generate New Object

1. run script to start diffusion model (You may need to download model parameters upon first usage)

   ```bash
   python stable_diffusion.py
   ```
2. The program will ask you for the name of the image you wish to generate on. (for example if your image name is "mycat.png", you can just enter "my" or "mycat")

   For example:

   ```bash
   img1
   ```
3. The program will also ask you a sentence of what to generate

   ```
   "A chair on the ground"
   ```
4. It takes time to compute and generate
5. Check your results in images/outputs/xxxx_output.png

   For example:

   ```bash
   images/img1_output.png
   ```
