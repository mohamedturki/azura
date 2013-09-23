from django.test import TestCase
from django.core.files import File
from django.template import Template, Context

from testapp.models import Film


class TemplateTagTest(TestCase):
    def setUp(self):
        self.film = Film()
        self.film.title = "Blow"
        self.film.poster = File(open("testdata/test_image.jpg"))
        self.film.save()

    def test_thumbnail_not_generated(self):
        out = Template(
            "{% load thumbnail_tags %}"
            "{% for film in films %}"
            "<img src='{% thumbnail size=\"50x50\" path=film.poster.name %}'/>"
            "{% endfor %}"
        ).render(Context({'films': Film.objects.all()}))

        self.assertEqual(
            out,
            "<img src='/generate/?path={0}&size=50x50'/>".format(
                self.film.poster.name
            )
        )

    def test_thumbnail_generated(self):
        self.film.poster = File(open("testdata/50_50_test_image.jpg"))
        self.film.save()

        out = Template(
            "{% load thumbnail_tags %}"
            "<img src='{% thumbnail size=\"50x50\" path=film.poster.name %}'/>"
        ).render(Context({'films': Film.objects.all()}))

        self.assertEqual(
            out,
            "<img src='{0}'/>".format(
                self.film.poster.url
            )
        )
        self.assertEqual(self.film.poster.name, self.film.poster.url)