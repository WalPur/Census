from django.shortcuts import render
from django.http import HttpResponse
from .forms import registrationForms
from .forms import signinForms

# Create your views here.
def index(request):
	return render(request, "index.html")
def registration(request):
	registForm = registrationForms()
	return render(request, "registation.html", {"form": registForm})
def signin(request):
	signinForm = signinForms()
	return render(request, "signin.html", {"form": signinForms})