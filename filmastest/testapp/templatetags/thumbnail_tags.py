from django import template
from django.conf import settings

from azure.storage import BlobService
from azure import WindowsAzureMissingResourceError

register = template.Library()
blob_service = BlobService(
    account_name=settings.AZURE_STORAGE_ACCOUNT,
    account_key=settings.AZURE_STORAGE_KEY
)


@register.simple_tag
def thumbnail(path, size):
    image_size = size.split("x")
    try:
        filename = path.split('/')[-1]
        resized_image_filename = "{0}_{1}_{2}".format(
            image_size[0], image_size[1], filename
        )
        resized_image_path = path.replace(filename, resized_image_filename)

        blob = blob_service.list_blobs(
            settings.AZURE_STORAGE_CONTAINER, prefix=resized_image_path
        )
        if blob.blobs:
            return blob.blobs[0].url
        else:
            return "/generate/?path={0}&size={1}".format(path, size)
    except WindowsAzureMissingResourceError:
        return "/generate/?path={0}&size={1}".format(path, size)
