from flask import Flask, request, send_file, render_template_string
import os
from PIL import Image
import numpy as np
from fpdf import FPDF
import tempfile

app = Flask(__name__)

def calculate_brightness(image):
    grayscale_image = image.convert('L')
    np_image = np.array(grayscale_image)
    return np.mean(np_image)

def calculate_saturation(image):
    hsv_image = image.convert('HSV')
    np_image = np.array(hsv_image)
    saturation = np_image[:, :, 1]
    return np.mean(saturation)

def create_sorted_pdf(image_folder, output_pdf, sort_by='brightness', max_width=200, max_height=200):
    images = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(image_folder, filename)
            try:
                image = Image.open(image_path)
                
                if sort_by == 'brightness':
                    metric = calculate_brightness(image)
                elif sort_by == 'saturation':
                    metric = calculate_saturation(image)
                
                images.append((metric, image_path))
            except (IOError, FileNotFoundError):
                print(f"Skipped invalid file: {filename}")

    if not images:
        print("No valid images found.")
        return

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

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return "No file part"
    
    images = request.files.getlist('images')
    sort_by = request.form.get('sort_by', 'brightness')

    with tempfile.TemporaryDirectory() as temp_dir:
        for img in images:
            img.save(os.path.join(temp_dir, img.filename))

        output_pdf = os.path.join(temp_dir, 'sorted_images.pdf')
        create_sorted_pdf(temp_dir, output_pdf, sort_by=sort_by)

        return send_file(output_pdf, as_attachment=True, download_name='sorted_images.pdf')

if __name__ == "__main__":
    app.run(debug=True)
