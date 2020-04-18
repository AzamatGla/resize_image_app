import io

from PIL import Image
from django.test import TestCase
from django.urls import reverse


class ResponseTest(TestCase):
    def test_index_page(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_page(self):
        response = self.client.get('/upload/', follow=True)
        self.assertEqual(response.status_code, 200)


class UploadPhotoTests(TestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_photo(self):

        url = reverse('upload')

        photo_file = self.generate_photo_file()

        data = {
                'file':photo_file
            }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 302) #302 redirect

