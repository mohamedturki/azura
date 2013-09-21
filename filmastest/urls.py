from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^thumbnails/', 'testapp.views.index', name="index"),
        url(r'^generate/', 'thumbgen.views.generate_thumbnail', name="generate_thumbnail")        
)
