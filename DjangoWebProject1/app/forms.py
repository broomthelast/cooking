"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.db import models
from .models import Comment
from .models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Имя пользователя",
        min_length=3 
    )
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3 or len(username) > 150:
            self.add_error('username', "Имя пользователя должно содержать от 3 до 150 символов.")
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Это имя пользователя уже занято.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        allowed_domains = ['@gmail.com', '@mail.ru', '@yandex.ru']
        if not any(domain in email for domain in allowed_domains):
            self.add_error('email', "Пожалуйста, используйте адрес электронной почты с доменом @gmail.com, @mail.ru или @yandex.ru.")

        if User.objects.filter(email=email).exists():
            self.add_error('email', "Этот адрес электронной почты уже зарегистрирован.")

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            self.add_error('password', "Пароль должен содержать не менее 8 символов.")
        if not any(char.isupper() for char in password):
            self.add_error('password', "Пароль должен содержать хотя бы одну букву верхнего регистра.")
        if not any(char.islower() for char in password):
            self.add_error('password', "Пароль должен содержать хотя бы одну букву нижнего регистра.")
        if not any(char.isdigit() for char in password):
            self.add_error('password', "Пароль должен содержать хотя бы одну цифру.")
        if not any(not char.isalnum() for char in password):
            self.add_error('password', "Пароль должен содержать хотя бы один специальный символ.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Пароли не совпадают.")

        return cleaned_data

class RatingFormCoolEdition(forms.Form):
    name = forms.CharField(
        label = 'Ваше имя (необязательно):',
        required=False,
        max_length=254,
        widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя:'}))

    age = forms.ChoiceField(
        label="Ваш возраст:",
        choices=[
            ('', 'Выберите возраст'),
            ('<18', '< 18 лет'),
            ('18-25', '18-25 лет'),
            ('26-35', '26-35 лет'),
            ('36-45', '36-45 лет'),
            ('46-55', '46-55 лет'),
            ('55+', '55+'),
        ],
        widget=forms.RadioSelect
    )

    gender = forms.ChoiceField(
        label="Ваш пол:",
        choices=[
            ('', 'Выберите пол'),
            ('male', 'Мужской'),
            ('female', 'Женский'),
            ('prefer_not_say', 'Предпочитаю не указывать'),
        ],
        widget=forms.RadioSelect
    )

    frequency = forms.ChoiceField(
        label="Как часто вы пользуетесь нашим веб-сайтом?",
        choices=[
            ('', 'Выберите частоту'),
            ('daily', 'Ежедневно'),
            ('weekly', 'Несколько раз в неделю'),
            ('monthly', 'Несколько раз в месяц'),
            ('rarely', 'Реже'),
            ('first_time', 'Впервые'),
        ],
        widget=forms.Select
    )

    liked_features = forms.MultipleChoiceField(
        label="Что вам больше всего нравится в нашем веб-сайте? (Можно выбрать несколько вариантов):",
        choices=[
            ('quality', 'Оформление'),
            ('price', 'Функционал'),
            ('usability', 'Удобство использования'),
            ('support', 'Поддержка пользователей'),
            ('other', 'Другое (пожалуйста, укажите в поле ниже)'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False 
    )

    other_liked_features_text = forms.CharField(
        label="Если выбрали 'Другое' в предыдущем вопросе, поясните:",
        widget=forms.TextInput(attrs={'placeholder': 'Введите пояснение'}),
        required=False
    )

    improvements = forms.CharField(
        label="Что бы вы хотели улучшить в нашем веб-сайте?",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40})
    )

    satisfaction = forms.IntegerField(
        label="Оцените, пожалуйста, уровень вашей удовлетворенности нашим веб-сайтом (от 1 до 5, где 1 - совсем не удовлетворен, а 5 - полностью удовлетворен):",
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5}),
        min_value=1,
        max_value=5
    )

    how_did_you_hear = forms.CharField(
        label="Как вы узнали о нас?",
        widget=forms.TextInput(attrs={'placeholder': 'Введите источник информации'})
    )

    recommend = forms.ChoiceField(
        label="Готовы ли вы рекомендовать наш веб-сайт своим друзьям и знакомым?",
        choices=[
            ('', 'Выберите вариант'),
            ('yes_definitely', 'Да, конечно'),
            ('yes_probably', 'Скорее да, чем нет'),
            ('unsure', 'Затрудняюсь ответить'),
            ('no_probably', 'Скорее нет, чем да'),
            ('no_definitely', 'Нет, ни в коем случае'),
        ],
        widget=forms.RadioSelect)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': 'Комментарий'} # метка к полю формы text


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'image']
