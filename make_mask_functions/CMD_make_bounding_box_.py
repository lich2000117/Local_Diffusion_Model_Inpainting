from PIL import Image, ImageDraw

def resize_image(image_path):
    with Image.open(image_path) as im:
        return im.resize((512, 512))

def get_bbox_input():
    print("Please input the bounding box coordinates as 'x1 y1 x2 y2':")
    x1, y1, x2, y2 = map(int, input().split())
    return x1, y1, x2, y2

def create_mask(im, bbox):
    mask = Image.new('L', im.size, color=0)  # L mode for grayscale
    draw = ImageDraw.Draw(mask)
    draw.rectangle(bbox, fill=255)  # white color for the mask
    return mask

if __name__ == '__main__':
    image_path = input("Enter the image path: ")

    # 1. Open and resize image
    image = resize_image(image_path)

    # 2. & 3. Let user specify bounding box
    bbox = get_bbox_input()

    # 4. Create mask and show it
    mask = create_mask(image, bbox)
    mask.show()
    mask.save("masked_image.png")  # Save masked image
