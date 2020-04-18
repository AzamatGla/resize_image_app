from django.urls import path

from app.views import index_view, upload_view, image_view

urlpatterns = [
    path('', index_view, name='index'),
    path('upload/', upload_view, name='upload'),
    path('<int:pk>/', image_view, name='image')
]