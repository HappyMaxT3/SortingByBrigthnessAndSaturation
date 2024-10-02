import os
import shutil
from flask import Flask, request, render_template, send_file, url_for
from werkzeug.utils import secure_filename
from image_processing import create_sorted_pdf

app = Flask(__name__)
STATIC_FOLDER = 'static'  # static directory to store temporary files (Flask troubles)
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploaded_images')  # directory to store uploaded images
OUTPUT_PDF = os.path.join(STATIC_FOLDER, 'sorted_images.pdf')   # output PDF file path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # allowed image file extensions

# function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# function to clear temporary files
def clear_temporary_files():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)  # remove the directory with uploaded images
        print(f"Temporary files deleted: {UPLOAD_FOLDER}")
    if os.path.exists(OUTPUT_PDF):
        os.remove(OUTPUT_PDF)  # remove the PDF file
        print(f"Output file deleted: {OUTPUT_PDF}")

# route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    pdf_ready = False  # variable to track if the PDF is ready for download
    pdf_url = None  
    pdf_preview_url = None 

    if request.method == 'POST':
        # create the static and upload directories if they don't exist
        if not os.path.exists(STATIC_FOLDER):
            os.makedirs(STATIC_FOLDER)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # check if 'images_folder' is in the request files
        if 'images_folder' not in request.files:
            return "Error: No files selected", 400

        # saving multiple files uploaded by the user
        files = request.files.getlist('images_folder')
        if not files:
            return "Error: No files selected", 400
        
        # iterate over the uploaded files and save them
        for file in files:
            if file and allowed_file(file.filename): 
                filename = secure_filename(file.filename)  # secure the filename
                file_path = os.path.join(UPLOAD_FOLDER, filename)  # create full file path
                file.save(file_path)  # save the file to the upload folder
                print(f"Saved file: {file_path}") 
        
        # check the selected sorting method
        sort_by = request.form.get('sort_by', 'brightness')
        
        try:
            print("Creating PDF...") 
            # call the function to create the sorted PDF from uploaded images
            create_sorted_pdf(UPLOAD_FOLDER, OUTPUT_PDF, sort_by=sort_by)
            print(f"PDF created at: {os.path.abspath(OUTPUT_PDF)}")  # debug message
            pdf_ready = True
            pdf_url = url_for('download_file')  # get the URL for downloading the PDF
            pdf_preview_url = url_for('static', filename='sorted_images.pdf')  # URL for PDF preview
        except Exception as e:
            return f"Error creating PDF: {str(e)}", 500  # return error if PDF creation fails

    return render_template('index.html', pdf_ready=pdf_ready, pdf_url=pdf_url, pdf_preview_url=pdf_preview_url)

# route for downloading the generated PDF
@app.route('/download')
def download_file():
    # check if the PDF file exists
    if os.path.exists(OUTPUT_PDF):
        print("PDF exists and ready for download")  # debug message
        
        # send the PDF file as an attachment to the user
        response = send_file(OUTPUT_PDF, as_attachment=True)

        # clear temporary files after sending the response
        clear_temporary_files()

        return response
    else:
        print("PDF file not found") 
        return "File not found", 404 

# main entry point for the application
if __name__ == '__main__':
    app.run(port=8000, debug=True)
