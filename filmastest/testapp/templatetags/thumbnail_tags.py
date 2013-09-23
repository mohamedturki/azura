import urllib

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def thumbnail(path, size):
    image_size = size.split("x")
    filename = path.split('/')[-1]
    resized_image_filename = "{0}_{1}_{2}".format(
        image_size[0], image_size[1], filename
    )
    resized_image_path = path.replace(filename, resized_image_filename)

    image_url = "http://{0}.blob.core.windows.net/{1}/{2}".format(
        settings.AZURE_STORAGE_ACCOUNT,
        settings.AZURE_STORAGE_CONTAINER,
        resized_image_path
    )
    image = urllib.urlopen(image_url)

    if image.getcode() == 200:
        return image_url
    elif image.getcode() == 404:
        return "/generate/?path={0}&size={1}".format(path, size)
