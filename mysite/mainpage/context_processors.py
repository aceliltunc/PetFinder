from accounts.models import UserProfile  # UserProfile modelini senin kullandığın isme göre değiştir

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
    else:
        profile = None

    return {'user_profile': profile}
