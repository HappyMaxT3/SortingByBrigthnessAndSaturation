import os
from PIL import Image
import numpy as np
from fpdf import FPDF

# function to calculate the brightness of an image
def calculate_brightness(image):
    grayscale_image = image.convert('L')
    np_image = np.array(grayscale_image)
    return np.mean(np_image)

# function to calculate the saturation of an image
def calculate_saturation(image):
    hsv_image = image.convert('HSV')
    np_image = np.array(hsv_image)
    saturation = np_image[:, :, 1]
    return np.mean(saturation)

# function to create a sorted PDF from images based on brightness or saturation
def create_sorted_pdf(image_folder, output_pdf, sort_by='brightness', max_width=200, max_height=200):
    images = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)
            
            if sort_by == 'brightness':
                metric = calculate_brightness(image)
            elif sort_by == 'saturation':
                metric = calculate_saturation(image)
            else:
                print(f"Invalid sort parameter '{sort_by}'. Defaulting to brightness.")
                metric = calculate_brightness(image)
            
            images.append((metric, image_path))

    images.sort(reverse=True, key=lambda x: x[0])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=5)
    pdf.add_page()

    margin = 1
    y_offset = margin

    for i, (metric, image_path) in enumerate(images):
        image = Image.open(image_path)
        original_width, original_height = image.size
        
        scale = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        page_width = pdf.w - 2 * margin
        x_offset = (page_width - new_width) / 2

        if y_offset + new_height > pdf.page_break_trigger - 5:
            pdf.add_page()
            y_offset = margin

        pdf.image(image_path, x=x_offset, y=y_offset, w=new_width, h=new_height)
        
        y_offset += new_height + margin

    pdf.output(output_pdf)
