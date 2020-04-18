import re

from django.shortcuts import render, redirect
from app.models import ImageModel
from urllib.parse import urlparse
from app.forms import ImageForm
from project import settings
from PIL import Image
import tempfile
import requests
import shutil
import os


def index_view(request):
    image_list = ImageModel.objects.all()
    return render(request, 'index.html', {'image_list': image_list})


def upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['link']:
                image = ImageModel.objects.create()
                link_path = urlparse(form.cleaned_data['link'])
                name = os.path.basename(link_path.path)
                temp_file = tempfile.NamedTemporaryFile()
                temp_file.write(requests.get(form.cleaned_data['link'], stream=True).content)
                image.file.save(name, temp_file)
            elif form.cleaned_data['file']:
                form.save()
            return redirect('index')
    elif request.method == 'GET':
        form = ImageForm()
        return render(request, 'upload.html', {'form': form})


def image_view(request, pk=None):
    if request.method == 'GET':
        if pk and ImageModel.objects.filter(id=pk).exists():
            image = ImageModel.objects.get(id=pk)
            img = Image.open(image.file.path)
            width = request.GET.get('width', None)
            height = request.GET.get('height', None)
            max_size = request.GET.get('max_size', None)
            if re.match(r'^\d+$', str(width)):
                width = int(width)
            else:
                width = None
            if re.match(r'^\d+$', str(height)):
                height = int(height)
            else:
                height = None
            if re.match(r'^\d+$', str(max_size)):
                max_size = int(max_size)
            else:
                max_size = None
            image_url = image.file.url
            if width and height:
                image_path = os.path.join(settings.MEDIA_ROOT, 'tmp', f'{width}_{height}_{image.filename()}')
                shutil.copy2(image.file.path, image_path)
                tmp_image = Image.open(image_path)
                tmp_image = tmp_image.resize((int(width), int(height)), Image.ANTIALIAS)
                tmp_image.save(image_path)
                image_url = settings.MEDIA_URL + 'tmp/' + f'{width}_{height}_{image.filename()}'
            elif width:
                wpercent = (int(width) / float(img.width))
                hsize = int((float(img.height) * float(wpercent)))
                image_path = os.path.join(settings.MEDIA_ROOT, 'tmp', f'{width}_{hsize}_{image.filename()}')
                shutil.copy2(image.file.path, image_path)
                tmp_image = Image.open(image_path).resize((int(width), hsize), Image.ANTIALIAS)
                tmp_image.save(image_path)
                image_url = settings.MEDIA_URL + 'tmp/' + f'{width}_{hsize}_{image.filename()}'
            elif height:
                hpercent = (int(height) / float(img.height))
                wsize = int((float(img.width) * float(hpercent)))
                image_path = os.path.join(settings.MEDIA_ROOT, 'tmp', f'{wsize}_{height}_{image.filename()}')
                shutil.copy2(image.file.path, image_path)
                tmp_image = Image.open(image_path).resize((wsize, int(height)), Image.ANTIALIAS)
                tmp_image.save(image_path)
                image_url = settings.MEDIA_URL + 'tmp/' + f'{wsize}_{height}_{image.filename()}'
            if max_size:
                image_path = os.path.join(settings.BASE_DIR, image_url.strip('/'))
                tmp_image = Image.open(image_path)
                filesize = os.path.getsize(image_path)
                if filesize > max_size:
                    aspect = tmp_image.width / tmp_image.height
                    size_deviation = filesize / max_size
                    new_width = tmp_image.width / size_deviation ** 0.5
                    new_height = new_width / aspect
                    image_path = os.path.join(settings.MEDIA_ROOT, 'tmp', f'{new_width}_{new_height}_{image.filename()}')
                    shutil.copy2(image.file.path, image_path)
                    tmp_image = tmp_image.resize((int(new_width), int(new_height)))
                    tmp_image.save(image_path)
                    image_url = settings.MEDIA_URL + 'tmp/' + f'{new_width}_{new_height}_{image.filename()}'
            return render(request, 'image.html', {'image': image_url})