from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.forms import PasswordChangeForm

# Register Forms
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('consumer', 'Consumer'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Register As")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'role', 'password', 'confirm_password', 'mobile', 'village', 'district', 'state']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        # Set role flags
        if role == 'farmer':
            user.is_farmer = True
            user.is_consumer = False
        elif role == 'consumer':
            user.is_consumer = True
            user.is_farmer = False

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user
    

class loginform(forms.Form):
    username=forms.CharField(label='username')
    password=forms.CharField(label='Password',widget=forms.PasswordInput)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']



class Password_change_form(PasswordChangeForm):
    old_password=forms.CharField(label='Current Password',widget=forms.PasswordInput)
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput)
    confirm_password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)