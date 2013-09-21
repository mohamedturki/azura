import StringIO
import os

from django.http import HttpResponseRedirect
from django.conf import settings

from azure.storage import BlobService
from PIL import Image

blob_service = BlobService(
    account_name=settings.AZURE_STORAGE_ACCOUNT,
    account_key=settings.AZURE_STORAGE_KEY
)


def generate_thumbnail(request):
    """
        Generates a thumbnail on demand
        and saves on Azure.
        1- open file locally (download from azure)
        2- resize the file.
        3- upload to Azure.
        4- return url
    """

    size = request.GET.get('size', "100x100").split("x")
    path = request.GET.get('path')

    image_stream = blob_service.get_blob(
        settings.AZURE_STORAGE_CONTAINER,
        path
    )
    image = Image.open(StringIO.StringIO(image_stream))
    image.thumbnail((int(size[0]), int(size[1])), Image.ANTIALIAS)

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

    return HttpResponseRedirect(
        resized_blob.blobs[0].url
    )
