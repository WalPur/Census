from django import forms

class registrationForms(forms.Form):
	surname = forms.CharField(label="Фамилия")
	name = forms.CharField(label="Имя")
	patronymic = forms.CharField(label="Отчество")

	SNILS = forms.CharField(label="СНИЛС")
	passportS = forms.IntegerField(label="Серия пасспорта")
	passportN = forms.IntegerField(label="Номер пасспорта")

	district = forms.CharField(label="Район")
	locality = forms.CharField(label="Населеннный пункт")
	address = forms.CharField(label="Адрес дома")

	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
	passwordReInput = forms.CharField(label="Подтвердите", widget=forms.PasswordInput)
	
	email = forms.CharField(label="Электронная почта", required=False)
	phone = forms.EmailField(label="Номер телефона")
	avatar = forms.ImageField(label="Фото профиля")

class signinForms(forms.Form):
	login = forms.CharField(label="СНИЛС или номер телефона")
	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)