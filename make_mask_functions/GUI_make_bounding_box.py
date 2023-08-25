import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import sys
sys.path.append('./utils')
from constants import *

class BoundingBoxDrawer:
    """This class asks user an image as input, using a user interface window to create a mask. 
    Then save this image to local disk with suffix. The images can be directly used in the diffusion inpainting model."""
    def __init__(self, root, image):
        self.root = root
        self.image = image

        self.canvas = tk.Canvas(root, width=512, height=512,cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.root.quit()

def resize_image(image_path):
    with Image.open(image_path) as im:
        return im.resize((512, 512))

def get_bbox_via_gui(image):
    root = tk.Tk()
    root.title("Draw Bounding Box")
    app = BoundingBoxDrawer(root, image)
    root.mainloop()

    coords = app.canvas.coords(app.rect)
    bbox = (coords[0], coords[1], coords[2], coords[3])
    return bbox

def create_mask(im, bbox):
    mask = Image.new('L', im.size, color=0)  # L mode for grayscale
    draw = ImageDraw.Draw(mask)
    draw.rectangle(bbox, fill=255)  # white color for the mask
    return mask

def save_mask_with_suffix(original_path, mask_img):
    # Split original path into directory, base name, and extension
    directory, filename = os.path.split(original_path)
    base_name, ext = os.path.splitext(filename)
    
    # Add suffix to the base name
    new_name = f"{base_name}_masked{ext}"
    
    # Combine to get new path
    new_path = os.path.join(directory, new_name)
    
    # Save mask to new path
    mask_img.save(new_path)
    return new_path

if __name__ == '__main__':
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", IMAGE_FORMAT)])
    if not image_path:
        print("No image selected. Exiting.")
        exit()

    # 1. Open and resize image
    image = resize_image(image_path)

    # 2. & 3. Let user specify bounding box via GUI
    bbox = get_bbox_via_gui(image)

    # 4. Create mask and show it
    mask = create_mask(image, bbox)# Save masked image

    # Save mask with suffix and display
    saved_path = save_mask_with_suffix(image_path, mask)
    print(f"Mask saved to {saved_path}")
    mask.show()