from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from django.template import Context, Template
from pages.models import Page

# Create your views here.

#home page
def index(request):
	view = "home"
	html = "<h1>This is %s page</h1>" %view
	return render_to_response('index.html')

#get page from id
def getPage(request, page_id):
	try:
		page = Page.objects.get(pk=page_id)
		return render_to_response('page-block.html',{'page':page})
	except Page.DoesNotExist:
		return render_to_response('404.html')

