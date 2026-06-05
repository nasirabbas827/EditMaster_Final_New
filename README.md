# EditMaster_Final_New  

A lightweight Django‑based web application that lets users upload PDF documents, convert each page to an image, and perform simple editing operations directly in the browser. The project demonstrates how to integrate PDF processing, image handling, and a clean HTML front‑end within a single Python/Django codebase.

---  

## Overview  

`EditMaster_Final_New` provides a minimal yet functional interface for:

* Uploading PDF files.  
* Converting PDF pages to images (JPEG/PNG).  
* Displaying the generated images in a responsive HTML UI.  
* Saving edited images back to the server (future extension).  

The repository contains the full Django project (`education` and `myapp` apps), a PDF specification document, and sample media files generated during conversion.

---  

## Features  

| ✅ | Feature |
|---|---------|
| 📄 | PDF upload with server‑side validation |
| 🖼️ | Automatic conversion of each PDF page to an image |
| 📂 | Media storage (`media/converted_pdfs/`) for generated images |
| 🛠️ | Clean, responsive HTML templates (primary language: HTML) |
| 🧩 | Extensible Django architecture (apps, forms, models, URLs) |
| 🐍 | Ready‑to‑run `manage.py` commands for development and testing |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Django 4.x |
| **PDF → Image** | `pdf2image`, `poppler` (system dependency) |
| **Image Handling** | Pillow |
| **Front‑end** | HTML5, CSS3 (Bootstrap optional) |
| **Database** | SQLite (default) |
| **Deployment** | WSGI/ASGI compatible (e.g., Gunicorn, Daphne) |

---  

## Installation  

> **Prerequisite:** Ensure you have Python 3.9+ installed and `git` available on your machine.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/EditMaster_Final_New.git
cd EditMaster_Final_New

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install django pillow pdf2image

# 4. Install Poppler (required by pdf2image)
# macOS (Homebrew)
brew install poppler
# Ubuntu/Debian
sudo apt-get install poppler-utils
# Windows – download from https://github.com/oschwartz10612/poppler-windows/releases
#   and add the bin folder to your PATH
```

> **Optional:** If a `requirements.txt` file is added later, replace step 3 with `pip install -r requirements.txt`.

---  

## Usage  

```bash
# Apply migrations (creates the default SQLite DB)
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

1. Open your browser and navigate to `http://127.0.0.1:8000/`.  
2. Use the **Upload PDF** form to select a PDF file.  
3. After upload, the server converts each page to an image and stores them under