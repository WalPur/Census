from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from .forms import registrationForms
from .forms import signinForms
from .forms import residenseForms
from .forms import docsForms
from .forms import comfirmForms
from .forms import codeForm
from .models import profile
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from smsc_api import *

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
		data = {"place": place, "num": count, "address": user.address}
		return render(request, "index.html", context=data)
	return render(request, "index.html")
def bonus(request):
	if request.user.is_authenticated:
		discount = 0
		user = profile.objects.get(user_id=request.user.id)
		if user.isActive == 1:
			discount += 10
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
		return redirect('/')
	if request.method == "POST":
		password = request.POST.get("password")
		if password != request.POST.get("passwordReInput"):
			data = {"form": registrationForms, "errorMessage": "Пароли не совпадают"}
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
		person.password = password

		user = User.objects.create_user(username, "",password)
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
	if request.user.is_authenticated:
		return redirect('/')
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
def docs(request):
	if not request.user.is_authenticated:
		return redirect('/')
	person = profile.objects.get(user_id=request.user.id)
	if request.method == "POST":
		SNILS = request.POST.get("SNILS")
		passportS = request.POST.get("passportS")
		passportN = request.POST.get("passportN")
		SNILS_ctrl = int(SNILS[12] + SNILS[13])
		SNILS_number = SNILS[0] + SNILS[1] + SNILS[2] + SNILS[4] + SNILS[5] + SNILS[6] + SNILS[8] + SNILS[9] + SNILS[10]
		childs = request.POST.get("childs")
		group = request.POST.get("group")
		person.childs = childs
		person.group = group
		person.SNILS_number = SNILS_number
		person.SNILS_ctrl = SNILS_ctrl
		person.passportN = request.POST.get("passportN")
		person.passportS = request.POST.get("passportS")
		person.save(update_fields=["passportS", "passportN", "SNILS_ctrl", "SNILS_number", 'childs', 'group'])
		user = User.objects.get(id=person.user_id)
		if person.SNILS_number != "" and (person.phone != "" or user.email != "") and person.locality != "" and person.isActive == 0:
			person.isActive = 1
			person.save(update_fields=["isActive"])
		return redirect('/bonus')
	return render(request, "dataFill.html", {'form': docsForms})
def residense(request):
	if not request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		person = profile.objects.get(user_id=request.user.id)
		district = request.POST.get("district")
		locality = request.POST.get("locality")
		address = request.POST.get("address")
		person.district = district
		person.locality = locality
		person.address = address
		person.save(update_fields=["district", "locality", "address"])
		user = User.objects.get(id=person.user_id)
		if person.SNILS_number != "" and (person.phone != "" or user.email != "") and person.locality != "" and person.isActive == 0:
			person.isActive = 1
			person.save(update_fields=["isActive"])
		return redirect('/bonus')
	return render(request, "dataFill.html", {'form': residenseForms})
def contacs(request):
	if not request.user.is_authenticated:
		return redirect('/')
	person = profile.objects.get(user_id=request.user.id)
	user = User.objects.get(id=person.user_id)
	if request.method == "POST":
		person = profile.objects.get(user_id=request.user.id)
		email = request.POST.get("email")
		phone = request.POST.get("phone")
		if email == phone:
			return render(request, "dataFill.html", {'form': comfirmForms, 'errorMessage': "Надо указать хотябы один"})
		user = User.objects.get(id=person.user_id)
		user.email = email
		person.phone = phone
		code = str(randint(100000, 999999))
		person.code = code
		if email != "" and phone != "":
			send_mail('Ваш код для дальнейшей авторизации', code, settings.EMAIL_HOST_USER, [email])
			string = "Ваш код для дальнейшей авторизации: " + code
			smsc = SMSC()
			r = smsc.send_sms(profile.phone, string, format=0, translit=1)
			print(r)
		elif email != "":
			send_mail('Ваш код для дальнейшей авторизации', code, settings.EMAIL_HOST_USER, [email])
		else:
			string = "Ваш код для дальнейшей авторизации: " + code
			smsc = SMSC()
			r = smsc.send_sms(profile.phone, string, format=0, translit=1)
			print(r)
		person.save(update_fields=['code', 'phone'])
		user.save(update_fields=['email'])
		return redirect('/code')
	return render(request, "dataFill.html", {'form': comfirmForms})
def code(request):
	if not request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		person = profile.objects.get(user_id=request.user.id)
		user = User.objects.get(id=person.user_id)
		code = request.POST.get("code")
		if code == person.code:
			person.code = ""
			if person.SNILS_number != "" and (person.phone != "" or user.email != "") and person.locality != "" and person.isActive == 0:
				person.isActive = 1
				person.save(update_fields=["isActive"])
		else:
			return render(request, "dataFill.html", {'form': codeForm, 'errorMessage': 'Код неправильно написан<br><a href="/contacs">Сменить номер, email</a>'})
		return redirect('/')
	return render(request, "dataFill.html", {'form': codeForm, 'errorMessage': '<a href="/contacs">Сменить номер, email</a>'})
def logout(request):
	django_logout(request)
	return redirect('/')
