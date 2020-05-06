from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from .forms import registrationForms
from .forms import signinForms
from .models import profile
from random import randint

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		user = profile.objects.get(user_id=request.user.id)
		place = user.district + " " + user.locality
		people = profile.objects.in_bulk()
		count = 0
		for id in people:
			if place == people[id].district + " " +  people[id].locality:
				count += 1
		data = {"place": place, "num": count, "address": user.address, "dateOfBirth": user.dateOfBirth}
		return render(request, "index.html", context=data)
	return render(request, "index.html")
def bonus(request):
	if request.user.is_authenticated:
		discount = 10
		user = profile.objects.get(user_id=request.user.id)
		if user.group != 0:
			if user.group == 1:
				discount += 20
			elif user.group == 2:
				discount += 10
			else:
				discount += 5 #Третья группа
		if user.childs >= 3:
			discount += 10 + (user.childs - 3) * 2.5
		data = {"discount": discount, "token": user.token}
		return render(request, "bonus.html", context=data)
	return render(request, "bonus.html")
def news(request):
	return render(request, "news.html")
def info(request):
	return render(request, "info.html")
def registration(request):
	if request.user.is_authenticated:
		return redirect('/lk')
	if request.method == "POST":
		password = request.POST.get("password")
		if password != request.POST.get("passwordReInput"):
			data = {"form": registForm, "errorMessage": "Пароли не совпадают"}
			return render(request, "registration.html", context=data)

		#Надо добавить валидацию по СНИЛС

		person = profile()
		surname = request.POST.get("surname")
		name = request.POST.get("name")
		patronymic = request.POST.get("patronymic")
		username = surname + " " + name + " " + patronymic

		person.username = username
		person.surname = surname
		person.name = name
		person.patronymic = patronymic

		dateOfBirth = request.POST.get("dateOfBirth")

		person.dateOfBirth = dateOfBirth

		SNILS = request.POST.get("SNILS")
		passportS = request.POST.get("passportS")
		passportN = request.POST.get("passportN")
		SNILS_ctrl = int(SNILS[12] + SNILS[13])
		SNILS_number = SNILS[0] + SNILS[1] + SNILS[2] + SNILS[4] + SNILS[5] + SNILS[6] + SNILS[8] + SNILS[9] + SNILS[10]

		person.SNILS_number = SNILS_number
		person.SNILS_ctrl = SNILS_ctrl
		person.passportN = request.POST.get("passportN")
		person.passportS = request.POST.get("passportS")

		district = request.POST.get("district")
		locality = request.POST.get("locality")
		address = request.POST.get("address")

		person.district = district
		person.locality = locality
		person.address = address

		email = request.POST.get("email")
		phone = request.POST.get("phone")
		avatar = request.POST.get("avatar")

		person.email = email
		person.phone = phone
		person.avatar = avatar

		person.password = password

		childs = request.POST.get("childs")
		group = request.POST.get("group")

		person.childs = childs
		person.group = group

		user = User.objects.create_user(username, email, password)
		user.save()
		person.user = user
		
		user = authenticate(username=username, password=password)
		login(request, user)

		num1 = randint(100000000, 999999999)
		num2 = randint(1000000000, 9999999999)
		person.token = str(num1) + ":" + str(num2)
		person.save()
		return redirect("/")
	registForm = registrationForms()
	data = {"form": registForm}
	return render(request, "registration.html", context=data)
def signin(request):
	if request.method == "POST":
		fullName = request.POST.get("login")
		password = request.POST.get("password")
		print(fullName)
		user = authenticate(username = fullName, password = password)
		if user != None:
			if user.is_active:
				login(request, user)
				return redirect('/')
	signinForm = signinForms()
	return render(request, "signin.html", {"form": signinForms})
def logout(request):
	django_logout(request)
	return redirect('/')