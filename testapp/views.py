from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Film


def index(request):
    return render_to_response(
        'thumbnails_list.html',
        {'films': Film.objects.all()},
        context_instance=RequestContext(request)
    )
    # return HttpResponseRedirect('')
