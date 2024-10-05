from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import CustomUser
from home.models import Group

class SignUpForm(UserCreationForm):
    firstname = forms.CharField(
        label="Firstname", 
        max_length=20, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-6', 
            'placeholder': 'Firstname',
        }),

    )

    lastname = forms.CharField(
        label="Lastname", 
        max_length=20, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-6',  
            'placeholder': 'Lastname',
        }),
        
    )
    biography = forms.CharField(
        label="Biography",
        max_length=250,
        required=False, 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'I am using TaskSphere', 
            'rows': '4',
        }),
    )

    profile_picture = forms.ImageField(
        max_length=30,
        label="Profile picture",
        help_text = '<br> <span class="form-text text-white-50">Allowed file formats: .png and .jpg</span>',
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'firstname', 'lastname', 'biography', 'profile_picture',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'example@myemail.com'
        self.fields['email'].label = 'Email address'
        self.fields['email'].widget.attrs['required'] = 'required'
        self.fields['email'].help_text = '<span class="form-text text-white-50">Your email is only visible for people in your group.</span>'
        self.fields['email'].max_length = 30,
    

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = ''
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '<ul class="form-text text-white-50"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'


        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-white-50">Enter the same password as before, for verification.</span>'
    
	