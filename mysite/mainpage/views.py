from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Pet, AdoptionRequest, PetSighting, Message,Tag
from .forms import PetForm, AdoptionRequestForm,PetSightingForm
from django.db.models import Q,Max
from django.http import JsonResponse
from django.utils import timezone

def pet_search(request):
    query_name = request.GET.get('name', '')
    query_species = request.GET.get('species', '')
    query_age = request.GET.get('age', '')

    pets = Pet.objects.filter(status='Lost')

    if query_name:
        pets = pets.filter(name__icontains=query_name)
    if query_species:
        pets = pets.filter(species__icontains=query_species)
    if query_age:
        pets = pets.filter(age=query_age)

    return render(request, 'mainpage/pet_search.html', {
        'pets': pets,
        'name': query_name,
        'species': query_species,
        'age': query_age,
    })

# Tüm kayıp hayvan ilanlarını listele
def pet_list(request):
    pets = Pet.objects.filter(status='Lost').order_by('-date_reported')
    return render(request, 'mainpage/pet_list.html', {'pets': pets})

# Detay sayfası
@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    # Sadece sahibi görsün
    sightings = pet.sightings.all().order_by('-date_seen') if request.user == pet.owner else None

    return render(request, 'mainpage/pet_detail.html', {
        'pet': pet,
        'sightings': sightings,
    })

# Yeni kayıp bildirimi oluştur
@login_required
def pet_report(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()          # Önce kaydet
            form.save_m2m()     # Sonra ManyToMany ilişkileri kaydet
            return redirect('mainpage:pet_detail', pk=pet.pk)
    else:
        form = PetForm()
    return render(request, 'mainpage/pet_form.html', {'form': form})


# Güncelleme
@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('mainpage:pet_detail', pk=pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'mainpage/pet_form.html', {'form': form})

# Silme
@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        return redirect('mainpage:pet_list')
    return render(request, 'mainpage/pet_confirm_delete.html', {'pet': pet})

import csv
from io import TextIOWrapper
from .forms import CSVImportForm

@login_required
def import_pets(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='windows-1254')
            reader = csv.DictReader(csv_file)

            for row in reader:
                Pet.objects.create(
                    name=row['name'],
                    species=row['species'],
                    breed=row['breed'],
                    age=int(row['age']),
                    gender=row['gender'],
                    description=row['description'],
                    status=row['status'],
                    owner=request.user,
                    # image alanı göz ardı ediliyor
                )
            return redirect('mainpage:pet_list')
    else:
        form = CSVImportForm()
    return render(request, 'mainpage/import_pets.html', {'form': form})


from django.http import HttpResponse

@login_required
def export_pets(request):
    pets = Pet.objects.filter(owner=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_pets.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'species', 'breed', 'age', 'gender', 'description', 'status'])

    for pet in pets:
        writer.writerow([
            pet.name,
            pet.species,
            pet.breed,
            pet.age,
            pet.gender,
            pet.description,
            pet.status,
        ])

    return response
#Kayıp hayvanı gördüm bildirimi
@login_required
def report_pet_sighting(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetSightingForm(request.POST, request.FILES, pet=pet, reporter=request.user)
        if form.is_valid():
            form.save()
            return redirect('mainpage:pet_detail', pk=pet_id)
        else:
            print(form.errors)  # Hataları görmek için
    else:
        form = PetSightingForm(pet=pet, reporter=request.user)

    return render(request, 'mainpage/report_sighting.html', {'form': form, 'pet': pet})


#hayvanı gören ve sahibi arasında chat bölümü
@login_required
def start_chat(request, user_id):
    receiver = get_object_or_404(User, pk=user_id)
    room_name = f"chat_{min(request.user.id, receiver.id)}_{max(request.user.id, receiver.id)}"

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            timestamp = timezone.now()  # Zaman damgasını burada oluştur
            Message.objects.create(sender=request.user, receiver=receiver, content=content, timestamp=timestamp)
            return redirect('mainpage:start_chat', user_id=receiver.id)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'mainpage/chat.html', {
        'receiver': receiver,
        'messages': messages,
        'room_name': room_name,
    })

def get_new_messages(request, user_id):
    receiver = get_object_or_404(User, pk=user_id)
    last_timestamp_str = request.GET.get('last_timestamp', None)
    last_timestamp = None
    if last_timestamp_str:
        try:
            last_timestamp = timezone.datetime.fromisoformat(last_timestamp_str.replace(' ', 'T'))  # ' ' yerine 'T' koy
        except ValueError:
            # Eğer hala hata varsa, daha fazla temizlik yapabilirsiniz veya None olarak bırakabilirsiniz
            last_timestamp = None

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    if last_timestamp:
        messages = messages.filter(timestamp__gt=last_timestamp)

    new_messages = [{
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages]
    return JsonResponse({'messages': new_messages})


#Chat list
@login_required
def chat_list(request):
    # En son mesajlaşan kullanıcıları bul
    subquery = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').annotate(
        latest_timestamp=Max('timestamp')
    ).order_by('-latest_timestamp')

    user_ids = set()
    for item in subquery:
        user_ids.add(item['sender'])
        user_ids.add(item['receiver'])
    user_ids.discard(request.user.id)  # Kendimizi listeden çıkar

    users = User.objects.filter(id__in=user_ids)

    last_messages = {}
    for user in users:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        if last_message:
            last_messages[user] = last_message
    print("last_messages:", last_messages)  # Bunu ekleyin!
    return render(request, 'mainpage/chat_list.html', {'users': users, 'last_messages': last_messages})

#admin paneli

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_views(request):
    return render(request, 'admin/panel.html') # Ana admin paneli sayfası (model listesi)

@staff_member_required
def admin_pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'admin/admin_pet_list.html', {'pets': pets})