from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from pages.models import Page

from django.contrib import auth

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
# Create your views here.

#home page
def index(request):
	if not auth.get_user(request).is_authenticated():
		c = {}
		c.update(csrf(request))
		return render_to_response('index.html', c)
	else:
		html = "<h1>Redirect on private room</h1>"
		return HttpResponse(html)

#get page from id
def getPage(request, page_id):
	try:
		page = Page.objects.get(pk=page_id)
		if(page.isPublished):
			args = {}
			args['page'] = page
			args['username'] = auth.get_user(request).username
			return render_to_response('page-block.html',args)
		else:
			return render_to_response('404.html')
	except Page.DoesNotExist:
		return render_to_response('404.html')

