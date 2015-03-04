# coding: utf8
from .models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField, Form, PasswordInput, EmailField

# Допиливаем форму добавления пользователя. В Meta.model указываем нашу модель.
# Поля указывать нет необходимости т.к. они переопределяются в UserAdmin.add_fieldsets 
class AdminUserAddForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


# Допиливаем форму редактирования пользователя. В Meta.model указываем нашу модель.
class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'


class RegistrationForm(Form):
    username = CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'class': 'name', 'placeholder': 'Username','name':'username'}),
        error_messages={'required': 'Enter username'})
    email = EmailField(
        max_length=100,
        label='',
        widget=forms.EmailInput(attrs={'class': 'email', 'placeholder': 'Email','name':'email'}),
        error_messages={'required': 'Enter email address'})
    password1 = CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'name', 'placeholder': 'Password','name':'password1'}),
        error_messages={'required': 'Enter password'})
    password2 = CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'name', 'placeholder': 'Confirm password','name':'password2'}),
        error_messages={'required': 'Confirm password'})
    def clean_username(self):
        data = self.cleaned_data
        try:
            User.objects.get(username = data['username'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This username is already taken.')

    def clean_email(self):
        data = self.cleaned_data
        try:
            User.objects.get(email = data['email'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This email is already registered.')
    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords must be same!')
        return self.cleaned_data
