from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import UserProfile
import re
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return password2

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="E-posta", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Yeni Şifre", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password2 = forms.CharField(label="Yeni Şifreyi Tekrarla", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'contact_number']
        widgets = {
            'profile_picture': forms.FileInput(),
        }
    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if not contact_number:
            return contact_number  

        
        phone_pattern = re.compile(r'^05\d{2}-\d{3}-\d{4}$')

        if phone_pattern.match(contact_number):
            contact_number = re.sub(r'\D', '', contact_number)
            return f"05{contact_number[2:4]}-{contact_number[4:7]}-{contact_number[7:]}"
        else:
            raise forms.ValidationError("Lütfen geçerli bir telefon numarası girin (Örn: 05xx-xxx-xxxx).")
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            return email
        if '@' not in email:
            raise forms.ValidationError("Lütfen geçerli bir e-posta adresi girin.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            return username
        if len(username) < 3:
            raise forms.ValidationError("Kullanıcı adı en az 3 karakter olmalıdır.")
        return username