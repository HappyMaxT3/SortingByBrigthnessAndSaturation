
# Sorting Images by Brightness and Saturation

This project is a web application built with Flask that allows users to upload images, sort them by brightness or saturation, and generate a previewable and downloadable PDF file of sorted images. The site also provides a preview of the generated PDF before download.

## Features

- Upload multiple images
- Sort images by brightness or saturation
- Generate a PDF with the sorted images
- Preview the generated PDF in the browser
- Download or print the PDF file

## Prerequisites

- Python 3.x
- Flask
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://git.miem.hse.ru/mstolmachev/sortingbybrigthnessandsaturation_gitlab.git
```

### 2. Creating and Activating a Virtual Environment

To prevent dependency conflicts, it's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Installing Dependencies

Install the necessary dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Running the Application

Once the dependencies are installed, you can run the application using Flask:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # Optional for debug mode
flask run
```

Alternatively, on Windows:

```bash
set FLASK_APP=app.py
flask run
```

The application will be available at `http://127.0.0.1:8000/`.

## 5. Functionalities of the Application

- **Upload Images**: Users can upload multiple image files (allowed extensions: `.png`, `.jpg`, `.jpeg`).
- **Sorting Options**: Users can sort the images based on brightness or saturation.
- **PDF Generation**: After sorting, the images are compiled into a PDF that can be previewed in the browser.
- **Preview and Download**: Users can preview the generated PDF and download it if necessary.

## 6. Project Structure

```bash
sorting-images/
│
├── app.py                        # Main Flask application
├── image_processing.py           # Image processing and PDF generation logic
├── static/                       # Static files like CSS and images
│   ├── uploaded_images/          # Temporary folder for uploaded images
|   ├── css/styles.css            # Styles for HTML page
|   ├── images/                   # GIFs for HTML page
|   ├── fonts/                    # GIFs for HTML page
│   └── sorted_images.pdf         # Generated output PDF file
│
├── templates/                    # HTML templates for rendering pages
│   └── index.html                # Main page for uploading images and displaying the PDF preview
│
├── requirements.txt              # Python package dependencies
└── README.md                     # Project documentation
```

### 7. Code Overview

#### app.py

- **Flask Application**: The main application that handles routes, file uploads, and PDF generation.
- **Routes**:
  - `/`: Handles the main page for uploading images and sorting them.
  - `/download`: Handles the download of the generated PDF file.

#### image_processing.py

- **Functions**:
  - `create_sorted_pdf(upload_folder, output_pdf, sort_by)`: Processes uploaded images, sorts them based on the specified criterion (brightness or saturation), and generates a PDF.

### 8. Building and Running with Docker

#### Building the Docker Image:

To build a Docker image for the application, run the following command:

```bash
docker build -t sorting-images .
```

#### Running the Application in Docker:

To run the application using Docker, execute:

```bash
docker run -d -p 8000:8000 sorting-images
```

### 9. Pushing the Docker Image to a Repository:

To push the Docker image to a repository (e.g., Docker Hub), follow these steps:

1. Log in to Docker Hub:

```bash
docker login
```

2. Tag your image:

```bash
docker tag sorting-images your-username/sorting-images:latest
```

3. Push the image:

```bash
docker push your-username/sorting-images:latest
```

## Conclusion

This web application provides a simple interface for sorting images by brightness or saturation and generating a PDF. With the added functionality of Docker, it can easily be deployed in various environments. Directed by the marvelous Max Tolmachev, a big fan of brutal skeletons, rum, video games and programming.
