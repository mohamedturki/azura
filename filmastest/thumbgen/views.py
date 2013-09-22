import StringIO
import os

from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic.base import View

from azure.storage import BlobService
from PIL import Image

blob_service = BlobService(
    account_name=settings.AZURE_STORAGE_ACCOUNT,
    account_key=settings.AZURE_STORAGE_KEY
)


class ThumbnailGeneratorView(View):

    def get(self, request):
        size = request.GET.get('size', "100x100").split("x")
        path = request.GET.get('path')

        image_stream = blob_service.get_blob(
            settings.AZURE_STORAGE_CONTAINER,
            path
        )
        image = Image.open(StringIO.StringIO(image_stream))
        image = image.resize((int(size[0]), int(size[1])), Image.ANTIALIAS)

        original_filename = path.split('/')[-1]
        resized_image_filename = '{0}_{1}_{2}'.format(
            size[0], size[1], original_filename
        )
        resized_image_path = path.replace(
            original_filename, resized_image_filename
        )
        image.save(resized_image_filename)
        image_output = StringIO.StringIO()
        image.save(image_output, format="JPEG")

        blob_service.put_blob(
            settings.AZURE_STORAGE_CONTAINER,
            resized_image_path,
            image_output.getvalue(),
            x_ms_blob_type='BlockBlob',
            x_ms_blob_content_type='image/jpeg'
        )

        resized_blob = blob_service.list_blobs(
            settings.AZURE_STORAGE_CONTAINER, prefix=resized_image_path
        )
        del image
        os.remove(resized_image_filename)

        response = HttpResponseRedirect(
            resized_blob.blobs[0].url
        )

        response['Cache-Control'] = "max-age=414000"
        return response
