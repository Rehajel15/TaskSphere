from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import CustomUser

# Profile Extra Form
class ProfilePicform(forms.ModelForm):
	profile_image = forms.ImageField(label="Profile picture")

	class Meta:
		model = CustomUser
		fields = ('profile_image',)


class SignUpForm(UserCreationForm):
	firstname = forms.CharField(label="Firstname", max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Firstname',}))
	lastname = forms.CharField(label="Lastname", max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lastname',}))
	biography = forms.CharField(label="Biography", required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'I am using TaskSphere', 'rows': '4'}))

	class Meta:
		model = CustomUser
		fields = ('email', 'password1', 'password2', 'firstname', 'lastname', 'biography')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['placeholder'] = 'example@myemail.com'
		self.fields['email'].label = 'Email address'
		self.fields['email'].widget.attrs['required'] = 'required'
		self.fields['email'].help_text = '<span class="form-text text-white-50"><small>Your email is only visible for people in your group.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = ''
		self.fields['password1'].label = 'Password'
		self.fields['password1'].help_text = '<ul class="form-text text-white-50 small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-white-50"><small>Enter the same password as before, for verification.</small></span>'