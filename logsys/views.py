from django.shortcuts import render_to_response,redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from django.contrib import auth
from .forms import RegistrationForm
from .models import User

# Create your views here.


def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		args['login_error'] = "POST"
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			args['login_error'] = "Please check your login and password."
			return render_to_response('login.html',args)
	else:
			redirect('/page/1')

def logout(request):
	auth.logout(request)
	return redirect('/')

def register(request):
	args = {}
	args.update(csrf(request))
	if auth.get_user(request).is_authenticated():
		return redirect('/')
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			user = User.objects.create_user(username, email, password)
			user.save()
			user = auth.authenticate(username=username, password=password)
			auth.login(request,user)
			return redirect('/')
	else:
		form = RegistrationForm()
	args['form']=form
	return render_to_response('registration.html',args)