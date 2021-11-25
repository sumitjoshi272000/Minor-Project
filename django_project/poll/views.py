from django.shortcuts import render
from .forms import CreatePollForm
from .models import Poll
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def first(request):
	return render(request,'poll/first.html')

@login_required
def home(request):
	polls=Poll.objects.all()
	context={
	     'polls':polls
	}
	return render(request,'poll/home.html',context)

def create(request):
	if request.method == 'POST':
		form=CreatePollForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form=CreatePollForm()

	context={
	'form':form
	}
	return render(request,'poll/create.html',context)

def vote(request, poll_id):
	poll=Poll.objects.get(pk=poll_id)

	if request.method=='POST':
		selected_option=request.POST['poll']
		if selected_option=='option1':
			poll.option_one_count +=1
		elif selected_option=='option2':
			poll.option_two_count +=1
		elif selected_option=='option3':
			poll.option_three_count +=1
		else:
			return HttpResponse(400,'Invalid Form')

		poll.save()
		return redirect('results',poll.id)

	context={
	'poll':poll
	}
	return render(request,'poll/vote.html',context)
	
def results(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	context={
	'poll':poll
	}
	return render(request,'poll/results.html',context)

def register(request):
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form=UserCreationForm()

	return render(request,'poll/register.html',{'form':form})

def login(request):
	if request.method=='POST':
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			return redirect('home')
	else:
		form=AuthenticationForm()
	return render(request,'poll/login.html',{'form':form})

def logout(request):
	return redirect(login)
	return render(request,'poll/logout.html')