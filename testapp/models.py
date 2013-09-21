from django.db import models

from .storage import AzureStorage

class Film(models.Model):
	title = models.CharField(max_length=200)
	poster = models.ImageField(
        upload_to="test_thumbnails/",
        storage=AzureStorage(container="media")
    )

	def __unicode__(self):
		return self.title