from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import RegisterForm, CustomPasswordResetForm, CustomSetPasswordForm, UserProfileForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from mainpage.models import Pet
from django.contrib.messages import get_messages
from django.shortcuts import redirect

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Kayıt başarılı! Hoş geldiniz.')
            return redirect('mainpage:pet_list')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('mainpage:pet_list')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    storage = get_messages(request)
    for _ in storage:
        pass
    logout(request)
    messages.info(request, 'Başarıyla çıkış yaptınız.')
    return redirect('accounts:login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = '/accounts/password_reset/done/'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/accounts/password_reset/complete/'

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Lütfen hataları düzeltin.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if 'remove_profile_picture' in request.POST:
            # Profil resmini sil
            if user_profile.profile_picture:
                user_profile.profile_picture.delete(save=False)
                user_profile.profile_picture = None
                user_profile.save()
            messages.success(request, 'Profil resminiz başarıyla kaldırıldı!')
            return redirect('accounts:profile')
        elif form.is_valid():
            # Kullanıcı bilgilerini güncelle
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            if new_username:
                request.user.username = new_username
            if new_email:
                request.user.email = new_email
            request.user.save()

            # Profil bilgilerini güncelle
            user_profile.contact_number = form.cleaned_data.get('contact_number', user_profile.contact_number)
            if form.cleaned_data['profile_picture']:
                user_profile.profile_picture = form.cleaned_data['profile_picture']
            user_profile.save()

            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Lütfen hataları düzeltin.')
    else:
        form = UserProfileForm(instance=user_profile)

    pets = Pet.objects.filter(owner=request.user)

    context = {
        'form': form,
        'user': request.user,
        'pets': pets,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/profile.html', context)