import os
from PIL import Image
import numpy as np
from fpdf import FPDF

def calculate_brightness(image):
    grayscale_image = image.convert('L')
    np_image = np.array(grayscale_image)
    return np.mean(np_image)

def calculate_saturation(image):
    hsv_image = image.convert('HSV')
    np_image = np.array(hsv_image)
    saturation = np_image[:, :, 1] 
    return np.mean(saturation)

def create_thumbnail(image, size=(100, 100)):
    return image.copy().thumbnail(size)

def create_sorted_pdf(image_folder, output_pdf, sort_by='brightness'):
    images = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)
            
            if sort_by == 'brightness':
                metric = calculate_brightness(image)
            elif sort_by == 'saturation':
                metric = calculate_saturation(image)
            
            images.append((metric, image, filename))
    
    images.sort(reverse=True, key=lambda x: x[0])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    thumbnail_size = (100, 100)
    margin = 10
    images_per_row = 4
    x_offset, y_offset = margin, margin

    for i, (metric, image, filename) in enumerate(images):
        thumbnail = image.copy()
        thumbnail.thumbnail(thumbnail_size)
        pdf.image(thumbnail.filename, x=x_offset, y=y_offset, w=thumbnail_size[0], h=thumbnail_size[1])
        
        x_offset += thumbnail_size[0] + margin
        if (i + 1) % images_per_row == 0:
            x_offset = margin
            y_offset += thumbnail_size[1] + margin
        
        if y_offset > pdf.page_break_trigger - 20:
            pdf.add_page()
            x_offset, y_offset = margin, margin

    pdf.output(output_pdf)

image_folder = 'images_folder'  
output_pdf = 'sorted_images.pdf'
sort_by = input("Choose parameter of sorting (brightness/saturation): ").strip().lower()

create_sorted_pdf(image_folder, output_pdf, sort_by=sort_by)
