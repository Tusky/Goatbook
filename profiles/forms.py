from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from profiles.models import Profile

class RegistrationForm(ModelForm):
    first_name  = forms.CharField(label=(u'First Name'))
    last_name   = forms.CharField(label=(u'Last Name'))
    username    = forms.CharField(label=(u'User Name'))
    email       = forms.EmailField(label=(u'Email'))
    password    = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1   = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
                                'first_name',
                                'last_name',
                                'birth_date',
                                'countries',
                                'username',
                                'email',
                                'password',
                                'password1',
                                'profile_pic',
                                'about_me',
                                ]

    class Meta:
        model = Profile
        exclude = ('user','friends')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('That username is taken.')

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('The passwords does not match!')
        return self.cleaned_data

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'Username'), widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False,attrs={'placeholder': 'Password'}))

class EditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','friends')

