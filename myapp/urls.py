from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'), 
    path('signin/', views.signin, name='signin'),            
    path('logout/', views.custom_logout, name='logout'),         
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit-pdf/', views.edit_pdf, name='edit_pdf'), 
    path('merge-pdf/', views.merge_pdf, name='merge_pdf'),
    path('split-pdf/', views.split_pdf, name='split_pdf'),
    path('rotate-pdf/', views.rotate_pdf, name='rotate_pdf'),
    path('convert-pdf-to-images/', views.pdf_to_image, name='convert_pdf_to_images'),
    path('edit-image/', views.edit_image, name='edit_image'),
    path('remove-background/', views.remove_background, name='remove_background'),
    path('convert-images-to-pdf/', views.convert_images_to_pdf, name='convert_images_to_pdf'),
    path('image-editor/', views.image_editor, name='image_editor'),
    path('notifications/', views.view_notifications, name='notifications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
