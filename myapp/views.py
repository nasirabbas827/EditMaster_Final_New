from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import userform, userchangeform
from django.contrib.auth import login, logout
from django.contrib import messages

def home(request):
    return render(request, 'dashboard.html')

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = userform()
    return render(request, 'signup.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = userchangeform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
    else:
        form = userchangeform(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

@login_required
def edit_pdf(request):
    # Your edit PDF view logic goes here
    # This view should render the edit_pdf.html template
    # and handle any PDF editing actions
    return render(request, 'edit_pdf.html')

from django.shortcuts import render
from django.http import HttpResponse
from PyPDF4 import PdfFileReader, PdfFileWriter
import io

def merge_pdfs(pdf_files):
    pdf_writer = PdfFileWriter()

    for pdf_file in pdf_files:
        pdf_reader = PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

    output_pdf = io.BytesIO()
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)
    
    return output_pdf

def merge_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')
        merged_pdf = merge_pdfs(pdf_files)
        
        response = HttpResponse(merged_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged_pdf.pdf"'
        return response

    return render(request, 'merge_pdf.html')

import os
import zipfile
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from PyPDF2 import PdfReader, PdfWriter

def pdf_splitter(file):
    new_file_paths = []
    file_name = os.path.basename(file).split('.')[0]  # Extract file name without extension

    read_file = PdfReader(file)

    for i, page in enumerate(read_file.pages):
        new_pdf = PdfWriter()
        new_pdf.add_page(page)
        new_file_path = f"{file_name}_page_{i+1}.pdf"
        with open(new_file_path, "wb") as f:
            new_pdf.write(f)
        new_file_paths.append(new_file_path)

    return new_file_paths

def create_zip(file_paths):
    zip_path = 'split_pdf.zip'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))
    return zip_path

