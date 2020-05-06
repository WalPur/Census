from django import forms

class registrationForms(forms.Form):
	surname = forms.CharField(label="Фамилия")
	name = forms.CharField(label="Имя")
	patronymic = forms.CharField(label="Отчество")

	dateOfBirth = forms.DateField(label="Дата рождения", help_text="год/месяц/день или год-месяц-день", input_formats=['%d/%m/%Y', '%d-%m-%Y'])

	SNILS = forms.CharField(label="СНИЛС", min_length=14, max_length=14)
	passportS = forms.IntegerField(label="Серия пасспорта")
	passportN = forms.IntegerField(label="Номер пасспорта")

	district = forms.CharField(label="Район")
	locality = forms.CharField(label="Населеннный пункт")
	address = forms.CharField(label="Адрес дома")

	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
	passwordReInput = forms.CharField(label="Подтвердите", widget=forms.PasswordInput)
	
	email = forms.EmailField(label="Электронная почта", required=False)
	phone = forms.CharField(label="Номер телефона")
	avatar = forms.ImageField(label="Фото профиля", required=False)

	group = forms.IntegerField(label="Группа инвалидности", max_value=3, initial=0)
	childs = forms.IntegerField(label="Дети", initial=0)

class signinForms(forms.Form):
	login = forms.CharField(label="ФИО")
	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)