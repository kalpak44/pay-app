from django.shortcuts import render_to_response,redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
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
			args['login_error'] = "User not found. Please check your login and password."
			return render_to_response('index.html',args)
	else:
			redirect('/page/1')

def logout(request):
	auth.logout(request)
	return redirect('/')