def split_pdf(request):
    user = request.user
    uploaded_pdfs = None
    split_pdf_paths = None
    
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        try:
            # Save the uploaded PDF temporarily
            with open('temp_pdf.pdf', 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)
            
            # Split the PDF
            split_pdf_paths = pdf_splitter('temp_pdf.pdf')
            print("PDF splitted Successfully")

            # Create a zip file containing the split PDFs
            zip_path = create_zip(split_pdf_paths)
            if zip_path:
                # Serve the zip file for download using FileResponse
                response = FileResponse(open(zip_path, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="split_pdf.zip"'
                return response
        except Exception as e:
            print(e)
            
        finally:
            # Clean up: remove temporary PDF and split PDF files
            os.remove('temp_pdf.pdf')
            if split_pdf_paths:
                for file_path in split_pdf_paths:
                    os.remove(file_path)
            
        return redirect('home')

    return render(request, 'split_pdf.html', {'user': user, 'uploaded_pdfs': uploaded_pdfs, 'split_pdf_paths': split_pdf_paths})


from PyPDF2 import PdfReader, PdfWriter
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.conf import settings

def rotate_pdf_pages(pdf_path, angle):
    file_name = os.path.basename(pdf_path).split('.')[0]  # Extract file name without extension
    output_path = f"{file_name}_rotated.pdf"

    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)

        with open(output_path, "wb") as out_f:
            writer.write(out_f)

    return output_path

def rotate_pdf(request):
    user = request.user
    uploaded_pdfs = None
    
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        angle = int(request.POST.get('angle', 0))  # Default angle is 0
        
        try:
            # Save the uploaded PDF temporarily
            with open('temp_pdf.pdf', 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)
            
            # Rotate the PDF
            rotated_pdf_path = rotate_pdf_pages('temp_pdf.pdf', angle)
            print("PDF rotated successfully")
            
            # Serve the rotated PDF for download
            with open(rotated_pdf_path, 'rb') as rotated_pdf_file:
                response = HttpResponse(rotated_pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(rotated_pdf_path)}"'
                return response
        except Exception as e:
            print(e)
            
        finally:
            # Clean up: remove temporary PDF and rotated PDF files
            os.remove('temp_pdf.pdf')
            if rotated_pdf_path:
                os.remove(rotated_pdf_path)
            
        return redirect('home')

    return render(request, 'rotate_pdf.html', {'user': user, 'uploaded_pdfs': uploaded_pdfs})


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
import os
import zipfile
from pdf2image import convert_from_path
from io import BytesIO

def pdf_to_image(request):
    user = request.user
    uploaded_pdfs = None
    
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        try:
            # Save the uploaded PDF temporarily
            with open('temp_pdf.pdf', 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)
            
            # Convert PDF to images
            images = convert_from_path('temp_pdf.pdf')
            if images:
                # Create a zip buffer to store images
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for i, image in enumerate(images):
                        image_path = f'image_{i+1}.jpg'
                        image.save(image_path, 'JPEG')
                        zip_file.write(image_path)
                        os.remove(image_path)  # Remove the image file after adding it to the zip
                
                zip_buffer.seek(0)
                # Serve the zip buffer as a response
                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="converted_images.zip"'
                return response
            else:
                # Handle if no images are generated
                return HttpResponse("No images found in the PDF.")
        except Exception as e:
            # Handle any errors during conversion
            return HttpResponse(f"Error: {e}")
        finally:
            # Clean up: remove temporary PDF file
            os.remove('temp_pdf.pdf')
    
    return render(request, 'pdf_to_images.html', {'user': user, 'uploaded_pdfs': uploaded_pdfs})


def edit_image(request):
    return render(request, 'edit_image.html')


from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from PIL import Image
from rembg import remove
import os

def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Get the uploaded image file
            image_file = request.FILES['image']
            
            # Define the directory for temporary images
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
            
            # Save the uploaded image temporarily
            temp_image_path = os.path.join(temp_dir, 'temp_image.png')
            with open(temp_image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            
            # Open the uploaded image
            input_image = Image.open(temp_image_path)
            
            # Remove the background from the image
            output_image = remove(input_image)
            
            # Define the directory for processed images
            output_dir = os.path.join(settings.MEDIA_ROOT, 'processed_images')
            os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
            
            # Define the output path for the processed image
            output_filename = f'processed_image.png'
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the processed image
            output_image.save(output_path)
            
            # Serve the processed image as a download
            with open(output_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="remove_bg_image.png"'
            return response
        
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'remove_background.html')

from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import img2pdf

def convert_images_to_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        try:
            # Get the uploaded images
            image_files = request.FILES.getlist('images')
            
            # Define the output directory for the PDF file
            output_dir = "media/converted_pdfs"
            os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
            
            # Create a list to store the paths of the converted images
            converted_image_paths = []
            
            # Convert each uploaded image to PDF
            for i, image_file in enumerate(image_files):
                # Save the uploaded image temporarily
                temp_image_path = os.path.join(output_dir, f"temp_image_{i}.png")
                with open(temp_image_path, 'wb') as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)
                
                # Open the uploaded image
                with Image.open(temp_image_path) as img:
                    # Convert the image to RGB mode to remove alpha channel
                    img = img.convert("RGB")
                    
                    # Define the output path for the converted image
                    output_image_path = os.path.join(output_dir, f"converted_image_{i}.jpg")
                    
                    # Save the image without alpha channel
                    img.save(output_image_path)
                    
                    # Add the path of the converted image to the list
                    converted_image_paths.append(output_image_path)
            
            # Convert the list of converted image paths to a single PDF
            pdf_path = os.path.join(output_dir, "converted_images.pdf")
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(converted_image_paths))
            
            # Serve the PDF for download
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="converted_images.pdf"'
                return response
        
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, 'pdf_images.html')

from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
from io import BytesIO
import os

def image_editor(request):
    return render(request, 'image_editor.html')

from django.shortcuts import render
from .models import Notification

def view_notifications(request):
    # Retrieve notifications for the current user
    notifications = Notification.objects.all()
    
    return render(request, 'notifications.html', {'notifications': notifications})
