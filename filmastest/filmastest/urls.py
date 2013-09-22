from django.conf.urls import patterns, include, url
from django.contrib import admin

from thumbgen.views import ThumbnailGeneratorView

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^generate/', ThumbnailGeneratorView.as_view(), name="generate_thumbnail"),
        url(r'^$', 'testapp.views.index', name="index"),
                
)
